---
title: "S1 Python 工程与基础算法（Python Engineering and Algorithms）"
aliases:
  - "S1 Python Engineering and Algorithms"
tags:
  - career/llm-application-engineer
  - interview/python
status: published
created: 2026-08-27
updated: 2026-08-27
---
# S1 Python 工程与基础算法（Python Engineering and Algorithms）
> [!tip] 导航（Navigation）
> 上一阶段：[[01-S0 开发环境与基础复核（Environment and Foundation Review）]]｜[[00-概览（Overview）]]｜下一阶段：[[03-S2 PyTorch、深度学习与 NLP 基础（PyTorch, Deep Learning and NLP）]]
## 1. Python 对象、复制与函数参数（Objects, Copying, and Function Parameters）
### 概念与原理（Concept and Mechanism）
- Python 变量保存对象引用（Object Reference），不是把值复制进变量盒子。可变对象（Mutable Object）可原地改变，不可变对象（Immutable Object）需要创建新对象。
- 浅拷贝（Shallow Copy）只复制最外层容器，内部对象仍共享；深拷贝（Deep Copy）递归复制对象图，但代价更高，也不适合复制数据库连接等外部资源。
- 默认参数在函数定义时求值，因此不能用可变对象作为共享默认容器。

### 最小代码示例（Minimal Example）
```python
def append_item(item: str, items: list[str] | None = None) -> list[str]:
    # 每次调用都创建新列表，避免多个调用共享同一个默认对象。
    result = [] if items is None else items
    result.append(item)
    return result

print(append_item("a"))  # 输出: ['a']
print(append_item("b"))  # 输出: ['b']
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：`is` 和 `==` 有什么区别？**

**参考答案：**`is` 判断两个引用是否指向同一个对象，`==` 调用相等性协议比较值。判断 `None` 应使用 `is None`；比较业务值通常使用 `==`。

**问题：为什么函数默认参数不能写成 `items=[]`？**

**参考答案：**默认对象只在函数定义时创建一次，后续调用会复用同一列表，导致状态跨调用泄漏。应以 `None` 为哨兵，在函数内部创建新容器。

### 相关笔记（Related Notes）
- [[02-Python 基础语法（Python Basics）]]

## 2. 数据建模、类型提示与模块边界（Data Modeling, Type Hints, and Modules）
### 概念与原理（Concept and Mechanism）
- `dataclass` 适合表达内部数据结构；Pydantic 适合位于系统边界的外部输入验证和序列化。类型提示（Type Hint）主要服务静态检查、IDE 和阅读，不会自动阻止运行时传入错误类型。
- `if __name__ == "__main__":` 只在文件被直接运行时执行入口代码，被其他模块导入时不会执行，便于复用和测试。

### 最小代码示例（Minimal Example）
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Document:
    title: str
    content: str

document = Document(title="RAG", content="retrieval")
print(document.title)  # 输出: RAG
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：类型提示能否替代运行时校验？**

**参考答案：**不能。Python 默认不会依据类型提示拒绝错误输入；外部 API、配置和文件数据仍需 Pydantic 或显式校验。类型提示主要提前暴露开发期错误并表达接口契约。

### 相关笔记（Related Notes）
- [[04-文件、路径、模块与包（Files Paths Modules and Packages）]]
- [[05-面向对象编程（Object-Oriented Programming）]]

## 3. 异常、重试、日志与配置（Exceptions, Retries, Logging, and Configuration）
### 概念与原理（Concept and Mechanism）
- 异常应在能够恢复、转换或增加上下文的层处理；不知道如何处理时应继续传播。
- 可重试错误（Retryable Error）通常来自短暂网络或服务故障；认证失败、输入错误和业务拒绝通常不可重试。
- 日志记录事件及上下文，不能记录 API Key、密码、完整隐私文本或不可控的大模型上下文。异常日志应保留 traceback 和请求标识符（Request ID）。

### 最小代码示例（Minimal Example）
```python
import logging

logger = logging.getLogger(__name__)

def parse_count(raw_value: str) -> int:
    try:
        return int(raw_value)
    except ValueError:
        logger.exception("count 解析失败")
        raise

print(parse_count("3"))  # 输出: 3
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：`logger.error()` 和 `logger.exception()` 有什么区别？**

