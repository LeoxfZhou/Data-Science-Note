---
title: Python 并发与网络编程（Python Concurrency and Networking）
aliases:
  - Python Concurrency and Networking
  - Python 进程线程与 Socket
status: published
detail_level: comprehensive
merge_policy: union-zero-loss
published_at: 2026-08-17
updated_at: 2026-08-17
---
# Python 并发与网络编程（Python Concurrency and Networking）
## 1. 并发、并行、进程与线程（Concurrency, Parallelism, Processes, and Threads）
### 1.1 并发与并行（Concurrency and Parallelism）
- **并发（Concurrency）**：多个任务在一段时间内交错推进，重点是任务调度与结构；单核也能并发。
- **并行（Parallelism）**：多个任务在同一时刻真正执行，通常需要多个 CPU 核心、多个进程或其他并行硬件。
- 并发不保证程序更快。创建执行单元、切换上下文、同步和通信都会产生开销。
> [!tip] 大白话理解（Plain-language Intuition）
> 并发像一个人轮流处理多件事，等待某件事时先做另一件；并行像多个人同时做不同任务。任务太小时，协调成本可能比真正工作还高。
### 1.2 进程与线程对比（Process vs. Thread）

|维度（Dimension）|进程（Process）|线程（Thread）|
|---|---|---|
|内存|通常拥有独立地址空间|共享所属进程的大部分内存|
|隔离|较强；单个子进程崩溃通常不直接破坏其他进程内存|较弱；错误共享状态可能影响整个进程|
|通信|需要队列、管道、共享内存等进程间通信（Inter-process Communication, IPC）|可直接共享对象，但必须防范竞态条件（Race Condition）|
|创建与切换成本|通常较高|通常较低|
|常见场景|CPU 密集型任务、需要隔离的任务|I/O 密集型任务、需要共享状态的任务|

CPython 的全局解释器锁（Global Interpreter Lock, GIL）使同一进程中通常只有一个线程执行 Python 字节码。因此：
- I/O 等待期间线程可以切换，网络、磁盘等 I/O 密集型任务常能从多线程受益。
- 纯 Python CPU 密集型任务通常不能靠多线程获得多核并行，常使用多进程；释放 GIL 的本地扩展是例外。
## 2. 多进程（Multiprocessing）
### 2.1 `multiprocessing.Process`
`Process(target=..., args=..., kwargs=...)` 创建子进程：
- **`target`**：子进程执行的可调用对象。
- **`args`**：按位置传参的元组；单个参数必须写成 `(value,)`。
- **`kwargs`**：按名称传参的字典。
- `start()` 启动子进程；`join()` 等待子进程结束并回收其进程状态。

```python
from multiprocessing import Process
import time

def code(name: str, count: int) -> None:
    for index in range(count):
        time.sleep(0.1)
        print(f"{name} 正在编写第 {index + 1} 行代码")

def listen(name: str, count: int) -> None:
    for index in range(count):
        time.sleep(0.1)
        print(f"{name} 正在听第 {index + 1} 首歌")

if __name__ == "__main__":
    # Windows 和 macOS 常使用 spawn；入口保护可避免子进程重新导入模块时无限创建进程。
    process_code = Process(target=code, args=("乔峰", 2))
    process_music = Process(target=listen, kwargs={"name": "虚竹", "count": 2})
    process_code.start()
    process_music.start()
    process_code.join()
    process_music.join()

# 输出包含两类各 2 行消息；具体交错顺序由操作系统调度决定。
```
### 2.2 进程数据与失败处理（Process Data and Failures）
- 普通 Python 对象不会自动在进程间保持同步；应使用 `multiprocessing.Queue`、`Pipe`、共享内存或高层执行器传递结果。
- 传给子进程的对象通常需要可序列化；大型对象反复序列化会显著增加开销。
- `join()` 后检查 `exitcode`；长期任务还应设计超时、取消和异常回传。
## 3. 多线程（Multithreading）
### 3.1 `threading.Thread`
`Thread` 的 `target`、`args` 和 `kwargs` 与 `Process` 类似。线程共享进程内对象，因此写共享数据时需要锁（Lock）、线程安全队列或不变数据结构。

