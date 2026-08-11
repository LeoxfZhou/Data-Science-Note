---
title: PyTorch 数据集、变换与加载器（PyTorch Datasets, Transforms, and DataLoaders）
aliases:
  - PyTorch Data Pipeline
tags:
  - data-science/deep-learning/pytorch
  - data-science/data-pipeline
status: published
created: 2026-08-11
published_at: 2026-08-11
---
# PyTorch 数据集、变换与加载器（PyTorch Datasets, Transforms, and DataLoaders）
## 1. 数据管线职责（Data Pipeline Responsibilities）
- 数据集（Dataset）负责定义“有哪些样本”和“如何读取一个样本”。
- 变换（Transform）负责解码、缩放、类型转换、归一化（Normalization）和随机数据增强（Data Augmentation）。
- 数据加载器（DataLoader）负责采样（Sampling）、批处理（Batching）、整理（Collation）、多进程预取和内存固定（Memory Pinning）。
- 一条典型路径是：磁盘文件与标注 → `Dataset.__getitem__()` → Transform → 单样本张量 → `DataLoader` 批次 → 迁移到模型设备。
- 训练和推理必须共享确定性预处理，例如颜色通道、尺寸、数值范围和归一化参数；随机翻转、旋转、随机裁剪等训练增强通常不在推理阶段执行。
## 2. 自定义数据集（Custom Dataset）
### 2.1 映射式数据集（Map-style Dataset）
- 继承 `torch.utils.data.Dataset` 的常见类实现三个方法：
  - `__init__()`：保存路径与配置，读取或建立文件名和标签索引。
  - `__len__()`：返回可索引样本总数。
  - `__getitem__(index)`：读取一个样本，执行变换并返回数据与标签。
