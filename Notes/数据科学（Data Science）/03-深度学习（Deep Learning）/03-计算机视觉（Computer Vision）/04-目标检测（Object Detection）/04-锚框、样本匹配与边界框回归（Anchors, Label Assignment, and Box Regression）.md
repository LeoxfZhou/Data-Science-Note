---
title: 锚框、样本匹配与边界框回归（Anchors, Label Assignment, and Box Regression）
tags:
  - data-science/deep-learning/computer-vision/object-detection/anchors
  - data-science/deep-learning/computer-vision/object-detection/label-assignment
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# 锚框、样本匹配与边界框回归（Anchors, Label Assignment, and Box Regression）
## 1. 锚框的作用（Purpose of Anchors）
锚框（Anchor Box）是在特征图位置上预先定义的参考框，具有指定尺度（Scale）与长宽比（Aspect Ratio）。锚框式检测器不直接从任意坐标开始预测，而是分类锚框并回归它相对真实框的偏移。
> [!tip] 大白话理解（Plain-language Intuition）
> 锚框像预先准备的不同尺寸纸样：模型先选最接近目标形状的纸样，再说明中心应移动多少、宽高应缩放多少。纸样提供起点，但选错数量和比例也会制造大量无用候选。
### 1.1 解决的问题与边界（Benefits and Boundaries）
- 一个位置可放置多个锚框，使其能同时提出不同尺度、比例的候选。
- 相对偏移通常比直接回归绝对像素坐标更易参数化。
- 锚框本身不保证高召回率或快速收敛，效果依赖覆盖率、匹配策略、损失与数据。
- YOLOv1 的网格责任限制不能简单归因于“没有锚框”；其每个网格可预测多个框，但类别预测与包含目标中心的网格绑定，密集相邻目标仍受结构约束。
## 2. 锚框尺寸设计（Anchor Shape Design）
### 2.1 人工尺度与长宽比（Manual Scales and Ratios）
Faster R-CNN 的经典 RPN 在每个滑动位置组合多个尺度和长宽比。常见教材示例是 3 个尺度乘 3 个比例形成 9 个锚框，但实际配置应依据特征步长、输入尺寸和数据分布。
### 2.2 宽高聚类（Width–Height Clustering）
YOLOv2 使用训练集真实框宽高执行 $k$-means，并采用：
$$
d(box,centroid)=1-\operatorname{IoU}(box,centroid)
$$
该距离关注形状重叠而非大框主导的欧氏距离。聚类前必须明确宽高是否按输入尺寸归一化，以及不同检测尺度如何分配聚类中心。
### 2.3 覆盖率检查（Coverage Check）
- 统计每个真实框与最佳锚框的最大 IoU。
- 按目标尺寸和长宽比检查低覆盖群体。
- 重新设计输入分辨率、特征步长或锚框，而不是只增加锚框数量。
## 3. 标签分配（Label Assignment）
标签分配决定每个锚框是正样本（Positive）、负样本（Negative）还是忽略样本（Ignored）。典型静态规则包括：
1. 与某个真实框 IoU 高于正阈值的锚框设为正样本。
2. 即使未达到正阈值，也可保证每个真实框的最佳 IoU 锚框为正样本，避免真实目标无人负责。
3. 与所有真实框 IoU 低于负阈值的锚框设为背景负样本。
4. 位于两个阈值之间的锚框忽略，不参与部分或全部损失。
教材中常用 `IoU > 0.5` 作为正样本、`IoU < 0.3` 作为负样本、中间区间忽略的示例；这些数值不是所有检测器的默认契约。
> [!tip] 大白话理解（Plain-language Intuition）
> 标签分配像安排导师：与真实框最合适的候选负责学习它，明显不合适的学习背景，模棱两可的先不处罚。若让太多候选负责同一目标会产生重复和类别不平衡；太少则可能漏掉难例。
### 3.1 重要实现差异（Implementation Differences）
- Faster R-CNN RPN、SSD、YOLOv2/v3/v5 的匹配阈值和保证规则不同。
- 现代动态分配器会结合分类分数、IoU、中心先验或任务对齐度，不只使用固定 IoU 阈值。
- 正负样本极不平衡可通过采样、难例挖掘（Hard Negative Mining）或焦点损失（Focal Loss）处理。
- 训练匹配 IoU 阈值与数据集评估 IoU、NMS IoU 是三个不同参数。
## 4. Faster R-CNN 风格的框编码（Faster R-CNN-style Encoding）
设锚框中心与尺寸为 $(x_a,y_a,w_a,h_a)$，真实框为 $(x^*,y^*,w^*,h^*)$：
$$
t_x^*=\frac{x^*-x_a}{w_a},\quad t_y^*=\frac{y^*-y_a}{h_a},\quad
t_w^*=\log\frac{w^*}{w_a},\quad t_h^*=\log\frac{h^*}{h_a}
$$
解码预测偏移 $(t_x,t_y,t_w,t_h)$：
$$
x=t_xw_a+x_a,\quad y=t_yh_a+y_a,\quad
w=e^{t_w}w_a,\quad h=e^{t_h}h_a
$$
中心偏移按锚框尺寸归一化，宽高使用对数比例，让放大和缩小具有较对称的数值表达。
## 5. YOLOv2/v3 风格的框解码（YOLOv2/v3-style Decoding）
对于网格偏移 $(c_x,c_y)$、锚框宽高 $(p_w,p_h)$ 和网络输出 $(t_x,t_y,t_w,t_h)$：
$$
b_x=\sigma(t_x)+c_x,\quad b_y=\sigma(t_y)+c_y
$$
$$
b_w=p_we^{t_w},\quad b_h=p_he^{t_h}
$$
- Sigmoid 把中心的网格内偏移限制在 $(0,1)$；最终坐标还需按网格和输入尺寸换算。
- 指数保证宽高为正，但大 $t_w,t_h$ 可能产生数值过大，具体实现会采用初始化、裁剪或不同参数化控制。
- YOLOv5 等实现的宽高解码公式已有变化，不能机械套用上述公式。
> [!warning] 坐标格式边界（Coordinate Contract）
> 编码前必须确认使用 `xyxy`、`xywh`、像素坐标还是归一化坐标，以及右下边界是闭区间还是半开区间。格式混用会造成训练标签和 IoU 全部错误。
## 6. 锚框式检测的优点与代价（Advantages and Costs）
### 6.1 优点（Advantages）
- 提供尺度和比例先验，可在同一位置预测多个候选。
- 与密集卷积输出自然结合，便于构建多尺度检测头。
- 有成熟的匹配、采样和回归经验。
### 6.2 代价（Costs）
- 锚框数量、尺度、比例和阈值形成额外超参数，换数据集可能需要重新调整。
- 密集锚框产生大量背景样本，并增加分类、内存和后处理负担。
- 锚框覆盖差会降低某些尺寸或长宽比目标的匹配质量。
## 7. 无锚框检测（Anchor-free Detection）
无锚框检测器可预测中心热图、关键点或特征位置到边界的距离。FCOS 和 Ultralytics YOLOv8 是现代无锚框代表。
- **减少的内容**：不再预设一组锚框宽高，不需要锚框聚类。
- **仍然存在的内容**：特征网格/点、正负区域、尺度分配、标签分配和框解码。
- **取舍**：减少一类超参数，但并未消除所有匹配与尺度设计问题。
## 8. 常见错误（Common Errors）
- 把锚框坐标和真实框坐标放在不同尺度中计算 IoU。
- 宽高为 0、负数或框坐标越界后未做检查。
- 每个真实框没有任何正样本，训练召回率长期为 0。
- 正样本数极少，却直接对所有背景等权求和，导致背景损失淹没前景。
- 推理时忘记把 Letterbox 填充和缩放逆变换回原图坐标。
## 参考资料（References）
- [Faster R-CNN](https://arxiv.org/abs/1506.01497)
- [YOLO9000: Better, Faster, Stronger](https://openaccess.thecvf.com/content_cvpr_2017/html/Redmon_YOLO9000_Better_Faster_CVPR_2017_paper.html)
- [FCOS](https://openaccess.thecvf.com/content_ICCV_2019/html/Tian_FCOS_Fully_Convolutional_One-Stage_Object_Detection_ICCV_2019_paper.html)
