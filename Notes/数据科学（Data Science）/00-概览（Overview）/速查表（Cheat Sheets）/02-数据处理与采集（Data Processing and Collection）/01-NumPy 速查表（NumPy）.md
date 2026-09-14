---
title: "NumPy 速查表（NumPy Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - numpy
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "NumPy 2.x；已按 2.5 参考手册核对"
---
# NumPy 速查表（NumPy Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
安装：`python -m pip install numpy`；导入：`import numpy as np`。核心对象 `ndarray` 由形状、数据类型、步幅和底层缓冲区共同定义。
- **安装包（Distribution）**：`numpy`。
- **导入模块（Import Module）**：`numpy`，惯例别名为 `np`。
- **安装命令（Installation）**：`python -m pip install -U numpy`。
- **用途（Purpose）**：多维数组、向量化运算、线性代数、随机采样与数值 I/O。
- **正式笔记（Detailed Note）**：[[01-NumPy 数值计算（NumPy）]]。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 创建、类型与形状（Creation, Dtype, and Shape）
先明确 `dtype` 与形状，避免隐式截断和对象数组。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|数组|`np.array(data, dtype=None)`|返回 ndarray；通常复制输入|
|等差序列|`np.arange(start, stop, step)`|返回半开区间数组；浮点步长可能累积误差|
|等分序列|`np.linspace(start, stop, num=50)`|返回固定元素数数组，默认包含 stop|
|全零|`np.zeros(shape, dtype=float)`|返回新数组|
|全一|`np.ones(shape, dtype=float)`|返回新数组|
|未初始化|`np.empty(shape, dtype=float)`|返回未初始化数组，值不可依赖|
|单位矩阵|`np.eye(n, m=None)`|返回二维数组|
|改形状|`a.reshape(*shape)`|尽可能返回视图，元素总数必须一致|
|增减维度|`np.expand_dims(a, axis) / np.squeeze(a, axis=None)`|返回视图；指定的压缩轴必须为 1|
|轴交换|`a.transpose(*axes) / np.moveaxis(a, src, dst)`|返回重排视图|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import numpy as np
a = np.arange(6).reshape(2, 3)
print(a.shape, a.dtype)
print(a.T)
# 期望输出:
# (2, 3) int64
# [[0 3]
#  [1 4]
#  [2 5]]
```
## 索引、选择与修改（Indexing, Selection, and Mutation）
基础切片常返回视图，高级索引通常返回副本。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|基础索引|`a[rows, cols]`|返回标量或视图|
|布尔筛选|`a[a > 0]`|返回一维副本|
|整数数组索引|`a[[2, 0]]`|返回副本|
|条件选择|`np.where(cond, x, y)`|返回按条件组合的新数组|
|截断|`np.clip(a, min, max)`|返回新数组；out 可原地写入|
|按索引取值|`np.take(a, indices, axis=None)`|返回新数组|
|按条件索引|`np.nonzero(a) / np.argwhere(a)`|返回索引元组或坐标数组|
|唯一值|`np.unique(a, return_counts=True)`|返回唯一值及可选索引、计数|
|排序|`np.sort(a, axis=-1)`|返回排序副本|
|原地排序|`a.sort(axis=-1)`|原地修改，返回 None|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import numpy as np
a = np.array([3, -1, 3, 5])
print(np.where(a > 0, a, 0))
print(np.unique(a, return_counts=True))
# 期望输出:
# [3 0 3 5]
# (array([-1,  3,  5]), array([1, 2, 1]))
```
## 广播、拼接与拆分（Broadcasting, Joining, and Splitting）
从尾维对齐；维度相等或其中一个为 1 才可广播。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|广播检查|`np.broadcast_shapes(shape1, shape2)`|返回共同形状；不兼容抛 ValueError|
|显式广播|`np.broadcast_to(a, shape)`|返回只读视图|
|纵向拼接|`np.concatenate(arrays, axis=0)`|沿已有轴返回新数组|
|新增轴堆叠|`np.stack(arrays, axis=0)`|沿新轴返回数组；各输入形状必须相同|
|垂直堆叠|`np.vstack(arrays)`|按第 0 轴拼接|
|水平堆叠|`np.hstack(arrays)`|按第 1 轴或一维横向拼接|
|均匀拆分|`np.split(a, sections, axis=0)`|返回视图列表；不能整除时抛 ValueError|
|近似拆分|`np.array_split(a, sections, axis=0)`|返回尽量均匀的数组列表|
|平铺|`a.ravel()`|尽可能返回视图|
|复制平铺|`a.flatten()`|总是返回副本|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import numpy as np
x = np.array([[1], [2]])
y = np.array([10, 20, 30])
print(x + y)
# 期望输出:
# [[11 21 31]
#  [12 22 32]]
```
## 统计、缺失值与线性代数（Statistics, Missing Values, and Linear Algebra）
`axis` 指被消去的轴；`keepdims=True` 保留维度便于广播。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|求和与均值|`np.sum(a, axis=None) / np.mean(a, axis=None)`|返回标量或降维数组|
|标准差|`np.std(a, axis=None, ddof=0)`|返回总体标准差；样本常用 ddof=1|
|忽略 NaN|`np.nanmean(a, axis=None)`|忽略 NaN；全 NaN 切片产生警告和 NaN|
|最大值索引|`np.argmax(a, axis=None)`|返回首次最大值索引|
|分位数|`np.quantile(a, q, axis=None)`|返回分位数|
|矩阵乘|`a @ b / np.matmul(a, b)`|返回矩阵乘结果，内维必须匹配|
|点积|`np.dot(a, b)`|随维数语义变化；高维优先明确使用 matmul/einsum|
|求解线性方程|`np.linalg.solve(A, b)`|返回解；奇异矩阵抛 LinAlgError|
|SVD|`np.linalg.svd(A, full_matrices=False)`|返回 U、奇异值、Vh|
|范数|`np.linalg.norm(a, ord=None, axis=None)`|返回范数|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import numpy as np
a = np.array([[1., 2.], [3., 4.]])
print(a.mean(axis=0))
print(np.linalg.solve(a, np.array([5., 11.])))
# 期望输出:
# [2. 3.]
# [1. 2.]
```
## 随机、保存与性能（Randomness, Persistence, and Performance）
使用 `Generator` 隔离随机状态；向量化前先测量。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|随机生成器|`np.random.default_rng(seed)`|返回 Generator|
|均匀随机|`rng.random(shape)`|返回 [0,1) 浮点数组|
|正态随机|`rng.normal(loc=0, scale=1, size=None)`|返回标量或数组|
|随机整数|`rng.integers(low, high=None, size=None)`|返回整数，high 不包含|
|抽样|`rng.choice(a, size=None, replace=True, p=None)`|返回样本；无放回时 size 不得超总体|
|打乱|`rng.shuffle(a, axis=0)`|原地打乱，返回 None|
|二进制保存|`np.save(path, a)`|写 `.npy`，有外部副作用|
|多数组压缩|`np.savez_compressed(path, **arrays)`|写 `.npz`|
|二进制读取|`np.load(path, allow_pickle=False)`|返回数组或 NpzFile|
|内存映射|`np.memmap(path, dtype, mode, shape)`|返回磁盘映射数组|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import numpy as np
rng = np.random.default_rng(42)
print(rng.integers(0, 10, size=4))
# 期望输出:
# [0 7 6 4]
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
- [[01-NumPy 数值计算（NumPy）]]
- [[01-基于 NumPy 的三层 BP 神经网络（Three-layer BP Neural Network with NumPy）]]
## 官方参考（Official References）
- [NumPy 参考手册](https://numpy.org/doc/stable/reference/routines.html)
