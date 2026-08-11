---
title: NumPy 数值计算（NumPy）
aliases:
  - NumPy
status: review
detail_level: comprehensive
merge_policy: union-zero-loss
reviewed_at: 2026-08-11
source:
  - Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/NumPy.md
suggested_target: Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/07-NumPy 数值计算（NumPy）.md
operation: 新建
merge_target: null
---

# NumPy 数值计算（NumPy）

> [!important] 完整性与合并 (Merge)原则（Completeness and Merge Policy）
> 本稿以 Inbox 原稿的逐段信息为基线，并把上一版 Review 的补充知识按主题嵌入相邻章节。仅调整标题层级、纠正明显错误 (Error)和移除完全重复内容；参数 (Parameter)、示例、边界条件、异常 (Exception)说明与原注释均保留。

- **来源原稿（Source Note）**：`Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/NumPy.md`
- **合并 (Merge)方式（Merge Method）**：取并集（Union），原稿细节 + Review 补充。
- **状态（Status）**：仅供 Review 校准，未写入 Notes。

### 一、 NumPy 简介 (Introduction)

#### 结构化补充（Structured Supplement）：常见错误 (Error)

- 混淆 `*` 与 `@`。
- 不知道切片 (Slicing)共享原数组 (Array)数据。
- 忽略整数 (Integer)除法、类型提升或低精度溢出。
- 只看元素数量，不检查轴 (Axis)顺序。
- 用 Python 循环替代本可向量化 (Vectorization)的操作。
- 使用 `np.empty()` 后忘记初始化其中的数据。

NumPy (Numerical Python) 是 Python 进行科学计算 (Scientific Computing) 的一个扩展库，提供了大量的函数 (Function)和操作，主要用于对多维数组 (Array)执行计算，它比 Python 自身的嵌套列表 (List)结构要高效得多。
**NumPy 数组 (Array) 和 Python 列表 (List) 的主要区别:**
- 数组 (Array)会对元素的数据类型 (Data Type)做统一，而列表 (List)不会。
- 数组 (Array)创建后具有固定大小，而列表 (List)由于内存自动管理，可动态调整。
---
### 二、 创建数组 (Array)与属性 (Creating Arrays and Attributes)

#### 结构化补充（Structured Supplement）：创建数组 (Array)

```python
import numpy as np

zeros = np.zeros((2, 3), dtype=np.float32)
ones = np.ones((2, 3))
filled = np.full((2, 3), 7)

integers = np.arange(0, 10, 2)
points = np.linspace(0.0, 1.0, num=5)
identity = np.eye(3)
```

`arange()` 更适合整数 (Integer)步长；需要指定区间内固定数量的浮点数 (Floating-point Number)时优先 `linspace()`。

#### 1. 创建数组 (Array)
`np.array(object, dtype=None)`
- `object`: `array_like`，类似于数组 (Array)的对象。如果 `object` 是标量 (Scalar)，则返回包含 `object` 的 0 维数组 (Array)。
- `dtype`: `data-type`，数据类型 (Data Type)。如果没有给出，会从输入数据推断数据类型 (Data Type)。
- **作用**: 创建一个数组 (Array)对象并返回 (`ndarray` 实例对象 (Instance Object))。

```Python
import numpy as np
num = 789
arr = np.array(num)
print(num)
print(arr)
print(type(num))
print(type(arr))
## 789
## 789
## <class 'int'>
## <class 'numpy.ndarray'>
lst = [6, 7, 1, 0, 9, 8]
arr = np.array(lst)
print(lst)
print(arr)
lst = [[6, 7, 1], [0, 9, 8]]
arr = np.array(lst)
print(lst)
print(arr)
## [6, 7, 1, 0, 9, 8]
## [6 7 1 0 9 8]
lst = [[[6, 7], [1, 0], [9, 8]]]
arr = np.array(lst)
print(lst)
print(arr)
## [[6, 7, 1], [0, 9, 8]]
## [[6 7 1]
##  [0 9 8]]
## [[[6, 7], [1, 0], [9, 8]]]
## [[[6 7]
##   [1 0]
##   [9 8]]]
```

#### 2. DTYPE 常用值 (Common Data Types)

##### 结构化补充（Structured Supplement）：数据类型 (Data Types) 与类型转换 (Type Casting)

常见数据类型 (Data Types)：

| 类别 | 常见 `dtype` | 说明 |
|---|---|---|
| 有符号整数 (Signed Integer) | `int8`、`int16`、`int32`、`int64` | 位数决定可表示范围 |
| 无符号整数 (Unsigned Integer) | `uint8`、`uint16`、`uint32` | 图像像素常见 `uint8` |
| 浮点数 (Floating Point) | `float16`、`float32`、`float64` | 精度、内存和速度不同 |
| 复数 (Complex Number) | `complex64`、`complex128` | 实部和虚部均为浮点数 (Floating-point Number) |
| 布尔值 (Boolean) | `bool_` | 常用于掩码 (Mask) |
| 字符串 (String) | `str_`、`bytes_` | 长度通常固定在数组 (Array) `dtype` 中 |

```python
import numpy as np

values = np.array([1.2, 2.8, -3.4])
integers = values.astype(np.int32)

# 浮点转整数会截断小数部分，不会四舍五入。
print(integers)  # [ 1  2 -3]
```

先四舍五入再转换：

```python
rounded = np.rint(values).astype(np.int32)
```

> [!warning] 整数 (Integer)溢出 (Integer Overflow)
> 固定位数整数 (Integer)超过范围时可能回绕。处理像素累加、计数和大索引 (Index)时要确认 `dtype`。

```python
pixels = np.array([250, 10], dtype=np.uint8)
print(pixels.sum())  # 聚合通常提升类型，但逐元素运算仍需检查 dtype。

safe_pixels = pixels.astype(np.int16)
print(safe_pixels + 20)

# 期望输出:
# 260
# [270  30]
```

|DTYPE 常用值|描述 (Description)|
|---|---|
|`np.int8`|有符号整数 (1个字节)|
|`np.int16`|有符号整数 (2个字节)|
|`np.int32`|有符号整数 (4个字节)|
|`np.int64`|有符号整数 (8个字节)|
|`np.uint8`|无符号整数 (1个字节)|
|`np.uint16`|无符号整数 (2个字节)|
|`np.uint32`|无符号整数 (4个字节)|
|`np.uint64`|无符号整数 (8个字节)|
|`np.float16`|半精度浮点数 (2个字节)|
|`np.float32`|单精度浮点数 (4个字节)|
|`np.float64`|双精度浮点数 (8个字节)|

#### 3. NDARRAY 常用属性 (NDARRAY Attributes)

##### 结构化补充（Structured Supplement）：`ndarray` 的核心属性

