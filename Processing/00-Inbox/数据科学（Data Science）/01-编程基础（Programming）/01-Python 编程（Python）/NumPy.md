## 一、 NumPy 简介 (Introduction)
NumPy (Numerical Python) 是 Python 进行科学计算 (Scientific Computing) 的一个扩展库，提供了大量的函数和操作，主要用于对多维数组执行计算，它比 Python 自身的嵌套列表结构要高效得多。
**NumPy 数组 (Array) 和 Python 列表 (List) 的主要区别:**
- 数组会对元素的数据类型做统一，而列表不会。
- 数组创建后具有固定大小，而列表由于内存自动管理，可动态调整。
---
## 二、 创建数组与属性 (Creating Arrays and Attributes)
### 1. 创建数组
`np.array(object, dtype=None)`
- `object`: `array_like`，类似于数组的对象。如果 `object` 是标量 (Scalar)，则返回包含 `object` 的 0 维数组。
- `dtype`: `data-type`，数据类型。如果没有给出，会从输入数据推断数据类型。
- **作用**: 创建一个数组对象并返回 (`ndarray` 实例对象)。

```Python
import numpy as np
num = 789
arr = np.array(num)
print(num)
print(arr)
print(type(num))
print(type(arr))
# 789
# 789
# <class 'int'>
# <class 'numpy.ndarray'>
lst = [6, 7, 1, 0, 9, 8]
arr = np.array(lst)
print(lst)
print(arr)
lst = [[6, 7, 1], [0, 9, 8]]
arr = np.array(lst)
print(lst)
print(arr)
# [6, 7, 1, 0, 9, 8]
# [6 7 1 0 9 8]
lst = [[[6, 7], [1, 0], [9, 8]]]
arr = np.array(lst)
print(lst)
print(arr)
# [[6, 7, 1], [0, 9, 8]]
# [[6 7 1]
#  [0 9 8]]
# [[[6, 7], [1, 0], [9, 8]]]
# [[[6 7]
#   [1 0]
#   [9 8]]]
```

### 2. DTYPE 常用值 (Common Data Types)
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
### 3. NDARRAY 常用属性 (NDARRAY Attributes)
|属性名|描述 (Description)|
|---|---|
|`ndarray.ndim`|秩 (Rank)，即轴的数量或维度的数量|
|`ndarray.shape`|数组的形状|
|`ndarray.size`|数组中数据的总个数|
|`ndarray.dtype`|数组中的数据类型|
|`ndarray.itemsize`|数组中的数据大小，以字节为单位|

```Python
import numpy as np
lst = [[6, 7, 1], [0, 9, 8]]
arr = np.array(lst)
print(arr.ndim)
print(arr.dtype)
print(arr.itemsize)
print(arr.shape)
print(arr.size)
# 2
# int64
# 8
# (2, 3)
# 6
```

---
## 三、 生成数组 (Generating Arrays)
### 1. `np.arange([start,] stop[, step])`
返回给定区间内的均匀间隔值构成的数组。

```Python
import numpy as np
print(np.arange(3))
print(np.arange(3.0))
print(np.arange(3, 7))
print(np.arange(3, 7, 2))
print(np.arange(7, 3, -2))
print(np.arange(3, 7, 0.5))
# [0 1 2]
# [0. 1. 2.]
# [3 4 5 6]
# [3 5]
# [7 5]
# [3.  3.5 4.  4.5 5.  5.5 6.  6.5]
```

### 2. `np.linspace(start, stop, num=50, dtype=None)`
把给定区间分成 `num` 个均匀间隔的样本，构成数组并返回。
- `num`: 生成的样本数量。
- `dtype`: 默认自动推断数据类型，推断出的 `dtype` 永远不会是整数；即使参数会产生一个整数数组，也会选择 `np.float64`。

```Python
import numpy as np
print(np.linspace(1, 50))
print(np.linspace(1, 10, num=10))
print(np.linspace(1, 10, num=10, dtype=np.int32))
# [ 1.  2.  3.  4.  5.  6.  7.  8.  9. 10. 11. 12. 13. 14. 15. 16. 17. 18.
#  19. 20. 21. 22. 23. 24. 25. 26. 27. 28. 29. 30. 31. 32. 33. 34. 35. 36.
#  37. 38. 39. 40. 41. 42. 43. 44. 45. 46. 47. 48. 49. 50.]
# [ 1.  2.  3.  4.  5.  6.  7.  8.  9. 10.]
# [ 1  2  3  4  5  6  7  8  9 10]
```

