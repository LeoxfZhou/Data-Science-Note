---
title: Python 基础语法（Python Basics）
aliases:
  - Python Basics
  - 基础语法
status: review
detail_level: comprehensive
source:
  - Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/基础语法.md
suggested_target: Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/02-Python 基础语法（Python Basics）.md
operation: 新建
merge_target: null
---

# Python 基础语法（Python Basics）

## 1. 代码结构与命名

Python 使用缩进表示代码块，通常每层使用 4 个空格。不要混用 Tab 和空格。

```python
temperature = 28

if temperature > 30:
    print("炎热")
elif temperature >= 20:
    print("舒适")
else:
    print("偏冷")
```

常用命名约定：

- 变量、函数、模块：`snake_case`
- 类：`PascalCase`
- 常量：`UPPER_SNAKE_CASE`
- 内部实现：名称以单下划线开头，例如 `_cache`

不要覆盖内置名称：

```python
# list = [1, 2, 3]  # 之后无法正常调用 list()，因此不应这样命名。
numbers = [1, 2, 3]
```

注释使用 `#`。三引号创建的是字符串字面量，不等同于注释；函数、类和模块开头的三引号字符串称为 docstring。

## 2. 变量、对象与可变性

变量是指向对象的名称，不是固定类型的“盒子”。

```python
left = [1, 2]
right = left
right.append(3)

# 两个名称指向同一个可变列表，因此两边都能观察到修改。
print(left)  # [1, 2, 3]
print(left is right)  # True
```

- 不可变对象：`int`、`float`、`bool`、`str`、`tuple`、`frozenset`。
- 可变对象：`list`、`dict`、`set` 以及多数自定义实例。
- `==` 比较值是否相等；`is` 比较是否是同一个对象。
- 判断空值使用 `value is None`，不要使用 `value == None`。

需要独立列表时显式复制：

```python
original = [1, 2, 3]
copied = original.copy()
copied.append(4)
```

嵌套可变对象需要深复制时使用 `copy.deepcopy()`，但应先判断数据结构是否可以设计得更简单。

## 3. 常用内置类型

| 类型 | 示例 | 特点 |
|---|---|---|
| `int` | `42` | 任意精度整数 |
| `float` | `3.14` | 浮点数存在表示误差 |
| `bool` | `True` | `bool` 是 `int` 的子类 |
| `str` | `"hello"` | 不可变 Unicode 文本 |
| `list` | `[1, 2]` | 有序、可变 |
| `tuple` | `(1, 2)` | 有序、不可变 |
| `dict` | `{"name": "Ada"}` | 键值映射，键必须可哈希 |
| `set` | `{1, 2}` | 无重复元素的集合 |
| `None` | `None` | 表示“没有值” |

### 真值判断

`0`、`0.0`、`None`、空字符串和空容器通常为假，其余对象通常为真。

```python
items = []
if not items:
    print("没有数据")
```

浮点数不要直接判断精确相等：

```python
import math

print(0.1 + 0.2 == 0.3)  # False
print(math.isclose(0.1 + 0.2, 0.3))  # True
```

## 4. 字符串

```python
name = "Ada"
score = 0.9567

# f-string 可读性好，并能直接控制格式。
message = f"{name} 的分数是 {score:.2%}"
print(message)
```

常用操作：

```python
text = "  Python,NumPy,Pandas  "
cleaned = text.strip()
parts = cleaned.split(",")
joined = " | ".join(parts)

print(cleaned.startswith("Python"))
print(cleaned.replace("Pandas", "Polars"))
```

切片规则是左闭右开：`sequence[start:stop:step]`。

```python
word = "python"
print(word[0])     # p
print(word[-1])    # n
print(word[1:4])   # yth
print(word[::-1])  # nohtyp
```

原始字符串适合正则和 Windows 路径，但不能以奇数个反斜杠结束，参见 [[06-正则表达式（Regular Expressions）]]。

## 5. 列表、元组、字典与集合

### 列表

```python
scores = [0.8, 0.6, 0.9]
scores.append(0.7)
scores.extend([0.5, 1.0])

sorted_scores = sorted(scores, reverse=True)  # 返回新列表。
scores.sort()  # 原地修改，返回 None。
```

### 元组与解包

```python
record = ("cat", 0.92)
label, confidence = record

first, *middle, last = [1, 2, 3, 4]
```

单元素元组必须带逗号：`(1,)`。

### 字典

```python
metrics = {"loss": 0.42, "accuracy": 0.91}

loss = metrics["loss"]
f1_score = metrics.get("f1", 0.0)  # 键不存在时返回默认值。

for name, value in metrics.items():
    print(name, value)
```

访问必须存在的键时使用 `mapping[key]`，因为缺失时的 `KeyError` 能暴露数据问题；只有缺失是正常情况时才使用 `get()`。

### 集合

```python
train_ids = {1, 2, 3}
test_ids = {3, 4}

overlap = train_ids & test_ids
all_ids = train_ids | test_ids
only_train = train_ids - test_ids
```

集合适合去重和成员判断，但不应该依赖集合的展示顺序。

