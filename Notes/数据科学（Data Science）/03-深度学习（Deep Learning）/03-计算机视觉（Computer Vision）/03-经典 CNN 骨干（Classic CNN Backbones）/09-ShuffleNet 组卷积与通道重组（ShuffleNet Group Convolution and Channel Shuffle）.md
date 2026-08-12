---
title: ShuffleNet 组卷积与通道重组（ShuffleNet Group Convolution and Channel Shuffle）
tags:
  - data-science/deep-learning/computer-vision/backbones/shufflenet
  - efficient-neural-networks
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# ShuffleNet 组卷积与通道重组（ShuffleNet Group Convolution and Channel Shuffle）
## 引言与核心目标（Motivation）

- **设计背景**：由旷视科技提出，与 MobileNet、SqueezeNet 类似，是一款专注于**移动端与嵌入式设备**的高效轻量化 CNN 模型。
- **技术路线**：属于**模型结构设计**方向，旨在有限的计算资源约束下，通过精心设计的网络架构来最大化模型精度，在速度和精度之间取得平衡，而非对大模型进行后期压缩。
- **核心创新**：创新性地引入了 **Pointwise Group Convolution（逐点组卷积）** 和 **Channel Shuffle（通道洗牌/重组）** 两大操作，在保持模型准确率的同时大幅度降低了计算量。
> [!tip] 大白话理解（Plain-language Intuition）
> 分组卷积像把通道分成几个互不交流的小组，虽然省计算，但信息会被困在组内。Channel Shuffle 把各组成员重新排队，让下一层每个组都能收到来自不同旧组的信息。

## 核心设计理念
### 1. 传统组卷积（Group Convolution）的弊端

- **特征稀疏连接**：传统卷积属于全通道的密集连接（Dense Connection），而组卷积（GConv）将输入特征图分组后独立进行卷积，属于稀疏连接（Sparse Connection），能显著降低计算量。
- **逐点卷积的计算瓶颈**：虽然 MobileNet 和 ResNeXt 采用了组卷积或深度卷积（DWConv），但它们在 1x1 卷积上依然使用密集的逐点卷积（Dense Pointwise Convolution）。在 ResNeXt 中，1x1 卷积甚至占据了约 **93.4%** 的乘加运算。
- **信息阻断问题**：如果将 1x1 卷积也改为稀疏的组卷积，堆叠多层后会导致**不同组之间的特征图互不通信（无 Cross-talk）**。每个组只处理自己内部的特征，这会严重降低网络的特征提取与信息表达能力。

###  2. Channel Shuffle 机制

为了在利用组卷积省算力的同时解决“信息不流转”的缺陷，ShuffleNet 提出了 **Channel Shuffle（通道重组）** 操作。

- **基本原理**：在每一次组卷积之后，对输出的特征图通道进行“均匀地打乱”再重新分组，确保下一层组卷积的输入能够均衡地来自前一层不同的组，从而实现跨通道的信息流转。
- **具体程序实现步骤**： 假设总通道数为 $C$，划分为 $g$ 个组，每组包含 $n$ 个通道（即 $C = g \times n$）。
    1. 将通道维度进行 Reshape 拆分为两个维度：`(g, n)`。
    2. 将这两个维度进行转置（Transpose）变换为：`(n, g)`。
    3. 最后重新 Flatten/Reshape 回一维特征维度，作为下一层组卷积的输入。
![[09-ShuffleNet 组卷积与通道重组（ShuffleNet Group Convolution and Channel Shuffle）-20260726190159815.png]]
##  ShuffleNet 基本单元（Unit）结构
![[09-ShuffleNet 组卷积与通道重组（ShuffleNet Group Convolution and Channel Shuffle）-20260726190211313.png]]
ShuffleNet 的基本单元是在 ResNet 瓶颈残差单元（Bottleneck Unit）的基础上改造而来的：

###  1. 步长为 1 的基本单元（Stride = 1）

