---
title: "Hugging Face Tokenizer 与 Datasets 数据管线（Hugging Face Tokenizer and Datasets Pipeline）"
tags:
  - data-science/nlp
  - hugging-face
status: published
created: 2026-08-20
published_at: 2026-08-20
---
# Hugging Face Tokenizer 与 Datasets 数据管线（Hugging Face Tokenizer and Datasets Pipeline）
> [!tip] 大白话理解（Plain-language Intuition）
> `Tokenizer` 像“翻译员”，把人类文本变成模型能计算的整数和掩码；`Datasets` 像“流水线”，负责加载、筛选、切分、批量编码和保存样本。两者接起来后，原始文本才能稳定地进入模型训练或推理。
> [!warning] 版本与输出（Version and Output）
> Token ID 取决于具体检查点（Checkpoint）的词表，示例中的整数只对所示模型成立。在线下载、缓存、磁盘保存和数据导出具有外部副作用，因此不伪造固定输出。
## 1. Tokenizer 的加载与使用（Tokenizer Usage）
### 概述
在 Hugging Face 的 Transformers 库中，每一个预训练模型都配套绑定有一个专用的 Tokenizer，它负责将原始文本转换为模型可以理解的输入格式（如 input_ids、attention_mask 等），是连接原始文本与模型计算之间的关键环节。
这些 Tokenizer 通常集成了从文本到张量的全流程处理能力，主要包括以下几个方面：
- 子词切分（subword tokenization）：将输入文本拆分为子词单元；
- 编码映射：将每个子词转换为对应的整数 ID，即 input_ids；
- 添加特殊 Token（Special Token）n：自动插入如 [CLS]、[SEP] 等任务相关的特殊符号；
- 截断与补齐（truncation & padding）：统一输入序列长度，构造批量输入；
- 生成辅助输入：根据模型需求生成 attention_mask、token_type_ids 等附加字段；
### 加载Tokenizer
在Transformers库中，AutoTokenizer用于加载与指定模型配套的分词器。它会根据模型名称自动选择并实例化正确的分词器类型（如 BertTokenizer、GPT2Tokenizer、T5Tokenizer 等）。
AutoTokenizer的用法与AutoModel相似，具体用法如下：

```python
from transformers import AutoTokenizer
# 加载分词
tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-chinese")
```
上述代码执行的操作如下：
AutoTokenizer 会根据提供的模型名称，从 Hugging Face Hub 上下载所需的文件资源，包括配置文件词表。这些文件会自动缓存到本地，默认路径是：~/.cache/huggingface/hub/。下次加载相同模型时会直接读取缓存，不再联网下载。
注意：如需使用国内镜像站，需配置如下环境变量

```bash
export HF_ENDPOINT=https://hf-mirror.com
```
之后AutoTokenizer便会根据配置文件和词表实例化一个Tokenizer对象。
除了在线加载模型之外，from_pretrained()也支持从本地路径加载模型，要求目录中包含词表和配置文件，代码如下

```python
from transformers import AutoTokenizer
# 加载模型
tokenizer = AutoTokenizer.from_pretrained("./pretrained/bert-base-chinese")
```
### 使用Tokenizer
#### 概述
前文提到过，Transformers库中的Tokenizer包括如下功能：
- 子词切分
- 编码映射
- 添加特殊 Token（Special Token）
- 截断与补齐
- 生成辅助输入
- 下面逐一进行演示：
#### 常用API
##### 分词（tokenize）

```python
from transformers import AutoTokenizer
# 加载分词器和模型
tokenizer = AutoTokenizer.from_pretrained("./pretrained/bert-base-chinese")
tokens = tokenizer.tokenize("我爱自然语言处理")
print(tokens)
```
输出内容如下

```python
['我', '爱', '自', '然', '语', '言', '处', '理']
```
##### token转ID（convert_tokens_to_ids）

