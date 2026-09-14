---
title: "CNN、经典骨干与图像分类速查表（CNN, Classic Backbones, and Image Classification Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - computer-vision/classification
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "PyTorch/torchvision 配套稳定版"
---
# CNN、经典骨干与图像分类速查表（CNN, Classic Backbones, and Image Classification Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
图像分类输出通常 `(N,C)`；迁移学习时输入归一化必须匹配预训练权重元数据。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 卷积模块与形状（Convolution Modules and Shapes）
卷积核共享权重提取局部模式；大白话：同一小滤镜滑过整张图寻找相同特征。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|二维卷积|`nn.Conv2d(Cin,Cout,kernel_size,stride=1,padding=0)`|返回 `(N,Cout,Hout,Wout)`|
|深度卷积|`nn.Conv2d(C,C,k,groups=C)`|每通道独立卷积|
|池化|`nn.MaxPool2d(kernel_size,stride=None)`|返回下采样 Tensor|
|自适应池化|`nn.AdaptiveAvgPool2d((1,1))`|返回固定空间形状|
|批归一|`nn.BatchNorm2d(C)`|返回同形状 Tensor并维护运行统计|
|Dropout2d|`nn.Dropout2d(p=.5)`|训练时随机置零通道|
|展平|`torch.flatten(x,1)`|保留批次轴并返回二维 Tensor|
|感受野|`由 kernel/stride/dilation 层层累积`|决定输出位置可见输入范围|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torch import nn
x=torch.randn(2,3,32,32)
y=nn.Conv2d(3,16,3,padding=1)(x)
z=nn.AdaptiveAvgPool2d(1)(y)
print(tuple(y.shape),tuple(z.shape))
# 期望输出:
# (2, 16, 32, 32) (2, 16, 1, 1)
```
## 经典骨干与迁移学习（Backbones and Transfer Learning）
选型考虑精度、参数量、延迟、显存与部署算子支持。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|LeNet/AlexNet|`经典浅层/早期深 CNN`|教学和历史基线|
|VGG|`重复 3x3 卷积`|结构简单但参数和计算大|
|ResNet|`resnet18(weights='DEFAULT')`|残差连接改善深层优化|
|DenseNet|`densenet121(weights='DEFAULT')`|密集特征复用|
|MobileNetV3|`mobilenet_v3_small(weights='DEFAULT')`|移动端轻量骨干|
|EfficientNet|`efficientnet_b0(weights='DEFAULT')`|复合缩放网络|
|ConvNeXt|`convnext_tiny(weights='DEFAULT')`|现代卷积骨干|
|替换分类头|`model.fc=nn.Linear(in_features,num_classes)`|原地替换 ResNet 头|
|冻结骨干|`for p in backbone.parameters(): p.requires_grad=False`|停止骨干梯度|
|权重变换|`weights.transforms()`|返回匹配预训练权重的预处理|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
from torchvision.models import resnet18
m=resnet18(weights=None)
print(m.fc.in_features, m.fc.out_features)
# 期望输出:
# 512 1000
```
## 训练、评估与解释（Training, Evaluation, and Explainability）
分类准确率需结合类别分布、Top-k、混淆矩阵和校准。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|交叉熵|`nn.CrossEntropyLoss()`|接 `(N,C)` logits 和 `(N,)` 标签|
|预测类别|`logits.argmax(1)`|返回 `(N,)` 索引|
|Top-k|`logits.topk(k,dim=1)`|返回值与类别索引|
|冻结 BN|`model.eval()`|停止 BatchNorm 运行统计更新|
|混合精度|`torch.autocast('cuda')`|返回自动精度上下文|
|标签平滑|`CrossEntropyLoss(label_smoothing=.1)`|返回平滑损失|
|Mixup/CutMix|`torchvision.transforms.v2`|返回混合图像和软标签|
|Grad-CAM|`目标梯度加权最后卷积特征`|返回类别关注热图|
|测试时增强|`对多个确定性变换预测取平均`|返回集成概率|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
logits=torch.tensor([[1.,4.,2.]])
values,idx=logits.softmax(1).topk(2,1)
print(idx.tolist(),round(values.sum().item(),4))
# 期望输出:
# [[1, 2]] 0.9572
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
- [[01-CIFAR-10 图像分类实践（CIFAR-10 Image Classification Practice）]]
- [[05-ResNet 残差学习与快捷连接（ResNet Residual Learning and Shortcut Connections）]]
## 官方参考（Official References）
- [PyTorch 文档](https://docs.pytorch.org/docs/stable/)
