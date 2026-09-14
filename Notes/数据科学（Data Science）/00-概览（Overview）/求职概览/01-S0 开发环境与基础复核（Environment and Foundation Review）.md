---
title: "S0 开发环境与基础复核（Environment and Foundation Review）"
aliases:
  - "S0 Environment and Foundation Review"
tags:
  - career/llm-application-engineer
  - interview/foundation
status: published
created: 2026-08-27
updated: 2026-08-27
---
# S0 开发环境与基础复核（Environment and Foundation Review）
> [!tip] 导航（Navigation）
> [[00-概览（Overview）]]｜[[大模型应用工程师学习计划]]｜下一阶段：[[02-S1 Python 工程与基础算法（Python Engineering and Algorithms）]]
## 1. Python 解释器、虚拟环境与依赖（Interpreter, Virtual Environment, and Dependencies）
### 概念与原理（Concept and Mechanism）
- Python 解释器（Python Interpreter）负责执行代码；虚拟环境（Virtual Environment）为项目提供独立的解释器入口与第三方包目录；依赖清单（Dependency Manifest）记录项目需要哪些包和版本。
- 虚拟环境解决“项目 A 与项目 B 依赖版本冲突”，锁定文件解决“同一项目在不同机器安装出不同依赖集合”。仅创建虚拟环境但不记录版本，仍不能保证复现。

> [!tip] 大白话理解（Plain-language Intuition）
> 解释器像厨房，虚拟环境像每个项目自己的储物柜，锁定文件则是精确采购清单。只有三者都明确，别人才能做出同一道菜。

### 使用场景与最小示例（Scenario and Minimal Example）
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -c "import sys; print(sys.executable)"
```
上述命令会创建目录并安装依赖，属于文件与网络副作用；解释器路径取决于当前项目位置。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：虚拟环境和 Docker 有什么区别？**

**参考答案：**虚拟环境只隔离 Python 包和解释器入口，不隔离操作系统库、进程、网络或文件系统；Docker 容器（Container）基于镜像（Image）封装应用及系统级依赖，隔离边界更完整，但构建和运行成本也更高。开发阶段常同时使用两者：本地虚拟环境提高迭代速度，容器保证交付环境一致。

**问题：为什么不建议只提交 `pip freeze` 的结果？**

**参考答案：**`pip freeze` 会记录当前环境中的全部直接和间接依赖，可能混入无关包，也不能表达哪些是直接依赖。更可靠的方式是维护直接依赖清单，并使用锁定工具解析和固定完整依赖图。

### 相关笔记（Related Notes）
- [[01-Python 环境配置（Environment Setup）]]
- [[04-文件、路径、模块与包（Files Paths Modules and Packages）]]

## 2. PyTorch 设备、驱动与 CUDA（PyTorch Device, Driver, and CUDA）
### 概念与原理（Concept and Mechanism）
- `torch.device` 决定张量（Tensor）和模型在哪个计算设备上执行；参与同一次运算的张量通常必须位于兼容设备。
- NVIDIA 驱动（NVIDIA Driver）负责操作系统与 GPU 通信；CUDA 运行时（CUDA Runtime）提供 GPU 计算库；PyTorch 安装包需要与驱动能力和平台兼容。系统安装了 CUDA Toolkit，不代表当前 PyTorch 构建一定支持 CUDA。

### 最小代码示例（Minimal Example）
```python
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tensor = torch.tensor([1.0, 2.0], device=device)
print(device.type in {"cpu", "cuda", "mps"})  # 输出: True
print(tensor.device.type == device.type)         # 输出: True
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么明明有 GPU，`torch.cuda.is_available()` 仍可能是 `False`？**

**参考答案：**常见原因包括安装了 CPU 版 PyTorch、驱动不兼容、容器没有透传 GPU、当前平台不是 CUDA 平台、环境变量或动态库加载失败。排查时应分别确认硬件与驱动、PyTorch 构建信息、容器运行参数和实际解释器环境，不能只看是否安装了 CUDA Toolkit。

### 相关笔记（Related Notes）
- [[01-PyTorch 张量基础（PyTorch Tensor Fundamentals）]]
- [[05-远程 GPU 服务器与 Linux 基础（Remote GPU Server and Linux Basics）]]

## 3. 性能计时与基准测试（Timing and Benchmarking）
### 概念与原理（Concept and Mechanism）
- 短代码计时优先使用单调时钟（Monotonic Clock），例如 `time.perf_counter()`，避免系统时间校准造成倒退。
- 首次运行可能包含导入、内核编译、缓存填充和内存分配，因此需要预热（Warm-up）；GPU 操作通常异步提交，计时前后需要同步，否则测到的主要是任务提交时间。
- 单次测量受调度、缓存和后台任务影响，应重复多次报告中位数或分位数。

