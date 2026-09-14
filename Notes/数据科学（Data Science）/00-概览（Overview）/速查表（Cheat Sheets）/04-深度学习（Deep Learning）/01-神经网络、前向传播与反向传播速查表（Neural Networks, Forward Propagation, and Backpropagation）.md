---
title: "神经网络、前向传播与反向传播速查表（Neural Networks, Forward Propagation, and Backpropagation Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - deep-learning/fundamentals
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "PyTorch 2.3–2.14；数学原理与框架无关"
---
# 神经网络、前向传播与反向传播速查表（Neural Networks, Forward Propagation, and Backpropagation Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
输入通常按 `(batch, features)`；先理解计算图、链式法则与梯度累积，再使用自动微分。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 2. TensorFlow 与 Keras 包（TensorFlow and Keras Packages）
### 2.1 TensorFlow（TensorFlow）
- **安装包（Distribution）**：`tensorflow`。
- **导入模块（Import Module）**：`tensorflow`，惯例别名为 `tf`。
- **安装命令（Installation）**：`python -m pip install -U tensorflow`；GPU 支持方式随平台变化，安装前核对 TensorFlow 官方平台矩阵。
- **用途（Purpose）**：张量运算、自动微分、数据流水线、模型训练和部署。
- **正式笔记（Detailed Note）**：[[02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）]] 中的 TensorFlow/Keras 对照。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|张量|`tf.constant(data, dtype=...)`|返回不可变 Tensor|
|变量|`tf.Variable(value)`|返回可原地赋值的状态变量|
|梯度带|`with tf.GradientTape() as tape:`|记录被监视操作以便求梯度|
|求梯度|`tape.gradient(loss, variables)`|返回梯度列表或 `None`|
|数据集|`tf.data.Dataset.from_tensor_slices(data)`|返回惰性数据集|

```python
import tensorflow as tf

x = tf.Variable(3.0)
with tf.GradientTape() as tape:
    y = x ** 2
print(tape.gradient(y, x).numpy())  # 输出: 6.0
```
### 2.2 Keras（Keras）
- **安装包（Distribution）**：独立多后端使用 `keras`；TensorFlow 集成通常随 `tensorflow` 提供 `tf.keras`。
- **导入模块（Import Module）**：`keras` 或 `tensorflow.keras`，同一项目避免混用来源不一致的对象。
- **安装命令（Installation）**：`python -m pip install -U keras`，或直接安装匹配的 `tensorflow`。
- **用途（Purpose）**：声明层、模型、损失、指标、优化器与高层训练循环。
- **正式笔记（Detailed Note）**：[[03-Seq2Seq 与注意力机制（Seq2Seq and Attention）]] 中的 Keras 实现对照。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|顺序模型|`keras.Sequential(layers)`|返回按顺序连接的模型|
|编译|`model.compile(optimizer=..., loss=..., metrics=...)`|原地配置训练步骤|
|训练|`model.fit(x, y, epochs=..., validation_data=...)`|更新权重并返回 History|
|评估|`model.evaluate(x, y, return_dict=True)`|返回损失与指标|
|预测|`model.predict(x)`|返回 NumPy 预测数组|