```python
from transformers import AutoTokenizer
# 加载分词器和模型
tokenizer = AutoTokenizer.from_pretrained("./pretrained/bert-base-chinese")
tokens = tokenizer.tokenize("我爱自然语言处理")
ids = tokenizer.convert_tokens_to_ids(tokens)
print(ids)
```
输出内容如下

```python
[2769, 4263, 5632, 4197, 6427, 6241, 1905, 4415]
```
##### ID转token（convert_ids_to_tokens）

```python
from transformers import AutoTokenizer
# 加载分词器和模型
tokenizer = AutoTokenizer.from_pretrained("./pretrained/bert-base-chinese")
ids = [2769, 4263, 5632, 4197, 6427, 6241, 1905, 4415]
tokens = tokenizer.convert_ids_to_tokens(ids)
print(tokens)
```
输出内容如下

```python
['我', '爱', '自', '然', '语', '言', '处', '理']
```
##### 编码（encode）
编码是将 tokenize + convert_tokens_to_ids 合并后的结果，通常还会自动添加特殊符号（如 [CLS] 和 [SEP]），除此之外，还支持padding、truncate等功能。

```python
from transformers import AutoTokenizer
# 加载分词器和模型
tokenizer = AutoTokenizer.from_pretrained("./pretrained/bert-base-chinese")
ids = tokenizer.encode("我爱自然语言处理")
print(ids)
```
输出内容如下

```python
[101, 2769, 4263, 5632, 4197, 6427, 6241, 1905, 4415, 102]
```
注：可通过add_special_tokens=False参数禁止添加特殊符号
##### 解码（decode）
解码会将一个 token ID 序列还原为对应的原始文本（或接近的文本）。

```python
from transformers import AutoTokenizer
# 加载分词器和模型
tokenizer = AutoTokenizer.from_pretrained("./pretrained/bert-base-chinese")
ids = [101, 2769, 4263, 5632, 4197, 6427, 6241, 1905, 4415, 102]
string = tokenizer.decode(ids)
print(string)
```
输出内容如下：

```python
[CLS] 我 爱 自 然 语 言 处 理 [SEP]
```
注：可通过skip_special_tokens=True参数跳过特殊符号
##### tokenizer() 方法（即 __call__）
这是最推荐的接口，用于直接构造模型所需的输入，其基本用法如下

```python
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("./pretrained/bert-base-chinese")
text = "我爱自然语言处理"
# 编码文本为模型输入格式
inputs = tokenizer(text)
print(inputs)
```
输出内容如下：

```python
{  'input_ids': [101, 2769, 4263, 5632, 4197, 6427, 6241, 1905, 4415, 102],   'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
```
除去text，tokenizer还提供了多个重要参数：

```python
inputs = tokenizer(
    text,
    padding=True,
    truncation=True,
    max_length=128,
    return_tensors="pt"
)
```
各参数含义如下请参考官方文档。
此外，tokenizer()方法还支持直接对多个文本组成的列表进行批量处理，非常适合用于模型训练或推理。

```python
from transformers import AutoTokenizer
# 加载分词器和模型
tokenizer = AutoTokenizer.from_pretrained("./pretrained/bert-base-chinese")
texts = ["我爱自然语言处理", "我爱人工智能", "我们一起学习"]
inputs = tokenizer(
    texts,
    padding="max_length",  # 自动补齐
    truncation=True,  # 自动截断
    max_length=10,  # 统一最大长度
    return_tensors="pt"  # 返回 PyTorch 张量格式
)
print(inputs)
```
输出内容是一个包含三个字段的字典，每个字段是形状为 (batch_size, seq_len) 的张量：

```python
{
'input_ids': tensor([[ 101, 2769, 4263, 5632, 4197, 6427, 6241, 1905, 4415,  102],
                        [ 101, 2769, 4263,  782, 2339, 3255, 5543,  102,    0,    0],
                        [ 101, 2769,  812,  671, 6629, 2110,  739,  102,    0,    0]]),
'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0]])
}
```
### 与预训练模型配合使用
从文本输入到模型输出的完整流程如下：

