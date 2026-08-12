---
title: R-CNN 系列两阶段检测器演化（Evolution of Two-stage R-CNN Detectors）
tags:
  - data-science/deep-learning/computer-vision/object-detection/two-stage
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# R-CNN 系列两阶段检测器演化（Evolution of Two-stage R-CNN Detectors）
## 1. 两阶段检测范式（Two-stage Detection Paradigm）
两阶段检测器（Two-stage Detector）把任务拆为：先生成可能含目标的候选区域（Region Proposal），再对候选区域分类并回归更准确的边界框。R-CNN 系列的主要演进方向是让更多计算共享，并逐步把独立模块纳入可训练网络。
> [!tip] 大白话理解（Plain-language Intuition）
> 第一阶段像在大图上圈出“这些位置值得细看”，第二阶段再逐个确认“是什么、框该怎么修”。早期方法给每个圈单独跑一遍卷积，后续方法先整图算一次特征，让所有圈共享，最后又把“怎么圈”本身交给网络学习。
## 2. R-CNN：候选区域逐个提取特征（Regions with CNN Features）
### 2.1 推理流程（Inference Pipeline）
1. 使用选择性搜索（Selective Search）从大量可能窗口压缩到约 2,000 个类别无关候选区域。
2. 将每个候选区域裁剪或变形（Warp）为 CNN 所需的固定输入尺寸；各向异性缩放会造成几何扭曲，各向同性缩放可用平均颜色填充外围。
3. 每个候选区域分别通过 CNN，得到固定长度特征向量。
4. 每类线性支持向量机（Linear Support Vector Machine, Linear SVM）执行分类。
5. 类别特定的边界框回归器（Bounding-box Regressor）修正位置，最后用 NMS 去除重复框。
选择性搜索、IoU 与 NMS 的算法细节见前置笔记；本节重点是它们在 R-CNN 管线中的位置。
### 2.2 训练阶段（Training Stages）
- 先在大规模分类数据上预训练 CNN。
- 用检测候选区域对 CNN 微调（Fine-tuning）。
- 将提取出的特征写入磁盘，分别训练 SVM 分类器与边界框回归器。
- 多阶段目标和数据准备彼此分离，训练复杂且磁盘占用大。
### 2.3 主要瓶颈（Main Bottlenecks）
- 约 2,000 个重叠候选区域分别执行 CNN，重复计算严重，单图检测慢。
- 候选特征落盘会消耗大量存储。
- 分类、定位和特征微调不是单一端到端目标。
## 3. SPP-net：一次卷积，共享候选特征（Spatial Pyramid Pooling Network）
空间金字塔池化网络（Spatial Pyramid Pooling Network, SPP-net）先对整张图计算卷积特征图，再对任意尺寸候选区域执行多层级空间池化，拼接成固定长度向量。
- 传统固定尺寸输入常通过裁剪或拉伸实现，可能丢失内容或扭曲几何。
- SPP 在不同网格层级内做最大池化，例如 `1×1`、`2×2`、`4×4`，拼接后长度固定。
- 所有候选共享一次卷积特征，避免把重叠区域逐个送入 CNN。
> [!tip] 大白话理解（Plain-language Intuition）
> R-CNN 像先把蛋糕切成 2,000 块，再把每块单独烤；SPP-net 是先把整块蛋糕烤好，再按候选区域切片并用固定格子汇总。最贵的“烘烤”只做一次。
### 3.1 边界（Boundary）
原始 SPP-net 的深层卷积层在检测微调时受限，这也是 Fast R-CNN 进一步改进联合训练的重要背景。
## 4. Fast R-CNN：RoI Pooling 与多任务联合训练（Fast R-CNN）
Fast R-CNN 保留外部候选区域生成，但把特征提取、分类与边界框回归整合进一个网络：
1. 整张图像只通过卷积主干一次。
2. 将每个候选框映射到共享特征图。
3. RoI 池化（Region of Interest Pooling, RoI Pooling）把不同大小的 RoI 量化并池化为固定空间尺寸，例如 `7×7`。
4. 全连接层后的两个同级输出分别给出 Softmax 类别分布和类别特定的边界框偏移。
5. 使用多任务损失联合优化分类与定位。
### 4.1 RoI Pooling（Region of Interest Pooling）
RoI Pooling 将候选边界量化到离散特征格，再划分固定数量的池化格，每格做最大池化。它解决全连接层需要固定输入长度的问题，但两次量化会产生位置误差；这一缺点在 Mask R-CNN 中由 RoIAlign 解决。
### 4.2 仍未解决的问题（Remaining Limitation）
候选区域仍由选择性搜索等外部算法生成，候选步骤不能通过检测损失学习，且可能成为 CPU 侧瓶颈。
## 5. Faster R-CNN：可学习的区域提议网络（Faster R-CNN）
Faster R-CNN 使用区域提议网络（Region Proposal Network, RPN）替代外部选择性搜索。RPN 与检测头共享主干特征图，使候选生成也能学习。
### 5.1 RPN 工作过程（RPN Procedure）
1. 在共享特征图上用小型滑动卷积提取局部表示。
2. 为每个空间位置放置 $k$ 个不同尺度和长宽比的锚框（Anchor）。经典论文示例组合 3 个尺度与 3 个比例，得到 $k=9$；这是论文配置，不是通用定律。
3. 每个锚框输出目标性（Objectness）分数和 4 个边界框偏移。
4. 按分数筛选、裁剪到图像边界、移除过小框并执行 NMS，保留少量提议送入 Fast R-CNN 检测头。
5. RPN 与检测器交替或近似联合训练，共享卷积权重。
> [!tip] 大白话理解（Plain-language Intuition）
> Fast R-CNN 仍要等外部程序递来“可疑位置清单”；Faster R-CNN 在共享特征图旁增加一个轻量侦察员，让侦察员自己学会递清单，随后主检测头做精审。
### 5.2 损失职责（Loss Responsibilities）
- RPN 分类损失判断锚框是前景还是背景。
- RPN 回归损失只对正锚框修正坐标。
- 第二阶段检测头输出具体类别与更精细的边界框回归。
- 正负阈值、采样比例、候选数与 NMS 阈值属于具体实现配置，必须查所用框架。
## 6. R-FCN：位置敏感的全卷积检测头（Region-based Fully Convolutional Network）
R-FCN 继续减少每个 RoI 独立执行的计算。它在整图共享特征上生成位置敏感得分图（Position-sensitive Score Maps），把一个 RoI 分成 $k×k$ 个相对位置格，每格只从对应的位置敏感通道池化，最后聚合分类分数。
- **平移不变性（Translation Invariance）**有利于分类：目标移到别处仍应认成同一类别。
- **平移变化性（Translation Variance）**有利于定位：模型必须知道目标各部件相对框的位置。
- 位置敏感 RoI 池化在共享卷积与定位敏感性之间折中，减少 Fast/Faster R-CNN 中较重的逐 RoI 全连接计算。
> [!tip] 大白话理解（Plain-language Intuition）
> 普通分类只问“像不像猫”；检测还关心“猫头是否在框的上部、猫脚是否在下部”。R-FCN 为框内不同格子准备不同通道，让分类结果保留空间角色。
## 7. 演化对比（Evolution Comparison）

