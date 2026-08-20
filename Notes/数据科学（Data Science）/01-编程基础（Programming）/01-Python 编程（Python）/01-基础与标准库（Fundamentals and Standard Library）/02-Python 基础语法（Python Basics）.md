---
title: Python 基础语法（Python Basics）
aliases:
  - Python Basics
  - 基础语法
status: published
detail_level: comprehensive
merge_policy: union-zero-loss
reviewed_at: 2026-08-11
published_at: 2026-08-11
updated_at: 2026-08-17
---

# Python 基础语法（Python Basics）
## 1. 基础概念、变量与输入输出（Fundamentals, Variables, and I/O）
### 1.1 代码结构、命名、缩进与注释（Code Structure, Naming, Indentation, and Comments）
#### 源码编码与关键字检查（Source Encoding and Keyword Inspection）

Python 3 源文件默认使用 UTF-8 编码（Encoding）。只有确实需要其他编码时，才在第一行或紧随 Shebang 的第二行写编码声明，例如 `# -*- coding: cp1252 -*-`；源码实际保存编码必须与声明一致，否则解释器可能无法解码文件。Python 3 允许非 ASCII 标识符（Identifier），但团队代码通常仍优先采用清晰的英文命名，以降低输入法、字体和跨语言协作成本。

关键字（Keyword）会随 Python 版本演化，不应长期维护一份可能过时的手写列表。使用标准库 `keyword` 查询当前解释器：

```python
import keyword

print(keyword.iskeyword("class"))  # True
print(keyword.iskeyword("match"))  # False；当前是软关键字（Soft Keyword）
print(keyword.issoftkeyword("match"))  # True
print("yield" in keyword.kwlist)  # True
```

- `keyword.kwlist`：当前解释器全部关键字。
- `keyword.softkwlist`：当前解释器全部软关键字；软关键字只在特定语法上下文中具有特殊含义。
- `keyword.iskeyword(value)` 与 `keyword.issoftkeyword(value)`：分别判断普通关键字与软关键字。

Python 使用缩进表示代码块，通常每层使用 4 个空格。不要混用 Tab 和空格。

```python
temperature = 28

if temperature > 30:
    print("炎热")  # temperature > 30 时输出: 炎热
elif temperature >= 20:
    print("舒适")  # 当前示例输出: 舒适
else:
    print("偏冷")  # temperature < 20 时输出: 偏冷
```

常用命名约定：
- 变量 (Variable)、函数 (Function)、模块 (Module)：`snake_case`
- 类：`PascalCase`
- 常量：`UPPER_SNAKE_CASE`
- 内部实现：名称以单下划线开头，例如 `_cache`

不要覆盖内置名称：

```python
# list = [1, 2, 3]  # 之后无法正常调用 list()，因此不应这样命名。
numbers = [1, 2, 3]
```

注释使用 `#`。三引号创建的是字符串 (String)字面量，不等同于注释；函数 (Function)、类和模块 (Module)开头的三引号字符串 (String)称为 docstring。

#### 1. 缩进 (Indentation)
Python 使用行首的空白区域来表示代码的 **层级关系 (Hierarchy)**，这是语法的强制要求。
- **定义**：行首的空白。
- **规范**：通常一次缩进对应 **4 个空格**。
- **作用**：在复合语句（如函数 (Function)、循环、条件判断）中表示代码块的从属关系。
- **注意**：不正确的缩进会导致程序逻辑错误 (Error)甚至直接报错（`IndentationError`）。

> **快捷键**：
>
> - `Tab`：增加缩进
>
> - `Shift + Tab`：减少缩进
#### 2. 注释 (Comment)
解释器 (Interpreter) 在执行时会完全忽略的内容，仅供人阅读。
- **单行注释**：以 `#` 开头。
- **多行注释**：使用成对的三个单引号 `'''` 或三个双引号 `"""`。只有当多行注释未被赋值给变量 (Variable)或未被程序调用时，它才充当注释。

```Python
## 这是单行注释
'''
这是多行注释
可以写很多行
'''
def func():
    """
    这是函数的文档注释 (Docstring)
    """
    pass
```

#### 3. 行拼接 (Line Splicing)
当一行代码过长影响可读性时，可以将其拆分为多行。
- **显式拼接 (Concatenation)**：在行尾使用反斜杠 `\\` (续行符)。
- **隐式拼接 (推荐)**：在列表 (List) `[]`、元组 (Tuple) `()`、字典 (Dictionary) `{}` 等容器内部换行，Python 会自动识别为同一行。

```Python
## 显式拼接 (不推荐，容易出错)
a = 1 + 2 + \
    3 + 4
## 隐式拼接 (推荐)
b = [
    1, 2, 3,
    4, 5, 6
]
```

---
### 1.2 变量、对象与内存机制（Variables, Objects, and Memory）
#### 对象绑定、别名与复制（Object Binding, Aliasing, and Copying）

变量 (Variable)是指向对象的名称，不是固定类型的“盒子”。

```python
left = [1, 2]
right = left
right.append(3)

# 两个名称指向同一个可变列表，因此两边都能观察到修改。
print(left)  # [1, 2, 3]
print(left is right)  # True
```
- 不可变对象 (Immutable Object)：`int`、`float`、`bool`、`str`、`tuple`、`frozenset`。
- 可变对象 (Mutable Object)：`list`、`dict`、`set` 以及多数自定义实例。
- `==` 比较值是否相等；`is` 比较是否是同一个对象。
- 判断空值使用 `value is None`，不要使用 `value == None`。

> [!tip] 大白话理解（Plain-language Intuition）
> Python 变量更像贴在对象上的标签，而不是直接装值的盒子。两个变量可以同时指向同一个可变对象，所以通过其中一个变量修改对象，另一个变量也会看到变化；重新赋值只是把标签改贴到别处，不会自动修改旧对象。

需要独立列表 (List)时显式复制：

```python
original = [1, 2, 3]
copied = original.copy()
copied.append(4)
```

嵌套可变对象 (Mutable Object)需要深复制 (Deep Copy)时使用 `copy.deepcopy()`，但应先判断数据结构是否可以设计得更简单。

#### 1. 变量 (Variable)的本质：引用 (Reference)
**语法**：`variable_name = data`
- **内存模型**：
    1. Python 在内存中开辟空间存储 **数据** (Data)。
    1. **变量 (Variable)名** (Variable Name) 仅仅是一个标签，它 **指向** 该数据的内存地址 (Memory Address)。
- **引用计数 (Reference Counting)**：Python 记录每个数据被多少个变量 (Variable)引用 (Reference)。
    - 当引用计数 (Reference Count)归零时，该数据被视为垃圾数据，触发 **垃圾回收 (Garbage Collection)机制 (Garbage Collection)** 将其释放。

#### 2. 数据的不可变性 (Immutability)
**数字 (Number)** 和 **字符串 (String)** 是 **不可变数据**。
- **核心逻辑**：内存中的数字或字符串 (String)一旦创建，本身无法被修改。
- **修改假象**：
    - 执行 `a = a + 1` 时，Python **并没有** 修改原地址的数据。
    - **实际操作**：计算结果，开辟**新内存**存入新结果，然后让 `a` **重新指向** 新地址。旧数据若无其他引用 (Reference)则被回收。

```Python
a = 789
b = a       # b 也指向 789，引用计数为 2
a = 345     # a 指向新地址 345
## 此时 b 仍然指向 789，789 不会被回收，引用计数变为 1
print(b)    # 输出 789
```

#### 3. 标识符 (Identifier)命名规范 (Naming Conventions)
- **硬性规则**：
    - 由字母、数字、下划线组成。
    - **不能以数字开头**。
    - 区分大小写 (Case Sensitive)。
    - 不能使用关键字 (Keywords，如 `if`, `def`, `class`)。
- **最佳实践**：
    - **下划线命名法 (Snake Case)**：`my_lucky_number` (变量 (Variable)名推荐)。
    - **驼峰命名法 (Camel Case)**：`MyClass` (大驼峰，通常用于类名)。
    - **避免冲突**：尽量不要使用内置函数 (Function)名 (Built-in Functions) 作为变量 (Variable)名（如 `print`, `input`, `type`），否则会导致原函数 (Function)失效。

```Python
## 错误示例：覆盖内置函数
print = 100
## print("Hello")  # 此时会报错：'int' object is not callable
```

---
### 1.3 输入、输出与类型转换（Input, Output, and Type Conversion）
#### 基础输入输出与显式转换（Basic I/O and Explicit Conversion）

`input()` 总是返回字符串 (String)：

```python
raw_age = input("年龄：")

try:
    age = int(raw_age)
except ValueError:
    print("请输入整数")

# 输出场景: 输出取决于用户输入 (User Input)。输入 `20` 时转换成功，不产生额外提示；输入 `abc` 时输出：
# 期望输出:
# 年龄：abc
# 请输入整数
```

类型提示用于文档、IDE 和静态检查，不会自动阻止运行时传入错误 (Error)类型。

#### 1. 输出函数 (Function) `print()`
**语法**：`print(*values, sep=' ', end='\\n')`
- **values** **(不定长参数 (Parameter))**：
    - 可以接收任意数量的位置参数 (Positional Arguments)。
    - "贪婪"特性：尽可能多地接收参数 (Parameter)。
- **`sep`** **(Separator)**：
    - 多个对象输出时的 **间隔符**。
    - 默认值：空格 `' '`。
- **`end`** **(End)**：
    - 输出结束后的 **结尾符**。
    - 默认值：换行符 `\\n`。若设为空字符串 (String) `''`，则不换行。

```Python
## 默认情况
print("Hello", "World")  # 输出: Hello World（中间为空格，末尾换行）
## 自定义间隔符和结尾符
print("Hello", "World", sep=" - ", end="!!!")  # 输出: Hello - World!!!（末尾不换行）
```

#### 2. 输入函数 (Function) `input()`
**语法**：`variable = input([prompt])`
- **阻塞 (Blocking)**：程序执行到此处暂停，等待用户输入并回车。
- **提示信息 (Prompt)**：参数 (Parameter)可以是字符串 (String)，用于在控制台提示用户。
- **返回值 (Return Value)**：**永远是字符串 (String)**。
    - 即使输入的是数字 `123`，得到的也是字符串 (String) `"123"`。若需计算，必须进行类型转换 (Type Conversion)。

```Python
name = input("请输入您的姓名: ")
print(f"{name}, 你好！")
## 类型转换示例
age_str = input("请输入年龄: ")
age = int(age_str) # 转换为整数
print(f"明年你就 {age + 1} 岁了")

# 输出场景: 姓名输入“小明”，年龄输入“20”时：
# 期望输出:
# 请输入您的姓名: 小明
# 小明, 你好！
# 请输入年龄: 20
# 明年你就 21 岁了
```

## 2. 标准数据类型与数据结构（Standard Data Types and Data Structures）
### 2.1 类型总览与真值判断（Type Overview and Truth Testing）

| 类型 | 示例 | 特点 |
|---|---|---|
| `int` | `42` | 任意精度整数 (Integer) |
| `float` | `3.14` | 浮点数 (Floating-point Number)存在表示误差 |
| `bool` | `True` | `bool` 是 `int` 的子类 |
| `str` | `"hello"` | 不可变 Unicode 文本 |
| `list` | `[1, 2]` | 有序、可变 |
| `tuple` | `(1, 2)` | 有序、不可变 |
| `dict` | `{"name": "Ada"}` | 键值映射，键必须可哈希 |
| `set` | `{1, 2}` | 无重复元素的集合 (Set) |
| `None` | `None` | 表示“没有值” |

#### 真值判断

`0`、`0.0`、`None`、空字符串 (String)和空容器通常为假，其余对象通常为真。

```python
items = []
if not items:
    print("没有数据")  # 输出: 没有数据
```

浮点数 (Floating-point Number)不要直接判断精确相等：

```python
import math

print(0.1 + 0.2 == 0.3)  # False
print(math.isclose(0.1 + 0.2, 0.3))  # True
```

