---
title: "Python 并发与网络编程速查表（Python Concurrency and Network Programming Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - python/concurrency
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "Python 3.11–3.14；HTTP 客户端示例以 requests/httpx 当前稳定版为准"
---
# Python 并发与网络编程速查表（Python Concurrency and Network Programming Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
I/O 密集任务优先线程或 `asyncio`；CPU 密集任务优先多进程。网络调用必须设置超时、重试边界和凭据保护。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 线程与锁（Threading and Locks）
线程共享进程内存，适合阻塞型 I/O；共享可变状态必须同步。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建线程|`threading.Thread(target=fn, args=(x,))`|返回 Thread|
|启动线程|`thread.start()`|调度执行，返回 None|
|等待线程|`thread.join(timeout=None)`|等待结束，返回 None|
|互斥锁|`threading.Lock()`|返回非重入锁|
|重入锁|`threading.RLock()`|返回同线程可重复获取的锁|
|事件通知|`threading.Event()`|返回线程安全事件对象|
|信号量|`threading.Semaphore(value)`|限制并发进入数量|
|线程本地状态|`threading.local()`|返回线程独享属性容器|
|线程池|`ThreadPoolExecutor(max_workers=n)`|返回执行器|
|提交任务|`executor.submit(fn, *args)`|返回 Future|
|按完成顺序|`concurrent.futures.as_completed(futures)`|返回 Future 迭代器|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from concurrent.futures import ThreadPoolExecutor
def square(x: int) -> int:
    return x * x

with ThreadPoolExecutor(max_workers=2) as pool:
    print(list(pool.map(square, [1, 2, 3])))
# 期望输出:
# [1, 4, 9]
```
## 多进程（Multiprocessing）
进程隔离内存并绕过常规 CPython GIL 对 CPU 密集 Python 代码的限制，但有序列化开销。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建进程|`multiprocessing.Process(target=fn)`|返回 Process|
|启动进程|`process.start()`|启动子进程，返回 None|
|等待进程|`process.join()`|等待结束，返回 None|
|进程池|`ProcessPoolExecutor(max_workers=n)`|返回进程执行器|
|进程队列|`multiprocessing.Queue()`|返回跨进程队列|
|共享值|`multiprocessing.Value(typecode, value)`|返回同步共享标量|
|CPU 数量|`os.cpu_count()`|返回逻辑 CPU 数或 None|
|终止池|`executor.shutdown(wait=True, cancel_futures=False)`|释放工作进程|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from concurrent.futures import ProcessPoolExecutor
def cube(x: int) -> int:
    return x ** 3

# 脚本中应放在 if __name__ == "__main__" 保护下
# with ProcessPoolExecutor() as pool:
#     print(list(pool.map(cube, [1, 2, 3])))
print([cube(x) for x in [1, 2, 3]])
# 期望输出:
# [1, 8, 27]
```
## asyncio 协程（Asyncio Coroutines）
协程在等待 I/O 时主动让出控制权；不要在事件循环中执行阻塞调用。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|运行入口|`asyncio.run(main())`|创建事件循环并返回 main 的结果|
|创建任务|`asyncio.create_task(coro)`|返回已调度 Task|
|并发等待|`await asyncio.gather(*aws)`|按输入顺序返回结果列表|
|按完成等待|`asyncio.as_completed(aws)`|返回可等待对象迭代器|
|超时上下文|`asyncio.timeout(seconds)`|超时抛 TimeoutError|
|休眠让权|`await asyncio.sleep(delay)`|暂停当前任务并返回 None|
|异步队列|`asyncio.Queue(maxsize=0)`|返回协程安全队列|
|异步锁|`asyncio.Lock()`|返回事件循环内互斥锁|
|取消任务|`task.cancel()`|请求取消并返回布尔值|
|转移阻塞调用|`await asyncio.to_thread(fn, *args)`|在线程执行并返回结果|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import asyncio
async def work(x: int) -> int:
    await asyncio.sleep(0)
    return x * 2

async def main() -> None:
    print(await asyncio.gather(*(work(x) for x in range(3))))

