---
title: 梯度下降、优化器与学习率调度（Gradient Descent, Optimizers, and Learning-rate Scheduling）
tags:
  - data-science/deep-learning/optimization
  - data-science/deep-learning/pytorch
status: published
created: 2026-08-11
published_at: 2026-08-12
---
# 梯度下降、优化器与学习率调度（Gradient Descent, Optimizers, and Learning-rate Scheduling）
## 1. 最速下降的局部推导（Local Steepest-descent Derivation）
一阶泰勒近似：
$$
f(x+\Delta x)\approx f(x)+\nabla f(x)^{\mathsf T}\Delta x
$$
固定 $\|\Delta x\|$ 时，内积在 $\Delta x$ 与梯度反向时最小，因此欧氏范数下的局部最速下降方向是 $-\nabla f(x)$。
$$
\theta_{t+1}=\theta_t-\eta\nabla J(\theta_t)
$$
- 学习率（Learning Rate）$\eta$ 控制步长；太小通常收敛慢，太大可能震荡或发散。
- “负梯度最速”是局部、指定度量下的结论；有限步长、曲率和非凸结构会改变实际轨迹。
## 2. Batch、Iteration 与 Epoch
- **Batch**：一次前向/反向使用的样本集合。
- **Iteration**：用一个 Batch 完成一次参数更新。
- **Epoch**：训练集中的样本按当前采样策略被遍历一轮。
- 对 $N=50000$、`batch_size=256` 且不丢尾批次，单 Epoch 批次数为 $\lceil50000/256\rceil=196$；10 Epoch 为 1960 次迭代。
## 3. 三种数据用量（Batch, Stochastic, and Mini-batch GD）

|方法（Method）|每次更新样本|优点|限制|
|---|---:|---|---|
|批量梯度下降（Batch GD）|全部样本|梯度确定、凸问题轨迹平滑|计算和内存成本高，不适合频繁在线更新|
|随机梯度下降（Stochastic GD）|1 个样本|更新便宜、噪声可能帮助探索|方差大、轨迹震荡|
|小批量梯度下降（Mini-batch GD）|如 32/64/128|矩阵并行效率与方差折中|`batch_size` 影响吞吐、统计与泛化|
## 4. 特征缩放（Feature Scaling）
- 不同尺度会让等高线形成狭长峡谷，统一学习率在陡峭方向震荡、平缓方向进展慢。
- 标准化或归一化可改善条件数，使可用学习率范围更宽；提速程度依赖数据和模型，不保证“指数级”。
- 数据变换应仅在训练集拟合统计量，再应用到验证/测试集，避免数据泄漏。
## 5. 指数移动平均（Exponential Moving Average, EMA）
$$
s_t=\beta s_{t-1}+(1-\beta)y_t
$$
- 越新的观测权重越大；$\beta$ 越接近 1，曲线越平滑、响应越慢。
- 使用 30 个随机气温值比较 $\beta=0.5$ 与 $0.9$，可以说明指数加权平均的平滑机制，但不能据此证明优化器性能。

