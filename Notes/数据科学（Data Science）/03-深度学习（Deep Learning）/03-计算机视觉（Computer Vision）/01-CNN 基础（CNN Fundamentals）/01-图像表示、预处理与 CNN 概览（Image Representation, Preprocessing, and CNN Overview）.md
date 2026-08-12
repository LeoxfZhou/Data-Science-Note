---
title: 图像表示、预处理与 CNN 概览（Image Representation, Preprocessing, and CNN Overview）
tags:
  - data-science/deep-learning/computer-vision/cnn
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# 图像表示、预处理与 CNN 概览（Image Representation, Preprocessing, and CNN Overview）
## 1. 数字图像（Digital Image）的基本表示
数字图像（Digital Image）可以理解为按空间位置排列的数值。每个像素（Pixel）记录一个位置的亮度、颜色索引或多个颜色通道（Color Channel）。图像也可以泛指照片、绘画、地图、手写文字、卫星云图、影视帧、X 光图像以及其他视觉或科学成像结果。
> [!tip] 大白话理解（Plain-language Intuition）
> 计算机不会直接“看见”汽车或猫，只会接收到一张数字表。图像模型的任务，就是从这张数字表里逐层找出边缘、纹理、部件，最后组合成可用于分类或定位的语义。
### 1.1 常见图像类型（Common Image Types）

|图像类型（Image Type）|典型存储|值域（Value Range）|含义与用途|
|---|---|---|---|
|二值图像（Binary Image）|每像素 1 位或逻辑值|`0`、`1`|通常约定 `0` 为黑、`1` 为白；用于文字或线条识别、掩膜（Mask）、形态学操作与轮廓分析|
|灰度图像（Grayscale Image）|常见为无符号 8 位整数（Unsigned 8-bit Integer, `uint8`）|`0`–`255`|通常 `0` 为黑、`255` 为白，中间值表示由暗到亮；二值图像可视为其特例|
|索引图像（Indexed Image）|二维索引矩阵 + 颜色映射表（Color Map）|索引范围取决于颜色表|像素保存的不是最终 RGB，而是颜色表的行索引；例如 256 色图像可配 `256 × 3` 的 RGB 映射表|
|真彩色图像（True-color Image）|三个颜色通道|每通道常见为 `0`–`255`，也可为归一化浮点数|每个像素直接保存红、绿、蓝分量；三个 `H × W` 平面共同组成彩色图像|

