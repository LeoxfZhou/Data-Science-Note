---
title: ResNet 残差学习与快捷连接（ResNet Residual Learning and Shortcut Connections）
tags:
  - data-science/deep-learning/computer-vision/backbones/resnet
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# ResNet 残差学习与快捷连接（ResNet Residual Learning and Shortcut Connections）
## 架构概述（Architecture Overview）
![[05-ResNet 残差学习与快捷连接（ResNet Residual Learning and Shortcut Connections）-20260726174012678.png]]
- **提出背景**：ResNet（残差网络）由微软研究院的何恺明等人在2015年的论文《Deep Residual Learning for Image Recognition》中正式提出。
- **大赛战绩**：残差网络一举夺得了ILSVRC 2015图像分类比赛的冠军，其Top-5错误率达到了惊人的3.6%，性能大幅超越同期的GoogLeNet与VGG。
- **网络深度**：得益于残差结构，网络层数突破了以往的瓶颈，最高可达152层，比传统的VGG网络深了8倍。
- **应用场景**：作为强大的特征提取骨干网络（Backbone），它被广泛应用于图像分类、目标检测（配合Faster R-CNN、YOLO等）、语义分割（如DeepLab、FCN），并在图像生成、风格迁移、医疗图像分析、视频分析以及自然语言处理的部分特征提取任务中得到大量应用。
> [!tip] 大白话理解（Plain-language Intuition）
> 普通深层网络要求每个模块重新学出完整答案；残差块允许模块只学“在输入基础上要改多少”。如果这一块暂时没必要改变信息，快捷路径仍能把输入直接送过去，优化器更容易找到接近恒等映射的解。

## 核心痛点与退化问题

- **深层训练困境**：在传统的深度神经网络中，随着卷积网络层数的增加，误差逆传播过程中会产生严重的**梯度消失**或**梯度爆炸**问题，导致模型训练难以进行。
- **退化问题（Degradation Problem）**：实验表明，随着网络深度的加深，模型的精度会趋于饱和，甚至出现训练集上的**训练误差先降低再升高**的现象。这种非过拟合引起的网络性能变差被称为退化问题。
- **残差网络的解法**：残差块提供恒等信息与梯度路径，主要缓解深层网络的优化退化。规范化与初始化已能缓解许多梯度消失/爆炸问题；残差连接并不保证任意深度或超参数都稳定。

## 残差学习机制
### 1. 核心思想

传统网络尝试直接学习期望的映射函数 $H(\mathbf{x}) = \mathcal{F}(\mathbf{x})$。而ResNet的核心创新在于让网络去学习**残差函数** $\mathcal{F}(\mathbf{x})$，即将目标映射重构为 $H(\mathbf{x}) = \mathcal{F}(\mathbf{x}) + \mathbf{x}$。其本质在底层结构上体现为一个简单的加法（Adding）算子。

### 2. 数学表达

一个基本的残差块可以表示为：

$$\mathbf{y} = \mathcal{F}(\mathbf{x}, \{W_i\}) + \mathbf{x}$$

- $\mathbf{x}$：残差块的输入向量。
- $\mathcal{F}(\mathbf{x}, \{W_i\})$：网络需要学习的残差映射，通常由2层或3层卷积、批归一化（BN）以及激活函数（ReLU）堆叠而成。
- $\mathbf{y}$：残差块的最终输出向量。

对于原始 ResNet v1 的两层基本块，可概括为：`Conv → BN → ReLU → Conv → BN → Add → ReLU`。第二个卷积的 BN 后先与快捷路径相加，再执行块末 ReLU；不能把第二个 ReLU 放进残差分支后再相加。

### 3. 设计动机

- **直接梯度路径**：加法使梯度包含沿恒等快捷路径传播的分量，不需要逐层只穿过残差分支。它改善深层优化，但没有改变优化器对参数的基本更新规则，也不是从 RNN 必然推导而来。
- **恒等映射退路**：如果某一层网络的恒等映射（即什么都不做）已经是最优解，网络只需将残差部分优化至 $\mathcal{F}(\mathbf{x}) = 0$，这极大地降低了直接拟合复杂非线性函数的训练难度。

## 快捷连接方式 (Shortcut Connections)
![[05-ResNet 残差学习与快捷连接（ResNet Residual Learning and Shortcut Connections）-20260726174038547.png|432]]
残差块中的加法操作依靠跳跃连接（Skip Connection）**或**快捷连接（Shortcut Connection）来实现。根据输入与输出的特征图通道数（Channel）是否匹配，实际应用中包含以下两种计算路径：
![[05-ResNet 残差学习与快捷连接（ResNet Residual Learning and Shortcut Connections）-20260726174109867.png|235]]
- **实线连接（通道数相同）**：当输入与输出的特征图维度完全一致时（例如都是 $3\times3\times64$ 的特征图），直接执行恒等加法：
    
    $$\mathbf{y} = \mathcal{F}(\mathbf{x}) + \mathbf{x}$$
    
- **虚线连接（通道数不同）**：当通道数发生变化（例如从64维变换到128维）或空间尺寸缩小时，输入 $\mathbf{x}$ 无法直接与 $\mathcal{F}(\mathbf{x})$ 相加。此时需要引入一个 $1\times1$ 的卷积矩阵 $W$ 对输入进行升维或下采样调整，计算公式变更为：
    
    $$\mathbf{y} = \mathcal{F}(\mathbf{x}) + W\mathbf{x}$$

此外，学术界针对Shortcut的架构设计还探索了多种变体，包括：原始结构（Original）、常数缩放（Constant Scaling）、排他门控（Exclusive Gating）、仅快捷路径门控（Shortcut-only Gating）、卷积快捷路径（Conv Shortcut）以及Dropout快捷路径（Dropout Shortcut）。

## 常用变体与网络拓扑

|**网络名称**|**残差块内部结构**|**特点与适用场景**|
|---|---|---|
|**ResNet-18 / ResNet-34**|**基础结构 (Basic Block)**<br><br>  <br><br>由两个 $3\times3$ 卷积层连续堆叠组成。|结构相对较浅，计算开销小，适合资源受限或任务简单的工程场景。|
|**ResNet-50 / ResNet-101 / ResNet-152**|**瓶颈结构 (Bottleneck)**<br><br>  <br><br>采用三层复合结构：$1\times1$ 卷积（降维） $\rightarrow$ $3\times3$ 卷积 $\rightarrow$ $1\times1$ 卷积（升维）。|这种“两头大、中间小”的瓶颈设计能在加深网络的同时压低参数量与计算量，适合大型数据集和复杂的视觉任务。|

残差连接促进了 ResNeXt、SE-ResNet、预激活 ResNet 等架构。DenseNet 也关注跨层信息流，但采用通道拼接而非逐元素残差相加；EfficientNet 的核心贡献是基线搜索与复合缩放，不能简单视为 ResNet 的直接衍生。

基于残差机制的演进使得网络深度不再是训练的限制，这也确立了ResNet在现代计算机视觉领域基石般的地位。

## 参考资料（References）
- [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)