NumPy 的核心是同质多维数组 (Array) `ndarray`。同一数组 (Array)中的元素通常共享一个 `dtype`，因此它能进行高效的向量化 (Vectorization)运算。

```python
import numpy as np

array = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32)

print(array.shape)   # (2, 3)
print(array.ndim)    # 2
print(array.size)    # 6
print(array.dtype)   # float32
print(array.itemsize)  # 4（float32 的每个元素占 4 字节）
```

在深度学习代码中，先检查 `shape`、`dtype` 和设备，往往比直接修改模型更快定位问题。

##### 结构化补充（Structured Supplement）：内存布局 (Memory Layout) 与性能

NumPy 数组 (Array)通常以连续内存 (Contiguous Memory)存储。转置 (Transpose)和切片 (Slicing)可能创建非连续视图 (Non-contiguous View)，某些底层库需要连续数组 (Array)。

```python
array = np.arange(12).reshape(3, 4)
transposed = array.T

print(array.flags["C_CONTIGUOUS"])
print(transposed.flags["C_CONTIGUOUS"])

contiguous = np.ascontiguousarray(transposed)

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

优化顺序：

1. 先选择正确算法和数据结构。
2. 用向量化 (Vectorization) 替代 Python 层逐元素循环。
3. 避免不必要的副本 (Copy) 和类型转换 (Type Casting)。
4. 测量真实瓶颈后再优化内存布局 (Memory Layout)。

|属性名|描述 (Description)|
|---|---|
|`ndarray.ndim`|秩 (Rank)，即轴 (Axis)的数量或维度 (Dimension)的数量|
|`ndarray.shape`|数组 (Array)的形状|
|`ndarray.size`|数组 (Array)中数据的总个数|
|`ndarray.dtype`|数组 (Array)中的数据类型 (Data Type)|
|`ndarray.itemsize`|数组 (Array)中的数据大小，以字节为单位|

```Python
import numpy as np
lst = [[6, 7, 1], [0, 9, 8]]
arr = np.array(lst)
print(arr.ndim)
print(arr.dtype)
print(arr.itemsize)
print(arr.shape)
print(arr.size)
## 2
## int64
## 8
## (2, 3)
## 6
```

---
### 三、 生成数组 (Generating Arrays)
#### 1. `np.arange([start,] stop[, step])`
返回给定区间内的均匀间隔值构成的数组 (Array)。

```Python
import numpy as np
print(np.arange(3))
print(np.arange(3.0))
print(np.arange(3, 7))
print(np.arange(3, 7, 2))
print(np.arange(7, 3, -2))
print(np.arange(3, 7, 0.5))
## [0 1 2]
## [0. 1. 2.]
## [3 4 5 6]
## [3 5]
## [7 5]
## [3.  3.5 4.  4.5 5.  5.5 6.  6.5]
```

#### 2. `np.linspace(start, stop, num=50, dtype=None)`
把给定区间分成 `num` 个均匀间隔的样本，构成数组 (Array)并返回。
- `num`: 生成的样本数量。
- `dtype`: 默认自动推断数据类型 (Data Type)，推断出的 `dtype` 永远不会是整数 (Integer)；即使参数 (Parameter)会产生一个整数 (Integer)数组 (Array)，也会选择 `np.float64`。

```Python
import numpy as np
print(np.linspace(1, 50))
print(np.linspace(1, 10, num=10))
print(np.linspace(1, 10, num=10, dtype=np.int32))
## [ 1.  2.  3.  4.  5.  6.  7.  8.  9. 10. 11. 12. 13. 14. 15. 16. 17. 18.
##  19. 20. 21. 22. 23. 24. 25. 26. 27. 28. 29. 30. 31. 32. 33. 34. 35. 36.
##  37. 38. 39. 40. 41. 42. 43. 44. 45. 46. 47. 48. 49. 50.]
## [ 1.  2.  3.  4.  5.  6.  7.  8.  9. 10.]
## [ 1  2  3  4  5  6  7  8  9 10]
```

---
### 四、 基本运算与广播机制 (Basic Operations and Broadcasting)

#### 结构化补充（Structured Supplement）：向量化 (Vectorization)运算

```python
import numpy as np

values = np.array([1.0, 2.0, 3.0])

normalized = (values - values.mean()) / values.std()
clipped = np.clip(values, 1.5, 2.5)
mask = values > 1.5
```

优先数组 (Array)运算，不要把 NumPy 当作普通列表 (List)逐元素循环；向量化 (Vectorization)通常更简洁，也能利用底层优化。

#### 结构化补充（Structured Supplement）：广播（Broadcasting）

NumPy 从最后一个维度 (Dimension)开始比较形状；两个维度 (Dimension)相等，或其中一个为 `1` 时可以广播 (Broadcasting)。缺失的前导维度 (Dimension)视为 `1`。

```python
import numpy as np

matrix = np.array([[1, 2, 3], [4, 5, 6]])  # (2, 3)
column_means = matrix.mean(axis=0)           # (3,)
centered = matrix - column_means             # (2, 3) - (3,) 可以广播。
```

无法广播 (Broadcasting)的例子：`(2, 3)` 与 `(2,)`，因为最后一维 `3` 和 `2` 既不相等，也没有一个是 `1`。

基本运算：数组 (Array)的算术运算和比较运算为逐元素操作 (Element-wise Operations)。
**广播机制 (Broadcasting):** 后缘维度 (Dimension)相同或者不同的维度 (Dimension)有1，可以广播 (Broadcasting)。

```Python
import numpy as np
a = np.array([[1, 2], [3, 4], [5, 6]])
print(a + 2)        # [[3 4]
                    #  [5 6]
                    #  [7 8]]
print(a - 2)        # [[-1  0]
                    #  [ 1  2]
                    #  [ 3  4]]
print(a * 2)        # [[ 2  4]
                    #  [ 6  8]
                    #  [10 12]]
print(a / 2)        # [[0.5 1. ]
                    #  [1.5 2. ]
                    #  [2.5 3. ]]
print(a < 4)        # [[ True  True]
                    #  [ True False]
                    #  [False False]]
print(a > 3)        # [[False False]
                    #  [False  True]
                    #  [ True  True]]
b = np.array([[2, 2], [2, 1], [1, 1]])
print(a + b)        # [[3 4]
                    #  [5 5]
                    #  [6 7]]
print(a - b)        # [[-1  0]
                    #  [ 1  3]
                    #  [ 4  5]]
print(a * b)        # [[2 4]
                    #  [6 4]
                    #  [5 6]]
print(a / b)        # [[0.5 1. ]
                    #  [1.5 4. ]
                    #  [5.  6. ]]
print(a < b)        # [[ True False]
                    #  [False False]
                    #  [False False]]
print(a > b)        # [[False False]
                    #  [ True  True]
                    #  [ True  True]]
