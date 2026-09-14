---
title: "Python 标准库与工程工具速查表（Python Standard Library and Engineering Tools Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - python/standard-library
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "Python 3.11–3.14"
---
# Python 标准库与工程工具速查表（Python Standard Library and Engineering Tools Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
本页的 `os`、`sys`、`pathlib`、`json`、`csv`、`logging`、`argparse`、`subprocess`、`tempfile`、`shutil`、`datetime`、`collections`、`itertools`、`functools`、`statistics`、`sqlite3` 等均属于 Python 标准库（Standard Library）：随 Python 提供，无独立 PyPI 安装包，也不应执行同名 `pip install`。第三方工程工具集中列在 [[02-Python 项目结构、配置、日志与 pytest 速查表（Python Project Structure, Configuration, Logging, and pytest）]]。
### JupyterLab 与 IPython Kernel（JupyterLab and IPython Kernel）
- **安装包（Distribution）**：`jupyterlab`、`ipykernel`。
- **导入模块（Import Module）**：`jupyterlab`、`ipykernel`；通常通过 CLI 启动而非在业务代码中导入。
- **安装命令（Installation）**：`python -m pip install -U jupyterlab ipykernel`。
- **用途（Purpose）**：JupyterLab 提供交互式开发界面，IPython Kernel 把当前 Python 环境注册为 Notebook 内核。
- **正式笔记（Detailed Note）**：[[01-Python 环境配置（Environment Setup）]]。

|功能（Operation）|实际写法（Usage）|返回值与状态变化|
|---|---|---|
|启动 JupyterLab|`python -m jupyter lab`|启动本地 Web 服务并持续占用进程|
|注册内核|`python -m ipykernel install --user --name NAME --display-name LABEL`|写用户级 kernelspec|
|列出内核|`python -m jupyter kernelspec list`|输出可选内核与目录|
|删除内核|`python -m jupyter kernelspec uninstall NAME`|删除 kernelspec；不删除虚拟环境|

