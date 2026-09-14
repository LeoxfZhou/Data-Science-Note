---
title: "BERT、GPT、ELMo 与预训练速查表（BERT, GPT, ELMo, and Pretraining Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - nlp/pretraining
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "Python 3.11+；PyTorch/Hugging Face 配套稳定版"
---
# BERT、GPT、ELMo 与预训练速查表（BERT, GPT, ELMo, and Pretraining Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
文本流水线必须保存分词器、词表、特殊 token、最大长度、标签映射和评估脚本；训练与推理完全复用。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 预训练目标与架构（Objectives and Architectures）
预训练从大规模无标注文本学习表示，再通过微调、提示或检索适配任务。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|ELMo|`双向语言模型上下文层加权`|返回上下文词表示|
|BERT|`掩码语言建模编码器`|返回双向上下文表示|
|GPT|`因果语言建模解码器`|返回下一个 token logits|
|MLM|`随机遮盖 token 并预测原 token`|只对选中位置计损失|
|Causal LM|`预测每个位置的下一个 token`|标签相对输入移一位|
|NSP/SOP|`判断句间关系/顺序`|返回句级分类损失|
|SentencePiece|`从原始文本学习子词模型`|返回可逆子词 ID|
|BPE|`反复合并高频符号对`|得到子词词表|
|特殊 token|`CLS/SEP/MASK/BOS/EOS/PAD`|参与任务格式与掩码|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。
## 下游任务与头（Downstream Tasks and Heads）
任务头只读取所需表示；token 任务需把子词预测映射回原词。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|序列分类|`AutoModelForSequenceClassification.from_pretrained(name,num_labels=n)`|返回分类模型|
|Token 分类|`AutoModelForTokenClassification...`|返回每 token logits|
|抽取问答|`AutoModelForQuestionAnswering...`|返回 start/end logits|
|掩码预测|`AutoModelForMaskedLM...`|返回词表 logits|
|文本生成|`AutoModelForCausalLM...`|返回因果 LM|
|句向量|`池化 token 表示并归一化`|返回 `(N,D)` 嵌入|
|冻结骨干|`for p in model.base_model.parameters(): p.requires_grad=False`|只训练任务头|
|分层学习率|`骨干小 lr、头部大 lr`|返回优化器参数组|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
hidden=torch.tensor([[[1.,0.],[0.,1.],[1.,1.]]])
mask=torch.tensor([[1,1,0]]).unsqueeze(-1)
pooled=(hidden*mask).sum(1)/mask.sum(1)
print(pooled.tolist())
# 期望输出:
# [[0.5, 0.5]]
```
## 微调、参数高效与生成（Fine-tuning, PEFT, and Generation）
全量微调改全部权重；PEFT 只训练小量增量参数。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|全量微调|`optimizer(model.parameters())`|更新全部可训练参数|
|LoRA|`低秩矩阵注入注意力/线性层`|训练适配器参数|
|Prefix/Prompt Tuning|`训练连续虚拟 token`|保持骨干冻结|
|量化 LoRA|`4-bit 基座 + LoRA`|降低微调显存|
|贪心生成|`model.generate(**inputs,max_new_tokens=n)`|返回 token ID|
|采样|`do_sample=True,temperature=.7,top_p=.9`|返回随机生成序列|
|束搜索|`num_beams=4,do_sample=False`|返回高累计分候选|
|重复控制|`repetition_penalty / no_repeat_ngram_size`|改变 logits|
|终止|`eos_token_id / stopping_criteria`|控制生成结束|
|保存适配器|`peft_model.save_pretrained(path)`|写文件|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。
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
- [[01-Transformer 架构与注意力（Transformer Architecture and Attention）]]
- [[02-Transformer PyTorch 实现（Transformer PyTorch Implementation）]]
- [[03-FastText 文本分类与词向量（FastText Classification and Embeddings）]]
- [[04-NLP 迁移学习（NLP Transfer Learning）]]
- [[05-BERT 原理与模型族（BERT Principles and Family）]]
- [[06-ELMo 上下文词表示（ELMo Contextual Embeddings）]]
- [[07-GPT 模型演进（GPT Model Evolution）]]
- [[08-BERT、GPT 与 ELMo 对比（BERT, GPT, and ELMo Comparison）]]
- [[06-预训练模型迁移学习实践（Pretrained Model Transfer Learning Practice）]]
## 官方参考（Official References）
- [Hugging Face Tokenizer 文档](https://huggingface.co/docs/transformers/main_classes/tokenizer)
