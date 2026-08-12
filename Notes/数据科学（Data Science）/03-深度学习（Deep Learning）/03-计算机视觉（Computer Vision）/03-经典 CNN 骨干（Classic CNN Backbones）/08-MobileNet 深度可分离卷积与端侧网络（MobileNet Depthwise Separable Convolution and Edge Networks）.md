---
title: MobileNet 深度可分离卷积与端侧网络（MobileNet Depthwise Separable Convolution and Edge Networks）
tags:
  - data-science/deep-learning/computer-vision/backbones/mobilenet
  - efficient-neural-networks
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# MobileNet 深度可分离卷积与端侧网络（MobileNet Depthwise Separable Convolution and Edge Networks）
## 设计初衷与背景（Motivation）

- **痛点**：传统的深度卷积神经网络（如 ResNet、VGG）为了追求高分类准确率，模型越做越深、复杂度越来越高，导致模型过于庞大，面临**内存不足**和**高延迟**的问题。
- **应用场景限制**：在移动端或嵌入式设备（如自动驾驶中的行人检测、手机端实时视觉任务）中，硬件资源有限，要求系统必须具备**低延迟**和**快速响应**的能力。
- **技术路线**：小模型的研究通常有两个方向（一是大模型压缩，二是直接设计小模型）。MobileNet 属于**后者**，由 Google 提出，是一种专注于在**准确率（Accuracy）与延迟（Latency）之间取得最佳折中**的轻量化神经网络。
> [!tip] 大白话理解（Plain-language Intuition）
> 标准卷积一次同时做“每个通道看周围”和“通道之间交流”。MobileNet v1 把两件事拆开：深度卷积各通道自己看周围，`1 × 1` 逐点卷积再负责通道交流，因此显著减少乘加运算。

## 核心创新：深度可分离卷积（Depthwise Separable Convolution）

MobileNet 的核心基本单元是深度可分离卷积，它将传统的标准卷积操作分解为两个更小的步骤：**深度卷积（Depthwise）**和**逐点卷积（Pointwise）**。
![[08-MobileNet 深度可分离卷积与端侧网络（MobileNet Depthwise Separable Convolution and Edge Networks）-20260726184748391.png|298]]
### 1. 概念拆解

- **深度卷积 (Depthwise Convolution, DW)**：
    - **标准卷积**的卷积核会同时作用在所有的输入通道上。
    - **深度卷积**针对每一个输入通道使用一个独立的卷积核进行操作（一个卷积核对应一个通道）。它只负责在空间维度上进行滤波，而不融合通道间的特征。
- **逐点卷积 (Pointwise Convolution, PW)**：
    - 其实就是普通的卷积，但其卷积核大小固定为 **1×1**。
    - 它的主要作用是将深度卷积输出的各个通道特征进行线性组合与融合，从而转换通道数。
![[08-MobileNet 深度可分离卷积与端侧网络（MobileNet Depthwise Separable Convolution and Edge Networks）-20260726184807290.png]]
###  2. 计算量对比与数学推导

假设输入特征图大小为 $D_F \times D_F \times M$，输出特征图大小为 $D_G \times D_G \times N$，卷积核大小为 $D_K \times D_K$。为了简化对比，假定输入与输出的空间分辨率一致（即 $D_F = D_G$）。

- **标准卷积的计算量**：
    
    $$FLOPs_{\text{standard}} = D_K \cdot D_K \cdot M \cdot N \cdot D_G \cdot D_G$$
    
- **深度可分离卷积的计算量**：
    
    $$FLOPs_{\text{separable}} = \underbrace{D_K \cdot D_K \cdot M \cdot D_G \cdot D_G}_{\text{Depthwise 计算量}} + \underbrace{M \cdot N \cdot D_G \cdot D_G}_{\text{Pointwise 计算量}}$$
    
- **计算量优化比例**：
    
    $$\frac{FLOPs_{\text{separable}}}{FLOPs_{\text{standard}}} = \frac{D_K \cdot D_K \cdot M \cdot D_G \cdot D_G + M \cdot N \cdot D_G \cdot D_G}{D_K \cdot D_K \cdot M \cdot N \cdot D_G \cdot D_G} = \frac{1}{N} + \frac{1}{D_K^2}$$

