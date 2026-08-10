## 一、 OpenCV 概述与安装

### 1. OpenCV 简介

**OpenCV (Open Source Computer Vision Library)** 是一个开源的图像处理框架，是传统计算机视觉中最常用、最强大的图像处理库。

- **多语言支持**：提供 C++、Python、Java 等版本的 API。
- **多平台支持**：支持 Windows、Linux、macOS、iOS 以及 Android。
- **深度学习时代的定位**：
    
    1. **图像预处理**：在模型训练前对数据进行清洗、增强。
    2. **模型部署**：使用 PyTorch 等框架训练好的模型，可以使用 OpenCV 的 DNN 模块进行轻量化部署。

### 2. 官方资源

- **官网**：[opencv.org](https://www.google.com/search?q=https://opencv.org/&authuser=4)
- **源码**：[GitHub - opencv/opencv](https://github.com/opencv/opencv)
- **文档**：[docs.opencv.org](https://www.google.com/search?q=https://docs.opencv.org/&authuser=4)

### 3. 安装命令

```Bash
pip install opencv-python==4.5.5.64
```

## 二、 图像存储原理与颜色空间

### 1. 主流颜色空间

- **RGB 颜色空间**（加法混色，用于显示器）：
    - **3 通道**：Red、Green、Blue。
    - **取值范围**：$[0, 255]$ 或 $[0.0, 1.0]$。
    - **典型值**：白色 $(255, 255, 255)$、黑色 $(0, 0, 0)$。
- **CMY(K) 颜色空间**（减法混色，用于印刷）：
    - **4 通道**：Cyan（青）、Magenta（洋红）、Yellow（黄）、Key（黑色）。
- **HSV 颜色空间**（符合人类视觉直觉）：
    - **3 通道**：
        - **H (Hue)**：色调（颜色种类）。
        - **S (Saturation)**：饱和度（颜色的浓淡）。
        - **V (Value)**：明度（颜色的明亮程度）。
    - > **注意**：在不同的平台/库中，HSV 各通道的取值范围存在差异（例如 OpenCV 中 $H$ 的范围是 $[0, 180]$）。

### 2. 图像的计算机存储格式

- **BGR 三通道彩色图**：在 OpenCV 中，彩色图像默认的通道顺序是 **BGR**（而非 RGB），其底层存储为大小为 $H \times W \times C$ 的三维 NumPy 矩阵。
- **单通道灰度图**：仅包含亮度信息，取值范围为 $[0, 255]$。
- **灰度转换公式**：
    
    $$Gray = R \times 0.3 + G \times 0.59 + B \times 0.11$$

## 三、 OpenCV 基础操作与算术运算

### 1. 基础图像与视频操作 API

|**API**|**功能描述**|
|---|---|
|`cv.imread(path)`|从磁盘加载图像（默认使用 **BGR** 格式读取）|
|`cv.imshow(winname, mat)`|窗口展示图像|
|`cv.imwrite(path, img)`|将图像保存到磁盘|
|`cv.waitKey(delay)`|暂停程序，等待并接收键盘输入|
|`cv.destroyAllWindows()`|释放所有 OpenCV 窗口资源|
|`cv.VideoCapture()`|创建摄像头捕获对象，或读取视频文件|
|`cv.line()` / `cv.circle()` / `cv.rectangle()`|绘制直线、圆、矩形|
|`cv.ellipse()` / `cv.polylines()`|绘制椭圆、多边形|
|`cv.putText()`|在图像中绘制文字|

### 2. 图像算术与像素操作

> **💡 核心提示**：使用 Python 时，OpenCV 读取的图像就是 **NumPy 数组**，可以直接利用 NumPy 的切片和索引进行高效的像素级操作。

|**API / 数组操作**|**功能描述**|
|---|---|
|`img.item(r, c, ch)` / `img.itemset()`|高效获取 / 设置特定像素通道的值|
|`cv.split(img)`|将多通道图像拆分为单通道列表|
|`cv.merge(mv)`|将多个单通道合并为多通道图像|
|`cv.copyMakeBorder()`|在图像四周添加边框（用于 Padding 边界填充）|
|`cv.addWeighted(src1, alpha, src2, beta, gamma)`|将两幅图像进行加权融合（重叠混合）|
|`cv.bitwise_not(src)`|**按位取反**：$dst = \text{uint8}(\sim src)$|
|`cv.bitwise_and(src1, src2)`|**按位与**：$dst = \text{uint8}(src1 \ \& \ src2)$|
|`cv.bitwise_or(src1, src2)`|**按位或**：$dst = \text{uint8}(src1 \ \vert{} \ src2)$|
|`cv.bitwise_xor(src1, src2)`|**按位异或**：$dst = \text{uint8}(src1 \ \wedge \ src2)$|

## 四、 图像几何变换

在图像平移、旋转或仿射变换中，对于未被原图像覆盖的空白区域，OpenCV 默认**填充黑色像素**。

|**API**|**功能描述**|**核心原理**|
|---|---|---|
|`cv.cvtColor()`|颜色空间转换|如 `COLOR_BGR2GRAY` 转换为灰度图|
|`cv.resize()`|图像大小缩放|调整图像的分辨率（可指定插值算法）|
|`cv.warpAffine()`|仿射变换|使用 $2 \times 3$ 变换矩阵 $M$，保证点共线性不变（平移、旋转）|
|`cv.warpPerspective()`|透视变换|使用 $3 \times 3$ 变换矩阵 $M$，保证三点共线，适应空间视角旋转|
|`cv.threshold()`|简单二值化|根据全局单一阈值，将灰度图转为黑白二值图|
|`cv.adaptiveThreshold()`|自适应二值化|根据像素邻域的局部特征动态计算阈值，抗光照不均效果好|

## 五、 空域变换：滤波、卷积与形态学

### 1. 滤波与卷积基础

- **原理**：在图像的每个位置 $(x, y)$，取其邻域像素与**卷积核 (Kernel)** 进行加权求和。
- **卷积核尺寸**：通常为**奇数**（如 $3 \times 3$, $5 \times 5$, $7 \times 7$），以便确定唯一的中心像素点。
- **边界填充 (Padding)**：为了使滤波前后的图像尺寸一致。
    - **API**：`cv.copyMakeBorder()`
    - **常见填充模式**：
        - 补常数 (`BORDER_CONSTANT`)
        - 复制边界像素 (`BORDER_REPLICATE`)
        - 块复制 (`BORDER_WRAP`)
        - 镜像反射 (`BORDER_REFLECT`)

### 2. 三种经典的平滑（去噪）滤波器

1. **均值滤波 (Averaging)**：
    
    - Kernel 内所有权重系数完全相同，且系数之和为 1。适用于滤除温和的随机噪声，但会使图像边缘变模糊。
        
2. **中值滤波 (Median Blur)**：
    
    - **原理**：统计邻域内的所有像素值，排序后取**中位数**作为输出。
    - **特点**：能**极其有效地滤除椒盐噪声**，且对边缘的保护好于均值滤波。
        
3. **高斯滤波 (Gaussian Blur)**：
    
    - **原理**：模拟人眼，距离中心越近的像素权重越大。可有效滤除高斯噪声。
    - **2D 高斯函数**：
        
        $$G_{\sigma}(x,y) = \frac{1}{2\pi\sigma^{2}}e^{-\frac{x^{2}+y^{2}}{2\sigma^{2}}}$$
        
        _(注：标准差 $\sigma$ 越小，关注范围越窄；$\sigma$ 越大，图像越模糊。)_
        
    - **级联可分解性**：2D 高斯卷积可分解为两个连续的 1D 卷积（水平 + 垂直），能够将计算复杂度从 $O(K^2)$ 降低到 $O(2K)$：
        
        $$G_{\sigma}(x,y) = \left(\frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{x^{2}}{2\sigma^{2}}}\right) \cdot \left(\frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{y^{2}}{2\sigma^{2}}}\right)$$

### 3. 图像形态学操作

形态学操作主要用于处理二值图像，通过控制膨胀与腐蚀来提取形状、去噪和连接区域。

- **腐蚀 (Erode)**：
    - **原理**：用结构元素的**最小值**代替中心像素（类似于局部**最小值滤波 / 最小池化**）。
    - **作用**：消除图像边缘的细小分支或白噪点，使线条变细。
- **膨胀 (Dilate)**：
    - **原理**：用结构元素的**最大值**代替中心像素（类似于局部**最大值滤波 / 最大池化**）。
    - **作用**：增加白域面积，用于在腐蚀后恢复并增强目标区域的信息。
- **开运算 (Open)**：
    - $\text{Open} = \text{先腐蚀} \rightarrow \text{后膨胀}$。常用于**消除明亮的孤立噪点**（白噪声）。
- **闭运算 (Close)**：
    - $\text{Close} = \text{先膨胀} \rightarrow \text{后腐蚀}$。常用于**填充前景物体内的细小黑色空洞**或连接邻近断开的区域。
- **形态学梯度 (Morphological Gradient)**：
    - $\text{Gradient} = \text{Dilate} - \text{Erode}$。能非常直观地**提取物体的边缘轮廓**。
- **顶帽 (Top Hat)**：
    - $\text{TopHat} = \text{Image} - \text{Open}$。用于分离比邻域更亮的微小局部特征（非交叉点信息）。
- **黑帽 (Black Hat)**：
    - $\text{BlackHat} = \text{Close} - \text{Image}$。用于分离比邻域更暗的局部微小特征。

## 六、 边缘检测与梯度算子

### 1. 边缘的数学定义

边缘是指图像中**像素值发生剧烈变化**的区域。在数学上对应于像素值函数的一阶导数极值点。因为导数运算对高频噪声极度敏感，所以**在提取边缘之前，必须先进行高斯去噪**。

- **微分与卷积的结合**：
    
    $$\frac{d}{dx}(f * g) = f * \frac{d}{dx}g$$

### 2. 常见梯度算子

- **Sobel 算子**：结合了高斯平滑与差分运算。
    - **水平梯度 $S_x$（检测垂直边缘）**：
        
        $$S_{x} = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}$$
        
    - **垂直梯度 $S_y$（检测水平边缘）**：
        
        $$S_{y} = \begin{bmatrix} 1 & 2 & 1 \\ 0 & 0 & 0 \\ -1 & -2 & -1 \end{bmatrix}$$
        
