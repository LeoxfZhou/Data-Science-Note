---
title: YOLOv1、YOLOv2 与 YOLOv3 演化（YOLOv1-v3 Evolution）
tags:
  - data-science/deep-learning/computer-vision/object-detection/yolo
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# YOLOv1、YOLOv2 与 YOLOv3 演化（YOLOv1-v3 Evolution）
## 1. YOLOv1：端到端单阶段检测（YOLOv1）

YOLOv1（You Only Look Once v1）是目标检测领域的一个里程碑。在 R-CNN 到 Faster R-CNN 的演进中，算法都基于**候选区域+分类 (Proposal + Classification)** 的两阶段模式，虽精度高但速度慢。YOLOv1 另辟蹊径，创造性地将目标检测从**分类问题 (Classification Problem)** 转换为**回归问题 (Regression Problem)**，直接在输出层回归边界框的位置和所属类别的置信度。

## 一、 算法核心突破与流程
### 1. 主要特点

- **速度极快 (High Speed)**：能够达到实时检测的要求。在 Titan X GPU 上可以达到 **45 fps**（帧每秒）。
- **全局全图上下文 (Global Context)**：使用全图信息进行预测，相比两阶段算法，其**背景错误 (Background Error)**（即把背景误检为物体）的情况明显更少。
- **泛化能力强 (Strong Generalization)**：能学到物体更本质的泛化特征。
### 2. 推理三步走 (Three-Step Inference Phase)

YOLOv1 处理图像的流程非常简单明了：

1. **图像缩放 (Resize)**：将输入图像统一缩放到 $448 \times 448$ 大小。
2. **单网络运行 (Single CNN)**：在图像上运行单个卷积神经网络。论文模型受 GoogLeNet 启发，由 24 个卷积层和 2 个全连接层组成；Darknet 命名与骨干体系主要出现在后续 YOLO 版本，不能倒置到 YOLOv1。
3. **后处理优化 (Post-processing)**：根据模型输出的置信度，对检测结果进行**非极大值抑制 (NMS, Non-Maximum Suppression)**，消除冗余重复框。
![[07-YOLOv1、YOLOv2 与 YOLOv3 演化（YOLOv1-v3 Evolution）-20260626102735623.png]]
## 二、 核心思想：统一检测 (Unified Detection)

YOLOv1 将目标检测的分离组件统一为了单个神经网络，使用整张图像的特征来直接预测所有的边界框。
### 1. 网格划分与责任制

- **网格划分 (Grid Cell Division)**：将输入图像划分为 $S \times S$ 个**网格单元 (Grid Cell)**。
- **物体中心原则**：**如果一个物体的中心位于某个网格单元内，那么该网格单元就必须负责检测这个物体**。
    - _示例_：如 PPT 所示，狗的中心点落入第 5 行、第 2 列的格子内，因此这个特定格子就负责预测这只狗。
![[07-YOLOv1、YOLOv2 与 YOLOv3 演化（YOLOv1-v3 Evolution）-20260626102902456.png]]
### 2. 网格预测内容

每一个网格单元（Grid Cell）都需要预测以下两类信息：

- **$B$ 个边界框坐标与置信度**：
    - **坐标信息 $(x, y, w, h)$**：其中 $(x, y)$ 表示边界框中心点坐标相对于当前网格的偏移量；$(w, h)$ 是边界框的宽度、高度相对于实际整张图像宽高的比值。
    - **置信度 (Confidence)**：反映模型对于这个预测框中包含物体的可能性大小以及预测框的准确度。
- **$C$ 个条件类别概率 (Conditional Class Probability)**：
    - 表示在当前网格单元包含物体的条件下，属于某个特定类别 $C$ 的概率。
![[07-YOLOv1、YOLOv2 与 YOLOv3 演化（YOLOv1-v3 Evolution）-20260626103030505.png|428]]

**核心概念辨析 (NOTE)**
> 
> - **Confidence（置信度）**：表示边界框包含物体的概率值（针对 Bounding Box）。
> - **Conditional Class Probability（条件类别概率）**：表示网格单元属于某个类别的概率值（针对 Grid Cell）。
### 3. 测试阶段分数计算

