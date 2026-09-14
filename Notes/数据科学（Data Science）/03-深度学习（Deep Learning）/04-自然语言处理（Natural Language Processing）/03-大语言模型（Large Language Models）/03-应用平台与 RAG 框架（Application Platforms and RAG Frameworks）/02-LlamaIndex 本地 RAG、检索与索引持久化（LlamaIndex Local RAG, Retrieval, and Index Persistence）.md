---
title: LlamaIndex 本地 RAG、检索与索引持久化（LlamaIndex Local RAG, Retrieval, and Index Persistence）
tags:
  - data-science/nlp/llamaindex
  - data-science/rag
status: published
created: 2026-09-10
published_at: 2026-09-10
verified_at: 2026-09-10
---
# LlamaIndex 本地 RAG、检索与索引持久化（LlamaIndex Local RAG, Retrieval, and Index Persistence）
## 1. 定位与核心流程
LlamaIndex 是面向大模型数据接入、索引、检索与查询编排的框架。它与 LangChain 有重叠，但常把重点放在数据到检索链路：
```text
数据源 → Document → Node/Chunk → Embedding → VectorStoreIndex
                                              ├── Retriever
                                              └── Query Engine → LLM → Response
```
- `Document`：一份逻辑文档及其元数据。
- `Node`：从文档切出的可检索单元，通常继承来源元数据。
- 嵌入（Embedding）：把文本映射为数值向量，支持相似度搜索。
- `VectorStoreIndex`：组织向量和节点，使查询可检索相关内容。
- 检索器（Retriever）：只返回相关节点，不生成自然语言答案。
- 查询引擎（Query Engine）：完成检索、上下文拼接和答案合成。
> [!tip] 大白话理解（Plain-language Intuition）
> LlamaIndex 像资料管理员：先把文件拆成带标签的小卡片，再把每张卡片变成可以按语义查找的坐标。Retriever 只把相关卡片拿出来，Query Engine 再把卡片交给模型组织成答案。
## 2. 安装与模块拆分
现代 LlamaIndex 将核心包与提供者集成分开安装，具体包名应按当前官方文档核对。
```bash
python -m pip install llama-index-core
python -m pip install llama-index-llms-ollama
python -m pip install llama-index-embeddings-ollama
```
安装会改变 Python 环境且可能访问网络，不提供固定输出。运行前应确认当前解释器：
```python
import sys

print(sys.executable)  # 输出当前 Python 解释器的实际路径
```
## 3. 生成模型与嵌入模型必须分工
- 大语言模型（Large Language Model, LLM）负责基于问题和上下文生成答案。
- 嵌入模型（Embedding Model）负责为文档块和查询生成同一向量空间中的表示。
- 构建索引和重新嵌入需要嵌入模型；仅加载已持久化索引通常不应重新处理全部文档。
- 更换嵌入模型、向量维度、切块策略或关键清洗逻辑后，旧索引通常不再兼容，应重新构建并记录版本。
## 4. 最小本地 RAG 示例
```python
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

Settings.llm = Ollama(
    model="<generation-model>",
    base_url="http://localhost:11434",
    request_timeout=120.0,
)
Settings.embed_model = OllamaEmbedding(
    model_name="<embedding-model>",
    base_url="http://localhost:11434",
)

documents = SimpleDirectoryReader(
    input_dir="data",
    recursive=True,
).load_data()

index = VectorStoreIndex.from_documents(documents)
index.storage_context.persist(persist_dir="storage")

query_engine = index.as_query_engine(similarity_top_k=3)
response = query_engine.query("文档的核心结论是什么？")
print(str(response))

# 输出模式:
# <模型根据检索到的文档块生成的答案，实际文本取决于数据与模型>
```
该示例会读取文件、调用本地模型并写入索引目录，属于外部副作用；输出只能描述模式，不能伪造固定答案。
### 4.1 关键参数

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|加载目录|`SimpleDirectoryReader(input_dir="data").load_data()`|返回 `Document` 列表；读取文件系统|
|递归读取|`recursive=True`|包含子目录；读取范围扩大|
|构建索引|`VectorStoreIndex.from_documents(documents)`|切块、嵌入并创建索引；可能调用嵌入服务|
|保存索引|`index.storage_context.persist(persist_dir="storage")`|把文档存储、索引存储和默认向量存储写入磁盘|
|生成检索器|`index.as_retriever(similarity_top_k=3)`|返回 Retriever，不调用生成模型|
|生成查询引擎|`index.as_query_engine(similarity_top_k=3)`|返回 Query Engine；查询时检索并调用 LLM|

