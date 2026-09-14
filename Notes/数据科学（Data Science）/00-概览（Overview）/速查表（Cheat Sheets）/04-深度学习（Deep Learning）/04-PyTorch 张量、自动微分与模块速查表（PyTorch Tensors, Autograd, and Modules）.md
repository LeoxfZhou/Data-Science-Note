---
title: "PyTorch 张量、自动微分与模块速查表（PyTorch Tensors, Autograd, and Modules Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - pytorch/core
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "Python 3.11+；PyTorch 2.x；CPU/CUDA/ROCm 构建必须按官方安装矩阵匹配"
---
# PyTorch 张量、自动微分与模块速查表（PyTorch Tensors, Autograd, and Modules Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
导入：`import torch` 与 `from torch import nn`。设备迁移、dtype 转换和形状变化必须显式。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
### PyTorch 包信息（PyTorch Package Metadata）
- **安装包（Distribution）**：`torch`。
- **导入模块（Import Module）**：`torch`。
- **安装命令（Installation）**：CPU、CUDA 与 ROCm 的 wheel 不同，应使用 PyTorch 官方安装选择器生成命令，不盲目复制固定 CUDA 索引。
- **用途（Purpose）**：张量计算、自动微分、神经网络模块、优化器和设备加速。
- **正式笔记（Detailed Note）**：[[01-PyTorch 张量基础（PyTorch Tensor Fundamentals）]]、[[02-PyTorch 自动微分与神经网络组件（PyTorch Autograd and Neural Network Components）]]。

