---
title: YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）
tags:
  - data-science/deep-learning/computer-vision/object-detection/yolov4
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）

YOLOv4（2020年）是目标检测领域的集大成之作。它不仅是对 YOLOv3 的升级，更是一场目标检测先进技术的博览会。作者将当时计算机视觉界几乎所有有效的优化技巧整合在一起，分为 **Bag of Freebies**（免费赠品：只增加训练成本，不影响推理速度） 和 **Bag of Specials**（特价商品：轻微增加推理成本，但大幅提升性能），在维持高实时性（FPS）的同时，实现了准确率（AP）的巨大飞跃。

## 一、 YOLOv4 五大核心改进模块总览

YOLOv4 将网络架构科学地解构，并进行了全面升级：
![[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）-20260727112155631.png]]
1. **输入端 (Input)**：Mosaic / MixUp / CutMix / SAT 自对抗训练 / Label Smoothing (标签平滑)
2. **主干网络 (Backbone)**：CSPDarknet-53 / Mish 激活函数 / DropBlock
3. **颈部网络 (Neck)**：SPP (空间金字塔池化) / PAN (路径聚合网络)
4. **检测头 (Head)**：延续 YOLOv3 的锚框式多尺度耦合检测头，并调整边界框解码以消除网格敏感度；YOLOv4 不是后来 YOLOX/YOLOv8 意义上的解耦头。
5. **输出端 (Prediction)**：CIoU Loss / DIoU-NMS

## 二、 输入端硬核增强：花式数据增强与正则化

YOLOv4 极具前瞻性地组合了多种图像遮挡与多图组合技术，最大限度榨干数据集的潜力：
![[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）-20260727112212258.png|561]]
![[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）-20260727112241456.png]]
- **单一图片遮挡技术**：
    - **RandomErase / Cutout**：随机用均值或随机像素块擦除图像区域，强迫网络通过局部特征残片进行预测。
    ![[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）-20260727112304105.png|489]]
    - **Cutout**：在输入图像上遮挡连续矩形区域，使模型减少对局部显著特征的依赖；它不是“只对 CNN 第一层使用”的层内操作。
    ![[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）-20260727112838101.png|565]]
    - **Hide and Seek**:将图像分割成一个由 SxS 图像补丁组成的网格，根据概率设置随机隐藏一些补丁，从而让模型学习整个对象的样子，而不是单独一块，比如不单独依赖动物的脸做识别。
    ![[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）-20260727112336957.png|503]]
	- **Grid Mask**：将图像的区域隐藏在网格中，作用也是为了让模型学习对象的整个组成部分。
    ![[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）-20260727112405914.png|475]]
    - **MixUp**：两张图像及其标签按比例进行凸面叠加。
     ![[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）-20260727112855285.png|207]]
- **多图组合技术**：
    - **CutMix**：将一张图的裁剪区域直接粘贴到另一张图上。
    ![[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）-20260727112923181.png|355]]
    - **Mosaic（马赛克增强）**：将 4 张图片随机缩放、裁剪和排布后拼接，同时变换各图的边界框。它增加单张训练输入中的场景与尺度多样性，并让小目标更常出现；不等价于把有效批量大小无条件扩大 4 倍。
    ![[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）-20260727113024110.png]]
- **自对抗训练 (SAT, Self-Adversarial Training)**：利用对抗攻击思想。CNN 先计算出 Loss，通过反向传播**修改图片像素**（不改变网络权重），制造出“图中没有目标”的假象，随后让网络对修改后的图进行正常检测，大幅提升了模型的抗干扰鲁棒性。
![[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）-20260727113042962.png|588]]
- **类标签平滑 (Class Label Smoothing)**：Class label smoothing是一种正则化方法。如果神经网络过度拟合和/或过度自信，我们都可以尝试平滑标签。也就是说在训练时标签可能存在错误，而我们可能“过分”相信训练样本的标签，并且在某种程度上没有审视了其他预测的复杂性。因此为了避免过度相信，更合理的做法是对类标签表示进行编码，以便在一定程度上对不确定性进行评估。YOLO V4使用了类平滑，选择模型的正确预测概率为0.9，例如[0,0,0,0.9,0...,0 ]。将硬标签（如 `[0, 1]`）转化为软标签（如 `[0.05, 0.95]`）。避免模型在训练时对标签“过度自信”，从而实现更好的泛化特征聚类。
![[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）-20260727113054422.png]]