---
## 四、 基本运算与广播机制 (Basic Operations and Broadcasting)
基本运算：数组的算术运算和比较运算为逐元素操作 (Element-wise Operations)。
**广播机制 (Broadcasting):** 后缘维度相同或者不同的维度有1，可以广播。

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
# 广播机制示例
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
## 五、 索引和切片 (Indexing and Slicing)
数组除了支持 Python 序列的索引和切片操作以外，还可以针对各个轴进行索引和切片操作。
### 1. 序列索引和切片
返回视图 (View)，修改切片会影响原数组 (动态性)。

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
# 动态性：修改原对象
lst[2] = 99
arr[2] = 99
print(item_lst)   # 9      ← 列表的 item_lst 是独立整数，不受影响
print(part_lst)   # [9]    ← 列表切片是副本，不受影响
print(item_arr)   # 9      ← 数组的 item_arr 是独立整数，不受影响
print(part_arr)   # [99]   ← 数组切片是视图，随原数组改变而更新！
```

### 2. 数组针对各个轴的索引和切片

```Python
import numpy as np
lst = [[[6, 7, 5, 1], [2, 9, 8, 0], [3, 4, 2, 8]],
       [[4, 5, 2, 3], [2, 9, 7, 1], [9, 5, 6, 7]]]
arr = np.array(lst)  # shape: (2, 3, 4)
# 单元素访问：三种方式等价
print(lst[1][0][2])        # 2
print(arr[1][0][2])        # 2
print(arr[1, 0, 2])        # 2
# 多级切片对比
print(lst[1:2][:1])        # [[[4, 5, 2, 3], [2, 9, 7, 1], [9, 5, 6, 7]]]
print(arr[1:2][:1])        # [[[4 5 2 3]
                           #   [2 9 7 1]
                           #   [9 5 6 7]]]
print(arr[1:2, :1])        # [[[4 5 2 3]]]
# 混合切片 + 索引
print(lst[1][::2][0])      # [4, 5, 2, 3]
print(arr[1][::2][0])      # [4 5 2 3]
print(arr[1, ::2, 0])      # [4 9]
```

### 3. 数组的高阶索引 (Advanced Indexing)
把整数列表或者 bool 数组作为索引。

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
# 可以理解为x[2], x[0], x[0]构成一个更高维度的数组
print(x[[2, 0, 0]])  # [[[16 17 18 19]
                     #   [20 21 22 23]]
                     #
                     #  [[ 0  1  2  3]
                     #   [ 4  5  6  7]]
                     #
                     #  [[ 0  1  2  3]
                     #   [ 4  5  6  7]]]
# 可以理解为x[2, 0], x[0, 0], x[1, 1]构成一个更高维度的数组
print(x[[2, 0, 1], [0, 0, 1]])  # [[16 17 18 19]
                                #  [ 0  1  2  3]
                                #  [12 13 14 15]]
# 可以理解为x[2, 0, 1], x[0, 0, 2], x[1, 1, 3]构成一个更高维度的数组
print(x[[2, 0, 1], [0, 0, 1], [1, 2, 3]])  # [17  2 15]
# 基本索引和高阶索引组合时, 会发生广播, 下面三个是等价的
print(x[0, [0, 0, 1], [1, 2, 3]])           # [1 2 7]
print(x[[0], [0, 0, 1], [1, 2, 3]])         # [1 2 7]
print(x[[0, 0, 0], [0, 0, 1], [1, 2, 3]])   # [1 2 7]
# 下面三个也是等价的
print(x[0, [0, 0, 1], 2])                   # [2 2 6]
print(x[[0], [0, 0, 1], [2]])               # [2 2 6]
print(x[[0, 0, 0], [0, 0, 1], [2, 2, 2]])   # [2 2 6]
# 切片在高阶索引一侧, 按照轴的顺序定shape即可
print(x[::2, [0, 0, 1], [3, 0, 2]])  # shape: (2, 3)
                                     # [[ 3  0  6]
                                     #  [19 16 22]]
print(x[[2, 0, 1], [1, 0, 1], ::2])  # shape: (3, 2)
                                     # [[20 22]
                                     #  [ 0  2]
                                     #  [12 14]]
# 切片两侧都有高阶索引时, 定shape时高阶索引在前, 切片在后
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
# x > 13 得到一个shape为(3, 2, 4)的bool数组
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
## 六、 常用操作 (Common Operations)
### 1. 数组形状改变
- `np.reshape(arr_like, newshape)`  
    保证 `size` 不变，在不更改数据的情况下为数组赋予新的形状。`newshape` 如果是整数，则结果将是该长度的 1-D 数组 (1-D Array)。`newshape` 的一个形状维度可以是 `1`，值将自行推断。
- `ndarray.flatten()`  
    返回扁平化到一维的数组。

```Python
import numpy as np
# reshape
arr1 = np.arange(6).reshape((2, 1, 3))   # shape: (2, 1, 3)
arr2 = np.reshape(arr1, 6)               # 展平为 1D，长度 6
arr3 = np.reshape(arr1, -1)              # -1 表示自动推断该维度大小
arr4 = np.reshape(arr1, (-1,))           # 等价于上面，显式写成元组
print(arr2)  # [0 1 2 3 4 5]
print(arr3)  # [0 1 2 3 4 5]
print(arr4)  # [0 1 2 3 4 5]
# 多维 reshape 中使用 -1（只能有一个 -1）
arr1 = np.arange(24)                     # shape: (24,)
arr2 = np.reshape(arr1, (2, 2, -1, 2))   # 总元素 24，已知 2×2×?×2 = 24 → ? = 3
print(arr2.shape)  # (2, 2, 3, 2)
# flatten
a = np.array([[1,2], [3,4]])
print(a.flatten())  # [1 2 3 4]
```

### 2. 轴与转置 (Axes and Transposition)
- `ndarray.T`: 转置数组 (Transpose)
- `np.swapaxes(arr_like, axis1, axis2)`: 交换数组的两个轴
- `np.transpose(arr_like, axes=None)`: 通过 `axes` 参数排列数组的 `shape`，`axes` 没有指定，默认为转置。

```Python
import numpy as np
# swapaxes
a = np.array([[1, 2, 3], [4, 5, 6]])
print(a)                              # [[1 2 3]
                                      #  [4 5 6]]
