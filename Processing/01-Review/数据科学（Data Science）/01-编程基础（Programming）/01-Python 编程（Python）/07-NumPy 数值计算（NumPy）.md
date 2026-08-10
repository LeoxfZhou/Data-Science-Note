---
title: NumPy 数值计算（NumPy）
aliases:
  - NumPy
status: review
detail_level: comprehensive
source:
  - Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/NumPy.md
suggested_target: Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/07-NumPy 数值计算（NumPy）.md
operation: 新建
merge_target: null
---

# NumPy 数值计算（NumPy）

## 1. `ndarray` 的核心属性

NumPy 的核心是同质多维数组 `ndarray`。同一数组中的元素通常共享一个 `dtype`，因此它能进行高效的向量化运算。

```python
import numpy as np

array = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32)

print(array.shape)   # (2, 3)
print(array.ndim)    # 2
print(array.size)    # 6
print(array.dtype)   # float32
print(array.itemsize)
```

在深度学习代码中，先检查 `shape`、`dtype` 和设备，往往比直接修改模型更快定位问题。

## 2. 创建数组

```python
import numpy as np

zeros = np.zeros((2, 3), dtype=np.float32)
ones = np.ones((2, 3))
filled = np.full((2, 3), 7)

integers = np.arange(0, 10, 2)
points = np.linspace(0.0, 1.0, num=5)
identity = np.eye(3)
```

`arange()` 更适合整数步长；需要指定区间内固定数量的浮点数时优先 `linspace()`。

## 3. 索引、切片、视图与副本

```python
import numpy as np

array = np.arange(12).reshape(3, 4)

print(array[1, 2])
print(array[:, 1])
print(array[1:, :2])
print(array[array % 2 == 0])  # 布尔索引。
```

> [!warning] 切片通常是视图
> 修改切片可能同时修改原数组。需要独立数据时显式调用 `.copy()`。

```python
view = array[:, :2]
view[0, 0] = 999
print(array[0, 0])  # 999

independent = array[:, :2].copy()
independent[0, 0] = -1
```

基础切片通常返回视图；整数数组索引和布尔索引通常返回副本。不要仅凭变量名判断是否共享内存。

## 4. 向量化运算

```python
import numpy as np

values = np.array([1.0, 2.0, 3.0])

normalized = (values - values.mean()) / values.std()
clipped = np.clip(values, 1.5, 2.5)
mask = values > 1.5
```

优先数组运算，不要把 NumPy 当作普通列表逐元素循环；向量化通常更简洁，也能利用底层优化。

## 5. 广播（Broadcasting）

NumPy 从最后一个维度开始比较形状；两个维度相等，或其中一个为 `1` 时可以广播。缺失的前导维度视为 `1`。

```python
import numpy as np

matrix = np.array([[1, 2, 3], [4, 5, 6]])  # (2, 3)
column_means = matrix.mean(axis=0)           # (3,)
centered = matrix - column_means             # (2, 3) - (3,) 可以广播。
```

无法广播的例子：`(2, 3)` 与 `(2,)`，因为最后一维 `3` 和 `2` 既不相等，也没有一个是 `1`。

## 6. `axis` 与聚合

```python
import numpy as np

matrix = np.array([[1, 2, 3], [4, 5, 6]])

matrix.sum()          # 所有元素。
matrix.sum(axis=0)    # 压缩行轴，得到每一列的和，shape=(3,)。
matrix.sum(axis=1)    # 压缩列轴，得到每一行的和，shape=(2,)。
matrix.mean(axis=1, keepdims=True)  # shape=(2, 1)，便于继续广播。
```

理解 `axis` 的可靠方法是：指定哪个轴，哪个轴就在聚合结果中被压缩。

## 7. 形状变换与拼接

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

## 8. 矩阵乘法

```python
import numpy as np

features = np.array([[1.0, 2.0], [3.0, 4.0]])
weights = np.array([[0.5], [1.5]])

predictions = features @ weights
```

- `*` 是逐元素乘法。
- `@` / `np.matmul()` 是矩阵乘法。
- 高维批量矩阵乘法时，`matmul` 会把最后两个轴当作矩阵轴，并广播前面的批次轴。

## 9. 随机数与可复现性

```python
import numpy as np

# 新代码优先使用 Generator，避免依赖全局随机状态。
rng = np.random.default_rng(seed=42)

samples = rng.normal(loc=0.0, scale=1.0, size=(100, 3))
indices = rng.choice(len(samples), size=10, replace=False)
rng.shuffle(samples)
```

固定种子能复现实验中的随机序列，但不保证跨所有库、硬件和版本得到完全相同结果。

## 10. 缺失值、无穷值与数值稳定性

```python
import numpy as np

values = np.array([1.0, np.nan, np.inf])

print(np.isnan(values))
print(np.isfinite(values))
print(np.nanmean(values))
```

整数数组不能直接存储 `NaN`；加入 `NaN` 通常会转换为浮点类型。

```python
probabilities = np.array([1e-12, 0.5, 1.0])
safe_probabilities = np.clip(probabilities, 1e-7, 1 - 1e-7)
log_values = np.log(safe_probabilities)
```

## 11. 保存与加载

```python
import numpy as np

array = np.arange(6).reshape(2, 3)
np.save("array.npy", array)
loaded = np.load("array.npy")

np.savez("arrays.npz", features=array, labels=np.array([0, 1]))
archive = np.load("arrays.npz")
```