## 6. 控制流程

```python
for index, value in enumerate([10, 20, 30], start=1):
    print(index, value)

for name, score in zip(["A", "B"], [0.8, 0.9], strict=True):
    # strict=True 能在两个序列长度不同时尽早报错，避免静默丢数据。
    print(name, score)
```

`break` 终止循环，`continue` 跳过本次迭代。循环的 `else` 只在没有被 `break` 终止时执行。

```python
target = 7
for value in [1, 3, 7, 9]:
    if value == target:
        print("found")
        break
else:
    print("not found")
```

## 7. 推导式与生成器表达式

```python
squares = [number**2 for number in range(10) if number % 2 == 0]
mapping = {name: len(name) for name in ["numpy", "pandas"]}
unique_lengths = {len(name) for name in ["a", "bb", "cc"]}
```

推导式适合短而清晰的转换；包含多层条件或副作用时改用普通循环。

生成器表达式按需产生数据：

```python
total = sum(number**2 for number in range(1_000_000))
```

## 8. 函数与参数

```python
def calculate_mean(values: list[float]) -> float:
    """返回非空数值列表的平均值。"""
    if not values:
        raise ValueError("values 不能为空")
    return sum(values) / len(values)
```

常见参数形式：

```python
def train(
    dataset,
    epochs: int,
    *,
    learning_rate: float = 0.001,
    verbose: bool = False,
):
    # * 后面的参数只能按名称传入，避免多个布尔值或数字难以辨认。
    ...


train(data, 10, learning_rate=0.01, verbose=True)
```

可变参数：

```python
def summarize(*values: float, precision: int = 2, **metadata) -> dict:
    return {
        "mean": round(sum(values) / len(values), precision),
        "metadata": metadata,
    }
```

### 可变默认参数陷阱

```python
def add_sample(sample, samples=None):
    # 默认值只在函数定义时创建一次；使用 None 才能为每次调用建立新列表。
    if samples is None:
        samples = []
    samples.append(sample)
    return samples
```

## 9. 作用域与闭包

名称查找遵循 LEGB：Local → Enclosing → Global → Built-in。

```python
def make_multiplier(factor: float):
    def multiply(value: float) -> float:
        # factor 来自外层函数作用域，形成闭包。
        return value * factor

    return multiply


double = make_multiplier(2)
print(double(5))
```

优先通过参数和返回值传递数据，尽量避免 `global`。`nonlocal` 只在确实需要修改闭包变量时使用。

## 10. 输入、输出与类型转换

`input()` 总是返回字符串：

```python
raw_age = input("年龄：")

try:
    age = int(raw_age)
except ValueError:
    print("请输入整数")
```

类型提示用于文档、IDE 和静态检查，不会自动阻止运行时传入错误类型。

## 11. 运算符 (Operators) 详细参考

### 11.1 算术运算符 (Arithmetic Operators)

| 运算符 | 含义 | 示例 | 结果 |
|---|---|---|---|
| `+` | 加法或序列拼接 | `2 + 3` | `5` |
| `-` | 减法 | `5 - 2` | `3` |
| `*` | 乘法或序列重复 | `"ab" * 2` | `"abab"` |
| `/` | 真除法 (True Division) | `5 / 2` | `2.5` |
| `//` | 向下取整除法 (Floor Division) | `5 // 2` | `2` |
| `%` | 取模 (Modulo) | `5 % 2` | `1` |
| `**` | 幂运算 (Exponentiation) | `2 ** 3` | `8` |

负数参与 `//` 时结果向负无穷方向取整：

```python
print(-5 // 2)  # -3，而不是 -2。
print(-5 % 2)   # 1；Python 保证 a == (a // b) * b + (a % b)。
```

### 11.2 比较、成员与身份

```python
age = 20
print(18 <= age < 65)  # Python 支持链式比较。

labels = {"cat", "dog"}
print("cat" in labels)
print("bird" not in labels)

value = None
print(value is None)  # None 是单例，使用身份判断。
```

### 11.3 逻辑运算符 (Logical Operators) 与短路 (Short-circuiting)

优先级为 `not` > `and` > `or`。`and` 和 `or` 返回参与运算的对象，不一定返回 `bool`。

```python
configured_name = ""
display_name = configured_name or "untitled"

user = None
# user 为 None 时右侧不会执行，避免访问不存在的属性。
is_admin = user is not None and user.role == "admin"
```

当表达式影响可读性时使用括号，不要依赖读者背诵完整优先级表。

## 12. 常用容器方法 (Container Methods) 详细参考

### 12.1 字符串方法 (String Methods)

| 方法 | 作用 | 是否修改原字符串 |
|---|---|---|
| `strip()` | 移除两端指定字符，默认空白 | 否 |
| `split(sep)` | 按分隔符拆分 | 否 |
| `join(iterable)` | 用当前字符串连接多个字符串 | 否 |
| `replace(old, new, count)` | 替换子串 | 否 |
| `find(sub)` | 返回位置，找不到返回 `-1` | 否 |
| `index(sub)` | 返回位置，找不到抛出 `ValueError` | 否 |
| `startswith()` / `endswith()` | 检查开头或结尾 | 否 |
| `lower()` / `upper()` / `casefold()` | 大小写转换 | 否 |
| `isdecimal()` | 是否全部为十进制数字 | 否 |

