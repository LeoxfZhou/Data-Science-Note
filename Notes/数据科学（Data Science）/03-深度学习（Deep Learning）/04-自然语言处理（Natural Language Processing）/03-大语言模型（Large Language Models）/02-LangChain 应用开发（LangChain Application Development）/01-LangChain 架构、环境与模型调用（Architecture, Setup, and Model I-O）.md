---
title: "LangChain 架构、环境与模型调用（Architecture, Setup, and Model I/O）"
tags:
  - data-science/deep-learning/nlp/llm/LangChain
status: published
created: 2026-09-07
published_at: 2026-09-07
source_document_version: V1.0.2
target_framework_line: LangChain 1.1.x
---
# LangChain 架构、环境与模型调用（Architecture, Setup, and Model I/O）
## LangChain 概述（LangChain Overview）
## 什么是 LangChain
LangChain 是 Harrison Chase 于 2022 年发起的开源框架，用于开发由大语言模型（Large Language Model, LLM）驱动的应用程序。
相关入口：
- **GitHub**：https://github.com/langchain-ai/langchain
- **官网**：https://www.langchain.com/langchain
- **官方文档**：https://docs.langchain.com/oss/python/langchain/overview
- **API 文档（API Reference）**：https://reference.langchain.com/python/langchain/
LangChain 常用于智能体（Agent）、问答系统（Question Answering, QA）、文档搜索、检索增强生成（Retrieval-Augmented Generation, RAG）与工具调用（Tool Calling）。
下图记录了原稿所引用的 GitHub Stars 热度变化；Stars 只能反映社区关注度，不能直接代表框架质量或生产成熟度。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）-20260907161350490.png]]
下面通过两个问题，来看下LangChain所提供的价值：
#### 问题1：LLMs用的好好的，为什么还需要LangChain？
在大语言模型（LLM）如 ChatGPT、Claude、DeepSeek 等快速发展的今天，开发者不仅希望能“使用”这些模型，还希望能将它们灵活集成到自己的应用中，实现更强大的对话能力、检索增强生成（RAG）、工具调用（Tool Calling）、多轮推理等功能。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）-20260907161350491.png]]
#### 问题2：我们可以使用GPT 或GLM4 等模型的API进行开发，为何需要LangChain这样的框架？
不使用LangChain，确实可以使用GPT 或GLM4 等模型的API进行开发。
但使用LangChain的好处：
- 简化开发难度：更简单、更高效、效果更好。
- 开发人员可以更专注于业务逻辑，而无须花费大量时间和精力处理底层技术细节。
- 学习成本更低：不同模型的API不同，调用方式也有区别，切换模型时学习成本高。使用LangChain，可以以统一、规范的方式进行调用，有更好的移植性。
- 现成的Agent构建方法：LangChain提供了现成的构建Agent的方式。让复杂的逻辑变得结构化、易组合、易扩展。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）-20260907161350498.jpeg]]
> [!tip] 大白话解释（Intuition）
> 直接调用模型供应商的 SDK，像是每换一种电器就重新配一套插头；LangChain 把常见的模型、提示词、解析器、检索器和工具包装成相对统一的接口，便于替换和组合，但并不会消除各供应商独有参数与行为差异。
## 包与核心模块（Packages and Core Modules）
### 主要软件包（Packages）
LangChain所包含的包及其描述，如下所示：