- `__getitem__()` 不应依赖隐藏的全局状态；多进程加载时，每个 worker 持有 Dataset 副本。
- 文件列表应排序或由标注明确决定顺序，避免不同文件系统遍历顺序造成标签错位。
```python
from pathlib import Path
from typing import Callable

from PIL import Image
from torch import Tensor
from torch.utils.data import Dataset


class ImageClassificationDataset(Dataset[tuple[Tensor, int]]):
    def __init__(
        self,
        image_paths: list[Path],
        labels: list[int],
        transform: Callable[[Image.Image], Tensor],
    ) -> None:
        if len(image_paths) != len(labels):
            # 文件与标签错位会静默污染训练，因此在入口立即拒绝。
            raise ValueError("image_paths and labels must have the same length")
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, index: int) -> tuple[Tensor, int]:
        path = self.image_paths[index]
        # 统一为 RGB 可避免灰度图或带 Alpha 通道图片造成通道数不一致。
        with Image.open(path) as image:
            image = image.convert("RGB")
            tensor = self.transform(image)
        return tensor, self.labels[index]
```
该示例读取磁盘图片，属于文件 I/O（File I/O），输出取决于实际文件，因此不附固定 Output。
### 2.2 `ImageFolder`
- `torchvision.datasets.ImageFolder(root, transform=...)` 适合 `root/class_name/image.ext` 目录结构，文件夹名决定类别。
- `dataset.classes` 给出按内部规则排序的类别名称；`class_to_idx` 保存名称到整数标签的映射。部署时必须保存或重建完全相同的映射，否则预测类别会错位。
- 它不能替代复杂标注读取；目标检测、多标签或自定义元数据通常需要自定义 Dataset。
## 3. 图像变换（Image Transforms）
### 3.1 训练变换与推理变换（Training and Inference Transforms）
- 训练变换可包含随机水平翻转、随机垂直翻转、随机旋转、随机裁剪和亮度/对比度扰动，以增加样本多样性。
- 推理变换只保留确定性的颜色转换、缩放、张量与类型转换、归一化；否则同一输入可能产生不同预测。
- 垂直翻转并非所有任务都保持标签语义，例如行人、文字和道路场景通常不应随意上下颠倒。
- Resize 到固定尺寸可能改变纵横比；需要保留几何比例时可采用短边缩放、填充（Padding）或任务特定策略。
### 3.2 torchvision v2 推荐写法（Recommended torchvision v2 Style）
- 当前 torchvision 文档推荐 `torchvision.transforms.v2`；它可以同步处理图像、边界框（Bounding Box）、掩码（Mask）、视频和关键点（Keypoint）。
- `v2.ToImage()` 只转换表示，不缩放像素值；`v2.ToDtype(torch.float32, scale=True)` 把整数图像转换为浮点并按类型范围缩放到 `[0,1]`。
- `v2.Normalize(mean, std)` 按通道执行 $(x-mean)/std$，其 mean/std 必须与模型训练时一致。
```python
import torch
from torchvision.transforms import v2

train_transform = v2.Compose([
    v2.Resize((256, 256), antialias=True),
    v2.RandomHorizontalFlip(p=0.5),
    v2.RandomRotation(degrees=10),
    v2.ToImage(),
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])

inference_transform = v2.Compose([
    v2.Resize((256, 256), antialias=True),
    v2.ToImage(),
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])
```
### 3.3 v1 `transforms` 行为（Legacy v1 Transforms）
- 原稿的 `transforms.Compose()`、`Resize()`、`RandomHorizontalFlip()`、`RandomVerticalFlip()`、`RandomRotation()`、`ToTensor()` 和 `Normalize()` 仍广泛存在。
- v1 `ToTensor()` 对常见 `uint8` PIL/NumPy 图像通常转换为 `float32` 并缩放到 `[0,1]`；对其他输入模式或 dtype 不应盲目假设缩放行为。
- 原稿通过 `transforms.Lambda(lambda image: image.convert("RGB"))` 做通道防御。lambda 在需要序列化、TorchScript 或多进程 spawn 的环境中可移植性较差，优先在 Dataset 中显式 `convert("RGB")` 或定义顶层可调用对象。
### 3.4 Albumentations
- Albumentations 常用于高性能图像增强，并能同步变换图像、分割掩码和边界框。
- `A.Compose([...])` 接受命名输入，通常通过 `transform(image=image_array)["image"]` 取结果。
- 边界框任务必须配置坐标格式、标签字段和裁剪后的合法框过滤；只变换图像而不变换标注会产生错误训练数据。
```python
import albumentations as A
from albumentations.pytorch import ToTensorV2

albu_transform = A.Compose([
    A.RandomCrop(width=256, height=256),
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.2),
    ToTensorV2(),
])

# transformed = albu_transform(image=image_array)
# image_tensor = transformed["image"]
```
该示例只定义变换；输出依赖输入图像与随机采样。
## 4. 音频变换（Audio Transform）
- `torchaudio.transforms.MelSpectrogram` 把波形转换为梅尔频谱图（Mel Spectrogram）。
- **sample_rate**：输入音频采样率；若真实采样率不同，应先重采样。
- **n_fft**：短时傅里叶变换（Short-time Fourier Transform, STFT）的 FFT 长度；影响频率分辨率和时间窗口。
- **n_mels**：梅尔滤波器组数量，决定输出频率轴大小。
```python
import torchaudio

audio_transform = torchaudio.transforms.MelSpectrogram(
    sample_rate=16_000,
    n_fft=400,
    n_mels=128,
)
```
该代码只定义变换，不读取音频，因此没有控制台输出。
## 5. DataLoader 参数（DataLoader Parameters）

|参数（Parameter）|作用（Purpose）|关键边界（Important Boundary）|
|---|---|---|
|`dataset`|提供样本的数据集|支持映射式和迭代式数据集|
|`batch_size`|每批样本数|最后一批可能更小|
|`shuffle`|每个 epoch 重排索引|与显式 `sampler` 互斥|
|`num_workers`|数据加载子进程数；0 表示主进程|不是固定设为 CPU 核心数一半；应实测吞吐、内存和平台行为|
|`collate_fn`|把样本列表整理为批次|变长序列、检测框和自定义对象常需自定义|
|`pin_memory`|把返回张量放入固定页内存|主要帮助 CPU→CUDA 传输；自定义批对象需实现 `pin_memory()`|
|`drop_last`|丢弃不完整尾批次|会丢样本；对 `IterableDataset` 多 worker 时可丢每个 worker 的尾批次|
|`persistent_workers`|跨 epoch 保留 worker|减少重启开销，但增加长期资源占用|
|`prefetch_factor`|每个 worker 预取批次数|提高吞吐也会增加内存占用|
|`generator`|控制采样与 worker 基础种子|用于可复现性，但不能保证跨版本、跨硬件完全一致|

