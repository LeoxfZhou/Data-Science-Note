---
title: PyTorch 线性回归实战（PyTorch Linear Regression）
aliases:
  - PyTorch Linear Regression
  - PyTorch 线性回归
tags:
  - data-science/deep-learning/pytorch
  - data-science/machine-learning/regression
status: published
published_at: 2026-08-11
created: 2026-08-11
---
# PyTorch 线性回归实战（PyTorch Linear Regression）
## 1. 任务与模型（Task and Model）
### 1.1 线性回归（Linear Regression）
- 单特征线性回归用仿射函数（Affine Function）拟合连续目标：
$$
\hat{y}=wx+b
$$
- `w` 是权重（Weight），`b` 是偏置（Bias），$\hat{y}$ 是预测值（Prediction），$y$ 是真实目标（Target）。
- 示例使用 `sklearn.datasets.make_regression()` 生成 100 个样本、1 个特征、噪声强度 10、真实偏置 14.5 的数据，并返回真实系数用于比较。
### 1.2 均方误差（Mean Squared Error）
对 $N$ 个样本，均方误差（Mean Squared Error, MSE）为：
$$
\operatorname{MSE}=\frac{1}{N}\sum_{i=1}^{N}(\hat{y}_i-y_i)^2
$$
- `nn.MSELoss()` 默认 `reduction='mean'`，返回当前输入中全部误差元素的平均值。
- 如果按小批次（Mini-batch）统计整个 epoch 的平均损失，不能简单平均不同大小批次的批均值；应把每批均值乘以批次样本数后累加，再除以 epoch 总样本数。
### 1.3 训练的四个组成部分（Four Training Components）
1. 准备训练数据（Training Data）。
2. 构建模型（Model）。
3. 设置损失函数（Loss Function）和优化器（Optimizer）。
4. 执行训练循环（Training Loop）。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/02-框架与工具（Frameworks and Tools）/03-PyTorch 线性回归实战（PyTorch Linear Regression）/03-PyTorch 线性回归实战（PyTorch Linear Regression）-20260328152707925.png|PyTorch 线性回归组件]]
## 2. 核心 API 映射（Core API Mapping）

|职责（Responsibility）|PyTorch API|本例作用|
|---|---|---|
|数据集（Dataset）|`TensorDataset`|把特征张量和目标张量按样本配对|
|数据加载器（Data Loader）|`DataLoader`|分批、打乱并迭代数据|
|线性模型（Linear Model）|`nn.Linear`|实现 $xW^{\mathsf T}+b$|
|损失函数（Loss Function）|`nn.MSELoss`|度量预测与连续目标的平方误差|
|优化器（Optimizer）|`optim.SGD`|按梯度下降更新权重和偏置|

