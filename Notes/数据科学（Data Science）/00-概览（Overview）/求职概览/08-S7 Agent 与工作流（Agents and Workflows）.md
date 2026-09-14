---
title: "S7 Agent 与工作流（Agents and Workflows）"
aliases:
  - "S7 Agents and Workflows"
tags:
  - career/llm-application-engineer
  - interview/agent
status: published
created: 2026-08-27
updated: 2026-08-27
---
# S7 Agent 与工作流（Agents and Workflows）
> [!tip] 导航（Navigation）
> 上一阶段：[[07-S6 RAG 优化与评测（RAG Optimization and Evaluation）]]｜[[00-概览（Overview）]]｜下一阶段：[[09-S8 部署、安全与可观测性（Deployment, Security and Observability）]]
## 1. Agent、工具调用与固定工作流（Agent, Tool Calling, and Fixed Workflows）
### 概念与原理（Concept and Mechanism）
- 智能体（Agent）让模型依据当前状态选择下一步动作；工具调用（Tool/Function Calling）让模型生成结构化工具名称与参数，可信代码验证并执行工具，再把结果返回模型。
- 固定工作流（Deterministic Workflow）由代码预先决定步骤，适合路径稳定、合规严格和失败代价高的任务。Agent 适合步骤无法完全预先列出、需要基于中间结果选择工具的任务。

> [!tip] 大白话理解（Plain-language Intuition）
> 工作流像按清单做事，Agent 像根据现场情况决定下一步。能用清单稳定解决的问题，不必增加一个会自由选择步骤的决策者。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：什么情况不应该使用 Agent？**

**参考答案：**步骤固定、输入输出明确、需要强事务保证或错误代价高时应优先普通代码或状态机。Agent 会引入非确定性、额外延迟、成本和调试复杂度。

## 2. Tool Schema 与参数验证（Tool Schema and Argument Validation）
### 概念与原理（Concept and Mechanism）
- 工具 Schema 应包含稳定名称、明确用途、参数类型、必填项、枚举和边界。模型产生的参数是不可信输入，必须再次进行 Schema、权限和业务规则校验。
- 工具描述应区分相近工具，避免模型因名称含糊选错；不能在描述中放入密钥或内部安全策略。

### 最小代码示例（Minimal Example）
```python
from pydantic import BaseModel, Field

class SearchArguments(BaseModel):
    query: str = Field(min_length=1, max_length=200)
    top_k: int = Field(default=5, ge=1, le=20)

arguments = SearchArguments.model_validate({"query": "RAG", "top_k": 3})
print(arguments.top_k)  # 输出: 3
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：模型已经支持严格结构化输出，还要做业务校验吗？**

**参考答案：**需要。结构校验只能保证字段和类型，不能保证用户有权访问目标资源、金额合理、文件存在或操作安全。权限与业务不变量必须由工具执行层强制检查。

## 3. 工具执行结果与结构化错误（Tool Results and Structured Errors）
### 概念与原理（Concept and Mechanism）
- 工具执行层应返回明确的成功数据或结构化错误，包括错误类别、可否重试和安全的用户消息。模型不能把工具失败解释成“已经执行成功”。
- 工具结果重新进入上下文时应限制长度、去除敏感字段并保留来源标识。

### 最小代码示例（Minimal Example）
```python
def tool_error(code: str, message: str, retryable: bool) -> dict[str, object]:
    return {"ok": False, "error": {"code": code, "message": message, "retryable": retryable}}

print(tool_error("NOT_FOUND", "document not found", False)["ok"])  # 输出: False
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：工具调用失败后是否应该让模型自己猜结果？**

**参考答案：**不应该。模型应收到可识别的失败结果，并选择有限重试、替代工具、请求补充信息或明确告知失败。伪造工具结果会破坏系统可审计性和用户信任。

## 4. 对话历史、状态与长期记忆（Conversation History, State, and Long-term Memory）
### 概念与原理（Concept and Mechanism）
- 对话历史（Conversation History）记录消息；短期状态（Working State）记录当前任务的中间变量、已调用工具和剩余步骤；长期记忆（Long-term Memory）保存跨会话可复用的信息。
- 长期记忆写入需要用户范围、来源、有效期、隐私和删除能力。不能把所有对话自动永久保存，也不能把模型总结当作未经验证的事实。

