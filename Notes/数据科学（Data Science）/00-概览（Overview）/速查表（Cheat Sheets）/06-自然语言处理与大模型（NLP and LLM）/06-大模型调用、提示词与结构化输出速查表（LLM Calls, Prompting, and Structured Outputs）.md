---
title: "大模型调用、提示词与结构化输出速查表（LLM Calls, Prompting, and Structured Outputs Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - llm/prompting
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "Python 3.11+；PyTorch/Hugging Face 配套稳定版"
---
# 大模型调用、提示词与结构化输出速查表（LLM Calls, Prompting, and Structured Outputs Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
文本流水线必须保存分词器、词表、特殊 token、最大长度、标签映射和评估脚本；训练与推理完全复用。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 2. OpenAI Python SDK（OpenAI Python SDK）
- **安装包（Distribution）**：`openai`。
- **导入模块（Import Module）**：`openai`；当前客户端入口为 `from openai import OpenAI, AsyncOpenAI`。
- **安装命令（Installation）**：`python -m pip install -U openai`。
- **用途（Purpose）**：调用 Responses、Chat Completions、Embeddings、Files 等 OpenAI 或兼容接口。
- **正式笔记（Detailed Note）**：[[01-大语言模型术语、生命周期与工程生态（LLM Terminology and Lifecycle）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|同步客户端|`OpenAI(api_key=..., base_url=..., timeout=..., max_retries=...)`|返回连接配置客户端|
|异步客户端|`AsyncOpenAI(...)`|返回异步客户端|
|Responses 调用|`client.responses.create(model=..., input=...)`|发起网络请求并返回 Response|
|文本结果|`response.output_text`|返回聚合文本字符串|
|流式调用|`client.responses.create(..., stream=True)`|返回事件流|
|兼容聊天接口|`client.chat.completions.create(model=..., messages=...)`|返回聊天完成对象|

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.getenv("OPENAI_BASE_URL"),
    timeout=30,
    max_retries=2,
)
# response = client.responses.create(model=os.environ["OPENAI_MODEL"], input="只回复 OK")
# 网络调用可能计费；供应商切换时同时核对 base_url、model、认证和接口兼容范围。
```
- **错误分类（Error Classes）**：分别处理连接/超时、认证、限流、无效请求和服务端错误；只对瞬时网络错误、限流或部分 5xx 做有上限且带抖动的重试。
## 3. vLLM OpenAI 兼容服务（vLLM OpenAI-compatible Serving）
- **安装包（Distribution）**：`vllm`。
- **导入模块（Import Module）**：`vllm`；常用服务入口为 `vllm serve`。
- **安装命令（Installation）**：按 vLLM 官方 GPU/平台矩阵安装 `vllm`，不能跨 CUDA/PyTorch 构建机械复制 wheel。
- **用途（Purpose）**：高吞吐本地/服务器大模型推理，并暴露 OpenAI 兼容 HTTP API。
- **正式笔记（Detailed Note）**：[[01-大语言模型术语、生命周期与工程生态（LLM Terminology and Lifecycle）]]。

```bash
vllm serve /models/local-model --host 127.0.0.1 --port 8000 --api-key "$VLLM_API_KEY"
# 启动常驻服务并占用 GPU；模型路径、显存需求和启动时间取决于部署环境。
```
- **安全边界（Security Boundary）**：不要把未鉴权的服务直接暴露到公网；限制监听地址、请求体大小、最大上下文和并发。
## 请求、消息与参数（Requests, Messages, and Parameters）
系统约束、用户数据和工具结果分角色隔离；不把不可信文本当指令。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|客户端|`OpenAI(api_key=os.environ['OPENAI_API_KEY'])`|返回客户端|
|响应|`client.responses.create(model=...,input=...)`|返回响应对象，有网络副作用|
|文本输出|`response.output_text`|返回聚合文本|
|温度|`temperature=0..2`|改变采样随机性（支持情况依模型）|
|输出上限|`max_output_tokens=n`|限制最大生成 token|
|流式|`client.responses.stream(...)`|返回事件流上下文|
|超时|`客户端或请求设置 timeout`|超时抛异常|
|重试|`仅对限流和暂时性服务错误指数退避`|返回最终响应或失败|
|请求 ID|`记录响应 request id`|返回可追踪标识，不记录输入秘密|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。
## OpenAI 兼容接口与多厂商切换（OpenAI-compatible APIs and Provider Switching）
OpenAI 兼容接口（OpenAI-compatible API）复用相似的客户端和请求结构，但兼容不代表模型名称、参数范围、流式事件、错误码或工具调用能力完全一致。切换供应商时至少把 API Key、Base URL 和 Model 同时配置化。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|读取密钥|`os.environ['LLM_API_KEY']`|返回密钥字符串；缺失时立即抛 `KeyError`|
|创建兼容客户端|`OpenAI(api_key=key, base_url=base_url, timeout=30.0, max_retries=2)`|返回客户端；尚未发起网络请求|
|选择模型|`model=os.environ['LLM_MODEL']`|把供应商模型标识与代码解耦|
|消息输入|`messages=[{'role':'system',...},{'role':'user',...}]`|形成有角色边界的请求数据|
|聊天补全|`client.chat.completions.create(model=model, messages=messages)`|返回补全对象，有网络与计费副作用|
|读取文本|`response.choices[0].message.content`|返回首个候选文本或 `None`|
|流式调用|`stream=True` 后迭代事件|逐块返回增量；事件字段由兼容程度决定|
|请求超时|`timeout=30.0`|超过期限抛超时异常，不保证服务端停止计算|
|重试|`max_retries=2`|对 SDK 认定的暂时错误重试，可能增加延迟与费用|
|请求追踪|`response._request_id` 或响应头中的 request id|返回服务端追踪标识；不同 SDK/供应商字段可能不同|

### 可切换供应商的最小模板（Minimal Provider-switching Template）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url=os.environ["LLM_BASE_URL"],
    timeout=30.0,
    max_retries=2,
)
response = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=[
        {"role": "system", "content": "只返回一句简短回答。"},
        {"role": "user", "content": "什么是向量数据库？"},
    ],
)
print(response.choices[0].message.content)
# 输出依赖远程模型；调用会产生网络请求并可能计费。
```
### 错误分类与处理（Error Taxonomy and Handling）
- **401/403 鉴权错误**：核对环境变量、权限范围、账户和 Base URL；不要把完整密钥写入日志。
- **404**：常见原因是路径、API 版本或模型名不被供应商支持，不应无条件重试。
- **429**：区分速率限制和额度不足；只对可恢复的限流执行带抖动的指数退避。
- **5xx 或连接错误**：有限次数重试并设置总时限；写操作或工具调用必须使用幂等键防止重复副作用。
- **400 参数错误**：依据供应商文档移除不支持参数或修正 schema；换模型后重新核对温度、工具、结构化输出和上下文限制。
- **流式差异**：不要假定所有兼容服务都返回相同事件对象；先对单个短请求验证结束事件、用量统计和异常传播。
## 提示词模式（Prompt Patterns）
清楚定义任务、输入边界、输出契约、评判标准和失败行为。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|任务说明|`一句话说明目标与受众`|限制模型任务|
|输入分隔|`用明确标签包住用户数据`|降低边界混淆|
|少样本|`提供少量输入输出对`|建立格式和决策示例|
|分解|`先抽取事实再生成结果`|减少一步承担过多职责|
|检索上下文|`只基于给定证据回答并标出处`|返回可溯源答案|
|拒答条件|`证据不足时返回固定状态`|避免臆测|
|自检|`要求核对输出 schema 和硬约束`|返回最终合规结果|
|提示注入防护|`把网页/文档标为不可信数据`|忽略其中操作指令|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。
## 结构化输出、工具与评测（Structured Output, Tools, and Evaluation）
结构化输出由 schema 约束；业务侧仍要解析、验证和限制副作用。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|Pydantic schema|`class Result(BaseModel): ...`|定义字段、类型与约束|
|结构化解析|`client.responses.parse(...,text_format=Result)`|返回解析对象（按 SDK 能力）|
|JSON Schema|`response_format / text.format schema`|约束 JSON 输出|
|工具定义|`name+description+JSON parameters`|返回工具调用请求|
|工具结果|`以对应 call id 回传`|继续模型执行|
|参数校验|`Model.model_validate(tool_args)`|返回验证对象或抛 ValidationError|
|幂等键|`业务操作附唯一 request id`|避免重试重复写入|
|离线样本集|`输入、参考、评分标准`|返回可重复评测数据|
|成对评估|`盲化比较候选并人工抽检`|返回偏好与错误类别|
|安全边界|`高风险工具需确认、最小权限和审计`|限制实际副作用|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
from pydantic import BaseModel,Field,ValidationError
class Answer(BaseModel):
    label:str
    confidence:float=Field(ge=0,le=1)
print(Answer.model_validate({"label":"yes","confidence":.9}).model_dump())
try: Answer.model_validate({"label":"x","confidence":2})
except ValidationError: print("invalid")
# 期望输出:
# {'label': 'yes', 'confidence': 0.9}
# invalid
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
- [[01-大语言模型术语、生命周期与工程生态（LLM Terminology and Lifecycle）]]
- [[01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）]]
- [[02-输出解析、提示词与 LCEL 链（Output Parsing, Prompts, and LCEL Chains）]]
- [[03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）]]
- [[04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）]]
- [[05-LangChain Agent 与本地工具（Agents and Local Tools）]]
- [[06-MCP 工具集成（MCP Tool Integration）]]
- [[07-Agent 记忆与中间件（Agent Memory and Middleware）]]
- [[03-OpenAI 兼容接口、鉴权与多厂商切换（OpenAI-compatible APIs, Authentication, and Provider Switching）]]
## 官方参考（Official References）
- [OpenAI API 快速开始](https://platform.openai.com/docs/quickstart)
- [vLLM 官方文档](https://docs.vllm.ai/)
- [OpenAI API 文档](https://platform.openai.com/docs/)
- [Pydantic 文档](https://docs.pydantic.dev/latest/)
