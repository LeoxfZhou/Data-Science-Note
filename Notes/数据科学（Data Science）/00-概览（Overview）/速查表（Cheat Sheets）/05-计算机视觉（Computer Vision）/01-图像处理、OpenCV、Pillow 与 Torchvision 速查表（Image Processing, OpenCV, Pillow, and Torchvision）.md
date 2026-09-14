---
title: "图像处理、OpenCV、Pillow 与 Torchvision 速查表（Image Processing, OpenCV, Pillow, and Torchvision Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - computer-vision/image-processing
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "OpenCV 4.8–5.0；Pillow 10+；torchvision 与 PyTorch 配套版本"
---
# 图像处理、OpenCV、Pillow 与 Torchvision 速查表（Image Processing, OpenCV, Pillow, and Torchvision Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
OpenCV 默认 BGR，Pillow 常用 RGB，Torchvision 张量通常为 `(C,H,W)`；跨库转换必须明确颜色和 dtype。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 2. 包级安装与导入索引（Package Installation and Import Index）
### 2.1 OpenCV（OpenCV）
- **安装包（Distribution）**：桌面版 `opencv-python`；无 GUI 服务器可选 `opencv-python-headless`，两者不要同时安装。
- **导入模块（Import Module）**：`cv2`。
- **安装命令（Installation）**：`python -m pip install -U opencv-python`。
- **用途（Purpose）**：图像/视频读取、颜色转换、几何变换、滤波、特征与传统视觉算法。
- **正式笔记（Detailed Note）**：[[02-OpenCV 图像处理原理（OpenCV Image Processing Principles）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|读取|`cv2.imread(path, cv2.IMREAD_COLOR)`|返回 BGR `ndarray`；失败返回 `None`|
|颜色转换|`cv2.cvtColor(image, cv2.COLOR_BGR2RGB)`|返回新数组|
|缩放|`cv2.resize(image, dsize, interpolation=...)`|返回指定尺寸数组|
|高斯模糊|`cv2.GaussianBlur(image, ksize, sigmaX)`|返回滤波数组|
|写文件|`cv2.imwrite(path, image)`|写文件并返回成功布尔值|

```python
import cv2
import numpy as np

bgr = np.array([[[255, 0, 0]]], dtype=np.uint8)
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
print(rgb.tolist())  # 输出: [[[0, 0, 255]]]
```
### 2.2 Pillow（Python Imaging Library Fork, Pillow）
- **安装包（Distribution）**：`Pillow`。
- **导入模块（Import Module）**：`PIL`。
- **安装命令（Installation）**：`python -m pip install -U Pillow`。
- **用途（Purpose）**：图像文件解码、模式转换、裁剪、缩放、绘制与保存。
- **正式笔记（Detailed Note）**：[[01-Pillow 与 Torchvision 图像变换（Pillow and Torchvision Image Transforms）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|读取|`Image.open(path)`|惰性打开并返回 Image；应使用上下文管理器|
|新建|`Image.new(mode, size, color)`|返回内存图像|
|模式转换|`image.convert('RGB')`|返回新图像|
|缩放|`image.resize(size, resample=...)`|返回新图像|
|裁剪|`image.crop((left, top, right, bottom))`|返回新图像|
|保存|`image.save(path, format=None, **params)`|编码并写文件|

```python
from PIL import Image

image = Image.new("RGB", (2, 1), color=(255, 0, 0))
print(image.mode, image.size, image.getpixel((0, 0)))  # 输出: RGB (2, 1) (255, 0, 0)
```
### 2.3 Torchvision（Torchvision）
- **安装包（Distribution）**：`torchvision`，版本必须与 `torch` 匹配。
- **导入模块（Import Module）**：`torchvision`。
- **安装命令（Installation）**：按 PyTorch 官方安装选择器安装匹配的 `torch torchvision` 组合。
- **用途（Purpose）**：视觉数据集、图像/视频变换、预训练模型和检测算子。
- **正式笔记（Detailed Note）**：[[01-PyTorch 数据集、变换与加载器（PyTorch Datasets, Transforms, and DataLoaders）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|组合变换|`transforms.Compose([...])`|返回顺序变换对象|
|转张量|`transforms.ToTensor()`|把 PIL/数组转为 `[C,H,W]` 浮点张量|
|归一化|`transforms.Normalize(mean, std)`|逐通道返回归一化张量|
|加载模型|`models.resnet18(weights=...)`|返回模型；指定权重时可能下载|
|读取图像|`torchvision.io.read_image(path)`|返回 `uint8 [C,H,W]` 张量|

```python
import torch
from torchvision.transforms import Normalize

x = torch.tensor([[[0.5]], [[0.25]], [[0.0]]])
y = Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])(x)
print(y.flatten().tolist())  # 输出: [0.0, -0.5, -1.0]
```
### 2.4 Albumentations 数据增强（Albumentations Augmentation）
- **安装包（Distribution）**：`albumentations`。
- **导入模块（Import Module）**：`albumentations`，惯例别名为 `A`。
- **安装命令（Installation）**：`python -m pip install -U albumentations`。
- **用途（Purpose）**：对图像、边界框、关键点和分割掩码执行同步增强。
- **正式笔记（Detailed Note）**：[[01-Pillow 与 Torchvision 图像变换（Pillow and Torchvision Image Transforms）]] 中的数据增强部分。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|组合增强|`A.Compose(transforms, bbox_params=..., keypoint_params=...)`|返回可调用流水线|
|水平翻转|`A.HorizontalFlip(p=0.5)`|按概率返回翻转后的字段|
|缩放裁剪|`A.RandomResizedCrop(size=(h,w), scale=...)`|返回统一尺寸结果|
|张量转换|`ToTensorV2()`|把 NumPy 图像转为 PyTorch 张量|

```python
import albumentations as A
import numpy as np

image = np.arange(6, dtype=np.uint8).reshape(2, 3)
result = A.HorizontalFlip(p=1.0)(image=image)["image"]
print(result.tolist())  # 输出: [[2, 1, 0], [5, 4, 3]]
```
- **边界（Boundary）**：检测和分割任务必须显式传入并校验 `bbox_params`、`label_fields`、`keypoint_params` 与 mask；否则标注可能不随图像同步变换。
## 读取、颜色与几何（I/O, Color, and Geometry）
图片读取失败可能返回 `None` 或抛异常，应立即验证。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|OpenCV 读取|`cv2.imread(path,cv2.IMREAD_COLOR)`|返回 BGR ndarray 或 None|
|OpenCV 写入|`cv2.imwrite(path,image)`|写文件并返回成功布尔值|
|Pillow 读取|`Image.open(path)`|返回惰性 Image，需关闭或上下文|
|颜色转换|`cv2.cvtColor(img,cv2.COLOR_BGR2RGB)`|返回新 ndarray|
|缩放|`cv2.resize(img,(width,height),interpolation=...)`|返回新图像|
|裁剪|`img[y1:y2,x1:x2]`|返回视图|
|翻转|`cv2.flip(img,flipCode)`|返回翻转图像|
|仿射|`cv2.warpAffine(img,M,dsize)`|返回变换图像|
|透视|`cv2.warpPerspective(img,H,dsize)`|返回变换图像|
|边界填充|`cv2.copyMakeBorder(img,top,bottom,left,right,type)`|返回扩展图像|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import cv2
import numpy as np
img=np.zeros((10,20,3),dtype=np.uint8)
small=cv2.resize(img,(5,4))
print(img.shape,small.shape)
# 期望输出:
# (10, 20, 3) (4, 5, 3)
```
## 滤波、形态学与边缘（Filtering, Morphology, and Edges）
核大小、边界模式和阈值决定效果。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|高斯模糊|`cv2.GaussianBlur(img,(5,5),sigmaX=0)`|返回平滑图|
|中值滤波|`cv2.medianBlur(img,ksize=5)`|返回去脉冲噪声图|
|双边滤波|`cv2.bilateralFilter(img,d,sigmaColor,sigmaSpace)`|保边平滑|
|阈值|`cv2.threshold(gray,thresh,maxval,type)`|返回阈值和二值图|
|自适应阈值|`cv2.adaptiveThreshold(...)`|返回局部二值图|
|Canny|`cv2.Canny(gray,t1,t2)`|返回边缘二值图|
|腐蚀|`cv2.erode(mask,kernel,iterations=1)`|返回收缩前景|
|膨胀|`cv2.dilate(mask,kernel,iterations=1)`|返回扩张前景|
|形态学|`cv2.morphologyEx(mask,op,kernel)`|返回开闭等结果|
|轮廓|`cv2.findContours(mask,mode,method)`|返回轮廓列表与层级|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import cv2
import numpy as np
gray=np.array([[0,0,255],[0,255,255],[0,0,0]],dtype=np.uint8)
_,mask=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
print(int((mask>0).sum()))
# 期望输出:
# 3
```
## Torchvision 变换与批处理（Torchvision Transforms）
训练增强带随机性；验证/推理只做确定性 resize、crop、normalize。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|组合|`transforms.Compose([...])`|返回顺序变换|
|张量化|`transforms.ToTensor()`|PIL/ndarray 转 float `(C,H,W)` 并常缩放到 0–1|
|缩放|`transforms.Resize(size)`|返回缩放图|
|中心裁剪|`transforms.CenterCrop(size)`|返回确定性裁剪|
|随机裁剪|`transforms.RandomResizedCrop(size)`|返回随机增强图|
|随机翻转|`transforms.RandomHorizontalFlip(p=.5)`|按概率翻转|
|颜色扰动|`transforms.ColorJitter(...)`|返回随机颜色变换|
|归一化|`transforms.Normalize(mean,std)`|逐通道变换 Tensor|
|批网格|`torchvision.utils.make_grid(batch,nrow=8)`|返回网格 Tensor|
|保存图|`torchvision.utils.save_image(tensor,path)`|写文件|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torchvision.transforms import Normalize
x=torch.ones(3,2,2)
y=Normalize([.5]*3,[.5]*3)(x)
print(tuple(y.shape),y.unique().tolist())
# 期望输出:
# (3, 2, 2) [1.0]
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
- [[01-OpenCV Python 工具箱（OpenCV Python Toolbox）]]
- [[02-OpenCV 图像处理原理（OpenCV Image Processing Principles）]]
- [[01-Pillow 与 Torchvision 图像变换（Pillow and Torchvision Image Transforms）]]
## 官方参考（Official References）
- [OpenCV Python 教程](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Pillow 文档](https://pillow.readthedocs.io/)
- [Torchvision 文档](https://docs.pytorch.org/vision/stable/)
- [Albumentations 文档](https://albumentations.ai/docs/)
- [OpenCV Python 教程](https://docs.opencv.org/5.0/py_tutorials/py_setup/py_intro/py_intro.html)