`.npy/.npz` 能保留形状和 `dtype`；与其他工具交换表格数据时再考虑 CSV。

## 12. 数据类型 (Data Types) 与类型转换 (Type Casting)

常见数据类型 (Data Types)：

| 类别 | 常见 `dtype` | 说明 |
|---|---|---|
| 有符号整数 (Signed Integer) | `int8`、`int16`、`int32`、`int64` | 位数决定可表示范围 |
| 无符号整数 (Unsigned Integer) | `uint8`、`uint16`、`uint32` | 图像像素常见 `uint8` |
| 浮点数 (Floating Point) | `float16`、`float32`、`float64` | 精度、内存和速度不同 |
| 复数 (Complex Number) | `complex64`、`complex128` | 实部和虚部均为浮点数 |
| 布尔值 (Boolean) | `bool_` | 常用于掩码 (Mask) |
| 字符串 (String) | `str_`、`bytes_` | 长度通常固定在数组 `dtype` 中 |

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

> [!warning] 整数溢出 (Integer Overflow)
> 固定位数整数超过范围时可能回绕。处理像素累加、计数和大索引时要确认 `dtype`。

```python
pixels = np.array([250, 10], dtype=np.uint8)
print(pixels.sum())  # 聚合通常提升类型，但逐元素运算仍需检查 dtype。

safe_pixels = pixels.astype(np.int16)
print(safe_pixels + 20)
```

## 13. 通用函数 (Universal Functions, Ufuncs)

通用函数 (Universal Functions, Ufuncs) 对数组逐元素运算，并支持广播 (Broadcasting)、输出数组和条件掩码。

```python
import numpy as np

values = np.array([-1.0, 0.0, 1.0])

print(np.abs(values))
print(np.exp(values))
print(np.log1p(values[1:]))  # log(1 + x)，小 x 时比直接计算更稳定。
print(np.sqrt(np.clip(values, 0, None)))
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

## 14. 高级索引 (Advanced Indexing)

### 整数数组索引 (Integer Array Indexing)

```python
import numpy as np

matrix = np.arange(12).reshape(3, 4)
rows = np.array([2, 0, 2])

selected_rows = matrix[rows]
selected_values = matrix[[0, 1, 2], [1, 2, 3]]
```

多个整数索引数组会先广播，再逐位置组合坐标；它们不是自动形成笛卡尔积 (Cartesian Product)。需要行列网格时使用 `np.ix_()`：

```python
row_indices = [0, 2]
column_indices = [1, 3]
submatrix = matrix[np.ix_(row_indices, column_indices)]
```

### 条件选择 (Conditional Selection)

```python
values = np.array([-2, -1, 0, 1, 2])

positive = values[values > 0]
labels = np.where(values >= 0, "non-negative", "negative")
bounded = np.clip(values, -1, 1)
```

## 15. 排序、查找与集合操作

```python
import numpy as np

values = np.array([3, 1, 3, 2])

print(np.sort(values))
print(np.argsort(values))       # 返回排序后元素对应的原索引。
print(np.unique(values))
print(np.unique(values, return_counts=True))
print(np.where(values == 3)[0])
```

```python
left = np.array([1, 2, 3])
right = np.array([3, 4])

np.intersect1d(left, right)
np.union1d(left, right)
np.setdiff1d(left, right)
np.isin(left, right)
```

## 16. 统计与分位数 (Quantiles)

```python
import numpy as np

values = np.array([1.0, 2.0, 3.0, 100.0])

print(values.mean())
print(np.median(values))
print(values.var(ddof=0))  # 总体方差 (Population Variance)。
print(values.var(ddof=1))  # 样本方差 (Sample Variance)。
print(np.quantile(values, [0.25, 0.5, 0.75]))
```

`ddof` 表示自由度修正 (Delta Degrees of Freedom)。统计定义不同会产生不同结果，不能只记 API 而忽略问题语义。

## 17. 线性代数 (Linear Algebra)

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

## 18. 内存布局 (Memory Layout) 与性能

NumPy 数组通常以连续内存存储。转置和切片可能创建非连续视图 (Non-contiguous View)，某些底层库需要连续数组。

```python
array = np.arange(12).reshape(3, 4)
transposed = array.T

print(array.flags["C_CONTIGUOUS"])
print(transposed.flags["C_CONTIGUOUS"])

contiguous = np.ascontiguousarray(transposed)
```

优化顺序：

1. 先选择正确算法和数据结构。
2. 用向量化 (Vectorization) 替代 Python 层逐元素循环。
3. 避免不必要的副本 (Copy) 和类型转换 (Type Casting)。
4. 测量真实瓶颈后再优化内存布局。

## 19. 常见错误

- 混淆 `*` 与 `@`。
- 不知道切片共享原数组数据。
- 忽略整数除法、类型提升或低精度溢出。
- 只看元素数量，不检查轴顺序。
- 用 Python 循环替代本可向量化的操作。
- 使用 `np.empty()` 后忘记初始化其中的数据。

## 20. 完成检查

- [ ] 能根据 `shape` 判断每个轴的含义。
- [ ] 能解释广播规则和 `axis` 聚合。
- [ ] 能区分视图与副本、`concatenate` 与 `stack`、`*` 与 `@`。
- [ ] 能使用布尔索引和向量化完成数据筛选与变换。
- [ ] 能使用 `default_rng()` 生成可复现随机数据。

## 参考资料

- [NumPy User Guide](https://numpy.org/doc/stable/user/)
- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
