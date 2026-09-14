---
title: "RAG、嵌入、检索与 Milvus 速查表（RAG, Embeddings, Retrieval, and Milvus Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - rag/retrieval
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "Python 3.11+；PyTorch/Hugging Face 配套稳定版"
---
# RAG、嵌入、检索与 Milvus 速查表（RAG, Embeddings, Retrieval, and Milvus Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
文本流水线必须保存分词器、词表、特殊 token、最大长度、标签映射和评估脚本；训练与推理完全复用。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 2. 包级安装与导入索引（Package Installation and Import Index）
### 2.1 LlamaIndex（LlamaIndex）
- **安装包（Distribution）**：整合包 `llama-index`；按连接器最小安装时使用对应的 `llama-index-core`、`llama-index-readers-*`、`llama-index-llms-*`、`llama-index-embeddings-*`。
- **导入模块（Import Module）**：统一从 `llama_index` 命名空间导入，例如 `llama_index.core`。
- **安装命令（Installation）**：`python -m pip install -U llama-index`；生产环境按实际组件改用最小拆分包并固定版本。
- **用途（Purpose）**：文档读取、节点切分、索引、检索、查询和存储持久化。
- **正式笔记（Detailed Note）**：[[03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|文档对象|`Document(text=..., metadata=...)`|返回文档|
|目录读取|`SimpleDirectoryReader(path).load_data()`|读取文件并返回文档列表|
|构建索引|`VectorStoreIndex.from_documents(documents)`|嵌入并返回索引；可能联网与持久化|
|检索器|`index.as_retriever(similarity_top_k=k)`|返回检索器|
|查询引擎|`index.as_query_engine(...)`|返回检索生成接口|
|持久化|`index.storage_context.persist(persist_dir=path)`|写入索引状态|
|重新加载|`load_index_from_storage(StorageContext.from_defaults(persist_dir=path))`|读取并恢复索引|

```python
from llama_index.core import Document

document = Document(text="RAG combines retrieval and generation.", metadata={"source": "demo"})
print(document.metadata["source"], len(document.text))  # 输出: demo 38
```
- **边界（Boundary）**：构建向量索引通常需要嵌入模型，默认配置可能联网；生产环境必须显式固定嵌入模型、向量维度、持久化目录和索引版本。
### 2.2 FlagEmbedding（FlagEmbedding）
- **安装包（Distribution）**：`FlagEmbedding`。
- **导入模块（Import Module）**：`FlagEmbedding`。
- **安装命令（Installation）**：`python -m pip install -U FlagEmbedding`。
- **用途（Purpose）**：BGE 系列稠密嵌入、重排序和检索模型。
- **正式笔记（Detailed Note）**：[[03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|加载嵌入模型|`FlagModel(model_name_or_path, use_fp16=True)`|加载权重并返回编码器|
|编码查询|`model.encode_queries(texts)`|返回二维向量数组|
|编码语料|`model.encode_corpus(texts)`|返回二维向量数组|
|加载重排器|`FlagReranker(model_name_or_path, use_fp16=True)`|加载交叉编码重排器|
|计算分数|`reranker.compute_score(pairs)`|返回相关性分数|

```python
from FlagEmbedding import FlagModel

# model = FlagModel("BAAI/bge-small-zh-v1.5", use_fp16=False)
# vectors = model.encode_queries(["什么是向量检索？"])
# 首次执行可能下载模型并占用大量内存；向量值依赖模型版本，不提供固定输出。
```
### 2.3 PyMilvus（Milvus Python SDK）
- **安装包（Distribution）**：`pymilvus`。
- **导入模块（Import Module）**：`pymilvus`。
- **安装命令（Installation）**：`python -m pip install -U pymilvus`。
- **用途（Purpose）**：连接 Milvus、管理集合、写入向量并执行近似最近邻检索。
- **正式笔记（Detailed Note）**：[[04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建客户端|`MilvusClient(uri=..., token=...)`|返回客户端；连接可能延迟到首次操作|
|创建集合|`client.create_collection(collection_name=..., dimension=...)`|创建持久化集合|
|插入|`client.insert(collection_name=..., data=rows)`|写数据并返回主键/计数信息|
|检索|`client.search(collection_name=..., data=vectors, limit=k, output_fields=[...])`|返回分批命中列表|
|标量查询|`client.query(collection_name=..., filter=..., output_fields=[...])`|返回实体字典列表|
|删除|`client.delete(collection_name=..., ids=...)`|持久化删除并返回结果|

```python
from pymilvus import DataType

print(DataType.FLOAT_VECTOR.name)  # 输出: FLOAT_VECTOR
# MilvusClient 的建表、插入、检索和删除依赖外部服务；真实 URI 与令牌必须来自环境变量。
```
- **形状边界（Shape Boundary）**：写入向量维度必须和集合 schema 完全一致；索引度量（如 COSINE/IP/L2）必须与嵌入归一化策略一致。
### 2.4 Unstructured 与 Python-Markdown（Document Parsing Packages）
- **安装包（Distribution）**：`unstructured`（按格式选择 `unstructured[md]`、`unstructured[docx]` 等 extra）、`Markdown`。
- **导入模块（Import Module）**：`unstructured`、`markdown`。
- **安装命令（Installation）**：`python -m pip install -U 'unstructured[md,docx]' Markdown`；部分格式还需系统级解析器。
- **用途（Purpose）**：Unstructured 把多种文档拆为语义元素；Python-Markdown 把 Markdown 转为 HTML，供加载器或预处理流程使用。
- **正式笔记（Detailed Note）**：[[03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）]]。

```python
import markdown
from unstructured.partition.text import partition_text

html = markdown.markdown("# Title")
elements = partition_text(text="Title\n\nBody")
print(html, len(elements))  # 输出: <h1>Title</h1> 2
```
- **边界（Boundary）**：PDF、Office、OCR 等格式可能需要额外系统依赖且解析结果受版式影响；必须抽样核对标题、表格、页码和阅读顺序。
## 文档解析、切块与嵌入（Ingestion, Chunking, and Embeddings）
切块应保持语义单元和来源元数据；大白话：把长文切成能独立回答问题的小段，再转成可比较的向量。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|加载文档|`loader.load()`|返回 Document 列表|
|递归切块|`RecursiveCharacterTextSplitter(chunk_size,chunk_overlap)`|返回文档块|
|Token 切块|`按 tokenizer 长度切分`|返回不超过上下文预算的块|
|元数据|`{'source':path,'section':title,'version':...}`|随块保存来源|
|嵌入|`embedding_model.embed_documents(texts)`|返回向量列表|
|查询嵌入|`embedding_model.embed_query(query)`|返回单向量|
|归一化|`vector/np.linalg.norm(vector)`|返回单位向量|
|批处理|`按 API 上限与 token 数分批`|返回全部嵌入|
|指纹|`sha256(normalized_content)`|返回去重与增量索引键|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。
## 检索、重排与上下文（Retrieval and Reranking）
召回先广泛找候选，重排再精确排序；生成只接收预算内证据。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|稠密检索|`vector_store.similarity_search(query,k=10)`|返回相似文档|
|带分数|`similarity_search_with_score(query,k)`|返回文档分数对|
|元数据过滤|`filter={'tenant_id':...}`|限制搜索范围|
|MMR|`max_marginal_relevance_search(query,k,fetch_k)`|返回兼顾相关性与多样性的文档|
|混合检索|`融合 BM25 与向量排名`|返回合并候选|
|交叉编码重排|`reranker.score(query,documents)`|返回更精细相关分|
|阈值拒答|`top_score<threshold`|返回证据不足状态|
|上下文预算|`按重排分数累积至 token 上限`|返回最终证据块|
|引用|`为每块分配稳定 source id`|返回可追踪答案|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。
## Milvus 索引与评估（Milvus and Evaluation）
向量维度、距离类型和索引参数必须与嵌入模型一致。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|连接|`MilvusClient(uri=...,token=...)`|返回客户端|
|创建集合|`client.create_collection(name,dimension,metric_type='COSINE')`|创建集合|
|插入|`client.insert(collection_name,data)`|写向量并返回结果|
|搜索|`client.search(collection_name,data=[query],limit=k,filter=...)`|返回命中列表|
|标量查询|`client.query(collection_name,filter,output_fields=...)`|返回实体列表|
|删除|`client.delete(collection_name,ids=...)`|删除实体，有外部副作用|
|索引|`client.create_index(collection_name,index_params)`|创建 ANN 索引|
|加载集合|`client.load_collection(name)`|载入查询资源|
|Recall@k|`相关文档是否在前 k`|返回召回比例|
|MRR/nDCG|`按首个相关项或分级相关性评分`|返回排名质量|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。
## Dify、Coze 与 Ollama（Application Platforms and Local Models）
Dify 和 Coze 用于编排模型、知识库、工具与工作流；Ollama 负责在本机启动和提供模型推理接口。平台不是模型本身，模型服务也不会自动完成 RAG 的切块、索引和引用管理。

|功能（Operation）|实际写法（Usage）|返回值与状态变化|
|---|---|---|
|本地模型列表|`ollama list`|输出本机已安装模型|
|启动模型服务|`ollama serve`|启动本地 HTTP 服务并持续占用进程|
|拉取模型|`ollama pull <model>`|下载模型文件，有网络与磁盘副作用|
|Dify 知识库|`上传文档 → 切块 → 嵌入 → 建索引`|创建可检索的数据集与索引|
|Dify 工作流|`开始节点 → 检索 → LLM → 结束节点`|按节点传递变量并返回结果|
|Coze 工作流|`模型、插件、知识库与节点编排`|形成托管应用工作流|
|容器访问宿主机|`http://host.docker.internal:<port>`|让 Docker Desktop 容器访问宿主机服务|
|容器访问 Compose 服务|`http://<service-name>:<port>`|通过 Compose 网络的服务名解析目标容器|

### 地址选择（Address Selection）
- **浏览器访问宿主机服务**：通常使用 `localhost:<host_port>`。
- **容器访问宿主机 Ollama**：Docker Desktop 通常使用 `host.docker.internal:11434`；Linux 原生 Docker 可能需要显式添加 host gateway。
- **容器互访**：使用 Compose 服务名和容器端口，不使用宿主机映射端口。
- **排错顺序**：先确认 Ollama 进程和模型，再从宿主机测试 HTTP，然后进入 Dify 容器测试相同地址，最后检查平台中的模型名称、凭据与超时。
### Ollama HTTP 最小调用（Minimal Ollama HTTP Call）
```bash
curl http://127.0.0.1:11434/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen3:8b","prompt":"只回复 OK","stream":false}'
# 需要 ollama serve 与已下载模型；响应文本、耗时和资源占用依赖本地模型。
```
### Dify API 最小调用（Minimal Dify API Call）
```bash
curl -X POST "$DIFY_BASE_URL/v1/chat-messages" \
  -H "Authorization: Bearer $DIFY_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"inputs":{},"query":"只回复 OK","response_mode":"blocking","user":"local-user"}'
# 会调用外部或本地 Dify 应用；API Key 必须来自环境变量，输出取决于应用工作流。
```
### Coze API 最小调用（Minimal Coze API Call）
```bash
curl -X POST "$COZE_BASE_URL/v3/chat" \
  -H "Authorization: Bearer $COZE_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"bot_id\":\"$COZE_BOT_ID\",\"user_id\":\"local-user\",\"stream\":false,\"additional_messages\":[{\"role\":\"user\",\"content\":\"只回复 OK\",\"content_type\":\"text\"}]}"
# 会访问 Coze 服务；端点与字段必须按所用地区和当前官方 API 版本复核。
```
## LlamaIndex 本地 RAG（LlamaIndex Local RAG）
LlamaIndex 把数据连接器、节点切分、索引、检索器和查询引擎串起来。生成模型（LLM）负责组织答案，嵌入模型（Embedding Model）负责把文本转换为向量，二者不能互换。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|读取目录|`SimpleDirectoryReader('data').load_data()`|返回 `Document` 列表；读取本地文件|
|构建向量索引|`VectorStoreIndex.from_documents(documents)`|切分、嵌入并返回索引，可能调用模型服务|
|创建检索器|`index.as_retriever(similarity_top_k=4)`|返回只召回节点的检索器|
|执行检索|`retriever.retrieve(query)`|返回带分数的 `NodeWithScore` 列表|
|创建查询引擎|`index.as_query_engine(similarity_top_k=4)`|返回“检索 + 生成”的查询入口|
|执行问答|`query_engine.query(question)`|返回响应对象，可能产生网络或本地推理副作用|
|持久化索引|`index.storage_context.persist(persist_dir='storage')`|写入索引、文档与元数据文件|
|加载存储|`StorageContext.from_defaults(persist_dir='storage')`|读取持久化状态并返回存储上下文|
|恢复索引|`load_index_from_storage(storage_context)`|返回已恢复索引，避免重新嵌入|

### 最小本地索引模板（Minimal Local Index Template）
```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
retriever = index.as_retriever(similarity_top_k=2)
nodes = retriever.retrieve("项目使用什么数据库？")
print(len(nodes) <= 2)  # True
# 构建和检索可能调用嵌入服务；召回内容取决于本地文档。
```
### 持久化与故障排查（Persistence and Troubleshooting）
- **模型未配置**：显式设置 LLM 和 Embedding Model；只想检索时仍然需要嵌入模型，但可以不调用生成模型。
- **索引重复构建**：启动时优先检测持久化目录并恢复；文档变化时按内容指纹增量更新或明确重建。
- **恢复后结果不同**：核对嵌入模型名称、向量维度、切块参数、元数据 schema 和库版本。
- **召回为空**：检查输入文件是否被加载、切块是否为空、查询与文档语言是否匹配以及 `similarity_top_k` 和过滤条件。
- **容器连接失败**：从发起请求的运行环境判断 `localhost` 指向谁，再选择服务名、`host.docker.internal` 或真实网络地址。
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
- [[03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）]]
- [[04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）]]
- [[01-Dify、Coze 与 Ollama 应用平台（Dify, Coze, and Ollama Application Platforms）]]
- [[02-LlamaIndex 本地 RAG、检索与索引持久化（LlamaIndex Local RAG, Retrieval, and Index Persistence）]]
## 官方参考（Official References）
- [LlamaIndex 文档](https://docs.llamaindex.ai/)
- [Milvus PyMilvus 安装文档](https://milvus.io/docs/install-pymilvus.md)
- [Milvus 向量检索文档](https://milvus.io/docs/single-vector-search.md)
- [FlagEmbedding 官方仓库](https://github.com/FlagOpen/FlagEmbedding)
- [Milvus 文档](https://milvus.io/docs)
- [LangChain Retrieval](https://docs.langchain.com/oss/python/langchain/retrieval)
