---
title: SENet 通道注意力与特征重标定（SENet Channel Attention and Feature Recalibration）
tags:
  - data-science/deep-learning/computer-vision/backbones/senet
  - attention/channel-attention
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# SENet 通道注意力与特征重标定（SENet Channel Attention and Feature Recalibration）
## 前言（Introduction）

卷积神经网络（Convolutional Neural Network, CNN）分类模型常被目标检测（Object Detection）和语义分割（Semantic Segmentation）复用为骨干网络（Backbone）。SENet（Squeeze-and-Excitation Networks）的核心贡献是可插入现有骨干的通道重标定模块；基于 SE 的提交获得 ILSVRC 2017 分类任务冠军。

> [!tip] 大白话理解（Plain-language Intuition）
> SE 模块先看每个通道的全局摘要，再给每个通道一个 0–1 门控系数。它像调音台：根据当前输入提高有用通道、压低次要通道，但门控大小不等同于严格的因果解释。

> [!note] 竞赛口径（Competition Scope）
> 基于 SE 的提交在 ILSVRC 2017 分类任务中获得冠军；这表示该年度竞赛结果，不宜泛称整个 ImageNet 项目的“最后一届”。

## 主体思路

传统的卷积操作核心是对局部区域进行特征融合，这同时包含了空间上（H和W维度）以及通道间（C维度）的特征融合。过往的研究大多聚焦于提高感受野或提取多尺度空间信息（如 Inception 网络的多分支结构），或者通过组卷积（Group Convolution）等方式使模型更加轻量化。

而 **SENet 的创新点在于聚焦于通道（Channel）之间的关系**，旨在让模型能够自动学习到不同通道特征的重要程度。为此，SENet 提出了 **Squeeze-and-Excitation (SE) 模块**，通过在通道维度上引入注意力机制（Attention / Gating 机制），使模型能够自适应地提升有用的特征通道响应，并抑制对当前任务用处不大的通道特征。

## Squeeze-and-Excitation (SE) 模块详解
![[07-SENet 通道注意力与特征重标定（SENet Channel Attention and Feature Recalibration）-20260726184033024.png]]

对于给定的任意映射 $F_{tr}: X \to U$（以普通卷积为例），输入的特征图经过卷积核 $V = [v_1, v_2, \dots, v_C]$ 的计算得到输出 $U = [u_1, u_2, \dots, u_C]$，其中第 $c$ 个通道的输出可以表示为：