print(np.swapaxes(a, 0, 1))           # [[1 4]
                                      #  [2 5]
                                      #  [3 6]]
a = np.arange(24).reshape((2, 3, 4))
print(np.swapaxes(a, 0, 2).shape)     # (4, 3, 2)
# T and transpose
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

### 3. 数组连接 (Array Concatenation)
- `np.concatenate(arrays, axis=0)arrays`: `Sequence[ArrayLike]`。沿现有轴连接一系列数组，如果 `axis` 为 `None`，则数组在使用前会被扁平化。
- `np.stack(arrays, axis=0)arrays`: `Sequence[ArrayLike]`。沿新轴连接一系列数组。

```Python
import numpy as np
# concatenate
a = np.array([[1, 2], [3, 4]])   # shape: (2, 2)
b = np.array([[5, 6]])           # shape: (1, 2)
# 沿 axis=0 拼接（垂直方向）：行数相加，列数必须相同
print(np.concatenate((a, b), axis=0))    # [[1 2]
                                         #  [3 4]
                                         #  [5 6]]
# 沿 axis=1 拼接（水平方向）：需 b.T 变为 (2,1)，使行数匹配 a 的 2 行
print(np.concatenate((a, b.T), axis=1))  # [[1 2 5]
                                         #  [3 4 6]]
# axis=None：先展平所有数组，再拼成一维
print(np.concatenate((a, b), axis=None)) # [1 2 3 4 5 6]
# stack
a1 = np.arange(6).reshape((2, 3))      # shape: (2, 3)
a2 = np.arange(10, 16).reshape((2, 3))
a3 = np.arange(20, 26).reshape((2, 3))
a4 = np.arange(30, 36).reshape((2, 3))
# 默认 axis=0：在新维度（最前）堆叠 → (4, 2, 3)
print(np.stack((a1, a2, a3, a4)).shape)        # (4, 2, 3)
# axis=1：在第1维插入新轴 → (2, 4, 3)
print(np.stack((a1, a2, a3, a4), axis=1).shape)  # (2, 4, 3)
# axis=2：在最后一维插入新轴 → (2, 3, 4)
print(np.stack((a1, a2, a3, a4), axis=2).shape)  # (2, 3, 4)
```

