---
title: 错误与异常（Errors and Exceptions）
aliases:
  - 错误与异常
status: review
detail_level: comprehensive
merge_policy: union-zero-loss
reviewed_at: 2026-08-11
source:
  - Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/错误与异常.md
suggested_target: Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-错误与异常（Errors and Exceptions）.md
operation: 新建
merge_target: null
---

# 错误 (Error)与异常（Errors and Exceptions）

> [!important] 完整性与合并 (Merge)原则（Completeness and Merge Policy）
> 本稿以 Inbox 原稿的逐段信息为基线，并把上一版 Review 的补充知识按主题嵌入相邻章节。仅调整标题层级、纠正明显错误 (Error)和移除完全重复内容；参数 (Parameter)、示例、边界条件、异常 (Exception)说明与原注释均保留。

- **来源原稿（Source Note）**：`Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/错误与异常.md`
- **合并 (Merge)方式（Merge Method）**：取并集（Union），原稿细节 + Review 补充。
- **状态（Status）**：仅供 Review 校准，未写入 Notes。

## 错误 (Error)与异常 (Errors and Exceptions)
### 一、 错误 (Error)分类 (Error Classification)

#### 结构化补充（Structured Supplement）：错误 (Error)类型

- **语法错误（SyntaxError）**：代码无法被正确解析，程序尚未开始正常执行。
- **异常（Exception）**：语法合法，但运行时发生了无法继续完成的情况。

阅读 traceback 时从最后一行开始：先看异常 (Exception)类型和消息，再沿调用栈 (Call Stack)向上寻找自己代码中的第一处相关位置。

#### 结构化补充（Structured Supplement）：异常层级 (Exception Hierarchy)

大多数应用异常 (Exception)继承 (Inheritance)自 `Exception`。`BaseException` 还包含 `KeyboardInterrupt`、`SystemExit` 等控制程序退出的异常 (Exception)，因此普通业务代码通常不应捕获 `BaseException`。

```text
BaseException
├── SystemExit
├── KeyboardInterrupt
└── Exception
    ├── ArithmeticError
    │   └── ZeroDivisionError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── OSError
    │   └── FileNotFoundError
    ├── TypeError
    └── ValueError
```

先写具体异常 (Exception)，后写一般异常 (Exception)，否则一般异常 (Exception)会提前捕获其子类：

```python
try:
    load_data()
except FileNotFoundError:
    recover_missing_file()
except OSError:
    handle_other_io_error()
```

#### 结构化补充（Structured Supplement）：`assert`、警告 (Warnings) 与异常 (Exception)的区别

- `raise`：验证外部输入或表达运行时失败，生产环境必须保留。
- `assert`：检查开发者认为必然成立的内部不变量 (Invariant)。Python 优化模式可能移除断言，因此不能用它验证用户输入。
- `warnings.warn()`：当前行为仍能继续，但需要提醒弃用、精度或兼容性问题。

```python
def normalize(values: list[float]) -> list[float]:
    if not values:
        raise ValueError("values 不能为空")

    total = sum(values)
    if total == 0:
        raise ValueError("values 的和不能为 0")

    result = [value / total for value in values]
    assert len(result) == len(values)  # 检查内部不变量，而不是外部输入。
    return result
```

#### 结构化补充（Structured Supplement）：常见异常 (Exception)

| 异常 (Exception) | 常见原因 |
|---|---|
| `NameError` | 使用了尚未定义的名称 |
| `TypeError` | 操作或参数 (Parameter)类型不合适 |
| `ValueError` | 类型合适，但值不合法 |
| `KeyError` | 字典 (Dictionary)中不存在该键 |
| `IndexError` | 序列 (Sequence)索引 (Index)越界 |
| `AttributeError` | 对象不存在该属性 |
| `FileNotFoundError` | 路径 (Path)不存在 |
| `ModuleNotFoundError` | 模块 (Module)未安装或导入路径 (Path)不正确 |

错误 (Error)一般可分为两种：
- **语法错误 (Syntax Error)**：又称解析错误 (Parsing Error)，是在语法分析器检查代码时发现的错误 (Error)。
- **异常 (Exception)错误 (Exception Error)**：在运行时 (Runtime) 检测到的错误 (Error)，此时程序的语法是正确的。
---
### 二、 处理异常 (Handling Exceptions)