> [!warning] 通道顺序（Channel Order）取决于库与格式
> RGB 图像的颜色语义是红、绿、蓝，但内存数组的实际通道顺序取决于读取库：Matplotlib 与 Pillow 常见为 RGB，OpenCV 的 `cv2.imread()` 默认常见为 BGR。显示前必须确认并在需要时转换，不能把 BGR 当成所有彩色图像的固定顺序。
### 1.2 张量形状（Tensor Shape）
- NumPy、Matplotlib 和许多图像文件接口常使用通道后置（Channels-last）布局：`[H, W, C]`。
- PyTorch 单张图像通常使用通道前置（Channels-first）布局：`[C, H, W]`。
- PyTorch 二维卷积批输入通常使用 `NCHW`：`[N, C, H, W]`。
- **批次大小（Batch Size, `N`）**：一次并行处理的样本数，通常在网络前向传播中保持不变。
- **通道（Channel, `C`）**：输入阶段可能是 1 或 3；经过卷积后由输出卷积核数量决定，常随网络加深而增多。
- **高度与宽度（Height and Width, `H`, `W`）**：由卷积的步长、填充、空洞率与池化共同决定，通常逐阶段减小。
> [!tip] 大白话理解（Plain-language Intuition）
> `[N, C, H, W]` 可以读成“这次有几张图、每张图有几张特征表、每张表有多高和多宽”。卷积主要改变特征表数量，步长和池化主要改变表的高宽。
## 2. 图像读取与可视化（Image Loading and Visualization）
### 2.1 构造黑白图像
```python
import matplotlib.pyplot as plt
import numpy as np

black = np.zeros((200, 200, 3), dtype=np.uint8)
white = np.full((200, 200, 3), 255, dtype=np.uint8)

figure, axes = plt.subplots(1, 2, figsize=(6, 3))
axes[0].imshow(black)
axes[0].set_title("Black")
axes[0].axis("off")
axes[1].imshow(white)
axes[1].set_title("White")
axes[1].axis("off")
plt.tight_layout()
plt.show()
```
该示例产生图形窗口，属于依赖图形后端的视觉输出，因此不附固定控制台 Output。
### 2.2 读取、保存和检查图像
```python
import matplotlib.pyplot as plt

image = plt.imread("data/img.jpg")
print(image.shape)  # 代表性输出: (640, 640, 3)，实际值取决于文件

# 保存文件会修改外部文件系统；输出文件内容还可能受编码参数影响。
plt.imsave("data/img_copy.jpg", image)
plt.imshow(image)
plt.axis("off")
plt.show()
```
- `plt.imread()` 返回的数组形状和数据类型取决于图像格式与读取后端。
- `plt.imsave()` 有写文件副作用（Side Effect）；应避免覆盖唯一原图。
- 训练代码通常还需要处理方向元数据、透明通道（Alpha Channel）、色彩空间和损坏文件。
## 3. 输入预处理（Input Preprocessing）
### 3.1 目的
- **统一数值尺度（Numerical Scale）**：避免不同特征量级使优化路径严重失衡。
- **改善优化条件（Optimization Conditioning）**：中心化或标准化通常能让梯度下降更容易找到有效步长。
- **降低饱和风险（Saturation Risk）**：Sigmoid、Tanh 等激活在绝对值较大处导数很小；合适的输入尺度可降低早期层落入饱和区的概率。
- **匹配预训练模型（Pretrained Model）**：使用预训练权重时必须采用相应权重文档规定的尺寸、通道顺序、缩放和均值/标准差。
> [!tip] 大白话理解（Plain-language Intuition）
> 如果一个输入特征在几千量级，另一个只有零点几，优化器会像在一条又长又窄的峡谷里走路：某个方向一步就跨过头，另一个方向又几乎没动。预处理是在训练前把地形整理得更好走。
### 3.2 常见方法
- **缩放（Rescaling）**：把 `uint8` 的 `0`–`255` 转为浮点数 `0`–`1`。
- **去均值（Zero-centering）**：按通道或特征减去训练集均值。
- **标准化（Standardization）**：再除以训练集标准差，使各通道尺度相近。
- **几何变换（Geometric Transform）**：缩放、裁剪、旋转、翻转；其中随机操作可作为数据增强（Data Augmentation）。
- **颜色变换（Color Transform）**：灰度化、亮度、对比度、饱和度、色调调整。
- **图像合成（Image Composition）**：Mixup、CutMix 等方法需要同步处理标签语义。
- **主成分分析（Principal Component Analysis, PCA）与白化（Whitening）**：经典机器学习中可用于降维与去相关；现代 CNN 原始像素输入通常不把它们作为默认步骤，因为计算成本、空间结构变化以及与端到端表征学习的重复性都需要权衡。
### 3.3 防止数据泄漏（Data Leakage）
- 均值、标准差、PCA 基向量和白化参数只能由训练集估计。
- 验证集和测试集必须复用训练集参数，不能各自重新拟合。
- 数据增强通常只用于训练集；验证与测试应使用确定性变换。
## 4. 为什么使用卷积神经网络（Convolutional Neural Network, CNN）
把 `32 × 32 × 3` 图像直接连接到 1,000 个全连接神经元需要约 `32 × 32 × 3 × 1,000 = 3,072,000` 个权重；图像分辨率上升时参数量迅速增长。CNN 利用图像的局部结构减少参数，并让同一特征检测器能在不同空间位置复用。
### 4.1 核心归纳偏置（Inductive Bias）
- **局部连接（Local Connectivity）**：一个输出位置只观察输入的局部感受野（Receptive Field）。
- **参数共享（Parameter Sharing）**：同一个卷积核在空间位置间共享权重。
- **层次化表征（Hierarchical Representation）**：浅层常学习边缘、颜色对比和纹理；更深层组合出部件、形状和任务相关语义。
- **平移等变性（Translation Equivariance）**：理想条件下，输入平移会使特征图相应平移；边界填充、步长和离散采样会影响严格等变性。
- **近似不变性（Approximate Invariance）**：池化、全局平均、数据增强和任务训练可使最终预测对小幅位移更稳定，但不是无条件的旋转、缩放或平移不变。
> [!tip] 大白话理解（Plain-language Intuition）
> 全连接层像给图像的每个位置都配一套独立规则；卷积像拿同一个“特征模板”扫描整张图。这样既少学很多参数，也不会因为边缘从左边移到右边就必须重新学一遍“什么是边缘”。
### 4.2 基本组件与职责