### 5.1 基本装配（Basic Assembly）
```python
from torch.utils.data import DataLoader, TensorDataset
import torch

dataset = TensorDataset(
    torch.arange(20).reshape(10, 2),
    torch.arange(10),
)
loader = DataLoader(
    dataset,
    batch_size=4,
    shuffle=False,
    num_workers=0,
    pin_memory=False,
    drop_last=False,
)
print([features.shape[0] for features, _ in loader])  # 输出: [4, 4, 2]
```
### 5.2 `drop_last` 与 BatchNorm（Drop-last and BatchNorm）
- 原稿称 `drop_last=True` 可以“防止 BatchNorm 报错”。更准确地说，训练态 `BatchNorm1d` 在某些输入布局下遇到只有一个统计样本的尾批次可能报错或无法估计方差；丢弃尾批次是一种规避手段，不是 DataLoader 的普遍必需设置。
- 如果每个样本仍包含多个空间位置，BatchNorm2d 的统计样本数不一定只有 1；应根据实际输入形状判断。
- 验证和测试通常不能随意 `drop_last=True`，否则指标漏算样本。
### 5.3 固定内存与异步传输（Pinned Memory and Non-blocking Transfer）
- CUDA 训练常组合 `pin_memory=True` 与 `tensor.to(device, non_blocking=True)`；是否提速取决于硬件、批次、预处理和传输是否真正与计算重叠。
- 不建议让多进程 DataLoader 直接返回 CUDA 张量；官方文档推荐 worker 返回 CPU 张量，再用固定内存迁移。
## 6. 多进程与可复现性（Multiprocessing and Reproducibility）
### 6.1 平台差异（Platform Differences）
- Windows 与 macOS 常使用 spawn 启动 worker；程序入口应放在 `if __name__ == "__main__":` 下。
- Dataset、自定义 `collate_fn` 和 `worker_init_fn` 应定义在模块顶层，不能使用不可序列化的局部 lambda。
- worker 会复制父进程中访问到的 Python 对象；巨大文件名列表与大量 worker 可能放大内存占用。
### 6.2 worker 随机种子（Worker Random Seeds）
```python
import random
import numpy as np
import torch
from torch.utils.data import DataLoader


def seed_worker(worker_id: int) -> None:
    del worker_id  # worker seed 已由 PyTorch 根据 worker id 派生。
    worker_seed = torch.initial_seed() % (2**32)
    np.random.seed(worker_seed)
    random.seed(worker_seed)


generator = torch.Generator().manual_seed(0)
# loader = DataLoader(
#     dataset,
#     batch_size=32,
#     num_workers=4,
#     worker_init_fn=seed_worker,
#     generator=generator,
# )
```
- 固定种子只能限制特定环境中的随机来源；PyTorch 不保证跨版本、平台、CPU/GPU 的完全可复现。
## 7. 自定义整理函数（Custom Collation）
- 默认 `collate_fn` 会堆叠形状一致的张量。
- 变长文本可在批次内 padding 并返回原长度或 attention mask；目标检测可保留每个样本不同数量的框。
```python
import torch
from torch.nn.utils.rnn import pad_sequence


def collate_sequences(batch: list[tuple[torch.Tensor, int]]) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    sequences, labels = zip(*batch)
    lengths = torch.tensor([len(sequence) for sequence in sequences])
    padded = pad_sequence(sequences, batch_first=True)
    return padded, lengths, torch.tensor(labels)
```
## 8. 排错清单（Troubleshooting Checklist）
- 标签与样本错位：检查文件排序、标注主键和类别映射。
- 训练与推理结果差异异常：逐项比较 RGB/灰度、尺寸、数值范围、mean/std 和随机增强。
- worker 卡死或重复执行：检查 `__main__` 防护、顶层定义和 Dataset 中不可序列化对象。
- 内存快速增长：降低 `num_workers`、预取批次数和父进程 Python 对象规模。
- GPU 等待数据：先分析数据加载耗时，再尝试 worker、固定内存、批次大小和更高效解码；不要机械套用 CPU 核心比例。
- 检测标注错位：确认图像增强同步更新边界框、掩码和关键点。
## 参考资料（References）
- [PyTorch 数据加载官方文档](https://docs.pytorch.org/docs/stable/data.html)
- [torchvision v2 变换官方文档](https://docs.pytorch.org/vision/stable/transforms.html)
- [PyTorch 可复现性官方说明](https://docs.pytorch.org/docs/stable/notes/randomness.html)
