---
title: "输出解析、提示词与 LCEL 链（Output Parsing, Prompts, and LCEL Chains）"
tags:
  - data-science/deep-learning/nlp/llm/LangChain
status: published
created: 2026-09-07
published_at: 2026-09-07
source_document_version: V1.0.2
target_framework_line: LangChain 1.1.x
---
# 输出解析、提示词与 LCEL 链（Output Parsing, Prompts, and LCEL Chains）
## 模型调用结果解析（Model Output Parsing）
模型通常返回自然语言文本，但程序需要的是可验证、可解析的结构化输出（Structured Output），例如 JSON 对象。LangChain 在 `langchain_core.output_parsers` 中提供输出解析器，也能调用模型提供商原生的结构化输出能力。
### 获取 JSON 结果（JSON Output）
要想大模型输出JSON字符串，有两种方式：
- 在提示词（Prompt）中明确约束模型输出 JSON，再由解析器校验。
- 使用模型提供商原生的结构化输出接口，以 Schema 约束响应。
#### 通过提示词约束（Prompt-based Constraint）
要使用Prompt明确约束大模型输出，需要使用到langchain所提供的JSONOutputParser,整体流程如下：
1. 通过 Pydantic 模型定义 JSON Schema。
2. 用 Pydantic 模型构造 `JsonOutputParser`。
3. 调用 `json_parser.get_format_instructions()` 取得格式约束，并放入系统消息（System Message）。
4. 调用模型后，使用 `json_parser.invoke()` 或 `parse()` 把响应解析为 Python 字典（`dict`）。
> [!tip] 大白话解释（Intuition）
> 提示词约束相当于“口头要求模型按表格填”；提供商原生结构化输出更像“系统只允许按表格字段提交”。前者兼容面广但更依赖模型自觉，后者通常更可靠，但受模型和供应商能力限制。
下面以一个具体实例来讲解，定义JSON结构：
```python
def json_output_parser():
    import os
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import JsonOutputParser
    from pydantic import BaseModel, Field
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    class Prime(BaseModel):
        prime: list[int] = Field(description="素数")
        count: list[int] = Field(description="小于该素数的素数个数")
    json_parser = JsonOutputParser(pydantic_object=Prime)
    # print(json_parser.get_format_instructions())
    res = llm.invoke([("system",json_parser.get_format_instructions()),("user","任意生成5个1000-100000之间素数，并标出小于该素数的素数个数")])
    print(res.content)
    parsed_res = json_parser.invoke(res)
    print(type(parsed_res))
```
Prompt约束，对于模型能力有一定依赖，如果模型参数不够强，容易出现幻觉，从而导致生成的JSON字符串语法有问题，或者是不符合我们所定义的JSON结构。
#### 通过模型提供商的结构化输出（Provider-native Structured Output）
对于主流大模型厂商，其API已经提供了专门的参数，用以限制模型输出内容符合我们所定义的schema结构。
以OpenAI为例，其官方文档如下：https://platform.openai.com/docs/guides/structured-outputs
示例代码如下所示：
```python
def openai_json_output_demo():
    import os
    from openai import OpenAI
    from pydantic import BaseModel

    client = OpenAI()

    class CalendarEvent(BaseModel):
        name: str
        date: str
        participants: list[str]

    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Alice and Bob are going to a science fair on Friday.",
            }
        ],
        response_format=CalendarEvent
    )

    print(response.choices[0].message.parsed)
```
再以Google Gemini为例，
```python
def gemini_json_output_demo():
    import os
    from google import genai
    from pydantic import BaseModel, Field
    from typing import List, Optional
    # 1、定义一个Pydantic模型，用于表示日历事件
    class CalendarEvent(BaseModel):
        name: str
        date: str
        participants: list[str]

    # 2、初始化 Gemini Developer API 客户端
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
    )

    # 3、定义一个提示模板，用于生成日历事件
    prompt = """
    Alice and Bob are going to a science fair on Friday.
    """

    # 4、调用Gemini模型生成内容
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": CalendarEvent.model_json_schema(),
        },

    )

    print(response.text)

    # 5、解析Gemini模型的响应,将JSON字符串转换为CalendarEvent对象
    event = CalendarEvent.model_validate_json(response.text)
    print(event)
```
两个案例当中，都没有在Prompt当中明确指定以JSON输出，但是调用API返回结果仍然能够正确得到结果。
LangChain也对这种能力提供了封装：不同厂商的模型都是继承了ChatModel基类，而ChatModel提供了 with_structured_output方法，传入pydantic base model类作为schema对象，得到一个新的llm对象，调用新的llm对象即可。
具体代码如下所示：
```python
def json_output_use_langchain():
    import os
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
    from langchain_core.output_parsers import JsonOutputParser
    from pydantic import BaseModel, Field
    # 1、初始化llm: 可以使用OpenAI,也可以使用Gemini
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    # llm = ChatGoogleGenerativeAI(
    #     model="gemini-2.5-flash-lite",
    #     temperature=0.0,
    #     google_api_key=os.getenv("GOOGLE_API_KEY"),
    # )

    # 2、定义一个Pydantic模型，用于表示日历事件
    class CalendarEvent(BaseModel):
        name: str
        date: str
        participants: list[str]

    #3、使用with_structured_output，得到一个新的llm，用于生成结构化输出
    new_llm=llm.with_structured_output(schema=CalendarEvent)
    #4、调用新的llm，生成结构化输出
    res = new_llm.invoke("Alice and Bob are going to a science fair on Friday.")
    print(res)
    print(type(res))
```
不管使用什么模型，都是调用统一的方法，就能够实现相关的需求，如果需要换模型，只需要调整llm实例化代码即可，其余代码无需改动，这正是LangChain框架的强大之处。
### 解析其他输出类型（Other Output Parsers）
要想获取其他形式的结果，例如XML等，也可通过output_parser当中的其他类来实现，在output_parser包中提供的parser有如下：
```python
__all__ = [
    "BaseCumulativeTransformOutputParser",
    "BaseGenerationOutputParser",
    "BaseLLMOutputParser",
    "BaseOutputParser",
    "BaseTransformOutputParser",
    "CommaSeparatedListOutputParser",
    "JsonOutputKeyToolsParser",
    "JsonOutputParser",
    "JsonOutputToolsParser",
    "ListOutputParser",
    "MarkdownListOutputParser",
    "NumberedListOutputParser",
    "PydanticOutputParser",
    "PydanticToolsParser",
    "SimpleJsonOutputParser",
    "StrOutputParser",
    "XMLOutputParser",
]
```
由于JSON的强大，对于其他类型，此处不再赘述，大部分场景下，使用JSON输出即可满足需求。
## 提示词模板（Prompt Templates）
在应用开发中，固定的提示词限制了模型的灵活性和适用范围。通过提示词模板，我们可以将变量插入到模板中，从而创建出不同的Prompt。
LangChain当中有多种类型的提示模板，常用的有 PromptTemplate（字符串提示模板）和 ChatPromptTemplate（聊天提示模板）。
提示词模板以字典作为输入，其中每个键代表要填充的提示模板中的变量。并输出一个 PromptValue。这个 PromptValue 可以传递给聊天模型，也可以转换为字符串或消息列表。PromptValue 存在的目的是为了方便在字符串和消息之间切换。
以下使用PromptTemplate为例子做一个介绍：
```python
def prompt_template_demo():
    from langchain_core.prompts import ChatPromptTemplate
    from langchain.chat_models import init_chat_model
    # 使用构造方法实例化提示词模板
    chat_prompt_template = ChatPromptTemplate.from_messages(
        messages=[
            ("system", "你是一个专业的评论员"),
            ("human", "请评价{product}的优缺点，包括{aspect1}和{aspect2}。"),
        ],
    )

    chat_message_list = chat_prompt_template.invoke({"product": "iPhone 15", "aspect1": "性能", "aspect2": "外观"})

    llm = init_chat_model(
        model="gpt-4o-mini",
        model_provider="openai",
    )
    resp = llm.invoke(chat_message_list)
    print(resp.content)
```
## 链与可运行对象（Chains and Runnables）
在前面的例子当中所涉及到的模型调用、解析器调用，以及对PromptTemplate调用，都使用到了invoke方法，这是因为这些类都实现了LangChain最底层定义的Runnable接口，其代表了LangChain 中可以调用、批处理、流式传输、转换和组合的工作单元，是使用 LangChain 组件的基础，它在许多组件中实现，例如语言模型、输出解析器、检索器、编译的 LangGraph 图等。
Runnable 接口定义了一系列标准的方法，如下所示：