### 2.2 核心容器概览（Core Container Overview）
#### 列表 (List)

```python
scores = [0.8, 0.6, 0.9]
scores.append(0.7)
scores.extend([0.5, 1.0])

sorted_scores = sorted(scores, reverse=True)  # 返回新列表。
scores.sort()  # 原地修改，返回 None。
```

#### 元组 (Tuple)与解包

```python
record = ("cat", 0.92)
label, confidence = record

first, *middle, last = [1, 2, 3, 4]
```

单元素元组 (Tuple)必须带逗号：`(1,)`。

#### 字典 (Dictionary)

```python
metrics = {"loss": 0.42, "accuracy": 0.91}

loss = metrics["loss"]
f1_score = metrics.get("f1", 0.0)  # 键不存在时返回默认值。

for name, value in metrics.items():
    print(name, value)

# 期望输出:
# loss 0.42
# accuracy 0.91
```

访问必须存在的键时使用 `mapping[key]`，因为缺失时的 `KeyError` 能暴露数据问题；只有缺失是正常情况时才使用 `get()`。

#### 集合 (Set)

```python
train_ids = {1, 2, 3}
test_ids = {3, 4}

overlap = train_ids & test_ids
all_ids = train_ids | test_ids
only_train = train_ids - test_ids

print(overlap)     # 输出: {3}
print(all_ids)     # 输出示例: {1, 2, 3, 4}；集合不保证显示顺序。
print(only_train)  # 输出示例: {1, 2}；集合不保证显示顺序。
```

集合 (Set)适合去重 (Deduplication)和成员判断，但不应该依赖集合 (Set)的展示顺序。

### 2.3 常用容器方法速查（Container Method Quick Reference）
#### 字符串方法速查（String Method Quick Reference）

| 方法 | 作用 | 是否修改原字符串 (String) |
|---|---|---|
| `strip()` | 移除两端指定字符，默认空白 | 否 |
| `split(sep)` | 按分隔符拆分 | 否 |
| `join(iterable)` | 用当前字符串 (String)连接多个字符串 (String) | 否 |
| `replace(old, new, count)` | 替换子串 | 否 |
| `find(sub)` | 返回位置，找不到返回 `-1` | 否 |
| `index(sub)` | 返回位置，找不到抛出 `ValueError` | 否 |
| `startswith()` / `endswith()` | 检查开头或结尾 | 否 |
| `lower()` / `upper()` / `casefold()` | 大小写转换 | 否 |
| `isdecimal()` | 是否全部为十进制数字 | 否 |

字符串 (String)不可变，因此所有转换都会返回新字符串 (String)。

#### 列表方法速查（List Method Quick Reference）

| 方法 | 作用 | 返回值 (Return Value) |
|---|---|---|
| `append(x)` | 末尾加入一个对象 | `None` |
| `extend(iterable)` | 逐个加入可迭代对象的元素 | `None` |
| `insert(i, x)` | 指定位置插入 | `None` |
| `remove(x)` | 删除第一个等于 `x` 的元素 | `None`，找不到抛错 |
| `pop(i=-1)` | 删除并返回指定元素 | 被删除的元素 |
| `clear()` | 删除全部元素 | `None` |
| `index(x)` | 查找第一个位置 | 整数 (Integer)，找不到抛错 |
| `count(x)` | 统计出现次数 | 整数 (Integer) |
| `sort()` | 原地排序 (Sorting) | `None` |
| `reverse()` | 原地反转 | `None` |
| `copy()` | 浅复制 (Shallow Copy) | 新列表 (List) |

```python
items = [1, 2]
items.append([3, 4])   # [1, 2, [3, 4]]：把列表作为一个元素加入。
items.extend([5, 6])   # [1, 2, [3, 4], 5, 6]：逐个加入元素。
```

#### 字典方法速查（Dictionary Method Quick Reference）

```python
config = {"epochs": 10}

config["batch_size"] = 32
config.update({"epochs": 20, "device": "cpu"})

epochs = config.pop("epochs")
device = config.setdefault("device", "cpu")

for key, value in config.items():
    print(key, value)

# 期望输出:
# batch_size 32
# device cpu
```

`setdefault()` 会在键不存在时写入默认值；只想读取默认值时使用 `get()`，避免意外修改字典 (Dictionary)。

#### 集合方法速查（Set Method Quick Reference）

```python
seen = {1, 2}
seen.add(3)
seen.update([3, 4, 5])

seen.discard(99)  # 元素不存在时不报错。
# seen.remove(99)  # 元素不存在时抛出 KeyError。
```

Python 3 中有六种标准数据类型 (Data Type)：
- **不可变数据 (Immutable)**：数字 (`Number`)、字符串 (`String`)、元组 (`Tuple`)
- **可变数据 (Mutable)**：列表 (`List`)、字典 (`Dictionary`)、集合 (`Set`)
---
### 2.4 数字（Number）
#### 1. 特性
- **不可变 (Immutable)**：数字一旦定义，其值无法更改。对变量 (Variable)的修改（如 `a = a + 1`）实际上是创建了一个新的数字对象，并让变量 (Variable)指向新地址。
- **非序列 (Non-Sequence)**：数字是原子性的整体，没有“元素”的概念，不支持索引 (`Index`) 和切片 (`Slice`)。
#### 2. 分类 (Classification)
#### 整数 (int)
- 包括正整数 (Integer)、负整数 (Integer)和零。
- **特性**：Python 的整数 (Integer)没有长度限制（仅受限于内存），可以表示非常大的数。
- **示例**：`789`, `789`, `0`
#### 浮点数 (float)
- 即数学中的小数。
- **书写方式**：
    - 常规写法：`7.89`, `8.0`, `.78` (省略0), `78.` (省略小数位)。
    - **科学计数法 (Scientific Notation)**：如 `3e4` ($3 \times 10^4 = 30000.0$)。凡是用科学计数法表示的数，Python 都会认定为浮点数 (Floating-point Number)。

#### 布尔型 (bool)
- `True` 和 `False` 是 Python 的关键字（**首字母必须大写**）。
- **本质**：布尔型 (Boolean Type)是整数 (Integer)的子类。
    - `True` 对应数值 `1`
    - `False` 对应数值 `0`
- **运算**：可以参与数学运算。

```Python
print(True + 1)   # 输出: 2
print(False * 10) # 输出: 0
```

#### 复数 (complex)
- **格式**：`实部 + 虚部` (Real + Imaginary)。
- **虚部单位**：使用 `j` 或 `J`。
    - 示例：`a = 3 + 4j`
- **注意**：当虚部系数为 `1` 时，**不能省略**，必须写成 `1j`。
    - _解释_：如果写成 `j`，Python 会将其视为一个名为 `j` 的变量 (Variable)，而不是虚数单位。
    - 数学中的 i^2 = -1，Python 中 `1j * 1j` 结果为 `(-1+0j)`（保持复数 (Complex Number)类型）。

#### 3. 数字相关类型转换 (Type Conversion)函数 (Function)
#### `type(object)`
- 返回 `object` 的类型。
#### `int([x])`
- 将 `x` 转换为十进制整数 (Integer)。
- **规则**：
    - 浮点数 (Floating-point Number)转整数 (Integer)：**直接截断**（去掉小数部分），而非四舍五入。
    - 字符串 (String)转整数 (Integer)：字符串 (String)必须符合整数 (Integer)格式（不能包含小数点）。
    - 不传参返回 `0`。

```Python
print(int())      # 0
print(int(3))     # 3
print(int(-3))    # -3
print(int(3.99))  # 3 (截断)
print(int(-3.99)) # -3
print(int(True))  # 1
print(int(False)) # 0
print(int('12'))  # 12
print(int('-12')) # -12
int('12.1')     # ValueError: 字符串包含小数点
```

#### `float([x])`
- 将 `x` 转换为浮点数 (Floating-point Number)。
- 不传参返回 `0.0`。

```Python
print(float())       # 0.0
print(float(3))      # 3.0
print(float(-3))     # -3.0
print(float(3.99))   # 3.99
print(float(True))   # 1.0
print(float(False))  # 0.0
print(float('12'))   # 12.0
print(float('-12'))  # -12.0
print(float('12.1')) # 12.1
```

#### `bool([x])`
- 将 `x` 转换为布尔值 (Boolean Value)。
- **判定为 False 的情况**：
    - 数字：`0`, `0.0`, `0j`
    - 关键字 (Keyword)：`False`, `None`
    - 空容器：空字符串 (String) `''`, 空列表 (List) `[]`, 空元组 (Tuple) `()`, 空字典 (Dictionary) `{}`, 空集合 (Set) `set()`
- **判定为 True 的情况**：除上述以外的所有值（包括字符串 (String) `'0'`, `'False'`, `'None'`）。

```Python
print(bool(0))       # False
print(bool(0.0))     # False
print(bool(0j))      # False
print(bool(''))      # False
print(bool([]))      # False
print(bool(None))    # False
print(bool(' '))     # True (包含空格)
print(bool('0'))     # True (非空字符串)
print(bool('False')) # True
```

#### `complex([real[, imag]])`
- 创建一个复数 (Complex Number) `real + imag * 1j`。
- 如果第一个参数 (Parameter)是字符串（如 `"3+4j"`），则**不能**有第二个参数 (Parameter)，且字符串 (String)内 `+` 号两边**不能有空格**。

```Python
print(complex())         # 0j
print(complex(3.2, 4))   # (3.2+4j)
print(complex(3.2))      # (3.2+0j)
print(complex('3.2'))    # (3.2+0j)
print(complex("3.2+4j")) # (3.2+4j)
```

#### 标准库数学与伪随机工具（Standard-library Math and Pseudorandom Tools）

`math` 处理实数数学函数与常量；复数运算使用 `cmath`。角度参与三角函数前通常需要先用 `math.radians()` 转为弧度（Radian）。

```python
import math

print(math.ceil(4.1))  # 5
print(math.floor(4.9))  # 4
print(math.sqrt(81))  # 9.0
print(math.log(100, 10))  # 2.0
print(math.isclose(math.sin(math.radians(30)), 0.5))  # True
print(math.hypot(3, 4))  # 5.0
print(round(math.pi, 5))  # 3.14159
```

常用接口：
- `math.ceil(x)` / `math.floor(x)`：分别向正无穷与负无穷方向取整。
- `math.fabs(x)`：返回浮点绝对值；一般对象的绝对值使用内置 `abs()`。
- `math.exp(x)`、`math.log(x, base)`、`math.log10(x)`、`math.sqrt(x)`：指数、对数与平方根。
- `math.sin(x)`、`math.cos(x)`、`math.tan(x)` 及对应反函数：参数或结果以弧度表示。
- `math.degrees(x)` / `math.radians(x)`：弧度与角度互转。
- `math.pi` / `math.e`：圆周率与自然常数。

`random` 是确定性的伪随机数生成器（Pseudorandom Number Generator），适合模拟、抽样和测试，不适合密码、令牌或安全验证码；安全随机值使用 `secrets`。

```python
import random

rng = random.Random(42)  # 独立实例避免修改模块级全局随机状态，并让示例可复现。
values = ["red", "green", "blue", "yellow"]

print(rng.randrange(0, 10, 2))  # 0；从 range(0, 10, 2) 选择
print(rng.randint(1, 6))  # 1；上下界都包含
print(rng.choice(values))  # blue；从非空序列选择一个元素
print(rng.sample(values, k=2))  # ['green', 'red']；无放回抽样
rng.shuffle(values)  # 原地打乱并返回 None。
print(values)  # ['yellow', 'red', 'blue', 'green']
```

- `random.random()`：返回满足 `0.0 <= x < 1.0` 的浮点数。
- `random.randrange(start, stop, step)`：从对应 `range` 中选一个值，`stop` 不包含在内。
- `random.randint(a, b)`：等价于 `randrange(a, b + 1)`，因此包含 `a` 和 `b`。
- `random.choice(sequence)`：从非空序列选择一个元素；空序列会抛出 `IndexError`。
- `random.sample(population, k)`：无放回抽样并返回新列表；`k` 大于总体长度时抛出 `ValueError`。
- `random.shuffle(sequence)`：原地打乱可变序列，不返回打乱后的副本。
- `random.uniform(a, b)`：从两个边界之间抽取浮点数；受浮点舍入影响，端点是否出现取决于计算结果。

