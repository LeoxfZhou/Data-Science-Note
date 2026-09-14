---
title: "S2 PyTorch、深度学习与 NLP 基础（PyTorch, Deep Learning and NLP）"
aliases:
  - "S2 PyTorch Deep Learning and NLP"
tags:
  - career/llm-application-engineer
  - interview/deep-learning
status: published
created: 2026-08-27
updated: 2026-08-27
---
# S2 PyTorch、深度学习与 NLP 基础（PyTorch, Deep Learning and NLP）
> [!tip] 导航（Navigation）
> 上一阶段：[[02-S1 Python 工程与基础算法（Python Engineering and Algorithms）]]｜[[00-概览（Overview）]]｜下一阶段：[[04-S3 大模型应用基础（LLM Application Fundamentals）]]
## 1. 张量、形状、数据类型与设备（Tensor, Shape, Dtype, and Device）
### 概念与原理（Concept and Mechanism）
- 张量（Tensor）是带形状（Shape）、数据类型（Dtype）和设备（Device）的多维数组。形状决定各轴语义，数据类型影响精度、内存和可用运算，设备决定执行位置。
- 模型输入的批次维、序列维和特征维必须与层的接口契约一致；形状能广播（Broadcasting）不代表语义一定正确。

### 最小代码示例（Minimal Example）
```python
import torch

batch = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32)
print(batch.shape)  # 输出: torch.Size([2, 2])
print(batch.dtype)  # 输出: torch.float32
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么训练时常见 `Expected all tensors to be on the same device`？**

**参考答案：**同一算子无法直接组合位于 CPU 与 GPU 的张量。常见遗漏是只移动模型、没有移动标签，或运行中创建了默认位于 CPU 的新张量。应在数据进入模型前统一设备，并避免在 `forward()` 内无意创建 CPU 张量。

### 相关笔记（Related Notes）
- [[01-PyTorch 张量基础（PyTorch Tensor Fundamentals）]]

## 2. Dataset、DataLoader 与 Batch（Dataset, DataLoader, and Batch）
### 概念与原理（Concept and Mechanism）
- `Dataset` 定义“如何按索引取得一个样本”，`DataLoader` 负责批处理、打乱、并行加载和调用 `collate_fn` 组装不规则样本。
- 训练集通常打乱以减少样本顺序偏差；验证集不需要打乱。可变长度文本必须填充、截断或通过自定义组批逻辑处理。

### 最小代码示例（Minimal Example）
```python
import torch
from torch.utils.data import DataLoader, TensorDataset

features = torch.tensor([[1.0], [2.0], [3.0], [4.0]])
labels = torch.tensor([0, 0, 1, 1])
loader = DataLoader(TensorDataset(features, labels), batch_size=2, shuffle=False)
first_features, first_labels = next(iter(loader))
print(first_features.shape)  # 输出: torch.Size([2, 1])
print(first_labels.tolist()) # 输出: [0, 0]
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：增大 `num_workers` 是否一定能加快训练？**

**参考答案：**不一定。它只可能改善数据准备瓶颈，还会增加进程、序列化、内存和 I/O 压力；数据已经在内存中、存储较慢或平台进程启动代价较高时，过多 worker 反而更慢。应依据 GPU 等待时间和数据加载分析调参。

### 相关笔记（Related Notes）
- [[01-PyTorch 数据集、变换与加载器（PyTorch Datasets, Transforms, and DataLoaders）]]

## 3. 训练、验证与测试流程（Training, Validation, and Testing Flow）
### 概念与原理（Concept and Mechanism）
- 训练集更新参数；验证集用于选择超参数、阈值和最佳检查点；测试集只用于最终无偏估计，不能反复据此调参。
- 标准训练步骤是前向传播（Forward Pass）→ 计算损失（Loss）→ 清空旧梯度 → 反向传播（Backward Pass）→ 优化器更新（Optimizer Step）。

