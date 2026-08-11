---
title: PyTorch 张量基础（PyTorch Tensor Fundamentals）
aliases:
  - PyTorch Tensor Fundamentals
  - PyTorch 张量
tags:
  - data-science/deep-learning/pytorch
  - programming/python
status: published
published_at: 2026-08-11
created: 2026-08-11
---
# PyTorch 张量基础（PyTorch Tensor Fundamentals）
## 1. PyTorch 概览（PyTorch Overview）
### 1.1 定位与用途（Positioning and Uses）
- PyTorch 是基于 Python 的科学计算与机器学习框架（Machine Learning Framework），用张量（Tensor）表示数据、模型输入、模型输出和参数。
- 张量 API 与 NumPy 的多维数组（Multidimensional Array）相似，但可以在中央处理器（Central Processing Unit, CPU）、图形处理器（Graphics Processing Unit, GPU）及其他受支持的加速设备上运行。
- PyTorch 同时提供自动微分（Automatic Differentiation）、神经网络模块（Neural Network Module）、损失函数（Loss Function）、优化器（Optimizer）、数据加载和分布式训练等能力。
- 常见应用包括计算机视觉（Computer Vision）、自然语言处理（Natural Language Processing）、强化学习（Reinforcement Learning）、科研原型和工业模型训练与部署。
- 与 scikit-learn 侧重统一的传统机器学习估计器接口不同，PyTorch 更关注张量计算、可组合网络结构、损失计算、梯度传播和参数优化。
### 1.2 主要特征（Key Features）
- **类 NumPy 张量计算（NumPy-like Tensor Computing）**：支持索引、广播（Broadcasting）、归约（Reduction）、线性代数和逐元素运算。
- **自动微分（Autograd）**：根据运行时实际执行的运算构建计算图（Computation Graph），通过链式法则（Chain Rule）计算梯度。
- **神经网络库（Neural Network Library）**：`torch.nn` 提供全连接层、卷积层、循环层、激活函数和损失函数；`torch.optim` 提供 SGD、Adam 等优化算法。
- **动态执行（Dynamic Execution）**：普通 Python 控制流可以直接参与前向计算，便于调试和研究。TensorFlow 1.x 主要使用静态图；TensorFlow 2.x 的即时执行（Eager Execution）同样支持动态风格，因此“PyTorch 动态、TensorFlow 静态”只适用于历史版本比较。
- **硬件加速（Hardware Acceleration）**：模型和数据必须位于兼容的设备与数据类型上，通常通过 `.to(device)` 迁移。
- **跨平台与分布式能力（Cross-platform and Distributed Support）**：支持 Linux、Windows、macOS，以及多 GPU 和分布式训练；具体设备支持取决于 PyTorch 构建版本与硬件后端，不能笼统认为所有安装都支持 CUDA 或 TPU。
### 1.3 简要发展脉络（Brief History）
- **Torch / Torch7**：早期 Torch 由 Ronan Collobert、Clément Farabet 等人推动，是提供多维张量与科学计算工具的框架；Torch7 使用 Lua，在深度学习中得到应用，之后逐渐停止维护。
- **PyTorch 0.1.0**：原稿把 2016 年 FAIR 发布的首个 PyTorch 版本记为 0.1.0。它承接 Torch7 的张量与神经网络经验，同时采用更符合 Python 习惯的接口，使模型定义和调试更直观。
- **PyTorch 0.2.0 的来源说法**：原稿称 0.2.0 “首次引入动态图”。该表述的精确版本时间线没有在本轮官方 API 文档中得到支持；动态图/运行时定义（Define-by-run）是早期 PyTorch 的核心设计，正式笔记不把“0.2.0 首次引入”当作已确认事实，但保留这项来源差异供审核。
- **PyTorch 1.0**：2018 年的稳定版本整合研究原型与生产部署路径，并延续即时执行（Eager Execution）体验。
- **PyTorch 2.x**：引入 `torch.compile` 编译加速路径，并持续改进编译器、分布式和硬件后端。版本能力应以当前官方文档为准，不应把 TorchDynamo 简化为对所有 `torch.jit.trace`、`torch.jit.script` 使用场景的直接替代。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/02-框架与工具（Frameworks and Tools）/01-PyTorch 张量基础（PyTorch Tensor Fundamentals）/01-PyTorch 张量基础（PyTorch Tensor Fundamentals）-20260328152712627.png|PyTorch 发展与编译栈]]
### 1.4 安装与环境确认（Installation and Environment Check）
- CPU、CUDA 和其他后端需要不同安装组合，优先使用 PyTorch 官网安装选择器生成命令。
- 原稿使用清华镜像安装通用 `torch` 包，命令可用于兼容的平台，但不会自动保证获得所需 CUDA 构建：
```bash
python -m pip install torch -i https://pypi.tuna.tsinghua.edu.cn/simple
```
- 安装后同时检查 Python、PyTorch、设备和后端状态：
```python
import sys
import torch

print(sys.version_info.major)  # 3
print(torch.__version__)       # 版本因环境而异，例如 2.6.0+cpu
print(torch.cuda.is_available())  # 仅在 CUDA 构建、驱动和硬件均可用时为 True
```
## 2. 张量模型（Tensor Model）
### 2.1 张量、维度与形状（Tensor, Dimension, and Shape）
- 张量（Tensor）是元素具有统一数据类型（Data Type）的多维、带步幅（Stride）数组，是 PyTorch 的核心数据抽象。
- 零维张量（0-D Tensor）表示标量（Scalar）；一维张量（1-D Tensor）表示向量（Vector）；二维张量（2-D Tensor）常表示矩阵（Matrix）。多个二维张量可以组成三维张量，多个三维张量可以组成四维张量，以此类推。
- `shape` 或 `size()` 描述每个维度的元素个数；`ndim` 描述维度数量；`numel()` 返回元素总数。
- 张量还携带 `dtype`、`device`、`layout` 和 `requires_grad` 等属性。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/02-框架与工具（Frameworks and Tools）/01-PyTorch 张量基础（PyTorch Tensor Fundamentals）/01-PyTorch 张量基础（PyTorch Tensor Fundamentals）-20260328152709468.png|张量的维度示意]]
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/02-框架与工具（Frameworks and Tools）/01-PyTorch 张量基础（PyTorch Tensor Fundamentals）/01-PyTorch 张量基础（PyTorch Tensor Fundamentals）-20260328152705946.png|多个二维张量组成三维张量]]
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/02-框架与工具（Frameworks and Tools）/01-PyTorch 张量基础（PyTorch Tensor Fundamentals）/01-PyTorch 张量基础（PyTorch Tensor Fundamentals）-20260328152710883.png|高维张量组合示意]]
### 2.2 常见数据类型（Common Data Types）

