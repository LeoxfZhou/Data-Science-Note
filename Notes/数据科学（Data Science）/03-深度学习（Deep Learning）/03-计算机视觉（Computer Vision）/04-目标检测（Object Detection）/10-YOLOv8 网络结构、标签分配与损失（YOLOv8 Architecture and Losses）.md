---
title: YOLOv8 网络结构、标签分配与损失（YOLOv8 Architecture and Losses）
tags:
  - data-science/deep-learning/computer-vision/object-detection/yolov8
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# YOLOv8 网络结构、标签分配与损失（YOLOv8 Architecture and Losses）
## 一、 算法引言与概述

- **YOLO (You Only Look Once)**：经典的 **One-Stage（单阶段）** 目标检测算法，仅需一次前向传播即可同时预测图像中物体的类别（Class）和边界框（Bounding Box）。
- **YOLOv8 的定位**：由 Ultralytics 公司推出。它不仅是一个特定的目标检测算法，更是一个支持图像分类、物体检测、实例分割和姿态估计的**通用算法框架**（开源库直接命名为 `ultralytics`）。
- **设计源流**：YOLOv8 在 2023 年发布时延续 Ultralytics 的工程接口，并采用 C2f、无锚框解耦检测头、Task-Aligned Assigner 与 DFL。它是版本化架构，不应继续称为“当前 SOTA”。
### 📊 YOLOv5 vs YOLOv8 性能对比 (基于 COCO Val2017)

> 💡 **概念澄清**：
> 
> - **FLOPs**（s小写）：浮点运算次数，用于衡量**模型/算法的复杂度**。
>     
> - **FLOPS**（S大写）：每秒运算浮点数，用于衡量**硬件的计算速度**。因此下表使用 FLOPs。
>     

|**模型尺度**|**YOLOv5 Params (M)**|**YOLOv5 FLOPs@640 (B)**|**YOLOv8 Params (M)**|**YOLOv8 FLOPs@640 (B)**|**性能趋势结论**|
|---|---|---|---|---|---|
|**n**|2.8|7.3|3.2|8.7|v8 同尺度常提高官方 COCO 指标，但参数、FLOPs 与速度必须按具体导出格式、硬件和官方表格协议比较。|
|**s**|7.2|16.5|11.2|28.6||
|**m**|21.2|49.0|25.9|78.9||
|**l**|46.5|109.1|43.7|165.2||
|**x**|86.7|205.7|68.2|257.8||

> ⚠️ **注意**：目前各 YOLO 系列算法在官方 COCO 数据集上提升明显，但在自定义数据集上的**泛化性**仍需结合业务场景具体验证。
> [!tip] 大白话理解（Plain-language Intuition）
> 同样叫 `n/s/m/l/x` 只表示各版本内部的缩放档位，不表示 YOLOv5s 与 YOLOv8s 有完全相同的计算量。选型应把精度、延迟、显存和目标设备放进同一份基准测试。

## 二、 YOLOv8 四大核心创新点

1. **全新的骨干网络与轻量化模块**：借鉴 CSP 思想，引入全新的 **C2f 模块** 替换了原有的 C3 模块，实现了更丰富的梯度流分支。
2. **解耦检测头 (Decoupled-Head)**：彻底弃用原有的耦合头，改用分类与回归完全分离的独立网络分支。
3. **无锚点机制 (Anchor-Free)**：放弃了传统的基于先验框（Anchor-Based）的聚类机制，拥抱更灵活的 Anchor-Free 匹配。
4. **动态标签分配与新损失函数**：抛弃静态 IoU 分配，采用 **Task-Aligned Assigner** 动态正负样本分配策略；分类使用 **BCE 损失**，回归使用 **DFL + CIoU 复合损失**。

## 三、 网络架构详解

YOLOv8 的网络骨架主要由 **Backbone（主干网络）**、**Neck（颈部网络）** 和 **Head（检测头）** 三部分组成。
![[10-YOLOv8 网络结构、标签分配与损失（YOLOv8 Architecture and Losses）-20260727113839511.png]]
### 1. Backbone（主干网络）

整体沿用 **CSPDarkNet** 结构，相比 YOLOv5 有三大核心改动：

- **初始下采样微调**：第一层卷积（Layer 0）的 Kernel Size 从 $6 \times 6$ 改为 $3 \times 3$。
- **重复块数调整**：实际重复数由 YAML 基础值和模型深度系数共同计算；`n/s/m/l/x` 不共享一组固定的 `3-6-6-3` 展开结果，检查具体模型 YAML 与解析后网络。
- **核心模块 C3 升级为 C2f**：

