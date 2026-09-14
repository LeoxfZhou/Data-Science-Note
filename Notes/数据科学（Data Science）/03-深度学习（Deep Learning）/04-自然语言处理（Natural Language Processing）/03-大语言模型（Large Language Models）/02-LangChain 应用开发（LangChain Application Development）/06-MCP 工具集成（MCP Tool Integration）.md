---
title: "MCP 工具集成（MCP Tool Integration）"
tags:
  - data-science/deep-learning/nlp/llm/LangChain
status: published
created: 2026-09-07
published_at: 2026-09-07
source_document_version: V1.0.2
target_framework_line: LangChain 1.1.x
---
# MCP 工具集成（MCP Tool Integration）
## 为 Agent 添加 MCP 工具
### 模型上下文协议（Model Context Protocol, MCP）
Model Context Protocol（MCP，模型上下文协议）是一个开源协议，它标准化了大语言模型与外部工具和数据源通信的方式，允许开发者和工具提供商只需集成一次，就能与任何兼容 MCP 的系统交互。MCP 就像 USB-C 标准：不需要为每个设备使用不同的连接器，而是使用一个端口来处理多种类型的连接。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/06-MCP 工具集成（MCP Tool Integration）/06-MCP 工具集成（MCP Tool Integration）-20260907112000029.png]]
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/06-MCP 工具集成（MCP Tool Integration）/06-MCP 工具集成（MCP Tool Integration）-20260907112000030.png]]
> [!tip] 大白话解释（Intuition）
> 没有 MCP 时，每个 AI 应用都要为每种工具单独写适配器；MCP 规定了发现能力、调用工具、读取资源和获取提示词的统一消息格式。它统一的是连接协议，不会自动让工具安全、可信或拥有正确权限。
### MCP 架构（MCP Architecture）
MCP 遵循客户端-服务器架构，架构中包括：

|组件（Component）|职责|
|---|---|
|MCP 主机|协调和管理一个或多个 MCP 客户端的 AI 应用|
|MCP 客户端|一个保持与 MCP 服务器连接的组件，通过 MCP 定义的消息处理通信，从服务器查找并请求资源和工具，并管理与服务器的连接生命周期|
|MCP 服务器|一个向 MCP 客户端提供服务的程序，通过协议暴露工具、资源和提示模板功能|
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/06-MCP 工具集成（MCP Tool Integration）/06-MCP 工具集成（MCP Tool Integration）-20260907112000031.png]]
### MCP 传输（MCP Transports）
MCP 客户端和服务端之间的数据传输机制，包括 Stdio、Streamable HTTP、SSE。

|传输（Transport）|机制与适用场景|
|---|---|
|stdio|客户端启动本地服务器子进程，通过标准输入与标准输出交换逐行 JSON-RPC 消息；适合本地工具|
|Streamable HTTP|该传输使用 HTTP POST 和 GET 请求，服务器可以选择使用SSE来流式传输多个服务器消息。支持流式传输和服务器到客户端通知，并支持标准 HTTP 身份验证方法，包括授权令牌、API 密钥和自定义头信息|
|SSE|带有 SSE（Server-Sent Events 服务器发送事件）的 HTTP，MCP早期传输机制，现逐渐被 Streamable HTTP 取代|
### MCP 工作流程（MCP Workflow）
MCP 的典型工作流程如下：
1. **连接与初始化（Connection and Initialization）**：stdio 模式由客户端启动本地服务器子进程；Streamable HTTP 模式则连接独立运行的远端或本地 HTTP 服务。双方协商协议版本与能力。
2. **能力发现（Capability Discovery）**：客户端查询服务器暴露的工具（Tools）、资源（Resources）和提示词（Prompts）及其描述，此时并未执行具体工具。
3. **上下文注入与模型决策（Context Injection and Model Decision）**：主机把用户问题和可用工具描述交给模型，由模型生成是否调用工具以及调用参数的建议。
4. **路由与执行（Routing and Execution）**：客户端把经过权限与参数校验的 JSON-RPC 请求发送给服务器；服务器在自己的进程或服务环境中执行逻辑。
5. **结果回传（Result Feedback）**：服务器返回结果，主机将结果加入模型上下文，再决定继续调用工具还是生成最终答案。
### MCP Python SDK
#### 标准输入输出传输（stdio Transport）
以下是使用MCP进行stdio模式下的服务端编码过程：
```python
# pip install mcp
from mcp.server.fastmcp import FastMCP

# 创建 MCP 实例
mcp = FastMCP("Demo")

# 为 MCP 实例添加工具
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

# 为 MCP 实例添加资源
@mcp.resource("greeting://default")
def get_greeting() -> str:
    return "Hello from static resource!"

# 为 MCP 实例添加提示词
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    styles = {
        "friendly": "写一句友善的问候",
        "formal": "写一句正式的问候",
        "casual": "写一句轻松的问候",
    }
    return f"为{name}{styles.get(style, styles['friendly'])}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```