将每个网格预测的类别概率与每个边界框的置信度相乘，即可得到每个边界框的**特定类别的置信度得分 (Class-Specific Confidence Score)**：

$$\text{Score} = \text{Conditional Class Probability} \times \text{Confidence}$$
![[07-YOLOv1、YOLOv2 与 YOLOv3 演化（YOLOv1-v3 Evolution）-20260626103219188.png]]
## 三、 输出张量结构分析 (Output Tensor Architecture)

根据论文建议，通常设置 $S = 7, B = 2$。在经典的 **PASCAL VOC 数据集** 中（有 $C = 20$ 个类别），网络的最终预测输出是一个形状为 **$7 \times 7 \times 30$** 的三维张量（Tensor）。
###  维度 $30$ 的拆解剖析

$$\text{Output Dimension} = B \times 5 + C = 2 \times 5 + 20 = 30$$

- **前 $10$ 个通道（$B \times 5$）**：由 2 个边界框组成。每个边界框包含 5 个预测值：$(x, y, w, h, \text{Confidence})$。
- **后 $20$ 个通道（$C$）**：该网格对应的 20 个类别的条件类别概率。
    ![[07-YOLOv1、YOLOv2 与 YOLOv3 演化（YOLOv1-v3 Evolution）-20260626104046415.png|454]]

```
    [ 7 x 7 网格空间 ]
      ├── Box 1: (x, y, w, h, confidence) -> 5 个值
      ├── Box 2: (x, y, w, h, confidence) -> 5 个值
      └── Class Probabilities: [P1, P2, ... P20] -> 20 个值
```

![[07-YOLOv1、YOLOv2 与 YOLOv3 演化（YOLOv1-v3 Evolution）-20260626103632919.png]]
![[07-YOLOv1、YOLOv2 与 YOLOv3 演化（YOLOv1-v3 Evolution）-20260626104007823.png]]
## 四、 损失函数设计 (Loss Function)

YOLOv1 采用均方和误差来计算总损失，但在设计上通过权重系数和数学技巧解决了正负样本不平衡及大小框敏感度问题：
### YOLOv1 的总损失函数共分为 **5 个部分**：

$$\begin{aligned} \text{Loss} &= \color{red}{\lambda_{\text{coord}} \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}_{ij}^{\text{obj}} \left[ (x_i - \hat{x}_i)^2 + (y_i - \hat{y}_i)^2 \right]} && \text{(1) 中心点坐标回归损失} \\ &+ \color{red}{\lambda_{\text{coord}} \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}_{ij}^{\text{obj}} \left[ (\sqrt{w_i} - \sqrt{\hat{w}_i})^2 + (\sqrt{h_i} - \sqrt{\hat{h}_i})^2 \right]} && \text{(2) 边界框宽高回归损失} \\ &+ \color{blue}{\sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}_{ij}^{\text{obj}} (C_i - \hat{C}_i)^2} && \text{(3) 含物体边界框置信度损失} \\ &+ \color{blue}{\lambda_{\text{noobj}} \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}_{ij}^{\text{noobj}} (C_i - \hat{C}_i)^2} && \text{(4) 不含物体背景框置信度损失} \\ &+ \color{green}{\sum_{i=0}^{S^2} \mathbb{1}_{i}^{\text{obj}} \sum_{c \in \text{classes}} (p_i(c) - \hat{p}_i(c))^2} && \text{(5) 条件类别概率预测损失} \end{aligned}$$

 **注意**：公式中带帽子（如 $\hat{x}, \hat{y}, \hat{w}, \hat{h}, \hat{C}, \hat{p}$）的数值代表 **真实标签 (Ground Truth)**，不带帽子的代表模型的 **预测值 (Predicted Value)**。
####  1. 坐标与宽高回归（第 1, 2 行）—— 解决“框得准不准”

- **(1) 中心点坐标损失**：约束预测框的中心点 $(x, y)$ 逼近真实物体的中心点。
- **(2) 宽高尺寸损失**：约束预测框的 $(w, h)$ 逼近真实物体的宽高。

####  2. 置信度预测（第 3, 4 行）—— 解决“有没有物体”