`similarity_top_k` 表示最多选择多少个高相关候选节点，不保证每个节点都正确，也不等于最终上下文一定只含这些节点。
## 5. 只检索、不生成答案
排查 RAG 时应先检查召回，再判断 LLM 是否回答正确。
```python
retriever = index.as_retriever(similarity_top_k=3)
nodes = retriever.retrieve("会员编号的格式是什么？")

for item in nodes:
    print(round(item.score or 0.0, 4), item.node.metadata)
    print(item.node.get_content()[:120])

# 输出模式:
# 0.8123 {'file_name': 'rules.md', ...}
# <被召回节点的前 120 个字符>
```
检查重点：来源文件、文本是否完整、查询关键词、得分排序、切块是否把答案与条件拆开。
## 6. 索引持久化与恢复
```python
from llama_index.core import StorageContext, load_index_from_storage

storage_context = StorageContext.from_defaults(persist_dir="storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine(similarity_top_k=3)
```
恢复过程读取已有索引，不应再次调用 `SimpleDirectoryReader` 和 `from_documents()`。如果同一目录保存多个索引，应设置并保存稳定的 `index_id`，加载时明确指定。
### 6.1 常见误区
- 持久化索引不是备份原始资料；原文、解析器版本和构建配置仍应独立保存。
- 默认本地存储适合学习和小规模应用；多进程、并发写入、权限控制与生产检索通常应选专用存储。
- 工作目录改变会影响相对路径。生产代码应从明确的项目根目录解析 `data` 和 `storage`。
- 先删除旧索引再构建有数据丢失风险；应构建到新目录、验证后再切换。
## 7. 宿主机与容器地址
- Python 脚本和 Ollama 都在宿主机：通常使用 `http://localhost:11434`。
- Python 脚本在 Docker Desktop 容器、Ollama 在宿主机：通常使用 `http://host.docker.internal:11434`。
- 两个服务都在同一 Compose 网络：使用 Ollama 服务名和容器端口。
- 远程服务器或原生 Linux：根据实际监听地址、路由、防火墙和认证配置处理。
“能在浏览器访问”不保证 Python 进程或容器走相同网络路径，应从实际运行位置测试。
## 8. 质量与排错清单
1. 导入失败：确认解释器与安装包属于同一个环境。
2. 连接失败：先直接请求模型服务，再排查 LlamaIndex 封装。
3. 检索为空：检查文档是否加载、节点数量、嵌入是否成功和过滤条件。
4. 召回错误：调整切块、重叠、元数据、查询改写、嵌入模型或混合检索。
5. 召回正确但答案错误：检查提示词、上下文窗口、回答约束和模型能力。
6. 加载索引失败：核对 LlamaIndex 版本、存储目录完整性、索引 ID 和嵌入配置。
7. 回答必须附带来源时，保留 `source_nodes` 或等价引用信息，不只保存最终字符串。
## 9. 与 LangChain 的关系
- LlamaIndex 常聚焦文档、节点、索引与检索；LangChain 常聚焦模型调用、工具、Agent、状态与工作流。
- 两者都能构建 RAG，也可以组合使用；选型应根据团队已有抽象和可观察性需求，不按“谁更高级”判断。
- 简单应用优先使用更少的抽象；需要定制数据摄取和检索时，再引入细粒度组件。
## 10. 参考资料
- [LlamaIndex 数据加载](https://developers.llamaindex.ai/python/framework/module_guides/loading/)
- [LlamaIndex 索引持久化与加载](https://developers.llamaindex.ai/python/framework/module_guides/storing/save_load/)
- [LlamaIndex Ollama 集成](https://developers.llamaindex.ai/python/framework/integrations/llm/ollama/)
- [[03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）]]
- [[04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）]]