```bash
python -m ipykernel install --user --name ds-env --display-name "Python (ds-env)"
python -m jupyter lab
# 第一条写入用户级 kernelspec；第二条启动本地常驻 Web 服务。
```
- **环境边界（Environment Boundary）**：必须在目标虚拟环境中执行 `python -m ipykernel install`；用 `sys.executable` 核对 Notebook 当前解释器，避免“终端已安装但 Notebook 导入失败”。
以下模块随 Python 安装：`pathlib`、`collections`、`itertools`、`functools`、`datetime`、`json`、`re`、`logging`、`argparse` 与 `typing`。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 路径与文件系统（pathlib and Filesystem）
`pathlib.Path` 用对象表达路径；跨平台代码避免手工拼接分隔符。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建路径|`Path('data') / 'raw.csv'`|返回新 Path|
|解析绝对路径|`path.resolve()`|返回解析后的绝对 Path|
|判断存在|`path.exists()`|返回布尔值|
|判断文件|`path.is_file()`|返回布尔值|
|创建目录|`path.mkdir(parents=True, exist_ok=True)`|创建目录，返回 None|
|读取文本|`path.read_text(encoding='utf-8')`|返回 str|
|写入文本|`path.write_text(text, encoding='utf-8')`|覆盖写入并返回字符数，有外部副作用|
|枚举直接子项|`path.iterdir()`|返回迭代器|
|递归匹配|`path.rglob('*.csv')`|返回 Path 迭代器|
|改名或移动|`path.rename(target)`|返回新 Path，有外部副作用|
|文件元数据|`path.stat()`|返回 os.stat_result|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from pathlib import PurePosixPath
path = PurePosixPath("data") / "raw" / "sample.csv"
print(path.name, path.suffix, path.parent)
# 期望输出:
# sample.csv .csv data/raw
```
## 常用容器（collections）
标准库容器提供计数、默认值、双端操作和字段化元组。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|频次统计|`Counter(items)`|返回 Counter 映射|
|最高频项|`counter.most_common(n)`|返回 (元素, 次数) 列表|
|默认容器|`defaultdict(list)`|缺键时创建默认值并写入映射|
|双端队列|`deque(iterable, maxlen=None)`|返回 deque|
|左端加入|`queue.appendleft(x)`|原地修改，返回 None|
|两端弹出|`queue.popleft() / queue.pop()`|移除并返回元素；空队列抛 IndexError|
|固定字段元组|`namedtuple('Point', 'x y')`|返回元组子类|
|映射叠加|`ChainMap(primary, fallback)`|返回按顺序查找的视图|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from collections import Counter, deque
counts = Counter("banana")
queue = deque([1, 2])
queue.appendleft(0)
print(counts.most_common(2))
print(queue.popleft(), list(queue))
# 期望输出:
# [('a', 3), ('n', 2)]
# 0 [1, 2]
```
## 迭代组合（itertools and functools）
组合迭代器避免一次性物化大数据；缓存和归约用于复用计算。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|连续计数|`itertools.count(start=0, step=1)`|返回无限迭代器|
|重复值|`itertools.repeat(obj, times=None)`|返回有限或无限迭代器|
|连接迭代器|`itertools.chain(a, b)`|惰性依次产出|
|组合|`itertools.combinations(items, r)`|返回无重复位置组合|
|排列|`itertools.permutations(items, r=None)`|返回位置排列|
|笛卡尔积|`itertools.product(a, b, repeat=1)`|返回元组迭代器|
|按相邻键分组|`itertools.groupby(items, key=...)`|返回键与组迭代器；通常先排序|
|累计|`itertools.accumulate(items, func=operator.add)`|返回累计结果迭代器|
|函数缓存|`functools.lru_cache(maxsize=128)`|装饰函数并缓存参数到结果|
|偏函数|`functools.partial(fn, preset)`|返回预绑定参数的新可调用对象|
|归约|`functools.reduce(fn, items, initial)`|返回单个累计结果|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from functools import lru_cache
from itertools import combinations
@lru_cache(maxsize=None)
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(list(combinations("ABC", 2)))
print(fib(10), fib.cache_info().hits)
# 期望输出:
# [('A', 'B'), ('A', 'C'), ('B', 'C')]
# 55 8
```
## 日期、JSON、CSV 与正则（Serialization and Text）
序列化前明确时区、编码、缺失值与 schema。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|当前 UTC|`datetime.now(timezone.utc)`|返回带时区 datetime|
|解析 ISO 时间|`datetime.fromisoformat(text)`|返回 datetime；格式非法抛 ValueError|
|时间差|`end - start`|返回 timedelta|
|JSON 编码|`json.dumps(obj, ensure_ascii=False)`|返回 JSON 字符串|
|JSON 解码|`json.loads(text)`|返回 Python 对象；非法 JSON 抛 JSONDecodeError|
|JSON 文件读取|`json.load(file)`|从文本流返回 Python 对象|
|CSV 字典读取|`csv.DictReader(file)`|逐行返回字符串字典|
|CSV 字典写入|`csv.DictWriter(file, fieldnames=...)`|返回写入器，有外部副作用|
|正则查找首项|`re.search(pattern, text)`|返回 Match 或 None|
|正则全部匹配|`re.findall(pattern, text)`|返回字符串或元组列表|
|正则替换|`re.sub(pattern, repl, text)`|返回新字符串|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import json, re
from datetime import datetime, timezone
record = {"name": "测试", "at": datetime(2026, 1, 1, tzinfo=timezone.utc).isoformat()}
text = json.dumps(record, ensure_ascii=False)
print(json.loads(text)["name"])
print(re.findall(r"\d+", "v2 has 14 items"))
# 期望输出:
# 测试
# ['2', '14']
```
## 日志、命令行与配置（Logging, CLI, and Configuration）
命令行参数承载显式配置；日志用于诊断，不得记录密码或令牌。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建记录器|`logging.getLogger(__name__)`|返回 Logger|
|基础配置|`logging.basicConfig(level=logging.INFO)`|配置根记录器，通常仅入口调用|
|带参数日志|`logger.info('rows=%d', rows)`|延迟格式化并写日志|
|定义解析器|`argparse.ArgumentParser()`|返回参数解析器|
|位置参数|`parser.add_argument('input')`|注册必填参数，返回 Action|
|可选参数|`parser.add_argument('--epochs', type=int, default=10)`|注册带默认值参数|
|布尔开关|`parser.add_argument('--debug', action='store_true')`|出现时结果为 True|
|解析参数|`parser.parse_args()`|返回 Namespace；非法参数退出进程|
|环境变量|`os.getenv('APP_MODE', 'dev')`|返回字符串或默认值|
|类型别名|`type Row = dict[str, object]`|Python 3.12+ 创建类型别名|
|类型检查|`typing.get_type_hints(fn)`|返回解析后的注解字典|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--epochs", type=int, default=10)
args = parser.parse_args([])
print(args.epochs)
# 期望输出:
# 10
```
## 复制、随机、统计与测试辅助（Utility Modules）
注意浅复制、伪随机和统计函数的边界。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|浅复制|`copy.copy(obj)`|复制最外层，嵌套对象仍共享|
|深复制|`copy.deepcopy(obj)`|递归复制，返回独立对象|
|固定随机种子|`random.seed(42)`|重置模块级伪随机状态|
|随机抽样|`random.sample(population, k)`|无放回返回新列表；k 过大抛 ValueError|
|安全随机令牌|`secrets.token_urlsafe(nbytes)`|返回适合安全用途的字符串|
|均值|`statistics.mean(data)`|返回算术平均；空输入抛 StatisticsError|
|中位数|`statistics.median(data)`|返回中位数|
|临时目录|`tempfile.TemporaryDirectory()`|返回可清理的上下文管理器|
|对象序列化|`pickle.dumps(obj)`|返回 bytes；不得反序列化不可信数据|
|差异比较|`difflib.unified_diff(a, b)`|返回统一差异格式迭代器|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import random, statistics
random.seed(7)
values = random.sample(range(10), 4)
print(values)
print(statistics.mean([2, 4, 6]))
# 期望输出:
# [5, 2, 6, 9]
# 4
```
## Conda 环境与解释器核验（Conda Environments and Interpreter Verification）
Conda 环境（Conda Environment）是可复用的解释器与依赖集合，项目（Project）是代码、配置和数据的组织边界；二者不是同一个概念。一个项目通常固定使用一个环境，但多个项目可以共享环境，项目也可以为不同任务准备多个环境。