### 最小代码示例（Minimal Example）
```python
import torch
from torch import nn

model = nn.Linear(2, 1)
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
features = torch.tensor([[1.0, 2.0]])
targets = torch.tensor([[1.0]])

predictions = model(features)
loss = nn.functional.mse_loss(predictions, targets)
optimizer.zero_grad()  # 梯度默认累积，不清空会把不同 batch 的梯度叠加。
loss.backward()
optimizer.step()
print(loss.ndim)  # 输出: 0
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么通常先 `zero_grad()` 再 `backward()`？**

**参考答案：**PyTorch 默认把新梯度累加到参数的 `.grad`。普通小批次训练希望每个 batch 独立估计梯度，因此更新前要清空旧梯度；只有明确进行梯度累积时才故意延迟清空。

### 相关笔记（Related Notes）
- [[04-PyTorch 训练与评估循环（PyTorch Training and Evaluation Loops）]]
- [[02-神经网络损失函数与输出契约（Neural Network Loss Functions and Output Contracts）]]
- [[03-反向传播与链式法则（Backpropagation and the Chain Rule）]]
- [[04-梯度下降、优化器与学习率调度（Gradient Descent, Optimizers, and Learning-rate Scheduling）]]

## 4. `train()`、`eval()` 与梯度控制（Training Mode, Evaluation Mode, and Gradient Control）
### 概念与原理（Concept and Mechanism）
- `model.train()` 和 `model.eval()` 切换模块行为，主要影响 Dropout、BatchNorm 等层；它们不会自动开启或关闭梯度。
- `torch.no_grad()` 或推理模式控制自动微分记录，减少推理内存和计算开销；验证时通常同时使用 `eval()` 与无梯度上下文。

### 最小代码示例（Minimal Example）
```python
import torch
from torch import nn

model = nn.Sequential(nn.Linear(2, 2), nn.Dropout(p=0.5))
model.eval()
with torch.no_grad():
    output = model(torch.ones(1, 2))
print(output.requires_grad)  # 输出: False
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：只调用 `model.eval()` 为什么仍可能消耗梯度内存？**

**参考答案：**`eval()` 只改变某些层的运行行为，不关闭自动微分。若输入和参数需要梯度，计算图仍会建立；推理或验证还应使用 `torch.no_grad()` 或适合的推理上下文。

## 5. 可复现性、泛化与数据问题（Reproducibility, Generalization, and Data Problems）
### 概念与原理（Concept and Mechanism）
- 随机种子（Random Seed）控制部分随机源，但不同硬件、并行执行和非确定性算子仍可能造成差异，因此“设种子”不等于字节级完全复现。
- 欠拟合（Underfitting）表现为训练与验证都差；过拟合（Overfitting）表现为训练持续改善而验证恶化；数据泄漏（Data Leakage）让模型在训练时接触本不该看到的验证或测试信息。
- 类别不平衡需要结合 Precision、Recall、F1、分层划分、加权损失或重采样处理，不能只看 Accuracy。

### 最小代码示例（Minimal Example）
```python
import random
import torch

random.seed(42)
torch.manual_seed(42)
print(torch.rand(2).tolist())  # 输出: [0.8822692632675171, 0.9150039553642273]
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：训练准确率很高、验证准确率很低，第一步查什么？**

**参考答案：**先确认训练与验证计算流程一致且数据划分无泄漏，再比较损失曲线和类别分布。若流程正确，才考虑过拟合，并通过数据增强、正则化、减小模型、早停或增加数据改善。

### 相关笔记（Related Notes）
- [[01-神经网络参数初始化与梯度流（Neural Network Initialization and Gradient Flow）]]
- [[02-模型欠拟合、过拟合与泛化（Model Underfitting, Overfitting, and Generalization）]]

## 6. Token、词表、Padding 与 Attention Mask（Tokens, Vocabulary, Padding, and Attention Mask）
### 概念与原理（Concept and Mechanism）
- 字符（Character）、词（Word）和子词（Subword）是不同粒度；Token 是分词器（Tokenizer）输出的模型单位，不一定对应自然语言中的完整词。
- 词表（Vocabulary）把 Token 映射为整数 ID；特殊 Token 表达填充、序列边界或未知项。Padding 对齐批次长度，Truncation 限制输入长度，Attention Mask 告诉模型哪些位置是真实内容。

### 最小代码示例（Minimal Example）
```python
sequences = [[101, 11, 102], [101, 22, 33, 102]]
max_length = max(map(len, sequences))
padded = [sequence + [0] * (max_length - len(sequence)) for sequence in sequences]
masks = [[int(token_id != 0) for token_id in sequence] for sequence in padded]
print(padded)  # 输出: [[101, 11, 102, 0], [101, 22, 33, 102]]
print(masks)   # 输出: [[1, 1, 1, 0], [1, 1, 1, 1]]
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么不能把 Token ID 当作有大小关系的数值特征？**

**参考答案：**Token ID 只是词表索引，ID 之间的数值距离没有语义。模型先通过嵌入层把离散 ID 映射为连续向量，语义关系由训练后的向量与后续网络表示。

### 相关笔记（Related Notes）
- [[06-Hugging Face Tokenizer 与 Datasets 数据管线（Hugging Face Tokenizer and Datasets Pipeline）]]
- [[07-子词分词算法：BPE、WordPiece 与 Unigram（Subword Tokenization Algorithms）]]