## 广播机制示例
a = np.arange(24).reshape((2, 3, 4))
b = np.arange(12).reshape((3, 4))
c = np.arange(4).reshape((1, 4))
d = np.arange(4).reshape(4)
e = np.arange(12).reshape((1, 3, 4))
f = np.arange(6).reshape((2, 3, 1))
g = np.arange(2).reshape((2, 1, 1))
h = np.arange(2).reshape((1, 2, 1, 1))
i = np.arange(10).reshape((5, 2, 1, 1))
print((a + b).shape)  # (2, 3, 4)
print((a + c).shape)  # (2, 3, 4)
print((a + d).shape)  # (2, 3, 4)
print((a + e).shape)  # (2, 3, 4)
print((a + f).shape)  # (2, 3, 4)
print((a + g).shape)  # (2, 3, 4)
print((a + h).shape)  # (1, 2, 3, 4)
print((a + i).shape)  # (5, 2, 3, 4)
```

---
### 五、 索引 (Index)和切片 (Indexing and Slicing)

#### 结构化补充（Structured Supplement）：索引 (Index)、切片 (Slicing)、视图 (View)与副本 (Copy)

```python
import numpy as np

array = np.arange(12).reshape(3, 4)

print(array[1, 2])
print(array[:, 1])
print(array[1:, :2])
print(array[array % 2 == 0])  # 布尔索引。

# 期望输出:
# 6
# [1 5 9]
# [[4 5]
#  [8 9]]
# [ 0  2  4  6  8 10]
```

> [!warning] 切片 (Slicing)通常是视图 (View)
> 修改切片 (Slicing)可能同时修改原数组 (Array)。需要独立数据时显式调用 `.copy()`。

```python
view = array[:, :2]
view[0, 0] = 999
print(array[0, 0])  # 999

independent = array[:, :2].copy()
independent[0, 0] = -1
```

基础切片 (Slicing)通常返回视图 (View)；整数 (Integer)数组 (Array)索引 (Index)和布尔索引 (Boolean Indexing)通常返回副本 (Copy)。不要仅凭变量 (Variable)名判断是否共享内存。

数组 (Array)除了支持 Python 序列 (Sequence)的索引 (Index)和切片 (Slicing)操作以外，还可以针对各个轴 (Axis)进行索引 (Index)和切片 (Slicing)操作。
#### 1. 序列 (Sequence)索引 (Index)和切片 (Slicing)
返回视图 (View)，修改切片 (Slicing)会影响原数组 (动态性)。

```Python
import numpy as np
lst = [6, 8, 9, 1, 3]
arr = np.array(lst)
print(lst)        # [6, 8, 9, 1, 3]
print(arr)        # [6 8 9 1 3]
item_lst = lst[2]       # 获取单个元素（值拷贝）
part_lst = lst[2:3]     # 切片返回新列表（副本）
item_arr = arr[2]       # 获取单个元素（值拷贝）
part_arr = arr[2:3]     # 切片返回视图（view），共享内存
print(item_lst)   # 9
print(part_lst)   # [9]
print(item_arr)   # 9
print(part_arr)   # [9]
## 动态性：修改原对象
lst[2] = 99
arr[2] = 99
print(item_lst)   # 9      ← 列表的 item_lst 是独立整数，不受影响
print(part_lst)   # [9]    ← 列表切片是副本，不受影响
print(item_arr)   # 9      ← 数组的 item_arr 是独立整数，不受影响
print(part_arr)   # [99]   ← 数组切片是视图，随原数组改变而更新！
```

#### 2. 数组 (Array)针对各个轴 (Axis)的索引 (Index)和切片 (Slicing)

```Python
import numpy as np
lst = [[[6, 7, 5, 1], [2, 9, 8, 0], [3, 4, 2, 8]],
       [[4, 5, 2, 3], [2, 9, 7, 1], [9, 5, 6, 7]]]
arr = np.array(lst)  # shape: (2, 3, 4)
## 单元素访问：三种方式等价
print(lst[1][0][2])        # 2
print(arr[1][0][2])        # 2
print(arr[1, 0, 2])        # 2
## 多级切片对比
print(lst[1:2][:1])        # [[[4, 5, 2, 3], [2, 9, 7, 1], [9, 5, 6, 7]]]
print(arr[1:2][:1])        # [[[4 5 2 3]
                           #   [2 9 7 1]
                           #   [9 5 6 7]]]
print(arr[1:2, :1])        # [[[4 5 2 3]]]
## 混合切片 + 索引
print(lst[1][::2][0])      # [4, 5, 2, 3]
print(arr[1][::2][0])      # [4 5 2 3]
print(arr[1, ::2, 0])      # [4 9]
```

#### 3. 数组 (Array)的高阶索引 (Advanced Indexing)

##### 结构化补充（Structured Supplement）：高级索引 (Advanced Indexing)

###### 整数 (Integer)数组 (Array)索引 (Integer Array Indexing)

```python
import numpy as np

matrix = np.arange(12).reshape(3, 4)
rows = np.array([2, 0, 2])

selected_rows = matrix[rows]
selected_values = matrix[[0, 1, 2], [1, 2, 3]]
```

多个整数 (Integer)索引 (Index)数组 (Array)会先广播 (Broadcasting)，再逐位置组合 (Composition)坐标；它们不是自动形成笛卡尔积 (Cartesian Product)。需要行列网格时使用 `np.ix_()`：

```python
row_indices = [0, 2]
column_indices = [1, 3]
submatrix = matrix[np.ix_(row_indices, column_indices)]
```

###### 条件选择 (Conditional Selection)

```python
values = np.array([-2, -1, 0, 1, 2])

positive = values[values > 0]
labels = np.where(values >= 0, "non-negative", "negative")
bounded = np.clip(values, -1, 1)
```

把整数 (Integer)列表 (List)或者 bool 数组 (Array)作为索引 (Index)。

```Python
import numpy as np
x = np.arange(24).reshape((3, 2, 4))
print(x)  # [[[ 0  1  2  3]
          #   [ 4  5  6  7]]
          #
          #  [[ 8  9 10 11]
          #   [12 13 14 15]]
          #
          #  [[16 17 18 19]
          #   [20 21 22 23]]]
## 可以理解为x[2], x[0], x[0]构成一个更高维度的数组
print(x[[2, 0, 0]])  # [[[16 17 18 19]
                     #   [20 21 22 23]]
                     #
                     #  [[ 0  1  2  3]
                     #   [ 4  5  6  7]]
                     #
                     #  [[ 0  1  2  3]
                     #   [ 4  5  6  7]]]
## 可以理解为x[2, 0], x[0, 0], x[1, 1]构成一个更高维度的数组
print(x[[2, 0, 1], [0, 0, 1]])  # [[16 17 18 19]
                                #  [ 0  1  2  3]
                                #  [12 13 14 15]]
