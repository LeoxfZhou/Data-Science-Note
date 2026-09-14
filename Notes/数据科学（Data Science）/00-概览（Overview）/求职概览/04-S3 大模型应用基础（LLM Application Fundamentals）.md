---
title: "S3 大模型应用基础（LLM Application Fundamentals）"
aliases:
  - "S3 LLM Application Fundamentals"
tags:
  - career/llm-application-engineer
  - interview/llm
status: published
created: 2026-08-27
updated: 2026-08-27
---
# S3 大模型应用基础（LLM Application Fundamentals）
> [!tip] 导航（Navigation）
> 上一阶段：[[03-S2 PyTorch、深度学习与 NLP 基础（PyTorch, Deep Learning and NLP）]]｜[[00-概览（Overview）]]｜下一阶段：[[05-S4 RAG 基础（RAG Fundamentals）]]
## 1. Token、上下文窗口与消息角色（Tokens, Context Window, and Message Roles）
### 概念与原理（Concept and Mechanism）
- Token 是模型处理文本的离散单位。上下文窗口（Context Window）限制一次请求可参与计算的输入与输出 Token 总量；最大输出长度只限制生成端，不会扩大模型上下文能力。
- System、User、Assistant 等消息角色用于表达指令层级和历史对话，但具体优先级与支持方式取决于模型和 API。应用仍必须在代码层执行权限和数据校验。

### 最小代码示例（Minimal Example）
```python
messages = [
    {"role": "system", "content": "只根据给定资料回答。"},
    {"role": "user", "content": "解释向量检索。"},
]
print([message["role"] for message in messages])  # 输出: ['system', 'user']
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：上下文窗口越大，回答一定越好吗？**

**参考答案：**不一定。更长上下文允许放入更多信息，但也增加延迟、成本和无关内容干扰，模型还可能忽视位于中间的信息。应先检索、去重和压缩，只提供完成任务所需的高质量上下文。

### 相关笔记（Related Notes）
- [[01-大语言模型术语、生命周期与工程生态（LLM Terminology and Lifecycle）]]

## 2. Temperature、Top-p、Stop 与 Seed（Sampling Controls）
### 概念与原理（Concept and Mechanism）
- Temperature 对 logits 缩放：较低值使概率分布更集中，较高值增加多样性，但不能提升事实正确性。
- Top-p 核采样（Nucleus Sampling）从累计概率达到阈值的最小候选集合中采样；Stop 在匹配指定序列时停止；Seed 只在供应商和执行路径支持时提高可重复性，不保证跨版本完全一致。

### 最小代码示例（Minimal Example）
```python
generation_config = {
    "temperature": 0.2,
    "top_p": 0.9,
    "max_output_tokens": 300,
    "stop": ["</answer>"],
}
print(generation_config["temperature"])  # 输出: 0.2
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：结构化抽取任务为什么通常使用较低 Temperature？**

**参考答案：**抽取任务强调格式稳定和结论一致，不需要大量创造性候选。较低 Temperature 可减少随机性，但仍必须使用 Schema 校验，因为低温度不能保证 JSON 合法或事实正确。

## 3. 幻觉、知识截止与上下文污染（Hallucination, Knowledge Cutoff, and Context Contamination）
### 概念与原理（Concept and Mechanism）
- 幻觉（Hallucination）是模型生成流畅但缺乏可靠依据或与事实冲突的内容；知识截止表示训练知识不覆盖较新信息；上下文污染表示错误、恶意或无关输入影响模型判断。
- 改善方法包括检索可信资料、要求引用、结构化验证、工具调用、拒答策略和人工复核，但不能承诺完全消除幻觉。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：Prompt 写得更严格能否解决幻觉？**

**参考答案：**只能降低部分风险。Prompt 是概率模型的输入，不是硬性权限或事实约束。高风险场景还需要可信数据源、工具结果校验、输出 Schema、业务规则、置信或证据检查和人工审批。

## 4. 云端模型与本地模型选型（Cloud and Local Model Selection）
### 概念与原理（Concept and Mechanism）
- 云端模型通常降低部署门槛并提供弹性能力，但存在网络、供应商、价格和数据出境约束。
- 本地模型提供更强的数据和运行控制，但需要显存、吞吐规划、模型更新、监控和安全维护。选型应同时衡量质量、延迟、吞吐、成本、隐私、可用性和团队运维能力。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：什么场景适合本地模型？**

**参考答案：**数据不能离开受控环境、调用规模稳定且硬件成本可接受、需要定制模型或离线运行时更适合本地部署；如果请求量波动大、团队缺少推理运维能力或需要最强闭源模型能力，云端 API 往往更合适。

## 5. Prompt、Few-shot 与结构化输出（Prompting, Few-shot, and Structured Output）
### 概念与原理（Concept and Mechanism）
- 稳定 Prompt 应明确任务、输入边界、约束、输出 Schema 和失败行为。Few-shot 示例通过展示输入输出对帮助模型理解标签边界和格式。
- 结构化输出必须由程序解析并通过 Schema 校验；语法正确不代表业务正确，仍要检查枚举、范围、权限和资源存在性。