#### 结构化补充（Structured Supplement）：捕获具体异常 (Exception)

```python
def parse_ratio(numerator: str, denominator: str) -> float:
    try:
        # 转换和除法可能产生不同异常，调用方需要知道失败原因。
        left = float(numerator)
        right = float(denominator)
        return left / right
    except ValueError as error:
        raise ValueError("输入必须是数字") from error
    except ZeroDivisionError as error:
        raise ValueError("分母不能为 0") from error
```

`raise ... from error` 会保留原始原因，排查问题时比丢弃上下文更有价值。

> [!warning]
> 避免裸写 `except:`，它连 `KeyboardInterrupt` 等退出信号也会捕获。通常应捕获明确的异常 (Exception)类型；确实需要兜底时使用 `except Exception`，并记录或重新抛出异常 (Exception)。

#### 结构化补充（Structured Supplement）：什么时候处理，什么时候继续抛出

只在当前层能够做出有效处理时捕获异常 (Exception)，例如：

- 使用备用方案。
- 补充上下文后转换成更合适的异常 (Exception)。
- 在程序边界记录错误 (Error)并返回明确响应。
- 释放当前层负责的资源。

如果只是打印一句“出错了”然后继续运行，往往会隐藏真正错误 (Error)。

```python
import logging

logger = logging.getLogger(__name__)


def run_job() -> None:
    try:
        process_data()
    except OSError:
        # logger.exception 会自动记录 traceback；随后重新抛出，让上层决定如何处理。
        logger.exception("数据处理失败")
        raise
```

#### 1. try ... except ...
这是处理异常 (Exception)最基础的结构。
- 如果在执行 `try` 子句 (Clause) 时没有异常 (Exception)发生，则不会执行 `except` 子句。
- 如果 `try` 子句发生了异常 (Exception)，则跳过该子句中剩下的部分，直接执行 `except` 子句。
- 如果 `except` 子句没有指定异常 (Exception)类型，则可以处理 `try` 中的所有异常 (Exception)类型。
- 如果 `except` 子句指定了异常 (Exception)类型，则只能处理对应的异常 (Exception)类型（指定多个异常 (Exception)类型时，可以用元组 (Tuple)来表示）。
- 如果一个异常 (Exception)没有与任何的 `except` 匹配，则会报错。
**代码示例：**
```Python
## 示例 1：通用 except
def div(a, b):
    try:
        c = a / b
        print(f"{a} / {b} = {c}")
    except:
        print('try中发生异常')
div(2, 1)
div(2, 0)
div('2', 2)
## 示例 2：指定特定异常类型
def div(a, b):
    try:
        c = a / b
        print(f"{a} / {b} = {c}")
    except ZeroDivisionError:
        print('try中发生了除数为0的异常')
    except TypeError:
        print('try中发生了类型异常')
div(2, 1)
div(2, 0)
div('2', 2)

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```
#### 2. 处理多个异常 (Exception)

##### 结构化补充（Structured Supplement）：多个异常 (Multiple Exceptions)

多个无关任务需要并行报告错误 (Error)时，现代 Python 提供异常组 (Exception Group) 和 `except*`。普通顺序代码仍优先使用常规 `try/except`。

```python311
errors = [ValueError("bad row"), OSError("file unavailable")]

try:
    raise ExceptionGroup("batch failed", errors)
except* ValueError as value_errors:
    print(value_errors)
except* OSError as io_errors:
    print(io_errors)

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

可以使用一个 `except` 子句捕获多个异常 (Exception)，将异常 (Exception)类名放入一个元组 (Tuple) 中。
**代码示例：**
```Python
def div(a, b):
    try:
        c = a / b
        print(f"{a} / {b} = {c}")
    except (ZeroDivisionError, TypeError):
        print('try中发生了除数为0或类型的异常')
div(2, 1)
div(2, 0)
div('2', 2)

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```
#### 3. 获取异常 (Exception)对象 (Exception Object)
可以使用 `as` 关键字 (Keyword)将捕获到的异常 (Exception)实例赋值给一个变量 (Variable)。
**代码示例：**
```Python
def div(a, b):
    try:
        c = a / b
        print(f"{a} / {b} = {c}")
    except Exception as e:
        print(f"捕获到异常：{e}")
        print(type(e))