|组件（Component）|主要职责|典型形状变化|是否有可学习参数|
|---|---|---|---|
|输入层（Input Layer）|读取、批处理、缩放与标准化|转换布局或尺寸|无|
|卷积层（Convolution Layer）|提取局部空间与跨通道特征|改变 `C`，可改变 `H/W`|有|
|激活层（Activation Layer）|引入非线性；逐元素激活通常不改变形状|通常不变|通常无|
|归一化层（Normalization Layer）|稳定中间激活的尺度与优化行为|通常不变|常有仿射参数|
|池化层（Pooling Layer）|空间聚合、下采样或固定输出尺寸|通常减小 `H/W`，保持 `C`|无|
|展平/全局池化（Flatten/Global Pooling）|把特征图连接到预测头|从空间张量变为特征向量|无|
|全连接层（Fully Connected Layer）|聚合全局信息并产生分类或回归输出|变为目标输出维度|有|

- 如果没有非线性激活，多层线性卷积与线性层的组合仍可合并成一个线性变换，表达能力受到限制。
- 卷积核覆盖整个输入空间且输出为 `1 × 1` 时，可实现与全连接层相同的连接模式；二者张量布局和权重组织仍可能不同。
- CNN 的参数效率与端到端学习减少了手工特征设计需求，但训练仍可能需要大量数据、算力与超参数选择；中间特征也不总能对应唯一可解释的物理概念。
## 5. 应用场景（Applications）
- 图像分类（Image Classification）：为整张图预测类别。
- 目标检测（Object Detection）：同时预测目标位置与类别。
- 图像分割（Image Segmentation）：为像素或区域预测语义类别。
- 人脸分析（Face Analysis）：检测、验证或识别身份；实际应用需评估隐私、公平性和误识别风险。
- 医学图像分析（Medical Image Analysis）：辅助检测异常、分割组织或预测风险；不能替代临床验证。
- 自动驾驶感知（Autonomous-driving Perception）：识别车道、车辆、行人和交通标志。
- 视频、语音和时序信号：一维或三维卷积也可处理局部相关结构。
## 6. 经典架构学习脉络（Classic Architecture Roadmap）
- **LeNet-5**：早期成功 CNN；卷积、子采样和全连接分类构成基础模板。
- **AlexNet**：以更深网络、ReLU、最大池化和 Dropout 推动大规模图像分类突破。
- **VGGNet**：系统使用堆叠的 `3 × 3` 卷积探索深度与统一结构。
- **GoogLeNet / Inception**：并行使用不同尺度分支并连接结果，在表达能力与计算量之间折中。
- **ResNet**：使用残差连接（Residual Connection）改善深层网络优化，让信息与梯度存在更短路径。
- **DenseNet**：每层接收之前多层特征，强调特征复用和直接信息流。
- **MobileNet**：以深度可分离卷积（Depthwise Separable Convolution）显著降低移动端计算量。
> [!tip] 大白话理解（Plain-language Intuition）
> 这条演化路线可以看作不断回答三个问题：怎样看得更深、怎样让梯度走得更顺、怎样用更少计算保留有效特征。学习时先掌握卷积和池化，再学残差连接，最后比较轻量化结构会更自然。
## 7. 关联笔记（Related Notes）
- [[神经网络激活函数（Neural Network Activation Functions）]]
- [[神经网络参数初始化与梯度流（Neural Network Initialization and Gradient Flow）]]
- [[模型欠拟合、过拟合与泛化（Model Underfitting, Overfitting, and Generalization）]]
- [[二维卷积、感受野与 Conv2d（2D Convolution, Receptive Field, and Conv2d）]]
- [[池化、尺寸变换与 CNN 网络结构（Pooling, Spatial Transformation, and CNN Architecture）]]
