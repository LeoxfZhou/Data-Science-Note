---
title: "激活函数、输出层与损失函数速查表（Activations, Output Layers, and Loss Functions Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - deep-learning/loss
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "PyTorch 2.3–2.14"
---
# 激活函数、输出层与损失函数速查表（Activations, Output Layers, and Loss Functions Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
损失输入语义必须与任务匹配：二分类 logits、单标签多分类 logits、多标签独立 logits、回归连续值。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 激活函数（Activation Functions）
激活函数引入非线性并影响梯度流。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|ReLU|`nn.ReLU(inplace=False)`|负值变 0，返回同形状 Tensor|
|LeakyReLU|`nn.LeakyReLU(.01)`|负半轴保留小斜率|
|GELU|`nn.GELU(approximate='none')`|平滑门控，Transformer 常用|
|SiLU|`nn.SiLU()`|返回 `x*sigmoid(x)`，现代 CNN 常用|
|Sigmoid|`torch.sigmoid(x)`|映射到 `(0,1)`|
|Tanh|`torch.tanh(x)`|映射到 `(-1,1)`|
|Softmax|`torch.softmax(logits, dim=-1)`|指定轴归一为概率和 1|
|LogSoftmax|`torch.log_softmax(logits, dim=-1)`|返回数值稳定对数概率|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
x=torch.tensor([-1.,0.,1.])
print(torch.relu(x).tolist())
print(torch.softmax(x,dim=0).sum().item())
# 期望输出:
# [0.0, 0.0, 1.0]
# 1.0
```
## 分类损失（Classification Losses）
框架损失通常直接接 logits，不要提前重复 sigmoid/softmax。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|单标签多分类|`nn.CrossEntropyLoss(weight=None, ignore_index=-100)`|logits `(N,C,...)` + 整数标签，返回标量默认均值|
|二分类/多标签|`nn.BCEWithLogitsLoss(pos_weight=None)`|稳定组合 sigmoid 与 BCE|
|负对数似然|`nn.NLLLoss()`|输入须为 log-probability|
|KL 散度|`nn.KLDivLoss(reduction='batchmean')`|常接 log-prob 与目标分布|
|标签平滑|`nn.CrossEntropyLoss(label_smoothing=.1)`|软化硬标签|
|焦点损失|`sigmoid_focal_loss(inputs, targets, alpha, gamma)`|降低易样本权重（torchvision）|
|类别权重|`weight=torch.tensor([...])`|按类别缩放损失|
|正类权重|`pos_weight=...`|在 BCE 中调整正例项|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torch import nn
logits=torch.tensor([[2.,0.,-1.]])
target=torch.tensor([0])
loss=nn.CrossEntropyLoss()(logits,target)
print(round(loss.item(),4))
# 期望输出:
# 0.1698
```
## 回归、分割与序列损失（Regression, Segmentation, and Sequence Losses）
损失的归约方式决定标量含义和有效样本权重。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|均方误差|`nn.MSELoss(reduction='mean')`|返回平方误差均值|
|平均绝对误差|`nn.L1Loss()`|返回绝对误差均值|
|平滑 L1|`nn.SmoothL1Loss(beta=1.0)`|小误差二次、大误差线性|
|Huber|`nn.HuberLoss(delta=1.0)`|返回鲁棒回归损失|
|余弦嵌入|`nn.CosineEmbeddingLoss(margin=0.0)`|比较向量方向|
|CTC|`nn.CTCLoss(blank=0, zero_infinity=False)`|对齐未知序列损失|
|Dice|`1-(2*intersection+eps)/(sum+eps)`|返回重叠损失，分割常用|
|忽略填充|`ignore_index=pad_id`|被忽略标签不贡献交叉熵|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torch import nn
pred=torch.tensor([1.,3.]); y=torch.tensor([2.,1.])
print(nn.L1Loss()(pred,y).item())
print(nn.MSELoss()(pred,y).item())
# 期望输出:
# 1.5
# 2.5
```
## 高频工作模式（Common Workflows）
- **基线（Baseline）**：先用最小可解释模型和极小数据过拟合测试，确认数据、损失和指标链路正确。
- **训练（Training）**：固定随机种子，记录数据版本、超参数、权重、指标与环境。
- **验证（Validation）**：验证集只用于选型与调参，最终测试集只评估一次。
- **推理（Inference）**：冻结随机行为、关闭梯度、统一预处理并验证输出 schema。
- **性能（Performance）**：先测量数据加载、计算、通信与后处理，再针对瓶颈优化。
- **上线（Production）**：增加输入校验、超时、批处理、监控、回滚和隐私保护。
## 常见错误与排查（Common Errors and Troubleshooting）
- **维度错误**：记录每个关键张量的 `shape/dtype/device`，按模块契约逐层核对。
- **训练不稳定**：检查输入归一化、标签范围、损失配对、学习率、梯度范数和 NaN/Inf。
- **指标虚高**：排查数据泄漏、重复样本、错误划分、阈值选择和只看单一平均指标。
- **推理漂移**：确保训练与服务使用同一 tokenizer、类别表、归一化统计和模型版本。
- **资源泄漏**：及时关闭文件、图像、客户端与进程；长任务持续观察 CPU/GPU/内存。
- **版本漂移**：固定主要依赖并以官方迁移说明处理弃用，不静默忽略警告。
## 相关详细笔记（Detailed Notes）
- [[02-神经网络损失函数与输出契约（Neural Network Loss Functions and Output Contracts）]]
- [[03-神经网络激活函数（Neural Network Activation Functions）]]
## 官方参考（Official References）
- [PyTorch 文档](https://docs.pytorch.org/docs/stable/)