```python
import torch

print(torch.tensor([1, 2]).dtype)  # 输出: torch.int64
print(torch.cuda.is_available())  # 输出依赖当前硬件、驱动和安装构建
```
## 张量创建与变形（Tensor Creation and Reshaping）
多数变形共享存储；需要独立内存时显式 `clone()`。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建|`torch.tensor(data,dtype=None,device=None)`|返回复制数据的 Tensor|
|范围|`torch.arange(start,end,step)`|返回半开区间 Tensor|
|等分|`torch.linspace(start,end,steps)`|返回含端点 Tensor|
|零/一|`torch.zeros(shape) / torch.ones(shape)`|返回新 Tensor|
|同形状|`torch.zeros_like(x)`|返回同 shape/device/dtype Tensor|
|改形状|`x.reshape(*shape)`|返回视图或副本|
|视图|`x.view(*shape)`|要求兼容内存布局|
|转置|`x.transpose(dim0,dim1) / x.permute(*dims)`|返回视图|
|增减轴|`x.unsqueeze(dim) / x.squeeze(dim)`|返回视图|
|展平|`torch.flatten(x,start_dim=0)`|返回视图或副本|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
x=torch.arange(6).reshape(2,3)
print(x.tolist())
print(tuple(x.permute(1,0).shape))
# 期望输出:
# [[0, 1, 2], [3, 4, 5]]
# (3, 2)
```
## 索引、归约与拼接（Indexing, Reduction, and Joining）
PyTorch 索引与 NumPy 类似，但需关注设备和梯度。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|布尔索引|`x[x>0]`|返回一维 Tensor|
|选取|`torch.index_select(x,dim,index)`|返回新 Tensor|
|聚集|`torch.gather(x,dim,index)`|按索引返回 Tensor|
|散射|`x.scatter_(dim,index,src)`|原地写入|
|拼接|`torch.cat(tensors,dim=0)`|沿已有轴返回 Tensor|
|堆叠|`torch.stack(tensors,dim=0)`|沿新轴返回 Tensor|
|求和|`x.sum(dim=None,keepdim=False)`|返回归约 Tensor|
|均值|`x.mean(dim=None)`|返回浮点归约 Tensor|
|最大值|`x.max(dim)`|返回 values 与 indices|
|唯一值|`torch.unique(x,return_counts=True)`|返回唯一值及计数|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
x=torch.tensor([[1.,2.],[3.,4.]])
print(x.sum(dim=0).tolist())
print(torch.cat([x,x],dim=0).shape)
# 期望输出:
# [4.0, 6.0]
# torch.Size([4, 2])
```
## 设备、dtype 与自动微分（Device, Dtype, and Autograd）
参与同一运算的张量通常必须位于同一设备且 dtype 兼容。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|迁移|`x.to(device='cuda',dtype=torch.float16)`|返回迁移后的 Tensor|
|查询设备|`x.device`|返回 device|
|查询类型|`x.dtype`|返回 dtype|
|复制|`x.clone()`|返回保留梯度关系的副本|
|分离|`x.detach()`|返回不追踪当前图的共享存储视图|
|梯度开关|`x.requires_grad_(True)`|原地设置并返回 self|
|反向|`scalar.backward()`|累积叶张量梯度|
|函数梯度|`torch.autograd.grad(y,x,create_graph=False)`|返回梯度元组|
|禁用梯度|`torch.no_grad()`|返回上下文/装饰器|
|清 CUDA 缓存|`torch.cuda.empty_cache()`|释放未占用缓存块，不释放活张量|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
x=torch.tensor([2.],requires_grad=True)
y=(x**3).sum(); (dx,)=torch.autograd.grad(y,x)
print(dx.item(), x.device.type)
# 期望输出:
# 12.0 cpu
```
## 模块、容器与保存（Modules, Containers, and Serialization）
自定义模块在 `__init__` 注册子模块，在 `forward` 定义计算。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|顺序容器|`nn.Sequential(layer1,layer2)`|按顺序返回复合模块|
|模块列表|`nn.ModuleList(modules)`|注册可迭代子模块|
|模块字典|`nn.ModuleDict(mapping)`|按键注册子模块|
|自定义参数|`nn.Parameter(tensor)`|注册可训练参数|
|缓冲区|`self.register_buffer(name,tensor)`|注册随设备/状态移动但不优化的 Tensor|
|状态|`model.state_dict()`|返回参数与持久缓冲映射|
|保存状态|`torch.save(model.state_dict(),path)`|写文件|
|安全加载|`torch.load(path,weights_only=True,map_location='cpu')`|返回权重对象|
|加载状态|`model.load_state_dict(state,strict=True)`|写入模型并返回缺失/多余键信息|
|钩子|`module.register_forward_hook(fn)`|返回可移除句柄|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torch import nn
m=nn.Sequential(nn.Linear(3,4),nn.ReLU(),nn.Linear(4,2))
x=torch.ones(5,3)
print(tuple(m(x).shape), len(m.state_dict()))
# 期望输出:
# (5, 2) 4
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
- [[01-PyTorch 数据集、变换与加载器（PyTorch Datasets, Transforms, and DataLoaders）]]
- [[02-PyTorch 模型工程结构与环境（PyTorch Model Engineering Structure and Environment）]]
- [[04-PyTorch 训练与评估循环（PyTorch Training and Evaluation Loops）]]
- [[05-PyTorch 模型持久化与推理（PyTorch Model Persistence and Inference）]]
- [[01-PyTorch 张量基础（PyTorch Tensor Fundamentals）]]
- [[02-PyTorch 自动微分与神经网络组件（PyTorch Autograd and Neural Network Components）]]
- [[03-PyTorch 线性回归实战（PyTorch Linear Regression）]]
- [[04-PyTorch 全连接网络与手机价格分类实践（PyTorch MLP and Phone-price Classification）]]
- [[02-Transformer PyTorch 实现（Transformer PyTorch Implementation）]]
## 官方参考（Official References）
- [PyTorch 安装选择器](https://pytorch.org/get-started/locally/)
- [PyTorch API 文档](https://docs.pytorch.org/docs/stable/)
- [PyTorch 文档](https://docs.pytorch.org/docs/stable/)
- [PyTorch Autograd](https://docs.pytorch.org/docs/stable/autograd)
