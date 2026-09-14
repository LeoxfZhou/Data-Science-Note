---
title: "Hugging Face Tokenizer、Datasets 与 Models 速查表（Hugging Face Tokenizers, Datasets, and Models Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - hugging-face
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "Python 3.11+；Transformers 4.x/5.x 迁移期；Datasets 3.x/4.x；Tokenizers 0.20+；PEFT 0.15+"
---
# Hugging Face Tokenizer、Datasets 与 Models 速查表（Hugging Face Tokenizers, Datasets, and Models Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
文本流水线必须保存分词器、词表、特殊 token、最大长度、标签映射和评估脚本；训练与推理完全复用。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 2. 包级安装与导入索引（Package Installation and Import Index）
### 2.1 Transformers 模型接口（Transformers Model APIs）
- **安装包（Distribution）**：`transformers`。
- **导入模块（Import Module）**：`transformers`。
- **安装命令（Installation）**：`python -m pip install -U transformers`；需要 PyTorch 后端时可安装 `transformers[torch]`。
- **用途（Purpose）**：统一加载预训练配置、分词器、模型、任务流水线和训练器。
- **正式笔记（Detailed Note）**：[[05-Hugging Face Transformers（Hugging Face Transformers）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|加载分词器|`AutoTokenizer.from_pretrained(name_or_path)`|下载或读取本地文件，返回分词器|
|加载任务模型|`AutoModelForSequenceClassification.from_pretrained(name_or_path)`|下载或读取权重，返回模型|
|快速推理|`pipeline(task, model=...)`|返回任务流水线|
|生成文本|`model.generate(**inputs, max_new_tokens=...)`|返回 token ID 张量|
|保存模型|`model.save_pretrained(path)`|写入配置与权重文件|

```python
from transformers import AutoConfig

config = AutoConfig.for_model("bert", hidden_size=64, num_hidden_layers=2)
print(config.model_type, config.hidden_size)  # 输出: bert 64
```
- **副作用边界（Side-effect Boundary）**：`from_pretrained()` 默认可能联网下载并写缓存；离线或生产环境应固定 revision，并使用已验证的本地快照。
### 2.2 Datasets 数据集（Hugging Face Datasets）
- **安装包（Distribution）**：`datasets`。
- **导入模块（Import Module）**：`datasets`。
- **安装命令（Installation）**：`python -m pip install -U datasets`。
- **用途（Purpose）**：表格式数据集、映射处理、批处理、缓存和 Hub 数据读取。
- **正式笔记（Detailed Note）**：[[06-Hugging Face Tokenizer 与 Datasets 数据管线（Hugging Face Tokenizer and Datasets Pipeline）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|从字典创建|`Dataset.from_dict(mapping)`|返回内存数据集|
|读取数据|`load_dataset(path, name=None, split=...)`|可能下载并缓存；返回 Dataset/DatasetDict|
|逐批转换|`dataset.map(fn, batched=True, batch_size=1000)`|返回新数据集并使用缓存|
|筛选|`dataset.filter(predicate)`|返回保留匹配行的新数据集|
|划分|`dataset.train_test_split(test_size=0.2, seed=42)`|返回含 `train`、`test` 的 DatasetDict|
|设置格式|`dataset.with_format('torch', columns=[...])`|返回采用指定输出格式的新视图|

```python
from datasets import Dataset

dataset = Dataset.from_dict({"text": ["a", "bb"], "label": [0, 1]})
long_text = dataset.filter(lambda row: len(row["text"]) > 1)
print(len(dataset), len(long_text), long_text[0]["text"])  # 输出: 2 1 bb
```
- **边界（Boundary）**：`map()` 的批处理函数必须让所有返回列长度一致；关闭缓存或函数不可哈希时会影响复现与速度。
### 2.3 Tokenizers 高性能分词器（Hugging Face Tokenizers）
- **安装包（Distribution）**：`tokenizers`。
- **导入模块（Import Module）**：`tokenizers`。
- **安装命令（Installation）**：`python -m pip install -U tokenizers`。
- **用途（Purpose）**：训练、保存和运行 Rust 加速的完整分词流水线。
- **正式笔记（Detailed Note）**：[[07-子词分词算法：BPE、WordPiece 与 Unigram（Subword Tokenization Algorithms）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建分词器|`Tokenizer(WordPiece(unk_token='[UNK]'))`|返回未训练分词器|
|编码|`tokenizer.encode(text)`|返回含 ID、token 与 offset 的 Encoding|
|解码|`tokenizer.decode(ids)`|返回字符串|
|启用截断|`tokenizer.enable_truncation(max_length=512)`|原地修改运行配置|
|启用填充|`tokenizer.enable_padding(length=512)`|原地修改运行配置|
|保存|`tokenizer.save(path)`|写入 JSON 配置文件|

```python
from tokenizers import Tokenizer
from tokenizers.models import WordLevel

tokenizer = Tokenizer(WordLevel({"[UNK]": 0, "hello": 1}, unk_token="[UNK]"))
print(tokenizer.get_vocab_size())  # 输出: 2
```
- **边界（Boundary）**：模型、规范化器、预分词器与后处理器共同决定结果；只构造词表并不等于完整可用的自然语言分词器。
### 2.4 SentencePiece 子词模型（SentencePiece）
- **安装包（Distribution）**：`sentencepiece`。
- **导入模块（Import Module）**：`sentencepiece`，惯例别名为 `spm`。
- **安装命令（Installation）**：`python -m pip install sentencepiece`。
- **用途（Purpose）**：从原始文本训练 BPE 或 Unigram 子词模型，并进行可逆编码。
- **正式笔记（Detailed Note）**：[[07-子词分词算法：BPE、WordPiece 与 Unigram（Subword Tokenization Algorithms）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|加载模型|`spm.SentencePieceProcessor(model_file=path)`|读取模型并返回回处理器|
|编码为片段|`processor.encode(text, out_type=str)`|返回子词字符串列表|
|编码为 ID|`processor.encode(text, out_type=int)`|返回整数 ID 列表|
|解码|`processor.decode(ids_or_pieces)`|返回重建文本|
|训练|`spm.SentencePieceTrainer.train(input=..., model_prefix=..., vocab_size=...)`|读取语料并写 `.model`、`.vocab`|

```python
import sentencepiece as spm

# spm.SentencePieceTrainer.train(input="corpus.txt", model_prefix="toy", vocab_size=8000)
# 训练读取语料并写模型文件；输出依赖语料，不提供固定结果。
```
### 2.5 PEFT 参数高效微调（Parameter-efficient Fine-tuning, PEFT）
- **安装包（Distribution）**：`peft`。
- **导入模块（Import Module）**：`peft`。
- **安装命令（Installation）**：`python -m pip install -U peft`。
- **用途（Purpose）**：LoRA 等参数高效微调、适配器保存与加载。
- **正式笔记（Detailed Note）**：[[05-Hugging Face Transformers（Hugging Face Transformers）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建 LoRA 配置|`LoraConfig(r=8, lora_alpha=16, target_modules=[...])`|返回适配器配置|
|包装模型|`get_peft_model(base_model, config)`|返回带可训练适配器的模型|
|检查参数|`model.print_trainable_parameters()`|打印可训练与总参数比例|
|保存适配器|`model.save_pretrained(path)`|只写适配器配置与权重|
|加载适配器|`PeftModel.from_pretrained(base_model, path)`|返回组合后的 PEFT 模型|

```python
from peft import LoraConfig

config = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05)
print(config.r, config.lora_alpha)  # 输出: 8 16
```
- **边界（Boundary）**：`target_modules` 必须匹配具体模型层名；适配器权重不能脱离兼容的基础模型配置独立推理。
### 2.6 可选分词与云存储依赖（Optional Tokenization and Cloud Dependencies）
#### regex 增强正则（regex Enhanced Regular Expressions）
- **安装包（Distribution）**：`regex`。
- **导入模块（Import Module）**：`regex`。
- **安装命令（Installation）**：`python -m pip install -U regex`。
- **用途（Purpose）**：为部分 tokenizer 提供 Unicode 属性、可变长后行断言等增强正则能力。
- **正式笔记（Detailed Note）**：[[05-Hugging Face Transformers（Hugging Face Transformers）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|Unicode 属性匹配|`regex.findall(r'\p{Han}+', text)`|返回汉字连续片段列表|
|完整匹配|`regex.fullmatch(pattern, text)`|返回 Match 或 `None`|
|带超时搜索|`regex.search(pattern, text, timeout=seconds)`|返回 Match/`None`；超时抛异常|

```python
import regex

print(regex.findall(r"\p{Han}+", "NLP 与中文分词"))  # 输出: ['与中文分词']
```
#### Sacremoses（Sacremoses）
- **安装包（Distribution）**：`sacremoses`。
- **导入模块（Import Module）**：`sacremoses`。
- **安装命令（Installation）**：`python -m pip install -U sacremoses`。
- **用途（Purpose）**：提供 Moses 分词、去分词和规范化的 Python 实现，供部分旧模型 tokenizer 使用。
- **正式笔记（Detailed Note）**：[[05-Hugging Face Transformers（Hugging Face Transformers）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|分词器|`MosesTokenizer(lang='en')`|返回语言相关分词器|
|分词|`tokenizer.tokenize(text, escape=False)`|返回 token 列表|
|去分词|`MosesDetokenizer(lang='en').detokenize(tokens)`|返回拼接字符串|

```python
from sacremoses import MosesTokenizer

tokens = MosesTokenizer(lang="en").tokenize("It's useful.", return_str=False, escape=False)
print(tokens)  # 输出: ['It', "'s", 'useful', '.']
```
#### Boto3（AWS SDK for Python, Boto3）
- **安装包（Distribution）**：`boto3`。
- **导入模块（Import Module）**：`boto3`。
- **安装命令（Installation）**：`python -m pip install -U boto3`。
- **用途（Purpose）**：旧版模型/数据分发或项目代码访问 Amazon Web Services（AWS）对象存储等服务；不是 Transformers 核心推理必需包。
- **正式笔记（Detailed Note）**：[[05-Hugging Face Transformers（Hugging Face Transformers）]] 的历史依赖清单。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|会话|`boto3.session.Session(profile_name=..., region_name=...)`|返回配置会话；可能读取本机凭据文件|
|客户端|`session.client('s3')`|返回低层服务客户端|
|资源接口|`session.resource('s3')`|返回高层资源代理|
|下载对象|`s3.download_file(bucket, key, path)`|访问网络并写本地文件|

```python
import boto3

session = boto3.session.Session(region_name="us-east-1")
print(session.region_name)  # 输出: us-east-1
# 创建具体服务客户端或执行请求时可能读取本机凭据并访问外部 AWS 服务。
```
## Tokenizer（Tokenizer）
分词器输出 ID、注意力掩码和可选映射；模型与 tokenizer 必须来自兼容 checkpoint。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|加载|`AutoTokenizer.from_pretrained(name_or_path)`|返回 tokenizer|
|批编码|`tokenizer(texts,padding=True,truncation=True,max_length=512,return_tensors='pt')`|返回 BatchEncoding|
|解码|`tokenizer.decode(ids,skip_special_tokens=True)`|返回字符串|
|批解码|`tokenizer.batch_decode(batch_ids,skip_special_tokens=True)`|返回字符串列表|
|词转 ID|`tokenizer.convert_tokens_to_ids(tokens)`|返回 ID 或列表|
|ID 转词|`tokenizer.convert_ids_to_tokens(ids)`|返回 token 或列表|
|添加 token|`tokenizer.add_tokens(new_tokens)`|修改词表并返回新增数|
|调整嵌入|`model.resize_token_embeddings(len(tokenizer))`|修改模型并返回嵌入模块|
|偏移映射|`return_offsets_mapping=True`|返回字符起止位置（fast tokenizer）|
|词对齐|`encoding.word_ids(batch_index=0)`|返回每子词对应原词索引|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
from transformers import AutoTokenizer
tok=AutoTokenizer.from_pretrained("bert-base-uncased")
e=tok("Hello world",return_tensors="pt")
print(sorted(e.keys()))
print(tuple(e["input_ids"].shape))
# 期望输出:
# ['attention_mask', 'input_ids', 'token_type_ids']
# (1, 4)
```
## Datasets（Datasets）
Dataset 使用 Arrow 列式存储；`map` 返回新数据集并可缓存。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|加载|`load_dataset(path,name=None,split=None)`|返回 DatasetDict/Dataset|
|本地字典|`Dataset.from_dict(mapping)`|返回 Dataset|
|查看特征|`dataset.features`|返回列 schema|
|映射|`dataset.map(fn,batched=False,remove_columns=None)`|返回变换数据集|
|筛选|`dataset.filter(fn)`|返回保留行 Dataset|
|排序|`dataset.sort(column)`|返回排序 Dataset|
|拆分|`dataset.train_test_split(test_size=.2,seed=42)`|返回 DatasetDict|
|格式|`dataset.with_format('torch',columns=...)`|返回指定输出格式 Dataset|
|保存磁盘|`dataset.save_to_disk(path)`|写 Arrow 数据|
|流式|`load_dataset(...,streaming=True)`|返回 IterableDataset|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。
## Models、Trainer 与 Pipeline（Models, Trainer, and Pipeline）
`Auto*` 按配置选择具体类；Trainer 封装训练但仍需理解数据、损失和指标。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|配置|`AutoConfig.from_pretrained(name)`|返回模型配置|
|基础模型|`AutoModel.from_pretrained(name)`|返回无任务头模型|
|任务模型|`AutoModelForSequenceClassification.from_pretrained(name)`|返回带头模型|
|输入迁移|`batch={k:v.to(device) for k,v in batch.items()}`|返回新映射|
|前向|`outputs=model(**batch)`|返回 ModelOutput|
|训练参数|`TrainingArguments(output_dir=...,...)`|返回训练配置|
|Trainer|`Trainer(model,args,train_dataset,eval_dataset,...)`|返回训练器|
|训练|`trainer.train(resume_from_checkpoint=None)`|执行训练并返回 TrainOutput|
|评估|`trainer.evaluate()`|返回指标字典|
|快速流水线|`pipeline('text-classification',model=name)`|返回任务 callable|

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
- [[01-PyTorch 数据集、变换与加载器（PyTorch Datasets, Transforms, and DataLoaders）]]
- [[05-Hugging Face Transformers（Hugging Face Transformers）]]
- [[06-Hugging Face Tokenizer 与 Datasets 数据管线（Hugging Face Tokenizer and Datasets Pipeline）]]
- [[03-NLP 标准数据集与任务基准（NLP Datasets and Benchmarks）]]
## 官方参考（Official References）
- [Hugging Face Tokenizer 文档](https://huggingface.co/docs/transformers/main_classes/tokenizer)
- [Transformers 快速开始](https://huggingface.co/docs/transformers/quicktour)
- [Datasets 文档](https://huggingface.co/docs/datasets/)
- [Tokenizers 文档](https://huggingface.co/docs/tokenizers/)
- [PEFT 文档](https://huggingface.co/docs/peft/)
- [SentencePiece 官方仓库](https://github.com/google/sentencepiece)
