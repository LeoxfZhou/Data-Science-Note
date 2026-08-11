---
title: PyTorch 训练与评估循环（PyTorch Training and Evaluation Loops）
aliases:
  - PyTorch Training Loop
  - PyTorch Evaluation Loop
tags:
  - data-science/deep-learning/pytorch
  - data-science/model-training
status: published
created: 2026-08-11
published_at: 2026-08-11
---
# PyTorch 训练与评估循环（PyTorch Training and Evaluation Loops）
## 1. 模式与梯度上下文（Model Modes and Gradient Contexts）
### 1.1 `model.train()`
- 把模块递归设置为训练模式（Training Mode）。
- 影响 Dropout、BatchNorm 等具有训练/评估分支的模块；它不负责开启梯度，因为梯度记录由 autograd 上下文和张量属性控制。
### 1.2 `model.eval()`
- 等价于 `model.train(False)`，把相关模块切换为评估模式（Evaluation Mode）。
- Dropout 停止随机丢弃，BatchNorm 使用已保存的运行统计量。
- `eval()` 不会关闭梯度，验证与推理仍应使用 `torch.no_grad()` 或 `torch.inference_mode()`。
### 1.3 `no_grad()` 与 `inference_mode()`
- `torch.no_grad()` 关闭反向模式梯度记录，适合验证和普通推理。
- `torch.inference_mode()` 关闭更多 autograd 簿记，纯推理可能更高效，但限制更强。
- 验证通常只需要指标，不调用 `backward()`。

