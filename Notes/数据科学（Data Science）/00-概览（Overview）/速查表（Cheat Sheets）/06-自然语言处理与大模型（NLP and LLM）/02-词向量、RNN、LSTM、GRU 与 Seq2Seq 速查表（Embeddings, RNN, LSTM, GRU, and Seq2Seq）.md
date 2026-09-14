---
title: "词向量、RNN、LSTM、GRU 与 Seq2Seq 速查表（Embeddings, RNN, LSTM, GRU, and Seq2Seq Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - nlp/sequence-models
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "Python 3.11+；PyTorch/Hugging Face 配套稳定版"
---
# 词向量、RNN、LSTM、GRU 与 Seq2Seq 速查表（Embeddings, RNN, LSTM, GRU, and Seq2Seq Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
文本流水线必须保存分词器、词表、特殊 token、最大长度、标签映射和评估脚本；训练与推理完全复用。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 词向量与嵌入（Embeddings）
嵌入把离散 ID 映射为稠密向量；相近向量只表示训练目标下的相似。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|嵌入层|`nn.Embedding(vocab_size,dim,padding_idx=pad_id)`|输入 ID，返回 `(...,dim)`|
|预训练权重|`nn.Embedding.from_pretrained(weight,freeze=True)`|返回嵌入层|
|词袋嵌入|`nn.EmbeddingBag(num_embeddings,dim,mode='mean')`|直接归约变长集合|
|余弦相似|`F.cosine_similarity(a,b,dim=-1)`|返回去掉比较维的相似度|
|Word2Vec|`gensim.models.Word2Vec(sentences,vector_size=...)`|返回训练模型|
|FastText|`gensim.models.FastText(...)`|利用子词处理未登录词|
|padding|`pad_sequence(sequences,batch_first=True)`|返回补齐批张量|
|打包|`pack_padded_sequence(x,lengths,batch_first=True,enforce_sorted=False)`|返回 PackedSequence|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torch import nn
emb=nn.Embedding(10,4,padding_idx=0)
x=torch.tensor([[1,2,0],[3,0,0]])
print(tuple(emb(x).shape))
print(emb(x)[0,2].tolist())
# 期望输出:
# (2, 3, 4)
# [0.0, 0.0, 0.0, 0.0]
```
## RNN、LSTM 与 GRU（Recurrent Networks）
循环网络按时间更新状态；LSTM/GRU 用门控缓解长依赖梯度问题。大白话：门决定记住、忘掉和输出什么。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|RNN|`nn.RNN(input_size,hidden_size,num_layers=1,batch_first=True)`|返回序列输出和 h_n|
|LSTM|`nn.LSTM(input_size,hidden_size,bidirectional=False)`|返回输出及 `(h_n,c_n)`|
|GRU|`nn.GRU(input_size,hidden_size,batch_first=True)`|返回输出和 h_n|
|双向|`bidirectional=True`|输出最后维变为 `2*hidden_size`|
|层间 Dropout|`dropout=p`|仅多层循环层之间生效|
|初始状态|h0 shape `(layers*directions,N,H)`|传入或默认为零|
|裁剪梯度|`clip_grad_norm_(model.parameters(),max_norm)`|返回裁剪前范数|
|最后有效状态|`按 lengths 索引或使用 h_n`|返回每序列表示|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torch import nn
x=torch.randn(2,5,3)
rnn=nn.LSTM(3,4,batch_first=True,bidirectional=True)
out,(h,c)=rnn(x)
print(tuple(out.shape),tuple(h.shape),tuple(c.shape))
# 期望输出:
# (2, 5, 8) (2, 2, 4) (2, 2, 4)
```
## Seq2Seq、解码与评估（Seq2Seq and Decoding）
教师强制用于训练，推理时模型消费自身输出，存在暴露偏差。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|编码器|`encoder(src,lengths)`|返回上下文和状态|
|教师强制|`decoder_input=target[:,t-1]`|训练时使用真值前 token|
|贪心解码|`next_id=logits.argmax(-1)`|返回局部最高概率 token|
|束搜索|`保留 top-k 累计对数概率序列`|返回候选序列|
|长度惩罚|`score/log(length)^alpha`|减轻偏好短序列|
|结束判断|`生成 eos 或达到 max_new_tokens`|停止当前序列|
|掩码损失|`CrossEntropyLoss(ignore_index=pad_id)`|padding 不计损失|
|注意力|`softmax(query·keys) @ values`|返回上下文向量|
|Scheduled Sampling|`按概率混用真值和模型输出`|缓解训练推理输入差异|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
logits=torch.tensor([[[1.,3.],[4.,2.]]])
ids=logits.argmax(-1)
print(ids.tolist())
# 期望输出:
# [[1, 0]]
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
- [[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）]]
- [[03-Seq2Seq 与注意力机制（Seq2Seq and Attention）]]
- [[03-FastText 文本分类与词向量（FastText Classification and Embeddings）]]
- [[03-注意力 Seq2Seq 机器翻译（Attention Seq2Seq Translation）]]
## 官方参考（Official References）
- [Hugging Face Tokenizer 文档](https://huggingface.co/docs/transformers/main_classes/tokenizer)