### 最小代码示例（Minimal Example）
```python
from statistics import median
from time import perf_counter

durations = []
for _ in range(5):
    started_at = perf_counter()
    sum(range(10_000))
    durations.append((perf_counter() - started_at) * 1_000)

print(len(durations))               # 输出: 5
print(median(durations) >= 0.0)     # 输出: True
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么 GPU 计时前后要调用同步操作？**

**参考答案：**CPU 通常只把 GPU 内核放入执行队列便立即返回。如果不等待队列完成，结束时间早于真实计算完成时间，得到的是提交延迟而不是执行延迟。同步会让 CPU 等待 GPU 完成本轮任务，从而测到实际耗时。

## 4. 项目复现、入口与敏感信息（Reproducibility, Entry Point, and Secrets）
### 概念与原理（Concept and Mechanism）
- 可复现项目至少说明环境、依赖、启动命令、输入、输出、配置、数据来源和常见失败方式。
- 程序入口（Entry Point）负责组装依赖和启动主流程，业务逻辑应放在可导入、可测试的函数或类中。
- 密钥、账号、本机绝对路径和私人数据不属于源代码配置，应通过环境变量或本地配置注入，并由 `.gitignore` 排除。

### 最小代码示例（Minimal Example）
```python
import os

api_key = os.getenv("MODEL_API_KEY")
if not api_key:
    raise RuntimeError("缺少 MODEL_API_KEY 环境变量")
```
该示例依赖外部环境变量；不要为了让程序启动而在代码中写入真实密钥。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：`.env` 文件是否安全？**

**参考答案：**`.env` 只是方便本地注入配置，不是安全存储系统。它必须被 Git 忽略、限制文件权限，并避免进入镜像和日志；生产环境应使用部署平台或专门的密钥管理服务注入敏感值。

## 5. 网络采集的可靠性与合规边界（Reliable and Compliant Data Collection）
### 概念与原理（Concept and Mechanism）
- 超时（Timeout）限制单次等待；有限重试（Bounded Retry）只处理短暂故障；请求间隔和并发上限减少对对方服务的压力。
- `User-Agent` 用于标识客户端，但不能赋予访问权限。登录、验证码、付费墙和访问控制属于安全边界，不能通过技术手段规避。

### 最小代码示例（Minimal Example）
```python
import requests

response = requests.get(
    "https://example.com/data.json",
    headers={"User-Agent": "learning-client/1.0"},
    timeout=(3.0, 10.0),  # 分别限制连接和读取等待时间，避免请求无限挂起。
)
response.raise_for_status()
```
该示例会发起网络请求，响应状态和内容取决于外部服务。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：所有网络错误都应该重试吗？**

**参考答案：**不应该。连接中断、部分超时或某些 `5xx` 可能是短暂故障；`401` 通常需要修正凭据，`403` 表示权限拒绝，参数校验失败也不会因重试而恢复。重试还必须考虑请求是否幂等，并设置次数、退避和总时间上限。

### 相关笔记（Related Notes）
- [[04-HTTP 请求与反爬处理（HTTP Requests and Anti-scraping）]]

## 6. SQL、约束、索引与事务（SQL, Constraints, Indexes, and Transactions）
### 概念与原理（Concept and Mechanism）
- 主键（Primary Key）唯一标识记录；唯一约束（Unique Constraint）维护业务唯一性；外键（Foreign Key）维护表间引用关系。
- 索引（Index）以额外空间和写入成本换取特定查询的更快定位；索引必须围绕真实查询条件设计，不是越多越好。
- 事务（Transaction）把多步修改作为一个一致性单元提交或回滚。参数化查询把 SQL 结构与数据分开，可避免输入被解释成 SQL 语法。

### 最小代码示例（Minimal Example）
```python
import sqlite3

connection = sqlite3.connect(":memory:")
connection.execute("CREATE TABLE documents (id INTEGER PRIMARY KEY, source TEXT UNIQUE)")
connection.execute("INSERT INTO documents(source) VALUES (?)", ("manual.md",))
count = connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
print(count)  # 输出: 1
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么数据库去重不能只依赖应用层先查询再插入？**

**参考答案：**两个并发请求可能同时查询到“不存在”，随后都执行插入，形成竞态条件（Race Condition）。应由数据库唯一约束提供最终一致性保障，应用捕获冲突后执行幂等返回或更新逻辑。

### 相关笔记（Related Notes）
- [[06-爬虫数据存储：MySQL 与 Redis（Crawler Data Storage）]]

## 参考资料（References）
- [[大模型应用工程师学习计划]]