> [!tip] 大白话理解（Plain-language Intuition）
> `train()`/`eval()` 决定模型里的某些层按训练规则还是推理规则工作；`no_grad()`/`inference_mode()` 决定是否记录求导信息。这是两个互相独立的开关，所以评估时通常既要 `eval()`，也要关闭梯度记录。
## 2. 单次参数更新（Single Optimization Step）
1. `optimizer.zero_grad()`：清除或置空历史梯度。
2. `outputs = model(inputs)`：前向传播（Forward Pass）。
3. `loss = criterion(outputs, labels)`：计算损失。
4. `loss.backward()`：反向传播（Backward Pass）。
5. `optimizer.step()`：根据梯度更新参数。
```python
import torch
from torch import nn

model = nn.Linear(4, 3)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
inputs = torch.ones((2, 4))
labels = torch.tensor([0, 2])

optimizer.zero_grad()
outputs = model(inputs)
loss = criterion(outputs, labels)
loss.backward()
optimizer.step()
print(outputs.shape)  # 输出: torch.Size([2, 3])
print(loss.ndim)      # 输出: 0
```
## 3. 训练一个 Epoch（Train One Epoch）
```python
from collections.abc import Iterable

import torch
from torch import nn


def train_one_epoch(
    model: nn.Module,
    loader: Iterable[tuple[torch.Tensor, torch.Tensor]],
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> float:
    model.train()
    total_weighted_loss = 0.0
    total_samples = 0

    for inputs, labels in loader:
        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # criterion 默认返回批次均值时，乘批次大小还原该批总损失，
        # 避免最后一个较小批次与完整批次拥有相同统计权重。
        batch_size = inputs.shape[0]
        total_weighted_loss += loss.item() * batch_size
        total_samples += batch_size

    if total_samples == 0:
        raise ValueError("training loader produced no samples")
    return total_weighted_loss / total_samples
```
该函数依赖外部模型、数据和随机状态，损失数值不固定。
### 3.1 reduction 边界（Reduction Boundary）
- 上述统计假设 `criterion` 返回当前批全部样本的均值。
- `reduction='sum'` 时直接累加 `loss.item()`；`reduction='none'` 时先按任务轴得到逐样本损失再汇总。
- 像素级分割、序列 padding 和类别权重会改变“平均”的分母，指标应与训练目标分开定义。
## 4. 评估循环（Evaluation Loop）
```python
from collections.abc import Iterable

import torch
from torch import nn


def evaluate_classifier(
    model: nn.Module,
    loader: Iterable[tuple[torch.Tensor, torch.Tensor]],
    criterion: nn.Module,
    device: torch.device,
) -> tuple[float, float]:
    model.eval()
    total_weighted_loss = 0.0
    total_correct = 0
    total_samples = 0

    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            logits = model(inputs)
            loss = criterion(logits, labels)

            predictions = logits.argmax(dim=1)
            batch_size = inputs.shape[0]
            total_weighted_loss += loss.item() * batch_size
            total_correct += (predictions == labels).sum().item()
            total_samples += batch_size

    if total_samples == 0:
        raise ValueError("evaluation loader produced no samples")
    return (
        total_weighted_loss / total_samples,
        total_correct / total_samples,
    )
```
- 对互斥多分类，logits 最大位置与 Softmax 后概率最大位置相同，计算类别索引无需先 Softmax。
- 准确率（Accuracy）不适合所有任务；类别不平衡时还需精确率（Precision）、召回率（Recall）、F1 或受试者工作特征曲线下面积（Area Under the ROC Curve, AUROC）。
## 5. 完整 Epoch 控制器（Epoch Controller）
```python
def fit(
    model,
    train_loader,
    validation_loader,
    criterion,
    optimizer,
    device,
    epochs: int,
):
    history = []
    for epoch in range(1, epochs + 1):
        train_loss = train_one_epoch(
            model,
            train_loader,
            criterion,
            optimizer,
            device,
        )
        validation_loss, validation_accuracy = evaluate_classifier(
            model,
            validation_loader,
            criterion,
            device,
        )
        history.append({
            "epoch": epoch,
            "train_loss": train_loss,
            "validation_loss": validation_loss,
            "validation_accuracy": validation_accuracy,
        })
    return history
```
- 该控制器依赖前述函数和外部数据，不附固定输出。
- 训练过程中可以按验证损失或任务指标保存最佳 checkpoint；不要只保存最后一个 epoch。
- 学习率调度器应按其 API 要求在 batch 或 epoch 边界调用；不同调度器的 `step()` 时机不同。
## 6. 图像分类最小闭环（Minimal Image-classification Loop）
- 示例使用 `ImageFolder` 从 `17flowers/train/<class>/...` 目录读取类别，并以 batch size 4/8、3 个 epoch 演示。
- 示例每两个 batch 打印一次 `epoch/batch/current loss`，并在 epoch 末打印平均损失。实际项目应把频率设为配置，避免小数据集日志过少或大数据集 I/O 过多；进度日志不能替代结构化实验记录。
- 完整程序需要先定义数据变换、DataLoader、模型、交叉熵和 SGD；路径应来自配置而不是硬编码 `D:\datas\17flowers\train`。
- 路径不存在应立即报告；空数据集、类别不足和损坏图片也需要显式错误处理。
```python
from pathlib import Path


def validate_training_directory(path: str | Path) -> Path:
    directory = Path(path).expanduser().resolve()
    if not directory.is_dir():
        raise FileNotFoundError(f"training directory does not exist: {directory}")
    if not any(child.is_dir() for child in directory.iterdir()):
        raise ValueError("ImageFolder root must contain class subdirectories")
    return directory
```
该代码检查文件系统，结果依赖本机路径。
## 7. 训练期间评估与保存（Evaluation and Saving During Training）
- 每个 epoch 训练后运行验证，可以观察欠拟合、过拟合和学习率问题。
- 选模指标必须提前定义：分类可能用验证损失、准确率、F1 或 mAP；回归可能用 MAE/RMSE。
- 验证集不得参与梯度更新；测试集不得用于反复调参。
- 保存 checkpoint 时包含 epoch、模型、优化器、调度器、最佳指标和随机状态，详见 [[05-PyTorch 模型持久化与推理（PyTorch Model Persistence and Inference）]]。
## 8. 常见错误（Common Errors）

|错误（Error）|影响（Impact）|修正（Fix）|
|---|---|---|
|忘记 `zero_grad()`|梯度跨 batch 累加|每个普通优化步骤前清理；有意梯度累积时按计划缩放损失|
|验证前未 `eval()`|Dropout/BatchNorm 行为仍处于训练态|验证入口调用 `model.eval()`|
|只 `eval()` 未关闭梯度|构建无用计算图|配合 `no_grad()`/`inference_mode()`|
|按批次数平均损失|尾批次权重失真|按样本数或任务元素数统计|
|用 `len(loader.dataset)` 但采样器只评估子集|指标分母错误|统计循环中实际处理的样本数|
|多分类先 Softmax 再 CrossEntropy|改变损失输入且稳定性降低|损失接收 logits；概率只用于展示或后处理|
|训练日志声称固定“毫秒级”|缺少硬件、批次、预热和并发测量|使用明确基准方案和百分位延迟|

## 关联笔记（Related Notes）
- [[02-PyTorch 模型工程结构与环境（PyTorch Model Engineering Structure and Environment）]]
- [[05-PyTorch 模型持久化与推理（PyTorch Model Persistence and Inference）]]
- [[02-模型欠拟合、过拟合与泛化（Model Underfitting, Overfitting, and Generalization）]]
## 参考资料（References）
- [PyTorch 优化模型参数官方教程](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
- [`torch.nn.Module.train` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.train)
