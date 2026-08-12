---
title: "HanLP 本地推理与 RESTful 调用（HanLP Native and RESTful Usage）"
tags:
  - data-science/nlp/hanlp
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# HanLP 本地推理与 RESTful 调用（HanLP Native and RESTful Usage）
## HanLP 的使用与调用方式（本地 vs. 远程）

`HanLP` 是一款面向生产环境的多语种自然语言处理工具包。在实际工程落地中，它支持远程云端调用（轻量快捷）**与**本地模型部署（自主可控）两种核心访问方式。

### 1. 访问方式对比与选型指南

|**维度**|**方式 1：远程 API 调用 (Remote/RESTful)**|**方式 2：本地加载模型预测 (Local)**|
|---|---|---|
|**依赖环境**|仅需安装轻量 SDK 或使用标准 `requests` 库|需要安装完整 `hanlp` 库及 PyTorch/TensorFlow 等深度学习框架|
|**计算资源**|几乎不占用本地 CPU/GPU，算力由云端服务器提供|极度依赖本地算力，推荐使用 GPU（如 CUDA）进行加速|
|**网络要求**|必须联网，且受限于网络带宽和延迟|支持完全离线运行，无网络延迟|
|**适用场景**|快速原型开发、轻量级脚本、算力受限的客户端设备|核心业务生产环境、高并发高吞吐场景、敏感数据脱敏|

### 2. 远程调用方式（RESTful API）

远程调用主要通过 HanLP 提供的 Web 后端接口实现，官方封装了 SDK，同时也支持使用标准的 HTTP `POST` 请求。

#### 2.1 方式一：使用官方客户端 SDK (`hanlp_restful`)

官方对 API 进行了高层封装，使用体验类似本地调用，支持复杂的语义依存分析和语义相似度计算。

```Python
from hanlp_restful import HanLPClient

# 初始化客户端
# auth: 申请的 API 秘钥（不填则为匿名受限访问）
# language: 'zh' 表示中文，'mul' 表示多语种
HanLP = HanLPClient('https://www.hanlp.com/api', auth=None, language='zh')

# 1. 综合分析 (Parse)：包含分词、词性标注、命名实体识别、依存句法分析等
r = HanLP.parse("2021年HanLPv2.1为生产环境带来次世代最先进的多语种NLP技术。阿婆主来到北京立方庭参观自然语义科技公司。")
print("分析结果:\n", r)

# 2. 语义文本相似度 (STS)
r_sts = HanLP.semantic_textual_similarity([
    ('看图猜一电影名', '看图猜电影'),
    ('无线路由器怎么无线上网', '无线上网卡和无线路由器怎么用'),
    ('北京到上海的动车票', '上海到北京的动车票'),
])
print("语义相似度分数列表:", r_sts) # 输出每对句子的相似度得分（0 ~ 1 之间）
```

#### 2.2 方式二：使用原生 `requests` 库（裸写 HTTP 请求）

如果不想在生产环境引入多余的第三方 SDK，可以直接通过 HTTP `POST` 访问 RESTful API。

```Python
import json
import requests

url = "https://www.hanlp.com/api/parse"

# 构造请求体 (Form Payload)
form = {
    'text': '2021年HanLPv2.1为生产环境带来次世代最先进的多语种NLP技术。',
    'tokens': None,
    'tasks': 'tok',         # 指定要执行的任务，'tok' 代表分词 (Tokenization)
    'skip_tasks': None,
    'language': 'zh'
}

# 发送 POST 请求
response = requests.post(url, json=form, headers={})

# 解析响应结果
result = json.loads(response.text) # 将返回的 JSON 字符串转换为 Python 字典
print("分词响应结果:", result)
```

### 3. 本地加载模型预测（Local Inference）

本地模式需要下载预训练好的深度学习模型（通常基于 Transformer 架构，如 ELECTRA、BERT），并在本地算力上完成推理。

#### 3.1 工业落地的工程经验

> ⚠️ **预训练模型（Pre-trained Models）的局限性**：
>
> 预训练模型只能在它**训练语料所覆盖的范围内**发挥出色的推理能力。如果业务场景中包含大量垂直领域的专业术语、行业暗语，默认模型的表现会大幅下滑。
>
> 💡 **工程落地策略**：
>
> 在实际工作中，我们**极少从零（From Scratch）开始训练**一个复杂的深度学习模型（代价昂贵）。通常的做法是：下载官方已训练好的通用领域模型参数，在此基础上使用我们自己的业务标注数据进行**微调训练（Fine-Tuning）**。

#### 3.2 本地调用实战（分词 + 命名实体识别 NER）

```Python
import hanlp

# ==================== Step 1: 载入本地分词模型 ====================
# 这里加载的是基于 ELECTRA 架构的高精度中文分词预训练模型
tok_hanlp = hanlp.load(hanlp.pretrained.tok.FINE_ELECTRA_SMALL_ZH)

# 对一批句子进行分词推理（传入 List[str]，返回 List[List[str]]）
sentences = [
    '2021年HanLPv2.1为生产环境带来次世代最先进的多语种NLP技术。',
    '阿婆主来到北京立方庭参观自然语义科技公司。'
]
tokens_list = tok_hanlp(sentences)
print("本地分词结果:\n", tokens_list)

# 打印模型底层网络结构，可以看到它是一个 Transformer/ELECTRA 模型
print("模型底层结构:", tok_hanlp.model)


# ==================== Step 2: 载入本地命名实体识别 (NER) 模型 ====================
# 加载基于 MSRA（微软亚洲研究院）数据集训练的命名实体识别模型
ner_hanlp = hanlp.load(hanlp.pretrained.ner.MSRA_NER_ELECTRA_SMALL_ZH)

# NER 模型通常需要“分词后的序列”作为输入
ner_results = ner_hanlp(tokens_list)
print("本地实体识别结果:\n", ner_results)
# 输出格式说明: [ [(实体, 实体类别, 起始Token索引, 结束Token索引), ...], ... ]
# 例如: ('北京立方庭', 'LOCATION', 4, 7) 代表在第 4 到 7 个 token 是地名
```