## 可以理解为x[2, 0, 1], x[0, 0, 2], x[1, 1, 3]构成一个更高维度的数组
print(x[[2, 0, 1], [0, 0, 1], [1, 2, 3]])  # [17  2 15]
## 基本索引和高阶索引组合时, 会发生广播, 下面三个是等价的
print(x[0, [0, 0, 1], [1, 2, 3]])           # [1 2 7]
print(x[[0], [0, 0, 1], [1, 2, 3]])         # [1 2 7]
print(x[[0, 0, 0], [0, 0, 1], [1, 2, 3]])   # [1 2 7]
## 下面三个也是等价的
print(x[0, [0, 0, 1], 2])                   # [2 2 6]
print(x[[0], [0, 0, 1], [2]])               # [2 2 6]
print(x[[0, 0, 0], [0, 0, 1], [2, 2, 2]])   # [2 2 6]
## 切片在高阶索引一侧, 按照轴的顺序定shape即可
print(x[::2, [0, 0, 1], [3, 0, 2]])  # shape: (2, 3)
                                     # [[ 3  0  6]
                                     #  [19 16 22]]
print(x[[2, 0, 1], [1, 0, 1], ::2])  # shape: (3, 2)
                                     # [[20 22]
                                     #  [ 0  2]
                                     #  [12 14]]
## 切片两侧都有高阶索引时, 定shape时高阶索引在前, 切片在后
print(x[[2, 0, 1], 1:, [3, 0, 2]])   # shape: (3, 1)
                                     # [[23]
                                     #  [ 4]
                                     #  [14]]
""" 如果需要利用bool索引对标量进行操作, 也就是针对最后一个维度,
    只需要创建一个shape为(3, 2, 4)的bool索引即可 """
bool_list = [[[True, False, True, False], [False, True, False, True]],
             [[True, False, True, False], [False, True, False, True]],
             [[True, False, True, False], [False, True, False, True]]]
print(x[np.array(bool_list)])  # [ 0  2  5  7  8 10 13 15 16 18 21 23]
## x > 13 得到一个shape为(3, 2, 4)的bool数组
print(x[x > 13])               # [14 15 16 17 18 19 20 21 22 23]
""" 如果需要利用bool索引对1轴进行操作,
    只需要创建一个shape为(3, 2)的bool索引即可 """
bool_list = [[True, False], [False, True], [True, False]]
print(x[np.array(bool_list)])  # [[[ 0  1  2  3]
                               #   [12 13 14 15]
                               #   [16 17 18 19]]]
""" 如果需要利用bool索引对0轴进行操作,
    只需要创建一个shape为(3,)的bool索引即可 """
bool_list = [True, False, True]
print(x[np.array(bool_list)])  # [[[ 0  1  2  3]
                               #   [ 4  5  6  7]]
                               #
                               #  [[16 17 18 19]
                               #   [20 21 22 23]]]
```

---
### 六、 常用操作 (Common Operations)

#### 结构化补充（Structured Supplement）：形状变换与拼接 (Concatenation)

```python
import numpy as np

array = np.arange(24)
batch = array.reshape(2, 3, 4)
flat = batch.reshape(-1)

transposed = batch.transpose(0, 2, 1)
swapped = batch.swapaxes(1, 2)
```

```python
left = np.ones((2, 3))
right = np.zeros((2, 3))

concatenated = np.concatenate([left, right], axis=0)  # 连接已有轴，shape=(4, 3)。
stacked = np.stack([left, right], axis=0)              # 新增一个轴，shape=(2, 2, 3)。
```

#### 结构化补充（Structured Supplement）：保存与加载

```python
import numpy as np

array = np.arange(6).reshape(2, 3)
np.save("array.npy", array)
loaded = np.load("array.npy")

np.savez("arrays.npz", features=array, labels=np.array([0, 1]))
archive = np.load("arrays.npz")
```

`.npy/.npz` 能保留形状和 `dtype`；与其他工具交换表格数据时再考虑 CSV。

#### 1. 数组形状 (Array Shape)改变
- `np.reshape(arr_like, newshape)`
    保证 `size` 不变，在不更改数据的情况下为数组 (Array)赋予新的形状。`newshape` 如果是整数 (Integer)，则结果将是该长度的 1-D 数组 (1-D Array)。`newshape` 的一个形状维度 (Dimension)可以是 `1`，值将自行推断。
- `ndarray.flatten()`
    返回扁平化到一维的数组 (Array)。

```Python
import numpy as np
## reshape
arr1 = np.arange(6).reshape((2, 1, 3))   # shape: (2, 1, 3)
arr2 = np.reshape(arr1, 6)               # 展平为 1D，长度 6
arr3 = np.reshape(arr1, -1)              # -1 表示自动推断该维度大小
arr4 = np.reshape(arr1, (-1,))           # 等价于上面，显式写成元组
print(arr2)  # [0 1 2 3 4 5]
print(arr3)  # [0 1 2 3 4 5]
print(arr4)  # [0 1 2 3 4 5]
## 多维 reshape 中使用 -1（只能有一个 -1）
arr1 = np.arange(24)                     # shape: (24,)
arr2 = np.reshape(arr1, (2, 2, -1, 2))   # 总元素 24，已知 2×2×?×2 = 24 → ? = 3
print(arr2.shape)  # (2, 2, 3, 2)
## flatten
a = np.array([[1,2], [3,4]])
print(a.flatten())  # [1 2 3 4]
```

#### 2. 轴 (Axis)与转置 (Axes and Transposition)
- `ndarray.T`: 转置 (Transpose)数组 (Transpose)
- `np.swapaxes(arr_like, axis1, axis2)`: 交换数组 (Array)的两个轴 (Axis)
- `np.transpose(arr_like, axes=None)`: 通过 `axes` 参数 (Parameter)排列数组 (Array)的 `shape`，`axes` 没有指定，默认为转置 (Transpose)。

```Python
import numpy as np
## swapaxes
a = np.array([[1, 2, 3], [4, 5, 6]])
print(a)                              # [[1 2 3]
                                      #  [4 5 6]]
print(np.swapaxes(a, 0, 1))           # [[1 4]
                                      #  [2 5]
                                      #  [3 6]]
a = np.arange(24).reshape((2, 3, 4))
print(np.swapaxes(a, 0, 2).shape)     # (4, 3, 2)
## T and transpose
a = np.array([[1, 2, 3], [4, 5, 6]])
print(a)                              # [[1 2 3]
                                      #  [4 5 6]]
print(a.T)                            # [[1 4]
                                      #  [2 5]
                                      #  [3 6]]
print(np.transpose(a))                # [[1 4]
                                      #  [2 5]
                                      #  [3 6]]