> **C3 模块（双分支并行）**：输入特征图被 split 为两部分，主分支通过 $1 \times 1$ 卷积降维后串联 $N$ 个 Bottleneck 提取特征，旁路分支直接经过 $1 \times 1$ 卷积，最后通过 Concat 在通道维度拼接融合。
> 
> **C2f 模块（多阶段串联）**：输入经 $1 \times 1$ 卷积后直接进行 Split。其中一个分支会穿过连续的 Bottleneck，**最核心的是：每个 Bottleneck 的输出都会引出一条快捷跨层连接（Shortcut）直接投递到末端**。最后将所有处理阶段的特征图进行大拼接。
> ![[10-YOLOv8 网络结构、标签分配与损失（YOLOv8 Architecture and Losses）-20260727113852347.png]]
> **带来的作用**：C2f 把各内部 Bottleneck 的输出一起拼接，提供更多直接梯度路径和特征复用；实际 FLOPs 与通道数由扩展率、重复数和模型尺度决定。
> [!tip] 大白话理解（Plain-language Intuition）
> C3 主要把两条大支路在末端汇合；C2f 还把中途每个 Bottleneck 的结果都保留下来一起交卷，后层可以直接复用不同深度的特征，梯度也有更多返回路线。
### 2. Neck（颈部网络）

- **结构**：采用双向通路的 **PANet（Path Aggregation Network）** 结构，同时包含自上而下（FPN）和自下而上（PAN）的路径，确保底层的空间几何信息与高层的语义信息能够双向充分融合。
- **精简点**：相比 YOLOv5，YOLOv8 移除了上采样路径中的 $1 \times 1$ 降采样层，并且同样将 C3 替换为了 C2f。
- **多尺度输出**：检测头通常使用步长 8、16、32 的 P3/P4/P5；当输入是 `640×640` 时才对应 `80×80`、`40×40`、`20×20`，其他输入尺寸按步长变化。
### 3. Head（检测头）

YOLOv8 在检测头部分做出了革命性的改进：
![[10-YOLOv8 网络结构、标签分配与损失（YOLOv8 Architecture and Losses）-20260727113927486.png]]
- **解耦头结构 (Decoupled-Head)**：分类和回归任务的冲突会导致模型难以同时收敛。YOLOv8 将其分离为两个独立的分支——**分类分支**专注于物体是什么（输出类别概率），**回归分支**专注于物体在哪里（输出位置坐标）。
- **去掉独立置信度分支（Objectness）**：YOLOv8 没有前景/背景的单独预测分值，而是直接将**分类分支输出的概率最大值**作为该锚点的目标置信度。

## 四、 YAML 配置文件逐层剖析

YOLOv8 配置文件采用 `[from, repeats, module, args]` 的统一格式：

- `from`：输入来源（`-1` 表示上一层，`[a, b]` 表示融合多层）。
- `repeats`：该层模块的重复堆叠次数。
- `args`：模块参数（如 `[输出通道数, 卷积核大小, 步长]`）。
### 📋 主干与颈部网络核心层解析流程表

|**层级 (Layer)**|**来源 (from)**|**模块 (module)**|**参数 (args)**|**输出尺寸与维度变化 (以640输入为例)**|**核心语义说明**|
|---|---|---|---|---|---|
|**0**|-1|Conv|`[64, 3, 2]`|$320 \times 320 \times 64$|初始下采样层，长宽减半，通道变64|
|**1**|-1|Conv|`[128, 3, 2]`|$160 \times 160 \times 128$|P2/4 阶段，长宽降为 1/4|
|**2**|-1|C2f|`[128, True]`|$160 \times 160 \times 128$|重复3次，True 表示开启残差快捷连接|
|**3**|-1|Conv|`[256, 3, 2]`|$80 \times 80 \times 256$|**P3/8 阶段**，特征图降为 $80 \times 80$|
|**...**|...|...|...|...|...|
|**9**|-1|SPPF|`[1024, 5]`|$20 \times 20 \times 1024$|**P5/32 阶段**，多尺度空间金字塔池化|
|**10**|-1|nn.Upsample|`[None, 2, 'nearest']`|$40 \times 40 \times 1024$|上采样层，尺寸放大 2 倍，通道不变|
|**11**|`[-1, 6]`|Concat|`[1]`|$40 \times 40 \times 1536$|将上采样结果与第6层（$40 \times 40 \times 512$）在通道维度拼接|
|**...**|...|...|...|...|...|
|**21**|-1|C2f|`[1024]`|$20 \times 20 \times 1024$|颈部网络输出的最高层大物体检测特征|
|**22**|`[15, 18, 21]`|Detect|`[nc]`|训练内部张量依实现组织|三个尺度进入无锚框解耦检测头|
### 🔍 区分内部训练通道与最终推理输出

- **`1`**：Batch Size（批大小）。
- **`8400`**：网格锚点总数。由三个尺度特征图的所有网格点加总而来（$80 \times 80 + 40 \times 40 + 20 \times 20 = 8400$）。
- **内部原始通道 `144`（COCO、`reg_max=16` 示例）**：每个位置包含：
    
    1. **分类部分（长度 80）**：对应 COCO 数据集的 80 个类别得分。
    2. **回归分布（长度 64）**：4 个 $l,t,r,b$ 偏移各有 16 个离散分布 logits，$4 \times 16=64$。
