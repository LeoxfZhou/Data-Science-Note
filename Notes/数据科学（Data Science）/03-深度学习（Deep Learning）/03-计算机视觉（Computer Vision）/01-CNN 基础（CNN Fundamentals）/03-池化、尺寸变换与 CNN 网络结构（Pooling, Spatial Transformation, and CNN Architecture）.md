---
title: 池化、尺寸变换与 CNN 网络结构（Pooling, Spatial Transformation, and CNN Architecture）
tags:
  - data-science/deep-learning/computer-vision/pooling
  - pytorch/nn
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# 池化、尺寸变换与 CNN 网络结构（Pooling, Spatial Transformation, and CNN Architecture）
## 1. 池化层（Pooling Layer）
池化层对每个输入通道的局部空间窗口执行固定聚合，用于下采样（Downsampling）或把可变空间尺寸映射为固定输出尺寸。它通常不混合通道，因此输入、输出通道数相同，也没有可学习权重和偏置。
### 1.1 主要作用与边界
- **降低空间分辨率（Spatial Resolution）**：减小后续层的计算量、内存占用和全连接层参数量。
- **扩大后续单元的有效感受野（Effective Receptive Field）**：下采样后，一个后续位置对应原输入更大的区域。
- **提供局部稳定性（Local Stability）**：小幅位移若没有改变池化窗口内的主响应，输出可能保持接近。
- **信息筛选（Information Selection）**：最大池化保留窗口最大响应，平均池化保留平均水平。
- **正则化副作用（Regularizing Side Effect）**：降维可能降低模型容量，但不能单独保证防止过拟合。
> [!tip] 大白话理解（Plain-language Intuition）
> 池化是在一小块特征里做摘要：最大池化只记“这里最强的信号有多强”，平均池化记“这里整体平均有多强”。摘要更省空间，但被丢掉的位置细节无法自动恢复。
> [!warning] 不变性（Invariance）不是绝对保证
> 池化可使特征对部分小位移更稳定，但窗口边界、步长和混叠都可能使一个像素的移动导致输出改变。旋转、缩放不变性更不能由普通池化单独保证。
### 1.2 常见类型
- **最大池化（Max Pooling）**：输出窗口最大值；常用于保留显著边缘或纹理响应。反向传播时，梯度只流向被选中的最大值位置；并列最大值的具体梯度路由由实现定义。
- **平均池化（Average Pooling）**：输出窗口平均值；更平滑地保留整体背景或响应强度，但可能削弱尖锐高频特征。
- **全局平均池化（Global Average Pooling, GAP）**：把每个通道的全部 `H × W` 位置平均为 `1 × 1`；常在分类头前替代大型全连接空间展开。
- **自适应池化（Adaptive Pooling）**：用户指定最终输出尺寸，框架根据输入尺寸划分池化区域，适合可变分辨率输入。
## 2. 输出尺寸（Output Shape）
对 `MaxPool2d` 的每个空间维度：
$$
H_{out}=\left\lfloor\frac{H_{in}+2P_H-D_H(K_H-1)-1}{S_H}+1\right\rfloor
$$
`ceil_mode=True` 时允许部分右侧或下侧窗口，并按官方定义使用向上取整规则。对无空洞的 `AvgPool2d`，通常取 $D=1$。
- `kernel_size`：池化窗口大小。
- `stride`：默认通常等于 `kernel_size`；可显式指定。
- `padding`：边界填充。
- `dilation`：最大池化采样点间距。
> [!tip] 大白话理解（Plain-language Intuition）
> 尺寸公式是在数“窗口一共能合法放几次”。填充让可放置范围变大，核和空洞让窗口有效跨度变大，步长决定每次跳多远。
## 3. PyTorch 池化 API
### 3.1 `nn.MaxPool2d`
```python
torch.nn.MaxPool2d(
    kernel_size,
    stride=None,
    padding=0,
    dilation=1,
    return_indices=False,
    ceil_mode=False,
)
```
- 边界填充在概念上使用负无穷（Negative Infinity），避免补边值错误成为最大值。
- `return_indices=True` 同时返回最大值索引，可用于 `MaxUnpool2d` 等需要位置线索的操作。
- `ceil_mode=True` 可让部分边缘窗口参与输出，但需要重新核对输出尺寸。
### 3.2 `nn.AvgPool2d`
```python
torch.nn.AvgPool2d(
    kernel_size,
    stride=None,
    padding=0,
    ceil_mode=False,
    count_include_pad=True,
    divisor_override=None,
)
```
- `count_include_pad=True`：补入的零计入平均值分母，边缘平均值可能因此变小。
- `count_include_pad=False`：分母只计算有效输入元素。
- `divisor_override`：用指定除数替代默认窗口元素计数；需确保数学含义符合任务。
### 3.3 自适应池化（Adaptive Pooling）
```python
from torch import nn

adaptive_max = nn.AdaptiveMaxPool2d((7, 7))
global_average = nn.AdaptiveAvgPool2d((1, 1))
```
自适应池化保证输出尺寸，不要求用户针对每个输入尺寸手工指定固定核和步长。其区域划分可能重叠或大小不完全相同，不能简单等同于某个固定核池化。
## 4. 单通道与多通道池化示例
```python
import torch
from torch import nn

single_channel = torch.tensor(
    [[[0, 1, 2], [3, 4, 5], [6, 7, 8]]],
    dtype=torch.float32,
)

maximum = nn.MaxPool2d(kernel_size=2, stride=1)(single_channel)
average = nn.AvgPool2d(kernel_size=2, stride=1)(single_channel)
print(maximum)
print(average)

# 期望输出:
# tensor([[[4., 5.],
#          [7., 8.]]])
# tensor([[[2., 3.],
#          [5., 6.]]])
```
```python
multi_channel = torch.tensor(
    [
        [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
        [[10, 20, 30], [40, 50, 60], [70, 80, 90]],
        [[11, 22, 33], [44, 55, 66], [77, 88, 99]],
    ],
    dtype=torch.float32,
)
pooled = nn.MaxPool2d(kernel_size=2, stride=1)(multi_channel)
print(pooled.shape)  # 输出: torch.Size([3, 2, 2])
print(pooled)

# 期望输出:
# tensor([[[ 4.,  5.],
#          [ 7.,  8.]],
#         [[50., 60.],
#          [80., 90.]],
#         [[55., 66.],
#          [88., 99.]]])
```
省略批次维度时，PyTorch 也可接受 `[C, H, W]`；训练中更常见的输入是 `[N, C, H, W]`。
## 5. 基础 CNN 网络拓扑（Basic CNN Architecture）
典型分类网络按以下职责组合：
1. 卷积块（Convolution Block）：`Conv2d → BatchNorm2d → ReLU`。
2. 空间下采样（Spatial Downsampling）：`MaxPool2d` 或带步长卷积。
3. 重复卷积块：空间尺寸逐步降低、通道数逐步增加。
4. 自适应池化（Adaptive Pooling）：把可变输入统一到固定空间尺寸。
5. 分类头（Classifier Head）：`Flatten → Linear → Activation → Dropout → Linear`，输出未归一化分数（Logits）。
### 5.1 可变分辨率的标准模板
```python
import torch
from torch import nn


class StandardCNN(nn.Module):
    def __init__(self, num_classes: int = 10) -> None:
        super().__init__()
        self.feature_extractor = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        # 输出固定为 4×4，因此 Linear 的输入维度不依赖原始 H/W。
        self.spatial_adapter = nn.AdaptiveAvgPool2d((4, 4))
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 4 * 4, 128),
            nn.ReLU(),
            nn.Dropout(p=0.5),
            nn.Linear(128, num_classes),
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        features = self.feature_extractor(inputs)
        fixed_size_features = self.spatial_adapter(features)
        return self.classifier(fixed_size_features)


model = StandardCNN(num_classes=10)
model.eval()  # 关闭 Dropout 随机性并使用 BN 的运行统计量。
with torch.inference_mode():
    first = model(torch.randn(4, 3, 32, 32))
    second = model(torch.randn(2, 3, 48, 48))
print(first.shape)   # 输出: torch.Size([4, 10])
print(second.shape)  # 输出: torch.Size([2, 10])
```
- 输出是 Logits；若训练使用 `CrossEntropyLoss`，不要在模型末尾先应用 Softmax。
- `AdaptiveAvgPool2d((4, 4))` 是固定尺寸自适应平均池化，不是 GAP；GAP 应使用 `(1, 1)`。
- 激活、初始化与 Dropout 的完整原理见关联笔记。
## 6. 下采样的工程取舍（Engineering Trade-offs）

