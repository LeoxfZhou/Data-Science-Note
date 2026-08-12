---
title: 非极大值抑制与 Soft-NMS（Non-Maximum Suppression and Soft-NMS）
tags:
  - data-science/deep-learning/computer-vision/object-detection/nms
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# 非极大值抑制与 Soft-NMS（Non-Maximum Suppression and Soft-NMS）
## 1. 为什么需要 NMS（Why NMS Is Needed）
密集检测头常在同一目标附近输出多个高重叠边界框。非极大值抑制（Non-Maximum Suppression, NMS）保留局部最高分框，并抑制被判定为重复的较低分框。
> [!tip] 大白话理解（Plain-language Intuition）
> 模型可能围着一辆车画十个相似框。NMS 让这些框比赛：先留下分数最高的，再删掉与它高度重叠的同类框，然后对剩余框继续比赛。
## 2. 标准 NMS 算法（Greedy NMS）
输入为候选框集合 $B$、分数 $S$、重叠阈值 $t$，通常还先应用最低置信度阈值。
1. 按分数从高到低排序。
2. 取最高分框 $M$ 加入结果集合 $D$。
3. 计算 $M$ 与剩余框的 IoU。
4. 抑制满足 $\operatorname{IoU}(M,b)>t$ 的重复框。
5. 对未被抑制的框重复步骤 2–4，直到集合为空或达到最大检测数。
### 2.1 伪代码（Pseudocode）
```text
输入: boxes, scores, iou_threshold
order <- 按 scores 降序排列的索引
keep <- 空列表
while order 非空:
    current <- order[0]
    keep 追加 current
    overlaps <- IoU(boxes[current], boxes[order[1:]])
    order <- order[1:][overlaps <= iou_threshold]
返回 keep
```
### 2.2 六框示例（Six-box Example）
假设车辆框分数为 $F>E>D>C>B>A$：
- 第一轮保留 $F$；若 $B,D$ 与 $F$ 的 IoU 超过阈值，则抑制 $B,D$。
- 剩余 $A,C,E$ 中保留最高分 $E$，再根据 $E$ 与 $A,C$ 的 IoU 抑制重复框。
- 重复直到没有候选框。
这里的结果取决于具体坐标和阈值，不能仅凭分数顺序确定最终保留集合。
## 3. 按类别与类别无关 NMS（Class-aware and Class-agnostic NMS）
- **按类别 NMS（Class-aware NMS）**：每个类别独立抑制；不同类别的重叠框不会相互删除，适合类别可重叠或分类仍有不确定性的场景。
- **类别无关 NMS（Class-agnostic NMS）**：所有类别共同抑制；可减少同一目标被报成多个类别，但可能误删真实重叠的不同类别目标。
- **多标签预测（Multi-label Prediction）**：同一框可拥有多个类别分数时，展开策略和 NMS 类别规则必须明确。
## 4. 阈值的影响（Threshold Trade-offs）
- 较低 NMS IoU 阈值会更积极地抑制重叠框，减少重复，但可能漏掉拥挤实例。
- 较高阈值保留更多相邻框，提高拥挤场景召回可能性，也可能留下重复检测。
- NMS IoU 阈值与评估 IoU 阈值语义不同；前者比较预测框之间的重复，后者比较预测框与真实框的定位质量。
> [!tip] 大白话理解（Plain-language Intuition）
> 阈值低像严格查重：长得有点像就删；阈值高像宽松查重：只有几乎一样才删。拥挤人群通常需要更谨慎，因为两个真实的人本来就可能高度重叠。
## 5. 标准 NMS 的局限（Limitations）
- **贪心顺序依赖（Greedy Order Dependence）**：最高分框若定位不佳，仍可能抑制更准确的低分框。
- **硬阈值不连续（Hard Threshold）**：IoU 刚好在阈值两侧的框会得到完全不同结果。
- **拥挤目标误抑制（Crowded-object Suppression）**：两个真实实例高度重叠时，较低分实例可能被当成重复框。
- **分数与定位质量不一致（Score–Localization Misalignment）**：分类高分不一定表示边界框更准确。
## 6. Soft-NMS（Soft Non-Maximum Suppression）
Soft-NMS 不在 IoU 超阈值时立即删除框，而是根据它与当前最高分框的重叠程度衰减分数。衰减后低于最低分数阈值的框仍会被移除。
### 6.1 线性衰减（Linear Decay）
$$
s_i\leftarrow
\begin{cases}
s_i,&\operatorname{IoU}(M,b_i)<N_t\\
s_i(1-\operatorname{IoU}(M,b_i)),&\operatorname{IoU}(M,b_i)\ge N_t
\end{cases}
$$
### 6.2 高斯衰减（Gaussian Decay）
$$
s_i\leftarrow s_i\exp\left(-\frac{\operatorname{IoU}(M,b_i)^2}{\sigma}\right)
$$
高斯形式对所有重叠程度连续降分；$\sigma$ 控制衰减强度。
> [!tip] 大白话理解（Plain-language Intuition）
> 标准 NMS 是“重叠超线就淘汰”，Soft-NMS 是“越像最高分框，扣分越多”。若它确实对应另一个目标，原分数足够高时仍可能留到最后。
### 6.3 流程差异（Process Difference）
1. 取当前最高分框加入结果。
2. 根据 IoU 更新剩余框分数，而非只删除超阈值框。
3. 因分数已改变，重新选择最高分框。
4. 丢弃低于最低分数阈值的框，并受最大检测数约束。
Soft-NMS 论文表明它可作为不重新训练模型的后处理替换，但收益依赖检测器和数据集，不能保证所有场景均提升。
## 7. 其他变体与端到端检测（Variants and End-to-end Detection）
- **DIoU-NMS**：同时考虑重叠和中心距离，常用于遮挡或中心分离场景。
- **加权框融合（Weighted Boxes Fusion, WBF）**：按分数融合多个框坐标，常用于模型集成；它不是简单抑制算法。
- **可学习 NMS（Learned NMS）**：用模型学习重复关系，但增加训练与部署复杂度。
- **NMS-free 检测（NMS-free Detection）**：一对一标签分配和端到端集合预测可直接输出非重复结果；并非所有无锚框检测器都天然不需要 NMS。
## 8. 工程检查（Engineering Checklist）
- 在 NMS 前裁剪非法框、去除非有限分数，并把坐标映射回同一尺度。
- 明确输入分数是类别概率、目标存在性与类别分数乘积，还是其他质量分数。
- 明确按类别还是类别无关执行，以及是否支持多标签。
- 限制 NMS 前候选数与最终 `max_det`，避免延迟和内存失控。
- 对拥挤、遮挡、小目标和跨类别重叠分别验证阈值。
- 基准测试必须包含解码和 NMS；只报告网络前向耗时会低估端到端延迟。
## 参考资料（References）
- [Soft-NMS — Improving Object Detection With One Line of Code](https://openaccess.thecvf.com/content_iccv_2017/html/Bodla_Soft-NMS_--_Improving_ICCV_2017_paper.html)
- [Learning Non-Maximum Suppression](https://openaccess.thecvf.com/content_cvpr_2017/html/Hosang_Learning_Non-Maximum_Suppression_CVPR_2017_paper.html)
- [Distance-IoU Loss](https://ojs.aaai.org/index.php/AAAI/article/view/6999)