asyncio.run(main())
# 期望输出:
# [0, 2, 4]
```
## HTTP 客户端（HTTP Clients）
请求必须设置连接和读取超时；状态码、内容类型和响应体共同决定是否成功。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|GET 请求|`requests.get(url, params=params, timeout=(3.05, 30))`|返回 Response，有网络副作用|
|POST JSON|`requests.post(url, json=payload, timeout=30)`|返回 Response，有网络副作用|
|复用会话|`requests.Session()`|返回连接复用会话|
|状态检查|`response.raise_for_status()`|4xx/5xx 抛 HTTPError，否则返回 None|
|解析 JSON|`response.json()`|返回 Python 对象；非法 JSON 抛解码异常|
|流式下载|`requests.get(url, stream=True, timeout=...)`|Response 按块读取，必须关闭|
|异步客户端|`httpx.AsyncClient(timeout=...)`|返回异步客户端上下文|
|异步请求|`await client.get(url)`|返回 httpx.Response|
|请求头|`headers={'Authorization': f'Bearer {token}'}`|随请求发送；令牌不得写入日志或 Git|
|重试|`urllib3.util.Retry(...)`|定义可重试状态、次数和退避策略|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import os, requests

url = "https://api.example.com/items"
token = os.environ["API_TOKEN"]
response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=(3.05, 30))
response.raise_for_status()
data = response.json()
# 网络请求有外部副作用，输出取决于服务端。
```
## Socket 与协议边界（Sockets and Protocol Boundaries）
Socket 是字节流或数据报接口；应用层必须自行定义消息边界、编码和最大尺寸。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建 TCP socket|`socket.socket(socket.AF_INET, socket.SOCK_STREAM)`|返回 socket|
|设置超时|`sock.settimeout(seconds)`|原地设置，返回 None|
|连接服务端|`sock.connect((host, port))`|建立连接，返回 None|
|发送完整缓冲|`sock.sendall(data)`|发送 bytes，成功返回 None|
|接收字节|`sock.recv(bufsize)`|返回 bytes；空 bytes 表示对端关闭|
|绑定地址|`sock.bind((host, port))`|绑定本地地址，返回 None|
|监听|`sock.listen(backlog)`|进入监听状态，返回 None|
|接受连接|`sock.accept()`|返回 (connection, address)|
|主机名解析|`socket.getaddrinfo(host, port)`|返回候选地址列表|
|TLS 包装|`ssl.create_default_context().wrap_socket(...)`|返回验证证书的 TLS socket|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import socket
left, right = socket.socketpair()
try:
    left.sendall("你好".encode("utf-8"))
    print(right.recv(32).decode("utf-8"))
finally:
    left.close(); right.close()
# 期望输出:
# 你好
```
## 队列、背压与可靠性（Queues, Backpressure, and Reliability）
有限队列形成背压；生产者、消费者与关闭信号必须有明确协议。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|线程安全队列|`queue.Queue(maxsize=n)`|返回有界或无界队列|
|加入任务|`q.put(item, timeout=seconds)`|入队，满且超时抛 Full|
|读取任务|`q.get(timeout=seconds)`|移除并返回，空且超时抛 Empty|
|任务完成|`q.task_done()`|减少未完成计数，错误调用抛 ValueError|
|等待清空|`q.join()`|等待所有任务完成|
|异步入队|`await async_q.put(item)`|队满时挂起|
|异步出队|`await async_q.get()`|队空时挂起|
|完成回调|`future.add_done_callback(fn)`|注册 Future 完成回调|
|检查异常|`future.exception()`|返回异常或 None；未完成时抛 InvalidStateError|
|取消未开始任务|`future.cancel()`|成功取消返回 True|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from queue import Queue
q: Queue[int | None] = Queue(maxsize=2)
q.put(1); q.put(2)
print(q.get(), q.qsize())
q.task_done()
# 期望输出:
# 1 1
```
## 高频工作模式（Common Workflows）
- **最小闭环（Minimum Loop）**：先用最小输入跑通读取、转换、验证与输出，再替换真实数据。
- **组合优先（Composition First）**：把解析、业务逻辑和 I/O 分层，便于单元测试和复用。
- **可观测性（Observability）**：在边界处记录输入规模、关键参数、耗时和异常，不记录凭据。
- **可复现性（Reproducibility）**：固定随机种子、依赖版本和配置，并保存数据与模型版本。
## 常见错误与排查（Common Errors and Troubleshooting）
- **类型或形状不匹配**：先打印 `type`、`dtype`、`shape`，再检查广播、索引和设备。
- **隐式修改**：链式操作前确认是否原地修改；必要时显式复制并写测试。
- **边界遗漏**：至少覆盖空输入、单元素、重复值、极端值和非法参数。
- **版本漂移**：遇到弃用警告时查询当前官方迁移说明，不长期屏蔽警告。
## 相关详细笔记（Detailed Notes）
- [[01-Python 环境配置（Environment Setup）]]
- [[02-Python 基础语法（Python Basics）]]
- [[03-错误与异常（Errors and Exceptions）]]
- [[04-文件、路径、模块与包（Files Paths Modules and Packages）]]
- [[05-面向对象编程（Object-Oriented Programming）]]
- [[06-正则表达式（Regular Expressions）]]
- [[07-Python 并发与网络编程（Python Concurrency and Networking）]]
- [[01-Python 爬虫前置基础（Python Prerequisites for Web Scraping）]]
- [[02-HTML 与 CSS 页面结构（HTML and CSS Page Structure）]]
- [[03-网页解析：正则、XPath 与 Beautiful Soup（Web Parsing）]]
- [[04-HTTP 请求与反爬处理（HTTP Requests and Anti-scraping）]]
- [[05-Selenium 浏览器自动化（Selenium Browser Automation）]]
- [[06-爬虫数据存储：MySQL 与 Redis（Crawler Data Storage）]]
- [[07-Scrapy 与 Scrapy-Redis 框架（Scrapy and Scrapy-Redis Frameworks）]]
- [[08-逆向分析与加密基础（Reverse Engineering and Cryptography Basics）]]
## 官方参考（Official References）
- [Python 3 文档](https://docs.python.org/3/)
