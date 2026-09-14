---
title: "Python 语法、函数与面向对象速查表（Python Syntax, Functions, and OOP Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - python/fundamentals
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "Python 3.11–3.14；以 Python 3 当前稳定文档为准"
---
# Python 语法、函数与面向对象速查表（Python Syntax, Functions, and OOP Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
`python --version` 确认解释器；常用入口为脚本、模块 `python -m package.module` 与交互式解释器。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 变量、表达式与控制流（Variables, Expressions, and Control Flow）
覆盖赋值、条件、循环与模式匹配等日常语法。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|查看类型|`type(obj)`|返回对象类型，不修改对象|
|检查类型|`isinstance(obj, (int, float))`|返回布尔值|
|多变量赋值|`a, b = b, a`|交换绑定关系|
|条件表达式|`x if condition else y`|返回被选中的表达式值|
|范围迭代|`range(start, stop, step)`|返回惰性 range 对象，stop 不包含|
|带索引迭代|`enumerate(items, start=0)`|返回索引和值的迭代器|
|并行迭代|`zip(a, b, strict=True)`|返回元组迭代器；长度不同且 strict=True 时抛 ValueError|
|模式匹配|`match value: ...`|执行第一个匹配的 case，不产生返回值|
|循环跳过|`continue`|跳过本轮剩余语句|
|循环退出|`break`|退出最内层循环|
|循环正常结束|`for ... else: ...`|未触发 break 时执行 else|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
values = [3, 1, 2]
labels = ["c", "a", "b"]
pairs = sorted(zip(values, labels, strict=True))
print(pairs)
# 期望输出:
# [(1, 'a'), (2, 'b'), (3, 'c')]
```
## 字符串与格式化（Strings and Formatting）
字符串（String）不可变；切片和替换会创建新对象。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|清理两端字符|`text.strip(chars=None)`|返回新字符串|
|拆分|`text.split(sep=None, maxsplit=-1)`|返回字符串列表|
|拼接|`sep.join(parts)`|返回拼接后的字符串|
|替换|`text.replace(old, new, count=-1)`|返回新字符串|
|查找|`text.find(sub)`|返回首个索引，未找到为 -1|
|强制查找|`text.index(sub)`|返回索引，未找到抛 ValueError|
|前后缀判断|`text.startswith(prefix) / text.endswith(suffix)`|返回布尔值|
|大小写归一|`text.casefold()`|返回适合无大小写比较的新字符串|
|格式化|`f'{value:.2f}'`|返回格式化字符串|
|编码|`text.encode('utf-8')`|返回 bytes|
|解码|`raw.decode('utf-8')`|返回 str|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
raw = "  Alice,92.5  "
name, score = raw.strip().split(",")
print(f"{name}: {float(score):.1f}")
# 期望输出:
# Alice: 92.5
```
## 函数与参数（Functions and Parameters）
函数是可调用对象；参数定义接口，返回值承载结果。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|定义函数|`def fn(a, b=0): ...`|创建函数对象|
|仅限位置参数|`def fn(a, /, b): ...`|斜杠前参数不能按关键字传入|
|仅限关键字参数|`def fn(*, mode='mean'): ...`|星号后参数必须按关键字传入|
|可变位置参数|`def fn(*args): ...`|args 为元组|
|可变关键字参数|`def fn(**kwargs): ...`|kwargs 为字典|
|返回多个值|`return a, b`|返回二元组|
|匿名函数|`lambda x: x * 2`|返回函数对象；适合短表达式|
|函数注解|`def fn(x: int) -> str: ...`|写入 __annotations__，运行时默认不强制|
|文档字符串|`fn.__doc__`|返回文档字符串或 None|
|局部闭包|`nonlocal name`|修改最近外层函数作用域绑定|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
def summarize(values: list[float], *, digits: int = 1) -> tuple[int, float]:
    return len(values), round(sum(values) / len(values), digits)

print(summarize([1, 2, 6], digits=2))
# 期望输出:
# (3, 3.0)
```
## 推导式、生成器与迭代协议（Comprehensions, Generators, and Iteration）
推导式适合构造容器；生成器按需产生值以控制内存。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|列表推导式|`[f(x) for x in xs if pred(x)]`|返回新列表|
|集合推导式|`{f(x) for x in xs}`|返回去重后的集合|
|字典推导式|`{k: f(v) for k, v in items}`|返回新字典|
|生成器表达式|`(f(x) for x in xs)`|返回惰性生成器|
|取得下一项|`next(iterator, default)`|返回下一项；耗尽时返回 default 或抛 StopIteration|
|创建迭代器|`iter(iterable)`|返回迭代器|
|生成值|`yield value`|暂停函数并返回一个值|
|委托生成|`yield from iterable`|逐项转发子迭代器|
|任一满足|`any(iterable)`|短路返回布尔值|
|全部满足|`all(iterable)`|短路返回布尔值；空输入为 True|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
squares = (x * x for x in range(6) if x % 2 == 0)
print(list(squares))
# 期望输出:
# [0, 4, 16]
```
## 类、数据类与协议（Classes, Dataclasses, and Protocols）
用类封装状态和行为；优先清晰组合，谨慎使用深继承。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|定义实例|`class Model: ...`|创建类对象|
|初始化|`def __init__(self, ...): ...`|初始化新实例状态，通常返回 None|
|对象表示|`def __repr__(self): ...`|返回调试字符串|
|属性访问器|`@property`|把无参方法暴露为只读或可控属性|
|类方法|`@classmethod`|首参为类，常用于替代构造器|
|静态方法|`@staticmethod`|不自动绑定实例或类|
|数据类|`@dataclass`|生成初始化、比较和表示等方法|
|不可变数据类|`@dataclass(frozen=True)`|属性赋值抛 FrozenInstanceError|
|抽象接口|`class P(Protocol): ...`|支持结构化静态类型检查|
|资源管理|`def __enter__ / __exit__`|支持 with 上下文管理|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from dataclasses import dataclass
@dataclass(frozen=True)
class Sample:
    name: str
    score: float

s = Sample("A", 0.95)
print(s.name, s.score)
# 期望输出:
# A 0.95
```
## 异常、上下文与模块（Exceptions, Contexts, and Modules）
异常表示无法按契约完成操作；捕获时应尽量具体。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|主动抛出|`raise ValueError('message')`|中断当前流程并携带异常|
|异常捕获|`try: ... except ValueError as exc: ...`|处理指定异常|
|无论如何清理|`finally: ...`|正常或异常路径均执行|
|异常链|`raise DomainError(...) from exc`|保留直接原因|
|断言|`assert condition, message`|失败抛 AssertionError；优化模式可移除|
|文件上下文|`with open(path, encoding='utf-8') as f`|离开块时关闭文件|
|自定义上下文|`@contextmanager`|把单生成器函数包装为上下文管理器|
|导入模块|`import package.module as alias`|绑定模块对象|
|脚本入口|`if __name__ == '__main__'`|:仅直接执行文件时进入|
|动态属性检查|`getattr(obj, name, default)`|返回属性或默认值|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
def parse_positive(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise ValueError("must be positive")
    return value

for raw in ["3", "0"]:
    try:
        print(parse_positive(raw))
    except ValueError as exc:
        print(type(exc).__name__)
# 期望输出:
# 3
# ValueError
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
## 官方参考（Official References）
- [Python 3 文档](https://docs.python.org/3/)