> [!tip] 大白话理解（Plain-language Intuition）
> 梯度指出当前位置“上坡最快”的方向，所以沿反方向走通常能让损失下降。学习率决定步子大小：太大会跨过低点来回震荡，太小则走得很慢；Momentum 像给小球增加惯性，Adam 则还会根据各方向历史梯度的大小自动调整步幅。
## 6. Momentum
一种常见教学记号：
$$
v_t=\beta v_{t-1}+(1-\beta)g_t,\qquad \theta_{t+1}=\theta_t-\eta v_t
$$
- 历史方向一致时积累速度，方向交替时平滑震荡；惯性可能穿过梯度接近 0 的区域，但不保证逃离所有鞍点或局部极小值。
- PyTorch SGD 的内部动量定义与是否含 $(1-\beta)$ 的教学公式存在尺度约定差异，应以 API 文档为准。
```python
import torch

w = torch.tensor([1.0], requires_grad=True)
optimizer = torch.optim.SGD([w], lr=0.01, momentum=0.9)
for step in range(2):
    loss = (w.square() / 2).sum()
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    print(step + 1, round(w.grad.item(), 6), round(w.item(), 6))
# 期望输出:
# 1 1.0 0.99
# 2 0.99 0.9711
```
## 7. AdaGrad
$$
G_t=G_{t-1}+g_t\odot g_t,qquad
\theta_{t+1}=\theta_t-\frac{\eta}{\sqrt{G_t}+\epsilon}\odot g_t
$$
- 每个参数使用自己的有效学习率；历史平方梯度大时步长缩小，适合稀疏特征。
- $G_t$ 单调累积，长训练中有效学习率可能过早衰减。
## 8. RMSProp
$$
v_t=\beta v_{t-1}+(1-\beta)g_t^2,qquad
\theta_{t+1}=\theta_t-\frac{\eta}{\sqrt{v_t}+\epsilon}\odot g_t
$$
- 用平方梯度的 EMA 替代 AdaGrad 的无界累加，更关注近期尺度。
- PyTorch `RMSprop` 中指数系数参数名为 `alpha`；还可配置 Momentum、centered 等选项。
## 9. Adam
$$
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,qquad
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2
$$
$$
\hat m_t=\frac{m_t}{1-\beta_1^t},\qquad
\hat v_t=\frac{v_t}{1-\beta_2^t}
$$
$$
\theta_{t+1}=\theta_t-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}
$$
- 一阶矩平滑方向，二阶矩适配坐标尺度，偏差修正补偿初始零状态。
- Adam 常是强基线，但不保证所有任务的最终泛化最好；视觉分类等任务中带 Momentum 的 SGD 仍常具有竞争力。
- 权重衰减若需与自适应更新解耦，使用 AdamW 并明确哪些参数组衰减。
## 10. 优化器选择（Optimizer Selection）

|优化器（Optimizer）|主要优势|主要风险|常见起点|
|---|---|---|---|
|SGD|简单、状态少|需要精心调学习率，噪声大|基线、小模型|
|SGD + Momentum|减少峡谷震荡、积累方向|多一个动量参数，可能过冲|视觉模型与稳定训练|
|AdaGrad|稀疏参数自适应|有效学习率持续缩小|稀疏特征、部分 NLP/推荐场景|
|RMSProp|近期平方梯度适配|超参数和任务敏感|非平稳目标、部分序列任务|
|Adam/AdamW|通常易于起步|状态内存大，泛化不总占优|复杂模型与快速基线|
## 11. 学习率为何需要调度（Why Schedule the Learning Rate）
- 训练初期较大学习率有利于快速移动；后期较小学习率可减小最优区域附近震荡。
- 调度器不会修复错误的数据、损失或梯度；应先确认基线能下降。
- PyTorch 常在每个 Epoch 的训练完成后调用 `scheduler.step()`；不同调度器的调用时机必须查文档。
## 12. StepLR、MultiStepLR 与 ExponentialLR
- `StepLR(optimizer, step_size=50, gamma=0.5)`：每 50 个调度步把学习率乘 0.5。
- `MultiStepLR(optimizer, milestones=[50,125,160], gamma=0.5)`：在指定里程碑乘 0.5。
- `ExponentialLR(optimizer, gamma=0.95)`：每个调度步把学习率乘 0.95，即 $lr_t=lr_0\gamma^t$。
```python
import torch

parameter = torch.nn.Parameter(torch.tensor(1.0))
optimizer = torch.optim.SGD([parameter], lr=0.1)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=2, gamma=0.5)
values = []
for _ in range(5):
    values.append(optimizer.param_groups[0]["lr"])
    optimizer.step()
    scheduler.step()
print(values)  # [0.1, 0.1, 0.05, 0.05, 0.025]
```
## 13. 非凸优化边界（Non-convex Optimization Boundaries）
- 深度网络损失通常非凸，包含平坦区、鞍点、狭长峡谷和大量等价参数化；一阶方法通常只寻求足够好的解，不保证全局最优。
- 高维空间中鞍点往往比“坏局部最小值”更常被讨论；梯度在精确鞍点可为 0，但随机 mini-batch 噪声、Momentum 和曲率会影响能否离开。
- 自适应方法可压缩高梯度坐标步长、放大低梯度坐标相对步长，但不能“轻松解决”所有病态曲率。
## 参考资料（References）
- [PyTorch `torch.optim` 官方文档](https://docs.pytorch.org/docs/stable/optim.html)
- [PyTorch 学习率调度器官方文档](https://docs.pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate)
