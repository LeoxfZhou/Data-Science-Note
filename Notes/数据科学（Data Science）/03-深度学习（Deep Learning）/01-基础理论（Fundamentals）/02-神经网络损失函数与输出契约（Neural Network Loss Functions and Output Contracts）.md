---
title: 神经网络损失函数与输出契约（Neural Network Loss Functions and Output Contracts）
tags:
  - data-science/deep-learning/loss-function
  - data-science/deep-learning/pytorch
status: published
created: 2026-08-11
published_at: 2026-08-12
---
# 神经网络损失函数与输出契约（Neural Network Loss Functions and Output Contracts）
## 1. 损失、代价与目标（Loss, Cost, and Objective）
- 单样本差异常称损失（Loss）；样本集合上的平均或总和常称代价（Cost）；加上正则项后的完整最小化表达式常称目标函数（Objective Function）。术语在文献中会交叉使用，应以公式为准。
- 损失函数既用于评估当前预测，也通过梯度为参数优化提供方向。
- 选择损失必须同时核对模型输出语义、目标编码、形状、数据类型、归约方式（Reduction）和数值范围。
## 2. 互斥多分类交叉熵（Multi-class Cross-entropy）
对 Logits $z_c$ 与真实类别 $y$：
$$
L=-\log\frac{e^{z_y}}{\sum_c e^{z_c}}
$$
- `nn.CrossEntropyLoss()` 内部组合 `LogSoftmax` 与负对数似然（Negative Log-likelihood）；输入应是未归一化 Logits，不要先做 Softmax。
- 输入常为 `(N, C)`；类别索引目标常为 `(N,)`、`torch.long` 且取值在 `[0,C)`。
- API 也支持概率分布目标、类别权重、`ignore_index`、`label_smoothing` 和不同 `reduction`，但概率目标的合法性由调用者保证。
```python
import torch
from torch import nn

logits = torch.tensor([[0.2, 0.6, 0.2], [0.1, 0.8, 0.1]])
targets = torch.tensor([1, 2], dtype=torch.long)
loss = nn.CrossEntropyLoss()(logits, targets)
print(round(loss.item(), 6))  # 1.120075
```
## 3. 二分类交叉熵（Binary Cross-entropy）
$$
L=-\left[y\log p+(1-y)\log(1-p)\right]
$$
- `BCELoss` 要求输入已是概率；`BCEWithLogitsLoss` 直接接收 Logits，并用稳定公式合并 Sigmoid 与 BCE，通常更推荐。
- 目标通常为浮点数，形状应与输出一致；多标签分类对每个标签独立应用二元损失。
```python
import torch
from torch import nn

probabilities = torch.tensor([0.6901, 0.5459, 0.2469])
targets = torch.tensor([0.0, 1.0, 0.0])
print(round(nn.BCELoss()(probabilities, targets).item(), 6))  # 0.686794
```
## 4. 平均绝对误差（Mean Absolute Error, MAE）
$$
L_{MAE}=\frac1N\sum_i|\hat y_i-y_i|
$$
- PyTorch 对应 `nn.L1Loss()`；对大残差线性增长，因此比 MSE 对离群点更鲁棒。
- 在残差 0 处数学导数不唯一，框架采用次梯度约定；两侧梯度幅值近似恒定，可能在最优点附近来回摆动。
- “L1 产生稀疏”主要指把 L1 范数施加在模型参数上作为正则化，不是 MAE 会让预测矩阵自动稀疏。
```python
import torch
from torch import nn

prediction = torch.tensor([1.0, 1.0, 1.9])
target = torch.tensor([2.0, 2.0, 2.0])
print(round(nn.L1Loss()(prediction, target).item(), 6))  # 0.7
```
## 5. 均方误差（Mean Squared Error, MSE）
$$
L_{MSE}=\frac1N\sum_i(\hat y_i-y_i)^2
$$
- PyTorch 对应 `nn.MSELoss()`；误差平方让大残差受到更强惩罚，因此对离群点敏感。
- 大残差会产生大梯度，但梯度爆炸还与网络深度、雅可比乘积和学习率有关，不能把 MSE 单独视为充分原因。
- MSE 损失与“L2 参数正则化”都含平方，但作用对象不同。
```python
import torch
from torch import nn

prediction = torch.tensor([1.0, 1.0, 1.9])
target = torch.tensor([2.0, 2.0, 2.0])
print(round(nn.MSELoss()(prediction, target).item(), 6))  # 0.67
```
## 6. 平滑 L1（Smooth L1）
- `SmoothL1Loss(beta)` 在 $|x|<\beta$ 时使用缩放二次项，在外部使用线性项；当默认 `beta=1` 时，分界为 `[-1,1]`。

> [!tip] 大白话理解（Plain-language Intuition）
> 损失函数像训练时的“计分规则”：它把模型当前错得多严重变成一个数。不同任务需要不同计分方式——回归关心预测距离，分类关心正确类别的相对得分或概率；选错损失函数，相当于让模型按错误的评分标准努力。
- 小误差区域平滑，避免 MAE 在零点的尖角；大误差区域线性，减弱 MSE 对离群点的放大。
```python
import torch
from torch import nn

prediction = torch.tensor([0.6, 0.4])
target = torch.tensor([0.0, 3.0])
print(round(nn.SmoothL1Loss()(prediction, target).item(), 6))  # 1.14
```
## 7. 速查表（Selection Table）

|任务（Task）|模型输出（Model Output）|目标（Target）|常用损失（Typical Loss）|
|---|---|---|---|
|互斥多分类|`(N,C)` Logits|`(N,)` 类别索引|`CrossEntropyLoss`|
|二分类/多标签|与目标同形状的 Logits|浮点 0/1 或软标签|`BCEWithLogitsLoss`|
|标准回归|连续值|连续值|`MSELoss`|
|含离群点回归|连续值|连续值|`L1Loss` 或 `SmoothL1Loss`|
## 参考资料（References）
- [PyTorch `CrossEntropyLoss` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)
- [PyTorch 损失函数模块官方文档](https://docs.pytorch.org/docs/stable/nn.html#loss-functions)
