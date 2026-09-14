---
title: "LangChain、LCEL、Agent、MCP 与记忆速查表（LangChain, LCEL, Agents, MCP, and Memory Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - langchain/agents
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "Python 3.11+；LangChain/LangGraph 1.x；MCP Python SDK 1.x；各集成包需保持兼容版本"
---
# LangChain、LCEL、Agent、MCP 与记忆速查表（LangChain, LCEL, Agents, MCP, and Memory Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
文本流水线必须保存分词器、词表、特殊 token、最大长度、标签映射和评估脚本；训练与推理完全复用。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 2. 包级安装与导入索引（Package Installation and Import Index）
### 2.1 LangChain 核心与 LCEL（LangChain Core and LCEL）
- **安装包（Distribution）**：`langchain`、`langchain-core`。
- **导入模块（Import Module）**：`langchain`、`langchain_core`。
- **安装命令（Installation）**：`python -m pip install -U langchain langchain-core`。
- **用途（Purpose）**：Agent 高层入口、可运行对象（Runnable）、提示模板、消息与输出解析器。
- **正式笔记（Detailed Note）**：[[01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）]]、[[02-输出解析、提示词与 LCEL 链（Output Parsing, Prompts, and LCEL Chains）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|包装函数|`RunnableLambda(fn)`|返回可调用 Runnable|
|串联|`left \| right`|返回 `RunnableSequence`|
|调用|`chain.invoke(input)`|同步返回一次结果|
|批量|`chain.batch(inputs)`|按输入顺序返回结果列表|
|流式|`chain.stream(input)`|返回结果块迭代器|
|提示模板|`ChatPromptTemplate.from_messages([...])`|返回消息提示模板|
|文本解析|`StrOutputParser()`|返回把模型消息转为字符串的解析器|

```python
from langchain_core.runnables import RunnableLambda

strip_text = RunnableLambda(str.strip)
upper_text = RunnableLambda(str.upper)
chain = strip_text | upper_text
print(chain.invoke("  data science  "))  # 输出: DATA SCIENCE
print(chain.batch([" ai ", " nlp "]))  # 输出: ['AI', 'NLP']
```
### 2.2 LangChain OpenAI 集成（LangChain OpenAI Integration）
- **安装包（Distribution）**：`langchain-openai`。
- **导入模块（Import Module）**：`langchain_openai`。
- **安装命令（Installation）**：`python -m pip install -U langchain-openai`。
- **用途（Purpose）**：在 LangChain 中调用 OpenAI 或兼容的聊天、嵌入接口。
- **正式笔记（Detailed Note）**：[[01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|聊天模型|`ChatOpenAI(model=..., temperature=0)`|返回模型 Runnable，不立即请求|
|兼容端点|`ChatOpenAI(base_url=..., api_key=..., model=...)`|返回指向指定供应商的客户端|
|嵌入模型|`OpenAIEmbeddings(model=...)`|返回嵌入 Runnable|
|结构化输出|`model.with_structured_output(Schema)`|返回按 Schema 解析的 Runnable|

```python
import os
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
    api_key=os.environ["OPENAI_API_KEY"],
    timeout=30,
    max_retries=2,
)
# response = model.invoke("只回复 OK")
# 网络调用会产生延迟和可能的计费；输出取决于模型与服务状态。
```
### 2.3 社区集成与文本切分（Community Integrations and Text Splitters）
- **安装包（Distribution）**：`langchain-community`、`langchain-text-splitters`。
- **导入模块（Import Module）**：`langchain_community`、`langchain_text_splitters`。
- **安装命令（Installation）**：`python -m pip install -U langchain-community langchain-text-splitters`。
- **用途（Purpose）**：社区维护的数据加载器/集成，以及独立文本切分器。
- **正式笔记（Detailed Note）**：[[03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|递归切分器|`RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)`|返回切分器|
|切分文本|`splitter.split_text(text)`|返回字符串块列表|
|切分文档|`splitter.split_documents(documents)`|返回保留元数据的 Document 列表|
|加载文本|`TextLoader(path, encoding='utf-8').load()`|读取文件并返回 Document 列表|

```python
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader("notes.txt", encoding="utf-8")
print(loader.file_path)  # 输出: notes.txt
splitter = RecursiveCharacterTextSplitter(chunk_size=6, chunk_overlap=1)
chunks = splitter.split_text("abcdefghij")
print(chunks)  # 输出: ['abcdef', 'fghij']
```
### 2.4 Ollama 集成（LangChain Ollama Integration）
- **安装包（Distribution）**：`langchain-ollama`；另需本机 Ollama 服务。
- **导入模块（Import Module）**：`langchain_ollama`。
- **安装命令（Installation）**：`python -m pip install -U langchain-ollama`；服务端按 Ollama 官方方式安装并执行 `ollama serve`。
- **用途（Purpose）**：从 LangChain 调用本地 Ollama 聊天模型和嵌入模型。
- **正式笔记（Detailed Note）**：[[01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|聊天模型|`ChatOllama(model='qwen3:8b', base_url=...)`|返回模型 Runnable|
|嵌入模型|`OllamaEmbeddings(model=...)`|返回嵌入接口|
|调用|`model.invoke(messages)`|向本地服务发请求并返回 AIMessage|

```python
from langchain_ollama import ChatOllama

model = ChatOllama(model="qwen3:8b", base_url="http://localhost:11434")
# result = model.invoke("只回复 OK")
# 需要已启动的 Ollama 服务和已下载模型；输出依赖本地模型。
```
### 2.5 Tavily 搜索工具（Tavily Search Tool）
- **安装包（Distribution）**：`langchain-tavily`。
- **导入模块（Import Module）**：`langchain_tavily`。
- **安装命令（Installation）**：`python -m pip install -U langchain-tavily`。
- **用途（Purpose）**：向 Agent 暴露 Tavily Web 搜索工具。
- **正式笔记（Detailed Note）**：[[05-LangChain Agent 与本地工具（Agents and Local Tools）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建搜索工具|`TavilySearch(max_results=5)`|返回 LangChain Tool|
|执行搜索|`tool.invoke({'query': text})`|发起网络请求并返回搜索结果|

```python
import os
from langchain_tavily import TavilySearch

tool = TavilySearch(max_results=3)
# results = tool.invoke({"query": "Python dataclass official docs"})
# 需要 TAVILY_API_KEY；会访问外部网络，结果实时变化。
```
### 2.6 LangGraph 状态图与记忆（LangGraph State Graph and Memory）
- **安装包（Distribution）**：`langgraph`。
- **导入模块（Import Module）**：`langgraph`。
- **安装命令（Installation）**：`python -m pip install -U langgraph`。
- **用途（Purpose）**：以有状态图组织 Agent 节点、条件路由、检查点和持久化记忆。
- **正式笔记（Detailed Note）**：[[07-Agent 记忆与中间件（Agent Memory and Middleware）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|建立图|`StateGraph(StateSchema)`|返回可配置状态图|
|添加节点|`builder.add_node(name, fn)`|原地注册节点|
|添加边|`builder.add_edge(source, target)`|原地注册转换|
|编译|`builder.compile(checkpointer=...)`|返回可运行图|
|调用|`graph.invoke(state, config=...)`|返回最终状态|
|内存检查点|`InMemorySaver()`|返回进程内检查点器|

```python
from typing import TypedDict
from langgraph.graph import END, START, StateGraph

class State(TypedDict):
    count: int

def increment(state: State) -> State:
    return {"count": state["count"] + 1}

builder = StateGraph(State)
builder.add_node("increment", increment)
builder.add_edge(START, "increment")
builder.add_edge("increment", END)
graph = builder.compile()
print(graph.invoke({"count": 2}))  # 输出: {'count': 3}
```
- **状态边界（State Boundary）**：节点返回的是状态更新；使用持久化检查点时必须为调用提供稳定的线程或会话标识，并管理存储生命周期。
### 2.7 MCP SDK 与 LangChain MCP Adapter（MCP SDK and Adapter）
- **安装包（Distribution）**：`mcp`、`langchain-mcp-adapters`。
- **导入模块（Import Module）**：`mcp`、`langchain_mcp_adapters`。
- **安装命令（Installation）**：`python -m pip install -U mcp langchain-mcp-adapters`。
- **用途（Purpose）**：实现模型上下文协议（Model Context Protocol, MCP）服务/客户端，并把 MCP 工具转换为 LangChain Tool。
- **正式笔记（Detailed Note）**：[[06-MCP 工具集成（MCP Tool Integration）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|定义 MCP 服务|`FastMCP(name)`|返回 MCP 服务对象|
|注册工具|`@mcp.tool()`|把函数注册为可发现工具|
|运行服务|`mcp.run(transport='stdio')`|启动阻塞式服务循环|
|多服务客户端|`MultiServerMCPClient(config)`|返回多服务器客户端|
|加载工具|`await client.get_tools()`|连接服务并返回 LangChain Tool 列表|

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calculator")

@mcp.tool()
def add(left: int, right: int) -> int:
    return left + right

print(add(2, 3))  # 输出: 5
# 作为服务运行时执行 mcp.run(transport="stdio")，该调用会持续占用当前进程。
```

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient({
    "calculator": {
        "transport": "stdio",
        "command": "python",
        "args": ["calculator_server.py"],
    }
})
# tools = await client.get_tools()
# 会启动受信任的本地子进程；不得把用户输入直接拼接成 command 或 args。
```
- **安全边界（Security Boundary）**：工具应使用白名单、最小权限、参数校验和高风险操作确认；只连接可信 MCP 服务器。
### 2.8 Google Gen AI 与 LangChain Google 集成（Google Gen AI and LangChain Integration）
- **安装包（Distribution）**：`google-genai`、`langchain-google-genai`。
- **导入模块（Import Module）**：`from google import genai`、`langchain_google_genai`。
- **安装命令（Installation）**：`python -m pip install -U google-genai langchain-google-genai`。
- **用途（Purpose）**：直接调用 Gemini API，或把 Gemini 聊天/嵌入模型接入 LangChain。
- **正式笔记（Detailed Note）**：[[01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）]]、[[02-输出解析、提示词与 LCEL 链（Output Parsing, Prompts, and LCEL Chains）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|Google 客户端|`genai.Client(api_key=...)`|返回 SDK 客户端|
|直接生成|`client.models.generate_content(model=..., contents=...)`|发起网络请求并返回响应|
|LangChain 聊天模型|`ChatGoogleGenerativeAI(model=...)`|返回 Runnable 模型|
|结构化输出|`model.with_structured_output(Schema)`|返回带 schema 解析的 Runnable|

```python
import os
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI

google_client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
langchain_model = ChatGoogleGenerativeAI(model=os.environ["GEMINI_MODEL"])
# 两种客户端都会访问外部服务并可能计费；输出依赖模型，不提供固定值。
```
### 2.9 Hugging Face LangChain 集成（Hugging Face LangChain Integration）
- **安装包（Distribution）**：`langchain-huggingface`；本地嵌入通常另需 `sentence-transformers`。
- **导入模块（Import Module）**：`langchain_huggingface`、`sentence_transformers`。
- **安装命令（Installation）**：`python -m pip install -U langchain-huggingface sentence-transformers`。
- **用途（Purpose）**：把 Hugging Face 本地/端点模型与 Sentence Transformers 嵌入接入 LangChain。
- **正式笔记（Detailed Note）**：[[03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|本地嵌入模型|`SentenceTransformer(model_name_or_path)`|加载/下载模型并返回编码器|
|编码|`model.encode(texts, normalize_embeddings=True)`|返回二维 NumPy 数组|
|LangChain 嵌入|`HuggingFaceEmbeddings(model_name=..., model_kwargs=...)`|返回 LangChain Embeddings|
|文档嵌入|`embeddings.embed_documents(texts)`|返回向量列表|

```python
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings

# model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# vectors = model.encode(["data science"], normalize_embeddings=True)
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# 首次运行可能下载模型；向量值与维度取决于模型版本。
```
## Runnable 与 LCEL（Runnables and LCEL）
Runnable 统一调用、批处理、流式和组合；管道运算符连接输入输出。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|提示模板|`ChatPromptTemplate.from_messages([...])`|返回可调用模板|
|解析器|`StrOutputParser()`|返回文本解析器|
|串联|`prompt \| model \| parser`|返回 RunnableSequence|
|调用|`chain.invoke(input,config=None)`|返回单结果|
|批量|`chain.batch(inputs,config={'max_concurrency':n})`|返回结果列表|
|流式|`chain.stream(input)`|返回结果块迭代器|
|并行|`RunnableParallel(a=chain1,b=chain2)`|返回字段结果字典|
|透传|`RunnablePassthrough.assign(...)`|保留输入并添加字段|
|回退|`runnable.with_fallbacks([backup])`|返回带失败回退的 Runnable|
|重试|`runnable.with_retry(stop_after_attempt=3)`|返回有限重试 Runnable|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。
## Agent、工具与 Middleware（Agents and Tools）
Agent 让模型在循环中选择工具；大白话：模型负责决定下一步，工具负责真正执行。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|工具|`@tool def search(query:str)->str`|返回带 schema 的工具|
|创建 Agent|`create_agent(model,tools,system_prompt=...)`|返回 agent graph|
|调用|`agent.invoke({'messages':[... ]})`|返回包含消息的状态|
|流式|`agent.stream(inputs,stream_mode='values')`|返回状态事件|
|动态提示|`@dynamic_prompt`|返回运行时 system message|
|工具错误|`@wrap_tool_call`|包装调用并返回可恢复错误|
|模型调用包装|`@wrap_model_call`|动态路由、重试或限制|
|人工审批|`HumanInTheLoopMiddleware(...)`|在敏感工具前暂停|
|限调用|`ToolCallLimitMiddleware(...)`|限制循环和费用|
|待办中间件|`TodoListMiddleware()`|为复杂任务维护计划|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。
## 状态、记忆与 MCP（State, Memory, and MCP）
短期记忆属于线程状态，长期记忆写入外部存储；MCP 将工具和资源以协议暴露。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|检查点|`checkpointer=InMemorySaver()`|保存线程内状态（仅开发）|
|线程 ID|`config={'configurable':{'thread_id':'...'}}`|选择记忆会话|
|长期存储|`store.put(namespace,key,value)`|写外部记忆|
|状态 schema|`AgentState 子类 / state_schema`|定义额外状态字段|
|上下文 schema|`context_schema=Context`|定义只读运行上下文|
|MCP 客户端|`MultiServerMCPClient(config)`|连接一个或多个 MCP server|
|加载工具|`await client.get_tools()`|返回 MCP 工具列表|
|stdio 传输|`transport='stdio'`|以本地子进程通信|
|HTTP 传输|`transport='streamable_http'`|经网络端点通信|
|安全|`服务白名单、最小权限、参数验证、用户确认`|限制 MCP 工具副作用|

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
- [[01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）]]
- [[02-输出解析、提示词与 LCEL 链（Output Parsing, Prompts, and LCEL Chains）]]
- [[03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）]]
- [[04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）]]
- [[05-LangChain Agent 与本地工具（Agents and Local Tools）]]
- [[06-MCP 工具集成（MCP Tool Integration）]]
- [[07-Agent 记忆与中间件（Agent Memory and Middleware）]]
## 官方参考（Official References）
- [LangChain Agents 文档](https://docs.langchain.com/oss/python/langchain/agents)
- [LangChain Middleware 文档](https://docs.langchain.com/oss/python/langchain/middleware/built-in)
- [LangChain Provider 集成文档](https://docs.langchain.com/oss/python/integrations/providers/overview)
- [LangGraph 安装文档](https://docs.langchain.com/oss/python/langgraph/install)
- [LangChain MCP 文档](https://docs.langchain.com/oss/python/langchain/mcp)
