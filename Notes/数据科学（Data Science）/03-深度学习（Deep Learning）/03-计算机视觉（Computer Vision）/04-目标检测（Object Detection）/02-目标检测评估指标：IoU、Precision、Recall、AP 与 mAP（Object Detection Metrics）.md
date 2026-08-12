---
title: 目标检测评估指标：IoU、Precision、Recall、AP 与 mAP（Object Detection Metrics）
tags:
  - data-science/deep-learning/computer-vision/object-detection/metrics
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# 目标检测评估指标：IoU、Precision、Recall、AP 与 mAP（Object Detection Metrics）
## 1. 评估链条（Evaluation Chain）
目标检测评估遵循以下逻辑：
$$
\text{IoU}\rightarrow\text{一对一匹配}\rightarrow TP/FP/FN\rightarrow Precision/Recall\rightarrow PR\text{ 曲线}\rightarrow AP\rightarrow mAP
$$
> [!tip] 大白话理解（Plain-language Intuition）
> 先判断每个预测框是否与某个真实框足够贴合，再统计“报出的有多少正确”和“真实目标找回多少”。最后改变置信度门槛，观察模型从谨慎到激进的完整表现，而不是只看某一个阈值。
## 2. 交并比（Intersection over Union, IoU）
给定真实框 $A$ 与预测框 $B$：
$$
\operatorname{IoU}(A,B)=\frac{|A\cap B|}{|A\cup B|}=\frac{|A\cap B|}{|A|+|B|-|A\cap B|}
$$
![[02-目标检测评估指标：IoU、Precision、Recall、AP 与 mAP（Object Detection Metrics）-20260627151208528.png|206]]
- **取值范围（Range）**：$0\leq\operatorname{IoU}\leq1$；无交集为 0，完全重合为 1。
- **尺度归一性（Scale Normalization）**：IoU 是面积比，同样的像素偏移对大框和小框产生不同相对惩罚，比单独比较中心像素距离更适合作为通用重叠度量。
- **边界（Boundary）**：IoU 只衡量几何重叠，不判断类别，也不衡量置信度是否校准。
### 2.1 轴对齐矩形的计算（Axis-aligned Box Calculation）
若边界框格式为 $(x_1,y_1,x_2,y_2)$，交集宽高为：
$$
w_I=\max(0,\min(x_{2A},x_{2B})-\max(x_{1A},x_{1B}))
$$
$$
h_I=\max(0,\min(y_{2A},y_{2B})-\max(y_{1A},y_{1B}))
$$
交集面积为 $w_Ih_I$。`max(0, ...)` 防止不相交时得到负面积。
### 2.2 IoU 的三类用途（Three Uses of IoU）
- **训练匹配（Training Matching）**：部分锚框式检测器用 IoU 决定正、负或忽略样本；具体阈值由模型定义。
- **数据集评估（Dataset Evaluation）**：用 IoU 阈值判断预测框是否满足定位要求。
- **重复框后处理（Duplicate Suppression）**：NMS 用预测框之间的 IoU 判断是否重复。
这三类阈值的语义不同，不能把“匹配阈值”“评估阈值”和“NMS 阈值”混为一个参数。
## 3. GIoU、DIoU 与 CIoU（IoU-derived Regression Measures）
### 3.1 广义交并比（Generalized IoU, GIoU）
令 $C$ 为包住 $A$ 和 $B$ 的最小闭包区域：
$$
\operatorname{GIoU}=\operatorname{IoU}-\frac{|C\setminus(A\cup B)|}{|C|}
$$
GIoU 在两个框不相交时仍能根据闭包中的空余区域区分位置关系，常构造为 $1-\operatorname{GIoU}$ 损失。
### 3.2 距离交并比（Distance IoU, DIoU）
令 $\rho^2(b,b^{gt})$ 为两框中心点距离平方，$c^2$ 为最小闭包框对角线平方：
$$
\operatorname{DIoU}=\operatorname{IoU}-\frac{\rho^2(b,b^{gt})}{c^2}
$$
DIoU 直接惩罚中心距离。完整交并比（Complete IoU, CIoU）在此基础上加入长宽比一致性项。
> [!tip] 大白话理解（Plain-language Intuition）
> 两个完全不重叠的框，其 IoU 都是 0，无法告诉优化器该往哪个方向移动。GIoU 看外围空白，DIoU 看中心距离，CIoU 再看形状比例，给回归提供更细的方向信息。
> [!warning] 评估与损失的边界（Metric–Loss Boundary）
> GIoU、DIoU、CIoU 可用于回归损失或补充分析，但 COCO/PASCAL 等数据集的标准 AP 仍按其规定的 IoU 匹配协议计算，不能擅自替换后继续沿用同一指标名称。
## 4. 一对一匹配与 TP、FP、FN（Matching and Outcomes）
在给定类别与 IoU 阈值下，通常把预测按置信度从高到低处理：
1. 为当前预测寻找 IoU 最大且尚未匹配的同类真实框。
2. 若 IoU 达到阈值，则当前预测计为真正例（True Positive, TP），真实框标记为已匹配。
3. 若类别错误、IoU 未达阈值、没有可匹配真实框，或重复命中已被高分框匹配的同一目标，则计为假正例（False Positive, FP）。
4. 最终仍未被任何有效预测匹配的真实目标计为假负例（False Negative, FN）。
5. 背景区域可无限枚举，真负例（True Negative, TN）通常不纳入检测核心指标。
> [!tip] 大白话理解（Plain-language Intuition）
> 一个真实目标只能给一个预测框记一次功。第一个合格高分框算 TP，后续围着同一目标重复报出的框即使也很贴合，仍算 FP；否则模型可以靠重复输出刷高分。
## 5. Precision、Recall 与 F1（Precision, Recall, and F1）
$$
\operatorname{Precision}=\frac{TP}{TP+FP},\qquad
\operatorname{Recall}=\frac{TP}{TP+FN}
$$
$$
F_1=2\frac{\operatorname{Precision}\cdot\operatorname{Recall}}{\operatorname{Precision}+\operatorname{Recall}}
$$
- **精确率（Precision）**：所有报出的预测中有多少正确，侧重控制误检。
- **召回率（Recall）**：所有真实目标中有多少被找到，侧重控制漏检。
- **F1 分数（F1 Score）**：Precision 与 Recall 的调和平均；分母为 0 时实现必须规定返回值或跳过策略。
- **阈值影响（Threshold Effect）**：提高置信度阈值通常减少预测，可能提高 Precision、降低 Recall；这不是严格单调保证，取决于分数排序与错误分布。
- **应用侧重（Application Emphasis）**：高 Precision 适合对虚警敏感的工业缺陷剔除等场景；高 Recall 适合对漏检敏感的行人安全或医疗筛查场景。实际系统仍应按错误成本同时约束二者，不能把“零漏检”或“零误检”当成默认可达目标。
## 6. PR 曲线与 AP（Precision–Recall Curve and Average Precision）
固定类别和 IoU 阈值后，将预测按置信度降序排列，逐个纳入并累计 TP/FP，即得到一系列 Precision–Recall 点。平均精度（Average Precision, AP）是经过协议规定的插值或积分后，PR 曲线下的面积。
### 6.1 三目标示例（Three-object Example）
假设数据集中有 3 个该类真实目标，按分数排序的前三个预测依次为 TP、FP、TP：