```python
import keras

model = keras.Sequential([keras.layers.Input((2,)), keras.layers.Dense(1)])
print(model.output_shape)  # 输出: (None, 1)
```
- **后端边界（Backend Boundary）**：独立 Keras 3 可以选择 TensorFlow、JAX 或 PyTorch 后端；保存格式、算子可用性和设备行为必须按实际后端验证。
## 张量与线性层（Tensors and Linear Layers）
线性层执行 `Y=XWᵀ+b`；大白话：每个输出都是输入特征的加权和再加偏置。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建张量|`torch.tensor(data, dtype=torch.float32)`|返回 Tensor|
|随机张量|`torch.randn(*shape, generator=g)`|返回正态随机 Tensor|
|线性层|`nn.Linear(in_features, out_features, bias=True)`|返回可训练模块|
|前向调用|`layer(x)`|返回形状 `(batch, out_features)`|
|参数枚举|`model.parameters()`|返回参数迭代器|
|命名参数|`model.named_parameters()`|返回名称与 Parameter 迭代器|
|参数量|`sum(p.numel() for p in model.parameters())`|返回整数|
|权重初始化|`nn.init.xavier_uniform_(layer.weight)`|原地修改权重并返回 Tensor|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torch import nn
torch.manual_seed(0)
layer=nn.Linear(3,2)
y=layer(torch.ones(4,3))
print(tuple(y.shape), sum(p.numel() for p in layer.parameters()))
# 期望输出:
# (4, 2) 8
```
## 计算图与反向传播（Graph and Backpropagation）
反向传播按链式法则从损失向叶参数传播；大白话：把最终错误逐层分摊到每个参数。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|记录梯度|`torch.tensor(..., requires_grad=True)`|返回需梯度 Tensor|
|反向传播|`loss.backward()`|把梯度累加到叶张量 `.grad`|
|读取梯度|`parameter.grad`|返回 Tensor 或 None|
|清空梯度|`optimizer.zero_grad(set_to_none=True)`|把梯度设 None 或零|
|局部关闭梯度|`with torch.no_grad()`|:块内结果默认不建反向图|
|推理模式|`with torch.inference_mode()`|:更强的推理优化与限制|
|取出数值|`tensor.detach()`|返回与图分离且共享存储的 Tensor|
|向量雅可比积|`torch.autograd.grad(outputs, inputs)`|返回所求梯度元组|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
x=torch.tensor(3.,requires_grad=True)
y=x**2+2*x
y.backward()
print(y.item(), x.grad.item())
# 期望输出:
# 15.0 8.0
```
## 训练闭环与诊断（Training Loop and Diagnostics）
标准闭环是清梯度、前向、损失、反向、更新；梯度默认累积。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|训练模式|`model.train()`|设置训练态并返回 self|
|评估模式|`model.eval()`|设置评估态并返回 self|
|前向|`pred=model(x)`|返回预测 Tensor|
|计算损失|`loss=criterion(pred,y)`|返回标量或逐样本损失|
|反向|`loss.backward()`|累积梯度|
|更新|`optimizer.step()`|按梯度原地更新参数|
|梯度裁剪|`clip_grad_norm_(model.parameters(), max_norm)`|原地裁剪并返回裁剪前总范数|
|异常检测|`torch.autograd.detect_anomaly()`|定位反向 NaN 或错误，速度较慢|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torch import nn
x=torch.tensor([[1.],[2.]]); y=2*x
m=nn.Linear(1,1); opt=torch.optim.SGD(m.parameters(),lr=.1)
opt.zero_grad(); loss=nn.MSELoss()(m(x),y); loss.backward(); opt.step()
print(loss.ndim, all(p.grad is not None for p in m.parameters()))
# 期望输出:
# 0 True
```
## 高频工作模式（Common Workflows）
- **基线（Baseline）**：先用最小可解释模型和极小数据过拟合测试，确认数据、损失和指标链路正确。
- **训练（Training）**：固定随机种子，记录数据版本、超参数、权重、指标与环境。
- **验证（Validation）**：验证集只用于选型与调参，最终测试集只评估一次。
- **推理（Inference）**：冻结随机行为、关闭梯度、统一预处理并验证输出 schema。
- **性能（Performance）**：先测量数据加载、计算、通信与后处理，再针对瓶颈优化。
- **上线（Production）**：增加输入校验、超时、批处理、监控、回滚和隐私保护。
## 常见错误与排查（Common Errors and Troubleshooting）
- **维度错误**：记录每个关键张量的 `shape/dtype/device`，按模块契约逐层核对。
- **训练不稳定**：检查输入归一化、标签范围、损失配对、学习率、梯度范数和 NaN/Inf。
- **指标虚高**：排查数据泄漏、重复样本、错误划分、阈值选择和只看单一平均指标。
- **推理漂移**：确保训练与服务使用同一 tokenizer、类别表、归一化统计和模型版本。
- **资源泄漏**：及时关闭文件、图像、客户端与进程；长任务持续观察 CPU/GPU/内存。
- **版本漂移**：固定主要依赖并以官方迁移说明处理弃用，不静默忽略警告。
## 相关详细笔记（Detailed Notes）
- [[01-人工神经网络与前向传播（Artificial Neural Networks and Forward Propagation）]]
- [[02-神经网络损失函数与输出契约（Neural Network Loss Functions and Output Contracts）]]
- [[03-反向传播与链式法则（Backpropagation and the Chain Rule）]]
- [[04-梯度下降、优化器与学习率调度（Gradient Descent, Optimizers, and Learning-rate Scheduling）]]
- [[03-神经网络激活函数（Neural Network Activation Functions）]]
- [[02-PyTorch 自动微分与神经网络组件（PyTorch Autograd and Neural Network Components）]]
- [[01-神经网络参数初始化与梯度流（Neural Network Initialization and Gradient Flow）]]
- [[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）]]
- [[01-基于 NumPy 的三层 BP 神经网络（Three-layer BP Neural Network with NumPy）]]
## 官方参考（Official References）
- [TensorFlow 安装文档](https://www.tensorflow.org/install)
- [Keras 文档](https://keras.io/)
- [PyTorch 文档](https://docs.pytorch.org/docs/stable/)
- [PyTorch Autograd](https://docs.pytorch.org/docs/stable/autograd)