a = np.arange(24).reshape((2, 3, 4))
print(a.T.shape)                      # (4, 3, 2)
print(np.transpose(a, (1, 0, 2)).shape)  # (3, 2, 4)
```

#### 3. 数组 (Array)连接 (Array Concatenation)
- `np.concatenate(arrays, axis=0)arrays`: `Sequence[ArrayLike]`。沿现有轴 (Axis)连接一系列数组 (Array)，如果 `axis` 为 `None`，则数组 (Array)在使用前会被扁平化。
- `np.stack(arrays, axis=0)arrays`: `Sequence[ArrayLike]`。沿新轴 (Axis)连接一系列数组 (Array)。

```Python
import numpy as np
## concatenate
a = np.array([[1, 2], [3, 4]])   # shape: (2, 2)
b = np.array([[5, 6]])           # shape: (1, 2)
## 沿 axis=0 拼接（垂直方向）：行数相加，列数必须相同
print(np.concatenate((a, b), axis=0))    # [[1 2]
                                         #  [3 4]
                                         #  [5 6]]
## 沿 axis=1 拼接（水平方向）：需 b.T 变为 (2,1)，使行数匹配 a 的 2 行
print(np.concatenate((a, b.T), axis=1))  # [[1 2 5]
                                         #  [3 4 6]]
## axis=None：先展平所有数组，再拼成一维
print(np.concatenate((a, b), axis=None)) # [1 2 3 4 5 6]
## stack
a1 = np.arange(6).reshape((2, 3))      # shape: (2, 3)
a2 = np.arange(10, 16).reshape((2, 3))
a3 = np.arange(20, 26).reshape((2, 3))
a4 = np.arange(30, 36).reshape((2, 3))
## 默认 axis=0：在新维度（最前）堆叠 → (4, 2, 3)
print(np.stack((a1, a2, a3, a4)).shape)        # (4, 2, 3)
## axis=1：在第1维插入新轴 → (2, 4, 3)
print(np.stack((a1, a2, a3, a4), axis=1).shape)  # (2, 4, 3)
## axis=2：在最后一维插入新轴 → (2, 3, 4)
print(np.stack((a1, a2, a3, a4), axis=2).shape)  # (2, 3, 4)
```

#### 4. 矩阵乘法 (Matrix Multiplication)

##### 结构化补充（Structured Supplement）：矩阵乘法 (Matrix Multiplication)

```python
import numpy as np

features = np.array([[1.0, 2.0], [3.0, 4.0]])
weights = np.array([[0.5], [1.5]])

predictions = features @ weights
```

- `*` 是逐元素乘法。
- `@` / `np.matmul()` 是矩阵乘法 (Matrix Multiplication)。
- 高维批量矩阵乘法 (Matrix Multiplication)时，`matmul` 会把最后两个轴 (Axis)当作矩阵轴 (Axis)，并广播 (Broadcasting)前面的批次轴 (Axis)。

##### 结构化补充（Structured Supplement）：线性代数 (Linear Algebra)

```python
import numpy as np

matrix = np.array([[3.0, 1.0], [1.0, 2.0]])
target = np.array([9.0, 8.0])

# 解 Ax=b 时使用 solve，比显式计算 inv(A) @ b 更稳定也更高效。
solution = np.linalg.solve(matrix, target)

norm = np.linalg.norm(target)
eigenvalues, eigenvectors = np.linalg.eig(matrix)
u, singular_values, vt = np.linalg.svd(matrix)
```

常用接口 (Interfaces)：

- `np.linalg.solve()`：求解方程组 (Linear System)。
- `np.linalg.lstsq()`：最小二乘解 (Least-squares Solution)。
- `np.linalg.norm()`：向量或矩阵范数 (Norm)。
- `np.linalg.eig()`：特征值分解 (Eigendecomposition)。
- `np.linalg.svd()`：奇异值分解 (Singular Value Decomposition, SVD)。

- `np.dot(a, b)`: 两个数组 (Array)的点积 (Dot Product)
- `np.matmul(x1, x2)`: 两个数组 (Array)的矩阵乘积 (Matrix Product)，也可使用 `@` 操作符表示。

```Python
import numpy as np
## dot
a = [1, 2, 3]
b = [1, 0, 2]
print(np.dot(a, b))        # 7   ← 1*1 + 2*0 + 3*2 = 1 + 0 + 6 = 7
a = [[1, 0], [0, 1]]       # 2x2 单位矩阵
b = [[4, 1], [2, 2]]
print(np.dot(a, b))        # [[4 1]
                           #  [2 2]]   ← 单位矩阵乘任何矩阵等于其本身
## matmul / @
a = np.array([[1, 0], [0, 1]])
b = np.array([[4, 1], [2, 2]])
print(np.matmul(a, b))     # [[4 1]
                           #  [2 2]]
print(a @ b)               # [[4 1]
                           #  [2 2]]
```

---
### 七、 比较运算 (Comparison Operations)
运算时 `x1`, `x2` 的形状必须相同，或者可以广播 (Broadcasting)。
- `np.greater(x1, x2)`: 按元素判断 `x1 > x2`
- `np.greater_equal(x1, x2)`: 按元素判断 `x1 >= x2`
- `np.less(x1, x2)`: 按元素判断 `x1 < x2`
- `np.less_equal(x1, x2)`: 按元素判断 `x1 <= x2`
- `np.equal(x1, x2)`: 按元素判断 `x1 == x2`
- `np.not_equal(x1, x2)`: 按元素判断 `x1 != x2`

```Python
import numpy as np
## greater
print(np.greater([4, 2], [2, 2]))        # [ True False]
a = np.array([[4, 2], [3, 1]])           # shape: (2, 2)
b = np.array([[2, 2]])                   # shape: (1, 2) → 可广播到 (2, 2)
print(np.greater(a, b))                  # [[ True False]
                                         #  [ True False]]
print(a > b)                             # [[ True False]
                                         #  [ True False]]
## greater_equal
print(np.greater_equal([4, 2], [2, 2]))  # [ True  True]
print(np.greater_equal(a, b))            # [[ True  True]
                                         #  [ True False]]
print(a >= b)                            # [[ True  True]
                                         #  [ True False]]
## less
print(np.less([4, 2], [2, 2]))           # [False False]
print(np.less(a, b))                     # [[False False]
                                         #  [False  True]]
print(a < b)                             # [[False False]
                                         #  [False  True]]
## less_equal
print(np.less_equal([4, 2], [2, 2]))     # [False  True]
print(np.less_equal(a, b))               # [[False  True]
                                         #  [False  True]]
print(a <= b)                            # [[False  True]
                                         #  [False  True]]
