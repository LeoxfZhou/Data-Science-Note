---
title: "LangChain Agent 与本地工具（Agents and Local Tools）"
tags:
  - data-science/deep-learning/nlp/llm/LangChain
status: published
created: 2026-09-07
published_at: 2026-09-07
source_document_version: V1.0.2
target_framework_line: LangChain 1.1.x
---
# LangChain Agent 与本地工具（Agents and Local Tools）
## 智能体（Agents）
## 智能体概述（Agent Overview）
智能体（Agent）是大模型应用的一种架构：模型根据当前状态决定是否调用工具，运行时执行工具并把结果反馈给模型，循环直到产生最终响应。原稿用自动驾驶分级类比人机协作程度，图示如下：
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/05-LangChain Agent 与本地工具（Agents and Local Tools）/05-LangChain Agent 与本地工具（Agents and Local Tools）-20260907112000025.png]]
语言模型本身无法采取行动——它们只是输出文本。LangChain 的一个重要功能是创建Agent。Agent 是一种使用 LLM 作为推理引擎的系统，它决定要采取哪些行动以及这些行动的输入应该是什么。这些行动的结果可以反馈给 Agent，由 Agent 决定是否需要采取更多行动，或者是否可以完成。
与传统的固定流程链不同，Agent 具备一定的自主决策能力，更适合处理开放式、多步骤的问题。它可以拆解任务，根据任务动态决定调用哪些工具，并利用中间结果推进任务。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/05-LangChain Agent 与本地工具（Agents and Local Tools）/05-LangChain Agent 与本地工具（Agents and Local Tools）-20260907112000026.png]]
> [!tip] 大白话解释（Intuition）
> 普通 Chain 像提前写好的流水线；Agent 像拿着工具箱的执行者，每一步先判断“下一步需要哪个工具”。模型只生成调用意图和参数，真正的网络请求、数据库写入或文件操作仍由程序执行，因此权限检查必须放在工具执行层，不能只依赖提示词。
Agent 的核心能力/组件：
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/05-LangChain Agent 与本地工具（Agents and Local Tools）/05-LangChain Agent 与本地工具（Agents and Local Tools）-20260907112000027.png]]
- 大模型(LLM)：作为大脑，提供推理、规划和知识理解能力。
- 记忆(Memory)：具备短期记忆和长期记忆，支持快速知识检索。
- 工具(Tools)：调用外部工具（如API、数据库）的执行单元。
- 规划(Planning)：任务分解、反思与自省框架实现复杂任务处理。
- 行动(Action)：实际执行决策的能力。
- 协作：通过与其他 Agent 交互合作，完成更复杂的任务目标。
## 构建智能体（Build an Agent）
LangChain当中提供了一个功能函数：create_agent，可以快速构建一个Agent。create_agent函数所需要传递的参数如下所示：