|包|描述|
|---|---|
|langchain|包含构建使用 LLM 的应用所需的所有实现的主入口点|
|langchain-core|LangChain 生态系统中的核心接口和抽象|
|langchain-openai/deepseek|LangChain和OpenAI（deepseek）集成包。langchain还包含一系列集成包，这些集成包涵盖了文本生成模型，工具，文档加载，向量存储等多个方面，构成了langchain生态系统。|
|langchain-mcp-adapters|在 LangChain 和 LangGraph 应用中提供 MCP 工具|
|langchain-text-splitters|用于文档处理的文本分割工具|
|langchain-tests|用于验证 LangChain 集成包实现的标准化测试套件|
|langchain-classic|遗留的 langchain 实现和组件，主要为1.0.0版本以前的相关内容|
### 核心模块（Core Modules）
LangChain的核心组件，从逻辑上可以划分为以下四大部分：Model I/O、Chains、RAG、Agents。
#### Model I/O
标准化大模型的输入和输出，包含提示模版，模型调用和格式化输出。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）-20260907161350497.png]]
##### Format（格式化）：通过模板管理大模型的输入。将原始数据格式化成模型可以处理的形式，插入到一个模板中，然后送入模型进行处理。
##### Predict（预测）：调用 LLM 接收输入，进行预测或生成回答。
##### Parse（解析）：规范化模型输出。比如将模型输出格式化为 JSON。
#### 链与可运行对象（Chains and Runnables）
“链条”用于将多个组件组合成一个完整的流程，方便链式调用。
#### 检索增强生成（Retrieval-Augmented Generation, RAG）
对应RAG：检索外部数据，作为参考信息输入LLM辅助生成答案。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）-20260907161350500.jpeg]]
#### 智能体（Agents）
Agent 自主规划执行步骤并使用工具来完成任务。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）-20260907161350494.png]]
## 环境准备（Environment Setup）
原稿示例环境使用 Python 3.12。实际项目应创建独立虚拟环境（Virtual Environment），并使用锁定版本的 `requirements.txt`、`pyproject.toml` 或其他依赖清单保证环境可复现；各示例所需的集成包在相邻代码中单独列出。
## 模型输入输出（Model I/O）
## 模型输入输出概览（Model I/O Overview）
Model I/O 部分是与语言模型进行交互的核心组件，包括输入提示（Prompt Template）、调用模型（Model）、输出解析（Output Parser）。简单来说，就是输入、处理、输出这三个步骤。
## 调用在线模型（Calling Hosted Models）
### 常用模型服务平台（Model Service Platforms）
有许多提供大模型API服务的平台，如下所示：
原稿列举的模型服务平台包括 OpenRouter、阿里云百炼、百度千帆、硅基流动以及第三方 OpenAI 代理服务。平台能力、模型、价格、地区限制和兼容程度会变化，使用前应核对各平台当前官方文档；第三方代理还需要额外评估数据合规、日志留存和密钥安全风险。
调用托管模型通常需要模型名、应用程序编程接口密钥（API Key）和基础地址（Base URL）。API Key 属于敏感凭据，只能通过环境变量、密钥管理服务或未被 Git 跟踪的 `.env` 文件注入，不能硬编码到代码、笔记、日志或版本库中。
配置环境变量有两种方式：
#### 通过 `.env` 文件配置
通过.env配置过程如下：
1. 在项目根目录创建 `.env`，写入 `OPENAI_BASE_URL` 和 `OPENAI_API_KEY`。
2. 通过 `python-dotenv` 的 `load_dotenv()` 加载文件。
3. 通过 Python 标准库 `os` 读取环境变量。
`.env` 示例：
```dotenv
OPENAI_API_KEY=replace-with-your-key
OPENAI_BASE_URL=https://api.example.com/v1
```
读取示例如下所示：
```python
# pip install python-dotenv
# 1、从dotenv导入load_dotenv方法
from dotenv import load_dotenv

# 2、调用load_dotenv方法加载.env文件
load_dotenv()

# 3、通过os模块读取环境变量
import os
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("未设置 OPENAI_API_KEY")
```
必须把 `.env` 加入 `.gitignore`。不要通过 `print()`、异常消息或调试日志输出完整密钥。Windows、macOS 与 Linux 也可以使用系统级环境变量；系统变量适合本机反复使用的配置，但不应把长期密钥共享给无关进程。
### 使用 OpenAI SDK 调用模型
OpenAI 的 GPT 系列模型影响了大模型技术发展的开发范式和标准。大部分模型，例如 Qwen、ChatGLM、DeepSeek 等模型，它们的使用方法和函数调用逻辑基本遵循 OpenAI 定义的规范，都可以使用OpenAI SDK来进行调用。
OpenAI的接口调用方式也经历的一些转变，其中最为经典的一套API，称之为ChatCompletionsAPI（官方文档链接：https://platform.openai.com/docs/api-reference/chat）。
而在2025年年中，OpenAI又发布了一套新的API: ResponsesAPI（官方文档链接：https://platform.openai.com/docs/api-reference/responses）。
ResponsesAPI是当前OpenAI中最先进的一套API，对ChatCompletionsAPI做了多处升级，例如，支持服务端内置工具调用，支持服务端维护状态（短期记忆）等。
#### ChatCompletionAPI 调用示例
```python
# pip install openai
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),  # 平台提供的 URL
    api_key=os.getenv("OPENAI_API_KEY"),  # 平台提供的 API-Key
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",  # 模型名称
    messages=[{"role": "user", "content": "将'你好'翻译成意大利语"}],  # 用户输入
)
print(completion.choices[0].message.content)
```
#### ResponsesAPI调用示例
```python
import os
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.1",
    input="中国国内今天发生了哪些大事儿？",
    tools=[{"type": "web_search"}] # 可以自动调用内置工具
)

print(response.output_text)
```
### 使用 Google SDK 调用模型
如果需要直接调用 Gemini 模型，可以使用 Google Gen AI SDK。下面使用官方环境变量名并避免写死第三方代理地址：
```python
# pip install google-genai
def call_gemini():
    import os
    from google import genai
    from dotenv import load_dotenv
    load_dotenv()
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="你是谁，能做什么",
    )
    print(response.text)
```
### 使用 LangChain API 调用模型
通过上面两个例子，可以看到，对于不同厂商的模型，需要学习不同的SDK的API来进行调用（注意：虽然大部分模型厂商可以兼容OpenAI SDK规范，但是对于复杂场景下，例如后面会学习到的结构化输出等场景，各厂商之间具体构造参数的方式仍有差别），而通过LangChain调用API，其封装了不同模型调用时，复杂的出入参的构建和解析，得到llm对象之后，我们可以通过统一的方法来进行模型调用和结果解析。
在使用langchain进行模型调用时，需要先安装相应的包。对于OpenAI，需要安装langchain-openai包，而如果需要使用DeepSeek的模型，则需要安装langchain-deepseek。（具体可参考官网：https://docs.langchain.com/oss/python/integrations/providers/overview）。
使用LangChainAPI进行调用的步骤如下：
- 构造聊天模型实例（Chat-model Instance）。
- 传入普通字符串或消息（Message）列表并调用模型。
- 解析模型返回的消息对象。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）-20260907161350495.png]]
#### 构造聊天模型实例（Chat-model Instance）
聊天模型（Chat Model）实例代表一个可调用的 LLM 对象，有两种初始化方式：
- 使用 LangChain 提供的统一函数 `init_chat_model()`。
- 使用特定集成包的模型类，例如 `langchain-openai` 中的 `ChatOpenAI`。
下面首先介绍init_chat_model的初始化参数，代码示例如下：
```python
# pip install langchain
# pip install langchain-openai
def get_model_from_init():
    import os
    import dotenv
    dotenv.load_dotenv()
    from langchain.chat_models import init_chat_model

    llm = init_chat_model(
        model="gpt-4o-mini",
        model_provider="openai",
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    resp = llm.invoke("你好")
    print(type(resp))  # <class 'langchain_core.messages.ai.AIMessage'>
    print(resp.content) # 获取结果
```
init_chat_model所接收的相关参数如下面所示：

