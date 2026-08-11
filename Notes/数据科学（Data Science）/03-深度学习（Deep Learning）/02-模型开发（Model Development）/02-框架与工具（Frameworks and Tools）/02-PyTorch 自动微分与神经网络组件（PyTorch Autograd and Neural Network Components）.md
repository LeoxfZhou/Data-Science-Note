---
title: PyTorch 自动微分与神经网络组件（PyTorch Autograd and Neural Network Components）
aliases:
  - PyTorch Autograd and Neural Network Components
  - PyTorch 自动微分
tags:
  - data-science/deep-learning/pytorch
  - data-science/deep-learning/neural-network
status: published
published_at: 2026-08-11
created: 2026-08-11
---
# PyTorch 自动微分与神经网络组件（PyTorch Autograd and Neural Network Components）
## 1. 自动微分概念（Automatic Differentiation Concepts）
### 1.1 梯度、反向传播与链式法则（Gradient, Backpropagation, and Chain Rule）
- 对标量函数 $y=f(\mathbf{x})$，梯度（Gradient）是各输入分量偏导数组成的向量：
$$
\nabla_{\mathbf{x}}y=\left[\frac{\partial y}{\partial x_1},\ldots,\frac{\partial y}{\partial x_n}\right]
$$
- 一维函数在某点的导数可以理解为曲线斜率；多维函数的梯度方向是局部增长最快方向，负梯度方向用于梯度下降（Gradient Descent）。
- 反向传播（Backpropagation）从输出向输入应用链式法则，传播的是损失对各中间量和参数的导数信息。
- PyTorch 的 `torch.autograd` 在前向运算时记录需要求导的操作，并在反向阶段计算向量-雅可比乘积（Vector-Jacobian Product, VJP），而不是显式构造完整雅可比矩阵（Jacobian Matrix）。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/02-框架与工具（Frameworks and Tools）/02-PyTorch 自动微分与神经网络组件（PyTorch Autograd and Neural Network Components）/02-PyTorch 自动微分与神经网络组件（PyTorch Autograd and Neural Network Components）-20260328152706310.png|自动微分计算图]]
### 1.2 计算图（Computation Graph）
- 叶张量（Leaf Tensor）通常是用户直接创建、需要梯度的输入或参数；其 `.grad` 用于累积梯度。
- 非叶张量（Non-leaf Tensor）由运算产生，若计算图被记录，其 `grad_fn` 指向生成它的反向函数。
- `requires_grad=True` 表示后续可微运算应被记录；它不表示张量已存在梯度。
- `.grad` 初始为 `None`，第一次有效 `backward()` 后才得到张量；后续反向传播默认累加，而不是自动覆盖。
```python
import torch

x = torch.tensor(3.0, requires_grad=True)
y = 2 * x**2
print(x.is_leaf)            # True
print(y.is_leaf)            # False
print(y.requires_grad)      # True
print(type(y.grad_fn).__name__)  # 'MulBackward0' 或等价的版本相关名称
y.backward()
print(x.grad.item())        # 12.0，因为 dy/dx = 4x
```
> [!note] `grad_fn` 名称的版本差异（Version-dependent `grad_fn` Name）
> `MmBackward0`、`AddmmBackward0` 等内部类名适合用于判断“计算图存在”，但不是稳定公共 API，不应在业务逻辑中依赖具体字符串。
## 2. 标量与非标量反向传播（Scalar and Non-scalar Backward）
### 2.1 标量输出（Scalar Output）
- 当输出仅含一个元素时，`output.backward()` 可省略 `gradient`，相当于以上游梯度 1 启动反向传播。
- `.sum()` 常把逐元素损失汇总为标量，但它改变了数学目标：得到的是所有输出分量之和对输入的梯度。
```python
import torch

x = torch.tensor(10.0, requires_grad=True)
y = 2 * x**2
y.backward()
print(y.item())       # 200.0
print(x.grad.item())  # 40.0
```
### 2.2 非标量输出与上游梯度（Non-scalar Output and Upstream Gradient）
- PyTorch 并非“不支持向量对向量求导”。当输出包含多个元素时，`backward(gradient=...)` 需要同形状的上游梯度，用于计算 $\mathbf{v}^{\mathsf T}J$。
- 若目标确实是所有输出之和，可调用 `y.sum().backward()`；若要完整雅可比矩阵，可使用 `torch.func.jacrev`、`torch.func.jacfwd` 或逐基向量求 VJP。
```python
import torch

x = torch.tensor([10.0, 20.0], requires_grad=True)
y = 2 * x**2
y.backward(gradient=torch.tensor([1.0, 0.5]))
print(x.grad.tolist())  # [40.0, 40.0]，即 [4*10*1, 4*20*0.5]
```
```python
import torch

x = torch.tensor([10.0, 20.0], requires_grad=True)
y = 2 * x**2
y.sum().backward()
print(x.grad.tolist())  # [40.0, 80.0]
```
### 2.3 梯度累积与清理（Gradient Accumulation and Reset）
- 每次反向传播会把新梯度累加到叶张量 `.grad`，便于多分支或梯度累积训练。
- 手工张量可用 `x.grad.zero_()` 清零；优化器管理的参数优先使用 `optimizer.zero_grad()`。
- 现代 `zero_grad()` 默认常使用 `set_to_none=True`，内存开销更低，但 `None` 与全零张量的语义不同：未收到梯度的参数可能被优化器跳过。
```python
import torch

x = torch.tensor(2.0, requires_grad=True)
(x**2).backward()
print(x.grad.item())  # 4.0
(x**2).backward()
print(x.grad.item())  # 8.0，第二次结果被累加
x.grad.zero_()
print(x.grad.item())  # 0.0
```
## 3. 控制梯度记录（Controlling Gradient Recording）
### 3.1 `torch.no_grad()`（No-grad Context）
- `torch.no_grad()` 临时关闭反向模式自动微分记录，常用于参数更新、评估和无需梯度的计算，可降低内存与计算开销。
- 它不会永久修改现有参数的 `requires_grad`；离开上下文后正常恢复记录。
```python
import torch

w = torch.nn.Parameter(torch.tensor([2.0]))
x = torch.tensor([3.0])
tracked = x * w
with torch.no_grad():
    untracked = x * w
print(tracked.requires_grad)    # True
print(untracked.requires_grad)  # False
```
### 3.2 `detach()`（Detach from Graph）
- `tensor.detach()` 返回与原张量共享存储但脱离当前计算图的新张量，其 `requires_grad` 通常为 `False`。
- 因为共享数据，对 detached 张量的原地修改也可能影响原张量；需要独立数据时使用 `tensor.detach().clone()`。
- 转换为 NumPy 的常见安全链路是 `tensor.detach().cpu().numpy()`；返回的 NumPy 数组仍可能与 detached CPU 张量共享内存。
```python
import torch

x = torch.tensor([10.0, 20.0], requires_grad=True)
detached = x.detach()
copied = x.detach().clone()
print(x.requires_grad)         # True
print(detached.requires_grad)  # False
print(copied.requires_grad)    # False
```
### 3.3 `torch.inference_mode()` 与模式切换（Inference Mode and Model Mode）
- `torch.inference_mode()` 比 `no_grad()` 关闭更多自动微分簿记，适合纯推理；其限制更强，不应把在其中创建的张量带回需要自动微分的区域继续使用。
- `model.eval()` 切换 Dropout、BatchNorm 等模块的训练/评估行为，但不关闭梯度；评估通常同时使用 `model.eval()` 与 `torch.no_grad()` 或 `torch.inference_mode()`。
## 4. 参数（Parameter）
### 4.1 `nn.Parameter`
- `nn.Parameter` 是张量子类（Tensor Subclass），默认 `requires_grad=True`。
- 把 `Parameter` 作为 `nn.Module` 属性赋值时，它会被自动注册，出现在 `parameters()`、`named_parameters()` 和 `state_dict()` 中。
- 普通张量不会因为被赋给模块属性就自动成为参数；固定状态应按语义选择普通属性或注册缓冲区（Registered Buffer）。
```python
import torch
from torch import nn

base = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
weight = nn.Parameter(base)
print(base.requires_grad)    # False
print(weight.requires_grad)  # True
print(weight.shape)          # torch.Size([2, 2])
```
### 4.2 手工全连接运算（Manual Fully Connected Operation）
- 输入 `x` 形状为 `(..., in_features)`，权重 `w` 可取 `(in_features, out_features)`，偏置 `b` 为 `(out_features,)`，则 `x @ w + b` 依靠广播加入偏置。
- `nn.Linear` 的权重内部形状是 `(out_features, in_features)`，所以等价表达式为 `x @ linear.weight.T + linear.bias`。
```python
import torch
from torch import nn

w = nn.Parameter(torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
b = nn.Parameter(torch.tensor([0.2, 0.2, 0.2]))
x = torch.tensor([[1.0, 2.0]])
y = x @ w + b
print(y.tolist())  # [[9.199999..., 12.199999..., 15.199999...]]（浮点显示可能略有差异）
print(y.requires_grad)  # True
```
## 5. 神经网络模块（Neural Network Modules）
### 5.1 `nn.Module`
- `nn.Module` 是神经网络组件的基础类。自定义模型应在 `__init__()` 中先调用 `super().__init__()`，再把子模块和参数赋为属性，以便完成注册。
- 调用 `model(x)` 会执行模块的 `__call__` 流程并转入 `forward()`，同时保留钩子（Hook）等框架机制；通常不要直接调用 `model.forward(x)`。
- `.to(device)`、`.train()`、`.eval()`、`.parameters()` 和 `.state_dict()` 依赖注册机制。
```python
import torch
from torch import nn

class TinyNetwork(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        # 注册为子模块后，参数才能被优化器和设备迁移自动发现。
        self.hidden = nn.Linear(2, 3)
        self.output = nn.Linear(3, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.output(torch.relu(self.hidden(x)))

model = TinyNetwork()
print(sum(parameter.numel() for parameter in model.parameters()))  # 13
print(model(torch.ones((2, 2))).shape)  # torch.Size([2, 1])
```
### 5.2 `nn.Linear`
- `nn.Linear(in_features, out_features, bias=True)` 对最后一个维度执行仿射变换（Affine Transformation）：
$$
y=xW^{\mathsf T}+b
$$
- 输入可以有任意前导维度，只要最后一维等于 `in_features`；输出保留前导维度并把最后一维替换为 `out_features`。
- `named_parameters()` 可查看 `weight` 和可选 `bias`；模型与输入必须位于兼容设备和类型。
```python
import torch
from torch import nn

torch.manual_seed(0)
linear = nn.Linear(in_features=2, out_features=3, bias=True)
x = torch.ones((4, 2))
result = linear(x)
equivalent = x @ linear.weight.T + linear.bias
print(result.shape)  # torch.Size([4, 3])
print(torch.allclose(result, equivalent))  # True
print([name for name, _ in linear.named_parameters()])  # ['weight', 'bias']
```
### 5.3 常用激活函数（Common Activation Functions）

