---
title: "Agent 记忆与中间件（Agent Memory and Middleware）"
tags:
  - data-science/deep-learning/nlp/llm/LangChain
status: published
created: 2026-09-07
published_at: 2026-09-07
source_document_version: V1.0.2
target_framework_line: LangChain 1.1.x
---
# Agent 记忆与中间件（Agent Memory and Middleware）
## Agent 短期记忆（Short-term Memory）
前面的agent在多次invoke过程中，并不会将会话历史保存下来，也就是没有短期记忆。要想Agent拥有短期记忆，就需要在create_agent当中为checkpointer参数赋值，该参数其实是底层LangGraph用以保存多次调用记录的检查点配置。
Agent拥有短期记忆能力之后，会将会话历史按照thread_id作为粒度进行隔离的。Thread_id是来自于agent的底层运行时—LangGraph—当中的概念。不同的thread_id，对应着不同的消息列表，如下图所示：
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/07-Agent 记忆与中间件（Agent Memory and Middleware）/07-Agent 记忆与中间件（Agent Memory and Middleware）-20260907112000032.png]]
在具体调用时，只需要指定一个thread_id，即可保证将所有短期记忆，存储到一个特定的消息列表当中；LLM在回复时，只会以当前thread_id所对应的消息列表作为上下文进行回复。
> [!tip] 大白话解释（Intuition）
> `thread_id` 像聊天窗口编号：同一个编号继续写入同一本会话记录，不同编号彼此隔离。`checkpointer` 是保存记录的组件；`InMemorySaver` 只适合开发和演示，进程退出后数据会丢失，生产环境应换成数据库支持的持久化 Checkpointer。
下面构造一个实际的WeatherAgent， 来演示记忆功能：
```python
import os
import datetime
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

# 定义 Tavily 搜索工具
search = TavilySearch(max_results=5)
tools = [search]

llm = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai",
)

# 关键点1：定义checkpointer实例
checkpointer = InMemorySaver()

# 创建 Agent
agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=checkpointer, # 关键点2：将checkpointer实例传递给Agent
)

# 调用
print("=== 第一次调用 ===")
for chunk in agent.stream(
    input={
        "messages": [
            {
                "role": "system",
                "content": f"当前时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            },
            {"role": "user", "content": "今天北京天气怎么样？"},
        ]
    },
    config={"configurable": {"thread_id": "abc123"}}, # 关键点3：为每个调用指定一个唯一的thread_id
):
    print(chunk, end="\n\n")

print("=== 第二次调用 ===")
for chunk in agent.stream(
    input={
        "messages": [
            {"role": "user", "content": "我刚才问你什么了"},
        ]
    },
    # 关键点4：在多次调用中使用相同的thread_id，模型会记住之前的对话
    config={"configurable": {"thread_id": "abc123"}},
):
    print(chunk, end="\n\n")
```
## Agent 中间件（Agent Middleware）
在create_agent方法当中，还有一个middleware参数，可以传入中间件列表，即可在调用过程中使用中间件。
在LangChain的Agent当中，中间件用于更加方便地控制Agent在执行过程当中的一些行为，例如，总结中间件可以在调用大模型前对历史消息列表进行总结，人在循环（Human-In-the-Loop）中间件，可以在调用工具过程中引入人类审核机制，人类审核通过后，才继续调用工具。
在没有中间件时，整个Agent的执行过程如下所示：
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/07-Agent 记忆与中间件（Agent Memory and Middleware）/07-Agent 记忆与中间件（Agent Memory and Middleware）-20260907112000033.png]]
用户先输入请求，会直接进入到model节点，model节点判断，如果需要调用工具，则进入到tools节点，调用完工具之后，再回到model节点，model节点内，大模型继续判断，是否需要进一步调用工具，如果不需要直接走到END节点即可。
而在引入了中间件之后，整个调用过程如下图所示：
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/07-Agent 记忆与中间件（Agent Memory and Middleware）/07-Agent 记忆与中间件（Agent Memory and Middleware）-20260907112000034.png]]
整个调用Agent的过程，可以在不改变model和tools的相关代码前提下，实现多处调整：
- before/after_agent：在agent调用的起始输入和终点输出，进行相关处理（切片编程思想）
- before/after_model: 在model调用的前后，进行相关处理（切片编程思想）
- wrap_tool/model_call: 通过handler回调的方式，拦截工具/模型执行，可以为工具执行/模型执行，添加重试，缓存，多次调用等相关逻辑（代理思想）。
注意：不同的中间件，可选择性地仅对以上的一个或者多个节点定义处理逻辑。
> [!tip] 大白话解释（Intuition）
> 中间件像在 Agent 流程的关键门口安装检查站：模型调用前可以裁剪上下文，模型调用后可以检查输出，工具执行前可以要求审批，失败时可以重试。核心 Agent 不必为每种横切需求反复改代码。
以下是两种中间件，及其分别实现的逻辑：
#### 摘要中间件（SummarizationMiddleware）
总结历史消息的中间件，可以通过多种不同的策略，使用一个单独的大模型总结历史消息。该中间件实现了before_model的处理逻辑：在调用模型前，先按照配置的策略对消息进行压缩，再传递给model节点进行调用。
实例化方式如下所示：
```python
from langchain.agents.middleware import SummarizationMiddleware

summary_middleware = SummarizationMiddleware(
    model="openai:gpt-4o-mini",
    trigger=("messages", 10),
    keep=("messages", 6),
)
```
`trigger` 表示触发总结的条件；`keep` 表示总结后保留多少最近上下文。触发条件可使用：
- (“messages”, 100)：agent消息列表的长度达到100以后，即进行总结压缩
- (“fraction”,0.5): agent消息列表当中的token总长度（langchain内部提供了token计算函数，也可以在该函数当中自定义token_counter）达到了model最大输入token数的0.5时，进行总结压缩
- (“tokens”,3000): agent消息列表当中的token总长度达到了一个绝对值之后（3000），进行总结压缩。
#### 人在回路中间件（HumanInTheLoopMiddleware）
调用工具前实现人工审核功能的中间件，可以对不同的工具，定义不同的审核策略（是否需要审核）。该中间件实现了after_model的处理逻辑。在模型回复后，该中间件判断模型的回复结果当中是否有工具调用。如果有，判断所需要调用的模型当中，是否有需要人工审核的工具。
具体实例化方式如下所示：
```python
from langchain.agents.middleware import HumanInTheLoopMiddleware

tool_name_to_interrupt = {"send_email": True, "get_current_date": False}
human_in_the_loop_middleware = HumanInTheLoopMiddleware(interrupt_on=tool_name_to_interrupt)
```
示例代码如下所示：
```python
import asyncio
from typing import Literal

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

# 1. 定义工具
@tool
def get_weather(city: str) -> str:
    """查询天气"""
    return f"{city}的天气晴朗，气温25度。"

@tool
def transfer_money(amount: int, to_account: str) -> str:
    """转账工具 (敏感操作)"""
    print(f"!!! 正在执行转账: {amount} -> {to_account} !!!")
    return f"成功转账 {amount} 元给 {to_account}。"

# 2. 初始化模型
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

# 3. 配置 HumanInTheLoopMiddleware
# 我们希望在调用 transfer_money 时暂停，让用户审核
# True 表示允许所有操作 (approve, edit, reject)
interrupt_config = {
    "transfer_money": True,
    "get_weather": False  # False 表示自动批准，不中断
}
hitl_middleware = HumanInTheLoopMiddleware(interrupt_on=interrupt_config)

# 4. 创建 Agent
# 注意：使用中断功能必须配置 checkpointer，因为中断需要保存状态
checkpointer = InMemorySaver()
agent = create_agent(
    model=llm,
    tools=[get_weather, transfer_money],
    middleware=[hitl_middleware],
    checkpointer=checkpointer,
)

async def run_demo():
    print("=== HumanInTheLoopMiddleware 演示 ===")
    print("场景：用户让 Agent 转账，Agent 在执行前会暂停等待批准。")

    thread_id = "thread-1"
    config = {"configurable": {"thread_id": thread_id}}

    # 第一步：用户发出指令,可以调整成查询天气
    print("\n[User]: 请帮我转账 100 元给 Alice")

    # 使用 ainvoke 或 stream 运行
    # 如果遇到中断，LangGraph 会暂停并保存状态
    # 我们需要在一个循环中处理这种情况，但为了演示清晰，我们分步执行

    # 第一次运行：Agent 思考 -> 决定调用 transfer_money -> Middleware 拦截 -> 中断
    # 注意：create_agent 返回的是一个 CompiledGraph，它的行为和标准 LangGraph 一致

    # 我们用一个循环来模拟持续交互，并处理潜在的中断
    current_input = {"messages": [{"role": "user", "content": "请帮我转账 100 元给 Alice"}]}
    current_command = None

    result = {}
    while True:
        try:
            # 如果有 resume command，就用它；否则用 input
            if current_command:
                result = await agent.ainvoke(current_command, config=config)
                current_command = None # 重置
            else:
                if not current_input:
                    break
                result = await agent.ainvoke(current_input, config=config)
                current_input = None # 处理完了

            # 打印结果消息
            if "messages" in result:
                for msg in result["messages"]:
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                         print(f"[Agent]: 我想调用工具: {msg.tool_calls}")
                    if msg.type == "tool":
                         print(f"[Tool Output]: {msg.content}")
                    if msg.type == "ai" and not msg.tool_calls:
                         print(f"[Agent]: {msg.content}")

        except Exception as e:
            print(f"发生错误: {e}")
            break

        # 检查是否中断，当中断时，result当中有__interrupt__键
        if "__interrupt__" in result:
            interrupt_value = result["__interrupt__"][0].value
            print(f"\n!!! 检测到中断 (Middleware 拦截) !!!")
            print(f"中断详情: {interrupt_value}")

            # 读取真实人工决策，不自动批准高风险操作
            print("\n[System]: 请审核上述操作 (approve/reject/edit):")
            decision_type = input().strip().lower()
            if decision_type not in {"approve", "reject"}:
                raise ValueError("示例仅接受 approve 或 reject")
            print(f"[User]: {decision_type}")

            # 构建回复
            # Middleware 期望的格式是 {"decisions": [{"type": "approve", ...}]}
            decisions = []
            action_requests = interrupt_value.get("action_requests", [])

            for req in action_requests:
                print(f"  - 审核操作: {req['name']} -> {decision_type}")
                decisions.append({"type": decision_type})

            # 人工审核结果：通过构造 resume command，并传入的方式传入给agent
            current_command = Command(resume={"decisions": decisions})
            print("[System]: 恢复执行...")
            continue

        # 如果没有中断，说明任务完成
        break

if __name__ == "__main__":
    asyncio.run(run_demo())
```