- **(3) 正样本置信度损失**：负责检测物体的那个 Bounding Box，其真实置信度标签 $\hat{C}_i$ 被设定为该预测框与真实框的实际 $\text{IoU}$。通过均方误差逼近这个 $\text{IoU}$。
- **(4) 负样本（背景）置信度损失**：由于绝大多数网格不包含物体中心，它们全被划分为背景框，其真实置信度标签 $\hat{C}_i = 0$。

####  3. 类别概率预测（第 5 行）—— 解决“是什么东西”

- **(5) 分类损失**：**不针对单个 Bounding Box**，而是针对整个网格单元（Grid Cell）。只要网格内包含物体中心（$\mathbb{1}_{i}^{\text{obj}}=1$），就计算该网格预测的 $C$ 个类别的条件概率与真实 One-hot 标签之间的均方误差。
### 数学设计技巧
### 1. 坐标损失权重 $\lambda_{coord} = 5.0$

- **目的**：由于大多数网格不包含物体，这会导致置信度损失主导梯度，造成网络不稳定。因此**加大、加强坐标信息预测失败所带来的损失**。
### 2. 宽高开平方根 ($\sqrt{w}, \sqrt{h}$)

- **目的**：**兼顾大框和小框的预测**。若直接用绝对宽高，同样大小的偏移对小框的影响是致命的，而对大框来说微不足道。开根号后，能让大框接受较大的绝对偏移，而让小框对偏移更加敏感（不接受较大偏移）。
### 3. 背景置信度惩罚权重 $\lambda_{noobj} = 0.5$

- **目的**：**减弱不包含物体的边界框（背景框）的置信度损失**，防止负样本淹没正样本。

## 五、 特征数据与训练准备 (Training Phase Data Prep)

在训练时，真实标签（Ground Truth）的特征数据处理规则如下：

- **类别矩阵**：$7 \times 7 = 49$ 个单元格，每个格对应一个 $20$ 维的类别向量。如果真实边框的中心点落在当前单元格，则对应类别的索引赋值为 `1`，其它为 `0`。
- **位置信息**：直接使用真实边框的中心点坐标 $(x, y)$、宽度 $w$、高度 $h$ 除以原始图像的宽高，归一化到 $[0, 1]$ 之间作为真实标签值。
- **置信度标签**：如果真实边框的中心点落在当前单元格内，则当前单元格中与真实边框 **IoU 最大的那个边界框** 负责预测该物体，其置信度的真实目标值设为该预测框与实际边框的 **IoU 值**；若不包含物体中心，则置信度目标值为 `0`。

## 六、 模型优缺点分析
### 优点

1. **超高推理速度**：完美达到实时（Real-time）处理的性能要求。
2. **背景低误检率**：利用了全图的上下文特征，有效降低了把背景误认为物体的概率。
### 缺点

1. **精度天花板较明显**：定位精度和整体效果在早期版本中没有同时期的 Faster R-CNN 好。
2. **密集空间物体的克星**：因为一个网格单元（Grid Cell）最多只负责预测一个物体，**如果一个网格内包含多个相同或不同类别的密集小物体，YOLOv1 很大可能只能检测出其中的某一个**，极易造成漏检。

**知识双链提示**：YOLOv1 彻底开启了一阶段检测流派，其对空间密集的局限性在后续 `[[Anchor Box (锚框机制)]]` 引入后（如 YOLOv2、`[[SSD]]`）得到了极大的改善。

## 2. YOLOv2：更准、更快、更强（YOLO9000: Better, Faster, Stronger）

YOLOv2（在结合大规模分类数据集时称为 YOLO9000）针对 YOLOv1 存在的**定位不准**和**召回率 (Recall)** 较低的致命缺陷进行了全面升级。论文从三个核心维度对模型进行了重新设计：

1. **更准 (Better)**：专注于提升检测精度。论文表格中 YOLOv1 在 VOC 2007 的 mAP 为 63.4；YOLOv2 以 544×544 输入报告 78.6 mAP。不同输入尺寸对应不同速度—精度点，不能把 78.6 当作所有 YOLOv2 配置的固定结果。
2. **更快 (Faster)**：通过全面重构网络骨干结构，极大提升了**前向计算速度 (Inference Speed)**。
3. **更强 (Stronger)**：通过改进**损失函数 (Loss Function)** 和引入联合训练机制，使得模型能够检测超过 9000 种物体分类。