---
### 2.5 字符串（String）
#### 字符串构造、格式化与切片概览（String Construction, Formatting, and Slicing Overview）

```python
name = "Ada"
score = 0.9567

# f-string 可读性好，并能直接控制格式。
message = f"{name} 的分数是 {score:.2%}"
print(message)  # 输出: Ada 的分数是 95.67%
```

常用操作：

```python
text = "  Python,NumPy,Pandas  "
cleaned = text.strip()
parts = cleaned.split(",")
joined = " | ".join(parts)

print(cleaned.startswith("Python"))
print(cleaned.replace("Pandas", "Polars"))

# 期望输出:
# True
# Python,NumPy,Polars
```

切片 (Slicing)规则是左闭右开：`sequence[start:stop:step]`。

```python
word = "python"
print(word[0])     # p
print(word[-1])    # n
print(word[1:4])   # yth
print(word[::-1])  # nohtyp
```

原始字符串 (Raw String)适合正则和 Windows 路径 (Path)，但不能以奇数个反斜杠结束，参见 [[06-正则表达式（Regular Expressions）]]。

#### 1. 特性
- **不可变 (Immutable)**：字符串 (String)一旦创建，内容不可修改。
- **序列 (Sequence)**：
    - **有元素**：由字符组成（Python 中没有专门的字符类型 `char`，字符就是长度为 1 的字符串 (String)）。
    - **有顺序**：字符排列顺序不同即为不同字符串 (String)。
    - **有索引 (Index)**：支持正向索引（0 开始）和反向索引（-1 开始）。

#### 2. 定义方式
- **单行字符串 (String)**：使用一对单引号 `' '` 或双引号 `" "`。
    - _Tip_：灵活使用引号可以避免转义（如字符串 (String)内部包含单引号时，外部用双引号包裹）。
- **多行字符串 (String)**：使用成对的三个单引号 `''' '''` 或三个双引号 `""" """`。

```Python
s1 = '这是一个单行字符串'
s2 = "这是一个单行字符串"
s3 = '''这是一个
多行字符串'''
s4 = """这是一个
多行字符串"""
```

#### 3. `str(object)`
- 将对象转换为字符串 (String)格式。

```Python
print(str())      # ''
print(str(1234))  # '1234'
print(str(-1.23)) # '-1.23'
```

在字符串 (String)中，反斜杠 `\\` 和特定字符组合 (Composition)组成转义字符。

|转义字符|描述|说明|
|---|---|---|
|`\\\\`|反斜杠|显示一个 `\\` 字符|
|`\\'`|单引号|用于在单引号包裹的字符串 (String)中显示 `'`|
|`\\"`|双引号|用于在双引号包裹的字符串 (String)中显示 `"`|
|`\\n`|换行符|将光标移到下一行开头|
|`\\t`|横向制表符|**Tab 对齐**：通常以 4 个或 8 个空格为一组。`\\t` 会补齐当前位置到下一组的起始位置，用于纵向对齐数据。|

```Python
print('https:\\\\www.example.com\\nuxy\\tngj')  # 输出: https:\\www.example.com\nuxy\tngj
```

#### 原始字符串（Raw String）
- **定义**：在字符串 (String)前加 `r` 或 `R`。
- **作用**：使字符串 (String)内的转义字符**失效**，所见即所得。常用于**文件路径 (Path)**（Windows 路径 (Path)包含 `\\`）和**正则表达式 (Regular Expression)**。
- **限制**：Raw 字符串 (String)**不能以奇数个反斜杠结尾**。
    - _原因_：结尾的反斜杠会转义掉闭合的引号，导致语法错误 (Syntax Error)。

```Python
print(r'https:\\\\www.example.com\\nuxy\\tngj') # 原样输出，\\n 不换行
## print(r"abc\\")  # 报错：SyntaxError
print(r"abc" + "\\\\") # 变通方法：拼接
```

---
#### 字符串格式化（String Formatting）
**1.** **`%`** **格式化 (Printf-style)**
使用 `%` 占位符。

|符号|描述|
|---|---|
|`%s`|格式化为字符串 (String)|
|`%d` / `%i`|格式化为十进制整数（仅限数字）|
|`%f` / `%F`|格式化为浮点数（默认保留 6 位小数）|

- `%.nf`：指定保留 `n` 位小数。

```Python
print('它说它叫%s,今年%d岁,每天睡%f小时!' % ('旺财', 2, 8.5))  # 输出: 它说它叫旺财,今年2岁,每天睡8.500000小时!
## 精度控制
print('今天买了%s斤青菜, %s元/斤, 花了%.2f元!' % (3.5, 2.59, 3.5*2.59))  # 输出: 今天买了3.5斤青菜, 2.59元/斤, 花了9.06元!
```

**2.** **`format`** **方法格式化**
使用 `{}` 占位符。
- **位置参数 (Positional Argument)**：按顺序填充。
- **关键字参数 (Keyword Argument)**：按名称填充。
- **下标索引 (Index)**：按参数 (Parameter)的索引 (Index)位置填充。
- **精度控制**：`{:.nf}`。

```Python
name = '旺财'
age1 = 2
age2 = 3
## 位置参数
print('它说它叫{},它今年{}岁,它宝宝{}个月了!'.format(name, age1, age2))  # 输出: 它说它叫旺财,它今年2岁,它宝宝3个月了!
## 关键字参数 (推荐，可读性高)
print('它说它叫{n},它今年{a1}岁,它宝宝{a2}个月了!'.format(a1=age1, n=name, a2=age2))  # 输出同上
## 下标参数
print('它说它叫{1},它今年{0}岁,它宝宝{2}个月了!'.format(age1, name, age2))  # 输出同上
## 精度控制
print('花了{:.2f}元!'.format(3.5 * 2.59))  # 输出: 花了9.06元!
```

**3. f-string 格式化 (Python 3.6+ 推荐)**
在字符串 (String)前加 `f`，直接在 `{}` 中写入变量 (Variable)或表达式。
- **特点**：代码最简洁，性能最高。
- **支持表达式**：`{age + 1}`。
- **精度控制**：`{value:.nf}`。

```Python
name = '旺财'
age = 2
age2 = 3
print(f'它说它叫{name},\n它{age}岁,\n它宝宝{age2}个月了!')
print(fr'它说它叫{name},\n它{age}岁') # f-string 与 raw string 结合
## 精度控制
print(f'花了{3.5 * 2.59:.2f}元!')

# 期望输出:
# 它说它叫旺财,
# 它2岁,
# 它宝宝3个月了!
# 它说它叫旺财,\n它2岁
# 花了9.06元!
```

---
#### 字符串常用方法（String Methods）
**1. 替换（Replacement）**
- **`str.replace(old, new, count=-1)`**
    - 用 `new` 替换 `old`。
    - `count`：替换次数，默认替换所有。
    - _注意_：因为字符串 (String)不可变，此方法返回的是一个**新字符串 (String)**副本 (Copy)。

```Python
s = "Line1 Line2 Line4"
print(s.replace("Li", "b"))     # 输出: bne1 bne2 bne4
print(s.replace("Li", "b", 2))  # 输出: bne1 bne2 Line4
```
- **`str.strip([chars])`**
    - 移除字符串 (String)**首尾**指定的字符。
    - 如果不指定 `chars`，默认移除**空白符**（空格 , 换行 `\\n`, 制表符 `\\t`）。

```Python
str1 = ' \\thello world h \\n'
print(str1.strip())  # 输出: hello world h

str2 = "ooho hello world"
print(str2.strip('o'))  # 输出: ho hello world

str3 = 'www.example.com'
print(str3.strip("cwom"))  # 输出: .example.
```

**2. 前缀与后缀检测**
- **`str.startswith(prefix[, start[, end]])`**：检查是否以 `prefix` 开头。
- **`str.endswith(suffix[, start[, end]])`**：检查是否以 `suffix` 结尾。
    - 参数 (Parameter)可以是**元组 (Tuple)** `("xx", "yy")`，满足其一即可。
    - `start`, `end` 用于指定检测范围。

```Python
str1 = "hello world"
print(str1.startswith("he"))        # True
print(str1.startswith("wo", 6))     # True (从索引6开始)
print(str1.endswith(("d", "lo")))   # True
```

**3. 类型检测**
- **`str.isdigit()`**
    - 判定字符串 (String)中**每个字符**是否都是数字字符。
    - _注意_：负数（如 `"-123"`）和小数（如 `"1.23"`）会返回 `False`，因为包含符号或小数点。

```Python
print('1234'.isdigit()) # True
print('-123'.isdigit()) # False
```

**4. 分割与连接**
- **`str.split(sep=None, maxsplit=-1)`**
  - 以 `sep` 为分隔符切分字符串 (String)，返回**列表 (List)**。
  - `sep` 不指定时，默认以所有空白符切分，并丢弃空字符串 (String)。

```Python
s = " Line1 \\nLine2 \\tLine3"
print(s.split())         # 输出: ['Line1', 'Line2', 'Line3']
print(s.split('Li', 2))  # 输出: ['', 'ne1 \\n', 'ne2 \\tLine3']
```
- **`str.join(iterable)`**
    - 用字符串 (String)作为连接符，将 `iterable`（如列表 (List)、元组 (Tuple)）中的元素连接成新字符串 (String)。
    - **限制**：`iterable` 中的元素必须全部是**字符串 (String)**类型。

```Python
s = '-.'
seq = ['1', '2', '3']
print(s.join(seq))  # 输出: 1-.2-.3
```

**5. 查找与计数**
- **`str.count(sub, [start, end])`**
    - 统计子串 `sub` 出现的**非重叠**次数。
- **`str.find(sub)`** / **`str.rfind(sub)`**
    - `find`: 从左找，`rfind`: 从右找。
    - 返回索引 (Index)，找不到返回 **-1**。注意 `-1` 也可能被误当作最后一个元素的索引 (Index)，因此只需判断是否存在时优先使用 `sub in text`。
- **`str.index(sub)`** / **`str.rindex(sub)`**
    - 功能同 `find`，但找不到时会**报错** (`ValueError`)。

```Python
s = "hello world"
print(s.count('l')) # 3
print(s.find('lo')) # 3
print(s.find('ol')) # -1
```

**6. 大小写转换**
- `str.capitalize()`: 首字母大写，其余小写。
- `str.title()`: 每个单词首字母大写 (Title Case)。
- `str.upper()`: 全大写。
- `str.lower()`: 全小写。
- `str.swapcase()`: 大小写反转。

```Python
s = '你好hELlo wo?rLD世界TuP'
print(s.capitalize()) # 你好hello wo?rld世界tup
print(s.title())      # 你好Hello Wo?Rld世界Tup
print(s.upper())      # 你好HELLO WO?RLD世界TUP
```

### 2.6 列表（List）
#### 特性
- **可变 (Mutable)**：列表 (List)是可变的，这意味着创建后可以修改其内容。
- **序列 (Sequence)**：列表 (List)是有序的，支持索引 (`index`) 和切片 (`slice`) 操作。
- **定义**：列表 (List)用方括号 `[]` 定义，元素之间用逗号分隔。
- **元素限制**：列表 (List)元素没有类型限制，可以是数字、字符串 (String)、列表 (List)等任意对象。

```Python
list0 = []
list1 = ['China', 1997, 2000]
list2 = [1, 2, 3, 4, 5]
list3 = ["a", "b", "c", "d"]
list4 = ['red', 'green', 'blue', 'yellow', 'white', 'black']
```

#### 修改列表 (Modifying Lists)
列表 (List)是可变的，可以通过索引 (Index)和切片 (Slicing)的方式来对列表 (List)的元素重新赋值。
**基础示例列表 (List)**：