```python
from transformers import AutoTokenizer, AutoModel
import torch
# 1. 加载模型和分词器
model_name = "bert-base-chinese"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
# 2. 准备批量文本
texts = ["我爱自然语言处理", "我爱人工智能", "我们一起学习"]
# 3. 编码文本为模型输入格式
encoded = tokenizer(
    texts,
    padding="max_length",
    truncation=True,
    max_length=10,
    return_tensors="pt"
)
# 5. 模型推理（不计算梯度）
with torch.no_grad():
    outputs = model(
        input_ids=encoded["input_ids"],
        attention_mask=encoded["attention_mask"],
        token_type_ids=encoded["token_type_ids"]
    )
# 6. 查看输出张量结构
print(outputs.keys())
print("last_hidden_state:", outputs.last_hidden_state.shape)
print("pooler_output:", outputs.pooler_output.shape)
```
输出内容如下：

```python
odict_keys(['last_hidden_state', 'pooler_output'])
last_hidden_state: torch.Size([3, 10, 768])
pooler_output: torch.Size([3, 768])
```
## 2. Datasets 库（Datasets Library）
### 概述
datasets是 Hugging Face 提供的一个轻量级数据处理库，专为自然语言处理任务设计，能够高效地支持模型训练流程中的数据加载与预处理操作。
它的主要特点包括：
- 加载方便：支持读取本地文件（如 CSV、JSON），也支持加载在线公开数据集；
- 结构清晰：数据集的内部结构类似表格，每条样本由若干字段组成；
- 无缝协作：与 tokenizer 等 Hugging Face 模块高度集成，可直接构造模型输入；
- 功能丰富：支持常见的数据处理操作，如批量映射（.map()）、字段筛选、训练/验证集划分（.train_test_split()）等。
datasets库的安装命令如下：

```python
pip install datasets
```
### 加载数据集
datasets库提供了统一的接口 load_dataset()，既支持从本地文件加载数据，也支持从 Hugging Face Hub 加载在线开源数据集。
#### 加载本地数据
load_dataset()支持多种本地文件格式，如 CSV、JSON、Parquet，并允许一次加载一个或多个文件。其基本语法如下：

```python
from datasets import load_dataset
dataset = load_dataset(format, data_files=路径或字典)
```
参数说明如下：

|参数|类型|说明|
|---|---|---|
|format|str|文件格式，常用的包括 "csv"、"json"、"parquet" 等|
|data_files|str 或 dict|文件路径。可传入字符串（加载单个文件）或字典（加载多个文件，如训练数据/测试数据）|
具体用法如下：
##### 加载多个文件

```python
from datasets import load_dataset
dataset_dict = load_dataset('csv', data_files={
    'train': './data/train.csv',
    'test': './data/test.csv'
})
```
此时返回的是一个包含两个Dataset的 DatasetDict，其中每个Dataset称为一个split。

```python
from datasets import load_dataset
dataset_dict = load_dataset('csv', data_files={
    'train': './data/train.csv',
    'test': './data/test.csv'
})
print(dataset_dict)
# DatasetDict({
#     train: Dataset(...),
#     test: Dataset(...)
# })
```
##### 加载单个文件

```python
from datasets import load_dataset
dataset_dict = load_dataset('csv', data_files='./data/dataset.csv')
```
此时返回的也是一个 DatasetDict，其中只包含默认命名为 "train" 的一个Dataset。

```python
print(dataset_dict)
# DatasetDict({
#     train: Dataset(...)
# })
```
#### 查看数据集
本节以情感分析案例中的评论数据集为例，演示如何使用  `datasets` 的常用 API 查看数据内容：
##### 获取 Dataset
load_dataset()返回的是一个 DatasetDict对象，可以像字典一样通过键名（如 "train"）访问split。