### 4. 矩阵乘法 (Matrix Multiplication)
- `np.dot(a, b)`: 两个数组的点积 (Dot Product)
- `np.matmul(x1, x2)`: 两个数组的矩阵乘积 (Matrix Product)，也可使用 `@` 操作符表示。

```Python
import numpy as np
# dot
a = [1, 2, 3]
b = [1, 0, 2]
print(np.dot(a, b))        # 7   ← 1*1 + 2*0 + 3*2 = 1 + 0 + 6 = 7
a = [[1, 0], [0, 1]]       # 2x2 单位矩阵
b = [[4, 1], [2, 2]]
print(np.dot(a, b))        # [[4 1]
                           #  [2 2]]   ← 单位矩阵乘任何矩阵等于其本身
# matmul / @
a = np.array([[1, 0], [0, 1]])
b = np.array([[4, 1], [2, 2]])
print(np.matmul(a, b))     # [[4 1]
                           #  [2 2]]
print(a @ b)               # [[4 1]
                           #  [2 2]]
```

---
## 七、 比较运算 (Comparison Operations)
运算时 `x1`, `x2` 的形状必须相同，或者可以广播。
- `np.greater(x1, x2)`: 按元素判断 `x1 > x2`
- `np.greater_equal(x1, x2)`: 按元素判断 `x1 >= x2`
- `np.less(x1, x2)`: 按元素判断 `x1 < x2`
- `np.less_equal(x1, x2)`: 按元素判断 `x1 <= x2`
- `np.equal(x1, x2)`: 按元素判断 `x1 == x2`
- `np.not_equal(x1, x2)`: 按元素判断 `x1 != x2`

```Python
import numpy as np
# greater
print(np.greater([4, 2], [2, 2]))        # [ True False]
a = np.array([[4, 2], [3, 1]])           # shape: (2, 2)
b = np.array([[2, 2]])                   # shape: (1, 2) → 可广播到 (2, 2)
print(np.greater(a, b))                  # [[ True False]
                                         #  [ True False]]
print(a > b)                             # [[ True False]
                                         #  [ True False]]
# greater_equal
print(np.greater_equal([4, 2], [2, 2]))  # [ True  True]
print(np.greater_equal(a, b))            # [[ True  True]
                                         #  [ True False]]
print(a >= b)                            # [[ True  True]
                                         #  [ True False]]
# less
print(np.less([4, 2], [2, 2]))           # [False False]
print(np.less(a, b))                     # [[False False]
                                         #  [False  True]]
print(a < b)                             # [[False False]
                                         #  [False  True]]
# less_equal
print(np.less_equal([4, 2], [2, 2]))     # [False  True]
print(np.less_equal(a, b))               # [[False  True]
                                         #  [False  True]]
print(a <= b)                            # [[False  True]
                                         #  [False  True]]
# equal
print(np.equal([4, 2], [2, 2]))          # [False  True]
print(np.equal(a, b))                    # [[False  True]
                                         #  [False False]]
print(a == b)                            # [[False  True]
                                         #  [False False]]
# not_equal
print(np.not_equal([4, 2], [2, 2]))      # [ True False]
print(np.not_equal(a, b))                # [[ True False]
                                         #  [ True  True]]
print(a != b)                            # [[ True False]
                                         #  [ True  True]]
```

---
## 八、 数学函数 (Mathematical Functions)
### 1. 三角函数 (Trigonometric Functions)
- `np.sin(x)`: 正弦函数 (Sine)
- `np.cos(x)`: 余弦函数 (Cosine)
- `np.tan(x)`: 正切函数 (Tangent)
- `np.arcsin(x)`: 反正弦函数 (Arcsine)
- `np.arccos(x)`: 反余弦函数 (Arccosine)
- `np.arctan(x)`: 反正切函数 (Arctangent)  
    （参数 `x` 对于三角函数为角度的弧度值）