```Python
lst = [567, 'hello', 78.9, 'world', False]
```

#### 1. 针对一个元素修改 (Index Assignment)
- **格式**：`lst[index] = value`

```Python
lst[2] = 9.87
lst[3] = 'dlrow'
print(lst)  # 输出: [567, 'hello', 9.87, 'dlrow', False]
```

#### 2. 针对多个元素修改 (Slice Assignment)
- **格式**：`lst[start: end: step] = iterable`
- **注意**：赋值号右边必须是可迭代对象 (`iterable`)。
**场景 A：步长 (step) 为 1**
此时切片 (Slicing)选中的元素个数与赋值的元素个数**不需要相等**，列表 (List)会自动伸缩。

```Python
lst = [0, 1, 2, 3, 4]
## 1 vs 1 (等量替换)
## 将索引2到3（不含3）的元素替换
lst[2:3] = [9]
## 结果: [0, 1, 9, 3, 4]
## n vs n (等量替换)
lst = [0, 1, 2, 3, 4]
lst[2:4] = [8, 9]
## 结果: [0, 1, 8, 9, 4]
## 1 vs n (插入/扩充)
lst = [0, 1, 2, 3, 4]
lst[2:3] = [7, 8, 9]
## 结果: [0, 1, 7, 8, 9, 3, 4]
## n vs m (不等量替换)
lst = [0, 1, 2, 3, 4]
lst[2:4] = [1, 2, 3]
## 结果: [0, 1, 1, 2, 3, 4]
## 1 vs 0 (删除)
lst = [0, 1, 2, 3, 4]
lst[2:3] = []
## 结果: [0, 1, 3, 4]
## 0 vs n (纯插入)
lst = [0, 1, 2, 3, 4]
lst[2:2] = ['a', 'b']
## 结果: [0, 1, 'a', 'b', 2, 3, 4]
```

**场景 B：步长 (step) 不为 1**
- **限制**：切出的元素个数必须与右边赋值的元素个数**严格相等**，否则报错。

```Python
lst = [0, 1, 2, 3, 4, 5]
## 切片取出3个元素 (索引0, 2, 4)，赋值必须也是3个
lst[::2] = ['a', 'b', 'c']
print(lst)
## 错误示例
try:
    lst[::2] = ['a', 'b']
except ValueError as error:
    print(f"{type(error).__name__}: {error}")

# 期望输出:
# ['a', 1, 'b', 3, 'c', 5]
# ValueError: attempt to assign sequence of size 2 to extended slice of size 3
```

#### 列表常用方法（List Methods）
##### 1. 新增（Add）
- `append(obj)`: 在列表 (List)末尾添加新的对象。
- `extend(iterable)`: 在列表 (List)末尾一次性追加另一个序列 (Sequence)中的多个值。
- `insert(index, obj)`: 将对象插入列表 (List)指定位置。

```Python
lst = [1, 2]
lst.append(3)           # [1, 2, 3]
lst.extend([4, 5])      # [1, 2, 3, 4, 5]
lst.insert(0, 'start')  # ['start', 1, 2, 3, 4, 5]
```

##### 2. 删除（Delete）
- `pop([index])`: 移除列表 (List)中的一个元素（默认最后一个元素），并且**返回**该元素的值。
- `remove(obj)`: 移除列表 (List)中某个值的**第一个**匹配项。
- `clear()`: 清空列表 (List)。

```Python
lst = ['a', 'b', 'c', 'b']
val = lst.pop()      # 移除 'b'，返回 'b'，lst变为 ['a', 'b', 'c']
lst.remove('b')      # 移除第一个 'b'，lst变为 ['a', 'c']
lst.clear()          # []
```

##### 3. 查找与统计（Search and Count）
- `index(x[, start[, end]])`: 从列表 (List)中找出某个值第一个匹配项的索引 (Index)位置。
- `count(x)`: 统计某个元素在列表 (List)中出现的次数。

```Python
lst = [1, 2, 3, 2, 1]
print(lst.index(2))  # 1
print(lst.count(1))  # 2
```

##### 4. 排序与反转（Sort and Reverse）
###### 反转列表（Reverse a List）
- **`list.reverse()`**：把列表 (List)中的元素倒过来，无返回值（**原地修改 / in-place**）。

```Python
## 原地反转 (In-place)
lst = [1, 3, 5, 2]
lst.reverse()
print(lst)       # [2, 5, 3, 1]
## 切片反转 (返回新副本 copy，不修改原列表)
lst = [1, 3, 5, 2]
print(lst[::-1]) # [2, 5, 3, 1]
```

###### 排序列表（Sort a List）

排序的 `key` 函数 (Key Function) 与稳定性 (Stability)：

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

`sorted()` 返回新列表 (List)；`list.sort()` 原地修改。Python 排序 (Sorting)是稳定排序 (Stable Sort)，键相等的元素保持原相对顺序。
- **`list.sort(key=None, reverse=False)`**：对原列表 (List)进行排序（**原地修改**）。
- **`sorted(iterable, [key], reverse=False)`**：对可迭代对象进行排序 (Sorting)，**以列表 (List)形式返回**排序 (Sorting)之后的结果（不改变原数据）。
    - `iterable`：要排序 (Sorting)的可迭代对象。
    - `key`：指定一个函数 (Function)，在排序 (Sorting)之前，每个元素都先应用这个函数 (Function)，之后再根据返回值 (Return Value)排序 (Sorting)。
    - `reverse`：默认为 `False`，代表升序；指定为 `True` 则为降序。

```Python
lst = [1, 2, -5, -3]
## 升序排序 (返回新列表)
print(sorted(lst))                     # [-5, -3, 1, 2]
## 降序排序 (返回新列表)
print(sorted(lst, reverse=True))       # [2, 1, -3, -5]
## 对字符串排序 (将字符拆分排序，返回列表)
print(sorted('hello world'))           # [' ', 'd', 'e', 'h', 'l', 'l', 'l', 'o', 'o', 'r', 'w']

"""
key 参数进阶用法示例：按照绝对值的大小降序排序
"""
## abs() 是求绝对值/模的内置函数
print(abs(0))      # 0
print(abs(-9))     # 9
print(abs(-9.87))  # 9.87
print(abs(True))   # 1
print(abs(False))  # 0
print(abs(3+4j))   # 求模, 5.0
lst = [1, 2, -5, -3]
## 把 lst 中的每个元素依次作为实参传递给 key 所指定的函数 abs 去调用:
## abs(1), abs(2), abs(-5), abs(-3)
## 返回值分别为: 1, 2, 5, 3。然后根据这个返回值的大小对原数据进行排序。
lst.sort(key=abs, reverse=True)
print(lst) # [-5, -3, 2, 1]
## 使用 sorted 同理
print(sorted(lst, key=abs, reverse=True))  # [-5, -3, 2, 1]
```

---
### 2.7 元组（Tuple）
#### 特性
- **不可变 (Immutable)**：元组 (Tuple)一旦创建，其内部元素不可修改（不支持赋值）。
- **序列 (Sequence)**：有序，支持索引 (Index)和切片 (Slicing)。
- **定义**：使用圆括号 `()` 定义，元素之间用逗号分隔。

```Python
tup1 = ('China', 1997, 2000)
tup2 = (1, 2, 3, 4, 5)
tup3 = "a", "b", "c", "d"  # 不需要括号也可以定义元组（自动装包）
```

#### 特殊语法注意
当元组 (Tuple)中**只有一个元素**时，需要在元素后面添加逗号 `,`，否则括号会被当作运算符 (Operator)使用。

```Python
tup_wrong = (50)
print(type(tup_wrong)) # <class 'int'>
tup_right = (50,)
print(type(tup_right)) # <class 'tuple'>
```

#### 元组 (Tuple)的不可变性 (Immutability)详解
元组 (Tuple)的“不可变”指的是元组 (Tuple)所指向的内存地址 (Memory Address)中的内容不可变。如果元组 (Tuple)中包含可变对象（如列表 (List)），该可变对象 (Mutable Object)内部的元素是可以修改的。

```Python
tup = (1, 2, ['a', 'b'])
tup[0] = 3  # 报错：TypeError
## 但是可以修改元组内的列表
tup[2][0] = 'A'
print(tup) # (1, 2, ['A', 'b'])
```

#### 元组 (Tuple)常用方法 (Tuple Methods)
由于元组 (Tuple)不可变，所以它没有增、删、改的方法，只有查询方法。
- `index(x[, start[, end]])`: 查找值 x 的索引 (Index)。
- `count(x)`: 统计值 x 出现的次数。
### 2.8 字典（Dictionary）

- **可变 (Mutable)**：字典 (Dictionary)创建后，可以修改其内容（增删改）。
- **无序 (Unordered)**：在 Python 3.6 之前字典 (Dictionary)是无序的；虽然 Python 3.7+ 保持了插入顺序，但从概念上讲，字典 (Dictionary)是通过键来访问的，而不是通过索引 (Index)。
- **键的限制**：
    - **唯一性**：键必须是唯一的，如果重复，后一个值会覆盖前一个值。
    - **不可变性 (Immutability)**：键必须是**不可变数据类型 (Data Type)**（如数字、字符串 (String)、元组 (Tuple)）。列表 (`list`) 和字典 (`dict`) 不能作为键。

#### 2.8.1 定义（Definition）
使用花括号 `{}` 定义，键和值之间用冒号 `:` 分隔，键值对之间用逗号 `,` 分隔。

```Python
## 空字典
d0 = {}
d0_b = dict()
## 基础定义
d1 = {'name': 'Tom', 'age': 18}
d2 = {1: 'a', 2: 'b'}
## 键必须是不可变类型
d3 = {(1, 2): 'tuple_key'}
## d4 = {[1, 2]: 'list_key'} # 报错：TypeError: unhashable type: 'list'
```

#### 2.8.2 访问字典（Accessing）
字典 (Dictionary)不支持索引 (`index`) 和切片 (`slice`)，只能通过键 (`key`) 来访问。
- **`dict[key]`**：获取指定键的值。如果键不存在，会**报错** (`KeyError`)。
- **`dict.get(key[, default])`**：获取指定键的值。如果键不存在，返回 `None` (或者指定的默认值)，**不会报错**。

```Python
dic = {'name': 'Tom', 'age': 18}
print(dic['name'])      # 'Tom'
print(dic['gender'])  # 报错：KeyError: 'gender'
print(dic.get('name'))  # 'Tom'
print(dic.get('gender')) # None
print(dic.get('gender', 'Male')) # 'Male' (返回默认值)
```

#### 2.8.3 新增与修改（Add and Modify）
- **`update(other_dict)`**：将另一个字典 (Dictionary)的键值对更新到当前字典 (Dictionary)中（有则改，无则增）。

```Python
dic = {'name': 'Tom', 'age': 18}
## 修改
dic['age'] = 20
print(dic) # {'name': 'Tom', 'age': 20}
## 新增
dic['gender'] = 'Male'
print(dic) # {'name': 'Tom', 'age': 20, 'gender': 'Male'}
## update
dic.update({'id': 101, 'age': 22})
print(dic) # {'name': 'Tom', 'age': 22, 'gender': 'Male', 'id': 101}
```

#### 2.8.4 删除（Delete）
- **`pop(key[, default])`**：删除指定键的键值对，并**返回**该值。如果键不存在且未指定默认值，会报错。
- **`del dict[key]`**：删除指定键的键值对。
- **`clear()`**：清空字典 (Dictionary)。

```Python
dic = {'name': 'Tom', 'age': 18, 'gender': 'Male'}
val = dic.pop('age')    # 删除 'age'，返回 18
print(val)              # 18
print(dic)              # {'name': 'Tom', 'gender': 'Male'}
item = dic.popitem()    # 删除最后一项
print(item)             # ('gender', 'Male')
del dic['name']         # 删除 'name'
print(dic)              # {}
```

#### 2.8.5 常用方法（Common Methods）
- **`keys()`**：返回所有的键。
- **`values()`**：返回所有的值。
- **`items()`**：返回所有的键值对（元组 (Tuple)列表 (List)形式）。

