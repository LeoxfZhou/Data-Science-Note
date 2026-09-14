---
title: "优化器、学习率与泛化速查表（Optimizers, Learning Rates, and Generalization Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - deep-learning/optimization
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "PyTorch 2.3–2.14"
---
# 优化器、学习率与泛化速查表（Optimizers, Learning Rates, and Generalization Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
优化器状态应随模型 checkpoint 保存；学习率策略的调用时机要与批次或 epoch 契约一致。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 优化器（Optimizers）
优化器把梯度转成参数更新；大白话：决定沿哪个方向、迈多大步。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|SGD|`torch.optim.SGD(params, lr, momentum=0, weight_decay=0)`|返回优化器|
|Adam|`torch.optim.Adam(params, lr=1e-3, betas=(.9,.999))`|维护一二阶矩估计|
|AdamW|`torch.optim.AdamW(params, lr=1e-3, weight_decay=.01)`|解耦权重衰减|
|RMSprop|`torch.optim.RMSprop(params, lr=.01, alpha=.99)`|按平方梯度缩放|
|参数组|`AdamW([{'params': backbone,'lr':1e-4}, ...])`|不同组使用不同超参数|
|更新|`optimizer.step()`|原地更新参数和优化器状态|
|清梯度|`optimizer.zero_grad(set_to_none=True)`|清除累计梯度|
|状态字典|`optimizer.state_dict()`|返回可序列化状态|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
w=torch.tensor([1.],requires_grad=True)
opt=torch.optim.SGD([w],lr=.1)
(w**2).sum().backward(); opt.step(); opt.zero_grad(set_to_none=True)
print(round(w.item(),2), w.grad)
# 期望输出:
# 0.8 None
```
## 学习率调度（Learning-rate Scheduling）
过大震荡、过小收敛慢；预热可稳定训练早期。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|阶梯衰减|`StepLR(opt, step_size, gamma=.1)`|每固定 epoch 缩放学习率|
|多节点衰减|`MultiStepLR(opt, milestones, gamma=.1)`|指定 epoch 衰减|
|余弦退火|`CosineAnnealingLR(opt, T_max, eta_min=0)`|余弦降低学习率|
|平台衰减|`ReduceLROnPlateau(opt, mode='min', patience=10)`|指标停滞时降低；step(metric)|
|一次循环|`OneCycleLR(opt, max_lr, total_steps=...)`|每批更新的先升后降策略|
|线性 Lambda|`LambdaLR(opt, lr_lambda=fn)`|按函数缩放基准学习率|
|顺序调度|`SequentialLR(opt, schedulers, milestones)`|串联预热和主策略|
|当前学习率|`scheduler.get_last_lr()`|返回参数组学习率列表|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
w=torch.tensor([1.],requires_grad=True); opt=torch.optim.SGD([w],lr=.1)
s=torch.optim.lr_scheduler.StepLR(opt,step_size=1,gamma=.5)
opt.step(); s.step(); print(s.get_last_lr())
# 期望输出:
# [0.05]
```
## 泛化、正则与稳定性（Generalization and Stability）
泛化来自数据、归纳偏置和验证，而非单一技巧。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|权重衰减|`AdamW(..., weight_decay=.01)`|更新时收缩参数|
|Dropout|`nn.Dropout(p=.5)`|训练时随机置零，eval 时恒等|
|BatchNorm|`nn.BatchNorm1d(C)`|训练用批统计并更新运行统计，eval 用运行统计|
|LayerNorm|`nn.LayerNorm(normalized_shape)`|按样本末尾维归一化|
|早停|`验证指标连续 patience 轮不改善`|停止并恢复最佳权重|
|数据增强|`随机裁剪、翻转、颜色扰动`|改变训练输入分布|
|混合精度|`torch.autocast(device_type=...)`|返回低精度上下文|
|梯度缩放|`torch.amp.GradScaler(...)`|降低 float16 下溢风险|
|梯度裁剪|`clip_grad_norm_(params,max_norm)`|限制爆炸梯度|
|EMA|`参数指数移动平均`|得到更平滑的评估权重|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torch import nn
x=torch.ones(4)
d=nn.Dropout(p=.5); d.eval()
print(torch.equal(d(x),x))
# 期望输出:
# True
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
- [[04-梯度下降、优化器与学习率调度（Gradient Descent, Optimizers, and Learning-rate Scheduling）]]
- [[01-神经网络参数初始化与梯度流（Neural Network Initialization and Gradient Flow）]]
- [[02-模型欠拟合、过拟合与泛化（Model Underfitting, Overfitting, and Generalization）]]
- [[03-批归一化与常见归一化方法（Batch Normalization and Common Normalization Methods）]]
## 官方参考（Official References）
- [PyTorch 文档](https://docs.pytorch.org/docs/stable/)