- **推理解码输出（Decoded Inference Output）**：DFL 对每组 16 维分布求期望并解码为 4 个框坐标，再与类别分数组合，常见检测导出形状为批次 × `(4+nc)` × 候选数或其转置；是否包含 NMS 由导出选项和后端决定。
- **结论（Contract）**：`[1,8400,144]` 不能统一称为所有 YOLOv8 API 的“最终输出”；先检查模型版本、任务、类别数、动态尺寸与导出后处理。
> [!tip] 大白话理解（Plain-language Intuition）
> 训练时模型为每条边保留 16 个“可能距离”的分数，便于计算 DFL；真正交给使用者前，会把 16 个分数加权成一个距离并解码成框。调试部署时若把中间账本当成最终框，维度就会完全对不上。

## 五、 标签分配策略与损失函数
### 1. 正负样本分配：Task-Aligned Assigner

YOLOv8 抛弃了基于固定 IoU 阈值的静态分配，采用了动态对齐策略：

- **对齐指标公式**：
    
    $$t = s^{\alpha} \times u^{\beta}$$
    
    - $s$：当前预测框对应真实类别的分类得分。
    - $u$：预测框与真实框（GT Box）之间的 IoU 值。
    - $\alpha, \beta$：权重控制超参数。
- **判定机制**：$t$ 可以同时控制分类和回归的协同优化。只有当预测框既猜得准类别（$s$ 高），又套得准位置（$u$ 高）时，$t$ 才会接近 1，从而被优先选为正样本。
- **具体步骤**：
    
    1. 根据公式计算候选锚点（Anchor Point）的对齐分数 `alignment_metrics`；这里的 Anchor Point 是特征图位置，不是预定义宽高锚框。
    2. 过滤掉中心点不在真实框内部的候选位置。
    3. 对每个真实框选择对齐分数前 $K$ 的候选，并解决同一候选被多个真实框选中的冲突。
    4. 用归一化后的对齐质量构造软分类目标，其余候选作为背景。
### 2. 分类损失 (Classification Loss)

- **实现边界（Implementation Boundary）**：经典 Ultralytics YOLOv8 检测损失使用带 logits 的二元交叉熵（Binary Cross-entropy with Logits）计算分类项；源码中可能保留 Varifocal Loss 等实现或历史实验代码，是否启用必须查当前版本调用路径。
### 3. 回归损失 (Regression Loss)

回归损失由 **CIoU Loss** 与 **DFL Loss** 联合组成。

#### 💡 核心机制：Distribution Focal Loss (DFL)

- **解决的问题**：把连续边界距离表示为离散区间上的分布，使模型能学习更细的距离估计，并为相邻区间提供连续监督；不能把输出分布直接解释为真实世界边界不确定性的完整概率模型。
- **DFL 的原理**：若连续标签 $y$ 位于相邻整数 $y_i,y_{i+1}$ 之间，损失按距离给这两个位置分配线性权重；推理时对 softmax 分布与区间索引求期望。
- **偏移量计算**：
    
    在 `reg_max=16` 的设定下，模型输出 16 维向量，代表偏移量落在这 16 个小区间段内的概率。最终的实际偏移量并不是取概率最大的一项，而是**将 16 个概率值与对应的区间中心点进行加权平均（求期望）**，从而大大提高了模糊边缘的定位精度。
## 六、 YOLOv5 与 YOLOv8 结构边界（YOLOv5 vs YOLOv8）

|维度（Dimension）|历史 YOLOv5|YOLOv8|
|---|---|---|
|主干块|C3|C2f|
|空间池化|后期 SPPF|SPPF|
|检测头|原始仓库为锚框式耦合头|无锚框解耦头|
|目标性分支|独立 Objectness|无独立 Objectness 输出分支|
|框回归|锚框偏移 + IoU 类损失|锚点距离分布 + DFL + CIoU|
|样本分配|锚框匹配/AutoAnchor|Task-Aligned Assigner|
> [!warning] 名称与实现（Name vs Implementation）
> 当前 `ultralytics` 包也提供带 YOLOv8 式无锚框头的 YOLOv5u 配置；它与独立 `ultralytics/yolov5` 仓库的历史 YOLOv5 头不同。比较模型时必须写清仓库与配置名。
## 七、 参考资料（References）
- [Ultralytics YOLOv8](https://docs.ultralytics.com/models/yolov8/)
- [Ultralytics YOLO Architecture Guide](https://docs.ultralytics.com/guides/yolo-architecture/)
- [Generalized Focal Loss](https://arxiv.org/abs/2006.04388)
- [TOOD: Task-aligned One-stage Object Detection](https://arxiv.org/abs/2108.07755)