## equal
print(np.equal([4, 2], [2, 2]))          # [False  True]
print(np.equal(a, b))                    # [[False  True]
                                         #  [False False]]
print(a == b)                            # [[False  True]
                                         #  [False False]]
## not_equal
print(np.not_equal([4, 2], [2, 2]))      # [ True False]
print(np.not_equal(a, b))                # [[ True False]
                                         #  [ True  True]]
print(a != b)                            # [[ True False]
                                         #  [ True  True]]
```

---
### 八、 数学函数 (Mathematical Functions)

#### 结构化补充（Structured Supplement）：缺失值 (Missing Value)、无穷值 (Infinite Value)与数值稳定性 (Numerical Stability)

```python
import numpy as np

values = np.array([1.0, np.nan, np.inf])

print(np.isnan(values))
print(np.isfinite(values))
print(np.nanmean(values))

# 期望输出:
# [False  True False]
# [ True False False]
# inf
```

整数 (Integer)数组 (Array)不能直接存储 `NaN`；加入 `NaN` 通常会转换为浮点类型。

```python
probabilities = np.array([1e-12, 0.5, 1.0])
safe_probabilities = np.clip(probabilities, 1e-7, 1 - 1e-7)
log_values = np.log(safe_probabilities)
```

#### 结构化补充（Structured Supplement）：通用函数 (Universal Functions, Ufuncs)

通用函数 (Universal Functions, Ufuncs) 对数组 (Array)逐元素运算 (Element-wise Operation)，并支持广播 (Broadcasting)、输出数组 (Array)和条件掩码。

```python
import numpy as np

values = np.array([-1.0, 0.0, 1.0])

print(np.abs(values))
print(np.exp(values))
print(np.log1p(values[1:]))  # log(1 + x)，小 x 时比直接计算更稳定。
print(np.sqrt(np.clip(values, 0, None)))

# 期望输出:
# [1. 0. 1.]
# [0.36787944 1.         2.71828183]
# [0.         0.69314718]
# [0. 0. 1.]
```

使用 `where` 避免对无效位置计算：

```python
numerator = np.array([1.0, 2.0, 3.0])
denominator = np.array([1.0, 0.0, 2.0])
result = np.full_like(numerator, np.nan)

np.divide(
    numerator,
    denominator,
    out=result,
    where=denominator != 0,
)
```

#### 1. 三角函数 (Trigonometric Functions)
- `np.sin(x)`: 正弦函数 (Sine)
- `np.cos(x)`: 余弦函数 (Cosine)
- `np.tan(x)`: 正切函数 (Tangent)
- `np.arcsin(x)`: 反正弦函数 (Arcsine)
- `np.arccos(x)`: 反余弦函数 (Arccosine)
- `np.arctan(x)`: 反正切函数 (Arctangent)
    （参数 (Parameter) `x` 对于三角函数 (Function)为角度的弧度值）

```Python
import numpy as np
## 正弦函数 sin(x)：x 为弧度
print(np.sin(np.pi/2))                              # 1.0
print(np.sin(np.array((0, 30, 90)) * np.pi / 180))  # [0.  0.5 1. ]
## 余弦函数 cos(x)
print(np.cos(np.pi/2))                              # 6.123233995736766e-17 ≈ 0（浮点误差）
print(np.cos(np.array((0, 60, 90)) * np.pi / 180))  # [1.000000e+00 5.000000e-01 6.123234e-17]
## 正切函数 tan(x)
print(np.tan(-np.pi))                               # 1.2246467991473532e-16 ≈ 0
print(np.tan(np.array((0, 180)) * np.pi / 180))     # [ 0.0000000e+00 -1.2246468e-16]
## 反正弦 arcsin(x)：返回值范围 [-π/2, π/2]
print(np.arcsin(1))                                 # 1.5707963267948966 (= π/2)
print(np.arcsin(np.array([0.5, -0.5])))             # [ 0.52359878 -0.52359878] ≈ [π/6, -π/6]
## 反余弦 arccos(x)：返回值范围 [0, π]
print(np.arccos(-1))                                # 3.141592653589793 (= π)
print(np.arccos(np.array([0.5, 1])))                # [1.04719755 0.        ] ≈ [π/3, 0]
## 反正切 arctan(x)：返回值范围 [-π/2, π/2]
print(np.arctan(1))                                 # 0.7853981633974483 (= π/4)
print(np.arctan(np.array([0, -1])))                 # [ 0.         -0.78539816]
```

#### 2. 其他数学函数 (Function)
- `np.floor(x)`: 返回 `x` 的底限 (向下取整)
- `np.ceil(x)`: 返回 `x` 的上限 (向上取整)
- `np.exp(x)`: 计算 $e$ 的 `x` 幂次方
- `np.log(x)`: 计算 `x` 的自然对数
- `np.log2(x)`: 计算 `x` 的以 2 为底的对数
- `np.log10(x)`: 计算 `x` 的以 10 为底的对数

```Python
import numpy as np
a = np.array([-1.7, -1.5, -0.2, 0.2, 1.5, 1.7, 2.0])
print(np.floor(a))        # [-2. -2. -1.  0.  1.  1.  2.]
print(np.ceil(a))         # [-1. -1. -0.  1.  2.  2.  2.]
## e的0次方、e的1次方、e的2次方
print(np.exp([0, 1, 2]))  # [1.         2.71828183 7.3890561 ]
print(np.log([1, np.e, np.e**2]))  # [0. 1. 2.]
x = np.array([1, 2, 2**4])
print(np.log2(x))         # [0. 1. 4.]
print(np.log10([1e-15, 1000]))  # [-15.   3.]
```

---
### 九、 统计与聚合函数 (Statistics and Aggregation)

#### 结构化补充（Structured Supplement）：`axis` 与聚合 (Aggregation)

```python
import numpy as np

matrix = np.array([[1, 2, 3], [4, 5, 6]])

matrix.sum()          # 所有元素。
matrix.sum(axis=0)    # 压缩行轴，得到每一列的和，shape=(3,)。
matrix.sum(axis=1)    # 压缩列轴，得到每一行的和，shape=(2,)。
matrix.mean(axis=1, keepdims=True)  # shape=(2, 1)，便于继续广播。
```

理解 `axis` 的可靠方法是：指定哪个轴 (Axis)，哪个轴 (Axis)就在聚合 (Aggregation)结果中被压缩。

#### 结构化补充（Structured Supplement）：统计与分位数 (Quantiles)

```python
import numpy as np

values = np.array([1.0, 2.0, 3.0, 100.0])

print(values.mean())
print(np.median(values))
print(values.var(ddof=0))  # 总体方差 (Population Variance)。
print(values.var(ddof=1))  # 样本方差 (Sample Variance)。
print(np.quantile(values, [0.25, 0.5, 0.75]))