|步骤（Step）|纳入预测|累计 TP|累计 FP|Precision|Recall|
|---|---|---|---|---|---|
|1|预测 1：TP|1|0|$1$|$1/3$|
|2|预测 2：FP|1|1|$1/2$|$1/3$|
|3|预测 3：TP|2|1|$2/3$|$2/3$|

使用每个召回位置右侧的最高 Precision 构造单调精度包络后，该简化示例的面积为：
$$
AP=1\times\frac13+\frac23\times\frac13=\frac59\approx0.556
$$
![[02-目标检测评估指标：IoU、Precision、Recall、AP 与 mAP（Object Detection Metrics）-20260627161046154.png]]
> [!warning] AP 实现差异（AP Implementation Differences）
> VOC 2007 的 11 点插值、后续 VOC 的全点插值和 COCO 的 101 个召回阈值并不等价。手算示例用于理解排序与面积，正式结果应使用数据集官方评估实现。
### 6.2 多类别算例（Multi-class Example）
若只有飞机和坦克两个参与评估的类别，且 $AP_{airplane}=0.5$、$AP_{tank}=0.2$，则：
$$
mAP=\frac{0.5+0.2}{2}=0.35
$$
若某类别在评估集中没有真实实例，是否忽略该类别必须遵循评估工具规定。
## 7. mAP 与常见协议（mAP and Common Protocols）
若有 $N$ 个参与评估的类别：
$$
mAP=\frac1N\sum_{k=1}^{N}AP_k
$$
- **`AP50` / `mAP@0.5`**：固定 IoU 阈值为 0.50 后对类别求平均，定位要求相对宽松。
- **COCO `AP` / `AP@[0.50:0.95]`**：在 0.50、0.55、…、0.95 共 10 个 IoU 阈值上求平均，并结合 COCO 对召回采样、面积区间和最大检测数的规定。
- **`AP75`**：固定 IoU 0.75，定位要求高于 AP50。
- **`AP_S`、`AP_M`、`AP_L`**：按小、中、大目标面积区间报告；必须使用协议规定的面积边界。
### 7.1 报告指标时必须附带的信息（Required Reporting Context）
- 数据集、数据划分与评估实现。
- IoU 阈值或阈值范围。
- 是否按类别平均、是否排除无样本类别。
- 最大检测数、目标面积范围与忽略区域策略。
- 输入尺寸、单尺度或多尺度测试、测试时增强（Test-time Augmentation）。
## 8. 工程指标（Engineering Metrics）
- **时延（Latency）**：一次请求的耗时，应说明硬件、精度、批大小、预热、预处理和后处理是否计入。
- **吞吐量（Throughput）与 FPS**：单位时间处理量；批量吞吐不能直接代表批大小 1 的实时延迟。
- **参数量（Parameter Count）**：影响权重存储与部分内存占用，但不等于峰值运行内存。
- **浮点运算量（Floating-point Operations, FLOPs）**：理论算术复杂度；真实速度还取决于内存访问、并行度、算子融合和运行时实现。
- **功耗与能耗（Power and Energy）**：功耗是瞬时消耗，单样本能耗还与运行时间有关。
工程资料有时用 30 FPS 作为视频实时性的经验门槛，也会引用特定 YOLOv5 配置约 27 MB、367 MB 或批处理约 140 FPS 的结果。这些数值只对应特定模型变体、权重格式、硬件、批大小和软件版本，不能作为跨环境保证。
> [!tip] 大白话理解（Plain-language Intuition）
> AP 像考试成绩，Latency 和能耗像完成考试需要的时间与电量。模型参数少、FLOPs 低，不保证在某块芯片上就更快；最终要用目标设备实测。
## 9. 常见错误（Common Errors）
- 只写“mAP 80%”而不注明 `AP50` 还是 `AP@[0.50:0.95]`。
- 把置信度阈值当作 IoU 匹配阈值，或把 NMS IoU 阈值当作评估 IoU 阈值。
- 允许多个预测同时匹配一个真实框，导致重复框错误计为 TP。
- 比较不同数据集、输入尺寸、评估脚本或最大检测数下的 AP。
- 用 $FPS=1000/\text{latency(ms)}$ 推断批量吞吐，却忽略并发、流水线和预后处理。
## 参考资料（References）
- [COCO Detection Task](https://cocodataset.org/dataset/detection-2017.htm)
- [Generalized Intersection over Union](https://openaccess.thecvf.com/content_CVPR_2019/html/Rezatofighi_Generalized_Intersection_Over_Union_A_Metric_and_a_Loss_for_CVPR_2019_paper.html)
- [Distance-IoU Loss](https://ojs.aaai.org/index.php/AAAI/article/view/6999)