### 2.1 `TensorDataset`
- 每个输入张量的第 0 维长度必须一致；`dataset[i]` 返回各张量第 `i` 个元素组成的元组。
```python
import torch
from torch.utils.data import TensorDataset

features = torch.tensor([[1.0], [2.0], [3.0]])
targets = torch.tensor([[3.0], [5.0], [7.0]])
dataset = TensorDataset(features, targets)
print(len(dataset))           # 3
print(dataset[1][0].item())   # 2.0
print(dataset[1][1].item())   # 5.0
```
### 2.2 `DataLoader`
- **dataset**：实现数据集协议的数据对象。
- **batch_size**：每个小批次的最大样本数；最后一个批次可能更小。
- **shuffle**：每个 epoch 是否重新打乱样本，训练集通常为 `True`，验证与测试通常为 `False`。
- **drop_last**：是否丢弃不满 `batch_size` 的最后批次；默认 `False`，本例保留全部训练样本。
- **generator**：可选随机数生成器，用于控制单进程打乱顺序；多进程完整复现还需设置 worker 随机种子。
```python
import torch
from torch.utils.data import DataLoader, TensorDataset

dataset = TensorDataset(torch.arange(10).reshape(5, 2), torch.arange(5))
loader = DataLoader(dataset, batch_size=2, shuffle=False)
print([batch_x.shape[0] for batch_x, _ in loader])  # [2, 2, 1]
```
### 2.3 `nn.Linear`、`nn.MSELoss` 与 `optim.SGD`
- `nn.Linear(in_features=1, out_features=1)` 创建一个权重和一个偏置。
- `nn.MSELoss()` 比较形状兼容的预测和目标。若因广播让不正确形状也能运行，结果可能没有语义意义，因此应显式保证二者形状一致。
- `optim.SGD(model.parameters(), lr=1e-2)` 注册需要更新的模型参数，并以学习率（Learning Rate）0.01 执行随机梯度下降（Stochastic Gradient Descent）。
```python
import torch
from torch import nn, optim

model = nn.Linear(in_features=1, out_features=1)
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=1e-2)
print(model(torch.ones((4, 1))).shape)  # torch.Size([4, 1])
print(type(criterion).__name__)         # 'MSELoss'
print(type(optimizer).__name__)         # 'SGD'
```
## 3. 正确训练循环（Correct Training Loop）
### 3.1 单批次顺序（Per-batch Order）
1. 把批次迁移到与模型相同的设备，并确保浮点类型兼容。
2. `optimizer.zero_grad()` 清除上一批梯度。
3. `prediction = model(features)` 执行前向传播。
4. `loss = criterion(prediction, targets)` 计算损失。
5. `loss.backward()` 计算并累积梯度。
6. `optimizer.step()` 更新参数。
### 3.2 Epoch 损失统计（Epoch Loss Accounting）
- `total_loss` 和 `train_sample` 必须在每个 epoch 开头重置；如果把它们放在 epoch 循环外，`epoch_loss` 会变成“从训练开始到当前 epoch 的累计平均”，而不是当前 epoch 的平均损失。
- 如果目标是画每个 epoch 的损失，应在每个 epoch 开头重置累计值。
- 每个 batch 只把计数器加 1 得到的是批次数；要计算严格的样本平均，必须按 `batch_x.shape[0]` 累加样本数，使最后一个小批次按其实际大小加权。
```python
for epoch in range(epochs):
    model.train()
    total_weighted_loss = 0.0
    total_samples = 0
    for batch_x, batch_y in dataloader:
        optimizer.zero_grad()
        prediction = model(batch_x)
        loss = criterion(prediction, batch_y)
        loss.backward()
        optimizer.step()

        batch_size = batch_x.shape[0]
        total_weighted_loss += loss.item() * batch_size
        total_samples += batch_size

    epoch_loss = total_weighted_loss / total_samples
```
该片段依赖外部定义的 `model`、`dataloader`、`optimizer`、`criterion` 与 `epochs`，因此不附固定 Output。
## 4. 完整可运行案例（Complete Runnable Example）
```python
from __future__ import annotations

import matplotlib.pyplot as plt
import torch
from sklearn.datasets import make_regression
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset


# 中文字体是否可用取决于操作系统；缺少 SimHei 时 Matplotlib 会回退并警告。
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def create_dataset() -> tuple[torch.Tensor, torch.Tensor, float]:
    """生成单特征线性回归数据，并在进入模型前统一为 float32。"""
    features, targets, coefficient = make_regression(
        n_samples=100,
        n_features=1,
        noise=10,
        coef=True,
        bias=14.5,
        random_state=0,
    )

    # sklearn 默认常返回 float64，而 nn.Linear 默认参数为 float32。
    # 在数据入口统一类型，避免每个 batch 重复转换并防止 dtype 不匹配。
    feature_tensor = torch.tensor(features, dtype=torch.float32)
    target_tensor = torch.tensor(targets, dtype=torch.float32).reshape(-1, 1)
    return feature_tensor, target_tensor, float(coefficient)


def train(
    epochs: int = 100,
    batch_size: int = 16,
    learning_rate: float = 1e-2,
) -> tuple[nn.Linear, list[float], torch.Tensor, torch.Tensor, float]:
    """训练线性模型，并返回模型、每轮损失及绘图所需数据。"""
    torch.manual_seed(0)
    features, targets, true_coefficient = create_dataset()
    dataset = TensorDataset(features, targets)

    # 单独的生成器让 DataLoader 打乱顺序可复现，不依赖其他随机调用的先后。
    shuffle_generator = torch.Generator().manual_seed(0)
    dataloader = DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=True,
        drop_last=False,
        generator=shuffle_generator,
    )

    model = nn.Linear(in_features=1, out_features=1)
    criterion = nn.MSELoss(reduction="mean")
    optimizer = optim.SGD(params=model.parameters(), lr=learning_rate)
    epoch_losses: list[float] = []

    for _ in range(epochs):
        model.train()
        total_weighted_loss = 0.0
        total_samples = 0

        for batch_features, batch_targets in dataloader:
            # 梯度默认累加，因此每个优化步骤前必须清除上一批梯度。
            optimizer.zero_grad()
            predictions = model(batch_features)
            loss = criterion(predictions, batch_targets)
            loss.backward()
            optimizer.step()

            current_batch_size = batch_features.shape[0]
            total_weighted_loss += loss.item() * current_batch_size
            total_samples += current_batch_size

        epoch_losses.append(total_weighted_loss / total_samples)

    print(f"learned weight: {model.weight.item():.4f}")
    print(f"learned bias: {model.bias.item():.4f}")
    print(f"true weight: {true_coefficient:.4f}")
    print("prediction shape:", model(features).shape)  # torch.Size([100, 1])
    return model, epoch_losses, features, targets, true_coefficient


def plot_results(
    model: nn.Linear,
    epoch_losses: list[float],
    features: torch.Tensor,
    targets: torch.Tensor,
    true_coefficient: float,
) -> None:
    """绘制损失曲线、训练拟合直线与数据生成时的真实直线。"""
    plt.figure()
    plt.plot(range(1, len(epoch_losses) + 1), epoch_losses)
    plt.xlabel("训练轮次（Epoch）")
    plt.ylabel("均方误差（MSE）")
    plt.title("损失变化曲线")
    plt.grid(True)

    x_line = torch.linspace(features.min(), features.max(), 1000).reshape(-1, 1)
    model.eval()
    # 绘图预测不参与训练；关闭梯度可避免构建无用计算图。
    with torch.inference_mode():
        predicted_line = model(x_line)
        true_line = x_line * true_coefficient + 14.5

    plt.figure()
    plt.scatter(features.numpy(), targets.numpy(), label="样本", alpha=0.6)
    plt.plot(x_line.numpy(), predicted_line.numpy(), label="训练模型")
    plt.plot(x_line.numpy(), true_line.numpy(), label="真实关系")
    plt.xlabel("特征（Feature）")
    plt.ylabel("目标（Target）")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    trained_model, losses, x, y, true_coef = train()
    plot_results(trained_model, losses, x, y, true_coef)
```
> [!note] 输出说明（Output Notes）
> 该程序会打印训练权重、偏置、真实权重与 `torch.Size([100, 1])`，并打开两幅图。具体浮点值受 PyTorch 版本与数值实现影响；可靠预期是学习权重接近 `make_regression` 返回系数、偏置接近 14.5，且损失总体下降。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/02-框架与工具（Frameworks and Tools）/03-PyTorch 线性回归实战（PyTorch Linear Regression）/03-PyTorch 线性回归实战（PyTorch Linear Regression）-20260328152713641.png|训练损失曲线]]
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/02-框架与工具（Frameworks and Tools）/03-PyTorch 线性回归实战（PyTorch Linear Regression）/03-PyTorch 线性回归实战（PyTorch Linear Regression）-20260328152714017.png|训练拟合与真实直线]]
## 5. 实现选择与工程边界（Implementation Choices and Engineering Boundaries）