|参数|说明|
|---|---|
|model|模型名称或标识符，例如gpt-4o-mini|
|model_provider|模型提供厂商,例如：openai|
|base_url|发送请求的 API 端点的 URL。常由模型的提供商提供|
|api_key|与模型提供商进行身份验证所需的 API 密钥|
|temperature|控制采样分布的随机程度；具体范围与效果依模型供应商而异，不能简单等同于“创造力”|
|timeout|在取消请求之前，等待模型响应的最大时间（以秒为单位）|
|max_tokens|限制响应中的总tokens 数量，控制输出长度|
|max_retries|请求失败时系统尝试重新发送请求的最大次数|
令牌（Token）是模型分词器处理文本的基本单位，既不固定等于一个汉字，也不固定等于一个英文单词。字符与 Token 的换算取决于模型使用的分词器、语言、符号和文本内容；只能用对应模型的分词器实际测量，不能把固定平均值当成边界保证。模型供应商通常按输入与输出 Token 计量或收费。
Token与字符转化的可视化工具：
- OpenAI提供：https://platform.openai.com/tokenizer
- 百度智能云提供：https://console.bce.baidu.com/support/#/tokenizer
使用特定包下的类构造LLM实例和init_chat_model在本质上是一样的（init_chat_model底层就是调用特定包下的类构造LLM实例），参考代码如下所示：
```python
def get_model_from_openai_package():
    import os
    import dotenv
    dotenv.load_dotenv()
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    resp = llm.invoke("你好")
    print(type(resp))
    print(resp.content)

if __name__ == "__main__":
    get_model_from_openai_package()
```
对于其他厂商，代码类似，此处不再赘述。
#### 调用模型实例（Model Invocation）
调用LLM实例时，有两处需要关注：调用传入的对象类型和调用方式。
#### 调用传入对象类型
前面的例子当中，我们直接传入字符串对象，这通常适用于不需要保留对话历史的直接生成任务。
除此以外，更加好的方式是传入一个消息列表：
```python
def invoke_llm_with_message_list():
    import os
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    resp = llm.invoke([SystemMessage(content="你是一个专业的数学助手"),HumanMessage(content="你好，你是谁")])
    print(type(resp))
    print(resp.content)

if __name__ == "__main__":
    invoke_llm_with_message_list()
```
消息列表表示了一段“聊天记录历史”；而不同的消息类型，则代表了不同的角色，各种类型及相关描述如下：