## 一、 “更准 (Better)” —— 七大核心精度改良策略
### 1. 批归一化 (Batch Normalization, BN)

- **做法**：在卷积层后加入批归一化（Batch Normalization, BN），并移除 Dropout。
- **原论文动机（Original Motivation）**：论文以改善收敛、减少对其他正则化的依赖来解释 BN，并报告约 2 mAP 的提升。
- **后续演化/现代理解（Later Development / Modern Understanding）**：BN 的收益不能只归因于“内部协变量偏移”；更稳健的表述是它重参数化并平滑优化过程，同时引入依赖批统计量的训练行为。
> [!tip] 大白话理解（Plain-language Intuition）
> BN 像在每层之间设置一个会随批次校准的中转站，让后一层不必不断适应数值尺度的大幅漂移；但小批次时统计噪声也可能变大。
- **效果**：**mAP 提升了 2%**。
### 2. 高分辨率分类器 (High Resolution Classifier)

- **痛点**：传统检测模型通常直接沿用在 ImageNet 上预训练的分类网络（如 VGG），但它们的初始输入分辨率通常不足 $256 \times 256$，导致在目标检测时分辨率太低、小目标丢失。
- **改进**：YOLOv2 自定义了 Darknet 分类网络，先将图像的输入分辨率更改为 **$448 \times 448$**，在 ImageNet 上强行微调训练 10 个**轮次 (Epochs)**，让网络充分适应高分辨率输入。
- **效果**：在实际应用到检测任务进行 **微调 (Fine-tune)** 时，**mAP 提升了 4%**。
### 3. 基于锚框的卷积 (Convolutional with Anchor Boxes)

- **做法**：借鉴 Faster R-CNN 的 **锚框 (Anchor Boxes)** 思想，用于产生多个边界框候选区域，核心目的是提升模型的**召回率 (Recall)**。
- **重构细节**：
    - 删除了 YOLOv1 尾部的全部**全连接层 (Fully Connected Layers)**。
    - 去掉了最后一个**池化层 (Pooling Layer)**，以确保最终输出的特征图具有更高的分辨率。
    - 将输入图像尺寸缩减为 **$416 \times 416$**，由于网络整体下采样总步长为 32，最终得到的**特征图 (Feature Map)** 尺寸刚好为奇数网格：**$13 \times 13$**（奇数网格更有利于让正中心落在一个单一格子里，便于捕捉中心点大物体）。
### 4. 维度聚类 (Dimension Clusters)

- **痛点**：传统 Anchor Boxes 的高宽维度通常是人为凭经验指定的（比如 $1:1, 1:2, 2:1$），网络之后需要花费大量力气去学习长宽转换系数，收敛极慢。
- **改进**：YOLOv2 抛弃了人工指定，改用 **K-Means 聚类算法 (K-Means Clustering)** 对训练集所有的真实边界框（Ground Truth）进行统计分析。
- **度量标准**：聚类时不使用传统的欧氏距离（因为大框会产生更大的绝对误差），而是采用 **交并比 (IoU, Intersection over Union)** 作为距离公式，强行让聚类结果专注于形状本身：$$d(\text{box}, \text{centroid}) = 1 - \text{IoU}(\text{box}, \text{centroid})$$
### 5. 直接位置预测 (Direct Location Prediction)

- **痛点**：若完全套用传统 Anchor 机制的偏移量公式，模型在训练初期会极不稳定。因为预测出来的偏移量可以在整张图上漫游，导致任何一个网格都有可能预测出极远处的物体，模型收敛极慢。
- **改进**：YOLOv2 强制实施“网格本地负责制”，不采用直接的绝对偏移量，而是预测相对于当前**网格单元 (Grid Cell)** 左上角的相对坐标位置，并通过一个 **Sigmoid / 逻辑斯蒂函数 (Logistic Function)** 将数值严格限制在 $0 \sim 1$ 之间。

$$\begin{aligned} b_x &= \sigma(t_x) + c_x \\ b_y &= \sigma(t_y) + c_y \\ b_w &= p_w e^{t_w} \\ b_h &= p_h e^{t_h} \end{aligned}$$