- **结构顺序**：`1x1 组卷积 (GConv) -> Channel Shuffle -> 3x3 深度卷积 (DWConv) -> 1x1 组卷积 (GConv) -> 残差相加 (Element-wise Add)`。
- **细节设计**：在第一个 1x1 组卷积后加入 Channel Shuffle 操作；同时为了精简计算，3x3 深度卷积后**去掉了 ReLU 激活函数**。

###  2. 步长为 2 的降采样单元（Stride = 2）

当特征图空间分辨率减半、通道数需要增加时，网络单元做出如下调整以进一步降低计算量与参数量：

- **双分支设计**：
    - **主分支**：`1x1 GConv -> Channel Shuffle -> 3x3 DWConv（Stride=2） -> 1x1 GConv`。
    - **快捷连接分支（Shortcut）**：使用 `3 × 3` 平均池化（Average Pooling, stride=2）。它是局部平均池化，不是全局平均池化（Global Average Pooling）。
- **融合方式**：两个分支的输出最终采用 **通道拼接（Concat）** 操作组合在一起，而非传统的逐元素相加（Add），以此自然地实现通道数翻倍。

##  网络整体架构与特点

- **宏观结构**：网络开头使用传统的 3x3 标准卷积与最大池化层，随后连续堆叠三个阶段（Stage 2, 3, 4），每个阶段由多个 ShuffleNet 基本单元组成。最后通过全局池化与全连接层输出预测值。
- **阶段特征**：每个 Stage 的第一个基本单元步长均为 2（负责降低分辨率并使通道翻倍），后续的单元步长为 1，保持尺寸和通道数不变。
- **超参数 $g$（分组数）的作用**：$g$ 决定了组卷积中的分组规模。在相同的计算资源约束下，**$g$ 越大，网络可以配置的通道数（特征图数量）就越多**，特征提取能力越强，从而能够用更宽的网络换取更高的精度。

##  模型效果与实验结论

1. **$g$ 值的正向效应**：在 ImageNet 分类实验中，基本上 $g$ 取值越大，模型的分类误差越低。这是由于相同算力下，大 $g$ 值带来了更丰富的通道数。
2. **Channel Shuffle 的有效性**：对比实验表明，在相同网络配置下，开启 Channel Shuffle 后的模型性能显著优于不采用 Shuffle 的网络，直接证明了跨组信息交融的必要性。
3. **对比 MobileNet**：实验数据显示，ShuffleNet 在保持更低计算复杂度的同时，在分类精度上超越了同期的 MobileNet V1。

##  拓展：ShuffleNet V2 的前沿改进

结合网络结构图可以发现，旷视科技后续提出的 **ShuffleNet V2** 针对 V1 的一些实际工程瓶颈（如组卷积带来的过多内存访问成本 MAC）进行了改良：

- **引入 Channel Split（通道分割）**：在基本单元的输入端，直接将通道平分为两路。一路保持恒等映射，另一路经过标准 1x1 卷积、3x3 DWConv 和 1x1 卷积。
- **取消 Pointwise 组卷积**：V2 在主分支内部回归了标准的 1x1 卷积（不再使用 1x1 GConv），通过通道分割和最后的 Concat + Channel Shuffle 来天然地实现组间信息流转，这种设计在硬件实际推理中具备更高的速度优势。

> [!warning] FLOPs 与真实速度（FLOPs vs. Real Latency）
> 内存访问成本（Memory Access Cost, MAC）、并行度、碎片化操作和逐元素算子都会影响速度。模型比较必须在同一硬件、批次、精度、运行时和输入尺寸下测量延迟。

## 参考资料（References）
- [ShuffleNet: An Extremely Efficient Convolutional Neural Network for Mobile Devices](https://openaccess.thecvf.com/content_cvpr_2018/html/Zhang_ShuffleNet_An_Extremely_CVPR_2018_paper.html)
- [ShuffleNet V2: Practical Guidelines for Efficient CNN Architecture Design](https://openaccess.thecvf.com/content_ECCV_2018/html/Ningning_Light-weight_CNN_Architecture_ECCV_2018_paper.html)
