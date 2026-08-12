---
title: "Pillow 与 Torchvision 图像变换（Pillow and Torchvision Image Transforms）"
tags:
  - data-science/cv/image-libraries
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# Pillow 与 Torchvision 图像变换（Pillow and Torchvision Image Transforms）
## Pillow (PIL) 库与 torchvision 图像增强核心笔记

在深度学习（尤其是 PyTorch 生态）中，**Pillow** 是最常用的图像载入与基础处理库，而 **torchvision.transforms** 则是将数据送入神经网络前进行“图像增强”（Data Augmentation）的绝对主力。两者相辅相成，构成了深度学习视觉任务的数据前处理基石。

### 一、 Pillow (PIL) 库基础与核心 API

Pillow 是 Python 中最经典、最轻量化的图像处理库。与 OpenCV 的 `numpy.ndarray` 存储格式不同，Pillow 读取图像后会生成一个专有的 `PIL.Image.Image` 对象。

#### 1. 基础读取、保存与通道转换

```Python
from PIL import Image

# 1. 读取与展示
img = Image.open("cat.jpg")  # 此时不占用过多内存，属于懒加载
img.show()                  # 调用系统默认看图软件打开

# 2. 基础属性
width, height = img.size     # 注意：PIL 的 size 顺序是 (W, H)，与 OpenCV 的 (H, W) 相反！
mode = img.mode             # 'RGB', 'RGBA', 'L' (灰度图) 等

# 3. 保存与格式转换
img.save("cat_compressed.png", format="PNG")
gray_img = img.convert("L")  # 转换为单通道灰度图
```

#### 2. 图像几何变换操作

|**API**|**代码示例**|**功能描述**|
|---|---|---|
|**裁剪**|`img.crop((left, upper, right, lower))`|传入 4 元组，裁剪指定区域|
|**缩放**|`img.resize((new_w, new_h), resample=Image.BILINEAR)`|缩放图像，可指定插值算法|
|**旋转**|`img.rotate(45, expand=True)`|逆时针旋转度数，`expand=True` 保证不剪切图像|
|**翻转/转置**|`img.transpose(Image.FLIP_LEFT_RIGHT)`|镜像翻转、旋转 90/180/270 度|

#### 3. `ImageEnhance` 与 `ImageFilter` 模块

Pillow 内置了两个非常强大的图像增强与滤波子模块。

##### 🎨 ImageEnhance (图像亮度、对比度、色彩平衡与锐度调整)

使用时需要先实例化一个对应的增强器，再传入参数因子 $factor$（$1.0$ 代表原图，$< 1.0$ 代表减弱，$> 1.0$ 代表增强）。

```Python
from PIL import ImageEnhance

# 1. 亮度调整 (Brightness)
enh_bri = ImageEnhance.Brightness(img)
img_bright = enh_bri.enhance(1.5)  # 亮度提升 50%

# 2. 对比度调整 (Contrast)
enh_con = ImageEnhance.Contrast(img)
img_contrast = enh_con.enhance(0.8)  # 对比度降低 20%

# 3. 色彩饱和度调整 (Color)
enh_col = ImageEnhance.Color(img)
img_color = enh_col.enhance(2.0)  # 双倍饱和度

# 4. 锐度调整 (Sharpness)
enh_sha = ImageEnhance.Sharpness(img)
img_sharp = enh_sha.enhance(3.0)  # 图像锐化
```

##### 🔍 ImageFilter (经典图像滤波)

```Python
from PIL import ImageFilter

blur_img = img.filter(ImageFilter.BLUR)          # 模糊滤波
edge_img = img.filter(ImageFilter.FIND_EDGES)    # 边缘检测
```

### 二、 torchvision.transforms 图像增强 API

`torchvision.transforms` 是 PyTorch 专为计算机视觉设计的图像变换工具箱，通常写在数据读取管道（Dataset）中，用于**在线数据增强**，以防止模型过拟合。

#### 1. 基础通道与归一化转换（送入网络前的必备操作）

在将 PIL 图像输入到 PyTorch 神经网络前，必须进行转换与归一化：

- **`transforms.ToTensor()`**：
    - **作用**：将 `PIL Image` 或 `numpy.ndarray` (形状为 $H \times W \times C$，取值 $[0, 255]$) 转换为 `torch.FloatTensor` (形状为 $C \times H \times W$，取值自动缩放到 $[0.0, 1.0]$)。
- **`transforms.Normalize(mean, std)`**：
    - **数学原理**：对每个通道进行标准化：

        $$output[channel] = \frac{input[channel] - mean[channel]}{std[channel]}$$

    - **注意**：输入必须是 `Tensor`（即通常放在 `ToTensor()` 后面）。常用的 ImageNet 均值和标准差为：

        ```python
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ```