- **Laplacian 算子**：二阶微分算子，适用于块团（Blob）检测和边缘粗略定位。
    
    $$\Delta src = \frac{\partial^2 src}{\partial x^2} + \frac{\partial^2 src}{\partial y^2}$$
    
    - 常用 $3 \times 3$ 核：
        
        $$\begin{bmatrix} 0 & 1 & 0 \\ 1 & -4 & 1 \\ 0 & 1 & 0 \end{bmatrix} \quad \text{或} \quad \begin{bmatrix} 1 & 1 & 1 \\ 1 & -8 & 1 \\ 1 & 1 & 1 \end{bmatrix}$$

### 3. Canny 边缘检测算法（五部曲）

Canny 是传统视觉中最鲁棒、最经典的边缘检测算法。

```
[高斯滤波去噪] ──> [计算梯度幅值与方向] ──> [非极大值抑制(NMS)] ──> [双阈值检测] ──> [抑制孤立弱边缘]
```

1. **高斯滤波**：滤除图像高频噪点。
2. **计算梯度**：使用 Sobel 算子分别求出水平 $G_x$ 与垂直 $G_y$ 梯度，进而求出梯度幅值 $G$ 和方向 $\theta$：
    
    $$G = \sqrt{G_{x}^{2} + G_{y}^{2}}, \quad \theta = \arctan(G_{y} / G_{x})$$
    