|消息类型|描述|
|---|---|
|SystemMessage|代表一组初始指令，用于引导模型的行为。可以使用系统消息来设定语气、定义模型的角色，并建立响应的指导方针|
|HumanMessage|表示用户输入，可以在message当中传递其他元数据信息|
|AIMessage|模型生成的响应，包括文本内容、工具调用和token使用量等元数据信息|
|ToolMessage|表示工具调用的输出|
HumanMessage、AIMessage 和 SystemMessage 是常用的消息类型。
ToolMessage 是在工具调用场景下才会使用的特殊消息类型。
消息对象，除了使用HumanMessage等类以外，还可以通过元组对象来表示，元组对象第一个元素表示角色，第二个元素表示具体消息内容；也可以通过OpenAI官方使用的dict来表示，dict当中有两个键，第一个为role，表示角色，第二个为content，表示内容。
示例代码如下：
```python
def invoke_llm_with_message_list_use_tuple():
    import os
    import dotenv
    dotenv.load_dotenv()
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    # 以下两种方式是等价的
    messages_list = [("system","你是一个专业的数学助手"),("user","你好，你是谁")]
    message_list = [{"role":"system","content":"你是一个专业的数学助手"},{"role":"user","content":"你好，你是谁"}]
    resp = llm.invoke(message_list)
    print(type(resp))
    print(resp.content)

if __name__ == "__main__":
    invoke_llm_with_message_list_use_tuple()
```
#### 调用方式
除了上述调用方式外，LangChain的LLM对象还支持异步调用、流式调用、批调用等多种方式。
异步调用在实际生产环境下非常实用，可以大大提高程序的响应性能，示例代码如下：
```python
import asyncio
async def call_llm_async():

    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini"
    )
    response = await llm.ainvoke(
        input=[("user", "什么是LangChain")]
    )
    print(response.content)

if __name__ == "__main__":
    asyncio.run(call_llm_async())
```
流式调用，可以让大模型输出结果实现打字机效果，示例代码如下：
```python
def call_llm_streaming_mode():

    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini"
    )
    # 调用stream方法，返回迭代器对象
    response = llm.stream(
        input=[("user", "什么是LangChain")]
    )
    # 遍历迭代器对象，打印每个chunk的内容
    for chunk in response:
        print(chunk.content,end="")

call_llm_streaming_mode()
```
批次调用，可以并行发出多个请求，统一回收相关结果，示例代码如下：
```python
def call_llm_batch_mode():
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini"
    )
    # 调用batch方法，底部通过thread 并行调用模型
    response = llm.batch(
        inputs=[
            [("user", "什么是 LangChain？")],
            [("user", "LangChain 的核心价值是什么？")],
        ]
    )
    # 打印每个问题的回答
    for question_chunk in response:
        print(question_chunk.content)

call_llm_batch_mode()
```
#### 解析调用结果（Response Parsing）
解析调用结果会在3.4节中重点介绍，此处略过。
## 调用本地模型（Calling Local Models）
### Ollama 概述
Ollama 是用于下载、管理并在本地运行多种大语言模型的开源运行时，可运行 Qwen、DeepSeek、Llama 等多个模型家族。它适合本地开发、原型验证与单机使用；生产部署还需要结合吞吐量、并发、显存、模型许可和运维要求评估 Ollama、vLLM 或其他推理服务方案，不能仅凭工具名称判断。
Ollama官方地址：https://ollama.com
Ollama Github开源地址：https://github.com/ollama/ollama
### Ollama 安装
Ollama项目支持跨平台部署，目前已兼容Mac、Linux和Windows操作系统。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）-20260907161350503.png]]
无论使用哪个操作系统，Ollama项目的安装过程都设计得非常简单。
访问 https://ollama.com/download 下载对应系统的安装文件。
- Windows 系统执行.exe文件安装
- Linux 系统执行以下命令安装：
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
该命令会下载远程安装脚本并立即交给 `sh` 执行。执行前应从官方地址审查脚本；安装过程通常会检查系统环境、下载二进制文件、配置系统服务并启动 Ollama 服务。
### 模型下载与运行（Model Download and Run）
访问https://ollama.com/search可以查看Ollama支持的模型。使用命令行可以下载并运行模型，例如运行qwen3:8b模型：
```bash
ollama run qwen3:8b
```
#### 进入到Settings
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）/01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）-20260907161350501.png]]
#### 切换模型目录
在 Ollama 设置中可以把模型目录（Model Location）切换到具有足够磁盘空间的自定义目录。原稿截图显示了这一设置入口；正式配置不要照抄截图中的个人路径。
调用本地模型
举例：
```python
# pip install langchain-ollama
from langchain_ollama import ChatOllama

ollama_llm = ChatOllama(model="qwen3:8b")
messages = {"role": "user", "content": "你好，请介绍一下你自己"}
resp = ollama_llm.invoke(messages)
print(resp.content)
```
若 Ollama 不在本地默认端口运行，需指定 base_url，即：
```python
# pip install langchain-ollama
from langchain_ollama import ChatOllama

ollama_llm = ChatOllama(
    model="qwen3",    base_url="http://localhost:11434",
)
messages = {"role": "user", "content": "你好，请介绍一下你自己"}
resp = ollama_llm.invoke(messages)
print(resp.content)
```
