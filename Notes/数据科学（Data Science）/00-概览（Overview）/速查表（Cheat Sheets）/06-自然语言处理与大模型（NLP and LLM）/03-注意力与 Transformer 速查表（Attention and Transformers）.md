---
title: "注意力与 Transformer 速查表（Attention and Transformers Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - nlp/transformer
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "Python 3.11+；PyTorch/Hugging Face 配套稳定版"
---
# 注意力与 Transformer 速查表（Attention and Transformers Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
文本流水线必须保存分词器、词表、特殊 token、最大长度、标签映射和评估脚本；训练与推理完全复用。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 缩放点积注意力（Scaled Dot-product Attention）
注意力按查询与键的匹配度汇总值；大白话：当前 token 给其他位置打分，再按分数加权取信息。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|投影|`Q=XWq; K=XWk; V=XWv`|返回查询、键、值|
|分数|`Q @ K.transpose(-2,-1) / sqrt(dk)`|返回注意力 logits|
|掩码|`scores.masked_fill(mask,-inf)`|原地或返回掩码分数|
|权重|`softmax(scores,dim=-1)`|返回和为 1 的权重|
|汇总|`weights @ V`|返回上下文|
|官方实现|`F.scaled_dot_product_attention(q,k,v,attn_mask=None,is_causal=False)`|返回注意力输出|
|多头|`nn.MultiheadAttention(embed_dim,num_heads,batch_first=True)`|返回输出和可选权重|
|因果掩码|`上三角未来位置为不可见`|阻止自回归泄漏|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
import torch.nn.functional as F
q=k=v=torch.tensor([[[[1.,0.],[0.,1.]]]])
y=F.scaled_dot_product_attention(q,k,v)
print(tuple(y.shape))
print(torch.round(y[0,0],decimals=3).tolist())
# 期望输出:
# (1, 1, 2, 2)
# [[0.669, 0.331], [0.331, 0.669]]
```
## Transformer 模块（Transformer Blocks）
残差路径、归一化、注意力与前馈网络构成基本块。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|编码层|`nn.TransformerEncoderLayer(d_model,nhead,batch_first=True)`|返回模块|
|编码堆栈|`nn.TransformerEncoder(layer,num_layers)`|返回编码器|
|解码层|`nn.TransformerDecoderLayer(d_model,nhead,batch_first=True)`|返回模块|
|完整模块|`nn.Transformer(d_model,nhead,...)`|返回编码器-解码器|
|前馈|`Linear(d,4d) -> GELU -> Linear(4d,d)`|返回同维表示|
|层归一|`nn.LayerNorm(d_model)`|返回同形状 Tensor|
|残差|`x=x+sublayer(x)`|保持形状并改善梯度流|
|位置编码|`正弦/学习/旋转位置编码`|向顺序注入位置信息|
|padding mask|src_key_padding_mask shape `(N,S)`|True 位置被忽略|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torch import nn
layer=nn.TransformerEncoderLayer(16,4,batch_first=True)
x=torch.randn(2,5,16); y=layer(x)
print(tuple(y.shape))
# 期望输出:
# (2, 5, 16)
```
## 长序列、缓存与调试（Long Context, Cache, and Debugging）
标准注意力对序列长度的矩阵成本为平方级；缓存只避免重复计算过去 K/V。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|KV Cache|`每层保存历史 key/value`|自回归每步追加并返回缓存|
|Flash Attention|`融合内核计算精确注意力`|减少中间显存，受 dtype/设备约束|
|局部注意力|`每位置只看窗口`|降低长序列成本|
|RoPE|`对 Q/K 施加旋转位置变换`|注入相对位置信息|
|ALiBi|`注意力分数加距离偏置`|无需位置嵌入表|
|梯度检查点|`torch.utils.checkpoint.checkpoint(fn,*args)`|用额外计算换激活显存|
|检查权重|`need_weights=True`|返回注意力权重但可能禁用最快路径|
|掩码检查|`验证每行至少一个可见 key`|避免 softmax 全 `-inf` 产生 NaN|
|形状约定|`明确 batch/head/sequence/dim 顺序`|避免静默广播|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
S=4
mask=torch.triu(torch.ones(S,S,dtype=torch.bool),diagonal=1)
print(mask.int().tolist())
# 期望输出:
# [[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 0, 0, 0]]
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
- [[07-SENet 通道注意力与特征重标定（SENet Channel Attention and Feature Recalibration）]]
- [[03-Seq2Seq 与注意力机制（Seq2Seq and Attention）]]
- [[04-自注意力机制（Self-Attention）]]
- [[01-Transformer 架构与注意力（Transformer Architecture and Attention）]]
- [[02-Transformer PyTorch 实现（Transformer PyTorch Implementation）]]
- [[03-FastText 文本分类与词向量（FastText Classification and Embeddings）]]
- [[04-NLP 迁移学习（NLP Transfer Learning）]]
- [[05-BERT 原理与模型族（BERT Principles and Family）]]
- [[06-ELMo 上下文词表示（ELMo Contextual Embeddings）]]
- [[07-GPT 模型演进（GPT Model Evolution）]]
- [[08-BERT、GPT 与 ELMo 对比（BERT, GPT, and ELMo Comparison）]]
- [[05-Hugging Face Transformers（Hugging Face Transformers）]]
- [[03-注意力 Seq2Seq 机器翻译（Attention Seq2Seq Translation）]]
- [[04-Transformer 机器翻译（Transformer Machine Translation）]]
- [[05-Transformer 语言模型（Transformer Language Model）]]
## 官方参考（Official References）
- [Hugging Face Tokenizer 文档](https://huggingface.co/docs/transformers/main_classes/tokenizer)