字符串不可变，因此所有转换都会返回新字符串。

### 12.2 列表方法 (List Methods)

| 方法 | 作用 | 返回值 |
|---|---|---|
| `append(x)` | 末尾加入一个对象 | `None` |
| `extend(iterable)` | 逐个加入可迭代对象的元素 | `None` |
| `insert(i, x)` | 指定位置插入 | `None` |
| `remove(x)` | 删除第一个等于 `x` 的元素 | `None`，找不到抛错 |
| `pop(i=-1)` | 删除并返回指定元素 | 被删除的元素 |
| `clear()` | 删除全部元素 | `None` |
| `index(x)` | 查找第一个位置 | 整数，找不到抛错 |
| `count(x)` | 统计出现次数 | 整数 |
| `sort()` | 原地排序 | `None` |
| `reverse()` | 原地反转 | `None` |
| `copy()` | 浅复制 | 新列表 |

```python
items = [1, 2]
items.append([3, 4])   # [1, 2, [3, 4]]：把列表作为一个元素加入。
items.extend([5, 6])   # [1, 2, [3, 4], 5, 6]：逐个加入元素。
```

### 12.3 字典方法 (Dictionary Methods)

```python
config = {"epochs": 10}

config["batch_size"] = 32
config.update({"epochs": 20, "device": "cpu"})

epochs = config.pop("epochs")
device = config.setdefault("device", "cpu")

for key, value in config.items():
    print(key, value)
```

`setdefault()` 会在键不存在时写入默认值；只想读取默认值时使用 `get()`，避免意外修改字典。

### 12.4 集合方法 (Set Methods)

```python
seen = {1, 2}
seen.add(3)
seen.update([3, 4, 5])

seen.discard(99)  # 元素不存在时不报错。
# seen.remove(99)  # 元素不存在时抛出 KeyError。
```

## 13. 函数参数 (Function Parameters) 完整分类

```python
def example(positional_only, /, regular, *args, keyword_only, **kwargs):
    return positional_only, regular, args, keyword_only, kwargs


result = example(1, 2, 3, 4, keyword_only=5, debug=True)
```

- `/` 前是仅位置参数 (Positional-only Parameters)。
- 普通参数可按位置或名称传递。
- `*args` 收集额外位置参数，类型是元组 (Tuple)。
- `*` 或 `*args` 后是仅关键字参数 (Keyword-only Parameters)。
- `**kwargs` 收集额外关键字参数，类型是字典 (Dictionary)。

参数定义顺序大致为：仅位置 → 普通 → 可变位置 → 仅关键字 → 可变关键字。

### 参数传递与可变对象

Python 使用对象共享传递 (Call by Sharing)：函数获得的是同一个对象的引用副本。

```python
def mutate(values: list[int]) -> None:
    values.append(99)  # 修改共享的列表对象，调用方能够看到。


def rebind(values: list[int]) -> None:
    values = [99]  # 只让局部名称指向新列表，不影响调用方名称。
```

## 14. 迭代协议 (Iteration Protocol) 与惰性计算 (Lazy Evaluation)

可迭代对象 (Iterable) 能产生迭代器 (Iterator)；迭代器保存当前位置，并通过 `next()` 逐个返回元素。

```python
values = [10, 20, 30]
iterator = iter(values)

print(next(iterator))
print(next(iterator))
```

生成器函数 (Generator Function) 使用 `yield` 暂停并保存状态：

```python
def read_batches(items, batch_size: int):
    if batch_size <= 0:
        raise ValueError("batch_size 必须大于 0")

    for start in range(0, len(items), batch_size):
        # 每次只生成一个批次，调用方不需要等待所有结果先放入列表。
        yield items[start : start + batch_size]
```

生成器通常只能消费一次；需要重复遍历时重新创建生成器或保存结果。

## 15. 排序 (Sorting) 与 `key` 函数

```python
records = [
    {"name": "A", "score": 0.8},
    {"name": "B", "score": 0.9},
    {"name": "C", "score": 0.9},
]

ordered = sorted(
    records,
    key=lambda record: (-record["score"], record["name"]),
)
```

`sorted()` 返回新列表；`list.sort()` 原地修改。Python 排序是稳定排序 (Stable Sort)，键相等的元素保持原相对顺序。

## 16. 完成检查

- [ ] 能解释变量引用、可变对象和浅复制。
- [ ] 能根据任务选择 list、tuple、dict 或 set。
- [ ] 能正确使用切片、解包、`enumerate` 和 `zip`。
- [ ] 能编写带类型提示、边界检查和清晰返回值的函数。
- [ ] 能避免覆盖内置名称、可变默认参数和错误使用 `is`。

## 参考资料

- [Python 官方教程](https://docs.python.org/3/tutorial/)
- [Python 风格指南 PEP 8](https://peps.python.org/pep-0008/)
