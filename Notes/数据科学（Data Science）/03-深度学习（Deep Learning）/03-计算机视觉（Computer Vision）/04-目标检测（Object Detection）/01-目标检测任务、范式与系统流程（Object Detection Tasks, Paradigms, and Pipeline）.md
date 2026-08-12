---
title: 目标检测任务、范式与系统流程（Object Detection Tasks, Paradigms, and Pipeline）
tags:
  - data-science/deep-learning/computer-vision/object-detection/fundamentals
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# 目标检测任务、范式与系统流程（Object Detection Tasks, Paradigms, and Pipeline）
## 1. 任务定义（Task Definition）
目标检测（Object Detection）同时回答两个问题：图像中有什么，以及每个目标在哪里。模型通常为每个实例输出类别标签（Class Label）、边界框（Bounding Box）和置信度分数（Confidence Score）。
> [!tip] 大白话理解（Plain-language Intuition）
> 图像分类只需要说“这张图里有猫”；目标检测还要分别指出“哪一块是猫、哪一块是狗”。当目标重叠、尺寸很小或背景复杂时，模型既不能认错，也不能把框画偏。
### 1.1 与相关视觉任务的区别（Related Vision Tasks）

|任务（Task）|典型输出（Typical Output）|是否区分同类实例|
|---|---|---|
|图像分类（Image Classification）|整张图的类别|不适用|
|目标定位（Object Localization）|一个主要目标的类别与边界框|通常只考虑一个目标|
|目标检测（Object Detection）|多个实例的类别、边界框和分数|是|
|语义分割（Semantic Segmentation）|每个像素的语义类别|否|
|实例分割（Instance Segmentation）|每个实例的像素掩码与类别|是|
### 1.2 主要难点（Core Challenges）
- **尺度变化（Scale Variation）**：同一类别可能只占几个像素，也可能覆盖大部分图像。
- **遮挡（Occlusion）与拥挤（Crowding）**：实例相互遮挡，预测框高度重叠。
- **姿态与外观变化（Pose and Appearance Variation）**：视角、光照、形变和纹理改变。
- **类别不平衡（Class Imbalance）**：背景候选远多于前景目标，小众类别样本也可能不足。
- **定位与分类耦合（Localization–Classification Coupling）**：类别正确但框不准，或框准确但类别错误，都不能视为完整检测成功。
## 2. 传统目标检测流程（Traditional Detection Pipeline）
深度学习普及前，常见流程包含三个阶段：
1. **候选区域生成（Region Proposal Generation）**：滑动窗口（Sliding Window）或选择性搜索（Selective Search）提出可能含目标的区域。
2. **人工特征提取（Hand-crafted Feature Extraction）**：使用尺度不变特征变换（Scale-Invariant Feature Transform, SIFT）、方向梯度直方图（Histogram of Oriented Gradients, HOG）或 Haar 特征描述区域。
3. **分类与定位（Classification and Localization）**：支持向量机（Support Vector Machine, SVM）等分类器判断目标类别；部分系统再回归边界框。
分类器通常包含 $N$ 个目标类别与一个背景类别，即 $N+1$ 类。形变部件模型（Deformable Part Model, DPM）把对象表示为根部件与可形变子部件的组合，是传统方法的重要代表。
> [!tip] 大白话理解（Plain-language Intuition）
> 传统系统像流水线：先大量裁图，再靠人工设计的“边缘和纹理尺子”量每块区域，最后交给分类器判断。每一步由不同算法负责，错误会沿流水线累积。
### 2.1 滑动窗口与选择性搜索（Sliding Window and Selective Search）
- **滑动窗口（Sliding Window）**：用多种尺寸与长宽比遍历图像。覆盖全面，但候选数巨大且高度重复。
- **启发式窗口剪枝（Heuristic Pruning）**：限制尺寸、比例或位置；在固定视角场景可能有效，但通用性有限。
- **选择性搜索（Selective Search）**：利用分割区域的颜色、纹理、尺寸与填充关系逐步合并，产生类别无关的候选区域；它是早期 R-CNN 的关键组件，详见 [[候选区域与选择性搜索（Region Proposals and Selective Search）]]。
## 3. 深度学习检测器的共同组件（Common Components）
现代检测器通常由以下模块组合：
- **主干网络（Backbone）**：从图像中提取多层视觉特征，例如 ResNet、MobileNet 或 CSP 系列。
- **颈部网络（Neck）**：融合不同分辨率和语义层级的特征，例如特征金字塔网络（Feature Pyramid Network, FPN）与路径聚合网络（Path Aggregation Network, PAN）。FPN 是特征融合模块，不应单独归类为一阶段检测器。
- **检测头（Detection Head）**：输出类别分数、目标存在性（Objectness）和边界框参数；可以是耦合头或解耦头。
- **标签分配（Label Assignment）**：决定哪些预测位置或锚框负责哪些真实框。
- **损失函数（Loss Function）**：组合分类损失、目标存在性损失和边界框回归损失。
- **后处理（Post-processing）**：按置信度筛选，并使用非极大值抑制（Non-Maximum Suppression, NMS）等方法消除重复框。
## 4. 两阶段检测器（Two-stage Detectors）
两阶段检测器采用“先提出候选区域，再分类和精修”的主流程：
1. 第一阶段生成候选区域（Region Proposal）。早期 R-CNN 使用选择性搜索；Faster R-CNN 使用区域生成网络（Region Proposal Network, RPN）。
2. 第二阶段从候选区域提取固定尺寸特征，完成类别预测和边界框回归。
代表模型包括 R-CNN、SPP-net、Fast R-CNN、Faster R-CNN 和 R-FCN。
> [!tip] 大白话理解（Plain-language Intuition）
> 两阶段方法像先让侦察员圈出“这里可能有东西”，再让专家逐框鉴定并修正位置。候选框减少了无意义搜索，但候选生成和逐区域处理会增加流程与延迟。
### 4.1 优势与代价（Advantages and Costs）
- 候选区域能聚焦前景，通常便于获得较高定位质量。
- 流程较复杂，训练、导出和推理包含更多中间结构。
- “两阶段一定更准、一阶段一定更快”只是历史上的常见趋势，不是跨模型、硬件和输入尺寸都成立的定律。
## 5. 一阶段检测器（One-stage Detectors）
一阶段检测器直接在密集特征图上预测类别与边界框，不先运行独立的候选区域分类阶段。代表模型包括 SSD、YOLO 系列和 RetinaNet。
> [!tip] 大白话理解（Plain-language Intuition）
> 一阶段方法让一张特征图上的大量位置同时回答“这里有没有目标、是什么、框多大”。它把流水线压进一次网络前向传播，但必须处理大量背景预测和重复框。
### 5.1 锚框式与无锚框式（Anchor-based and Anchor-free）
- **锚框式检测（Anchor-based Detection）**：在每个位置放置多个预设尺度和长宽比的锚框，网络预测相对偏移和类别。Faster R-CNN、SSD、原始 YOLOv2/v3/v5 属于典型锚框式设计。
- **无锚框检测（Anchor-free Detection）**：直接预测中心点、角点或到边界的距离，避免显式预设锚框。YOLOv1 直接从网格预测框；FCOS 和 Ultralytics YOLOv8 使用现代无锚框设计。
- **边界说明（Boundary）**：无锚框不等于没有参考点、网格或标签分配规则；它只表示回归不依赖一组预定义锚框尺寸。
## 6. 训练与推理流程（Training and Inference）
### 6.1 训练阶段（Training Phase）
1. 读取图像与真实标注（Ground Truth）。
2. 执行缩放、裁剪、翻转或颜色扰动等数据增强（Data Augmentation），同步变换边界框。
3. 主干与颈部提取、融合多尺度特征。
4. 标签分配器把真实框分配给预测位置或锚框。
5. 计算分类、目标存在性与边界框回归损失。
6. 反向传播并更新参数。
### 6.2 推理阶段（Inference Phase）
1. 按模型要求预处理图像，并记录缩放和填充参数。
2. 网络输出密集预测。
3. 将回归参数解码为图像坐标，并把坐标还原到原图尺度。
4. 使用置信度阈值去除低分预测。
5. 使用 NMS、Soft-NMS 或模型规定的端到端筛选策略去重。
6. 输出类别、分数与最终边界框。
## 7. 学习依赖与笔记导航（Learning Dependencies）
- 评估检测结果：[[目标检测评估指标：IoU、Precision、Recall、AP 与 mAP（Object Detection Metrics）]]。
- 传统候选区域：[[候选区域与选择性搜索（Region Proposals and Selective Search）]]。
- 锚框与训练匹配：[[锚框、样本匹配与边界框回归（Anchors, Label Assignment, and Box Regression）]]。
- 重复框后处理：[[非极大值抑制与 Soft-NMS（Non-Maximum Suppression and Soft-NMS）]]。
- 特征提取前置知识：[[ResNet 残差学习与快捷连接（ResNet Residual Learning and Shortcut Connections）]]、[[MobileNet 深度可分离卷积与端侧网络（MobileNet Depthwise Separable Convolution and Edge Networks）]]。
## 参考资料（References）
- [Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)
- [You Only Look Once: Unified, Real-Time Object Detection](https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html)
- [FCOS: Fully Convolutional One-Stage Object Detection](https://openaccess.thecvf.com/content_ICCV_2019/html/Tian_FCOS_Fully_Convolutional_One-Stage_Object_Detection_ICCV_2019_paper.html)
