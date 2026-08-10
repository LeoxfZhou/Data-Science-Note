---
title: 错误与异常（Errors and Exceptions）
aliases:
  - 错误与异常
status: review
detail_level: comprehensive
source:
  - Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/错误与异常.md
suggested_target: Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-错误与异常（Errors and Exceptions）.md
operation: 新建
merge_target: null
---

# 错误与异常（Errors and Exceptions）

## 1. 错误类型

- **语法错误（SyntaxError）**：代码无法被正确解析，程序尚未开始正常执行。
- **异常（Exception）**：语法合法，但运行时发生了无法继续完成的情况。

阅读 traceback 时从最后一行开始：先看异常类型和消息，再沿调用栈向上寻找自己代码中的第一处相关位置。

## 2. 捕获具体异常

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
> 避免裸写 `except:`，它连 `KeyboardInterrupt` 等退出信号也会捕获。通常应捕获明确的异常类型；确实需要兜底时使用 `except Exception`，并记录或重新抛出异常。

## 3. `else` 与 `finally`

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

文件操作更推荐 `with`，它能自动管理资源：

```python
from pathlib import Path


def read_integer(path: Path) -> int:
    with path.open("r", encoding="utf-8") as file:
        return int(file.read().strip())
```

## 4. 主动抛出异常

```python
def set_probability(value: float) -> float:
    if not 0.0 <= value <= 1.0:
        # 尽早拒绝非法输入，可以让错误更靠近真正原因。
        raise ValueError("probability 必须位于 [0, 1]")
    return value
```

自定义异常适合表达业务层错误：

```python
class ModelNotReadyError(RuntimeError):
    """模型尚未加载，当前操作无法执行。"""


def predict(model, features):
    if model is None:
        raise ModelNotReadyError("请先加载模型")
    return model(features)
```

## 5. 什么时候处理，什么时候继续抛出

只在当前层能够做出有效处理时捕获异常，例如：

- 使用备用方案。
- 补充上下文后转换成更合适的异常。
- 在程序边界记录错误并返回明确响应。
- 释放当前层负责的资源。

如果只是打印一句“出错了”然后继续运行，往往会隐藏真正错误。

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

## 6. 异常层级 (Exception Hierarchy)

大多数应用异常继承自 `Exception`。`BaseException` 还包含 `KeyboardInterrupt`、`SystemExit` 等控制程序退出的异常，因此普通业务代码通常不应捕获 `BaseException`。

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

先写具体异常，后写一般异常，否则一般异常会提前捕获其子类：

```python
try:
    load_data()
except FileNotFoundError:
    recover_missing_file()
except OSError:
    handle_other_io_error()
```

## 7. `assert`、警告 (Warnings) 与异常的区别

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

## 8. 多个异常 (Multiple Exceptions)

多个无关任务需要并行报告错误时，现代 Python 提供异常组 (Exception Group) 和 `except*`。普通顺序代码仍优先使用常规 `try/except`。

```python311
errors = [ValueError("bad row"), OSError("file unavailable")]

try:
    raise ExceptionGroup("batch failed", errors)
except* ValueError as value_errors:
    print(value_errors)
except* OSError as io_errors:
    print(io_errors)
```

## 9. 常见异常

| 异常 | 常见原因 |
|---|---|
| `NameError` | 使用了尚未定义的名称 |
| `TypeError` | 操作或参数类型不合适 |
| `ValueError` | 类型合适，但值不合法 |
| `KeyError` | 字典中不存在该键 |
| `IndexError` | 序列索引越界 |
| `AttributeError` | 对象不存在该属性 |
| `FileNotFoundError` | 路径不存在 |
| `ModuleNotFoundError` | 模块未安装或导入路径不正确 |

## 10. 完成检查

- [ ] 能从 traceback 中找到异常类型、消息和自己代码的位置。
- [ ] 能解释为什么优先捕获具体异常。
- [ ] 能区分 `else` 与 `finally`。
- [ ] 能使用 `raise ... from ...` 保留异常链。
- [ ] 不会用异常处理掩盖程序错误。

## 参考资料

- [Python 官方教程：Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