|类别（Category）|常用 `dtype`|典型用途|
|---|---|---|
|浮点数（Floating Point）|`torch.float16`、`torch.bfloat16`、`torch.float32`、`torch.float64`|模型计算、连续特征|
|有符号整数（Signed Integer）|`torch.int8`、`torch.int16`、`torch.int32`、`torch.int64`|类别索引、计数、离散数据|
|无符号整数（Unsigned Integer）|`torch.uint8` 等受支持类型|图像或底层数据；运算支持需核对版本|
|布尔值（Boolean）|`torch.bool`|掩码（Mask）、逻辑判断|
|复数（Complex Number）|`torch.complex64`、`torch.complex128`|信号和频域计算|

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/02-框架与工具（Frameworks and Tools）/01-PyTorch 张量基础（PyTorch Tensor Fundamentals）/01-PyTorch 张量基础（PyTorch Tensor Fundamentals）-20260328152712389.png|PyTorch 数据类型表]]
- `torch.randn()`、`torch.rand()`、`torch.zeros()` 和 `torch.ones()` 未显式指定类型时通常使用当前默认浮点类型，通常为 `torch.float32`。
- 由 Python 整数序列推断的张量通常为 `torch.int64`；由 Python 浮点序列推断的张量通常使用默认浮点类型。
- 由 NumPy 数组创建时通常保留 NumPy 的数据类型，例如 macOS 上某些历史 NumPy 整数数组可能是 `int64`，原 notebook 保存输出中的 `int32` 不能视为跨平台固定结果。
- 默认设备通常是 CPU，但现代 PyTorch 可以修改默认设备；稳健代码应显式记录或指定 `device`。
### 2.3 核心属性检查（Core Property Inspection）
```python
import torch

x = torch.ones((2, 3), dtype=torch.float64)
print(x.shape)          # torch.Size([2, 3])
print(x.dtype)          # torch.float64
print(x.device.type)    # 'cpu'（默认环境）
print(x.requires_grad)  # False
print(x.ndim)           # 2
print(x.numel())        # 6
```
## 3. 创建张量（Creating Tensors）
### 3.1 从 Python 数据创建（Create from Python Data）
- `torch.tensor(data, *, dtype=None, device=None, requires_grad=False)` 会复制输入数据并创建没有既有自动微分历史的叶张量（Leaf Tensor）。
- 支持标量、列表、元组、NumPy 数组等类数组输入；未指定 `dtype` 时执行类型推断。
- 从 Python 列表创建后，列表与张量不共享内存，修改一方不会影响另一方。
```python
import torch

source = [1, 2, 3]
x = torch.tensor(source)
source[0] = 100
x[1] = 200
print(source)    # [100, 2, 3]
print(x.tolist())  # [1, 200, 3]
```
- `Tensor.tolist()` 把张量转换为嵌套 Python 列表或标量；必要时会先在内部转到 CPU，且该转换不可微分。大张量转换会产生大量 Python 对象，不适合性能关键路径。
### 3.2 按形状或指定值创建（Create by Shape or Value）
- `torch.empty(size)` 创建未初始化张量，其内容来自已分配内存，不能把显示出的任意数值当作初始值。
- 历史代码中的 `torch.Tensor(2, 3)` 等价于创建未初始化的默认浮点张量；新代码优先使用语义明确的 `torch.empty()` 或 `torch.tensor(data)`。
- `torch.zeros()`、`torch.ones()`、`torch.full()` 分别创建全 0、全 1、指定填充值张量；对应的 `_like` 版本继承参考张量的形状，并默认继承其类型和设备。
```python
import torch

zeros = torch.zeros((2, 3))
ones = torch.ones_like(zeros, dtype=torch.float64)
tens = torch.full((2, 3), 10)
print(zeros.shape, zeros.sum().item())  # torch.Size([2, 3]) 0.0
print(ones.dtype, ones.sum().item())    # torch.float64 6.0
print(tens.tolist())                    # [[10, 10, 10], [10, 10, 10]]
```
- `torch.IntTensor()`、`torch.FloatTensor()`、`torch.DoubleTensor()` 等旧式类型构造器仍可能出现在历史材料中，但容易混淆“按形状创建”和“按数据创建”，新代码优先传 `dtype=`。其他旧式构造器还包括 `ShortTensor`（`int16`）和 `LongTensor`（`int64`）；把浮点列表传给整数构造器会发生数值类型转换，例如 `torch.IntTensor([2.5, 3.3]).tolist()` 得到 `[2, 3]`，不应依赖隐式转换处理需要舍入的业务数据。
### 3.3 线性序列与随机张量（Linear Sequences and Random Tensors）
- `torch.arange(start, end, step)` 按步长生成左闭右开区间 `[start, end)`。
- `torch.linspace(start, end, steps)` 按元素个数生成包含两端点的序列；当 `steps > 1` 时，相邻差为 `(end - start) / (steps - 1)`。
- `torch.rand(size)` 生成 `[0, 1)` 上均匀分布（Uniform Distribution）的随机数；`torch.randn(size)` 生成均值 0、标准差 1 的标准正态分布（Standard Normal Distribution）随机数。
- `torch.randint(low, high, size)` 生成左闭右开区间 `[low, high)` 的随机整数，默认通常为 `torch.int64`。
- `torch.manual_seed(seed)` 设置随机种子；`torch.initial_seed()` 返回当前生成器的初始种子。完全可复现还可能需要设备、算法和并行设置配合。
```python
import torch

print(torch.arange(0, 10, 2).tolist())       # [0, 2, 4, 6, 8]
print(torch.linspace(0, 9, 10).tolist())     # [0.0, 1.0, ..., 9.0]
torch.manual_seed(100)
normal = torch.randn((2, 3))
integers = torch.randint(0, 10, size=(10,))
print(normal.shape, normal.dtype)             # torch.Size([2, 3]) torch.float32
print(integers.shape, integers.dtype)         # torch.Size([10]) torch.int64
```
## 4. NumPy 与 Python 转换（NumPy and Python Conversion）
### 4.1 NumPy 到张量（NumPy to Tensor）