|同步 / 异步方法|作用|
|---|---|
|`invoke()` / `ainvoke()`|将单个输入转换为输出|
|`batch()` / `abatch()`|批量将多个输入转换为输出|
|`stream()` / `astream()`|从单个输入产生流式输出|
|其他方法|具体能力取决于 Runnable 实现|
为什么需要统一调用方式？
假设没有统一调用方式，每个组件调用方式不同，组合时需要手动适配：
- 提示词渲染用 .format()
- 模型调用用 .generate()
- 解析器解析用 .parse()
- 工具调用用 .run()
代码会变成：
```python
prompt_text = prompt.format(topic="猫")  # 方法1
model_out = model.generate(prompt_text)  # 方法2
result = parser.parse(model_out)  # 方法3
```
Runnable 统一调用方式：
```python
# 分步调用
prompt_text = prompt.invoke({"topic": "猫"})  # 方法1
model_out = model.invoke(prompt_text)  # 方法2
result = parser.invoke(model_out)  # 方法3
```
而所有实现了Runnable接口的组件，均可以通过一种特定的方式，将其连接起来，打包成一整个可调用对象，这也就是LangChain当中的Chain的由来，而这种方式则称之为LCEL。
LCEL （LangChain Expression Language），中文名称为LangChain 表达式语言，是一种从现有的Runnable 构建新的 Runnable 的声明式方法，用于声明、组合和执行各种组件（模型、提示、工具、函数等）。
> [!tip] 大白话解释（Intuition）
> Runnable 是统一规格的积木，`invoke()` 是统一的“启动按钮”，`|` 则把前一块积木的输出接到后一块积木的输入。`RunnableSequence` 是流水线，`RunnableParallel` 是把同一份输入同时交给多条支路。
```python
# LCEL管道式
chain = prompt | model | parser  # 用管道符组合
result = chain.invoke({"topic": "猫"})  # 所有组件统一用invoke
```
无论组件的功能多复杂（模型/提示词/工具），调用方式完全相同。并且可以通过管道符 | 组合，自动处理类型匹配和中间结果传递。
我们称使用 LCEL 创建的 Runnable 为“链”，“链”本身就是 Runnable。
LCEL 两个主要的组合原语是 RunnableSequence 和 RunnableParallel。许多其他组合原语可以被认为是这两个原语的变体。
### 可运行序列（RunnableSequence）
RunnableSequence 按顺序“链接”多个可运行对象，其中一个对象的输出作为下一个对象的输入。
LCEL重载了 | 运算符，以便从两个 Runnables 创建 RunnableSequence。
```python
chain = runnable1 | runnable2
# 等同于
chain = RunnableSequence([runnable1, runnable2])
```
举例：提示模板➡️模型➡️输出解析器
```python
import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt_template = PromptTemplate(
    template="讲一个关于{topic}的笑话",
    input_variables=["topic"],
)

llm = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai", # 注意，此处没有再传入base_url=xxx 是因为默认也会读取相关环境变量，
)

parser = StrOutputParser()

chain = prompt_template | llm | parser

resp = chain.invoke({"topic": "人工智能"})
print(resp)
```
### 可运行并行（RunnableParallel）
RunnableParallel 同时运行多个可运行对象，并为每个对象提供相同的输入。
对于同步执行，RunnableParallel 使用 ThreadPoolExecutor 来同时运行可运行对象。对于异步执行，RunnableParallel 使用 asyncio.gather 来同时运行可运行对象。
构造RunnableParallel实例时，参数列表是可变数量关键字参数，一个参数名对应着一个可运行组件，每个可运行组件输出结果将作为参数名key所对应的值，封装到整个运行实例的结果当中。
具体代码如下所示：
```python
def runnable_parallel_demo():

    import os
    from langchain.chat_models import init_chat_model
    from langchain_core.prompts import PromptTemplate
    from langchain_core.runnables import RunnableParallel
    from langchain_core.output_parsers import StrOutputParser

    llm = init_chat_model(
        model="gpt-4o-mini",
        model_provider="openai",
    )

    english_chain = (
        PromptTemplate.from_template("把这个句子{topic}翻译成英文") | llm | StrOutputParser()
    )
    korean_chain = (
        PromptTemplate.from_template("把这个句子{topic}翻译成韩文") | llm | StrOutputParser()
    )

    map_chain = RunnableParallel(english=english_chain, korean=korean_chain)

    resp = map_chain.invoke({"topic": "人工智能是一种智能技术"})
    print(resp)

if __name__ == "__main__":
    runnable_parallel_demo()
```
在LCEL当中，要想定义并行运行结构，只需通过字典的方式定义即可，代码如下所示：
```python
def runnable_parallel_use_lcel_demo():

    import os
    from langchain.chat_models import init_chat_model
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    # 1、初始化两个模型
    llm = init_chat_model(
        model="gpt-4o-mini",
        model_provider="openai",
    )
    deepseek_llm = init_chat_model(
        model="deepseek-chat",
        model_provider="deepseek",
    )

    # 2、创建两个并行运行的chain：使用两个不同的模型回答同一个问题，用以对比结果
    paragraph_1_chain = (
        PromptTemplate.from_template("对这首诗{poem}做一下赏析，分析它蕴含的含义") | llm | StrOutputParser()
    )
    paragraph_2_chain = (
        PromptTemplate.from_template("对这首诗{poem}做一下赏析，分析它蕴含的含义") | deepseek_llm | StrOutputParser()
    )

    # 3、对前面的两个chain的结果进行分析总结
    summary_chain = (
        PromptTemplate.from_template("这两种赏析，第一种：{paragraph_1}，第二种：{paragraph_2}，哪个更好，为什么") | llm | StrOutputParser()
    )

    # 4、构造LCEL：将前面的两个chain并行运行，然后将结果传递给summary_chain
    map_chain = {
        "paragraph_1": paragraph_1_chain,
        "paragraph_2": paragraph_2_chain,
    } | summary_chain

    poem= """
    菩提本无树，
    明镜亦非台，
    本来无一物，
    何处惹尘埃。
    """

    # 5、运行LCEL
    resp = map_chain.invoke({"poem": poem})
    print(resp)

if __name__ == "__main__":
    runnable_parallel_use_lcel_demo()
```
### 其他可运行结构（Other Runnable Primitives）
LangChain所提供的其他Runnable组件，如下表所示，此处不再详细介绍。

|名称|描述|
|---|---|
|RunnableLambda|将普通函数，封装成符合Runnable接口的可运行组件|
|RunnableBranch|对输入进行if-else判断，并路由到不同的函数中|
|RunnablePassthrough|接收输入并将其原样输出；LCEL 体系中的“无操作节点”，用于在流水线中透传输入或保留上下文，也可以用于向输出中添加键|
|RunnableWithFallbacks|对Runnable组件进行兜底，使得 Runnable 失败后可以回退到其他 Runnable|
LCEL 适合确定性的有向数据流；需要循环决策、状态持久化和多步工具调用时，通常使用基于 LangGraph 的 Agent。两者不是简单替代关系：固定流程优先使用可预测的 Chain，需要模型动态决定下一步时再使用 Agent。