_(其中 $(c_x, c_y)$ 为当前网格左上角坐标，$p_w, p_h$ 为维度聚类出的先验 Anchor 宽高)_

- **效果**：结合**维度聚类**与**直接位置预测**后，**mAP 提升了 5%**。
### 6. 细粒度特征 (Fine-Grained Features)

- **核心思想**：为了提升小目标检测，模型引入转移层（Passthrough Layer / Space-to-Depth），把浅层高分辨率特征按空间位置重排到通道维，再与深层特征拼接。它不是残差加法连接，二者的数据变换与目标不同。
> [!tip] 大白话理解（Plain-language Intuition）
> Passthrough 把一张细网格图按 `2×2` 小块折叠到更多通道里，尺寸变小但局部细节没有直接丢掉，然后再交给深层特征一起判断小目标。
- **实现机制**：
    
    1. 提取浅层路径中大小为 $26 \times 26 \times 512$ 的高分辨率特征图。
    2. 进行**隔行隔列降采样采样（Re-org 变换）**，将其拆解并重组为 4 个大小为 $13 \times 13 \times 512$ 的新特征图。
    3. 通过 **拼接 (Concatenate)** 串联成一个 $13 \times 13 \times 2048$ 的特征图，并直接拼接到原本深层的 $13 \times 13 \times 1024$ 特征图上，融合后形成 $13 \times 13 \times 3072$ 的超级特征层。
- **效果**：**mAP 提升了 1%**。
### 7. 多尺度训练 (Multi-Scale Training)

- **优势**：由于 YOLOv2 内部彻底移除了全连接层，整流网络仅由卷积层和池化层构成，因此网络天然具备了**对任意输入尺寸的自适应性**。
- **做法**：在训练阶段，每隔 10 个 Epoch，网络就会从一组预设的尺寸中**随机选择**一个新的图片分辨率进行动态训练。
- **尺寸可选值**：因为降采样步长为 32，以 32 像素为增量梯度，范围从最小值 320 到最大值 608，可选集合为 $\{320, 352, 384, \dots, 608\}$，共计 10 种分辨率。
- **意义**：使得同一个模型可以在速度和精度之间自由切换。低 resolution 下适合低性能 GPU 或超高帧率场景，高 resolution 下适合静态高精度检测。

## 二、 “更快 (Faster)” —— 骨干网络 Darknet-19

为了突破检测速度，YOLOv2 抛弃了复杂度高、计算繁重的经典 **VGG-16 骨干网络**（VGG-16 在处理 $224 \times 224$ 图像时前向计算需要高达 306.9 亿次**浮点数运算 / FLOPs**），设计了全新的 **Darknet-19** 网络结构。
### 1. Darknet-19 的核心物理特性

- **计算效率极高**：一次前向传播仅需 **85.2 亿次** 浮点数计算，计算开销约为 VGG-16 的四分之一，而分类精度在 ImageNet 上仅低 2%（Top-5 准确率 88% vs 90%）。
- **网络设计范式**：
    - 大量采用 **$3 \times 3$ 卷积**：用于提取核心空间特征，保留空间上下文信息。
    - 巧妙嵌入 **$1 \times 1$ 卷积**：在 $3 \times 3$ 卷积之前用于压缩通道维度，大幅降低计算量和参数量。
    - 引入 **全局平均池化 (Global Average Pooling)**：完全替代最后重叠的全连接层，极大精简了模型体积。

## 三、 检测网络训练与输出张量配置 (Training & Output Details)
### 1. 分类网络预训练阶段 (Classification Pre-training)

1. **基础训练**：在 ImageNet 上使用标准的 $224 \times 224$ 大小输入训练 **160 个 Epoch**，采用 **随机梯度下降 (SGD)**，初始学习率为 0.1。
2. **高分辨率微调**：将分辨率提升至 $448 \times 448$，继续在 ImageNet 上训练 **10 个 Epoch**，将学习率降低到 0.001，使网络具备平滑处理高分辨率特征的能力。
### 2. 检测网络微调阶段 (Detection Fine-tuning)

