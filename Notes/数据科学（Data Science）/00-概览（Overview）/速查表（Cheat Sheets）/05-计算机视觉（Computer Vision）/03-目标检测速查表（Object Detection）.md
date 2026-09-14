---
title: "目标检测速查表（Object Detection Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - computer-vision/detection
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "torchvision 检测模型配套 PyTorch；Ultralytics 8.x 接口需按官方版核对"
---
# 目标检测速查表（Object Detection Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
检测输入涉及图像、框 `(x1,y1,x2,y2)`、类别和置信度；几何增强必须同步变换标注。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 2. Ultralytics YOLO 包（Ultralytics YOLO Package）
- **安装包（Distribution）**：`ultralytics`。
- **导入模块（Import Module）**：`ultralytics`。
- **安装命令（Installation）**：`python -m pip install -U ultralytics`。
- **用途（Purpose）**：YOLO 模型训练、验证、预测、追踪和导出。
- **正式笔记（Detailed Note）**：[[01-YOLOv8 自定义目标检测项目模板（YOLOv8 Custom Detection Project Template）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|加载模型|`YOLO(model_or_weights)`|读取配置/权重并返回模型；权重名可能触发下载|
|训练|`model.train(data=..., epochs=..., imgsz=...)`|执行训练并写运行目录|
|验证|`model.val(data=..., split='val')`|执行评估并返回指标对象|
|预测|`model.predict(source=..., conf=0.25, save=False)`|返回 Results 列表；`save=True` 写文件|
|追踪|`model.track(source=..., tracker=..., persist=True)`|返回带轨迹 ID 的 Results|
|导出|`model.export(format='onnx', imgsz=640, dynamic=False)`|转换并写出模型文件|

```python
from ultralytics import YOLO

model = YOLO("yolov8n.yaml")  # 只构建网络结构，不下载预训练权重
print(model.task)  # 输出: detect
# train/predict/export 会读取数据、占用设备并可能写文件；结果随模型、输入和版本变化。
```
- **边界（Boundary）**：数据 YAML 的路径、类别数和标签 ID 必须一致；模型配置名与权重名的下载行为不同，自动下载前应确认网络与许可范围。
## 框、IoU 与后处理（Boxes, IoU, and Post-processing）
IoU 衡量交并比；NMS 删除与高分框高度重叠的重复预测。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|框转换|`box_convert(boxes,'xyxy','cxcywh')`|返回转换框 Tensor|
|框面积|`box_area(boxes)`|返回面积 Tensor|
|交并比|`box_iou(boxes1,boxes2)`|返回两两 IoU 矩阵|
|广义 IoU|`generalized_box_iou(boxes1,boxes2)`|返回 GIoU 矩阵|
|裁剪框|`clip_boxes_to_image(boxes,(H,W))`|返回边界内框|
|移除小框|`remove_small_boxes(boxes,min_size)`|返回保留索引|
|NMS|`nms(boxes,scores,iou_threshold)`|返回保留索引|
|批量 NMS|`batched_nms(boxes,scores,labels,threshold)`|按类别分组抑制|
|置信阈值|`scores>=threshold`|返回候选布尔掩码|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torchvision.ops import box_iou,nms
boxes=torch.tensor([[0.,0.,10.,10.],[1.,1.,9.,9.],[20.,20.,30.,30.]])
scores=torch.tensor([.9,.8,.7])
print(nms(boxes,scores,.5).tolist())
print(round(box_iou(boxes[:1],boxes[1:2]).item(),2))
# 期望输出:
# [0, 2]
# 0.64
```
## 检测模型与训练（Detection Models and Training）
两阶段模型精细，单阶段模型常更快；实际表现取决于尺度和部署环境。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|Faster R-CNN|`fasterrcnn_resnet50_fpn(weights='DEFAULT')`|返回检测模型|
|RetinaNet|`retinanet_resnet50_fpn(weights='DEFAULT')`|返回焦点损失单阶段模型|
|FCOS|`fcos_resnet50_fpn(weights='DEFAULT')`|返回无锚框检测器|
|SSD|`ssdlite320_mobilenet_v3_large(...)`|返回轻量检测器|
|YOLOv8|`YOLO('yolov8n.pt')`|返回 Ultralytics 模型|
|训练调用|`model(images,targets)`|训练态返回损失字典|
|推理调用|`model(images)`|评估态返回 boxes/labels/scores 列表|
|替换类别头|`FastRCNNPredictor(in_features,num_classes)`|返回新预测头|
|冻结骨干|`trainable_backbone_layers=n`|控制可训练骨干阶段|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
m=fasterrcnn_resnet50_fpn(weights=None,weights_backbone=None,num_classes=3)
print(m.roi_heads.box_predictor.cls_score.out_features)
# 期望输出:
# 3
```
## 数据、指标与部署（Data, Metrics, and Deployment）
mAP 是多 IoU 阈值和类别的综合指标，不能代替逐类错误分析。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|目标字典|`{'boxes':FloatTensor[N,4],'labels':Int64Tensor[N]}`|返回单图监督结构|
|自定义合批|`collate_fn=lambda batch: tuple(zip(*batch))`|保留不同目标数量|
|COCO mAP|`MeanAveragePrecision(box_format='xyxy')`|累积后返回 map/map_50 等|
|精确率召回|`按置信阈值匹配预测与真值`|返回 PR 曲线|
|小中大目标|`按面积拆分 AP`|返回尺度分层表现|
|导出 ONNX|`torch.onnx.export(...,dynamic_axes=...)`|写模型文件|
|坐标还原|`框除以 resize scale 并补偿 padding`|返回原图坐标|
|批量推理|`同尺寸 padding 后堆叠`|提高吞吐|
|跟踪|`检测框 + 运动/外观匹配`|返回跨帧 track id|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
target={"boxes":torch.tensor([[1.,2.,5.,8.]]),"labels":torch.tensor([1])}
print(tuple(target["boxes"].shape),target["labels"].dtype)
# 期望输出:
# (1, 4) torch.int64
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
- [[01-目标检测任务、范式与系统流程（Object Detection Tasks, Paradigms, and Pipeline）]]
- [[02-目标检测评估指标：IoU、Precision、Recall、AP 与 mAP（Object Detection Metrics）]]
- [[03-候选区域与选择性搜索（Region Proposals and Selective Search）]]
- [[04-锚框、样本匹配与边界框回归（Anchors, Label Assignment, and Box Regression）]]
- [[05-非极大值抑制与 Soft-NMS（Non-Maximum Suppression and Soft-NMS）]]
- [[06-R-CNN 系列两阶段检测器演化（Evolution of Two-stage R-CNN Detectors）]]
- [[07-YOLOv1、YOLOv2 与 YOLOv3 演化（YOLOv1-v3 Evolution）]]
- [[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）]]
- [[09-YOLOv5 架构、训练与部署边界（YOLOv5 Architecture, Training, and Deployment）]]
- [[10-YOLOv8 网络结构、标签分配与损失（YOLOv8 Architecture and Losses）]]
- [[01-目标检测关联视觉模块：FCN、实例分割、RoIAlign 与 FPN（Related Vision Modules）]]
- [[01-YOLOv8 自定义目标检测项目模板（YOLOv8 Custom Detection Project Template）]]
## 官方参考（Official References）
- [Ultralytics Python 使用文档](https://docs.ultralytics.com/usage/python/)
- [PyTorch 文档](https://docs.pytorch.org/docs/stable/)
- [Ultralytics 文档](https://docs.ultralytics.com/)
