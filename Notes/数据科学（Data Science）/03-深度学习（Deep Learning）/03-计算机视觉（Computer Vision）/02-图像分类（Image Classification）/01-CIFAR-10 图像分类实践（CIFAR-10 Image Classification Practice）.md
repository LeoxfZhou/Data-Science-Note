---
title: CIFAR-10 图像分类实践（CIFAR-10 Image Classification Practice）
tags:
  - data-science/deep-learning/computer-vision/image-classification
  - pytorch/torchvision
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# CIFAR-10 图像分类实践（CIFAR-10 Image Classification Practice）
## 1. 任务与数据集（Task and Dataset）
CIFAR-10 是 10 类彩色图像分类数据集：
- 训练集（Training Set）：50,000 张图像。
- 测试集（Test Set）：10,000 张图像。
- 图像大小：`32 × 32`，3 个颜色通道。
- 每类总计 6,000 张图像，其中训练集每类 5,000 张、测试集每类 1,000 张。
- 类别：airplane、automobile、bird、cat、deer、dog、frog、horse、ship、truck。
> [!tip] 大白话理解（Plain-language Intuition）
> 这是一个小而完整的 CNN 练习场：图片很小，能快速验证数据加载、卷积、训练、保存和评估的全流程；但它不能代表高分辨率真实业务的算力与泛化难度。
## 2. 环境与导入（Environment and Imports）
```python
from pathlib import Path
import time

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import CIFAR10

BATCH_SIZE = 128
NUM_WORKERS = 0  # Notebook 与跨平台教学环境先用 0，稳定后再调大。
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CHECKPOINT = Path("model/image_classification.pth")
```
- 安装包应优先使用项目锁定环境；临时安装可使用 `pip install torch torchvision`，但 CUDA 构建需按 PyTorch 官方安装页选择。
- `NUM_WORKERS` 最优值取决于操作系统、磁盘、CPU、Notebook 与启动方式。
## 3. 加载与检查数据（Load and Inspect Data）
### 3.1 基础转换（Basic Transform）
`ToTensor()` 将 PIL 图像或 NumPy 数组转换为 `[C, H, W]` 浮点张量，并把常见 `uint8` 值缩放到 `[0, 1]`。
```python
basic_transform = transforms.ToTensor()


def create_datasets(root: str = "data") -> tuple[CIFAR10, CIFAR10]:
    train_dataset = CIFAR10(
        root=root,
        train=True,
        transform=basic_transform,
        download=True,
    )
    test_dataset = CIFAR10(
        root=root,
        train=False,
        transform=basic_transform,
        download=True,
    )
    return train_dataset, test_dataset
```
下载与本地写入属于网络和文件 I/O 副作用，因此不附固定 Output。
### 3.2 数据集元数据
```python
train_dataset, test_dataset = create_datasets()
print(train_dataset.class_to_idx)
print(train_dataset.data.shape)  # 输出: (50000, 32, 32, 3)
print(test_dataset.data.shape)   # 输出: (10000, 32, 32, 3)

# class_to_idx 的期望输出:
# {'airplane': 0, 'automobile': 1, 'bird': 2, 'cat': 3, 'deer': 4,
#  'dog': 5, 'frog': 6, 'horse': 7, 'ship': 8, 'truck': 9}
```
直接访问 `.data` 和 `.targets` 适合教学检查；训练应通过 Dataset 接口取样，使 `transform` 正常执行。
## 4. 基线网络（Baseline Network）
原始基线形状流：
1. 输入：`[N, 3, 32, 32]`。
2. `Conv2d(3, 6, 3)`：`[N, 6, 30, 30]`。
3. `MaxPool2d(2, 2)`：`[N, 6, 15, 15]`。
4. `Conv2d(6, 16, 3)`：`[N, 16, 13, 13]`。
5. `MaxPool2d(2, 2)`：`[N, 16, 6, 6]`。
6. 展平：`[N, 576]`。
7. 全连接：`576 → 120 → 84 → 10`。
```python
class BaselineCNN(nn.Module):
    def __init__(self, num_classes: int = 10) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, kernel_size=3)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=3)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.linear1 = nn.Linear(16 * 6 * 6, 120)
        self.linear2 = nn.Linear(120, 84)
        self.output = nn.Linear(84, num_classes)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        features = self.pool1(torch.relu(self.conv1(inputs)))
        features = self.pool2(torch.relu(self.conv2(features)))
        # 保留批次维度；最后一个不完整批次也能正确展平。
        features = torch.flatten(features, start_dim=1)
        features = torch.relu(self.linear1(features))
        features = torch.relu(self.linear2(features))
        return self.output(features)


model = BaselineCNN()
with torch.inference_mode():
    logits = model(torch.randn(8, 3, 32, 32))
print(logits.shape)  # 输出: torch.Size([8, 10])
```
- 最后一层返回 Logits；`CrossEntropyLoss` 内部处理 Log-Softmax 与负对数似然，不要在模型末尾重复加 Softmax。
- 全连接输入维度绑定 `32 × 32` 输入；若要支持可变分辨率，可使用自适应池化。
## 5. 数据加载器（DataLoader）
```python
train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=NUM_WORKERS,
    pin_memory=torch.cuda.is_available(),
)
test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS,
    pin_memory=torch.cuda.is_available(),
)
```
- 训练集打乱（Shuffle）可减少固定顺序造成的批次偏差。
- 测试集不需要打乱，便于复现和逐样本分析。
- 最后一个批次可能小于 `BATCH_SIZE`，代码必须使用真实 `labels.size(0)` 计数。
## 6. 训练循环（Training Loop）
```python
def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> tuple[float, float]:
    model.train()
    loss_sum = 0.0
    correct = 0
    sample_count = 0

    for images, labels in loader:
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        # 默认梯度会累加；每个批次前必须清零。
        optimizer.zero_grad(set_to_none=True)
        logits = model(images)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()

        batch_size = labels.size(0)
        loss_sum += loss.item() * batch_size
        correct += (logits.argmax(dim=1) == labels).sum().item()
        sample_count += batch_size

    return loss_sum / sample_count, correct / sample_count


def train_model(
    model: nn.Module,
    train_loader: DataLoader,
    epochs: int = 100,
    learning_rate: float = 1e-3,
) -> None:
    model.to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(1, epochs + 1):
        start = time.perf_counter()
        train_loss, train_accuracy = train_one_epoch(
            model, train_loader, criterion, optimizer, DEVICE
        )
        duration = time.perf_counter() - start
        print(
            f"epoch={epoch:03d} loss={train_loss:.5f} "
            f"accuracy={train_accuracy:.2%} time={duration:.2f}s"
        )

    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), CHECKPOINT)
```
训练耗时和指标取决于设备、版本、初始化、数据顺序与超参数；保存检查点有文件 I/O 副作用，因此不附固定 Output。
### 6.1 原稿历史训练记录（Historical Training Record）
原稿记录基线模型使用 Adam、学习率 `1e-3`、训练 100 轮时：
- 第 1 轮：损失约 `1.59926`，训练准确率约 `0.41`。
- 第 5 轮：损失约 `1.09832`，训练准确率约 `0.61`。
- 第 96–100 轮：损失约 `0.29`–`0.31`，训练准确率约 `0.89`–`0.90`。
- 单轮耗时约 29–38 秒。
这些数值是来源运行记录，不是跨设备可复现的 Expected Output。
## 7. 测试与推理（Evaluation and Inference）
```python
def evaluate(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
) -> float:
    model.eval()
    correct = 0
    sample_count = 0

    # 关闭自动微分可减少推理内存与调度开销。
    with torch.inference_mode():
        for images, labels in loader:
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)
            logits = model(images)
            correct += (logits.argmax(dim=1) == labels).sum().item()
            sample_count += labels.size(0)

    return correct / sample_count
```
### 7.1 加载权重
```python
model = BaselineCNN().to(DEVICE)

# weights_only=True 限制反序列化范围；仍只应加载可信来源的检查点。
state_dict = torch.load(
    CHECKPOINT,
    map_location=DEVICE,
    weights_only=True,
)
model.load_state_dict(state_dict)
accuracy = evaluate(model, test_loader, DEVICE)
print(f"test accuracy: {accuracy:.2%}")  # 数值取决于实际检查点
```
- `map_location` 防止在无 GPU 环境加载 GPU 检查点失败。
- `model.eval()` 会切换 Dropout 与 BatchNorm 行为，但不会关闭梯度；评估函数仍使用 `inference_mode()`。
- 原稿历史基线测试准确率为 `0.57`，表示训练准确率约 `0.90` 时存在明显泛化差距。
## 8. 改进模型与过拟合分析（Improved Model and Overfitting Analysis）
原稿的改进方案把通道从 `6/16` 增加到 `32/128`，全连接隐藏层扩展到 `2048/2048`，加入两处 `Dropout(p=0.5)`，并把学习率从 `1e-3` 降到 `1e-4`：
```python
class WiderCNN(nn.Module):
    def __init__(self, num_classes: int = 10) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(32, 128, kernel_size=3)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.linear1 = nn.Linear(128 * 6 * 6, 2048)
        self.linear2 = nn.Linear(2048, 2048)
        self.output = nn.Linear(2048, num_classes)
        self.dropout = nn.Dropout(p=0.5)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        features = self.pool1(torch.relu(self.conv1(inputs)))
        features = self.pool2(torch.relu(self.conv2(features)))
        features = torch.flatten(features, start_dim=1)
        features = self.dropout(torch.relu(self.linear1(features)))
        features = self.dropout(torch.relu(self.linear2(features)))
        return self.output(features)


model = WiderCNN()
with torch.inference_mode():
    logits = model.eval()(torch.randn(4, 3, 32, 32))
print(logits.shape)  # 输出: torch.Size([4, 10])
```
> [!warning] 改进结果的归因边界（Attribution Boundary）
> 原稿记录测试准确率从 `0.57` 提升到 `0.93`，但没有完整日志、随机种子和数据预处理配置。扩大模型本身会增加容量并可能加剧过拟合；降低学习率与加入 Dropout 也不一定单独产生该提升。必须在固定数据划分和随机种子下做消融实验（Ablation Study），才能区分各改动贡献。
### 8.1 更可靠的改进顺序
1. **建立验证集（Validation Set）**：测试集只用于最终报告，避免反复调参造成测试泄漏。
2. **标准化（Normalization）**：用 CIFAR-10 训练集统计量标准化；若使用预训练模型，采用其指定变换。
3. **数据增强（Data Augmentation）**：随机裁剪、水平翻转等需只作用于训练集。
4. **结构改进（Architecture）**：考虑 BatchNorm、残差块、GAP 或更成熟的 CIFAR 架构，而不是只放大全连接层。
5. **正则化（Regularization）**：比较权重衰减、Dropout、标签平滑等，并记录配置。
6. **学习率调度（Learning-rate Scheduling）**：记录优化器、初始学习率、调度器、轮数和早停规则。
7. **可复现性（Reproducibility）**：固定随机种子，记录 PyTorch、torchvision、CUDA、硬件和数据版本。
> [!tip] 大白话理解（Plain-language Intuition）
> “训练集 90%，测试集 57%”表示模型很会做练习题，却不会做新题。解决方法不是盲目把网络做大，而是用验证集判断方向，再逐项检查数据增强、正则化、网络结构和学习率到底谁真正改善了新题表现。
## 9. 完整实验记录清单（Experiment Record Checklist）
- 数据集版本、下载校验与训练/验证/测试划分。
- 训练和评估变换（Transform）。
- 模型结构、参数量和输入尺寸。
- 损失函数、优化器、学习率、调度器、权重衰减。
- 批次大小、轮数、随机种子、设备与软件版本。
- 每轮训练与验证损失、准确率和耗时。
- 最佳检查点的选择标准，不能使用测试集选模型。
- 混淆矩阵、逐类准确率与典型错误样本。
- 检查点来源与可信性；不要反序列化不可信文件。
## 10. 参考资料（References）
- [torchvision `CIFAR10` 官方文档](https://docs.pytorch.org/vision/stable/generated/torchvision.datasets.CIFAR10.html)
- [[图像表示、预处理与 CNN 概览（Image Representation, Preprocessing, and CNN Overview）]]
- [[二维卷积、感受野与 Conv2d（2D Convolution, Receptive Field, and Conv2d）]]
- [[池化、尺寸变换与 CNN 网络结构（Pooling, Spatial Transformation, and CNN Architecture）]]
- [[模型欠拟合、过拟合与泛化（Model Underfitting, Overfitting, and Generalization）]]