|方法|优点|代价与风险|
|---|---|---|
|最大池化（Max Pooling）|突出局部强响应，无学习参数|丢失非最大位置；梯度路径稀疏|
|平均池化（Average Pooling）|平滑聚合局部信息|可能削弱边缘和小目标响应|
|带步长卷积（Strided Convolution）|下采样方式可学习并可同时改变通道|增加参数；仍需处理混叠|
|全局平均池化（GAP）|大幅减少分类头参数，支持可变空间尺寸|丢失绝对空间布局|
|自适应池化（Adaptive Pooling）|明确控制最终尺寸|区域划分行为需理解；不能恢复已丢失细节|
## 7. 轻量化：深度可分离卷积（Depthwise Separable Convolution）
标准卷积同时聚合空间和通道；深度可分离卷积拆为：
1. **深度卷积（Depthwise Convolution）**：逐输入通道独立执行空间卷积。
2. **逐点卷积（Pointwise Convolution）**：使用 `1 × 1` 卷积混合通道。
设输入通道 $M$、输出通道 $N$、卷积核 $D_K × D_K$、输出空间 $D_F × D_F$：
$$
\text{Cost}_{standard}=D_K^2MND_F^2
$$
$$
\text{Cost}_{separable}=D_K^2MD_F^2+MND_F^2
$$
$$
\frac{\text{Cost}_{separable}}{\text{Cost}_{standard}}=\frac{1}{N}+\frac{1}{D_K^2}
$$
当使用 `3 × 3` 核且输出通道较多时，该比值接近 $1/9$；实际速度还受硬件、内存访问、算子融合和张量尺寸影响，不能只由 FLOPs 比值保证。
> [!tip] 大白话理解（Plain-language Intuition）
> 标准卷积一次完成“每个通道看周围”和“不同通道互相交流”。深度可分离卷积把这两件事拆开：先各看各的，再用 `1 × 1` 开会交流，因此少做大量重复计算。
## 8. 相关正则化与初始化边界（Regularization and Initialization Boundaries）
- 全零初始化所有权重会使同层神经元保持对称，通常无法学出不同特征；偏置可以初始化为零。
- ReLU 网络常使用 He / Kaiming 初始化；Tanh 等激活常考虑 Xavier / Glorot 初始化。具体 fan 模式与非线性参数必须匹配实现。
- L1/L2 权重惩罚、权重衰减（Weight Decay）和 Dropout 可缓解某些过拟合，但不是互相等价的通用替代品。
- 反向 Dropout（Inverted Dropout）在训练时以保留概率缩放激活，推理时无需再次缩放。PyTorch 的 `Dropout(p)` 中 `p` 是丢弃概率，不是保留概率。
- 回归任务是否使用 Dropout、是否把问题离散化为分类，取决于目标语义、损失函数、校准需求和验证结果；不存在“回归中 L2 前绝对不能使用 Dropout”的普遍规则。
## 9. 关联笔记与参考资料（Related Notes and References）
- [[神经网络激活函数（Neural Network Activation Functions）]]
- [[神经网络参数初始化与梯度流（Neural Network Initialization and Gradient Flow）]]
- [[模型欠拟合、过拟合与泛化（Model Underfitting, Overfitting, and Generalization）]]
- [PyTorch `MaxPool2d` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)
- [PyTorch `AvgPool2d` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html)
- [PyTorch `AdaptiveAvgPool2d` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.AdaptiveAvgPool2d.html)
