---
title: 二维卷积、感受野与 Conv2d（2D Convolution, Receptive Field, and Conv2d）
tags:
  - data-science/deep-learning/computer-vision/convolution
  - pytorch/nn
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# 二维卷积、感受野与 Conv2d（2D Convolution, Receptive Field, and Conv2d）
## 1. 二维卷积在神经网络中的含义
卷积层（Convolution Layer）用可学习的卷积核（Kernel / Filter）扫描输入的局部区域。每个输出位置是对应输入窗口与权重的逐元素乘积之和，再加偏置（Bias）。实践中的深度学习框架通常计算互相关（Cross-correlation），即不翻转卷积核；权重由训练自动学习，所以通常仍称为“卷积”。
对于输入 $X$、权重 $W$ 和偏置 $b$，忽略批次并用二维索引表示时：
$$
Y_{c_{out},i,j}=b_{c_{out}}+\sum_{c=0}^{C_{in}-1}\sum_{u=0}^{K_H-1}\sum_{v=0}^{K_W-1}W_{c_{out},c,u,v}X_{c,iS_H+uD_H-P_H,jS_W+vD_W-P_W}
$$
- $C_{in}$、$C_{out}$：输入、输出通道数（Input / Output Channels）。
- $K_H$、$K_W$：卷积核高度与宽度（Kernel Height / Width）。
- $S_H$、$S_W$：步长（Stride）。
- $P_H$、$P_W$：填充（Padding）。
- $D_H$、$D_W$：空洞率（Dilation）。
> [!tip] 大白话理解（Plain-language Intuition）
> 把卷积核想成一张很小的打分表。它在图像上移动，每到一个位置就检查“这里有多像我要找的模式”。一个核可能对竖边响应强，另一个核可能对某种纹理响应强；训练就是自动学会这些打分表。
## 2. 局部连接、参数共享与感受野
- **局部连接（Local Connectivity）**：输出单元只连接输入的一块局部区域，避免为整张图建立密集连接。
- **参数共享（Parameter Sharing）**：同一个输出通道在所有空间位置使用同一组卷积核权重。
- **感受野（Receptive Field）**：某个特征位置在原始输入上能够依赖的区域。堆叠卷积、增加步长、使用空洞卷积或池化都会扩大有效感受野。
- **重叠窗口（Overlapping Window）**：当步长小于有效卷积核时，相邻输出会使用重叠输入，保留更连续的空间信息。
- **平移等变性（Translation Equivariance）**：输入模式移动时，输出特征位置通常相应移动；边界、步长和离散采样会破坏严格等变性。
> [!tip] 大白话理解（Plain-language Intuition）
> 局部连接决定“每次只看一小块”，参数共享决定“到哪里都用同一把尺子”。层数变深后，后面的单元虽然仍只看前一层的小块，却已经间接汇总了原图更大的区域。
## 3. 多通道输入与多个卷积核
设输入形状为 `[N, C_in, H, W]`：
1. 每个输出卷积核的深度必须覆盖其组内的全部输入通道。
2. 每个通道分别与对应权重平面做互相关。
3. 各通道结果相加，再加该输出通道的偏置，得到一张输出特征图。
4. `C_out` 个不同卷积核产生 `C_out` 张输出特征图，输出形状为 `[N, C_out, H_out, W_out]`。
PyTorch 非分组卷积的权重形状为 `[C_out, C_in, K_H, K_W]`；分组卷积为 `[C_out, C_in / groups, K_H, K_W]`。
## 4. 控制空间尺寸的超参数
### 4.1 卷积核大小（Kernel Size）
- 常见二维核为 `1 × 1`、`3 × 3`、`5 × 5`，但 API 也支持偶数核和非方形元组。
- `1 × 1` 卷积不聚合相邻空间位置，但可以按位置混合通道并改变通道数。
- 较大卷积核直接覆盖更大局部范围，但计算量和参数量也更高；连续堆叠小卷积核可在加入更多非线性的同时扩大感受野。
### 4.2 填充（Padding）
- **有效卷积（Valid Convolution）**：`padding=0`，不补边，输出空间尺寸通常变小。
- **同尺寸填充（Same Padding）**：选择填充使输出尺寸满足目标；PyTorch `padding="same"` 当前不支持 `stride != 1`。
- **全填充（Full Padding）**：理论上让卷积核只要与输入有至少一个重叠元素就产生输出；常见深度学习 API 通常不直接以 `"full"` 模式命名，需要手工计算填充。
- 填充可延缓空间尺寸缩小并让边缘参与更多窗口，但补充值也会改变边界统计并可能引入伪影。
### 4.3 步长（Stride）
- `stride=1` 保留更多空间采样位置。
- `stride>1` 同时执行卷积与下采样，减少计算和输出分辨率；它会扩大相邻输出在原输入上的间隔，但也可能产生混叠（Aliasing）与细节损失。
### 4.4 空洞率（Dilation）
- `dilation>1` 在卷积核采样点之间插入间隔，在不增加权重数量的情况下扩大感受野。
- 有效卷积核大小为：
$$
K_{eff}=D(K-1)+1
$$
> [!tip] 大白话理解（Plain-language Intuition）
> 填充是在图片边上加“缓冲区”，步长是每次移动几格，空洞率是同一把尺子的刻度隔多远。三者共同决定输出有多大、看得多细，以及边缘如何处理。
## 5. 输出尺寸（Output Shape）
对每个空间维度分别计算：
$$
H_{out}=\left\lfloor\frac{H_{in}+2P_H-D_H(K_H-1)-1}{S_H}+1\right\rfloor
$$
$$
W_{out}=\left\lfloor\frac{W_{in}+2P_W-D_W(K_W-1)-1}{S_W}+1\right\rfloor
$$
例如 `H_in=W_in=640`、`kernel_size=3`、`stride=2`、`padding=0`、`dilation=1`：
$$
H_{out}=W_{out}=\left\lfloor\frac{640-3}{2}+1\right\rfloor=319
$$
若 `H_in=W_in=5`、`kernel_size=3`、`stride=1`、`padding=1`，输出保持 `5 × 5`。
## 6. 参数量与计算量（Parameter and Compute Count）
分组卷积参数量为：
$$
\text{weights}=C_{out}\times\frac{C_{in}}{G}\times K_H\times K_W
$$
如果 `bias=True`，再加 $C_{out}$ 个偏置。输出每个位置大约执行 $C_{out}(C_{in}/G)K_HK_W$ 次乘法，整体计算量还需乘 $N H_{out}W_{out}$。
## 7. PyTorch `nn.Conv2d`
### 7.1 主要签名与参数
```python
torch.nn.Conv2d(
    in_channels,
    out_channels,
    kernel_size,
    stride=1,
    padding=0,
    dilation=1,
    groups=1,
    bias=True,
    padding_mode="zeros",
    device=None,
    dtype=None,
)
```
- **`in_channels`**：输入通道数。
- **`out_channels`**：输出通道数，也等于输出卷积核数量。
- **`kernel_size`**：整数或 `(K_H, K_W)`。
- **`stride`**：整数或 `(S_H, S_W)`。
- **`padding`**：整数、二元组或字符串 `"valid"` / `"same"`。
- **`dilation`**：核元素间距。
- **`groups`**：控制输入和输出通道连接分组；`in_channels` 与 `out_channels` 必须能被它整除。
- **`bias`**：是否为每个输出通道学习一个偏置。
- **`padding_mode`**：如 `"zeros"`、`"reflect"`、`"replicate"`、`"circular"`。
### 7.2 可复现的形状示例
```python
import torch
from torch import nn

torch.manual_seed(0)
images = torch.randn(1, 3, 640, 640)
convolution = nn.Conv2d(
    in_channels=3,
    out_channels=4,
    kernel_size=3,
    stride=2,
    padding=0,
)
features = convolution(images)

print(images.shape)   # 输出: torch.Size([1, 3, 640, 640])
print(features.shape) # 输出: torch.Size([1, 4, 319, 319])
print(convolution.weight.shape)  # 输出: torch.Size([4, 3, 3, 3])
```
### 7.3 从 `[H, W, C]` 转为 `[N, C, H, W]`
```python
import matplotlib.pyplot as plt
import torch

image_hwc = plt.imread("data/img.jpg")
image_chw = torch.as_tensor(image_hwc).permute(2, 0, 1)
image_nchw = image_chw.unsqueeze(0).to(dtype=torch.float32)

print(image_hwc.shape)   # 代表性输出: (640, 640, 3)
print(image_chw.shape)   # 代表性输出: torch.Size([3, 640, 640])
print(image_nchw.shape)  # 代表性输出: torch.Size([1, 3, 640, 640])
```
- `permute(2, 0, 1)` 只改变维度视图顺序；后续操作需要连续内存时可调用 `.contiguous()`。
- 若图像是 `uint8`，转为浮点数后通常还需除以 `255` 并按训练集统计量标准化。
### 7.4 可视化输出通道
```python
import matplotlib.pyplot as plt

# 只取第一个样本；detach() 切断自动微分图，cpu() 确保 NumPy 可访问。
feature_maps = features[0].detach().cpu()
figure, axes = plt.subplots(1, feature_maps.shape[0], figsize=(12, 3))
for channel, axis in enumerate(axes):
    axis.imshow(feature_maps[channel].numpy(), cmap="gray")
    axis.set_title(f"channel {channel}")
    axis.axis("off")
plt.tight_layout()
plt.show()
```
该示例产生图形窗口，输出内容取决于随机权重与输入图像，因此不附固定控制台 Output。
## 8. 分组卷积与深度卷积（Grouped and Depthwise Convolution）
- `groups=1`：所有输入通道参与每个输出通道的计算。
- `groups>1`：通道被分组，只在组内连接；可降低参数和计算，但减少跨组信息交换。
- `groups=in_channels` 且 `out_channels=K × in_channels`：深度卷积（Depthwise Convolution），每个输入通道独立产生 `K` 个输出通道。
- 深度卷积后通常接 `1 × 1` 逐点卷积（Pointwise Convolution）完成跨通道混合，构成深度可分离卷积（Depthwise Separable Convolution）。
## 9. 常见错误（Common Errors）
- 把数学卷积核翻转规则直接套到 `Conv2d`，导致手算结果与框架互相关结果不一致。
- 输入仍是 `[N, H, W, C]`，造成通道数报错或错误解释空间维度。
- 忘记 `groups` 的整除约束。
- 把 `padding=kernel_size-1` 无条件当成 same padding；same padding 还取决于步长、空洞率与核大小。
- 声称卷积本身提供完全平移不变性；更准确的是结构上的平移等变性与有限条件下的稳定性。
- 直接对需要梯度或位于 GPU 的张量调用 `.numpy()`；应先 `.detach().cpu()`。
## 10. 参考资料（References）
- [PyTorch `torch.nn.Conv2d` 官方文档](https://docs.pytorch.org/docs/main/generated/torch.nn.Conv2d.html)