- **网络改造**：切除 Darknet-19 分类网络最后的全局平均池化和 Softmax 分类层。
- **检测头替换**：新增三个 $3 \times 3 \times 1024$ 的卷积层，并在每一个后面尾随一个 $1 \times 1$ 的卷积层，输出通道数直接对齐最终的目标检测需求。同时在倒数第二层接入 **Passthrough Layer（转移层）** 进行多尺度特征拼接。
###  最终输出维度计算公式 (以 PASCAL VOC 为例)

- **配置参数**：预测位置设置有 **$5$ 个先验 Anchor 框** ($B = 5$)。
- **单个框预测值**：包含 4 个坐标值 $(x, y, w, h)$ + 1 个置信度 (Confidence) + 20 个类别概率值 ($C = 20$)。
- **最终维度**：$$\text{Output Channels} = B \times (5 + C) = 5 \times (5 + 20) = 125$$
    因此，在最终 $13 \times 13$ 的物理网格上，其输出的特征张量形状精确为 **$13 \times 13 \times 125$**。

**知识双链提示**：YOLOv2 通过聚类锚框和多尺度融合，攻克了 YOLOv1 对密集物体的漏检死穴。而这一套关于高低层特征图拼接（Concatenate）的策略，直接启发了后续 `[[YOLOv3]]` 中更加成熟的 `[[FPN (特征金字塔网络)]]` 架构设计。
## 3. YOLOv3：多尺度融合与独立逻辑分类（YOLOv3）

YOLOv3 在维持极高推理速度（$\text{FPS} \ge 36$）的同时，大幅提升了检测准确率。它不仅完美继承了 YOLOv1 和 YOLOv2 的核心精髓，更广泛汲取了残差网络、特征金字塔等其他优秀网络的设计思想，成为了工业界最经典的单阶段目标检测基准之一。

## 一、 经典继承与基石保留 (Inherited Features)

YOLOv3 对前两代算法的优秀底座进行了完全保留：

- **网格负责制**：延续从 YOLOv1 开始的**单元格划分 (Grid Cell Division)** 检测机制，通过判断物体的中心点落入哪个网格来决定由谁负责检测。
- **激活函数**：全线统一采用 **Leaky ReLU** 激活函数。
- **训练模式**：采用**端到端训练 (End-to-End Training)**。
- **层级组合**：延续 YOLOv2 的规范，将 **批归一化 (BN, Batch Normalization)** 和 **Leaky ReLU** 紧密衔接在每一个卷积层之后。
- **相对坐标预测**：位置信息预测完全基于相对于当前网格单元（Grid Cell）的左上角相对偏移量。
- **动态策略**：保留**多尺度训练 (Multi-Scale Training)** 机制，在推理速度与准确率之间做完美的权衡（Trade-off）。

## 二、 五大核心改进点 (Key Improvements)
### 1. 主干网络跃升：Darknet-53

- 将 YOLOv2 的 Darknet-19 升级为更深、更强大的 **Darknet-53**。同时为了端侧或轻量化部署，官方也提供了高速轻量的 **tiny-darknet** 架构。
### 2. 多尺度特征图检测 (Multi-Scale Feature Maps)

- 借鉴了 **SSD** 与 **特征金字塔网络 (FPN, Feature Pyramid Network)** 的多尺度特征提取思想。YOLOv3 同时在 3 个不同尺度的特征图上进行目标预测，极大攻克了前两代算法对**小目标检测 (Small Object Detection)** 效果差的远古死穴。
### 3. 先验锚框增至 9 个 (9 Anchor Boxes)

- **先验框 (Anchor Boxes)** 的数量从 YOLOv2 的 5 个增加到了 **9 个**。这 9 个尺寸依然是通过 **K-Means 维度聚类 (Dimension Clusters)** 算法在数据集上统计得出的。
### 4. 逻辑斯蒂分类器替代 Softmax (Logistic Classifier)

- 抛弃了传统的 Softmax 分类器，改用多个独立的 **逻辑斯蒂回归分类器 (Logistic Classifiers / Sigmoid)** 来预测类别。
### 5. 损失函数重构 (Loss Function Improvement)

- 将原本分类与置信度损失中的多分类交叉熵，全面替换为**二元交叉熵损失 (BCE Loss, Binary Cross-Entropy Loss)**。