```python
from threading import Thread
import time

def work(name: str, count: int) -> None:
    for index in range(count):
        time.sleep(0.1)  # 模拟 I/O 等待；等待期间其他线程可继续推进。
        print(f"{name}: {index + 1}")

thread_a = Thread(target=work, args=("下载 A", 2))
thread_b = Thread(target=work, kwargs={"name": "下载 B", "count": 2})
thread_a.start()
thread_b.start()
thread_a.join()
thread_b.join()

# 输出包含 A、B 各 2 行；具体交错顺序不固定。
```
### 3.2 竞态条件与同步（Race Conditions and Synchronization）
- “读取 → 修改 → 写回”不是天然原子操作；多个线程交错执行可能丢失更新。
- `threading.Lock` 保护必须保持一致的临界区（Critical Section），但锁范围过大又会降低并发度。
- 优先用 `queue.Queue` 在线程之间传递任务，减少直接共享可变状态。
## 4. TCP Socket 基础（TCP Socket Fundamentals）
### 4.1 通信模型（Communication Model）
套接字（Socket）由协议族、传输协议和端点共同确定。本节使用：
- `socket.AF_INET`：IPv4。
- `socket.SOCK_STREAM`：TCP 字节流。
- IP 地址定位主机，端口号（Port）定位主机上的服务进程。

> [!example]- TCP 客户端与服务器通信图（TCP Client-server Diagram）
> ![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/01-基础与标准库（Fundamentals and Standard Library）/07-Python 并发与网络编程（Python Concurrency and Networking）/07-Python 并发与网络编程（Python Concurrency and Networking）-1742548401491.png]]

TCP 提供可靠、有序的字节流，但不保留应用消息边界。一次 `sendall()` 的数据可能被多次 `recv()` 收到，多次发送也可能被一次读取；真实协议必须使用长度前缀、分隔符、固定长度或连接关闭来定义消息边界。
> [!tip] 大白话理解（Plain-language Intuition）
> TCP 像一条保证顺序和送达的水管，只保证字节按顺序流过，不会替应用标记“这一段是一条完整消息”。消息如何分段必须由客户端和服务器共同约定。
### 4.2 TCP 服务端流程（TCP Server Flow）
1. 创建服务器 Socket。
2. `bind()` 绑定监听地址和端口。
3. `listen()` 进入监听状态并设置等待队列上限。
4. `accept()` 等待连接，返回“专门与该客户端通信的 Socket”和客户端地址。
5. 使用 `recv()`/`sendall()` 收发字节。
6. 关闭已连接 Socket 和监听 Socket。

```python
import socket

HOST = "127.0.0.1"
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # 开发阶段重启服务时端口可能仍处于等待状态；SO_REUSEADDR 可减少“地址已占用”等待。
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    connection, client_address = server.accept()
    with connection:
        data = connection.recv(1024)
        if data:
            message = data.decode("utf-8")
            print(f"服务器收到：{message}")
            connection.sendall("欢迎来到 Socket 的世界".encode("utf-8"))

# 该示例会绑定本机端口并阻塞等待客户端，控制台输出取决于收到的网络消息。
```
### 4.3 TCP 客户端流程（TCP Client Flow）
1. 创建客户端 Socket。
2. `connect()` 连接服务器 IP 和端口。
3. `sendall()` 发送编码后的字节。
4. `recv()` 接收回执并按约定编码解码。
5. 关闭 Socket。

```python
import socket

HOST = "127.0.0.1"
PORT = 12345

with socket.create_connection((HOST, PORT), timeout=3) as client:
    client.sendall("你好服务器端，我是客户端".encode("utf-8"))
    reply = client.recv(1024).decode("utf-8")
    print(f"客户端收到：{reply}")

# 该示例需要先启动上面的服务端，输出取决于服务端回执。
```
### 4.4 常见错误（Common Errors）
- `ConnectionRefusedError`：目标地址没有服务监听，或端口填写错误。
- `OSError: Address already in use`：端口被其他进程占用，或服务刚退出仍处于 TCP 状态转换。
- `socket.timeout`：对端没有在超时时间内响应；生产代码必须处理超时，避免永久阻塞。
- `UnicodeDecodeError`：两端编码约定不一致，或收到的不是完整文本帧。
- `recv()` 返回 `b""`：对端已经正常关闭连接。
## 5. 选择建议（Selection Guide）

|任务（Task）|优先方案|原因|
|---|---|---|
|大量网络/磁盘等待|线程池或异步 I/O|等待期间可切换其他任务|
|纯 Python CPU 密集计算|多进程|绕过单进程 GIL 并利用多核|
|强隔离任务|多进程|地址空间独立，故障边界更清楚|
|少量简单并发|高层执行器|比手动管理线程/进程更容易处理结果和异常|
## 6. 完成检查（Checklist）
- [ ] 能区分并发与并行，以及进程和线程的数据边界。
- [ ] 能解释 GIL 对 CPU 密集型和 I/O 密集型线程的不同影响。
- [ ] 能使用 `args`、`kwargs`、`start()` 和 `join()` 创建进程与线程。
- [ ] 能写出单连接 TCP 客户端/服务端，并解释 `accept()` 返回的两个对象。
- [ ] 知道 TCP 没有消息边界，并能处理超时、断线和空字节串。
