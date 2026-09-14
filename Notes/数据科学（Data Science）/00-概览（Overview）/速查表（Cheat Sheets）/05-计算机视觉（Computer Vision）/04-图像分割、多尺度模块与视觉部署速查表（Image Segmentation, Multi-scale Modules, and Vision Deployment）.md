---
title: "图像分割、多尺度模块与视觉部署速查表（Image Segmentation, Multi-scale Modules, and Vision Deployment Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - computer-vision/segmentation
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "PyTorch/torchvision 配套稳定版；ONNX Runtime 当前稳定版"
---
# 图像分割、多尺度模块与视觉部署速查表（Image Segmentation, Multi-scale Modules, and Vision Deployment Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
语义分割每像素分类，实例分割还区分同类个体，全景分割合并 thing 与 stuff。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 分割模型与输出（Segmentation Models and Outputs）
编码器提取语义，解码器恢复空间细节；跳连融合高低层。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|FCN|`fcn_resnet50(weights='DEFAULT')`|输出字典含 `out` logits|
|DeepLabV3|`deeplabv3_resnet50(weights='DEFAULT')`|空洞卷积扩大感受野|
|LRASPP|`lraspp_mobilenet_v3_large(...)`|轻量语义分割|
|U-Net|`编码器-解码器 + 同尺度跳连`|返回像素 logits|
|Mask R-CNN|`maskrcnn_resnet50_fpn(...)`|返回框、标签、分数和 masks|
|二分类掩码|`sigmoid(logits)>threshold`|返回布尔掩码|
|多分类掩码|`logits.argmax(dim=1)`|返回 `(N,H,W)` 类别索引|
|尺寸恢复|`F.interpolate(logits,size=(H,W),mode='bilinear')`|返回缩放 logits|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
import torch.nn.functional as F
logits=torch.randn(2,3,8,8)
up=F.interpolate(logits,size=(16,16),mode="bilinear",align_corners=False)
mask=up.argmax(1)
print(tuple(up.shape),tuple(mask.shape))
# 期望输出:
# (2, 3, 16, 16) (2, 16, 16)
```
## 多尺度与上下文（Multi-scale Context）
多尺度模块同时看局部细节和大范围语义。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|空洞卷积|`nn.Conv2d(...,dilation=d,padding=d)`|扩大感受野且保持尺寸|
|ASPP|`多膨胀率卷积分支 + 池化分支`|返回拼接融合特征|
|金字塔池化|`不同网格自适应池化后上采样`|返回多尺度上下文|
|FPN|`自顶向下 + 横向连接`|返回多分辨率特征字典|
|跳跃连接|`decoder = upsample + encoder_feature`|保留边界细节|
|转置卷积|`nn.ConvTranspose2d(...)`|可学习上采样，可能有棋盘伪影|
|像素重排|`nn.PixelShuffle(upscale_factor)`|通道重排为空间分辨率|
|特征拼接|`torch.cat([high,low],dim=1)`|通道数相加|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torch import nn
x=torch.randn(1,8,16,16)
y=nn.Conv2d(8,8,3,padding=2,dilation=2)(x)
print(tuple(y.shape))
# 期望输出:
# (1, 8, 16, 16)
```
## 损失、指标与部署（Losses, Metrics, and Deployment）
类别极不平衡时组合区域重叠损失与像素分类损失。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|像素交叉熵|`CrossEntropyLoss(ignore_index=255)`|接 `(N,C,H,W)` 与 `(N,H,W)`|
|BCE|`BCEWithLogitsLoss(pos_weight=...)`|二类或多标签像素损失|
|Dice|`dice_score(pred,target,eps)`|返回重叠分数|
|IoU/Jaccard|`intersection/union`|返回类级或平均 IoU|
|混淆矩阵|`按像素 bincount 编码`|返回 `C×C` 计数|
|滑窗推理|`重叠 tile 推理并加权融合`|返回大图 logits|
|测试时增强|`翻转/尺度预测逆变换后平均`|返回集成 logits|
|ONNX Runtime|`session.run(outputs,inputs)`|返回 NumPy 输出列表|
|半精度|`model.half(); input.half()`|降低部分设备内存与延迟|
|量化|`静态/动态/权重量化`|返回低精度模型，需校准精度|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
pred=torch.tensor([[1,1,0,0]],dtype=torch.bool)
target=torch.tensor([[1,0,1,0]],dtype=torch.bool)
i=(pred&target).sum(); u=(pred|target).sum()
print(i.item(),u.item(),round((i/u).item(),3))
# 期望输出:
# 1 3 0.333
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
- [[04-GoogLeNet 与 Inception 多尺度融合（GoogLeNet and Inception Multi-scale Fusion）]]
- [[01-目标检测关联视觉模块：FCN、实例分割、RoIAlign 与 FPN（Related Vision Modules）]]
## 官方参考（Official References）
- [PyTorch 文档](https://docs.pytorch.org/docs/stable/)