|方法（Method）|是否复制（Copy）|内存关系与限制|
|---|---|---|
|`torch.tensor(array)`|是|创建独立副本；后续修改互不影响|
|`torch.from_numpy(array)`|否|CPU 张量与数组共享内存；返回张量不可调整底层存储大小|
|`torch.as_tensor(array)`|尽可能不复制|在兼容时共享数据并尽可能保留历史|

```python
import numpy as np
import torch

array = np.array([1, 2, 3], dtype=np.int64)
copied = torch.tensor(array)
shared = torch.from_numpy(array)
array[0] = 100
shared[1] = 200
print(copied.tolist())  # [1, 2, 3]
print(shared.tolist())  # [100, 200, 3]
print(array.tolist())   # [100, 200, 3]
```
> [!warning] 共享内存边界（Shared-memory Boundary）
> 不要写入由只读 NumPy 数组创建的共享张量；官方文档将这种写入行为定义为不受支持。共享对象的生命周期、连续性和数据类型也必须满足接口要求。
### 4.2 张量到 NumPy（Tensor to NumPy）
- CPU 张量调用 `.numpy()` 时通常与返回的 `ndarray` 共享内存；如需隔离，使用 `.numpy().copy()`。
- 需要梯度的张量不能直接调用传统 `.numpy()` 路径，应先停止梯度关联并移到 CPU：`tensor.detach().cpu().numpy()`。
- 非 CPU 张量需要先 `.cpu()`；直接转换会因设备不受 NumPy 支持而失败。
```python
import torch

tensor = torch.tensor([2, 3, 4])
shared_array = tensor.numpy()
copied_array = tensor.numpy().copy()
shared_array[0] = 100
copied_array[1] = 200
print(tensor.tolist())        # [100, 3, 4]
print(shared_array.tolist())  # [100, 3, 4]
print(copied_array.tolist())  # [2, 200, 4]
```
### 4.3 提取标量（Extracting a Scalar）
- `.item()` 只适用于仅含一个元素的张量，返回对应 Python 数值；多元素张量调用会抛出异常。
```python
import torch

print(torch.tensor([30]).item())  # 30
print(torch.tensor(30).item())    # 30
```
## 5. 类型与设备（Dtype and Device）
### 5.1 类型转换（Dtype Conversion）
- 通用写法是 `tensor.to(dtype=...)`；便捷方法包括 `.half()`、`.float()`、`.double()`、`.short()`、`.int()` 和 `.long()`。
- 历史写法 `.type(torch.DoubleTensor)` 可以工作，但它把设备类型和数据类型绑定在旧式张量类中；现代代码优先使用 `.to()`。
```python
import torch

x = torch.full((2, 3), 10)
y = x.to(dtype=torch.float64)
z = x.double()
print(x.dtype)  # torch.int64
print(y.dtype)  # torch.float64
print(z.dtype)  # torch.float64
```
### 5.2 设备选择与迁移（Device Selection and Transfer）
- 数据、参数和参与同一运算的张量通常必须处于相同设备；否则会出现设备不匹配错误。
- `torch.device("cuda" if torch.cuda.is_available() else "cpu")` 是 CUDA/CPU 二选一的基础写法；Apple Silicon、XPU 等后端应根据项目需求单独检测。
- `.to(device=device, dtype=dtype)` 可同时迁移设备和转换数据类型；如果目标属性相同，可能直接返回原对象。
- `nn.Module.to(device)` 会迁移已注册参数（Registered Parameter）和缓冲区（Buffer）；输入张量仍需单独迁移。
```python
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
x = torch.ones((2, 3), dtype=torch.float32).to(device)
print(x.shape)        # torch.Size([2, 3])
print(x.device.type)  # 'cuda' 或 'cpu'，取决于环境
```
## 6. 数值运算与广播（Numerical Operations and Broadcasting）
### 6.1 基本运算与原地操作（Basic and In-place Operations）
- 运算符 `+`、`-`、`*`、`/` 和一元负号分别对应加、减、逐元素乘、除和取负；方法形式包括 `.add()`、`.sub()`、`.mul()`、`.div()`、`.neg()`。
- 以 `_` 结尾的方法（如 `.add_()`）是原地操作（In-place Operation），会直接修改对象。原地修改共享存储的视图或参与自动微分的值时尤其容易破坏所需历史，应谨慎使用。
```python
import torch

x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
y = x.add(10)
x.add_(10)
print(y.tolist())  # [[11.0, 12.0], [13.0, 14.0]]
print(x.tolist())  # [[11.0, 12.0], [13.0, 14.0]]
print(x.sub(100).tolist())  # [[-89.0, -88.0], [-87.0, -86.0]]
print(x.mul(2).tolist())    # [[22.0, 24.0], [26.0, 28.0]]
print(x.div(2).tolist())    # [[5.5, 6.0], [6.5, 7.0]]
print(x.neg().tolist())     # [[-11.0, -12.0], [-13.0, -14.0]]
```
### 6.2 广播（Broadcasting）
- 从最后一个维度向前比较：两个维度相等、其中一个为 1，或其中一方不存在时，维度可广播。
- 原 notebook 的 `(2, 3) + (2, 1)`、标量乘张量、`(1, 3) * (2, 3)` 都利用了广播。
- 广播通常通过步幅为 0 的视图避免真实复制；对扩展视图做原地写入可能让多个逻辑元素指向同一内存位置，必要时先 `.clone()`。
```python
import torch

x = torch.tensor([[1, 2, 3], [4, 5, 6]])
column = torch.tensor([[10], [20]])
row = torch.tensor([[2, 3, 4]])
print((x + column).tolist())  # [[11, 12, 13], [24, 25, 26]]
print((x * row).tolist())     # [[2, 6, 12], [8, 15, 24]]
```
### 6.3 哈达玛积与矩阵乘法（Hadamard Product and Matrix Multiplication）
- `x * y` 或 `torch.mul(x, y)` 表示逐元素乘法（Element-wise Multiplication），也称哈达玛积（Hadamard Product），允许兼容的广播形状。
- `x @ y` 或 `torch.matmul(x, y)` 表示矩阵乘法（Matrix Multiplication）。二维情况下，`(n, m) @ (m, p)` 得到 `(n, p)`。
- 对高维输入，`matmul` 把最后两个维度视为矩阵维度，前面的批次维度执行广播；原 notebook 的 `(2, 3, 2) @ (2, 2, 1)` 得到 `(2, 3, 1)`。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/02-框架与工具（Frameworks and Tools）/01-PyTorch 张量基础（PyTorch Tensor Fundamentals）/01-PyTorch 张量基础（PyTorch Tensor Fundamentals）-20260328152707553.png|逐元素乘法示意]]
```python
import torch

a = torch.tensor([[1, 2], [3, 4], [5, 6]])
b = torch.tensor([[5, 6], [7, 8]])
print((a * a).tolist())  # [[1, 4], [9, 16], [25, 36]]
print((a @ b).tolist())  # [[19, 22], [43, 50], [67, 78]]

batched_a = torch.ones((2, 3, 2))
batched_b = torch.ones((2, 2, 1))
print(torch.matmul(batched_a, batched_b).shape)  # torch.Size([2, 3, 1])
```
### 6.4 归约与常用数学函数（Reductions and Common Math Functions）
- `.mean(dim=...)` 与 `.sum(dim=...)` 沿指定维度求均值与和；不指定 `dim` 时归约所有元素。
- 对二维 `(row, column)` 张量，`dim=0` 消除行维度并对各列归约，`dim=1` 消除列维度并对各行归约；更高维张量应按轴编号理解，不能死记“按行/按列”。
- `.min()`、`.max()` 返回极值；按维度调用时通常同时返回值和索引。
- `torch.argmax(x, dim)` 返回最大值索引；`torch.topk(x, k, dim)` 返回最大的 `k` 个值及其索引。
- `torch.abs()`、`.pow()`、`.sqrt()`、`.exp()`、`.log()`、`.log2()`、`.log10()` 分别执行绝对值、幂、平方根、指数和不同底数的对数。平方根负数、非正数对数会产生非有限结果，使用前应检查定义域。
```python
import torch

x = torch.tensor([[1.0, 3.0, 2.0], [4.0, 0.0, 5.0]])
print(x.mean(dim=0).tolist())  # [2.5, 1.5, 3.5]
print(x.sum(dim=1).tolist())   # [6.0, 9.0]
print(torch.argmax(x, dim=-1).tolist())  # [1, 2]
top = torch.topk(x, k=2, dim=-1)
print(top.values.tolist())   # [[3.0, 2.0], [5.0, 4.0]]
print(top.indices.tolist())  # [[1, 2], [2, 0]]
print(torch.abs(torch.tensor([-2.0, 3.0])).tolist())  # [2.0, 3.0]
```
## 7. 索引（Indexing）
### 7.1 基础与范围索引（Basic and Slice Indexing）
- `x[0]` 取第 0 个切片，`x[:, 0]` 取所有行的第 0 列，`x[:3, :2]` 取前 3 行、前 2 列。
- 基础索引通常返回共享底层存储的视图；对结果原地写入可能同步修改原张量。
### 7.2 高级、布尔与多维索引（Advanced, Boolean, and Multidimensional Indexing）
- `x[[0, 1], [1, 2]]` 成对选择 `(0, 1)` 与 `(1, 2)` 两个元素。
- `x[[[0], [1]], [1, 2]]` 通过索引广播得到第 0、1 行与第 1、2 列的笛卡尔组合。
- `x[x[:, 2] > 5]` 用布尔掩码选择第 3 列大于 5 的整行；`x[:, x[1] > 5]` 按第 2 行条件选择列。
- 三维张量中，`x[0, :, :]`、`x[:, 0, :]`、`x[:, :, 0]` 分别固定第 0、1、2 轴上的一个索引。
- 高级索引通常返回副本；无论基础还是高级索引，赋值表达式会写回原张量。
```python
import torch

x = torch.arange(20).reshape(4, 5)
print(x[0].tolist())                 # [0, 1, 2, 3, 4]
print(x[:, 0].tolist())              # [0, 5, 10, 15]
print(x[[0, 1], [1, 2]].tolist())    # [1, 7]
print(x[:3, :2].tolist())            # [[0, 1], [5, 6], [10, 11]]
print(x[x[:, 2] > 5].shape)          # torch.Size([3, 5])
```
## 8. 形状、视图与连续性（Shape, Views, and Contiguity）
### 8.1 `reshape()` 与 `view()`
- `reshape(*shape)` 在元素总数不变的前提下改变形状；可以用一个 `-1` 自动推断对应维度。
- `reshape()` 在步幅兼容时返回视图，否则创建副本。调用者不应依赖它一定共享或一定复制。
- `view(*shape)` 必须满足形状与步幅兼容条件，成功时与原张量共享数据；转置后的非连续张量常不能直接 `view()`。
- `contiguous()` 在输入已经连续时返回自身，否则复制为连续布局；不确定能否使用 `view()` 时优先使用 `reshape()`，或显式 `contiguous().view(...)`。
```python
import torch

x = torch.arange(18).reshape(3, 6)
print(x.reshape(3, 2, -1).shape)  # torch.Size([3, 2, 3])
print(x.view(2, -1).shape)        # torch.Size([2, 9])
transposed = x.T
print(transposed.is_contiguous())  # False
print(transposed.contiguous().view(2, 9).shape)  # torch.Size([2, 9])
```
### 8.2 `squeeze()` 与 `unsqueeze()`
- `unsqueeze(dim)` 在指定位置插入大小为 1 的维度。
- `squeeze()` 删除所有大小为 1 的维度；`squeeze(dim)` 只在指定维度大小为 1 时删除该维度。
- 不指定 `dim` 可能意外删除批次维度（Batch Dimension），模型代码中通常应明确指定。
```python
import torch

x = torch.tensor([1, 2, 3, 4, 5])
print(x.unsqueeze(0).shape)   # torch.Size([1, 5])
print(x.unsqueeze(1).shape)   # torch.Size([5, 1])
print(x.unsqueeze(-1).shape)  # torch.Size([5, 1])
print(x.unsqueeze(-1).squeeze(-1).shape)  # torch.Size([5])
```
### 8.3 转置与维度重排（Transpose and Permutation）
- `transpose(dim0, dim1)` 交换两个维度；二维张量可用 `.T` 转置。
- `permute(dims)` 按完整维度顺序一次重排多个轴，返回视图。
- 高维张量直接使用 `.T` 会反转全部维度且相关行为曾出现版本警告；表达明确轴语义时优先 `transpose()`、`permute()`、`.mT` 或 `.mH`。
```python
import torch

x = torch.zeros((5, 3, 4, 10))
print(x.transpose(1, 2).shape)       # torch.Size([5, 4, 3, 10])
print(x.permute(0, 3, 1, 2).shape)  # torch.Size([5, 10, 3, 4])
```
## 9. 分割与拼接（Splitting and Joining）
### 9.1 `split()` 与 `chunk()`
- `torch.split(x, split_size_or_sections, dim)` 按每段大小或显式大小列表分割；最后一段可以小于指定大小。
- `torch.chunk(x, chunks, dim)` 尝试分成指定数量的块，但当维度长度过小时，实际返回块数可能少于 `chunks`，不能假设数量永远严格相等。
```python
import torch

x = torch.arange(12).reshape(2, 6)
print([part.shape for part in torch.split(x, 3, dim=1)])
print([part.shape for part in torch.chunk(x, 3, dim=1)])
# 期望输出:
# [torch.Size([2, 3]), torch.Size([2, 3])]
# [torch.Size([2, 2]), torch.Size([2, 2]), torch.Size([2, 2])]
```
### 9.2 `cat()`、`concat()` 与 `stack()`
- `torch.cat()` 沿现有维度连接，除拼接轴以外的形状必须一致；`torch.concat()` 是同义接口。
- `torch.stack()` 新建一个维度后堆叠，所有输入张量的形状必须完全相同。
```python
import torch

a = torch.ones((1, 2, 3))
b = torch.zeros((1, 2, 3))
print(torch.cat([a, b], dim=0).shape)   # torch.Size([2, 2, 3])
print(torch.cat([a, b], dim=1).shape)   # torch.Size([1, 4, 3])
print(torch.cat([a, b], dim=2).shape)   # torch.Size([1, 2, 6])
print(torch.stack([a, b], dim=0).shape) # torch.Size([2, 1, 2, 3])
print(torch.stack([a, b], dim=1).shape) # torch.Size([1, 2, 2, 3])
print(torch.stack([a, b], dim=2).shape) # torch.Size([1, 2, 2, 3])
```
## 10. 常见错误与排查（Common Errors and Troubleshooting）