```Python
dic = {'name': 'Tom', 'age': 18}
print(dic.keys())   # dict_keys(['name', 'age'])
print(dic.values()) # dict_values(['Tom', 18])
print(dic.items())  # dict_items([('name', 'Tom'), ('age', 18)])
## 遍历字典
for k, v in dic.items():
    print(k, v)

# 期望输出:
# 前 3 行分别为字典的键视图、值视图和键值对视图；最后一个循环输出：
# name Tom
# age 18
```

---
### 2.9 集合（Set）
#### 特性
- **无序 (Unordered)**：集合 (Set)中的元素没有固定顺序，不支持索引 (Index)和切片 (Slicing)。
- **唯一 (Unique)**：集合 (Set)中不允许有重复元素（自动去重 (Deduplication)）。
- **可变 (Mutable)**：可以添加或删除元素，但集合 (Set)中的元素本身必须是**不可变**的（hashable）。
#### 1. 定义 (Definition)
使用花括号 `{}` 定义，元素之间用逗号 `,` 分隔。
- **注意**：创建**空集合 (Set)**必须使用 `set()`，因为 `{}` 默认表示空字典 (Dictionary)。

```Python
s1 = {1, 2, 3, 4}
s2 = {1, 1, 2, 2, 3}
print(s2) # {1, 2, 3} (自动去重)
## 空集合
s_empty = set()
print(type(s_empty)) # <class 'set'>
## 错误示例：定义包含列表的集合
## s_wrong = {1, 2, [3, 4]} # 报错：TypeError: unhashable type: 'list'
```

#### 2. 集合 (Set)运算 (Set Operations)
集合 (Set)支持数学中的交集、并集、差集等运算。
- **交集 (Intersection)**：`&` 或 `intersection()`。返回两个集合 (Set)共同的元素。
- **并集 (Union)**：`|` 或 `union()`。返回两个集合 (Set)所有的元素（去重 (Deduplication)）。
- **差集 (Difference)**： 或 `difference()`。返回在前一个集合 (Set)中但不在后一个集合 (Set)中的元素。
- **对称差集 (Symmetric Difference)**：`^` 或 `symmetric_difference()`。返回两个集合 (Set)中不重复的元素（即去掉交集后的部分）。

```Python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
## 交集
print(a & b) # {3, 4}
## 并集
print(a | b) # {1, 2, 3, 4, 5, 6}
## 差集 (a - b: a中有b中没有的)
print(a - b) # {1, 2}
print(b - a) # {5, 6}
## 对称差集 (互相没有的)
print(a ^ b) # {1, 2, 5, 6}
```

#### 3. 常用方法（Common Methods）
##### 新增（Add）
- **`add(element)`**：添加一个元素。
- **`update(iterable)`**：添加多个元素（合并 (Merge)）。

```Python
s = {1, 2}
s.add(3)        # {1, 2, 3}
s.update([3, 4, 5]) # {1, 2, 3, 4, 5}
```

##### 删除（Delete）
- **`remove(element)`**：移除指定元素。如果元素不存在，会**报错** (`KeyError`)。
- **`discard(element)`**：移除指定元素。如果元素不存在，**不会报错**。
- **`pop()`**：任意移除并返回一个元素。集合 (Set) 无序，因此不能依赖其返回顺序；“任意”不等于统计意义上的随机 (Random)。
- **`clear()`**：清空集合 (Set)。
### 2.10 类型特性与创建注意事项（Type Characteristics and Construction Notes）
Python 3 的六大标准数据类型 (Data Type)分为 **不可变数据 (Immutable)** 和 **可变数据 (Mutable)** 两大类。以下是它们的特性与创建时的核心注意点整理：

|数据类型 (Data Type)|表现形式|特性 (Characteristics)|创建时需要注意的点 (Creation Notes)|
|---|---|---|---|
|**数字 (Number)**|`int`, `float`, `bool`, `complex`|**不可变**、非序列 (Non-Sequence)|1. `bool` 的 `True` 和 `False` 首字母必须大写。<br>2. 复数 (Complex Number)虚部系数为 `1` 时**不能省略**，必须写成 `1j`。<br>3. 科学计数法（如 `3e4`）默认生成的是浮点数 (Floating-point Number)。|
|**字符串 (String)**|`'...'`, `"..."`, `'''...'''`|**不可变**、序列 (Sequence)|1. 原始字符串 (Raw String，如 `r"..."`) **不能以奇数个反斜杠结尾**。<br>2. 注意内部引号的冲突，可灵活使用单/双/三引号互相嵌套。|
|**元组 (Tuple)**|`(...)`|**不可变**、序列 (Sequence)|1. 当元组 (Tuple)中**只有一个元素**时，元素后面**必须加逗号**（如 `(50,)`），否则括号会被当作数学运算符 (Operator)。|
|**列表 (List)**|`[...]`|**可变**、序列 (Sequence)|1. 元素没有类型限制，同一个列表 (List)内可以混合嵌套存储各种类型的数据。|
|**字典 (Dictionary)**|`{key: value}`|**可变**、映射类型|1. 键 (`key`) 必须是**可哈希对象 (Hashable Object)**（常见的有数字、字符串 (String)、只包含可哈希元素的元组 (Tuple)）。<br>2. 键必须是**唯一**的，重复的键会被后者的值覆盖。<br>3. Python 3.7+ 语言规范保证字典保留插入顺序，但仍应通过键而非位置表达业务含义。<br>4. 创建空字典 (Dictionary)使用 `{}` 或 `dict()`。|
|**集合 (Set)**|`{val1, val2}`|**可变**、无序、**元素唯一**|1. 创建**空集合 (Set)**必须使用 `set()`，因为 `{}` 默认是空字典 (Dictionary)。<br>2. 集合 (Set)内的元素必须是**可哈希对象 (Hashable Object)**（不能包含列表 (List)或字典 (Dictionary)等）。|

---
#### 核心注意事项代码示例 (Code Examples)
针对上述创建时的易错点，以下是具体的代码演示：

```Python
## 1. 数字 (Number)
num_float = 3e4          # 科学计数法，类型为 float (30000.0)
num_complex = 3 + 1j     # 复数虚部为1时，必须写1j，不能写成 3 + j
## 2. 字符串 (String)
## raw_str = r"C:\\test\\"  # 报错：SyntaxError，不能以奇数个反斜杠结尾
raw_str = r"C:\\test" + "\\\\" # 变通方法：通过字符串拼接解决
## 3. 元组 (Tuple)
tup_wrong = (50)         # 这是一个 int 类型，值为 50
tup_right = (50,)        # 这是一个 tuple 类型，包含一个元素 50
## 4. 字典 (Dictionary)
empty_dict = {}          # 创建空字典
## dict_wrong = {[1, 2]: 'a'} # 报错：TypeError，列表是可变类型，不能作为键
dict_right = {(1, 2): 'a'}   # 正确：元组是不可变类型，可以作为键
## 5. 集合 (Set)
empty_set = set()        # 创建空集合，绝对不能用 {}
s = {1, 2, 2, 3}
print(s)                 # 输出 {1, 2, 3} (自动去重)
## set_wrong = {1, 2, [3]} # 报错：TypeError，集合元素必须是不可变类型
```

### 2.11 序列索引与切片（Sequence Indexing and Slicing）
#### 序列 (Sequence)索引 (Sequence Indexing)
序列 (Sequence)中的每个元素都有一个编号，这个编号被称为 **索引 (Index)**。
**索引 (Index)特点**
- **降维 (Dimension Reduction)**：对序列 (Sequence)进行索引 (Index)操作，会使数据的维度 (Dimension)下降。
    - 例如：对 **1维数据**（列表 (List)）进行索引 (Index)，结果为 **0维数据**（单个元素）。

**代码示例 (Code Example)**

```Python
"""
类比0维数据
"""
item1 = 1
item2 = 2
item3 = 3
item4 = 4
item5 = 5
item6 = 6
item7 = 7
item8 = 8
item9 = 9
"""
类比1维数据
"""
lst1 = [item1, item2, item3]
lst2 = [item4, item5, item6]
lst3 = [item7, item8, item9]
## 对1维数据索引，结果为0维数据
print(lst1[0]) # 1
print(lst2[1]) # 5
print(lst3[2]) # 9
```

---
#### 序列 (Sequence)切片 (Sequence Slicing)
切片 (Slicing)操作用于从序列 (Sequence)中提取一个片段。
**语法结构**
`sequence[start : end : step]`
- `start`：起始索引（包含）。默认为 0。
- `end`：结束索引（不包含，开区间）。默认为序列 (Sequence)长度。
- `step`：步长。默认为 1。
    - 正数：从左往右取。
    - 负数：从右往左取（反向）。

**切片 (Slicing)特点**
- **不降维 (Dimension Preservation)**：切片 (Slicing)操作不会改变数据的维度 (Dimension)。
    - 例如：列表 (List)的切片 (Slicing)结果仍然是列表 (List)，字符串 (String)的切片 (Slicing)结果仍然是字符串 (String)。
- **方向一致性**：`start` 到 `end` 的方向必须与 `step` 的方向一致，否则返回空序列 (Sequence)。
**代码示例 (Code Example)**

```Python
string = "0123456789"
"""
特点：索引会降维，切片不会降维
"""
## 无论怎么切片，维度保持不变
print(lst1[::2])      # [1, 3]
print(lst2[1:2])      # [5] (注意这里是列表 [5] 而不是数字 5)
print(lst3[::2][1:2]) # [9]
"""
方向冲突示例：
start到end是从左往右，但step表示从右往左
结果为空
"""
print(string[1: 3: -1]) # ''
"""
常用技巧
"""
## 把该序列倒过来
print(string[::-1]) # '9876543210'
## 把该序列复制一份
print(string[:])    # '0123456789'
## 复杂切片
print(string[2::-1]) # '210'
## 等价写法
print(string[2:-len(string)-1:-1]) # '210'
```

---
### 2.12 `del` 语句（The `del` Statement）
`del` 语句用于删除对象引用 (Reference)。在列表 (List)操作中，它可以用来删除指定位置或片段的元素。
#### 语法
`del object`
#### 应用场景
1. **删除单个元素**：根据索引 (Index)删除。
1. **删除片段**：根据切片 (Slicing)删除多个元素。
1. **删除整个变量 (Variable)**：解除变量 (Variable)名与内存数据的关联。
#### 代码示例 (Code Example)
## 3. 运算符与表达式（Operators and Expressions）
### 3.1 运算符概览（Operator Overview）
#### 11.1 算术运算符 (Arithmetic Operators)

| 运算符 (Operator) | 含义 | 示例 | 结果 |
|---|---|---|---|
| `+` | 加法或序列 (Sequence)拼接 (Concatenation) | `2 + 3` | `5` |
| `-` | 减法 | `5 - 2` | `3` |
| `*` | 乘法或序列 (Sequence)重复 | `"ab" * 2` | `"abab"` |
| `/` | 真除法 (True Division) | `5 / 2` | `2.5` |
| `//` | 向下取整除法 (Floor Division) | `5 // 2` | `2` |
| `%` | 取模 (Modulo) | `5 % 2` | `1` |
| `**` | 幂运算 (Exponentiation) | `2 ** 3` | `8` |

负数参与 `//` 时结果向负无穷方向取整：

```python
print(-5 // 2)  # -3，而不是 -2。
print(-5 % 2)   # 1；Python 保证 a == (a // b) * b + (a % b)。
```

#### 11.2 比较、成员与身份

```python
age = 20
print(18 <= age < 65)  # Python 支持链式比较。

labels = {"cat", "dog"}
print("cat" in labels)       # True
print("bird" not in labels)  # True

value = None
print(value is None)  # True；None 是单例，使用身份判断。
```

#### 11.3 逻辑运算符 (Logical Operators) 与短路 (Short-circuiting)

优先级为 `not` > `and` > `or`。`and` 和 `or` 返回参与运算的对象，不一定返回 `bool`。