```python
from datasets import load_dataset
dataset_dict = load_dataset('csv', data_files='data/raw/online_shopping_10_cats.csv')
dataset = dataset_dict["train"]
```
此时 dataset是一个 `Dataset` 对象，表示训练集。
##### 访问样本
Dataset支持索引和切片操作来访问样本：

```python
print(dataset[0])       # 单条样本
print(dataset[:3])      # 多条样本（注意返回结构）
```
返回结构说明：

|访问方式|返回示例|
|---|---|
|dataset[0]|{'review': '很喜欢的一本书', 'label': 1, 'cat': '书籍'}|
|dataset[:3]|{'review': ['很喜欢的一本书', '内容丰富', '讲解清晰'], 'label': [1, 1, 1], 'cat': ['书籍','书籍','书籍']}|
##### 访问某个字段值
可以进一步通过字段名访问某个字段的值：

```python
print(dataset[0]['review'])        # 第一条样本的 review 字段
print(dataset[:3]['review'])       # 前三条样本的 review 字段列表
```
#### 加载在线数据
Hugging Face Hub 提供了大量开源数据集，涵盖文本分类、问答、翻译、摘要等任务，可以在官网浏览与搜索：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/06-Hugging Face Tokenizer 与 Datasets 数据管线（Hugging Face Tokenizer and Datasets Pipeline）/06-Hugging Face Tokenizer 与 Datasets 数据管线（Hugging Face Tokenizer and Datasets Pipeline）-2026082011300004.png]]
每个数据集页面都会提供示例代码，方便直接复制使用。

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/06-Hugging Face Tokenizer 与 Datasets 数据管线（Hugging Face Tokenizer and Datasets Pipeline）/06-Hugging Face Tokenizer 与 Datasets 数据管线（Hugging Face Tokenizer and Datasets Pipeline）-2026082011300005.png]]
具体代码如下图所示：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/06-Hugging Face Tokenizer 与 Datasets 数据管线（Hugging Face Tokenizer and Datasets Pipeline）/06-Hugging Face Tokenizer 与 Datasets 数据管线（Hugging Face Tokenizer and Datasets Pipeline）-2026082011300006.png]]
执行上述代码时，数据集会自动从 Hugging Face Hub 下载，并缓存至本地用户目录，默认路径为：~/.cache/huggingface/datasets/
后续再次使用时将自动从本地加载，无需联网或重复下载。
加载完成后，返回一个 DatasetDict对象，结构和使用方式与本地数据完全一致。
### 预处理数据集
除了加载数据， datasets库还支持常见的数据预处理操作，如编码文本、删除列、过滤样本、划分子集和设置张量格式。本节将逐步介绍这些功能。
#### 删除列
可通过 .remove_columns() 删除不再需要的字段

```python
dataset = dataset.remove_columns(["cat"])
```
#### 过滤行
可使用 .filter() 筛选符合条件的样本

```python
dataset = dataset.filter(lambda x: x["review"] is not None and x["review"].strip() != "" and x["label"] in [0, 1])
```
#### 划分数据集
可使用 .train_test_split() 将单一数据集划分为训练集和验证集：

```python
dataset_dict = dataset.train_test_split(test_size=0.2)
train_dataset = dataset_dict["train"]
test_dataset = dataset_dict["test"]
```
#### 编码数据
可使用.map()方法与tokenizer配合，将原始文本批量编码为模型可用的输入格式（如 input_ids、attention_mask、token_type_ids等）。
.map()是 datasets 中的核心方法之一，支持对整个数据集中的每一条样本或每一批样本进行统一处理，常用于文本编码（tokenizer）和数据字段换。.map() 方法基本语法如下：

```python
dataset = dataset.map(function, batched=False, remove_columns=None)
```
参数说明如下：

|参数|说明|
|---|---|
|function|要应用到每条样本上的函数（或每批样本上的函数）|
|batched|是否以“批”为单位处理样本；若为 True，则每次接收一个样本列表|
|remove_columns|是否删除原始列，常用于清理不再需要的字段|
以中文 BERT 模型为例，编码流程如下：