|名称|是否必传|描述|
|---|---|---|
|model|是|模型标识符或聊天模型实例|
|system_prompt|否|系统提示词|
|tools|是|工具列表；不需要工具时传空列表|
|response_format|否|结构化输出的schema信息|
|checkpointer|否|用以保存状态的实例，可用以实现短期记忆|
|middleware|否|要应用于代理的一系列中间件实例。 / 中间件可以在各个阶段拦截并修改代理的行为|
通过传递相关参数，即可构建一个复杂的Agent实例，接下来将详细讲解其中的tools, checkpointer和middleware参数。
## 添加本地工具（Local Tools）
Agent添加工具，本质上是使用大模型服务的function call能力，将所有的工具封装成json schema信息，在调用大模型时，传入所有的json schema，大模型在回答时，能够给出所需要调用的参数名字和入参信息。OpenAI中关于function call的文档链接：https://platform.openai.com/docs/guides/function-calling?api-mode=chat。
> [!warning] 工具安全（Tool Safety）
> 工具调用不是模型直接执行函数。应用必须校验工具名、参数类型、用户权限、资源范围和副作用；删除、付款、发信、提交代码等高风险动作应加入人工确认、幂等控制与审计日志。
#### 使用 OpenAI SDK 定义工具模式（Tool Schema）
以下代码演示了如何通过OpenAI的原生SDK来进行工具调用：
```python
from openai import OpenAI
import json

client = OpenAI()

# 1. 通过JSON结构定义工具，包括工具名称，描述，参数等
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get today's weather for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称, e.g. San Francisco",
                    },
                    "date" :{
                        "type":"string",
                        "description":"想要查询的天气的日期, e.g. 2023-12-25"
                    }
                },
                "required": ["city","date"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]

def get_weather(city,date):
    return f"{city} on {date} is cloudy with a chance of rain."

messages = [
    {"role": "user", "content": "What is the weather like in 北京 on 2024-12-25?"}
]

# 2. Prompt the model with tools defined
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages,
    tools=tools,
)

messages.append(response.choices[0].message)

for tool_call in response.choices[0].message.tool_calls or []:
    if tool_call.function.name == "get_weather":
        # 3. 执行工具函数的逻辑
        args = json.loads(tool_call.function.arguments)
        weather = get_weather(args["city"],args["date"])

        # 4. 将工具函数的执行结果添加到消息列表中
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps({"weather": weather}),
            }
        )

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages,
    tools=tools,
)

# 5. 模型会根据工具函数的执行结果，生成最终的回复
print(response.choices[0].message.content)
```
#### 通过 LangChain 定义工具（Tools）
通过原生的SDK定义工具时需要使用json来描述工具，比较繁琐。langchain.tools模块下提供了tool装饰器，可以通过 在函数上使用@tool的方式，就可以将一个函数创建成工具。
需要注意的是：定义函数时，需要通过使用 @tool装饰器内传参：description 或者是定义函数的文档字符串的方式，来添加函数的解释说明。
而对于参数的说明，没有对于参数描述的强制限制，不过也可以通过pydantic的BaseModel来定义一个入参的具体描述信息，传递到tool装饰内。
通过LangChain定义好工具之后，调用llm.bind_tools()方法，得到一个新的llm对象，后续在调用新的llm对象时，就可以使用相关的工具
示例代码如下：
```python
from langchain.tools import tool
from langchain_core.messages import HumanMessage,ToolMessage
import logging
logging.basicConfig(level=logging.DEBUG)

# 可选：通过BaseModel详细定义工具的参数
from pydantic import BaseModel,Field
class GetWeatherArgs(BaseModel):
    city: str = Field(description="城市名称")
    date: str = Field(description="日期，格式为YYYY-MM-DD")

@tool(args_schema=GetWeatherArgs)
def get_weather(city: str, date: str) -> str:
    """获取指定城市在指定日期的天气"""
    return f"{city} 在 {date} 天气多云，有下雨的可能性"

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1")

llm = llm.bind_tools([get_weather])

message_list = [
    HumanMessage(content="北京2024-12-25的天气")
]

res = llm.invoke(message_list)
message_list.append(res)

# 当前结果当中包含调用工具的出参
print('LLM的首次回复：',res)

# 解析调用工具的出参，手动调用工具
tool_call = res.tool_calls[0]
args = tool_call['args']
call_tool_res = get_weather.invoke(args)
tool_call_id = tool_call['id']

#构造Message对象
tool_message = ToolMessage(tool_call_id=tool_call_id,content=call_tool_res)
message_list.append(tool_message)

res = llm.invoke(message_list)

print('基于工具调用返回信息后，LLM的回复：',res)
```
#### 为 Agent 配置本地工具
了解了如何定义tool之后，就可以使用 create_agent来创建 一个可以调用工具的Agent了。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/05-LangChain Agent 与本地工具（Agents and Local Tools）/05-LangChain Agent 与本地工具（Agents and Local Tools）-20260907112000028.png]]
这里使用 Tavily （搜索引擎）作为工具，需要先获取它的 API-Key 并添加到环境变量。
```python
# pip install langchain-tavily
import os
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

# 定义模型
llm = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai",
)

# 定义 Tavily 搜索工具
search = TavilySearch(max_results=5)
tools = [search]

# 创建 Agent
agent = create_agent(
    model=llm,  # 模型
    tools=tools,  # 工具
    system_prompt="你是位助手，需要调用工具来帮助用户。",  # 系统提示词
)

# 调用 Agent
res = agent.invoke(
    {"messages": [{"role": "user", "content": "今天北京的天气怎么样？"}]}
)
print(res)
```
如果 Agent 执行多个步骤，这可能需要一些时间。为了显示中间进度，我们可以使用 stream 流式返回消息。
```python
# pip install langchain-tavily
import os
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

# 定义模型
llm = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai",
)

# 定义 Tavily 搜索工具
search = TavilySearch(max_results=5)
tools = [search]

# 创建 Agent
agent = create_agent(model=llm, tools=tools)

# 调用 Agent
for chunk in agent.stream(
    {
        "messages": [
            {"role": "system", "content": "你是位助手，需要调用工具来帮助用户。"},
            {"role": "user", "content": "今天北京的天气怎么样？"},
        ]
    }
):
    print(chunk, end="\n\n")
```
要想更加精确地看到每个步骤的耗时，以及输入输出等信息，可以通过LangSmith来实现。LangSmith 是一个用于调试、测试、评估和监控 LLM 应用程序（特别是基于 LangChain 和 LangGraph 构建的应用）的全流程开发平台，旨在帮助开发者将原型转化为生产级应用。
使用LangSmith非常简单，只需要配置如下两个环境变量，不需要改动任何代码，即可将整个调用过程在LangSmit当中展示，其中API_KEY可在langsmith官网进行配置：
```dotenv
LANGSMITH_TRACING="true"
LANGSMITH_API_KEY="replace-with-your-key"
```
配置好环境变量之后，可在 LangSmith 的 Tracing Projects 中查看跟踪记录。
LangSmith 默认将跟踪记录到 default 项目，可通过 LANGSMITH_PROJECT 环境变量设置 LangSmith 跟踪记录保存到哪个项目，如果该项目不存在则会创建。