|功能（Operation）|实际写法（Command / Python Usage）|返回值与状态变化|
|---|---|---|
|查看环境|`conda env list`|列出环境；当前环境带 `*`|
|创建环境|`conda create -n ds python=3.11`|创建名为 `ds` 的隔离环境，有磁盘副作用|
|从文件创建|`conda env create -f environment.yml`|按声明创建环境，有磁盘与网络副作用|
|激活环境|`conda activate ds`|修改当前 Shell 的 PATH 与环境变量|
|退出环境|`conda deactivate`|恢复上一层环境|
|导出最小历史|`conda env export --from-history`|输出显式安装的主要依赖|
|删除环境|`conda env remove -n ds`|删除整个环境；执行前确认不在使用且项目依赖已记录|
|核验 Python 命令|`command -v python`|输出 Shell 实际解析到的解释器路径|
|核验当前解释器|`python -c 'import sys; print(sys.executable)'`|输出运行代码的解释器绝对路径|
|核验 pip 归属|`python -m pip --version`|输出 pip 版本及所属环境路径|
|临时环境变量|`APP_ENV=dev python app.py`|只为该次进程及其子进程设置变量|
|读取环境变量|`os.environ['APP_ENV']`|返回字符串；缺失时抛 `KeyError`|
|可选读取|`os.getenv('APP_ENV', 'dev')`|返回字符串或默认值，不修改环境|

### 最小核验流程（Minimal Verification Workflow）
```bash
conda activate ds
command -v python
python -c 'import sys; print(sys.executable)'
python -m pip --version
# 输出中的三个路径都应指向同一个 ds 环境；绝对路径因机器而异。
```
### 常见错配与安全边界（Common Mismatches and Safety Boundaries）
- **终端能导入、IDE 不能导入**：IDE 选择了不同解释器；把项目解释器切换到 `sys.executable` 显示的环境。
- **`pip install` 后仍然找不到包**：裸 `pip` 可能属于别的环境；改用 `python -m pip install ...` 并再次核验路径。
- **Notebook 仍使用旧环境**：内核（Kernel）与启动 Notebook 的 Shell 可以不同；在单元格中检查 `sys.executable` 并选择正确内核。
- **删除边界**：删除环境前保存 `environment.yml` 或依赖锁定文件，确认目标名称和路径，不能把环境删除等同于删除项目代码。
- **秘密信息**：令牌只通过环境变量或秘密管理器注入；不要写入源码、命令历史、日志或 Git。
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
## 官方参考（Official References）
- [Python 3 文档](https://docs.python.org/3/)