```python
tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
def tokenize(example):
    encoded =  tokenizer(
        example["review"],
        padding="max_length",
        truncation=True,
        max_length=128
    )
    example['input_ids'] = encoded['input_ids']
    example['attention_mask'] = encoded['attention_mask']
    return example
train_dataset = train_dataset.map(tokenize, batched=True)
test_dataset = test_dataset.map(tokenize, batched=True)
```
编码后，数据集中将新增字段如 input_ids 和 attention_mask，可直接用于模型训练。
### 保存数据集
处理后的数据可保存到本地，供后续训练或复用，避免重复预处理。 Datasets提供了多种保存方式，适用于不同场景：

|数据格式|保存方法|适用对象|
|---|---|---|
|Arrow|save_to_disk()|Dataset 或 DatasetDict|
|CSV|to_csv()|仅限 Dataset|
|JSON|to_json()|仅限 Dataset|
#### Arrow格式
Arrow 格式是 Hugging Face 官方推荐的数据持久化方式，既支持单个 Dataset 也支持多个子集的DatasetDict。
- 保存

```python
dataset_dict.save_to_disk("./data/processed")
```
保存后的目录结构示例：

```python
processed/
├─ dataset_dict.json
├─ test/
│   ├─ data-00000-of-00001.arrow
│   ├─ dataset_info.json
│   └─ state.json
└─ train/
    ├─ data-00000-of-00001.arrow
    ├─ dataset_info.json
    └─ state.json
```
每个 split（如 train、test）都会单独保存一个 Arrow 文件和相应的元数据。
- 加载

```python
from datasets import load_from_disk
dataset_dict = load_from_disk("./data/processed")
```
#### CSV和JSON格式
如果希望将数据导出为通用格式（如用于可视化或非 Hugging Face 工具使用），可以使用 .to_csv() 或 .to_json()方法。但需注意，这些方法仅适用于单个 Dataset，不支持 DatasetDict。
- 保存

```python
# csv
train_dataset.to_csv("./data/processed/train.csv")
# json
train_dataset.to_json("./data/processed/train.json")
```
- 加载
使用 load_dataset()，指定格式和路径即可重新加载：

```python
from datasets import load_dataset
# 加载 CSV 文件
dataset_dict = load_dataset("csv", data_files="./data/processed/train.csv")
# 加载 JSON 文件
dataset_dict = load_dataset("json", data_files="./data/processed/train.json")
```
加载后返回一个结构完整的 DatasetDict，可直接用于训练、评估等任务。
### 集成Dataloader
经过预处理的datasets.Dataset对象可以直接与PyTorch的DataLoader集成使用。虽然它并非继承自torch.utils.data.Dataset类，但由于实现了__len__()和__getitem__()这两个核心接口，因此能够被DataLoader正确识别并进行批量迭代。
在使用前，需要通过.set_format()方法将指定字段转换为张量格式以适配模型输入。典型配置如下：

```python
train_dataset.set_format(
    type="torch",  # 指定输出为PyTorch张量
    columns=["input_ids", "attention_mask", "label"]  # 需要转换的字段
)
```
需要注意的是：
- 该方法仅改变通过__getitem__()（即dataset[i]）访问样本时的返回格式，不会修改底层数据存储
- 通过columns指定的字段会在访问时自动转换为torch.Tensor类型
- 未通过columns指定的字段在访问时将被自动过滤
完成格式设置后，即可创建标准的DataLoader实例：

```python
from torch.utils.data import DataLoader
# 训练集DataLoader
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
```

## 3. 官方参考（Official References）
- [Hugging Face Tokenizer API](https://huggingface.co/docs/transformers/main_classes/tokenizer)
- [Hugging Face Datasets 数据处理（Process）](https://huggingface.co/docs/datasets/process)