```Python
import numpy as np
# 正弦函数 sin(x)：x 为弧度
print(np.sin(np.pi/2))                              # 1.0
print(np.sin(np.array((0, 30, 90)) * np.pi / 180))  # [0.  0.5 1. ]
# 余弦函数 cos(x)
print(np.cos(np.pi/2))                              # 6.123233995736766e-17 ≈ 0（浮点误差）
print(np.cos(np.array((0, 60, 90)) * np.pi / 180))  # [1.000000e+00 5.000000e-01 6.123234e-17]
# 正切函数 tan(x)
print(np.tan(-np.pi))                               # 1.2246467991473532e-16 ≈ 0
print(np.tan(np.array((0, 180)) * np.pi / 180))     # [ 0.0000000e+00 -1.2246468e-16]
# 反正弦 arcsin(x)：返回值范围 [-π/2, π/2]
print(np.arcsin(1))                                 # 1.5707963267948966 (= π/2)
print(np.arcsin(np.array([0.5, -0.5])))             # [ 0.52359878 -0.52359878] ≈ [π/6, -π/6]
# 反余弦 arccos(x)：返回值范围 [0, π]
print(np.arccos(-1))                                # 3.141592653589793 (= π)
print(np.arccos(np.array([0.5, 1])))                # [1.04719755 0.        ] ≈ [π/3, 0]
# 反正切 arctan(x)：返回值范围 [-π/2, π/2]
print(np.arctan(1))                                 # 0.7853981633974483 (= π/4)
print(np.arctan(np.array([0, -1])))                 # [ 0.         -0.78539816]
```

### 2. 其他数学函数
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
# e的0次方、e的1次方、e的2次方
print(np.exp([0, 1, 2]))  # [1.         2.71828183 7.3890561 ]
print(np.log([1, np.e, np.e**2]))  # [0. 1. 2.]
x = np.array([1, 2, 2**4])
print(np.log2(x))         # [0. 1. 4.]
print(np.log10([1e-15, 1000]))  # [-15.   3.]
```

---
## 九、 统计与聚合函数 (Statistics and Aggregation)
- `np.max(arr_like, axis=None, keepdims=False)`: 返回最大值
- `np.min(arr_like, axis=None, keepdims=False)`: 返回最小值
- `np.mean(arr_like, axis=None, keepdims=False)`: 返回平均值
- `np.var(arr_like, axis=None, keepdims=False)`: 返回方差
- `np.std(arr_like, axis=None, keepdims=False)`: 返回标准差
(对于以上函数，`axis` 没有指定时，默认为 `None`，表示返回所有元素的聚合结果。)

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

- `np.prod(arr_like, axis=None, keepdims=np._NoValue, initial=np._NoValue)`: 返回给定轴上数组元素的乘积
- `np.sum(arr_like, axis=None, keepdims=np._NoValue, initial=np._NoValue)`: 返回给定轴上数组元素的和

```Python
import numpy as np
# 默认的 axis=None 将计算输入数组中所有元素的乘积/和
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
## 十、 查找与极值 (Searching and Extremes)
- `np.nonzero(arr_like)`: 返回非零元素的索引
- `np.argwhere(arr_like)`: 找出数组中按元素分组的非零元素的索引
- `np.where(condition, x=None, y=None)`
    - `condition`: `array_like`, bool
    - `x`, `y`: `array_like`，要么都传参，要么都不传。
    - 如果传三个参数，条件成立返回 `x`，不成立时返回 `y`。如果只传第一个参数，返回符合条件的元素的索引。

```Python
import numpy as np
# nonzero
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
# argwhere
x = np.arange(6).reshape(2, 3)
print(x)                          # [[0 1 2]
                                  #  [3 4 5]]
print(x > 1)                      # [[False False  True]
                                  #  [ True  True  True]]
print(np.argwhere(x > 1))         # [[0 2]
                                  #  [1 0]
                                  #  [1 1]
                                  #  [1 2]]
# where
a = np.arange(10)
print(np.where(a < 5, a, 10*a))   # [ 0  1  2  3  4 50 60 70 80 90]
# 当where内有三个参数时，当condition成立时返回x，当condition不成立时返回y
print(np.where([[True, False], [True, True]], [[1, 2], [3, 4]], [[9, 8], [7, 6]]))  
# [[1 8]
#  [3 4]]
# 如果只传第一个参数，返回符合条件的元素的索引
a = np.array([2, 4, 6, 8, 10])
print(np.where(a > 5))            # (array([2, 3, 4]),)
```

- `np.maximum(x1, x2)`: 返回 `x1` 和 `x2` 逐个元素比较中的最大值
- `np.minimum(x1, x2)`: 返回 `x1` 和 `x2` 逐个元素比较中的最小值
- `np.argmax(arr_like, axis=None)`: 返回沿轴的最大值的索引
- `np.argmin(arr_like, axis=None)`: 返回沿轴的最小值的索引