## 7. NLP 任务与分类指标（NLP Tasks and Classification Metrics）
### 概念与原理（Concept and Mechanism）
- 文本分类（Text Classification）为输入分配标签；语言建模（Language Modeling）预测 Token 概率；文本生成（Text Generation）按条件逐步采样后续 Token。
- Precision 衡量预测为正的样本中多少正确，Recall 衡量真实正样本中多少被找出，F1 是二者调和平均。混淆矩阵展示每类真实标签与预测标签的组合。

### 最小代码示例（Minimal Example）
```python
true_positive, false_positive, false_negative = 8, 2, 4
precision = true_positive / (true_positive + false_positive)
recall = true_positive / (true_positive + false_negative)
f1 = 2 * precision * recall / (precision + recall)
print(round(precision, 2))  # 输出: 0.8
print(round(recall, 2))     # 输出: 0.67
print(round(f1, 2))         # 输出: 0.73
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：类别严重不平衡时为什么 Accuracy 可能误导？**

**参考答案：**若负类占 99%，模型永远预测负类也有 99% Accuracy，却完全找不到正类。应结合每类 Precision、Recall、F1、混淆矩阵和业务错误成本选择指标。

### 相关笔记（Related Notes）
- [[01-自然语言处理概览（NLP Overview）]]
- [[03-NLP 标准数据集与任务基准（NLP Datasets and Benchmarks）]]

## 8. RNN 与 Transformer（RNN and Transformer）
### 概念与原理（Concept and Mechanism）
- 循环神经网络（Recurrent Neural Network, RNN）按时间步递归更新隐藏状态，天然表达顺序，但长路径反向传播容易梯度消失或爆炸，且时间步依赖限制训练并行。
- Transformer 使用自注意力（Self-Attention）直接建立任意位置之间的依赖，并通过位置编码补充顺序信息；训练并行性更好，但标准全注意力的时间和注意力矩阵空间复杂度随序列长度近似为 $O(n^2)$。

> [!tip] 大白话理解（Plain-language Intuition）
> RNN 像按顺序传话，每一步都依赖上一人；Transformer 像让所有词同时查看相关词。后者更容易并行和捕捉远距离关系，但长文本中“所有人互相查看”会变得昂贵。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：Transformer 是否在所有场景都优于 RNN？**

**参考答案：**不是。Transformer 通常更适合大规模并行训练和长程依赖，但标准注意力在长序列上计算与显存成本高；流式、低资源或严格在线状态场景仍可能使用循环结构、卷积结构或高效注意力变体。

### 相关笔记（Related Notes）
- [[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）]]
- [[01-Transformer 架构与注意力（Transformer Architecture and Attention）]]

## 9. 典型项目模型追问（Common Project-model Questions）
### BP 网络与 MNIST（BP Network and MNIST）
- **原理**：全连接层产生 logits，损失函数衡量预测与标签差异，反向传播依据链式法则计算梯度。
- **面试问题：为什么保存验证集最佳模型，而不是最后一轮模型？**
- **参考答案：**最后一轮可能已经过拟合；按预先定义的验证指标保存最佳检查点，能把模型选择与测试集隔离。
- **相关笔记**：[[01-基于 NumPy 的三层 BP 神经网络（Three-layer BP Neural Network with NumPy）]]。

### AlexNet、ResNet 与迁移学习（AlexNet, ResNet, and Transfer Learning）
- **原理**：卷积提取局部共享特征，池化或步幅压缩空间；残差连接让网络学习残差映射并提供更直接的梯度路径；迁移学习复用预训练表征。
- **面试问题：冻结主干和微调主干如何选择？**
- **参考答案：**数据少、领域相近或算力有限时先冻结主干，只训练分类头；数据更多、领域差异较大时逐步解冻并使用较小学习率，同时监控过拟合和灾难性遗忘。
- **相关笔记**：[[02-AlexNet 与大规模 GPU 视觉训练（AlexNet and Large-scale GPU Vision Training）]]、[[05-ResNet 残差学习与快捷连接（ResNet Residual Learning and Shortcut Connections）]]。

### 语言建模与生成策略（Language Modeling and Decoding）
- **原理**：因果语言模型根据此前 Token 预测下一个 Token。Greedy 每步选最高概率；Temperature 调整分布尖锐度；Top-k 和 Top-p 限制候选集合。
- **面试问题：为什么生成会重复？**
- **参考答案：**模型可能进入高概率循环，过低 Temperature 或过窄候选集合会加剧确定性重复；训练数据、上下文和停止条件也有影响。可调整采样、重复惩罚、停止序列，并检查提示与模型能力。
- **相关笔记**：[[05-Transformer 语言模型（Transformer Language Model）]]、[[05-Hugging Face Transformers（Hugging Face Transformers）]]。

## 参考资料（References）
- [[大模型应用工程师学习计划]]