3. **非极大值抑制 (NMS)**：为了实现边缘的“瘦身”。沿着当前像素的梯度方向比较相邻两点，如果当前像素非局部最大值，则将其梯度置为 0。
4. **双阈值检测 (Double Threshold)**：
    
    - $G > \text{HighThreshold} \rightarrow$ **强边缘**（保留）。
    - $G < \text{LowThreshold} \rightarrow$ **非边缘**（抑制）。
    - $\text{LowThreshold} \le G \le \text{HighThreshold} \rightarrow$ **弱边缘**（待定）。
        
5. **抑制孤立弱边缘**：检查弱边缘的 8 邻域像素。如果该弱边缘连接了强边缘，则保留；否则将其抑制。因为真实的弱边缘必然与强边缘相连。

## 七、 直方图、模板匹配与图像特征提取

### 1. 直方图与模板匹配

- **直方图 (Histogram)**：统计各个亮度值的分布比例，直方图均衡化（`cv.equalizeHist`）是提升图像对比度的有效手段。
- **模板匹配 (Template Matching)**：在大图中滑动搜索与模板图最匹配的区域（API：`cv.matchTemplate`）。

### 2. HOG 特征（方向梯度直方图）

**HOG (Histogram of Oriented Gradients)** 是一种通过统计局部区域梯度方向密度来构建特征的描述子，经典应用是 **HOG + SVM 进行行人检测**。