|模型（Model）|候选来源|卷积计算共享|候选后处理|主要改进|
|---|---|---|---|---|
|R-CNN|选择性搜索|否，每个候选独立|Warp/Crop 后 CNN|CNN 特征替代手工特征|
|SPP-net|外部候选|是|空间金字塔池化|任意尺寸转固定向量|
|Fast R-CNN|外部候选|是|RoI Pooling|分类与回归联合训练|
|Faster R-CNN|RPN|是|RoI Pooling|候选区域可学习且共享特征|
|R-FCN|RPN|是，连检测头也更共享|位置敏感 RoI Pooling|减少逐 RoI 计算并保留定位信息|
## 8. 与一阶段检测器的边界（Boundary with One-stage Detectors）
一阶段检测器直接在密集位置输出类别与边界框，不显式运行“候选提议后再分类”的第二阶段，通常更利于低延迟；两阶段方法通过少量提议上的精细分类与回归获得不同的速度—精度折中。实际系统还会出现混合设计，不能只凭是否使用 FPN、Anchor 或 NMS 判断阶段数。
## 9. 参考资料（References）
- [R-CNN](https://arxiv.org/abs/1311.2524)
- [SPP-net](https://arxiv.org/abs/1406.4729)
- [Fast R-CNN](https://arxiv.org/abs/1504.08083)
- [Faster R-CNN](https://arxiv.org/abs/1506.01497)
- [R-FCN](https://arxiv.org/abs/1605.06409)