```Python
import numpy as np
# maximum & minimum
print(np.maximum([2, 3, 4], [1, 5, 2]))          # [2 5 4]
print(np.maximum([[2, 3], [4, 5]], [[1, 5], [2, 6]]))  # [[2 5]
                                                       #  [4 6]]
print(np.minimum([2, 3, 4], [1, 5, 2]))          # [1 3 2]
print(np.minimum([[2, 3], [4, 5]], [[1, 5], [2, 6]]))  # [[1 3]
                                                       #  [2 5]]
# argmax & argmin
a = np.arange(6).reshape(2, 3) + 10
print(a)                                         # [[10 11 12]
                                                 #  [13 14 15]]
# 没有指定轴，则数组扁平化处理
print(np.argmax(a))                              # 5
print(np.argmax(a, axis=0))                      # [1 1 1]
print(np.argmax(a, axis=1))                      # [2 2]
print(np.argmin(a))                              # 0
print(np.argmin(a, axis=0))                      # [0 0 0]
print(np.argmin(a, axis=1))                      # [0 0]
```

---
## 十一、 随机模块 (Random Module)
- `np.random.normal(loc=0.0, scale=1.0, size=None)`:
    - `loc`: 均值 (中心)
    - `scale`: 标准差
    - `size`: 输出的形状
    - 返回从正态分布 (Normal Distribution) 中抽取的随机样本。
- `np.random.randint(low=None, high, size=None)`: 返回从 `[low, high)` 离散均匀分布 (Discrete Uniform Distribution) 中抽取的随机整数。
- `np.random.uniform(low=0.0, high=1.0, size=None)`: 返回从 `[low, high)` 均匀分布 (Uniform Distribution) 中抽取的随机样本。
- `np.random.permutation(x)`:
    - `x`: `int` or `array_like`
    - 如果 `x` 是整数，返回随机排列的 `np.arange(x)`
    - 如果 `x` 是数组，只对数组的第一个维度随机排列，返回新的数组。
- `np.random.seed([x])`: 随机数种子 (Random Seed)。

```Python
import numpy as np
# normal
print(np.random.normal(3, 2.5, size=(2, 4)))     
# [[2.77374601 6.39194169 3.50478002 0.32307184]
#  [1.79486353 3.11604183 3.17622272 3.59193008]]
# randint
print(np.random.randint(2, size=10))             # [0 1 0 1 0 0 0 0 0 1]
print(np.random.randint(0, 2, size=10))          # [1 1 1 0 0 1 1 1 1 0]
print(np.random.randint(1, 4, size=(2, 3)))      # [[2 2 3]
                                                 #  [3 1 2]]
# uniform
print(np.random.uniform(2, size=10))             
# [1.36872781 1.05440904 1.92293582 1.79682649 1.92452747 1.01096166
#  1.0021525  1.9405499  1.09845962 1.07890714]
print(np.random.uniform(0, 2, size=10))          
# [1.2311377  1.60301242 0.77386548 0.74841594 1.64789569 0.00279324
#  1.06320328 0.77354091 1.29033211 0.10265232]
print(np.random.uniform(1, 4, size=(2, 3)))      
# [[3.14995471 1.52158372 1.92005825]
#  [1.42513662 2.64660308 3.92028231]]
# permutation
print(np.random.permutation(6))                  # [1 0 3 4 5 2]
arr1 = np.array([0, 1, 2, 3, 4, 5])
print(np.random.permutation(arr1))               # [1 0 2 3 4 5]
arr2 = np.arange(10).reshape(5, 2)
print(np.random.permutation(arr2))               # [[2 3]
                                                 #  [4 5]
                                                 #  [0 1]
                                                 #  [8 9]
                                                 #  [6 7]]
# seed
np.random.seed(3)
print(np.random.uniform(1, 2, size=4))           
# [1.5507979  1.70814782 1.29090474 1.51082761]
np.random.seed(5)
print(np.random.uniform(1, 2, size=4))           
# [1.22199317 1.87073231 1.20671916 1.91861091]
np.random.seed(3)
print(np.random.uniform(1, 2, size=4))           
# [1.5507979  1.70814782 1.29090474 1.51082761]
np.random.seed()
print(np.random.uniform(1, 2, size=4))           
# [1.98011499 1.41251095 1.37907745 1.89147863]
```