## 三、 主干网络升级：CSPDarknet-53 架构与 Mish 激活

YOLOv4 将主干网络升级为 CSPDarknet-53，引入了两项关键改变：

1. **CSP 结构（跨阶段局部网络）**：源自 DenseNet 的思想，将输入特征图按通道划分为两部分。第一支路进行正常的残差卷积提取特征；第二支路直接跨越复杂卷积层进行 Skip Connection（捷径跳连），最后进行通道拼接（Concat）。这一设计巧妙地**解决了梯度信息重复问题**，支持特征重用，在保住准确性的同时大幅降低了计算量（FLOPs）与内存成本。
2. **Mish 激活函数**：在主干的论文配置中采用 Mish，检测器其他部分仍可能使用不同激活，不能写成所有层“全线替换”。
    
    $$Mish(x) = x \cdot \tanh(\ln(1 + e^x))$$
    
    Mish 平滑且非单调，论文把它作为候选激活之一；具体增益取决于主干、训练配方与数据集，不保留无协议的固定 `3%~5%` 说法。
    
3. **DropBlock 机制**：传统的 Dropout 随机丢弃单个独立像素，而卷积层局部相关性极强，网络极易通过周围像素猜出特征。DropBlock 直接强行丢弃一整块连续的局部区域，彻底切断了局部作弊通道，抗过拟合能力极强。

## 四、 颈部网络加强：SPP 与 PAN 完美聚合

1. **SPP 模块 (Spatial Pyramid Pooling)**：在 Backbone 之后加入恒等分支与 $5\times5$、$9\times9$、$13\times13$ 最大池化分支，再沿通道拼接；相邻的 $1\times1$ 是卷积，不是第四种池化核。相同步长池化保持空间尺寸，同时扩大感受野。
2. **PAN 路径聚合（Path Aggregation）**：在 FPN 自顶向下融合之外增加自底向上的信息路径，缩短低层定位信息到检测头的传播距离。YOLOv4 使用的是针对检测颈部调整后的 PAN 思想，不能把原 PANet 的所有模块都默认视为启用。
> [!tip] 大白话理解（Plain-language Intuition）
> SPP 让同一张特征图同时通过不同大小的“观察窗”，既看局部也看更大上下文；PAN 再让高层语义往下传、底层位置往上传，三种检测尺度都拿到更完整的信息。

## 五、 输出端变革：解耦优化与 CIoU 进化

1. **消除网格敏感度**：传统公式中中心点预测包含 Sigmoid 函数 $\sigma(t_x)$，其输出范围严格在 $(0, 1)$，导致模型很难预测刚好落在单元格边缘的目标。YOLOv4 在 Sigmoid 前乘以大于 1 的系数（如 1.05），让预测范围成功溢出网格边缘。
2. **CIoU Loss**：同时考虑 IoU、中心点距离与长宽比一致性，为没有重叠或长宽比例失配的预测提供更明确梯度。它不是所有框损失唯一线性的“终点”。
3. **DIoU-NMS**：把中心距离纳入抑制度量，可能减少相邻实例被标准 IoU-NMS 错误压制的情况；最终效果仍依赖阈值与场景。
## 六、 免费技巧与特殊技巧（Bag of Freebies and Bag of Specials）
- **免费技巧（Bag of Freebies, BoF）**：主要增加训练成本而不增加部署时前向结构成本，例如数据增强、标签平滑、CIoU Loss。
- **特殊技巧（Bag of Specials, BoS）**：通常小幅增加推理成本但改善感受野或特征融合，例如 SPP、PAN、SAM 等。
- “免费”只指推理图不增加相应模块，不代表训练时间、调参和数据管线没有成本。
## 七、 参考资料（References）
- [YOLOv4: Optimal Speed and Accuracy of Object Detection](https://arxiv.org/abs/2004.10934)
- [Cross Stage Partial Network](https://arxiv.org/abs/1911.11929)
- [Distance-IoU Loss](https://arxiv.org/abs/1911.08287)
    