# 期望输出:
# 26.5
# 2.5
# 1801.25
# 2401.6666666666665
# [ 1.75  2.5  27.25]
```

`ddof` 表示自由度修正 (Delta Degrees of Freedom)。统计定义不同会产生不同结果，不能只记 API 而忽略问题语义。

- `np.max(arr_like, axis=None, keepdims=False)`: 返回最大值
- `np.min(arr_like, axis=None, keepdims=False)`: 返回最小值
- `np.mean(arr_like, axis=None, keepdims=False)`: 返回平均值
- `np.var(arr_like, axis=None, keepdims=False)`: 返回方差 (Variance)
- `np.std(arr_like, axis=None, keepdims=False)`: 返回标准差
(对于以上函数 (Function)，`axis` 没有指定时，默认为 `None`，表示返回所有元素的聚合 (Aggregation)结果。)

```Python
import numpy as np
lis = [[0, 1, 7, 3], [4, 9, 6, 2], [8, 5, 11, 10]]
arr1 = np.array(lis)
print(arr1)                     # [[ 0  1  7  3]
                                #  [ 4  9  6  2]
                                #  [ 8  5 11 10]]
print(np.max(arr1))             # 11
print(np.max(arr1, axis=0))     # [ 8  9 11 10]
print(np.max(arr1, axis=1))     # [ 7  9 11]
print(np.min(arr1))             # 0
print(np.min(arr1, axis=0))     # [0 1 6 2]
print(np.min(arr1, axis=1))     # [0 2 5]
print(np.mean(arr1))            # 5.5
print(np.mean(arr1, axis=0))    # [4. 5. 8. 5.]
print(np.mean(arr1, axis=1))    # [2.75 5.25 8.5 ]
print(np.var(arr1))             # 11.916666666666666
print(np.var(arr1, axis=0))     # [10.66666667 10.66666667  4.66666667 12.66666667]
print(np.var(arr1, axis=1))     # [7.1875 6.6875 5.25  ]
print(np.std(arr1))             # 3.452052529534663
print(np.std(arr1, axis=0))     # [3.26598632 3.26598632 2.1602469  3.55902608]
print(np.std(arr1, axis=1))     # [2.68095132 2.58602011 2.29128785]
```

- `np.prod(arr_like, axis=None, keepdims=np._NoValue, initial=np._NoValue)`: 返回给定轴 (Axis)上数组 (Array)元素的乘积
- `np.sum(arr_like, axis=None, keepdims=np._NoValue, initial=np._NoValue)`: 返回给定轴 (Axis)上数组 (Array)元素的和

```Python
import numpy as np
## 默认的 axis=None 将计算输入数组中所有元素的乘积/和
print(np.prod([1, 2, 3, 4]))                          # 24        → 1×2×3×4
print(np.prod([[1, 2], [3, 4]]))                      # 24        → 所有元素相乘
print(np.prod([1, 2, 3, 4], initial=5))               # 120       → 5×1×2×3×4
print(np.prod([[1, 2], [3, 4]], axis=1))              # [ 2 12]   → 每行相乘: [1×2, 3×4]
print(np.prod([[1, 2], [3, 4]], axis=0))              # [3 8]     → 每列相乘: [1×3, 2×4]
print(np.prod([[1, 2], [3, 4]], axis=1, keepdims=True))  # [[ 2]    → 保持维度 (2,1)
                                                          #  [12]]
print(np.prod([[1, 2], [3, 4]], axis=0, keepdims=True))  # [[3 8]]  → 保持维度 (1,2)
print(np.sum([1, 2, 3, 4]))                           # 10        → 1+2+3+4
print(np.sum([[1, 2], [3, 4]]))                       # 10        → 所有元素求和
print(np.sum([1, 2, 3, 4], initial=5))                # 15        → 5+1+2+3+4
print(np.sum([[1, 2], [3, 4]], axis=1))               # [3 7]     → 每行求和: [1+2, 3+4]
print(np.sum([[1, 2], [3, 4]], axis=0))               # [4 6]     → 每列求和: [1+3, 2+4]
print(np.sum([[1, 2], [3, 4]], axis=1, keepdims=True))   # [[3]     → 保持维度 (2,1)
                                                           #  [7]]
print(np.sum([[1, 2], [3, 4]], axis=0, keepdims=True))   # [[4 6]]  → 保持维度 (1,2)
```

---
### 十、 查找与极值 (Searching and Extremes)

#### 结构化补充（Structured Supplement）：排序 (Sorting)、查找与集合 (Set)操作

```python
import numpy as np

values = np.array([3, 1, 3, 2])

print(np.sort(values))
print(np.argsort(values))       # 返回排序后元素对应的原索引。
print(np.unique(values))
print(np.unique(values, return_counts=True))
print(np.where(values == 3)[0])

# 期望输出:
# [1 2 3 3]
# [1 3 0 2]
# [1 2 3]
# (array([1, 2, 3]), array([1, 1, 2]))
# [0 2]
```

```python
left = np.array([1, 2, 3])
right = np.array([3, 4])

np.intersect1d(left, right)
np.union1d(left, right)
np.setdiff1d(left, right)
np.isin(left, right)
```

- `np.nonzero(arr_like)`: 返回非零元素的索引 (Index)
- `np.argwhere(arr_like)`: 找出数组 (Array)中按元素分组的非零元素的索引 (Index)
- `np.where(condition, x=None, y=None)`
    - `condition`: `array_like`, bool
    - `x`, `y`: `array_like`，要么都传参，要么都不传。
    - 如果传三个参数 (Parameter)，条件成立返回 `x`，不成立时返回 `y`。如果只传第一个参数 (Parameter)，返回符合条件的元素的索引 (Index)。

```Python
import numpy as np
## nonzero
x = np.array([[3, 0, 0], [0, 4, 0], [5, 6, 0]])
print(x)                          # [[3 0 0]
                                  #  [0 4 0]
                                  #  [5 6 0]]
print(np.nonzero(x))              # (array([0, 1, 2, 2]), array([0, 1, 0, 1]))
print(x[np.nonzero(x)])           # [3 4 5 6]
a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(a > 3)                      # [[False False False]
                                  #  [ True  True  True]
                                  #  [ True  True  True]]
print(np.nonzero(a > 3))          # (array([1, 1, 1, 2, 2, 2]), array([0, 1, 2, 0, 1, 2]))
print(a[np.nonzero(a > 3)])       # [4 5 6 7 8 9]
## argwhere
x = np.arange(6).reshape(2, 3)
print(x)                          # [[0 1 2]
                                  #  [3 4 5]]
print(x > 1)                      # [[False False  True]
                                  #  [ True  True  True]]
print(np.argwhere(x > 1))         # [[0 2]
                                  #  [1 0]
                                  #  [1 1]
                                  #  [1 2]]