```python
configured_name = ""
display_name = configured_name or "untitled"

user = None
# user 为 None 时右侧不会执行，避免访问不存在的属性。
is_admin = user is not None and user.role == "admin"
```

当表达式影响可读性时使用括号，不要依赖读者背诵完整优先级表。

### 3.2 算术运算符（Arithmetic Operators）

|运算符 (Operator)|描述|
|---|---|
|`+`|加|
|`-`|减|
|`*`|乘|
|`/`|除|
|`%`|取模 (求余数)|
|`**`|幂|
|`//`|整除 (相当于 `/` 的结果再向下取整)|

```Python
a = 5
b = 2
print(a + b)  # 7
print(a - b)  # 3
print(a * b)  # 10
print(a / b)  # 2.5
print(a ** b) # 25
print(a // b) # 2
print(a % b)  # 1
print(-15 % 4) # 1
```

### 3.3 比较运算符（Comparison Operators）
- 比较运算符 (Comparison Operator)用于判断两个对象值的大小关系。
- 运算结果会返回布尔值 (`bool`)：`True` 或 `False`。

|运算符 (Operator)|描述|
|---|---|
|`==`|等于|
|`!=`|不等于|
|`>`|大于|
|`<`|小于|
|`>=`|大于或等于|
|`<=`|小于或等于|

```Python
a = 456
b = 456
c = 789
print(a == b)
print(a != c)
print(c > a)
print(b < c)
print(a >= b)
print(a <= b)

# 期望输出:
# True
# True
# True
# True
# True
# True
```

### 3.4 赋值运算符（Assignment Operators）

|运算符 (Operator)|描述|示例说明 (以 `c` 和 `a` 为例)|
|---|---|---|
|`=`|简单的赋值运算符 (Assignment Operator)|`c = a + 2`|
|`+=`|加法赋值运算符 (Assignment Operator)|`c += a` 结果等于 `c = c + a`|
|`-=`|减法赋值运算符 (Assignment Operator)|`c -= a` 结果等于 `c = c - a`|
|`*=`|乘法赋值运算符 (Assignment Operator)|`c *= a` 结果等于 `c = c * a`|
|`/=`|除法赋值运算符 (Assignment Operator)|`c /= a` 结果等于 `c = c / a`|
|`%=`|取模赋值运算符 (Assignment Operator)|`c %= a` 结果等于 `c = c % a`|
|`**=`|幂赋值运算符 (Assignment Operator)|`c **= a` 结果等于 `c = c ** a`|
|`//=`|取整赋值运算符 (Assignment Operator)|`c //= a` 结果等于 `c = c // a`|

```Python
a = 3
c = a + 2
print(c) # 5
c += a   # c = c + a
print(c) # 8
c -= a   # c = c - a
print(c) # 5
c *= a   # c = c * a
print(c) # 15
c /= a   # c = c / a
print(c) # 5.0
c %= a   # c = c % a
print(c) # 2.0
c **= a  # c = c ** a
print(c) # 8.0
c //= a  # c = c // a
print(c) # 2.0
```

### 3.5 增强赋值与对象标识（Augmented Assignment and Object Identity）
- 增强赋值在条件符合的情况下（例如操作数是一个可变数据），会以 `inplace`（原地）的方式来进行处理。
- 而普通赋值则会以新建的方式进行处理。
#### `id(object)` 函数 (Function)
- 返回 `object` 的唯一标识符（内存地址 (Memory Address)）。
- 如果两个对象具有相同的 `id` 值，说明它们为同一对象。

```Python
## 增强赋值示例 (inplace)
lst1 = [1, 2]
lst2 = [3, 4, 5]
print(id(lst1))
lst1 += lst2
print(id(lst1)) # id 不变
print(lst1)
## 普通赋值示例 (新建)
lst1 = [1, 2]
lst2 = [3, 4, 5]
print(id(lst1))
lst1 = lst1 + lst2
print(id(lst1)) # id 改变
print(lst1)
## id 判断是否为同一对象
a = [1, 2, 3, 4]
b = [4, 3, 2, 1]
c = a
print(id(a))
print(id(b))
print(id(c)) # 与 a 的 id 相同

# 输出说明: `id()` 的具体整数由本次运行决定，因此这里只描述恒等关系。
# 期望输出:
# 第 1、2 行 id 相同，随后输出 [1, 2, 3, 4, 5]
# 第 4、5 行 id 不同，随后输出 [1, 2, 3, 4, 5]
# 最后 3 行中，id(a) 与 id(c) 相同，id(b) 不同
```

### 3.6 拼接运算（Concatenation）
- `+`、`+=`、、`=` 同样支持字符串 (`string`)、列表 (`list`)、元组 (`tuple`) 的拼接 (Concatenation)操作。

```Python
## 字符串拼接
str1 = 'hello '
str2 = 'world'
print(str1 + str2)
str1 += str2
print(str1)
str1 = 'hello '
print(str1 * 3)
str1 *= 3
print(str1)
## 列表拼接
lst1 = [1, 2]
lst2 = [3, 4, 5]
print(lst1 + lst2)
lst1 += lst2
print(lst1)
lst1 = [1, 2]
print(lst1 * 3)
lst1 *= 3
print(lst1)
## 元组拼接
tup1 = (1, 2)
tup2 = (3, 4, 5)
print(tup1 + tup2)
tup1 += tup2
print(tup1)
tup1 = (1, 2)
print(tup1 * 3)
tup1 *= 3
print(tup1)

# 期望输出:
# hello world
# hello world
# hello hello hello（实际输出末尾还有一个空格）
# hello hello hello（实际输出末尾还有一个空格）
# [1, 2, 3, 4, 5]
# [1, 2, 3, 4, 5]
# [1, 2, 1, 2, 1, 2]
# [1, 2, 1, 2, 1, 2]
# (1, 2, 3, 4, 5)
# (1, 2, 3, 4, 5)
# (1, 2, 1, 2, 1, 2)
# (1, 2, 1, 2, 1, 2)
```

### 3.7 序列赋值（Sequence Assignment）
#### 基本序列 (Sequence)赋值
- **格式**：`a, b, c, ... = iterable`
- 将 `iterable`（可迭代对象）的元素分别赋值给对应变量 (Variable)，元素和变量 (Variable)的个数需要一致。

```Python
a, b = 3, 4
print(a, b)
a, b, c = [3, 4, 5]
print(a, b, c)
a, b, c, d = '你好吗?'
print(a, b, c, d)

# 期望输出:
# 3 4
# 3 4 5
# 你 好 吗 ?
```

#### 多目标赋值 (Multiple-Target Assignment)
- 将一个对象同时赋值给多个变量 (Variable)。

```Python
## 不可变对象的多目标赋值
a = b = c = 999
print(id(a))
print(id(b))
print(id(c))
## 可变对象的多目标赋值 (多个变量指向同一内存地址)
a = b = c = [1, 2, 3]
print(id(a))
print(id(b))
print(id(c))
b.append(4)
print(a)
print(b)
print(c)

# 输出说明: `id()` 的具体整数由本次运行决定，但同组名称的输出值相同。
# 期望输出:
# 前 3 行 id 相同（整数 999 的三个名称指向同一对象）
# 后 3 行 id 相同（列表的三个名称也指向同一对象）
# [1, 2, 3, 4]
# [1, 2, 3, 4]
# [1, 2, 3, 4]
```

### 3.8 逻辑运算符与短路求值（Logical Operators and Short-circuit Evaluation）

|运算符 (Operator)|描述|
|---|---|
|`and`|布尔"与"（左边 bool 判定为 `False`，返回左边；否则返回右边）|
|`or`|布尔"或"（左边 bool 判定为 `True`，返回左边；否则返回右边）|
|`not`|布尔"非"（判定为 `False`，返回 `True`；判定为 `True`，返回 `False`）|

```Python
a = 2
b = 'hello'
c = []
d = 0
print(c and a) # []
print(a and c) # []
print(d and c) # 0
print(c and d) # []
print(a and b) # 'hello'
print(b and a) # 2
print(a or c)  # 2
print(c or a)  # 2
print(b or a)  # 'hello'
print(a or b)  # 2
print(c or d)  # 0
print(d or c)  # []
print(not a)   # False
print(not b)   # False
print(not c)   # True
print(not d)   # True
## 优先级: not > and > or
print(b and not a or c) # []
```

#### 短路机制 (Short-circuit Mechanism)
- 在逻辑表达式中，由于 `and` 和 `or` 的特点，表达式中的部分内容可能不会执行。

```Python
a = 0
b = 1
c = 0
print(c and b / c) # 0 (不会执行 b / c，避免了除零错误)
print(b or a + c)  # 1 (不会执行 a + c)
## b and a + c      # 这里会执行 a + c (因为b是1，需要继续往右判断)
```

#### `all()` 与 `any()` 函数 (Function)
- **`all(iterable)`**：如果 `iterable` 的所有元素 bool 判定都为 `True`，则返回 `True`。如果 `iterable` 为空，也返回 `True`。
- **`any(iterable)`**：如果 `iterable` 中存在至少一个元素 bool 判定为 `True`，则返回 `True`。如果 `iterable` 为空，也返回 `False`。

```Python
tup = ('0', '', 'None', 'False', '[]')
print(all(tup)) # True (非空字符串都为True)
print(all([]))  # True
tup2 = (0, '', None, False, [])
print(any(tup2)) # False (全是False的等价值)
print(any([]))   # False
```

### 3.9 成员运算符（Membership Operators）
- 成员运算符 (Membership Operator)用于判断某个对象是否为指定 `iterable` 的元素。
- 返回布尔值 (Boolean Value)：`True`，`False`。

|运算符 (Operator)|描述|
|---|---|
|`in`|在其中|
|`not in`|不在其中|

```Python
string = 'hello world'
print('e' in string)
print('lo' in string)
print('ol' not in string)
lst = [True, False, [2, 3], 4]
print(1 in lst)
print(0 in lst)
print(4 in lst)
print(2 not in lst)
print(3 not in lst)
d = {1: 2, 0: 4}
print(True in d)
print(False in d)
print(2 not in d)
print(4 not in d)

# 期望输出:
# True
# True
# True
# True
# True
# True
# True
# True
# True
# True
# True
# True
```

### 3.10 身份运算符（Identity Operators）
- 身份运算符 (Identity Operator)用于判断两个标识符 (Identifier)是不是引用 (Reference)自同一个对象。
- 返回布尔值 (Boolean Value)：`True`，`False`。

|运算符 (Operator)|描述|
|---|---|
|`is`|类似于判断 `id(a) == id(b)`|
|`is not`|类似于判断 `id(a) != id(b)`|

```Python
shared = [257]
alias = shared
independent = [257]

print(shared == alias)        # True：内容相等
print(shared is alias)        # True：引用同一个对象
print(id(shared) == id(alias))  # True

print(shared == independent)  # True：内容相等
print(shared is independent)  # False：是两个独立列表对象
print(id(shared) == id(independent))  # False
```

> [!warning] 整数缓存与常量折叠（Integer Caching and Constant Folding）
> CPython 的小整数缓存 (Small-integer Cache)会复用部分整数对象，但对象复用还会受到解释器实现、交互式环境和编译器常量折叠 (Constant Folding)影响，不能把某个固定整数边界当作 Python 语言保证。比较数值使用 `==`；只有判断 `None` 等单例 (Singleton)时才应依赖 `is`。

### 3.11 运算符优先级（Operator Precedence）
以下表格列出了从高到低优先级的常用运算符 (Operator)：

|运算符 (Operator)|描述|
|---|---|
|`**`|指数 (最高优先级)|
|`*`, `/`, `%`, `//`|乘，除，求余数和取整除|
|`+`, `-`|加法、减法|
|`<=`, `<`, `>`, `>=`|比较运算符 (Comparison Operator)|
|`==`, `!=`|等于运算符 (Operator)|
|`%=`, `/=`, `//=`, `-=`, `+=`, `*=`, `**=`, `=`|赋值运算符 (Assignment Operator)|
|`is`, `is not`|身份运算符 (Identity Operator)|
|`in`, `not in`|成员运算符 (Membership Operator)|
|`not`, `and`, `or`|逻辑运算符 (最低优先级)|