## 三、 主干网络 Darknet-53 架构深度解构

Darknet-53 巧妙融合了 **残差连接 (Residual Connections)** 思想（即下表中的 `Residual` 模块），在加深网络深度的同时彻底避免了梯度消失。

|**序号**|**变换类型 (Type)**|**卷积核大小/步长 (Size/Stride)**|**输出特征图分辨率 (Output)**|**核心构成与重复次数**|
|---|---|---|---|---|
|1|Convolutional|$3 \times 3$|$256 \times 256 \times 32$|基础输入层|
|2|Convolutional|$3 \times 3 / 2$|$128 \times 128 \times 64$|下采样 (Downsample)|
|3|**Residual**|$1 \times 1$, $3 \times 3$|$128 \times 128 \times 64$|**重复 1 次**|
|4|Convolutional|$3 \times 3 / 2$|$64 \times 64 \times 128$|下采样 (Downsample)|
|5|**Residual**|$1 \times 1$, $3 \times 3$|$64 \times 64 \times 128$|**重复 2 次**|
|6|Convolutional|$3 \times 3 / 2$|$32 \times 32 \times 256$|下采样 (Downsample)|
|7|**Residual**|$1 \times 1$, $3 \times 3$|$32 \times 32 \times 256$|**重复 8 次** $\rightarrow$ **引出 52x52 检测头**|
|8|Convolutional|$3 \times 3 / 2$|$16 \times 16 \times 512$|下采样 (Downsample)|
|9|**Residual**|$1 \times 1$, $3 \times 3$|$16 \times 16 \times 512$|**重复 8 次** $\rightarrow$ **引出 26x26 检测头**|
|10|Convolutional|$3 \times 3 / 2$|$8 \times 8 \times 1024$|下采样 (Downsample)|
|11|**Residual**|$1 \times 1$, $3 \times 3$|$8 \times 8 \times 1024$|**重复 4 次** $\rightarrow$ **引出 13x13 检测头**|

## 四、 多尺度检测头与 Anchor 分配机制 (Multi-Scale Prediction)

YOLOv3 拥有 3 个独立的**检测头 (Head)**，利用类似 FPN 的上采样与拼接机制，将深层语义信息与浅层高分辨率几何信息进行**特征融合 (Feature Fusion)**。
### 1. 三大尺度与 Anchor 尺寸精准匹配

9 个聚类出的 Anchor 按照“大尺度特征图检测小物体，小尺度特征图检测大物体”的原则严密分配：

- **$13 \times 13$ 特征图（下采样 32x）**：感受野最大，负责检测**大物体 (Large Objects)**。
    - 分配 Anchor 尺寸：`(116x90), (156x198), (373x326)`。
- **$26 \times 26$ 特征图（下采样 16x）**：感受野中等，负责检测**中等物体 (Medium Objects)**。
    - 分配 Anchor 尺寸：`(30x61), (62x45), (59x119)`。
- **$52 \times 52$ 特征图（下采样 8x）**：感受野最小，分辨率最高，负责检测**小物体 (Small Objects)**。
    - 分配 Anchor 尺寸：`(10x13), (16x30), (33x23)`。
### 📐 检测头最终输出通道数（Output Channels）计算

以 **COCO 数据集** 为例（包含 $C = 80$ 个类别），每个特征图尺度上分配 $B = 3$ 个 Anchor 框。

$$\text{Channels} = B \times (5 + C) = 3 \times (4 \text{ 坐标} + 1 \text{ 置信度} + 80 \text{ 类别}) = 3 \times 85 = 255$$

因此，YOLOv3 最终预测输出 3 个张量（Tensor）对象：

1. **`13 x 13 x 255`**
2. **`26 x 26 x 255`**
3. **`52 x 52 x 255`**

## 五、 多标签分类与损失函数重构 (Multi-label Classification)
### 1. 为什么弃用 Softmax？