|模块（Module）|公式（Formula）|输出范围与要点|
|---|---|---|
|`nn.ReLU()`|$\max(0,x)$|$[0,+\infty)$；负区间梯度为 0|
|`nn.Sigmoid()`|$1/(1+e^{-x})$|$(0,1)$；大绝对值区域可能饱和|
|`nn.Tanh()`|$(e^x-e^{-x})/(e^x+e^{-x})$|$(-1,1)$；以 0 为中心，也可能饱和|

```python
import torch
from torch import nn

x = torch.tensor([[-1.0, 0.0, 1.0]])
print(nn.ReLU()(x).tolist())  # [[0.0, 0.0, 1.0]]
print(nn.Sigmoid()(x).round(decimals=4).tolist())  # [[0.2689, 0.5, 0.7311]]
print(nn.Tanh()(x).round(decimals=4).tolist())     # [[-0.7616, 0.0, 0.7616]]
```
### 5.4 `nn.Sequential` 与模块容器（Sequential and Module Containers）
- `nn.Sequential` 按注册顺序串行调用子模块，适合单输入、单输出的直线型结构。
- 普通 Python `list` 中的层不会自动注册为模块，因此优化器、`.to()` 和 `state_dict()` 可能无法发现它们；需要列表语义时使用 `nn.ModuleList`，需要键值语义时使用 `nn.ModuleDict`。
- `nn.Sequential` 不是普通 Python 集合的替代品；含跳跃连接、多输入或分支结构时，应自定义 `nn.Module.forward()`。
```python
import torch
from torch import nn

network = nn.Sequential(
    nn.Linear(2, 3),
    nn.ReLU(),
    nn.Linear(3, 1),
)
x = torch.ones((2, 2))
print([type(module).__name__ for module in network.children()])
print(network(x).shape)
# 期望输出:
# ['Linear', 'ReLU', 'Linear']
# torch.Size([2, 1])
```
## 6. 交叉熵损失（Cross-entropy Losses）
### 6.1 `nn.CrossEntropyLoss`
- `nn.CrossEntropyLoss` 接收未归一化逻辑值（Unnormalized Logits），通常不应先手工调用 `softmax()`；内部组合了 `log_softmax` 与负对数似然损失（Negative Log-likelihood Loss）。
- 类别索引目标（Class-index Target）应为 `torch.long`，取值通常在 `[0, C)`；输入形状可为 `(C)`、`(N, C)` 或 `(N, C, d1, ..., dK)`。
- 也可传与输入同形状的浮点类别概率目标，但调用者必须保证每个样本的值位于 `[0, 1]` 且和为 1；PyTorch 不一定主动验证这些约束。
- `weight` 为各类别设置一维权重；`ignore_index` 忽略指定类别索引；`label_smoothing` 控制标签平滑（Label Smoothing）。
- `reduction='none'` 保留逐样本或逐位置损失，`'mean'` 返回均值，`'sum'` 返回和；历史参数 `size_average` 和 `reduce` 已弃用。
```python
import torch
from torch import nn

logits = torch.tensor([
    [2.0, 1.0, 0.0],
    [0.0, 1.0, 2.0],
])
target = torch.tensor([0, 2], dtype=torch.long)
per_sample = nn.CrossEntropyLoss(reduction="none")(logits, target)
manual = -torch.log_softmax(logits, dim=1)[torch.arange(2), target]
print(per_sample.shape)  # torch.Size([2])
print(torch.allclose(per_sample, manual))  # True
print(nn.CrossEntropyLoss()(logits, target).item())  # 约 0.4076
```
> [!warning] 不要重复应用 Softmax（Do Not Apply Softmax Twice）
> 把概率而非 logits 传入 `CrossEntropyLoss` 会改变目标函数，并削弱数值稳定性。只有在展示公式或生成预测概率时才单独调用 `softmax()`。
### 6.2 `nn.BCEWithLogitsLoss`
- `nn.BCEWithLogitsLoss` 把 Sigmoid 与二元交叉熵（Binary Cross-entropy, BCE）合并，通过对数求和指数技巧（Log-sum-exp Trick）提高数值稳定性。
- 输入和目标形状必须相同；目标通常为浮点数，可表示二分类或多标签分类（Multi-label Classification）中的每个独立标签，值通常位于 `[0,1]`。
- 它不同于互斥多分类的 `CrossEntropyLoss`：一个多标签样本可以同时拥有多个正类，也可以没有正类。
- `weight` 对损失元素进行缩放；`pos_weight` 调整正例项，需仔细遵守广播规则。增大某类别的正例权重通常偏向提高召回率（Recall），但实际效果取决于阈值与数据分布。
- `reduction='none'` 返回与输入同形状的逐元素损失；默认 `'mean'` 对全部元素取平均。
$$
\ell(x,y)=-\left[y\log\sigma(x)+(1-y)\log(1-\sigma(x))\right]
$$
```python
import torch
from torch import nn

logits = torch.tensor([[0.0, 1.0], [-1.0, 2.0]])
target = torch.tensor([[1.0, 1.0], [0.0, 1.0]])
loss = nn.BCEWithLogitsLoss(reduction="none")(logits, target)
probability = torch.sigmoid(logits)
manual = -(target * torch.log(probability) + (1 - target) * torch.log(1 - probability))
print(loss.shape)  # torch.Size([2, 2])
print(torch.allclose(loss, manual, atol=1e-6))  # True
print(nn.BCEWithLogitsLoss()(logits, target).item())  # 约 0.3616
```
### 6.3 损失函数选择（Choosing a Loss Function）