> **核心结论**：当输出通道数 $N$ 较大且使用 `3 × 3` 核时，比值接近 $1/9$。这是乘加量的近似比较，不保证任意硬件上获得 9 倍真实加速。

##  MobileNet 网络架构与工程特性
![[08-MobileNet 深度可分离卷积与端侧网络（MobileNet Depthwise Separable Convolution and Edge Networks）-20260726184821578.png]]

###  1. 基本单元结构

在网络实际构建中，MobileNet 在深度卷积和逐点卷积后面都会紧跟 **Batch Normalization (BN)** 和 **ReLU 激活函数**，其完整标准块结构为：

`3×3 Depthwise Conv -> BN -> ReLU -> 1×1 Pointwise Conv -> BN -> ReLU`

###  2. 整体网络特性

- **层数**：如果将 DW 和 PW 算作独立的卷积层，整个网络的主干结构共有 **28 层**（不含全局平均池化和 Softmax 分类层）。
- **下采样方式**：网络中没有使用传统的最大池化层，而是直接通过设置部分深度卷积的步长为 2（Stride=2）来实现特征图的分辨率缩减。
- **参数与计算量分布的秘密**：
    - **1×1 逐点卷积（PW）占了绝大部分的计算量（86.66%）和参数量（74.59%）**。
    - **工程优势**：在底层硬件实现中，标准卷积通常需要通过 `im2col` 方式进行内存重组后计算；而 1×1 卷积**不需要内存重组**，底层矩阵乘法（GEMM）调用效率极高，因此在实际设备上的运行速度比理论计算量表现得还要快。

###  3. 性能表现简述

论文中的特定 ImageNet 配置显示，MobileNet 在显著降低乘加次数和参数量时保持了有竞争力的准确率。与 VGG16、GoogLeNet 的高低关系依赖宽度乘子、分辨率乘子、训练配方和评估口径，不能推广为所有配置的固定排序。

##  模型瘦身：两大控制超参数

为了让模型能自适应更严苛的硬件环境，MobileNet 引入了两个全局超参数来对模型进行“瘦身”调优：

- **宽度因子 (Width Multiplier: $\alpha$)**：
    - **作用**：按比例等量减少每一层的通道数。引入后输入通道变为 $\alpha M$，输出通道变为 $\alpha N$。
    - **取值**：$\alpha \in (0, 1]$，常见取值为 `[1.0, 0.75, 0.5, 0.25]`。
    - **开销变化**：能够按大约 **$\alpha^2$** 的比例**同时降低计算量和参数量**。
- **分辨率因子 (Resolution Multiplier: $\rho$)**：
    - **作用**：按比例降低输入图像以及内部所有特征图的空间分辨率。
    - **取值**：$\rho \in (0, 1]$，常见的输入分辨率如 `224, 192, 160, 128`。
    - **开销变化**：能够按 **$\rho^2$** 的比例降低计算量，但**完全不改变模型的参数量**。

##  延伸拓展：MobileNet V2 的三大改进点

作为 V1 的升级版，MobileNet V2 针对 V1 存在的“部分特征易被 ReLU 破坏”等缺陷进行了优化，核心改进包括：

1. **引入倒残差结构 (Inverted Residuals)**：引入了 Shortcut 残差连接。与传统 ResNet“两头粗中间细”不同，V2 采用“两头细中间粗”的结构——在进行 3×3 深度卷积之前，先用 1×1 卷积**提升特征图的通道数**进行特征扩增。
2. **线性激活单元 (Linear Bottlenecks)**：在块的最后一层 1×1 逐点卷积后，使用 **Linear（线性激活）** 代替 ReLU，防止低维特征信息在非线性映射中被完全破坏。
3. **激活函数升级**：内部的非线性激活层统一升级为了更为适合移动端定点量化的 **ReLU6** 激活函数。

## 参考资料（References）
- [MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications](https://arxiv.org/abs/1704.04861)
- [MobileNetV2: Inverted Residuals and Linear Bottlenecks](https://arxiv.org/abs/1801.04381)