## 4. 控制流程与推导式（Control Flow and Comprehensions）
### 4.1 控制流程概览（Control-flow Overview）

```python
for index, value in enumerate([10, 20, 30], start=1):
    print(index, value)

for name, score in zip(["A", "B"], [0.8, 0.9], strict=True):
    # strict=True 能在两个序列长度不同时尽早报错，避免静默丢数据。
    print(name, score)

# 期望输出:
# 1 10
# 2 20
# 3 30
# A 0.8
# B 0.9
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

# 期望输出:
# found
```

### 4.2 条件语句（Conditional Statements）
#### 1. 格式一 (Format 1)
最基础的条件判断。当判断条件成立时，执行对应代码块。
**语法：**

```Python
if 判断条件:
    执行代码块
```

**代码示例 (Code Example)：**

```Python
age = float(input('请问你今年多少岁?'))
if age >= 18:
    print('你已经成年了!')

# 输出场景: 输入 `20` 时：
# 期望输出:
# 请问你今年多少岁?20
# 你已经成年了!
```
输入小于 `18` 的值时，条件不成立，除输入提示外没有额外输出。

#### 2. 格式二 (Format 2)
当判断条件成立时，执行代码块 1；如果条件不成立，则执行代码块 2。
**语法：**

```Python
if 判断条件:
    执行代码块1
else:
    执行代码块2
```

**代码示例 (Code Example)：**

```Python
age = float(input('请问你今年多少岁?'))
if age >= 18:
    print('你已经成年了!')
else:
    print('你还未成年!')

# 输出场景: 输入 `16` 时：
# 期望输出:
# 请问你今年多少岁?16
# 你还未成年!
```
输入 `18` 或更大值时输出 `你已经成年了!`。

#### 3. 格式三 (Format 3)
多重条件判断。当判断条件 1 成立时执行代码块 1，否则继续判断条件 2，以此类推。如果所有条件都不成立，执行 `else` 下的代码块。
**语法：**

```Python
if 判断条件1:
    执行代码块1
elif 判断条件2:
    执行代码块2
elif 判断条件3:
    执行代码块3
else:
    执行代码块n
```

**代码示例 (Code Example)：**

```Python
score = float(input('你这次考试考了多少分?'))
if score >= 90:
    print('厉害!')
elif score >= 80:
    print('优秀!')
elif score >= 70:
    print('良好!')
elif score >= 60:
    print('及格!')
else:
    print('不及格!')

# 输出场景: 输入 `85` 时：
# 期望输出:
# 你这次考试考了多少分?85
# 优秀!
```
边界分别为：`90` 输出“厉害”，`80` 输出“优秀”，`70` 输出“良好”，`60` 输出“及格”，小于 `60` 输出“不及格”。

#### 4. 三元表达式 (Ternary Expression)
三元表达式用来实现一些简单的条件语句 (Conditional Statement)，会比结构化的代码块更灵活、更简洁。
**代码示例 (Code Example)：**

```Python
age = float(input('请问你今年多少岁?'))
print('你已经成年了!') if age >= 18 else print('你还未成年!')

score = float(input('你这次考试考了多少分?'))
print('厉害!') if score >= 90 else \
print('优秀!') if score >= 80 else \
print('良好!') if score >= 70 else \
print('及格!') if score >= 60 else \
print('不及格!')

# 输出场景: 依次输入年龄 `20` 和分数 `85` 时：
# 期望输出:
# 请问你今年多少岁?20
# 你已经成年了!
# 你这次考试考了多少分?85
# 优秀!
```

---
### 4.3 循环语句（Loop Statements）
#### 1. `while` 循环（`while` Loop）

```Python
count = 0
while count < 3:
    print(count)
    count += 1

# 期望输出:
# 0
# 1
# 2
```

**搭配 else 使用：**
当 `while` 循环正常结束（即条件变为 `False`）时，会执行 `else` 代码块。如果是被 `break` 打断，则不会执行 `else`。

```Python
count = 0
while count < 3:
    print(count)
    count += 1
else:
    print('循环正常结束')

# 期望输出:
# 0
# 1
# 2
# 循环正常结束
```

#### 2. break 与 continue 语句
- **`break`**：直接终止并跳出整个循环。
- **`continue`**：跳过当前这一轮循环的剩余代码，直接进入下一轮循环的条件判断。
**代码示例 (Code Example)：**

```Python
## break 示例
count = 0
while count < 5:
    if count == 3:
        break  # 当 count 等于 3 时，直接终止整个循环
    print(count)
    count += 1
## continue 示例
count = 0
while count < 5:
    count += 1
    if count == 3:
        continue  # 当 count 等于 3 时，跳过本次 print，进入下一轮
    print(count)

# 输出场景: 第一个循环在 `count == 3` 时终止；第二个循环跳过 `3`：
# 期望输出:
# 0
# 1
# 2
# 1
# 2
# 4
# 5
```

#### 3. for 循环 (For Loop)
`for` 循环主要用于遍历序列（如字符串 (String)、列表 (List)、元组 (Tuple)等）或可迭代对象。
**代码示例 (Code Example)：**

```Python
## 遍历字符串
for char in 'hello':
    print(char)
## 遍历列表
lst = ['apple', 'banana', 'cherry']
for item in lst:
    print(item)
## for...else 结构
for item in lst:
    print(item)
else:
    print('遍历完成')

# 期望输出:
# h
# e
# l
# l
# o
# apple
# banana
# cherry
# apple
# banana
# cherry
# 遍历完成
```

#### 4. 嵌套循环 (Nested Loops)
在一个循环体内部，又包含了另一个完整的循环。
**代码示例 (Code Example)：**

```Python
for x in range(1, 4):
    for y in range(1, 4):
        print(f"x={x}, y={y}")

# 期望输出:
# x=1, y=1
# x=1, y=2
# x=1, y=3
# x=2, y=1
# x=2, y=2
# x=2, y=3
# x=3, y=1
# x=3, y=2
# x=3, y=3
```

---
### 4.4 推导式与生成器表达式（Comprehensions and Generator Expressions）
#### 推导式与惰性生成概览（Comprehension and Lazy-generation Overview）

```python
squares = [number**2 for number in range(10) if number % 2 == 0]
mapping = {name: len(name) for name in ["numpy", "pandas"]}
unique_lengths = {len(name) for name in ["a", "bb", "cc"]}
```

推导式适合短而清晰的转换；包含多层条件或副作用时改用普通循环。

生成器表达式 (Generator Expression)按需产生数据：

```python
total = sum(number**2 for number in range(1_000_000))
```

推导式提供了一种简洁的方式来创建数据集合 (Set)，可以替代简单的 `for` 循环结构。
#### 1. 列表推导式 (List Comprehension)
- **格式 1**：`[x for子句]`
- **格式 2**：`[x for子句 更多的for子句或者if子句]`
**代码示例 (Code Example)：**

```Python
## 示例 1
lst = [x ** 2 for x in range(4)]
print(lst)
## 类比普通的 for 循环写法:
lst = []
for x in range(4):
    lst.append(x ** 2)
print(lst)
## 示例 2：带有 if 和多个 for 子句
lst = [x + y for x in range(5) if x % 2 for y in (1, 2, 3)]
print(lst)
## 类比普通的嵌套循环写法:
lst = []
for x in range(5):
    if x % 2:
        for y in (1, 2, 3):
            lst.append(x + y)
print(lst)

# 期望输出:
# [0, 1, 4, 9]
# [0, 1, 4, 9]
# [2, 3, 4, 4, 5, 6]
# [2, 3, 4, 4, 5, 6]
```

#### 2. 字典推导式 (Dictionary Comprehension)
- **格式 1**：`{k: v for子句}`
- **格式 2**：`{k: v for子句 更多的for子句或者if子句}`
**代码示例 (Code Example)：**

```Python
## 示例 1
d = {x: x**2 for x in range(4)}
print(d)
## 类比普通的 for 循环写法:
d = {}
for x in range(4):
    d[x] = x ** 2
print(d)
## 示例 2：带有多个 for 和 if 子句
d = {x: v for x in range(4) for v in range(9) if v % 2}
print(d)
## 类比普通的嵌套循环写法:
d = {}
for x in range(4):
    for v in range(9):
        if v % 2:
            d[x] = v
print(d)

# 期望输出:
# {0: 0, 1: 1, 2: 4, 3: 9}
# {0: 0, 1: 1, 2: 4, 3: 9}
# {0: 7, 1: 7, 2: 7, 3: 7}
# {0: 7, 1: 7, 2: 7, 3: 7}
```

## 5. 函数、参数、迭代与作用域（Functions, Parameters, Iteration, and Scope）
### 5.1 函数定义、调用与返回值（Function Definition, Calls, and Return Values）

```python
def calculate_mean(values: list[float]) -> float:
    """返回非空数值列表的平均值。"""
    if not values:
        raise ValueError("values 不能为空")
    return sum(values) / len(values)
```

常见参数 (Parameter)形式：

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

可变参数 (Parameter)：

```python
def summarize(*values: float, precision: int = 2, **metadata) -> dict:
    return {
        "mean": round(sum(values) / len(values), precision),
        "metadata": metadata,
    }
```

#### 可变默认参数 (Default Parameter)陷阱

```python
def add_sample(sample, samples=None):
    # 默认值只在函数定义时创建一次；使用 None 才能为每次调用建立新列表。
    if samples is None:
        samples = []
    samples.append(sample)
    return samples
```

#### 1. 定义函数 (Define Function)
**语法格式：**

```text
def func_name([arg1 [, arg2, ... argN]]):
    func_body
```
- **形参 (Formal Parameter)**：函数 (Function)定义时声明的参数 (Parameter)。
- **实参 (Actual Parameter)**：函数 (Function)调用时传入的参数 (Parameter)。
- 函数 (Function)只需要定义一次，就可以被多次使用。
- 当函数 (Function)被调用时，才执行函数 (Function)体，定义时不执行。
**代码示例：**

```Python
def plus(num):
    print(num + 1)
## 调用函数
plus(2)  # 3
plus(5)  # 6
f = plus
print(plus)  # 输出形如: <function plus at 0x...>
print(f)     # 输出相同函数对象，地址与上一行一致
f(2)     # 3
f(5)     # 6

# 期望输出:
# 3
# 6
# <function plus at 0x...>
# <function plus at 0x...>  # 与上一行地址相同
# 3
# 6
```

#### 2. return 用法 (Return Usage)
- 把后面跟着的对象返回给函数 (Function)调用方，并结束所在的函数 (Function)。
- `return` 后面可以跟一个对象、多个对象，甚至不跟任何对象。
- `return` 后面什么都不跟，等价于 `return None`。
- 函数 (Function)执行时，没有遇到 `return`，也等价于 `return None`。
**代码示例：**

```Python
## 返回一个对象
def add1(left, right):
    res = left + right
    return res
def add2(left, right):
    return left + right
## 返回多个对象，自动打包成一个元组 (Tuple)
def add3(left, right):
    res1 = left + right
    res2 = left * right
    return res1, res2
def add4(left, right):
    return left + right, left * right
## return None
def add5(left, right):
    print(left + right)
    return
## 没有 return，也等价于 return None
def add6(left, right):
    pass
print(add1(3, 4))
print(add3(3, 4))
print(add5(3, 4))
print(add6(3, 4))

# 期望输出:
# 7
# (7, 12)
# 7
# None
# None
```

---
### 5.2 参数类型与传递规则（Parameter Types and Passing Semantics）
#### 完整参数分类（Complete Parameter Classification）