$$u_c = v_c * X = \sum_{s=1}^{C'} v_c^s * x^s$$

标准卷积同时学习局部空间模式和跨输入通道组合；SE 模块在卷积变换之后显式增加通道级重标定路径，使通道响应依赖全局上下文。它主要包含以下三个步骤：

### 1. Squeeze 操作（空间特征压缩）

由于卷积仅在局部空间内操作，在网络前层感受野较小时，输出 $u_c$ 很难获得足够的全局上下文信息来提取通道关系。Squeeze 操作通过全局平均池化（Global Average Pooling）将一个通道内整个空间特征（$H \times W$）编码为一个通道级的全局标量描述子 $z_c$：

$$z_c = F_{sq}(u_c) = \frac{1}{H \times W}\sum_{i=1}^{H}\sum_{j=1}^{W}u_c(i,j)$$

这一操作使靠近输入层的结构也能获得全局感受野的信息。

### 2. Excitation 操作（通道特征激励）

为了利用 Squeeze 得到的全局特征并抓取通道间的非线性关系，Excitation 操作采用了一种灵活的门控（Gating）机制：

$$s = F_{ex}(z, W) = \sigma(g(z,W)) = \sigma(W_2 \delta(W_1 z))$$

其中 $\delta$ 代表 ReLU 激活函数，$\sigma$ 代表 Sigmoid 激活函数。

为了降低模型复杂度并提升泛化能力，这里采用了包含两个全连接层（FC）的 **Bottleneck 结构**：

- **第一层全连接层 $W_1 \in \mathbb{R}^{\frac{C}{r} \times C}$**：起到降维作用，降维系数 $r$ 是一个超参数（论文中默认为 **16**）。
- **第二层全连接层 $W_2 \in \mathbb{R}^{C \times \frac{C}{r}}$**：将维度恢复至原始的通道数 $C$。

**采用双层全连接层的好处在于**：一方面带来了更多的非线性组合，能更好地拟合通道间复杂的依赖关系；另一方面相较于直接单层全连接，极大地减少了参数量与计算开销。

### 3. Scale / ReWeight 操作（特征重标定）

最后，将 Excitation 操作输出的各个通道激活值（即 **0~1** 之间的权重系数）作为重要性指标，通过逐通道的乘法加权到原始特征图 $U$ 上，完成特征在通道维度上的重标定：

$$\tilde{x}_c = F_{scale}(u_c, s_c) = s_c \cdot u_c$$

经过重标定后的特征图 $\tilde{X}$ 将更有辨别能力。

## SE 模块的通用集成与开销

SE 模块具有极高的灵活性，可以无缝嵌入到现有的各类网络架构中：

- **在 Inception 网络中**：由于没有残差结构，直接对整个 Inception 模块的输出应用 SE 模块。
- **在 ResNet 网络中**：将 SE 模块嵌入到残差结构内部的残差学习分支中（即 Element-wise 相加之前）。
![[07-SENet 通道注意力与特征重标定（SENet Channel Attention and Feature Recalibration）-20260726184101791.png]]

**模型开销分析**：

以 SE-ResNet-50 为例，增加 SE 模块后的模型参数增加量计算公式为：

$$\text{Parameters Increase} \approx \frac{2}{r} \sum_{s=1}^{S} C_s^2 \cdot N_s$$

当降维系数 $r = 16$ 时，SE-ResNet-50 仅增加了约 **10%** 的参数量，而计算量（GFLOPS）的增加甚至不到 **1%**。

## 模型效果

1. 在传统网络（如 ResNet、VGG）中引入 SE 模块后，分类准确度均获得了稳定的提升。
2. 在轻量化网络（如 MobileNet、ShuffleNet）中嵌入 SE 模块同样带来了明显的性能收益。
3. 最终，基于 ResNeXt 结构构建的 **SENet-154** 模型在 ImageNet 测试集上取得了 top-5 错误率 **2.251%** 的极佳表现，成功斩获 2017 年竞赛分类任务冠军。

## 缺点与改进方向

在完成对经典 SENet 的整理后，我们可以看到它虽然效果显著，但在后续的研究中也被指出了部分局限性，并演化出了更多的改进版本：

### 核心缺点

1. **门控路径不显式建模空间位置（No Explicit Spatial Attention）**：Squeeze 使用全局平均池化把每个通道压缩成一个标量，因此门控权重不保留空间位置；原始特征图仍在主路径中保留，并不会被 SE 模块“完全丢失”。需要位置相关注意力时，可增加空间注意力模块。
2. **全连接层降维带来的副作用（Side Effects of Dimensionality Reduction）**：为了控制参数量，SENet 在 Excitation 中对通道进行了降维（$C \to C/r$）。后来的研究（如 ECA-Net）指出，这种人为的维度缩减会破坏通道间的直接映射交流，对预测通道注意力产生负面影响。
3. **硬件上的推理延迟（Inference Latency）**：虽然 SENet 的理论计算量（GFLOPS）增加极少（不到 **1%**），但在实际工业落地中，全连接层以及最后的逐通道乘法（Scale）属于元素级操作或分支结构，在 GPU 等并行计算设备上会带来额外的访存开销，从而导致模型实际的推理速度（Latency）有所减慢。

### 常见改进方向

1. **CBAM (Convolutional Block Attention Module)**：针对 SENet 忽视空间信息的问题进行了改进。CBAM 将通道注意力（Channel Attention）与空间注意力（Spatial Attention）串联结合，不仅能学习到“哪个通道重要”，还能通过在空间维度做池化和卷积学习到“特征图的哪个位置重要”。
2. **ECA-Net (Efficient Channel Attention)**：针对 SENet 全连接层降维的缺陷进行改进。ECA-Net 提出了一种“不降维”的局部跨通道交互策略，直接在全局平均池化后利用高效的一维卷积（1D Convolution）代替全连接层，在显著降低参数量和复杂度的同时，避免了降维带来的性能损失。
3. **SKNet (Selective Kernel Networks)**：将通道注意力机制融合进了动态多尺度卷积中。通过注意力机制让网络根据输入信息自适应地选择不同感受野大小的卷积核，实现更具弹性的空间特征融合。

## 参考资料（References）
- [Squeeze-and-Excitation Networks](https://openaccess.thecvf.com/content_cvpr_2018/papers/Hu_Squeeze-and-Excitation_Networks_CVPR_2018_paper.pdf)