|任务（Task）|输出（Output）|目标（Target）|常用损失（Typical Loss）|
|---|---|---|---|
|互斥多分类（Single-label Multiclass）|每类一个 logit，形状 `(N,C)`|类别索引 `(N,)` 或合法类别分布|`CrossEntropyLoss`|
|二分类（Binary Classification）|一个 logit 或与目标同形状 logits|浮点 0/1 或软标签|`BCEWithLogitsLoss`|
|多标签分类（Multilabel Classification）|每个独立标签一个 logit|同形状多热向量（Multi-hot Vector）|`BCEWithLogitsLoss`|
|回归（Regression）|连续值|同形状连续目标|`MSELoss`、`L1Loss` 等|

## 7. 优化器与安全参数更新（Optimizer and Safe Parameter Updates）
### 7.1 标准更新顺序（Standard Update Order）
1. `optimizer.zero_grad()`：清除或置空上一轮梯度。
2. `prediction = model(input)`：执行前向传播（Forward Pass）。
3. `loss = loss_fn(prediction, target)`：计算标量损失。
4. `loss.backward()`：反向传播并累积参数梯度。
5. `optimizer.step()`：由优化算法更新参数。
### 7.2 手工梯度下降（Manual Gradient Descent）
- 手工梯度下降使用 `w = w - learning_rate * gradient`；参数更新应放在 `torch.no_grad()` 中，不得通过 `x.data = ...` 绕过自动微分安全检查。