|实现要点（Implementation Point）|推荐做法（Recommended Practice）|原因（Reason）|
|---|---|---|
|张量数据类型（Tensor Dtype）|在数据入口直接指定 `torch.float32`|避免每批重复转换，并集中表达类型意图|
|目标形状（Target Shape）|在数据入口统一为 `(N,1)`|避免训练时重复变形和意外广播警告|
|Epoch 损失统计（Loss Accounting）|每个 epoch 重置累计量并按样本数加权|确保曲线表示逐 epoch 样本平均，而不是跨 epoch 累计平均|
|批次计数（Batch Counting）|按 `batch_x.shape[0]` 累加样本数|避免把不完整尾批次与完整批次赋予相同权重|
|推理绘图（Inference Plotting）|结合 `model.eval()` 与 `torch.inference_mode()`|避免建立无用计算图，并正确切换状态相关模块|
|批量预测（Batched Prediction）|直接调用 `model(x_line)`|避免 Python 逐元素循环、额外复制和梯度警告|
|可复现性（Reproducibility）|同时设置全局随机种子与 DataLoader 生成器|使参数初始化和批次顺序在多次运行间可比较|

> [!tip] 大白话理解（Plain-language Intuition）
> 线性回归就是寻找一条最贴近样本的直线。损失函数衡量“这条线离所有真实点总体有多远”，梯度告诉参数怎样移动能让距离变小；训练循环只是反复计算误差、求梯度、移动直线，直到继续调整带来的改善很小。

## 6. 诊断与改进（Diagnostics and Improvements）
### 6.1 损失不下降（Loss Does Not Decrease）
- 检查特征和模型参数是否具有兼容 `dtype`、`device`。
- 检查是否遗漏 `loss.backward()` 或 `optimizer.step()`。
- 检查学习率是否过大导致发散，或过小导致收敛缓慢。
- 检查预测与目标形状，避免无意广播。
- 检查数据尺度；多特征任务常需要标准化（Standardization）。
### 6.2 参数与梯度检查（Parameter and Gradient Inspection）
```python
for name, parameter in model.named_parameters():
    print(name, parameter.shape, parameter.grad is None)
```
该片段依赖训练上下文；在 `backward()` 前梯度通常为 `None`，在 `backward()` 后应存在，除非参数未参与损失计算。
### 6.3 训练集、验证集与泛化（Training, Validation, and Generalization）
- 本例只演示训练闭环，没有划分验证集或测试集，不能据此评估泛化能力（Generalization）。
- 实际项目应分别报告训练与验证指标，在验证阶段使用 `model.eval()` 和无梯度上下文，并避免用测试集调参。
## 7. 关联笔记（Related Notes）
- [[01-PyTorch 张量基础（PyTorch Tensor Fundamentals）]]
- [[02-PyTorch 自动微分与神经网络组件（PyTorch Autograd and Neural Network Components）]]
## 参考资料（References）
- [PyTorch 基础学习路径（Learn the Basics）](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)
- [PyTorch 优化模型参数（Optimizing Model Parameters）](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
- [`torch.nn.Linear` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html)
- [`torch.nn.MSELoss` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.MSELoss.html)