#### 2. 常用数据增强 API 归类

`torchvision.transforms` 的 API 非常丰富，主要可以分为以下三大类：

##### 📐 几何变换 (Geometric)

用于改变图像的尺寸、角度、比例，帮助模型学习空间不变量。

- **`Resize(size)`**：缩放图像。`size` 可以是单个整数（缩放短边）或 `(H, W)` 序列。
- **`CenterCrop(size)`**：在图像中心裁剪出大小为 `size` 的区域。
- **`RandomCrop(size, padding=None)`**：在随机位置裁剪。
- **`RandomResizedCrop(size, scale=(0.08, 1.0), ratio=(0.75, 1.33))`**：**【极其常用】** 先随机裁剪出原图的一部分，再缩放到目标 `size`。常用于训练 ImageNet 分类模型。
- **`RandomHorizontalFlip(p=0.5)`**：以概率 $p$ 水平翻转图像。
- **`RandomVerticalFlip(p=0.5)`**：以概率 $p$ 垂直翻转图像。
- **`RandomRotation(degrees)`**：随机旋转指定的角度范围，如 `degrees=(-30, 30)`。
- **`RandomAffine(degrees, translate=None, scale=None, shear=None)`**：随机进行仿射变换（包含旋转、平移、缩放、错切）。

##### 🎨 色彩与像素变换 (Color & Pixel)

用于模拟不同的光照条件、相机曝光及噪声干扰。

- **`ColorJitter(brightness=0, contrast=0, saturation=0, hue=0)`**：**【经典】** 随机调整亮度、对比度、饱和度和色调。

    ```python
    # 四个参数可分别传入标量（如 0.2，表示在 [0.8, 1.2] 范围内随机变化）
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1)
    ```

- **`Grayscale(num_output_channels=1)`**：将图像转换为灰度图。
- **`RandomGrayscale(p=0.1)`**：以概率 $p$ 将图像随机转换为灰度图（保持 3 通道输出）。
- **`GaussianBlur(kernel_size, sigma=(0.1, 2.0))`**：对图像进行高斯模糊。
- **`RandomErasing(p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3))`**：**【针对 Tensor】** 随机用随机值或黑色擦除图像中的一个矩形区域。可以极大地增强模型对遮挡（Occlusion）的鲁棒性。

##### 🧠 组合容器 (Composition & Logic)

用于将多个数据增强步骤打包在一起执行。

- **`Compose(transforms_list)`**：顺序执行一系列转换。

    ```python
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(0.2, 0.2, 0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    ```

- **`RandomApply(transforms_list, p=0.5)`**：以概率 $p$ 决定是否执行这一组变换。
- **`RandomChoice(transforms_list)`**：从给定的变换列表中**随机挑选一个**执行。

#### 3. 🚀 进阶必知：torchvision.transforms v2 升级版

如果你正在使用较新版本的 PyTorch，官方强烈推荐使用 **`torchvision.transforms.v2`**。

> **💡 传统 v1 与 v2 的核心区别**：
>
> - **v1 版本**：只支持对图像（`PIL` 或 `Tensor`）进行变换。如果你做的是目标检测或语义分割，图像被随机裁剪/旋转了，标注的**边界框（Bounding Boxes）**和**分割掩码（Segmentation Masks）**不会跟着一起变换。
>
> - **v2 版本**：全面支持 **“多模态联合变换”**！你只需要将图像、边界框和掩码打包传入，v2 会自动同步应用相同的几何变换（如翻转、旋转、裁剪），彻底告别手动编写复杂对齐代码的痛苦。
>

### 三、 核心总结：OpenCV vs Pillow vs torchvision

为了避免在开发中将三者的 API 与存储格式混淆，以下为您梳理了这三者的核心对比表：

|**特征维度**|**OpenCV (cv2)**|**Pillow (PIL)**|**torchvision (transforms)**|
|---|---|---|---|
|**底层数据类型**|`numpy.ndarray`|`PIL.Image.Image` 对象|`PIL` 对象 或 PyTorch `Tensor`|
|**彩色图像通道顺序**|**BGR**|**RGB**|**RGB**|
|**图像维度顺序**|$H \times W \times C$|宽和高表示为 `(W, H)`|$C \times H \times W$ (转为 Tensor 后)|
|**色彩数值范围**|$[0, 255]$ (通常为 `uint8`)|$[0, 255]$|$[0.0, 1.0]$ (转为 Tensor 后)|
|**核心应用场景**|传统图像处理、特征提取、相机标定、视频读取。|轻量图像读写、格式转换、简单像素及增强处理。|深度学习模型训练阶段的**在线数据增强管道**。|
