---
title: 目标检测关联视觉模块：FCN、实例分割、RoIAlign 与 FPN（Related Vision Modules）
tags:
  - data-science/deep-learning/computer-vision/segmentation
  - data-science/deep-learning/computer-vision/feature-pyramid
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# 目标检测关联视觉模块：FCN、实例分割、RoIAlign 与 FPN（Related Vision Modules）
## 1. 像素级视觉任务（Pixel-level Vision Tasks）
### 1.1 语义分割（Semantic Segmentation）
语义分割为每个像素预测类别，同类实例共享同一语义标签；它能区分“人”和“背景”，但不区分图中两个不同的人。
![](https://pic3.zhimg.com/v2-61ad8591d5821305f0fc7e479f76b420_1440w.jpg)
### 1.2 实例分割（Instance Segmentation）
实例分割既预测像素类别，也分开同类的不同实例。输出通常为每个实例的类别、边界框、分数与二值掩码（Binary Mask）。
> [!tip] 大白话理解（Plain-language Intuition）
> 语义分割像用同一种颜色涂出所有“人”；实例分割还要给第一个人、第二个人分别剪出独立蒙版，即使两个人互相遮挡也不能粘成一块。
## 2. 全卷积网络（Fully Convolutional Network, FCN）
FCN 把分类 CNN 末端的全连接层改写为卷积层，使网络保留空间布局并输出低分辨率类别得分图，再通过可学习上采样恢复到输入尺度，对每个像素分类。
![](https://pic3.zhimg.com/v2-c94821f911754203a4e88fe210bbaeb4_1440w.jpg)
### 2.1 为什么需要跳跃连接（Skip Connection）
- 深层特征语义强，但分辨率低，边缘与小结构容易丢失。
- 浅层特征分辨率高，但语义弱。
- FCN-32s 只从最深层一次上采样；FCN-16s 和 FCN-8s 逐步融合较浅池化层，改善边界细节。
![](https://pic1.zhimg.com/v2-f08cfed129e91c78f46acd8dfec4e456_1440w.jpg)
> [!tip] 大白话理解（Plain-language Intuition）
> 深层网络知道“这大概是一只狗”，却只剩粗糙的小地图；浅层网络保留毛发边缘，却不知道那是什么。跳跃连接把“懂语义的粗地图”和“有边缘的细地图”叠起来。
### 2.2 上采样术语边界（Upsampling Terminology）
原稿把所有恢复尺寸操作称为“反卷积”。更准确的术语是转置卷积（Transposed Convolution）；它不是数学意义上的卷积逆运算。实际模型也可使用双线性插值后接普通卷积。
## 3. Mask R-CNN：检测与实例掩码并行（Mask R-CNN）
Mask R-CNN 在 Faster R-CNN 基础上，为每个 RoI 增加与分类、边界框回归并行的掩码分支。掩码分支用小型 FCN 为每个类别预测固定分辨率的二值掩码。
![](https://pic4.zhimg.com/v2-fef452697c46c4fd632b99a010f9ede1_1440w.jpg)
- **分类分支（Classification Branch）**：判断 RoI 是什么类别。
- **回归分支（Regression Branch）**：修正边界框。
- **掩码分支（Mask Branch）**：在 RoI 内预测逐像素前景概率。
- 掩码（Mask）在计算机视觉中表示覆盖区域；二值掩码通常用 1 表示该实例像素、0 表示背景，不同实例各有一张独立掩码。
> [!note] 数据集说明（Dataset Note）
> COCO 提供实例分割标注并广泛用于 Mask R-CNN 训练与评估，但它不是历史上第一个提供实例分割标注的数据集；正文不保留这一错误绝对化说法。
## 4. RoI Pooling 的量化误差（Quantization Error）
RoI Pooling 把连续坐标映射到离散特征格，并把每个池化分箱边界取整。检测框只要求近似位置时误差可能可接受，但逐像素掩码对边界偏移很敏感。
![](https://pic4.zhimg.com/v2-27625d7c8330f52783de70810ee06ced_1440w.jpg)
## 5. RoIAlign：保留连续坐标（Region of Interest Align）
RoIAlign 移除 RoI 边界和分箱边界的取整：
1. 保留映射到特征图后的浮点坐标。
2. 在每个分箱内选择规则采样点。
3. 用双线性插值（Bilinear Interpolation）从相邻四个特征位置计算采样值。
4. 对采样值执行最大或平均聚合，得到固定尺寸 RoI 特征。
![](https://pic3.zhimg.com/v2-3423d6826100cb056970953fa0bfb7f2_1440w.jpg)
### 5.1 双线性插值（Bilinear Interpolation）
设采样点位于四个格点之间，先沿一个轴做两次线性插值，再沿另一轴对中间结果插值；权重由距离决定且总和为 1。它近似连续位置的特征，不需要把 RoI 强行移动到整数格。
> [!tip] 大白话理解（Plain-language Intuition）
> RoI Pooling 像把框边缘四舍五入到方格线，框会被轻微挪动；RoIAlign 不挪框，而是在真实浮点位置用周围四格“按距离调色”，因此掩码边缘更能对齐原目标。
## 6. 特征金字塔网络（Feature Pyramid Network, FPN）
FPN 利用 CNN 天生的多尺度层级，通过自顶向下路径（Top-down Pathway）与横向连接（Lateral Connection），构建每个尺度都具有强语义的特征图。
![](https://pic2.zhimg.com/v2-a100c9646ce6f89bb1d9ab8440a8a96d_1440w.jpg)
### 6.1 构建流程（Construction）
1. 自底向上的主干产生不同分辨率特征 $C_2,C_3,C_4,C_5$。
2. 从最深层开始，用 `1×1` 横向卷积统一通道数。
3. 高层特征上采样 2 倍，与相邻浅层横向特征逐元素相加。
4. 每个融合结果通常再经 `3×3` 卷积，得到 $P_2,P_3,P_4,P_5$，减少上采样混叠影响。
5. 不同尺寸 RoI 或密集检测头分配到合适金字塔层。
### 6.2 为什么能处理多尺度（Why It Helps Multi-scale Objects）
- 浅层有精细空间位置，适合小目标，但原始语义较弱。
- 深层有大感受野和强语义，适合大目标，但分辨率低。
- 自顶向下融合把强语义传给高分辨率层，避免对每个输入图像尺度分别跑一遍完整主干。
> [!tip] 大白话理解（Plain-language Intuition）
> 小目标需要“放大地图”才能看见，大目标需要“缩小地图”才能看全。FPN 准备多张比例尺不同、但都标好语义的地图，让不同大小目标去合适的地图上被检测。
### 6.3 使用边界（Boundaries）
- FPN 是通用多尺度特征提取器，不等同于一阶段或两阶段检测器。
- Faster/Mask R-CNN、RetinaNet 和许多 YOLO 颈部都可采用金字塔思想，但具体融合方式不同。
- PANet 在 FPN 自顶向下路径之外增加自底向上的路径聚合，不能与原始 FPN 混为同一结构。
## 7. 模块关系（Module Relationships）

|模块（Module）|解决的问题|典型输入|典型输出|
|---|---|---|---|
|FCN|整图逐像素分类|整图特征|语义类别图|
|Mask R-CNN 掩码头|区分每个实例的像素|每个 RoI 特征|实例二值掩码|
|RoIAlign|避免 RoI 特征量化错位|浮点 RoI + 特征图|固定尺寸对齐特征|
|FPN|多尺度目标的语义与分辨率融合|多层主干特征|多层语义金字塔|
## 8. 参考资料（References）
- [Fully Convolutional Networks for Semantic Segmentation](https://arxiv.org/abs/1411.4038)
- [Mask R-CNN](https://arxiv.org/abs/1703.06870)
- [Feature Pyramid Networks for Object Detection](https://arxiv.org/abs/1612.03144)