> [!tip] 大白话理解（Plain-language Intuition）
> 自动微分像在每次张量运算旁记录“这个结果由谁算出来”。调用 `backward()` 时，PyTorch 沿记录反向追踪并套用链式法则，把每个叶子参数对损失的影响累积到 `.grad`。`no_grad()` 则是在明确告诉系统：这段操作只是更新参数，不需要再记进下一张计算图。
- 手工更新应放入 `torch.no_grad()`，并保持参数对象身份不变；更新后再清除梯度。
```python
import torch

x = torch.tensor(10.0, requires_grad=True)
learning_rate = 0.01
for _ in range(1000):
    y = x**2 + 20
    y.backward()
    with torch.no_grad():
        # 原地更新叶张量，既保持对象身份，又不把更新步骤加入计算图。
        x -= learning_rate * x.grad
    x.grad = None

print(round(x.item(), 6))  # 接近 0.0
print(round((x**2 + 20).item(), 6))  # 接近 20.0
```
## 8. 常见错误与边界（Common Errors and Boundaries）

|现象（Symptom）|原因（Cause）|处理（Fix）|
|---|---|---|
|非标量 `backward()` 报错|未提供上游梯度|提供同形状 `gradient`，或先明确归约目标|
|梯度比预期大|多次反向传播发生累积|每次优化迭代前 `zero_grad()`|
|`.grad is None`|张量不是叶节点、未参与损失，或梯度被置空|检查 `is_leaf`、`requires_grad` 与计算路径|
|第二次对同一图反向报错|第一次反向后中间缓存已释放|重新前向；仅确有需要时 `retain_graph=True`|
|需要梯度的张量 `.numpy()` 报错|NumPy 不跟踪 autograd|使用 `detach().cpu().numpy()`|
|模型参数未出现在优化器中|层存于普通列表或未注册|使用属性、`Sequential`、`ModuleList` 或 `ModuleDict`|
|分类损失异常|把概率重复传入 CE、目标类型/范围错误|CE 传 logits 与 long 索引；BCE logits 与浮点同形状目标|
|评估结果不稳定|只关闭梯度却未 `eval()`，或只 `eval()` 却仍记录梯度|评估同时设置模块模式和梯度上下文|

## 9. 关联笔记（Related Notes）
- [[01-PyTorch 张量基础（PyTorch Tensor Fundamentals）]]
- [[03-PyTorch 线性回归实战（PyTorch Linear Regression）]]
## 参考资料（References）
- [`torch.Tensor.backward` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.Tensor.backward.html)
- [`torch.nn.Module` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html)
- [`torch.nn.CrossEntropyLoss` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)
- [`torch.nn.BCEWithLogitsLoss` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html)
- [PyTorch 优化循环（Optimization Loop）官方教程](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