## where
a = np.arange(10)
print(np.where(a < 5, a, 10*a))   # [ 0  1  2  3  4 50 60 70 80 90]
## 当where内有三个参数时，当condition成立时返回x，当condition不成立时返回y
print(np.where([[True, False], [True, True]], [[1, 2], [3, 4]], [[9, 8], [7, 6]]))
## [[1 8]
##  [3 4]]
## 如果只传第一个参数，返回符合条件的元素的索引
a = np.array([2, 4, 6, 8, 10])
print(np.where(a > 5))            # (array([2, 3, 4]),)
```

- `np.maximum(x1, x2)`: 返回 `x1` 和 `x2` 逐个元素比较中的最大值
- `np.minimum(x1, x2)`: 返回 `x1` 和 `x2` 逐个元素比较中的最小值
- `np.argmax(arr_like, axis=None)`: 返回沿轴 (Axis)的最大值的索引 (Index)
- `np.argmin(arr_like, axis=None)`: 返回沿轴 (Axis)的最小值的索引 (Index)

```Python
import numpy as np
## maximum & minimum
print(np.maximum([2, 3, 4], [1, 5, 2]))          # [2 5 4]
print(np.maximum([[2, 3], [4, 5]], [[1, 5], [2, 6]]))  # [[2 5]
                                                       #  [4 6]]
print(np.minimum([2, 3, 4], [1, 5, 2]))          # [1 3 2]
print(np.minimum([[2, 3], [4, 5]], [[1, 5], [2, 6]]))  # [[1 3]
                                                       #  [2 5]]
## argmax & argmin
a = np.arange(6).reshape(2, 3) + 10
print(a)                                         # [[10 11 12]
                                                 #  [13 14 15]]
## 没有指定轴，则数组扁平化处理
print(np.argmax(a))                              # 5
print(np.argmax(a, axis=0))                      # [1 1 1]
print(np.argmax(a, axis=1))                      # [2 2]
print(np.argmin(a))                              # 0
print(np.argmin(a, axis=0))                      # [0 0 0]
print(np.argmin(a, axis=1))                      # [0 0]
```

---
### 十一、 随机模块 (Random Module)

#### 结构化补充（Structured Supplement）：随机数 (Random Number)与可复现性 (Reproducibility)

```python
import numpy as np

# 新代码优先使用 Generator，避免依赖全局随机状态。
rng = np.random.default_rng(seed=42)

samples = rng.normal(loc=0.0, scale=1.0, size=(100, 3))
indices = rng.choice(len(samples), size=10, replace=False)
rng.shuffle(samples)
```

固定种子能复现实验中的随机序列 (Sequence)，但不保证跨所有库、硬件和版本 (Version)得到完全相同结果。

- `np.random.normal(loc=0.0, scale=1.0, size=None)`:
    - `loc`: 均值 (中心)
    - `scale`: 标准差 (Standard Deviation)
    - `size`: 输出的形状
    - 返回从正态分布 (Normal Distribution) 中抽取的随机样本。
- `np.random.randint(low=None, high, size=None)`: 返回从 `[low, high)` 离散均匀分布 (Discrete Uniform Distribution) 中抽取的随机整数 (Integer)。
- `np.random.uniform(low=0.0, high=1.0, size=None)`: 返回从 `[low, high)` 均匀分布 (Uniform Distribution) 中抽取的随机样本。
- `np.random.permutation(x)`:
    - `x`: `int` or `array_like`
    - 如果 `x` 是整数 (Integer)，返回随机排列的 `np.arange(x)`
    - 如果 `x` 是数组 (Array)，只对数组 (Array)的第一个维度 (Dimension)随机排列，返回新的数组 (Array)。
- `np.random.seed([x])`: 随机数 (Random Number)种子 (Random Seed)。

```Python
import numpy as np
## normal
print(np.random.normal(3, 2.5, size=(2, 4)))
## [[2.77374601 6.39194169 3.50478002 0.32307184]
##  [1.79486353 3.11604183 3.17622272 3.59193008]]
## randint
print(np.random.randint(2, size=10))             # [0 1 0 1 0 0 0 0 0 1]
print(np.random.randint(0, 2, size=10))          # [1 1 1 0 0 1 1 1 1 0]
print(np.random.randint(1, 4, size=(2, 3)))      # [[2 2 3]
                                                 #  [3 1 2]]
## uniform
print(np.random.uniform(2, size=10))
## [1.36872781 1.05440904 1.92293582 1.79682649 1.92452747 1.01096166
##  1.0021525  1.9405499  1.09845962 1.07890714]
print(np.random.uniform(0, 2, size=10))
## [1.2311377  1.60301242 0.77386548 0.74841594 1.64789569 0.00279324
##  1.06320328 0.77354091 1.29033211 0.10265232]
print(np.random.uniform(1, 4, size=(2, 3)))
## [[3.14995471 1.52158372 1.92005825]
##  [1.42513662 2.64660308 3.92028231]]
## permutation
print(np.random.permutation(6))                  # [1 0 3 4 5 2]
arr1 = np.array([0, 1, 2, 3, 4, 5])
print(np.random.permutation(arr1))               # [1 0 2 3 4 5]
arr2 = np.arange(10).reshape(5, 2)
print(np.random.permutation(arr2))               # [[2 3]
                                                 #  [4 5]
                                                 #  [0 1]
                                                 #  [8 9]
                                                 #  [6 7]]
## seed
np.random.seed(3)
print(np.random.uniform(1, 2, size=4))
## [1.5507979  1.70814782 1.29090474 1.51082761]
np.random.seed(5)
print(np.random.uniform(1, 2, size=4))
## [1.22199317 1.87073231 1.20671916 1.91861091]
np.random.seed(3)
print(np.random.uniform(1, 2, size=4))
## [1.5507979  1.70814782 1.29090474 1.51082761]
np.random.seed()
print(np.random.uniform(1, 2, size=4))
## [1.98011499 1.41251095 1.37907745 1.89147863]
```

## 进阶补充与核对（Advanced Supplements and Verification）

### 结构化补充（Structured Supplement）：完成检查

- [ ] 能根据 `shape` 判断每个轴 (Axis)的含义。
- [ ] 能解释广播 (Broadcasting)规则和 `axis` 聚合 (Aggregation)。
- [ ] 能区分视图 (View)与副本 (Copy)、`concatenate` 与 `stack`、`*` 与 `@`。
- [ ] 能使用布尔索引 (Boolean Indexing)和向量化 (Vectorization)完成数据筛选与变换。
- [ ] 能使用 `default_rng()` 生成可复现随机数 (Random Number)据。

### 结构化补充（Structured Supplement）：参考资料

- [NumPy User Guide](https://numpy.org/doc/stable/user/)
- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