### 最小代码示例（Minimal Example）
```python
from pydantic import BaseModel, Field

class SearchIntent(BaseModel):
    query: str = Field(min_length=1, max_length=200)
    top_k: int = Field(default=5, ge=1, le=20)

intent = SearchIntent.model_validate({"query": "RAG evaluation", "top_k": 3})
print(intent.top_k)  # 输出: 3
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：模型已经按要求返回 JSON，为什么还要 Pydantic？**

**参考答案：**模型可能返回缺字段、错误类型、越界值或额外字段；JSON 语法合法只证明可解析。Pydantic 把外部不可信输出转换成明确的数据契约，失败时可触发修复、重试或拒绝流程。

**问题：Prompt 为什么不能代替权限控制？**

**参考答案：**用户或检索文档可以通过提示注入改变模型行为，模型也可能忽略文字规则。权限必须由可信代码依据身份和资源归属强制执行，模型只负责提出建议或生成参数。

## 6. Provider 抽象与模型 API（Provider Abstraction and Model APIs）
### 概念与原理（Concept and Mechanism）
- Provider 抽象应统一应用真正依赖的能力，例如普通生成、流式生成、结构化输出、模型标识、Token 统计和错误分类，而不是强行假设所有供应商参数完全相同。
- 适配层负责把供应商响应转换为内部数据结构，并保留原始请求 ID、模型版本和结束原因，便于追踪。

### 最小代码示例（Minimal Example）
```python
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class ModelResult:
    text: str
    input_tokens: int
    output_tokens: int

class ModelProvider(Protocol):
    async def generate(self, messages: list[dict[str, str]]) -> ModelResult: ...
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：统一多家模型接口最容易犯什么错误？**

**参考答案：**把最低公分母当成所有模型的完整能力，或静默丢弃供应商差异。更好的设计是统一稳定核心契约，同时通过能力声明或供应商扩展字段处理工具调用、结构化输出和 Token 统计差异。

## 7. 普通响应与流式响应（Buffered and Streaming Responses）
### 概念与原理（Concept and Mechanism）
- 普通响应在模型完成后一次返回，接口简单但首字节延迟较高；流式响应逐块传输，可降低用户感知等待，但必须处理断开、取消、半成品、背压和最终统计。
- 服务端发送事件（Server-Sent Events, SSE）适合服务器单向推送文本事件；WebSocket 适合需要双向持续通信的场景。

### 最小代码示例（Minimal Example）
```python
def event_stream() -> list[str]:
    return ["data: first\n\n", "data: second\n\n", "event: done\ndata: {}\n\n"]

print(len(event_stream()))  # 输出: 3
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：客户端中断流式连接后，服务端还应继续生成吗？**

**参考答案：**通常应传播取消信号并释放上游 HTTP 连接、生成任务和并发额度，否则会浪费 Token 与算力。若业务要求后台完成，则应显式转为后台任务并提供任务 ID，不能让行为含糊。

## 8. 错误分类、有限重试与可观测性（Error Taxonomy, Bounded Retry, and Observability）
### 概念与原理（Concept and Mechanism）
- 常见错误包括鉴权、限流、连接、读取超时、无效请求、内容安全拒绝、模型不可用和无效结构化输出。
- 记录模型、供应商、请求 ID、延迟、输入/输出 Token、结束原因和错误类别；不要记录密钥或默认记录完整敏感 Prompt。

### 最小代码示例（Minimal Example）
```python
def retry_delay(attempt: int, base: float = 0.5, cap: float = 8.0) -> float:
    return min(cap, base * (2 ** attempt))

print(retry_delay(0))  # 输出: 0.5
print(retry_delay(5))  # 输出: 8.0
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：结构化输出校验失败是否应该无限让模型自我修复？**

**参考答案：**不应该。修复次数必须有限，并记录原始错误；持续失败可能是 Schema、模型能力或输入本身的问题。达到上限后应返回可诊断错误或转人工处理，避免无限成本和循环。

## 9. 统一大模型调用服务的面试表达（Unified LLM Gateway Interview Framing）
- **接口（Interface）**：同一 API 选择本地或云端 Provider，支持普通、流式和结构化回答。
- **可靠性（Reliability）**：连接/读取超时、有限重试、并发上限、取消传播和错误分类。
- **可追踪性（Traceability）**：记录 Provider、模型、请求 ID、延迟、Token、结束原因和错误类型，不静默切换模型。
- **测试（Testing）**：Mock 供应商边界，覆盖成功、超时、`429`、无效 JSON、客户端取消和模型不可用。
- **高频追问（Common Follow-up）**：为什么不自动切换模型？静默切换会改变质量、价格、隐私边界和可复现性；若业务需要降级，必须显式记录策略与实际使用模型。

## 参考资料（References）
- [[大模型应用工程师学习计划]]
- [[05-Hugging Face Transformers（Hugging Face Transformers）]]
- [[01-FastAPI 核心开发参考（FastAPI Core Development Reference）]]