|现象（Symptom）|原因（Cause）|处理（Fix）|
|---|---|---|
|`Expected all tensors to be on the same device`|参与运算的张量位于不同设备|统一 `.to(device)`，模型与输入都要迁移|
|矩阵乘法形状错误|左张量末维与右张量倒数第二维不匹配|打印 `shape`，先明确批次维与矩阵维|
|`view` 兼容性错误|张量的步幅不满足视图要求|使用 `reshape()` 或 `contiguous().view()`|
|直接 `.numpy()` 报错|张量需要梯度或不在 CPU|使用 `tensor.detach().cpu().numpy()`|
|广播结果形状意外|从末维比较时误把大小为 1 的维度扩展|在运算前写出各轴含义并检查 `shape`|
|原地操作导致梯度报错|修改了自动微分保存的中间值|改用非原地操作，或仅在明确的 `no_grad` 更新区执行|
|NumPy 共享数据意外变化|`from_numpy()` 或 `.numpy()` 共享内存|需要隔离时显式 `.copy()` 或 `.clone()`|

## 11. 关联笔记（Related Notes）
- [[02-PyTorch 自动微分与神经网络组件（PyTorch Autograd and Neural Network Components）]]
- [[03-PyTorch 线性回归实战（PyTorch Linear Regression）]]
## 参考资料（References）
- [PyTorch 张量（Tensor）官方文档](https://docs.pytorch.org/docs/stable/tensors.html)
- [PyTorch 张量视图（Tensor Views）官方文档](https://docs.pytorch.org/docs/stable/tensor_view.html)
- [`torch.tensor` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.tensor.html)
- [`torch.from_numpy` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.from_numpy.html)