### 最小代码示例（Minimal Example）
```python
from dataclasses import dataclass, field

@dataclass
class AgentState:
    question: str
    step_count: int = 0
    visited_tools: list[str] = field(default_factory=list)

state = AgentState("比较两份报告")
state.visited_tools.append("document_search")
state.step_count += 1
print(state.step_count)  # 输出: 1
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：聊天记录和 Agent 状态有什么区别？**

**参考答案：**聊天记录是自然语言交互，状态是程序可验证的执行数据，例如任务 ID、步骤数、工具结果和审批状态。只靠聊天文本恢复流程容易产生歧义和重复执行。

## 5. 步骤、时间、成本与循环限制（Step, Time, Cost, and Loop Limits）
### 概念与原理（Concept and Mechanism）
- Agent 必须设置最大步骤、总超时、Token/金额预算、单工具并发和重复调用检测。每一步保存输入、工具、参数、结果、延迟和决策理由的安全摘要。
- 检测到相同工具与参数重复调用，或状态没有推进时，应终止、改变策略或请求人工帮助。

### 最小代码示例（Minimal Example）
```python
def should_stop(step_count: int, total_cost: float, max_steps: int = 8, max_cost: float = 0.50) -> bool:
    return step_count >= max_steps or total_cost >= max_cost

print(should_stop(step_count=8, total_cost=0.10))  # 输出: True
print(should_stop(step_count=2, total_cost=0.10))  # 输出: False
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：如何防止 Agent 无限循环？**

**参考答案：**使用硬性步骤、时间和成本上限；记录工具调用指纹检测重复；要求状态每步产生可验证进展；连续失败后停止并请求人工确认。只在 Prompt 中写“不要循环”不构成可靠控制。

## 6. 高风险工具与人工确认（High-risk Tools and Human Approval）
### 概念与原理（Concept and Mechanism）
- 发送消息、删除文件、付款、写数据库、执行代码和修改权限属于有副作用或高风险操作，应使用最小权限、白名单、参数预览和人工确认。
- 确认必须绑定具体工具、参数和过期时间；用户批准“查看订单”不能被复用为“取消订单”。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：Human-in-the-loop 应放在模型调用前还是工具执行前？**

**参考答案：**通常放在产生具体候选动作之后、真正副作用执行之前，让用户看到实际工具与参数。还应在执行层再次检查确认令牌与参数一致，防止确认后动作被替换。

## 7. 低代码平台与代码实现（Low-code Platforms and Code Implementations）
### 概念与原理（Concept and Mechanism）
- Dify、Coze 等平台可快速提供模型连接、知识库、工作流、UI 和观测能力，适合原型、演示和标准流程。
- 代码实现通常具有更强的数据契约、版本控制、测试、部署和底层调试能力。平台版本应作为对照，不替代对检索、权限和工具执行链路的理解。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：低代码平台版和代码版如何比较？**

**参考答案：**从开发速度、可定制性、测试、调试、数据控制、部署边界、供应商锁定和成本比较。平台版适合快速验证，代码版适合复杂业务约束和长期维护；选择取决于需求而非工具偏好。

## 8. 文档研究助手的控制流（Document Research Assistant Control Flow）
### 最小工作流（Minimal Workflow）
1. 分类问题并确定需要知识库、只读数据库或公开信息工具。
2. 生成并验证工具参数，同时检查用户权限和只读白名单。
3. 执行工具并保存结构化结果；失败时不伪造数据。
4. 判断证据是否足够，必要时在预算内继续检索。
5. 生成带来源报告；证据不足或高风险时请求人工确认。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么数据库工具只允许只读白名单查询？**

**参考答案：**模型生成的查询可能越权、昂贵或具有副作用。最安全的方式是暴露受控业务查询或只读视图，限制表、字段、行数和超时，而不是让模型执行任意 SQL。

**问题：执行轨迹应记录什么？**

**参考答案：**记录请求 ID、步骤、模型、工具名、脱敏参数、结果摘要、错误、延迟、Token/成本和审批信息；避免保存密钥与不必要的完整敏感数据。

## 参考资料（References）
- [[大模型应用工程师学习计划]]
- [[05-S4 RAG 基础（RAG Fundamentals）]]
- [[06-S5 AI 后端工程化（AI Backend Engineering）]]