#### 🪐 提取步骤：

1. **灰度化与 Gamma 校正**：降低图像局部阴影和光照变化带来的影响。
2. **计算梯度**：获取每个像素的梯度大小和方向，保留边缘结构信息。
3. **划分 Cell（细胞单元）**：将图像划分为不重叠的小区域（例如 $8 \times 8$ 像素）。在每个 Cell 内将 $0^\circ \sim 180^\circ$ 的梯度方向平均划分为 9 个区间（Bins），进行直方图加权统计，得到一个 9 维特征向量。
4. **组合 Block（块）**：将相邻的 Cell（例如 $2 \times 2$ 个 Cell，即 4 个 Cell）组合成一个 Block。将这 4 个 Cell 的 $4 \times 9 = 36$ 维特征串联，并做 **L2 范数归一化**。
5. **串联特征**：用 Block 滑动扫描整个图像，把所有 Block 归一化后的特征向量连接起来，即为整幅图的 HOG 特征。

#### 📐 特征维度计算示例：

假设输入图像大小为 $64 \times 128$，设 Cell 大小为 $16 \times 16$，Block 大小为 $2 \times 2$ 个 Cell（即 $32 \times 32$ 像素），扫描步长（BlockStride）为 8 像素。

- 每个 Cell 有 9 维特征 $\rightarrow$ 每个 Block 包含 $4 \times 9 = 36$ 维特征。
- 水平方向 Block 扫描窗口数：$\frac{64 - 32}{8} + 1 = 5$ 个。
- 垂直方向 Block 扫描窗口数：$\frac{128 - 32}{8} + 1 = 13$ 个。
- **最终 HOG 特征总维度**：
    
    $$\text{Dimension} = 36 \times 5 \times 13 = 2340 \text{ 维}$$

### 3. LBP 特征（局部二值模式）

**LBP (Local Binary Pattern)** 是一种描述图像局部纹理特征的算子，具有卓越的**旋转不变性**和**灰度不变性**。

#### 🪐 提取步骤：

1. **局部二值化**：在 $3 \times 3$ 窗口中，以中心像素灰度值为阈值，比较其周边的 8 个相邻像素：
    
    - 周边像素值 $\ge$ 中心像素值 $\rightarrow$ 标记为 1；
    - 周边像素值 $<$ 中心像素值 $\rightarrow$ 标记为 0。
        
2. **十进制转换**：顺时针（或逆时针）读取这 8 位二进制数，将其转换为十进制数，作为该中心像素的 LBP 值，反应该区域的纹理信息。
3. **分区直方图统计**：将图像划分为若干个不重叠的 Cell（例如 $16 \times 16$），统计各 Cell 的 LBP 直方图（如划分 9 个 Bins），并进行 L2 归一化。
4. **串联特征**：串联所有 Cell 的直方图，形成整幅图像的 LBP 纹理特征向量。

#### 📐 特征维度计算示例：

假设输入图像大小为 $64 \times 128$，Cell 大小为 $16 \times 16$，无重叠。

- 水平方向有 $64 / 16 = 4$ 个 Cell，垂直方向有 $128 / 16 = 8$ 个 Cell。
- 设每个 Cell 的 LBP 直方图有 9 维。
- **最终 LBP 特征总维度**：
    
    $$\text{Dimension} = 9 \times 4 \times 8 = 288 \text{ 维}$$

### 4. Haar 特征

- **原理**：利用数种固定形状的**黑色和白色矩形模板**，定义特征值为：
    
    $$\text{Haar 特征值} = \sum \text{白色矩形区域内所有像素和} - \sum \text{黑色矩形区域内所有像素和}$$
    
- **物理意义**：用于极快速地反映局部区域的灰度起伏（例如：人眼区域比额头、脸颊更暗，鼻梁比两侧更亮）。
- **应用**：结合 **Adaboost 弱分类器级联（Harr 级联分类器）**，实现高效率的人脸快速检测。