div(2, 0)
div('2', 2)

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```
---
### 三、 完整异常处理 (Exception Handling)结构 (Complete Structure)

#### 结构化补充（Structured Supplement）：`else` 与 `finally`

```python
from pathlib import Path


def read_integer(path: Path) -> int:
    file = None
    try:
        file = path.open("r", encoding="utf-8")
        content = file.read()
    except OSError as error:
        raise RuntimeError(f"读取文件失败：{path}") from error
    else:
        # else 只在 try 没有异常时执行，避免把转换错误误认为文件错误。
        return int(content.strip())
    finally:
        # finally 无论成功或失败都会执行，适合释放资源。
        if file is not None:
            file.close()
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

文件操作更推荐 `with`，它能自动管理资源：

```python
from pathlib import Path


def read_integer(path: Path) -> int:
    with path.open("r", encoding="utf-8") as file:
        return int(file.read().strip())
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

#### 1. try ... finally ...
- `finally` 子句将作为 `try` 语句结束前的最后一项任务被执行。
- 不论 `try` 语句是否产生了异常 (Exception)，`finally` 都会被执行。
**代码示例：**
```Python
def div(a, b):
    try:
        c = a / b
        print(f"{a} / {b} = {c}")
    finally:
        print("执行finally子句")
div(2, 0)

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```
#### 2. try ... except ... else ... finally ...
- `**else**` **子句**：在 `try` 子句没有发生任何异常 (Exception)时执行。
- `**finally**` **子句**：在任何情况下都会被执行。
**代码示例：**
```Python
def div(a, b):
    try:
        c = a / b
        print(f"{a} / {b} = {c}")
    except:
        print('except在发生异常时执行')
    else:
        print('else在没有异常时执行')
    finally:
        print('finally在任何情况下都会被执行')
print("--- 测试无异常情况 ---")
div(2, 1)
print("\\n--- 测试有异常情况 ---")
div(2, 0)

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```
---
### 四、 抛出异常 (Raising Exceptions)

#### 结构化补充（Structured Supplement）：主动抛出异常 (Exception)

```python
def set_probability(value: float) -> float:
    if not 0.0 <= value <= 1.0:
        # 尽早拒绝非法输入，可以让错误更靠近真正原因。
        raise ValueError("probability 必须位于 [0, 1]")
    return value
```

自定义异常 (Exception)适合表达业务层错误 (Error)：

```python
class ModelNotReadyError(RuntimeError):
    """模型尚未加载，当前操作无法执行。"""


def predict(model, features):
    if model is None:
        raise ModelNotReadyError("请先加载模型")
    return model(features)
```

- 使用 `raise` 语句可以主动抛出一个异常 (Exception)。
- `raise` 后面可以是异常 (Exception)实例 (Instance)、异常 (Exception)类 (Class) 或没有内容。
**代码示例：**
```Python
## 示例 1：抛出带自定义信息的异常
def div(a, b):
    if b == 0:
        raise ZeroDivisionError('除数为0')
    c = a / b
    print(f"{a} / {b} = {c}")
div(2, 1)
## div(2, 0)  # 这行会触发主动抛出的 ZeroDivisionError
## 示例 2：仅抛出异常类
def div(a, b):
    if b == 0:
        raise ZeroDivisionError
    c = a / b
    print(f"{a} / {b} = {c}")
div(2, 1)
## div(2, 0)

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

## 进阶补充与核对（Advanced Supplements and Verification）

### 结构化补充（Structured Supplement）：完成检查

- [ ] 能从 traceback 中找到异常 (Exception)类型、消息和自己代码的位置。
- [ ] 能解释为什么优先捕获具体异常 (Exception)。
- [ ] 能区分 `else` 与 `finally`。
- [ ] 能使用 `raise ... from ...` 保留异常 (Exception)链。
- [ ] 不会用异常处理 (Exception Handling)掩盖程序错误 (Error)。

### 结构化补充（Structured Supplement）：参考资料

- [Python 官方教程：Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