**参考答案：**`logger.exception()` 应在异常处理上下文中使用，会自动附带当前 traceback；`logger.error()` 默认只记录消息。没有 traceback 时，线上日志可能只能看到“失败”而无法定位调用链。

**问题：重试为什么必须设置上限？**

**参考答案：**无限重试会放大下游故障、占用连接和工作线程，并可能重复执行有副作用的操作。可靠重试需要限定次数、总时长、退避、抖动和可重试异常范围。

### 相关笔记（Related Notes）
- [[03-错误与异常（Errors and Exceptions）]]

## 4. 文件格式、流式处理与数据清洗（File Formats, Streaming, and Cleaning）
### 概念与原理（Concept and Mechanism）
- JSON 保存一个完整值；JSONL 每行一个独立 JSON 对象，适合追加、流式读取和隔离坏行；CSV 是表格交换格式，需要明确编码、分隔符、引号和空值语义。
- 生成器（Generator）按需产生元素，可降低大文件峰值内存；Pandas 适合列式清洗、聚合和探索，但超大数据仍需要分块或其他执行引擎。

### 最小代码示例（Minimal Example）
```python
import json
from collections.abc import Iterator

def parse_jsonl(lines: list[str]) -> Iterator[dict[str, object]]:
    for line in lines:
        if stripped := line.strip():
            yield json.loads(stripped)

records = list(parse_jsonl(['{"id": 1}', '', '{"id": 2}']))
print(records)  # 输出: [{'id': 1}, {'id': 2}]
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么 RAG 数据准备常使用 JSONL？**

**参考答案：**每行可独立解析，便于流式处理、增量追加、定位坏数据和分片；相比一个巨大 JSON 数组，读取单条记录不需要先把整个文件载入内存。

### 相关笔记（Related Notes）
- [[04-文件、路径、模块与包（Files Paths Modules and Packages）]]
- [[02-Pandas 数据处理（Pandas）]]

## 5. HTTP、超时、幂等与退避（HTTP, Timeouts, Idempotency, and Backoff）
### 概念与原理（Concept and Mechanism）
- HTTP 请求由方法（Method）、URL、Header 和可选 Body 组成，响应包含状态码、Header 和 Body。`2xx` 表示成功类别，`4xx` 表示请求或权限问题，`5xx` 表示服务器端失败，但业务仍需按具体状态码处理。
- 连接超时（Connect Timeout）限制建立连接的等待，读取超时（Read Timeout）限制等待响应数据的时间。
- 幂等（Idempotency）表示同一操作执行一次或多次对最终状态的影响相同。重试非幂等写操作必须使用幂等键或去重机制。

### 最小代码示例（Minimal Example）
```python
import httpx

with httpx.Client(timeout=httpx.Timeout(10.0, connect=3.0)) as client:
    response = client.get("https://example.com/api/items")
    response.raise_for_status()
```
该示例会访问外部网络，输出依赖服务状态。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：遇到 `429 Too Many Requests` 应如何处理？**

**参考答案：**先读取服务端提供的 `Retry-After` 或限流信息，在允许重试时采用有上限的指数退避（Exponential Backoff）和随机抖动（Jitter），同时限制客户端并发。不能立即无限重试，否则会进一步加重限流。

### 相关笔记（Related Notes）
- [[04-HTTP 请求与反爬处理（HTTP Requests and Anti-scraping）]]

## 6. 协程、事件循环与并发限制（Coroutines, Event Loop, and Concurrency Limits）
### 概念与原理（Concept and Mechanism）
- 并发（Concurrency）是多个任务在时间上交错推进，并行（Parallelism）是多个任务在同一时刻实际执行。
- 协程（Coroutine）在 `await` 可等待操作处主动让出控制权；事件循环（Event Loop）调度其他就绪任务。异步适合大量等待型 I/O，不会自动加速 CPU 密集计算。
- 超时、取消、并发上限和部分失败处理是异步系统正确性的一部分。

### 最小代码示例（Minimal Example）
```python
import asyncio

async def limited_work(item: int, semaphore: asyncio.Semaphore) -> int:
    async with semaphore:
        await asyncio.sleep(0.01)
        return item * 2

async def main() -> None:
    semaphore = asyncio.Semaphore(2)
    results = await asyncio.gather(*(limited_work(i, semaphore) for i in range(3)))
    print(results)  # 输出: [0, 2, 4]