- **非排他性多标签场景**：Softmax 带有强烈的排他性假设（即它默认一个边界框只能强行归属于分数最高的那一个类别）。但在工业界实际场景中，目标类别往往存在**层级重叠或多标签**的情况（例如：一个框既属于“女人 `Woman`”，同时也属于“人 `Person`”）。
- **解决方案**：Softmax 被多个**独立的逻辑斯蒂分类器 (Logistic Regressors)** 完全替代。面对每个类别，网络只需执行一次 Sigmoid 二分类：“它是不是当前这个类别？”即可，实验证明这种做法在多标签任务中准确率完全不下降。
### 2. 损失函数 (Loss Function) 演进

YOLOv3 依然维持了传统的均方误差计算几何坐标，但将**置信度 (Confidence Loss)** 与 **类别概率 (Class Probability Loss)** 模块全部重构为了**二元交叉熵损失 (Binary Cross-Entropy Loss)**：

$$\text{Loss}_{\text{cls/conf}} = -\sum \left[ y \log(\sigma(t)) + (1 - y) \log(1 - \sigma(t)) \right]$$

_(在代码实现层面，对应的 PyTorch 算子为 `nn.BCEWithLogitsLoss`，TensorFlow 中对应 `tf.nn.sigmoid_cross_entropy_with_logits`)_

## 六、 样本匹配策略与推理流程 (Sample Matching & Inference)
### 1. 训练阶段的正负样本划分 (Training Phase)

在训练过程中，针对每一张图片的真实边界框（Ground Truth），9 个预设的 Anchor 会被划分为三类标签：

- **正样本 (Positive)**：真实框中心所在网格位置中，与该真实框形状最匹配的先验锚框负责预测；正样本计算坐标、目标性和类别损失。
- **忽略样本 (Ignored)**：预测框与某个真实框的 IoU 超过忽略阈值，但并非负责该真实框时，不把它作为无目标负样本惩罚；忽略主要作用于目标性损失，而不是宣称该预测在所有损失中永久失效。
- **负样本 (Negative)**：未被分配为正样本、也未落入忽略条件的候选，按背景参与目标性损失。
### 2. 测试推理阶段流程 (Inference Phase)

1. **大吞吐量边界框生成**：
    
    全图总共会预测出高达 **10647** 个边界框：
    
    $$\text{Total Boxes} = (13 \times 13 \times 3) + (26 \times 26 \times 3) + (52 \times 52 \times 3) = 507 + 2028 + 8112 = 10,647$$
    
2. **计算最终类别得分**：
    
    提取出预测的类别概率最大值 $C^* = \arg\max P_c$，并与该框的置信度相乘得到最终得分：
    
    $$\text{Score}_{\text{final}} = P_{c^*} \times \sigma(t_o)$$
    
3. **阈值过滤**：过滤掉所有 $\text{Score}_{\text{final}} < \text{Threshold}$ 的低分垃圾框。
4. **尺度恢复**：将特征图上的相对边界框坐标重新等比例放大回原始图像尺寸。
5. **NMS 消除冗余**：应用**非极大值抑制 (NMS)**，根据设定的 IoU 阈值强行剔除重叠的多余框，输出最终的目标检测结果。

> [!tip] 大白话理解（Plain-language Intuition）
> YOLOv1 用一张较粗的网格直接猜框；YOLOv2 给每个位置准备更贴近数据形状的锚框，并把浅层细节折叠进来；YOLOv3 再让三种分辨率的特征图分别照顾大、中、小目标。
## 4. 版本演化总表（Evolution Summary）

|版本（Version）|框表示|特征与检测尺度|分类方式|关键边界|
|---|---|---|---|---|
|YOLOv1|每格预测 $B$ 个框，无锚框先验|单一最终网格|每格条件类别概率|一个网格只负责一个真实目标，密集小目标受限|
|YOLOv2|聚类锚框 + 受限中心偏移|Darknet-19 + Passthrough|每锚框类别预测|多尺度训练改变输入分辨率与速度—精度折中|
|YOLOv3|9 个锚框分配到 3 个尺度|Darknet-53 + 三尺度预测|独立 Logistic 分类器|类别不强制互斥，仍需阈值与 NMS|
## 5. 参考资料（References）
- [You Only Look Once](https://arxiv.org/abs/1506.02640)
- [YOLO9000: Better, Faster, Stronger](https://arxiv.org/abs/1612.08242)
- [YOLOv3: An Incremental Improvement](https://arxiv.org/abs/1804.02767)
