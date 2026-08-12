---
title: PyTorch 全连接网络与手机价格分类实践（PyTorch MLP and Phone-price Classification）
tags:
  - data-science/deep-learning/pytorch
  - data-science/deep-learning/classification
  - data-science/tabular-data
status: published
created: 2026-08-11
published_at: 2026-08-12
---
# PyTorch 全连接网络与手机价格分类实践（PyTorch MLP and Phone-price Classification）
## 1. 任务定义（Task Definition）
- 数据含 2,000 条二手手机记录、20 个特征和 4 个价格区间标签 `0–3`。
- 目标是预测价格区间而非连续价格，因此属于互斥多分类（Multi-class Classification）。
- 该实验使用 1,600 条训练数据与 400 条验证数据；正式实验还应保留独立测试集，避免把验证结果当作最终无偏性能。
## 2. 数据集构建（Dataset Construction）
```python
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import TensorDataset


def create_datasets(csv_path: Path) -> tuple[TensorDataset, TensorDataset, int, int]:
    data = pd.read_csv(csv_path)
    features = data.iloc[:, :-1].astype(np.float32)
    labels = data.iloc[:, -1].astype(np.int64)

    # stratify 保持类别比例；统计量只能在训练集拟合，避免验证集信息泄漏。
    x_train, x_valid, y_train, y_valid = train_test_split(
        features,
        labels,
        train_size=0.8,
        random_state=88,
        stratify=labels,
    )
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train).astype(np.float32)
    x_valid_scaled = scaler.transform(x_valid).astype(np.float32)

    train_dataset = TensorDataset(
        torch.from_numpy(x_train_scaled),
        torch.from_numpy(y_train.to_numpy()),
    )
    valid_dataset = TensorDataset(
        torch.from_numpy(x_valid_scaled),
        torch.from_numpy(y_valid.to_numpy()),
    )
    return train_dataset, valid_dataset, features.shape[1], labels.nunique()
```
- 该代码读取外部 CSV，无法给出固定 Output；数据结构要求 `input_dim=20`、`class_count=4`。
- `StandardScaler` 对树模型未必必要，但对基于梯度的 MLP 可改善不同特征尺度造成的病态曲率。
## 3. 基线网络（Baseline Network）
```python
import torch
from torch import nn


class PhonePriceMLP(nn.Module):
    def __init__(self, input_dim: int, class_count: int) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, class_count),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        # CrossEntropyLoss 需要 Logits；这里不能先做 Softmax。
        return self.network(features)


model = PhonePriceMLP(input_dim=20, class_count=4)
print(model(torch.randn(8, 20)).shape)  # torch.Size([8, 4])
print(sum(parameter.numel() for parameter in model.parameters()))  # 36740
```
## 4. 训练函数（Training Function）
```python
from pathlib import Path
from time import perf_counter

import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset


def train_model(
    train_dataset: Dataset,
    input_dim: int,
    class_count: int,
    checkpoint_path: Path,
    epochs: int = 50,
) -> PhonePriceMLP:
    torch.manual_seed(0)
    loader = DataLoader(train_dataset, shuffle=True, batch_size=8)
    model = PhonePriceMLP(input_dim, class_count)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

    for epoch in range(epochs):
        model.train()
        started = perf_counter()
        loss_sum = 0.0
        sample_count = 0
        for features, labels in loader:
            optimizer.zero_grad()
            logits = model(features)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            # 按样本加权，避免尾批次较小时仍与完整批次同权。
            loss_sum += loss.item() * labels.size(0)
            sample_count += labels.size(0)
        print(
            f"epoch={epoch + 1:03d} "
            f"loss={loss_sum / sample_count:.4f} "
            f"seconds={perf_counter() - started:.2f}"
        )

    # 写 checkpoint 有外部副作用，因此不提供固定 Output。
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), checkpoint_path)
    return model
```
## 5. 评估函数（Evaluation Function）
```python
import torch
from torch.utils.data import DataLoader, Dataset


def evaluate(model: PhonePriceMLP, valid_dataset: Dataset) -> float:
    loader = DataLoader(valid_dataset, batch_size=64, shuffle=False)
    model.eval()
    correct = 0
    sample_count = 0
    with torch.inference_mode():
        for features, labels in loader:
            predictions = model(features).argmax(dim=1)
            correct += (predictions == labels).sum().item()
            sample_count += labels.size(0)
    return correct / sample_count
```
- `model.train()` 或 `model.eval()` 应在整个训练或评估阶段设置一次，不需要在每个 batch 内重复调用。
- 评估必须关闭梯度记录；只有 `model.eval()` 不会减少 autograd 开销。
- 从本地权重加载时应使用与目标设备匹配的 `map_location`，只加载可信 checkpoint，并在版本支持时优先使用仅权重模式。
## 6. 基线配置与结果记录（Baseline Configuration and Result Record）
- 三层网络 `20→128→256→4`、SGD、学习率 $10^{-3}$、batch size 8、50 epochs 的验证准确率记录为 `0.64250`。由于数据集和完整运行环境未随笔记提供，该数值属于历史实验记录，当前无法复现验证。
- 该数值没有数据文件、依赖版本和运行日志佐证，不能当作当前复现结果。
## 7. 扩展实验配置（Extended Experiment Configuration）

> [!tip] 大白话理解（Plain-language Intuition）
> 端到端训练流程可以看成一条不能打乱顺序的流水线：先把训练数据的处理规则学出来，再用同一规则处理验证和测试数据；模型只在训练集上更新参数，验证集负责选方案，测试集最后只负责验收。任何一步偷看测试答案，都会让最终指标显得虚高。
- 数据划分增加 `stratify=y`；特征使用 `StandardScaler`。
- 网络扩大为 `20→128→256→512→128→4`，隐藏层使用 ReLU。
- 优化器从 SGD 改为 Adam，学习率从 $10^{-3}$ 改为 $10^{-4}$，仍训练 50 epochs。
- 这些变量同时变化，无法判断增益来自哪一项；网络加深可能提升容量，也可能过拟合，Adam 与更小学习率也不保证优于调好的 SGD。
## 8. 推荐实验顺序（Recommended Experiment Order）
1. 固定划分、随机种子和指标，保存未标准化的简单基线。
2. 只加入标准化，确认是否改善收敛。
3. 单独比较 SGD、SGD + Momentum、AdamW，并分别搜索学习率。
4. 再调整宽度、深度、BatchNorm、Dropout 和 weight decay。
5. 同时记录训练/验证损失与准确率，多次运行报告均值和波动。
6. 最后在从未参与调参的测试集评估，并保存预处理器、标签映射和模型权重。
## 9. 常见错误（Common Errors）
- 在 `CrossEntropyLoss` 前做 Softmax。
- 在划分数据前对全数据 `fit_transform`，造成数据泄漏。
- 目标不是 `long` 类别索引或标签超出 `[0,C)`。
- 按 batch 平均值再简单求平均，尾批次造成损失权重偏差。
- 评估时漏掉 `eval()` 或推理上下文。
- 用一次 `0.64250` 准确率判断模型优劣，不看类别不平衡、混淆矩阵和随机波动。