asyncio.run(main())
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么在 `async def` 中调用阻塞函数会影响所有请求？**

**参考答案：**事件循环通常运行在单个线程中；阻塞调用不让出控制权，其他协程即使已经就绪也无法被调度。应使用异步客户端，或把无法替换的阻塞 I/O 放入受控线程池；CPU 密集任务应考虑进程池或独立任务服务。

### 相关笔记（Related Notes）
- [[07-Python 并发与网络编程（Python Concurrency and Networking）]]

## 7. 测试、Mock、调试与 Git（Testing, Mocking, Debugging, and Git）
### 概念与原理（Concept and Mechanism）
- 单元测试（Unit Test）隔离验证小范围逻辑；集成测试（Integration Test）验证多个真实组件协作；端到端测试（End-to-end Test）验证完整用户流程。
- Mock 应替换真正的系统边界，例如模型供应商客户端，而不是把被测函数内部每一步都伪造掉。
- 调试先稳定复现，再缩小输入和调用范围，最后依据 traceback、日志和断点验证假设。
- Git commit 应形成可理解、可审查、可回滚的单一改动。

### 最小代码示例（Minimal Example）
```python
def normalize_query(query: str) -> str:
    return " ".join(query.strip().split())

def test_normalize_query() -> None:
    assert normalize_query("  vector   search ") == "vector search"
```
该示例由 `pytest` 运行；测试通过时默认只显示测试摘要，具体格式取决于 pytest 版本和参数。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么测试中不能只断言 HTTP 状态码是 200？**

**参考答案：**状态码只能证明请求被当作成功处理，不能证明返回 Schema、业务数据、权限隔离和副作用正确。还应断言响应结构、关键字段、数据库状态以及错误路径。

## 8. 复杂度与高频数据结构（Complexity and Common Data Structures）
### 概念与原理（Concept and Mechanism）
- 时间复杂度（Time Complexity）描述输入规模增长时操作次数的数量级；空间复杂度（Space Complexity）描述额外内存增长量。
- 哈希表适合平均常数时间查找，栈适合后进先出状态，队列适合先进先出处理，堆适合动态维护最值，图搜索适合关系网络。
- 面试不仅要给出复杂度，还要解释不变量（Invariant）、边界条件和为什么算法会终止。

### 最小代码示例（Minimal Example）
```python
from collections import Counter

def first_unique(values: list[str]) -> str | None:
    counts = Counter(values)
    return next((value for value in values if counts[value] == 1), None)

print(first_unique(["a", "b", "a", "c"]))  # 输出: b
```
该算法遍历输入两次，时间复杂度为 $O(n)$，哈希计数额外空间复杂度为 $O(n)$。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么哈希表查找通常说是 $O(1)$，而不是绝对保证 $O(1)$？**

**参考答案：**平均情况下哈希函数把键分散到不同槽位，可常数次定位；大量冲突、扩容或恶意输入会增加代价，因此复杂度取决于实现和输入分布。

### 相关笔记（Related Notes）
- [[01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）]]
- [[02-二分查找与边界搜索（Binary Search and Boundary Queries）]]
- [[09-哈希表与排序算法（Hash Tables and Sorting Algorithms）]]
- [[10-图结构、遍历与最短路径（Graphs, Traversal, and Shortest Paths）]]
- [[11-贪心、动态规划与分治（Greedy, Dynamic Programming, and Divide and Conquer）]]

## 9. 文本处理 API 的面试表达（Text-processing API Interview Framing）
- **问题（Problem）**：统一接收 TXT、JSONL 与 CSV，完成清洗、去重和统计，同时对坏编码、空文件和超大文件给出可诊断错误。
- **关键设计（Key Design）**：上传层限制大小和类型；解析层按格式分派；清洗层保持纯函数；统计层输出 Pydantic Schema；日志只记录元数据和错误类型。
- **测试重点（Test Focus）**：正常文件、空文件、编码错误、异常行、重复记录、超限文件、并发上传与外部依赖失败。
- **高频追问（Common Follow-up）**：哪些操作会阻塞事件循环？文件读取、Pandas 清洗和 CPU 密集统计都可能阻塞；应根据规模选择线程池、进程池、流式处理或后台任务。

## 参考资料（References）
- [[大模型应用工程师学习计划]]
- [[02-FastAPI 机器学习推理服务模板（FastAPI ML Inference Service Template）]]