```python
def example(positional_only, /, regular, *args, keyword_only, **kwargs):
    return positional_only, regular, args, keyword_only, kwargs

result = example(1, 2, 3, 4, keyword_only=5, debug=True)
```
- `/` 前是仅位置参数 (Positional-only Parameters)。
- 普通参数 (Parameter)可按位置或名称传递。
- `*args` 收集额外位置参数 (Positional Argument)，类型是元组 (Tuple)。
- `*` 或 `*args` 后是仅关键字参数 (Keyword-only Parameters)。
- `**kwargs` 收集额外关键字参数 (Keyword Argument)，类型是字典 (Dictionary)。

参数 (Parameter)定义顺序大致为：仅位置 → 普通 → 可变位置 → 仅关键字 (Keyword) → 可变关键字 (Keyword)。

##### 参数 (Parameter)传递与可变对象 (Mutable Object)

Python 使用对象共享传递 (Call by Sharing)：函数 (Function)获得的是同一个对象的引用 (Reference)副本 (Copy)。

```python
def mutate(values: list[int]) -> None:
    values.append(99)  # 修改共享的列表对象，调用方能够看到。

def rebind(values: list[int]) -> None:
    values = [99]  # 只让局部名称指向新列表，不影响调用方名称。
```

#### 1. 位置参数 (Positional Argument)
- 调用函数 (Function)时，根据函数 (Function)定义的参数 (Parameter)位置来传递参数 (Parameter)。
#### 2. 关键字参数 (Keyword Argument)
- 使用 `key = value` 的形式传递参数 (Parameter)，可以不按顺序。
- **注意**：如果混用，位置参数 (Positional Argument)必须在关键字参数 (Keyword Argument)之前。
**代码示例：**

```Python
def add(x, y, z):
    return x + y + z
## 位置参数
print(add(1, 2, 3))  # 6
## 关键字参数
print(add(x=1, y=2, z=3))  # 6
print(add(z=3, x=1, y=2))  # 6
## 混用 (位置参数在前)
print(add(1, z=3, y=2))  # 6
```

#### 3. 默认参数 (Default Argument)
- 在定义函数 (Function)时，为形参 (Formal Parameter)指定默认值。
- 如果调用时没有传入该参数 (Parameter)，则使用默认值。
- **注意**：默认参数 (Default Parameter)必须放在非默认参数 (Default Parameter)之后。
**代码示例：**

```Python
def add(x, y, z=10):
    return x + y + z
print(add(1, 2))     # 1+2+10 = 13
print(add(1, 2, 3))  # 1+2+3 = 6
```

---
### 5.3 可变数量参数（Variadic Arguments）
#### 1. `args`
- 接收任意多个位置参数 (Positional Argument)，并将其打包成一个元组 (Tuple)。
**代码示例：**

```Python
def func(*args):
    print(args)
    print(type(args))
func(1, 2, 3)

# 期望输出:
# (1, 2, 3)
# <class 'tuple'>
```

#### 2. `*kwargs`
- 接收任意多个关键字参数 (Keyword Argument)，并将其打包成一个字典 (Dictionary)。
**代码示例：**

```Python
def func(**kwargs):
    print(kwargs)
    print(type(kwargs))
func(a=1, b=2, c=3)

# 期望输出:
# {'a': 1, 'b': 2, 'c': 3}
# <class 'dict'>
```

---
### 5.4 封包与解包（Packing and Unpacking）
- **封包 (Packing)**：将多个值合并 (Merge)为一个容器（如元组 (Tuple)或字典 (Dictionary)）。
- **解包 (Unpacking)**：将容器中的元素提取出来。
**代码示例：**

```Python
## 解包元组/列表
def add(x, y, z):
    return x + y + z
lst = [1, 2, 3]
print(add(*lst)) # 等价于 add(1, 2, 3)
## 解包字典
dic = {'x': 1, 'y': 2, 'z': 3}
print(add(**dic)) # 等价于 add(x=1, y=2, z=3)
## 综合示例
def func(*args, **kwargs):
    print(args)
    print(kwargs)
func(1, 2, a=3, b=4)

# 期望输出:
# 6
# 6
# (1, 2)
# {'a': 3, 'b': 4}
```

---
### 5.5 迭代协议与惰性计算（Iteration Protocol and Lazy Evaluation）

可迭代对象 (Iterable) 能产生迭代器 (Iterator)；迭代器 (Iterator)保存当前位置，并通过 `next()` 逐个返回元素。

```python
values = [10, 20, 30]
iterator = iter(values)

print(next(iterator))
print(next(iterator))

# 期望输出:
# 10
# 20
```

生成器 (Generator)函数 (Generator Function) 使用 `yield` 暂停并保存状态：

```python
def read_batches(items, batch_size: int):
    if batch_size <= 0:
        raise ValueError("batch_size 必须大于 0")

    for start in range(0, len(items), batch_size):
        # 每次只生成一个批次，调用方不需要等待所有结果先放入列表。
        yield items[start : start + batch_size]
```

生成器 (Generator)通常只能消费一次；需要重复遍历时重新创建生成器 (Generator)或保存结果。

#### `StopIteration`、`for` 循环与 `generator.send()`

迭代器耗尽时，`next()` 会抛出 `StopIteration`；`for` 循环内部会捕获该异常并正常结束。迭代器的 `__iter__()` 返回自身，因此它既能被 `next()` 推进，也能直接交给 `for`。

```python
iterator = iter([10, 20])

print(iter(iterator) is iterator)  # True
print(next(iterator))  # 10
print(next(iterator))  # 20
print(next(iterator, "结束"))  # 结束；默认值可避免 StopIteration 向外传播
```

`generator.send(value)` 会恢复生成器，并让暂停位置的 `yield` 表达式得到 `value`。生成器尚未运行到第一个 `yield` 时没有接收位置，因此首次启动只能调用 `next(generator)` 或 `generator.send(None)`。

```python
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            return total
        total += value


generator = accumulator()
print(next(generator))  # 0；先运行到第一个 yield
print(generator.send(5))  # 5；5 成为 yield 表达式的结果
print(generator.send(3))  # 8
generator.close()  # 在暂停点抛出 GeneratorExit，用于主动结束生成器。
```

> [!warning] 首次发送非 `None` 值
> 对刚创建的生成器直接调用 `generator.send(5)` 会抛出 `TypeError`。`send()` 的返回值是生成器下一次 `yield` 产生的值；若生成器在此之前结束，则会抛出 `StopIteration`。

### 5.6 命名空间（Namespace）
命名空间 (Namespace)是名字到对象的映射。Python 中大多数命名空间 (Namespace)都是通过字典 (Dictionary)实现的。
#### 1. 分类
- **内置命名空间 (Built-in Namespace)**：包含内置函数 (Function)如 `abs`, `str`, `int` 等。在 Python 解释器 (Interpreter)启动时创建，退出时销毁。
- **全局命名空间 (Global Namespace)**：模块 (Module)级别的名字。在模块 (Module)被读入时创建。
- **局部命名空间 (Local Namespace)**：函数 (Function)内部的名字。在函数 (Function)被调用时创建，函数 (Function)执行完毕销毁。
### 5.7 作用域与闭包（Scope and Closure）
#### 闭包与名称解析补充（Closures and Name Resolution）

名称查找遵循 LEGB：Local → Enclosing → Global → Built-in。

```python
def make_multiplier(factor: float):
    def multiply(value: float) -> float:
        # factor 来自外层函数作用域，形成闭包。
        return value * factor

    return multiply

double = make_multiplier(2)
print(double(5))  # 输出: 10
```

优先通过参数 (Parameter)和返回值 (Return Value)传递数据，尽量避免 `global`。`nonlocal` 只在确实需要修改闭包 (Closure)变量 (Variable)时使用。
作用域 (Scope)是指 Python 程序可以直接访问命名空间 (Namespace)的区域。
#### 1. 分类 (L-E-G-B 规则)
1. **局部作用域 (Local) - L**：函数 (Function)内部。
1. **闭包 (Closure)函数 (Function)外的函数 (Function)中 (Enclosing) - E**：嵌套函数 (Function)的外层。

```Python
def outer():
    num = 10
    def inner():
        nonlocal num # 声明使用外层函数的局部变量
        num = 100
        print(num)
    inner()
    print(num)
outer()

# 期望输出:
# 100
# 100
```

#### 2. `global` 关键字 (Keyword)
- 用于在函数 (Function)内部声明全局变量 (Variable)，从而可以修改全局作用域 (Global Scope)中的变量 (Variable)。
**代码示例：**

```Python
num = 1
def fun1():
    global num # 声明使用全局变量
    print(num)
    num = 123
    print(num)
fun1()
print(num)

# 期望输出:
# 1
# 123
# 123
```

#### 3. `nonlocal` 关键字 (Keyword)
- 用于在嵌套函数 (Function)中，声明外层非全局作用域 (Global Scope)中的变量 (Variable)。
**代码示例：**

```Python
def outer():
    num = 10
    def inner():
        nonlocal num # 声明使用外层函数的局部变量
        num = 100
        print(num)
    inner()
    print(num)
outer()

# 期望输出:
# 100
# 100
```

#### 4. 装饰器（Decorator）
装饰器（Decorator）是“接收可调用对象（Callable）并返回新可调用对象”的函数，常用于鉴权、日志、缓存和计时。它通常利用闭包（Closure）保存被装饰函数，并在不修改目标函数主体的情况下增加行为。

`@decorator` 是 `target = decorator(target)` 的语法糖（Syntactic Sugar）。多个装饰器：
```python
@outer
@inner
def target():
    pass
```
等价于 `target = outer(inner(target))`：
- **装饰阶段（Decoration Phase）**：定义函数时先执行靠近函数的 `inner(target)`，再执行 `outer(...)`。
- **调用阶段（Call Phase）**：调用包装后的 `target()` 时先进入 `outer` 的包装函数，再进入 `inner` 的包装函数，最后执行原函数。

```python
from functools import wraps

def check_login(func):
    @wraps(func)  # 保留原函数名称和文档，避免调试、测试与反射信息被包装器覆盖。
    def wrapper(*args, **kwargs):
        print("校验登录")
        return func(*args, **kwargs)
    return wrapper

def check_code(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("校验验证码")
        return func(*args, **kwargs)
    return wrapper

@check_login
@check_code
def comment(content):
    print(f"发表评论：{content}")

comment("Python 很清晰")
# 期望输出:
# 校验登录
# 校验验证码
# 发表评论：Python 很清晰
```

包装器使用 `*args` 和 `**kwargs` 转发任意参数，并返回原函数结果；如果漏掉返回值，原本有返回值的函数经过装饰后会意外变成返回 `None`。

## 6. 完成检查（Checklist）

- [ ] 能解释变量 (Variable)引用 (Reference)、可变对象 (Mutable Object)和浅复制 (Shallow Copy)。
- [ ] 能根据任务选择 list、tuple、dict 或 set。
- [ ] 能正确使用切片 (Slicing)、解包、`enumerate` 和 `zip`。
- [ ] 能编写带类型提示、边界检查和清晰返回值 (Return Value)的函数 (Function)。
- [ ] 能避免覆盖内置名称、可变默认参数 (Default Parameter)和错误 (Error)使用 `is`。
- [ ] 能用 `keyword` 查询当前解释器的关键字 (Keyword)与软关键字 (Soft Keyword)。
- [ ] 能区分 `math`、`random` 与 `secrets` 的用途和安全边界。
- [ ] 能解释迭代器耗尽、`StopIteration` 以及 `generator.send()` 的首次启动约束。
- [ ] 能解释装饰阶段与调用阶段的顺序，并用 `functools.wraps`、`*args`、`**kwargs` 正确编写装饰器。

## 参考资料（References）

- [Python 官方教程](https://docs.python.org/3/tutorial/)
- [Python 风格指南 PEP 8](https://peps.python.org/pep-0008/)
- [Python 标准库：`keyword`](https://docs.python.org/3/library/keyword.html)
- [Python 标准库：`math`](https://docs.python.org/3/library/math.html)
- [Python 标准库：`random`](https://docs.python.org/3/library/random.html)
- [Python 语言参考：Yield expressions](https://docs.python.org/3/reference/expressions.html#yield-expressions)