stdio客户端使用MCP的流程为：
- 通过stdio_client启动进程：构建stdio启动参数
- 建立会话：通过ClientSession构建会话session
- 握手初始化：调用session.initialize()
- 获取与调用能力：通过 `session.list_tools()`、`session.call_tool()`、`session.list_resources()` 等方法查询或使用 MCP 能力
示例代码如下所示：
```python
# pip install mcp
import asyncio
import sys
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

async def stdio_run():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["./mcp_server_stdio.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()

            # 获取可用工具
            tools = await session.list_tools()
            print(tools)
            print()

            # 调用工具
            call_res = await session.call_tool("add", {"a": 1, "b": 2})
            print(call_res)
            print()

            # 获取可用资源
            resources = await session.list_resources()
            print(resources)
            print()

            # 调用资源
            read_res = await session.read_resource("greeting://default")
            print(read_res)
            print()

            # 获取可用提示
            prompts = await session.list_prompts()
            print(prompts)
            print()

            # 调用提示
            get_res = await session.get_prompt("greet_user", {"name": "Jack"})
            print(get_res)
            print()

asyncio.run(stdio_run())
```
#### 可流式 HTTP 传输（Streamable HTTP Transport）
构建StreamableHttp服务端和stdio服务端类似，只是需要将服务端运行起来。运行的方式同样是通过mcp.run，并设置transport为streamable-http即可：
```python
# pip install mcp
from mcp.server.fastmcp import FastMCP

# 创建 MCP 实例
mcp = FastMCP("Demo")

# 为 MCP 实例添加工具
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

# 为 MCP 实例添加资源
@mcp.resource("greeting://default")
def get_greeting() -> str:
    return "Hello from static resource!"

# 为 MCP 实例添加提示词
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    styles = {
        "friendly": "写一句友善的问候",
        "formal": "写一句正式的问候",
        "casual": "写一句轻松的问候",
    }
    return f"为{name}{styles.get(style, styles['friendly'])}"

if __name__ == "__main__":
    # mcp.settings.host = "0.0.0.0"
    # mcp.settings.port = 8888
    mcp.run(transport="streamable-http")  # 默认启动在 127.0.0.1:8000
```
Streamable HTTP 与 stdio 的会话 API 类似，但客户端通过 `streamable_http_client()` 连接单一 HTTP 端点。MCP 规范中的 Streamable HTTP 已替代旧的 HTTP+SSE 传输；SSE 仍可用于兼容旧服务器。
```python
# pip install mcp
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def streamablehttp_run():
    url = "http://127.0.0.1:8000/mcp"

    async with streamable_http_client(url=url) as (read,write,_):
        async with ClientSession(read,write) as session:
            # 初始化连接
            await session.initialize()

            # 获取可用工具
            tools = await session.list_tools()
            print(tools)
            print()

            # 调用工具
            call_res = await session.call_tool("add", {"a": 1, "b": 2})
            print(call_res)
            print()

            # 获取可用资源
            resources = await session.list_resources()
            print(resources)
            print()

            # 调用资源
            read_res = await session.read_resource("greeting://default")
            print(read_res)
            print()

            # 获取可用提示
            prompts = await session.list_prompts()
            print(prompts)
            print()

            # 调用提示
            get_res = await session.get_prompt("greet_user", {"name": "Jack"})
            print(get_res)
            print()

asyncio.run(streamablehttp_run())
```
### LangChain 使用 MCP
LangChain Agent 可以通过 `langchain-mcp-adapters` 使用 MCP 服务器定义的工具。原稿以魔搭 MCP 广场的 12306 服务为例，但截图和代码中的托管端点具有时效性，候选稿改为从 `MCP_SERVER_URL` 环境变量读取，避免把临时地址写入笔记。
`MultiServerMCPClient.get_tools()` 会把 MCP 工具转换为 LangChain 工具。客户端默认无状态：每次工具调用建立新的 `ClientSession`，执行后再清理；只有服务器需要跨调用保存会话状态时，才应显式管理持久会话。
```python
# pip install langchain_mcp_adapters
import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

client = MultiServerMCPClient(
    {
        "remote-tools": {
            "transport": "http",
            "url": os.environ["MCP_SERVER_URL"],
        }
    }
)

def print_message(message):
    from langchain.messages import AIMessage, HumanMessage, ToolMessage
    if isinstance(message, AIMessage):
        print("AI 回复：", message.content)
        print("AI 决定调用工具：", message.tool_calls)
    elif isinstance(message, HumanMessage):
        print("用户输入：", message.content)
    elif isinstance(message, ToolMessage):
        print("工具调用结果：", message.content)
    else:
        print("未知消息类型")

async def main():
    tools = await client.get_tools()
    print([tool.name for tool in tools])

    llm = ChatOpenAI(model="gpt-4o-mini")

    agent = create_agent(model=llm, tools=tools)
    while True:
        user_input = input(">")
        if user_input == "exit":
            break
        res = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )

        print(res["messages"][-1].content, end="\n\n")
        for message in res["messages"]:
            print_message(message)
            print()

asyncio.run(main())
```
> [!warning] 远端 MCP 安全（Remote MCP Security）
> 连接远端 MCP 服务器前，应核对服务方、认证方式、工具权限、传输加密与数据处理政策。不要把访问令牌或临时托管 URL 写入 Git；对具备写入、删除、发送消息或付费能力的工具增加人工审批。
