---
title: "OpenCV Python 工具箱：I/O、视频、交互与图像处理（OpenCV Python Toolbox）"
tags:
  - data-science/cv/opencv/toolbox
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# OpenCV Python 工具箱：I/O、视频、交互与图像处理（OpenCV Python Toolbox）
## 一、 环境搭建与 GUI 交互(Environment Setup and GUI Interaction)
### 1.1 环境配置与模块导入(Environment Setup and Module Imports)
使用所有图像处理模块的前置条件，需先导入 cv2、numpy 及 matplotlib 库。
```Python
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
```
### 1.2 窗口创建与图形显示(Window Creation and Display)
用于在屏幕上创建图形用户界面 (Graphical User Interface) 来展示图像。
#### 核心函数与参数
- `cv.namedWindow(winname, flags)`：创建指定名称的窗口。
    - `winname`：窗口名称字符串。
    - `flags`：窗口属性，如 `cv.WINDOW_NORMAL` 允许调整窗口大小。
- `cv.imshow(winname, mat)`：在指定窗口显示图像。
    - `winname`：窗口名称。
    - `mat`：要显示的图像矩阵数据。
- `cv.waitKey(delay)`：键盘绑定函数，让图像暂停指定毫秒数。
    - `delay`：等待时间（毫秒）。当 `delay=0` 时，表示无限期等待，直到有键盘任意输入。在 Linux 等系统中常配合 `& 0xFF` 提取低 8 位 ASCII 码 (ASCII Code)。
- `cv.destroyAllWindows()`：释放所有由 OpenCV 创建的窗口资源。
- `cv.destroyWindow(winname)`：释放指定的单一窗口资源。
- `cv.resizeWindow(winname, width, height)`：调整窗口大小（注：前提是窗口属性支持调整）。
#### 使用示例

```Python
# 加载图像
img = cv.imread("./images/xiaoren.png")
# 创建可调整大小的窗口并显示
cv.namedWindow('image', cv.WINDOW_NORMAL)
cv.imshow('image', img)
# 等待 Esc 键 (ASCII 码为 27) 退出
k = cv.waitKey(0) & 0xFF
if k == 27:
    print("Esc键退出")
# 释放资源
cv.destroyWindow('image')
cv.destroyAllWindows()
```

### 1.3 图像文件读取与保存(Image Input and Output)
OpenCV 默认读取图像的通道顺序为 BGR 格式，若图像包含透明通道需指定原样读取模式。
#### 核心函数与参数

- `cv.imread(filename, flags)`：加载图片。**注意：OpenCV 加载彩色图的默认通道 (Channel) 顺序是 BGR，而不是 RGB。** 不支持包含中文的路径。
    - `filename`：图片路径。
    - `flags`：加载模式标志（支持枚举常量或数字代号）：
        - `cv.IMREAD_COLOR`（或 `1`）：加载 3 通道 BGR 彩色图（默认模式，自动忽略 Alpha 透明通道）。
        - `cv.IMREAD_GRAYSCALE`（或 `0`）：加载为单通道灰度图 (Grayscale)。
        - `cv.IMREAD_UNCHANGED`（或 `-1`）：按原样加载（若图像包含 Alpha 透明通道，则保留读入为 4 通道 BGRA）。
- `cv.imwrite(filename, img)`：保存图片。
    - `filename`：保存的完整文件路径和名称（需包含后缀名）。
    - `img`：要保存的 Numpy 多维数组 (N-dimensional Array) 图像对象。
- `cv.cvtColor(src, code)`：颜色空间转换。
    - `src`：输入图像。
    - `code`：转换代码，例如 `cv.COLOR_BGR2GRAY` (转灰度)、`cv.COLOR_BGR2RGB` (转 RGB 以适配 Matplotlib)。

#### 使用示例

```python
# 1. 使用枚举常量读取为灰度图
img_gray = cv.imread('./images/t1.png', cv.IMREAD_GRAYSCALE)

# 2. 读取彩色图并转为 RGB 供 Matplotlib 显示
img_bgr = cv.imread('./images/t1.png', cv.IMREAD_COLOR)
img_rgb = cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)

# 3. 读取带透明通道的 PNG 图片
img_alpha = cv.imread('./images/logo.png', cv.IMREAD_UNCHANGED)

# 4. 保存图像
cv.imwrite('./images/output.png', img_gray)
```
### 1.4 路径兼容处理与安全退出机制(Path Compatibility and Safe Exit Mechanism)
包含中文路径的图片需结合 NumPy 字节流解码读取，程序安全退出需捕获键盘事件并显式释放窗口资源。
#### 1.4.1 路径问题与不同系统的差异
- **Windows 与 Mac/Linux 的路径符号差异**：
    Windows 系统默认使用反斜杠 `\\` 作为路径分隔符，而在 Python 字符串中 `\\` 是转义字符。Mac/Linux 系统使用正斜杠 `/`。

    - **解决办法**：在 Windows 中推荐使用原始字符串 (Raw String) 前缀 `r`，或者统一使用双反斜杠 `\\\\` 或正斜杠 `/`。
- **包含中文的路径**：
    OpenCV 的 `cv.imread` 底层是由 C++ 实现的，默认不支持带有中文字符的路径，读取会返回 `None` 且不报错，导致后续处理崩溃。

    - **解决办法**：尽量使用纯英文路径。如果必须使用中文路径，需使用 Numpy 的 `np.imdecode` 和 `np.fromfile` 结合来绕过限制。

#### 1.4.2 程序退出的逻辑问题
- 很多新手直接点击窗口右上角的“X”来关闭窗口，这会导致 Python 内核卡死或抛出异常。
- **正确的逻辑**：必须通过 `cv.waitKey()` 捕获键盘事件 (Keyboard Events) 来安全跳出循环，并执行 `cv.destroyAllWindows()` 释放内存。
### 核心代码示例

```Python
# 1. 安全读取带有中文的路径（绕过 imread 的限制）
import numpy as np
import cv2 as cv
# 使用 np.fromfile 读取文件字节流，再用 cv.imdecode 解码为图像矩阵
img_path = "./images/中文文件夹/测试.png"
img_data = np.fromfile(img_path, dtype=np.uint8)
img = cv.imdecode(img_data, cv.IMREAD_COLOR)
cv.imshow('Image', img)
# 2. 严谨的退出逻辑：等待按下 'q' 键或 'Esc' 键 (ASCII: 27)
while True:
    key = cv.waitKey(10) & 0xFF
    if key == 27 or key == ord('q'):  # ord() 函数获取字符的 ASCII 码
        break
cv.destroyAllWindows()
```

### 1.5 视频流读取、处理与录制写出 (Video Reading, Processing, and Writing)

OpenCV 通过 `cv.VideoCapture` 和 `cv.VideoWriter` 实现视频流的输入输出。处理视频的本质是**在循环中逐帧（Frame）处理图像矩阵**。

#### 1.5.1 视频读取与播放控制 (VideoCapture & Playback)

**核心函数与参数**
* `cv.VideoCapture(source[, apiPreference])`：
  * `source`：传入 `0` 打开默认摄像头；传入文件路径（如 `"classroom.mp4"`）播放静态视频。
  * `apiPreference`（Mac 专属）：显式指定 `cv.CAP_AVFOUNDATION` 可解决 Mac 打开摄像头报错/黑屏问题。
* `cap.read()`：读取下一帧，返回 `(success, frame)`。`success` 为布尔值，`frame` 为三通道图像矩阵。
* `cap.get(propId)` / `cap.set(propId, value)`：获取/设置视频属性：
  * `cv.CAP_PROP_FRAME_WIDTH` / `cv.CAP_PROP_FRAME_HEIGHT`：宽高尺寸。
  * `cv.CAP_PROP_FPS`：视频帧率。
  * `cv.CAP_PROP_FRAME_COUNT`：视频总帧数。

**帧率控制公式（关键）**
播放本地视频时，若直接使用 `cv.waitKey(1)` 会导致视频以 CPU 最大速度快进播放。必须根据视频 FPS 计算单帧延时毫秒数：
$$\text{delay} = \text{int}\left(\frac{1000}{\text{FPS}}\right)$$

---

#### 1.5.2 视频录制写出 (VideoWriter)

**核心函数与参数**
* `cv.VideoWriter(filename, fourcc, fps, frameSize)`：
  * `filename`：输出视频路径（如 `'./videos/output.avi'`）。
  * `fourcc`：视频编码器。常用 `cv.VideoWriter_fourcc(*'XVID')` 或 `'I', '4', '2', '0'`。
  * `fps`：录制帧率。
  * `frameSize`：`(width, height)` 元组，**必须与写入的 `frame` 矩阵尺寸严格一致**，否则导出的视频损坏无法播放。
* `writer.write(frame)`：写入单帧图像。
* `writer.release()`：保存并关闭文件（未 release 会导致视频文件不完整）。

---

#### 1.5.3 视频帧提取与数据集保存 (Frame Extraction)

将视频按特定时间/帧数间隔抽取为单张图像（常用于算法训练数据集制作）。

**关键逻辑**
1. 使用 `os.makedirs(output_dir, exist_ok=True)` 自动创建目录。
2. 使用取模运算 `frame_counter % frame_interval == 0` 控制抽帧频率。
3. 使用 f-string 填充零格式化文件名（如 `f"frame_{counter:06d}.jpg"`），确保排序正确。

---

#### 1.5.4 实时视频流处理与 macOS 平台避坑规范

在实时视频流循环中植入算法（如模板匹配 `cv.matchTemplate`、目标追踪、轮廓检测），并针对 macOS 系统 GUI 框架做兼容。

**macOS 四大避坑规范**
1. **摄像头后端**：打开摄像头时指定 `cv.VideoCapture(0, cv.CAP_AVFOUNDATION)`。
2. **硬件预热延时**：打开摄像头后增加 `time.sleep(0.5)` 给硬件初始化，避免前几帧 `read()` 报空。
3. **点击红叉安全退出**：检测窗口关闭事件 `if cv.getWindowProperty(win_name, cv.WND_PROP_VISIBLE) < 1: break`。
4. **清空 Cocoa 消息队列（解决卡死）**：调用 `destroyAllWindows()` 后，必须循环执行 4~5 次 `cv.waitKey(1)` 强行刷新 Mac 的底层 GUI 事件队列，否则窗口在关闭时会冻结卡死。

---

#### 综合代码示例（涵盖播放、抽帧与 Mac 实时流处理）

```python
import cv2 as cv
import os
import time

# 示例 1：标准视频播放（含延时控制）
def play_video(video_path):
    cap = cv.VideoCapture(video_path)
    fps = cap.get(cv.CAP_PROP_FPS) or 25
    delay = int(1000 / fps)  # 计算帧延时

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        cv.imshow("Video Player", frame)
        if cv.waitKey(delay) & 0xFF in (ord('q'), 27): break

    cap.release()
    cv.destroyAllWindows()
    cv.waitKey(1)

# 示例 2：Mac 专用实时视频流模板匹配
def real_time_matching_mac(template_path, threshold=0.75):
    template = cv.imread(template_path)
    th, tw = template.shape[:2]

    # 使用 AVFOUNDATION 后端打开 Mac 摄像头
    cap = cv.VideoCapture(0, cv.CAP_AVFOUNDATION)
    time.sleep(0.5)  # 硬件预热

    win_name = "Mac Real-time Matching"
    cv.namedWindow(win_name, cv.WINDOW_NORMAL)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: continue

        # 实时模板匹配
        res = cv.matchTemplate(frame, template, cv.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv.minMaxLoc(res)

        if max_val >= threshold:
            cv.rectangle(frame, max_loc, (max_loc[0] + tw, max_loc[1] + th), (0, 255, 0), 2)

        cv.imshow(win_name, frame)

        # 点击红叉或按 q 键安全退出
        if cv.getWindowProperty(win_name, cv.WND_PROP_VISIBLE) < 1: break
        if cv.waitKey(1) & 0xFF in (ord('q'), 27): break

    # 彻底释放资源与刷新 Mac 窗口队列
    cap.release()
    cv.destroyAllWindows()
    for _ in range(5):  # 刷新 Cocoa 队列，防止窗口残余卡死
        cv.waitKey(1)
```
## 1.6 基础图形与文本绘制(Basic Geometry and Text Drawing)
所有绘制函数均直接在目标图像矩阵上原地修改，坐标点参数严格按照宽度与高度的映射关系传递。
### 通用核心参数
- `img`：给定要绘画的图像矩阵。
- `color`：像素点的颜色，通常为 BGR 格式的元组，如 `(255, 0, 0)` 表示蓝色。
- `thickness`：线条粗细程度。如果是闭合图形（如圆、矩形），设置为 `1` 表示填充 (Fill) 内部。
- `lineType`：线条类型。如 `cv.LINE_AA` 为抗锯齿 (Anti-aliasing)，边缘更平滑。
### 具体函数说明与参数
- `cv.line(img, pt1, pt2, color, thickness)`：画直线。`pt1` 为起点坐标 `(x, y)`，`pt2` 为终点坐标。
- `cv.rectangle(img, pt1, pt2, color, thickness)`：画矩形。`pt1` 为左上角坐标，`pt2` 为右下角坐标。
- `cv.circle(img, center, radius, color, thickness)`：画圆。`center` 为中心点坐标，`radius` 为半径。
- `cv.ellipse(img, center, axes, angle, startAngle, endAngle, color, thickness)`：画椭圆。`axes` 是 `(长轴, 短轴)`，`angle` 是旋转角度，`startAngle` 和 `endAngle` 控制绘制圆弧的范围 (0-360为完整椭圆)。
- `cv.polylines(img, pts, isClosed, color, thickness)`：画多边形。`pts` 为多边形顶点坐标列表的列表 `[np.array]`，`isClosed` 为布尔值控制是否闭合。
- `cv.putText(img, text, org, fontFace, fontScale, color, thickness, lineType)`：添加文本。`org` 是文本左下角基准点。
### 使用示例

```Python
## 创建 512x512 的纯黑画布
img = np.zeros((512, 512, 3), np.uint8)
## 1. 画蓝色对角直线
cv.line(img, pt1=(0, 0), pt2=(511, 511), color=(255, 0, 0), thickness=5)
## 2. 画红色空心矩形
cv.rectangle(img, pt1=(10, 10), pt2=(50, 320), color=(0, 0, 255), thickness=5)
## 3. 画实心红色半椭圆
cv.ellipse(img, center=(410, 410), axes=(50, 50), angle=0, startAngle=0, endAngle=180, color=(0, 0, 255), thickness=-1)
## 4. 绘制白色抗锯齿文字
cv.putText(img, text='OpenCV', org=(10, 450), fontFace=cv.FONT_HERSHEY_SIMPLEX,
           fontScale=4, color=(255, 255, 255), thickness=2, lineType=cv.LINE_AA)
cv.imshow('Drawing', img)
cv.waitKey(0)
cv.destroyAllWindows()
```

## 1.7 鼠标事件交互控制(Mouse Event Interaction Control)
OpenCV 允许我们将鼠标事件（点击、双击、滑动）与特定的回调函数 (Callback Function) 绑定，实现用鼠标在图像上动态交互。
### 核心函数与参数
- `cv.setMouseCallback(windowName, onMouse, userdata)`：为指定窗口绑定鼠标回调函数。
    - `windowName`：必须是已经通过 `cv.namedWindow` 创建的窗口名称。
    - `onMouse`：你自己定义的鼠标事件处理函数。
    - `userdata`：传递给回调函数的额外参数（可选）。
- **回调函数的固定签名**：`def callBack(event, x, y, flags, userdata)`
    - `event`：触发的鼠标事件类型，如 `cv.EVENT_LBUTTONDOWN` (左键按下)、`cv.EVENT_MOUSEMOVE` (鼠标移动)、`cv.EVENT_LBUTTONDBLCLK` (左键双击)。
    - `x, y`：鼠标事件发生时的坐标位置。
    - `flags`：鼠标拖拽或键盘结合的标志位（如是否按住了 Shift 键）。

### 使用示例（双击鼠标画圆）

```Python
import cv2 as cv
import numpy as np
## 1. 定义鼠标回调函数
def draw_circle(event, x, y, flags, param):
    # 如果事件是鼠标左键双击
    if event == cv.EVENT_LBUTTONDBLCLK:
        # 在 img 对象上以 (x,y) 为圆心画一个红色的实心圆
        cv.circle(img, center=(x, y), radius=30, color=(0, 0, 255), thickness=-1)
## 2. 创建黑色画板
img = np.zeros((512, 512, 3), np.uint8)
## 3. 创建窗口并绑定回调函数
cv.namedWindow('Mouse Interaction')
cv.setMouseCallback('Mouse Interaction', draw_circle)
## 4. 循环显示画面，直到按下 Esc 退出
while True:
    cv.imshow('Mouse Interaction', img)
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()
```

## 1.8 动态调节控件响应(Trackbar Control and Response)
滑动条 (TrackBar) 是 OpenCV 提供的一个轻量级 GUI 组件，常用于动态调节算法参数（如阈值大小、画笔颜色、播放速度等）。
### 核心函数与参数
- `cv.createTrackbar(trackbarName, windowName, value, count, onChange)`：创建滑动条。
    - `trackbarName`：滑动条的名称。
    - `windowName`：滑动条依附的窗口名称。
    - `value`：滑动条的初始默认值。
    - `count`：滑动条的最大值（最小值为 0）。
    - `onChange`：每次滑动条数值改变时触发的回调函数。
- `cv.getTrackbarPos(trackbarName, windowName)`：在主循环中获取当前滑动条的最新数值。
### 使用示例（制作一个简单的 RGB 调色板）

```Python
import cv2 as cv
import numpy as np
## 空的回调函数，因为我们在这个例子中只在主循环里主动获取位置
def nothing(x):
    pass
## 创建一个纯黑的初始图像和窗口
img = np.zeros((300, 512, 3), np.uint8)
cv.namedWindow('Color Palette')
## 创建三个代表 R, G, B 的滑动条，范围都是 0-255
cv.createTrackbar('R', 'Color Palette', 0, 255, nothing)
cv.createTrackbar('G', 'Color Palette', 0, 255, nothing)
cv.createTrackbar('B', 'Color Palette', 0, 255, nothing)
while True:
    cv.imshow('Color Palette', img)
    k = cv.waitKey(1) & 0xFF
    if k == 27:  # 按 Esc 退出
        break
    # 获取当前三个滑动条的位置数值
    r = cv.getTrackbarPos('R', 'Color Palette')
    g = cv.getTrackbarPos('G', 'Color Palette')
    b = cv.getTrackbarPos('B', 'Color Palette')
    # 将所有像素的颜色修改为滑动条指定的颜色
    img[:] = [b, g, r]  # 注意 OpenCV 是 BGR 顺序
cv.destroyAllWindows()
```

# 二、 图像像素操作与基础几何变换(Pixel Operations and Basic Geometric Transformations)
## 2.1 NumPy 像素切片与感兴趣区域提取(NumPy Pixel Slicing and ROI Extraction)
图像在 OpenCV 中本质上是 Numpy 的 `ndarray` 格式。形状通常为 `[H, W, C]` (高度, 宽度, 通道数)。使用切片提取感兴趣区域时高度索引在前宽度索引在后。
### 2.1.1 Numpy 图像处理模块
#### 核心操作与参数
- **通道分离**：通过 Numpy 切片 (Slicing) 获取 B、G、R 通道特征信息。
    - `img[:, :, 0]`：B 通道。
    - `img[:, :, 1]`：G 通道。
    - `img[:, :, 2]`：R 通道。
- **图像截取 (裁剪)**：`img[y_start:y_end, x_start:x_end, :]`。
- **图像转置**：`np.transpose(a, axes)`。
    - `axes`：维度的顺序。例如 `(1, 0, 2)` 表示将高度(0)和宽度(1)对调。

#### 使用示例

```Python
## 通道分离与手动灰度计算公式：Gray = R*0.3 + G*0.59 + B*0.11
## 注意归一化 (Normalization) 到 0.0-1.0 区间
gray_compute = (img[:, :, 2]*0.3 + img[:, :, 1]*0.59 + img[:, :, 0]*0.11) / 255
## 图像截取（裁剪 y:200-400, x:100-300 的区域）
img_crop = img[200:400, 100:300, :]
## 图像转置（宽高互换）
img_transposed = np.transpose(img, (1, 0, 2))
```
### 2.1.2 图像裁剪与像素访问 (Image Cropping and Pixel Access)
Numpy 底层的多维数组 (N-dimensional Array) 允许我们直接用切片 (Slicing) 操作图像区域。OpenCV 也提供了基于对象的内置函数，用于提取或修改单像素。
- **数组切片**：使用切片方式（如 `img[:100, :300]`）从原始图像中裁剪感兴趣区域 (Region of Interest, ROI)。
- `img.item(y, x, c)`：基于 Image 对象，获取指定坐标（行、列）在特定通道上的标量像素值。
- `img.itemset((y, x, c), value)`：将指定坐标和通道的像素设定为新的像素值。

```Python
## 1. 裁剪图像（截取左上角区域）
img2 = img[:100, :300]
## 2. 访问与修改像素（切片方式，不推荐在大循环中使用）
px = img[250, 300]
img[:, :, 2] = 127  # 设置所有红色像素为 127
## 3. 基于 OpenCV Image 对象的标量读写
blue_value = img.item(250, 300, 0)
img.itemset((250, 300, 0), 100)  # 将位置(250, 300)对应的蓝色像素修改为 100
```

## 2.2 图像通道拆分与重组(Channel Splitting and Merging)
作用于多通道图像，常用于分离特定颜色分量进行单独分析或重组色彩通道顺序。
- `cv.split(m)`：将多通道图像分离为多个独立的单通道二维数组。
- `cv.merge(mv)`：将多个单通道图像重组成一个多通道图像，可用于交换颜色通道。

```Python
## 将BGR图像分割为单通道
b, g, r = cv.split(img)
## 交换颜色通道（原来的 r 当成新图像的 b，原来的 b 当成新图像的 r）
img_merged = cv.merge((r, g, b))
```

## 2.3 颜色空间转换与色彩区间提取(Color Space Conversion and Color Range Masking)
OpenCV 默认读取的彩色图像格式为 BGR。在进行颜色检测和分割时，通常将其转换为 HSV（色调 Hue、饱和度 Saturation、明度 Value）空间，因为 HSV 空间更符合人类感知颜色的方式。
### 核心函数与参数
- `cv.cvtColor(src, code)`：转换图像颜色空间。
    - `code`：转换标志，例如 `cv.COLOR_BGR2HSV`、`cv.COLOR_BGR2GRAY`。
- `cv.inRange(src, lowerb, upperb)`：检查数组元素是否在指定的上下限范围内，常用于基于颜色生成二值化掩膜 (Binary Mask)。
    - `src`：输入的 HSV 图像。
    - `lowerb, upperb`：颜色范围的下界和上界（Numpy 数组格式）。如果在范围内，对应像素值设为 255（白色），否则设为 0（黑色）。

### 使用示例（基于颜色提取掩膜）

```Python
## 1. 加载图像并转换为 HSV 格式
img = cv.imread('./images/opencv-logo.png')
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
## 2. 定义红色像素点在 HSV 空间中的范围
lower = np.array([165, 50, 50])
upper = np.array([180, 255, 255])
## 3. 生成二值图像（掩膜），只保留红色区域
mask = cv.inRange(hsv, lower, upper)
## 4. 进行 And 操作进行数据合并，提取原图中的红色部分
## 仅保留 mask=255 像素的值，其他重置为 0
dst = cv.bitwise_and(img, img, mask=mask)
```

## 2.4 图像简单变换：缩放、翻转与固定旋转 Simple Transformations: Resizing, Flipping and Fixed Rotation

调用尺寸重置接口时传入的宽高元组顺序严格为宽度在前高度在后，与 NumPy 矩阵的形状顺序相反。
### 2.4.1 图像大小重置 (Image Resizing)
改变图像的宽高尺寸。在 OpenCV 中，图像形状 `shape` 通常是 `(高度, 宽度, 通道数)`，但在调用重置函数时，尺寸参数需严格按照 `(宽度, 高度)` 的顺序传递。
**核心函数与参数**`cv.resize(src, dsize[, dst[, fx[, fy[, interpolation]]]]) -> dst`
- `src`: 输入图像。
- `dsize`: 绝对尺寸，格式为 `(width, height)`。注意宽度是元组的第一个元素，高度是第二个元素。
- `dst`: 可选参数，输出目标图像。
- `fx`: 沿水平轴（宽度）的缩放系数。当 `dsize` 设为 `None` 或 `(0, 0)` 时生效。默认值为 `0`。
- `fy`: 沿垂直轴（高度）的缩放系数。默认值为 `0`。
- `interpolation`: 插值方法 (Interpolation Method)，决定了如何计算新像素值。
    - `cv.INTER_NEAREST`: 最近邻插值（速度最快，但会产生锯齿）。
    - `cv.INTER_LINEAR`: 双线性插值（默认设置，适合缩小图像）。
    - `cv.INTER_CUBIC`: 双三次插值（4x4 像素邻域，适合放大图像，质量较好）。
    - `cv.INTER_LANCZOS4`: Lanczos 插值（8x8 像素邻域，高质量但计算较慢）。

**使用示例**

```Python
## 获取旧图像的高度和宽度
old_height, old_width = img.shape[:2]
## --- 方式 1：指定绝对尺寸 ---
new_height = int(old_height * 0.8)
new_width = 250
## 注意参数顺序：宽度在前，高度在后
dst_absolute = cv.resize(img, (new_width, new_height))
## --- 方式 2：按照比例缩放 ---
## 将图像宽和高都放大 2 倍，并使用双三次插值
dst_ratio = cv.resize(img, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)
```
### 2.4.2 图像翻转 (Image Flipping)
沿着特定的坐标轴将图像进行翻转。
**核心函数与参数**`cv.flip(src, flipCode[, dst]) -> dst`
- `src`: 输入图像。
- `flipCode`: 翻转模式控制标识。
    - `0`: 沿 X 轴翻转（垂直翻转，上下颠倒）。
    - `>0`（例如 `1`）: 沿 Y 轴翻转（水平翻转，左右镜像）。
    - `<0`（例如 `1`）: 同时沿 X 轴和 Y 轴翻转（相当于旋转 180 度）。
- `dst`: 可选参数，输出图像。
**使用示例**

```Python
import cv2 as cv
## 读取图像
img = cv.imread('image.jpg')
## 水平翻转 (镜像)
img_flipped_h = cv.flip(img, 1)
## 垂直翻转
img_flipped_v = cv.flip(img, 0)
```
### 2.4.3 图像简单旋转 (Image Rotation - Direct API)
以 90 度的倍数对图像进行快速旋转。如果需要任意角度的旋转，需使用仿射变换。
**核心函数与参数**`cv.rotate(src, rotateCode[, dst]) -> dst`
- `src`: 输入图像。
- `rotateCode`: 旋转模式。
    - `cv.ROTATE_90_CLOCKWISE`: 顺时针旋转 90 度。
    - `cv.ROTATE_180`: 旋转 180 度。
    - `cv.ROTATE_90_COUNTERCLOCKWISE`: 逆时针旋转 90 度。
- `dst`: 可选参数，输出图像。
**使用示例**

```Python
## 顺时针旋转 90 度
img_rotated = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
```

## 2.5 图像仿射变换：平移与任意角度旋转 Affine Transformations: Translation and Arbitrary Rotation
平移和任意角度的旋转本质上都是基于矩阵运算的坐标系转换，可以通过构建特定的 2x3 仿射矩阵 (Affine Matrix) `M`，然后调用仿射变换函数来实现。
**核心函数与参数**`cv.warpAffine(src, M, dsize[, dst[, flags[, borderMode[, borderValue]]]]) -> dst`
- `src`: 输入图像。
- `M`: 2x3 的变换矩阵，数据类型必须是 `np.float32` 格式。
- `dsize`: 输出图像的大小 `(width, height)`。
- `dst`: 可选参数，输出图像。
- `flags`: 插值方法的组合，与 `cv.resize` 中的插值参数相同（如 `cv.INTER_LINEAR`）。
- `borderMode`: 边界像素外推模式 (Border Mode)。决定如何处理超出边界的像素（如 `cv.BORDER_CONSTANT`, `cv.BORDER_REPLICATE`）。
- `borderValue`: 边界填充值。当 `borderMode` 为 `cv.BORDER_CONSTANT` 时生效，默认为 `0`（黑色填充）。
### 2.5.1 图像平移示例

```Python
import numpy as np
h, w = img.shape[:2]
## 构建平移矩阵 M：向右平移 20 像素，向上平移 10 像素 (ty为负)
## 公式格式: [[1, 0, tx], [0, 1, ty]]
M_translate = np.float32([
    [1, 0, 20],
    [0, 1, -10]
])
## 应用平移，保持原图的宽度和高度，超出部分默认用黑色填充
dst_translate = cv.warpAffine(img, M_translate, (w, h))
```

### 2.5.2 图像任意旋转示例
除了手动编写矩阵，OpenCV 提供了 `cv.getRotationMatrix2D(center, angle, scale)` 函数来快速生成包含旋转中心和缩放因子的复杂旋转矩阵。

```Python
## --- 手动构建旋转矩阵 ---
## m11、m22控制缩放，m21、m12控制旋转
M_manual_rotate = np.float32([
    [0.8, -0.15, 0],
    [0.15,  0.8, 0]
])
dst_manual_rotate = cv.warpAffine(img, M_manual_rotate, (w, h))
## --- 使用 API 生成旋转矩阵 (推荐) ---
## 参数: (旋转中心(x, y), 旋转角度(逆时针为正), 缩放比例)
center = (w // 2, h // 2)
M_auto_rotate = cv.getRotationMatrix2D(center, 45, 0.8)
## 应用旋转，并将背景填充为白色 (255, 255, 255)
dst_auto_rotate = cv.warpAffine(img, M_auto_rotate, (w, h), borderValue=(255, 255, 255))
```

# 三、 图像算术运算与掩膜组合(Image Arithmetic and Masking)
## 3.1 图像边界扩充填充(Image Border Padding)
用于扩充图像四周像素尺寸，通常作为图像卷积滤波或两图对齐融合前的预处理步骤。
- `cv.copyMakeBorder(src, top, bottom, left, right, borderType, value)`：给图像四周添加指定宽度的边框，从而改变图像的整体尺寸。

```Python
## 给图像四周添加常量边框（如：cv.BORDER_CONSTANT）
## 原图大小如 (99, 82, 3)，添加边框后变为 (119, 102, 3)
img_border = cv.copyMakeBorder(img, 10, 10, 10, 10, cv.BORDER_CONSTANT, value=[0, 255, 0])
```

## 3.2 图像加法与加权融合(Image Addition and Weighted Blending)
参与加权叠加或直接相加的两幅图像或感兴趣区域，必须具备完全相同的宽度、高度与通道数量。
- **加权叠加**：对截取出的两块图像区域按给定权重（如 0.7 和 0.3）进行线性叠加，然后粘贴回原图。
- `cv.add(src1, src2)`：将两张同尺寸图像的像素进行合并叠加。

```Python
## 1. 图像加权融合粘贴
box = img[0:95, 20:240]        # 截取的图
box2 = img[0:95, 280:500]      # 粘贴的位置
box2 = box2 * 0.7 + box * 0.3  # 叠加融合
img[0:95, 280:500] = box2      # 粘贴回去
## 2. 图像直接相加合并
dst = cv.add(img1_bg, img2_fg)
```

## 3.3 按位逻辑运算与掩膜抠图(Bitwise Operations and Masking)
常利用二值化阈值或 HSV 色彩空间提取掩膜 (Mask)，对图像进行非矩形区域的前景与背景分离、组合及替换操作。

### 核心函数与参数
- **`cv.threshold(src, thresh, maxval, type)`**：对单通道灰度图进行阈值处理以生成二值化掩膜 (Mask)。
- **`cv.bitwise_and(src1, src2[, mask])`**：对两幅图像对应像素进行**按位与**运算。
- **`cv.bitwise_or(src1, src2[, mask])`**：对两幅图像对应像素进行**按位或**运算。
- **`cv.bitwise_xor(src1, src2[, mask])`**：对两幅图像对应像素进行**按位异或**运算（相同为 0，不同为 255）。
- **`cv.bitwise_not(src[, mask])`**：对图像进行**按位非**（求反）操作，计算公式为 $255 - \text{src}$。

#### 掩膜 (Mask) 控制机制
所有按位运算函数均支持可选参数 `mask`：
1. `mask` 必须是**单通道 8 位二值图像**（像素值仅为 0 或 255）。
2. 当传入 `mask` 时，算法**仅在 `mask` 中像素为 255（白色）的对应位置进行按位运算**；在 `mask` 为 0（黑色）的位置，输出结果直接设为 0（黑色）。

### 典型使用场景：非矩形 Logo 贴图 / 扣图组合
将带有背景的 Logo（如 `img2`）精准无缝贴入大图（如 `img1`）指定 ROI 区域的完整流程：

```python
import cv2 as cv
import numpy as np

## 1. 读取主图 (img1) 与 Logo 图 (img2)
img1 = cv.imread('./images/xiaoren.png')
img2 = cv.imread('./images/opencv-logo.png')

## 2. 确定放置位置，并在主图上截取同尺寸 ROI
rows, cols, channels = img2.shape
roi = img1[0:rows, 0:cols]

## 3. 创建 Logo 的掩膜 (Mask) 与反向掩膜 (Mask Inv)
img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

## 像素值大于 10 的区域置为 255 (白色 Logo 部分)，其余置为 0 (黑色背景部分)
ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)

## 对掩膜求反，得到黑 Logo、白背景的掩膜
mask_inv = cv.bitwise_not(mask)

## 4. 提取 ROI 中扣除 Logo 形状后的背景区域
## 仅在 mask_inv 为白色的区域保留 ROI 的原始像素，其余变黑
img1_bg = cv.bitwise_and(roi, roi, mask=mask_inv)

## 5. 提取 Logo 图中的纯前景图案
## 仅在 mask 为白色的区域保留 Logo 的原始像素，其余变黑
img2_fg = cv.bitwise_and(img2, img2, mask=mask)

## 6. 前景与背景融合，并写回主图 ROI 区域
dst = cv.add(img1_bg, img2_fg)
img1[0:rows, 0:cols] = dst

## 7. 显示最终融合结果
cv.imshow('Masking Result', img1)
cv.waitKey(0)
cv.destroyAllWindows()
```
# 四、 卷积原理与图像滤波去噪(Convolution Principles and Image Filtering)
## 4.1 卷积矩阵计算原理(Convolution Principles and Output Calculation)
在图像卷积过程中，当没有边界填充时，卷积后输出图像的宽度（或高度）可通过以下公式计算：
`W_out = floor((W_in - F) / S) + 1`
- `W_in`：输入图像的宽度（或高度）。
- `F`：方形卷积核 (Convolutional Kernel) 的宽度（或高度）。
- `S`：滑动步长 (Stride)。
- `floor`：向下取整。如果 `(W_in - F)` 不能被 `S` 整除，则向下取整会丢弃边缘的部分数据。
## 4.2 自定义卷积核滤波(Custom Kernel Filtering)
需先使用 NumPy 构建归一化的浮点型卷积核，用于自定义边缘增强或特殊平滑效果。
- `cv.filter2D(src, ddepth, kernel)`：使用自定义的卷积核对图像进行二维滤波。
    - `ddepth`：目标图像所需的深度，设为 `1` 表示输出图像与原图深度一致。
    - `kernel`：由 Numpy 构建的矩阵核。

```Python
import numpy as np
import cv2 as cv
## 构建一个简单的 5x5 平均滤波器矩阵，并归一化（除以 25）
kernel = np.ones((5, 5), np.float32) / 25
## 应用自定义滤波
dst_filter2d = cv.filter2D(img, -1, kernel)
```

## 4.3 常用内置平滑滤波 Built-in Smoothing Filters
均值与高斯滤波核大小须为奇数，中值滤波适用于去除椒盐噪声，双边滤波可在去噪同时保留清晰边缘。
### 4.3.1 常见的内置滤波函数 (Common Built-in Filtering Functions)
OpenCV 提供了多种针对不同噪点特性的内置模糊函数：
- **均值滤波 (Mean Filtering)**：`cv.blur(src, ksize)`
    取卷积核覆盖区域的像素平均值来代替中心像素。
- **高斯滤波 (Gaussian Filtering)**：`cv.GaussianBlur(src, ksize, sigmaX)`
    使用高斯核，越靠近中心的像素权重越大。`sigmaX` 是 X 方向的标准差，设为 `0` 时会根据 `ksize` 自动计算。
- **中值滤波 (Median Filtering)**：`cv.medianBlur(src, ksize)`
    取邻域内所有像素的中值。对去除孤立的椒盐噪声非常有效。
- **双边滤波 (Bilateral Filtering)**：`cv.bilateralFilter(src, d, sigmaColor, sigmaSpace)`
    能够删除中间的纹理噪声，同时**保留清晰的边缘信息**。

    - `d`：滤波时考虑的邻域直径。
    - `sigmaColor`：颜色空间的标准差，值越大颜色差异容忍度越高。
    - `sigmaSpace`：坐标空间的标准差，值越大远处像素的影响越大。

```Python
## 1. 均值滤波
dst_blur = cv.blur(img, (5, 5))
## 2. 高斯滤波 (核大小必须为奇数)
dst_gaussian = cv.GaussianBlur(img, (5, 5), 0)
## 3. 中值滤波 (ksize 直接传一个奇数整数，如 5)
dst_median = cv.medianBlur(img, 5)
## 4. 双边滤波
dst_bilateral = cv.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
```
### 4.3.2 图像平滑与高斯模糊 (Gaussian Blur)
在进行二值化之前，由于图像本身往往携带噪点 (Noise)，直接设置阈值可能会产生很多零碎的白点（黑底情况下）。因此，“图像二值化 + 高斯模糊” 是一套经典的组合拳。高斯模糊通过卷积核平滑图像，能有效消除高频噪点。
#### 核心函数与参数
- `cv.GaussianBlur(src, ksize, sigmaX)`：使用高斯滤波器对图像进行平滑处理。
    - `src`：输入图像（可以是彩色图或灰度图）。
    - `ksize`：高斯卷积核 (Kernel) 的大小。它必须是一个正的奇数元组，例如 `(3, 3)` 或 `(5, 5)`。核越大，模糊效果越明显。
    - `sigmaX`：高斯核在 X 方向的标准差。如果设置为 0，则由 `ksize.width` 自动计算得出。

#### 使用示例（高斯模糊 + 二值化 组合操作）

```Python
## 1. 读取原图并转为灰度图
img = cv.imread('./images/noisy_image.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
## 2. 对灰度图应用高斯模糊进行降噪 (使用 5x5 的卷积核)
blurred_gray = cv.GaussianBlur(gray, (5, 5), 0)
## 3. 对降噪后的平滑图像进行二值化
ret, final_binary = cv.threshold(blurred_gray, 100, 255, cv.THRESH_BINARY)
## 此时得到的 final_binary 边缘会比直接二值化更加平滑、干净
```

# 五、 阈值分割与形态学操作(Threshold Segmentation and Morphological Operations)

| **形态学操作**            | **计算公式 / 逻辑** | **主要作用与应用场景**          |
| -------------------- | ------------- | ---------------------- |
| **腐蚀 (Erode)**       | 消除边缘像素，图像缩小   | 去除较小的噪点，分离相连的物体        |
| **膨胀 (Dilate)**      | 扩张边缘像素，图像增大   | 填补物体断裂/空隙，连接相邻的物体      |
| **开运算 (Open)**       | 先腐蚀，后膨胀       | 去除外部微小噪声、毛刺，保持前景形状基本不变 |
| **闭运算 (Close)**      | 先膨胀，后腐蚀       | 填充内部微小孔洞、缝隙，连通相邻区域     |
| **形态学梯度 (Gradient)** | 膨胀图 - 腐蚀图     | 提取前景目标的边缘轮廓            |
| **礼帽 (Top Hat)**     | 原始图像 - 开运算图像  | 提取比背景亮的小细节/局部高亮区域      |
| **黑帽 (Black Hat)**   | 闭运算图像 - 原始图像  | 提取比背景暗的小细节/暗色孔洞        |
## 5.1 图像二值化分割(Image Thresholding)
输入必须为单通道灰度图像，通常建议在二值化前先进行高斯平滑滤波以消除图像高频噪点。
图像二值化是将图像上的像素点的灰度值设置为 0 或 255（即纯黑或纯白），从而使整个图像呈现出明显的黑白效果。这在边缘检测、轮廓提取和图像分割等前置预处理中极其常见。
### 核心函数与参数
- `cv.threshold(src, thresh, maxval, type)`：对单通道数组（通常是灰度图）进行固定阈值操作。
    - `src`：输入图像，必须是单通道的灰度图像。
    - `thresh`：分类的阈值。
    - `maxval`：当像素值超过（或低于，取决于具体的 type）阈值时，被赋予的最大像素值（通常设定为 255）。
    - `type`：二值化的操作类型，常用如下：
        - `cv.THRESH_BINARY`：如果像素值大于阈值，则设置为 `maxval`，否则设置为 0。
        - `cv.THRESH_BINARY_INV`：反向二值化，大于阈值设为 0，否则设为 `maxval`。
    - **返回值**：返回两个值，第一个是实际使用的阈值 `ret`，第二个是处理后的二值化图像矩阵 `dst`。

### 使用示例

```Python
## 1. 假设 img 已经读取并转化为单通道灰度图
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
## 2. 全局固定阈值二值化 (将大于 127 的像素变成 255，其余变 0)
ret, binary_img = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)
## 3. 反向二值化
ret_inv, binary_inv_img = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY_INV)
```

## 5.2 基础形态学操作：腐蚀与膨胀 Basic Morphological Operations: Erosion and Dilation
主要作用于二值化图像或灰度图像，需要预先构建 8 位无符号整型的结构元素卷积核。
- `cv.erode(src, kernel, iterations)`：**腐蚀**操作，使图像中的亮区（白色区域）缩小。用于去除小的白色噪点或断开粘连的物体。
- `cv.dilate(src, kernel, iterations)`：**膨胀**操作，使图像中的亮区扩大。可用于弥补物体内的孔洞。值得注意的是，膨胀操作中使用的核可以与腐蚀操作中的核不同。

```Python
## 定义一个 5x5 的全 1 矩阵作为核
kernel = np.ones((5, 5), np.uint8)
## 腐蚀操作 (迭代执行 3 次)
img_eroded = cv.erode(img, kernel, iterations=3)
## 膨胀操作 (迭代执行 10 次)
img_dilated = cv.dilate(img_eroded, kernel, iterations=10)
```

## 5.3 高阶形态学复合运算(Advanced Morphological Operations)
基于腐蚀与膨胀的组合计算，用于消除背景小噪点、填充内部孔洞、提取形态梯度及局部亮暗斑块。
- `cv.morphologyEx(src, op, kernel, iterations=1)`
    - `op`：具体的操作类型标识符。
        - `cv.MORPH_OPEN`：**开运算 (Opening)**（先腐蚀后膨胀），常用来消除小黑点等背景噪声。
        - `cv.MORPH_CLOSE`：**闭运算 (Closing)**（先膨胀后腐蚀），常用来填充物体内部的小黑洞。
        - `cv.MORPH_GRADIENT`：**形态梯度 (Morphological Gradient)**（膨胀图减去腐蚀图），该操作可以显示物体的边缘位置轮廓。
        - `cv.MORPH_TOPHAT`：**顶帽 / 礼帽 (Top Hat)**（原图减去开运算图），用于分离比邻近点亮的一些斑块。
        - `cv.MORPH_BLACKHAT`：**黑帽 (Black Hat)**（闭运算图减去原图），用于分离比邻近点暗的一些斑块。

```Python
## 构建核
kernel = np.ones((5, 5), np.uint8)
## 1. 开运算
img_open = cv.morphologyEx(img, op=cv.MORPH_OPEN, kernel=kernel)
## 2. 闭运算
img_close = cv.morphologyEx(img, op=cv.MORPH_CLOSE, kernel=kernel)
## 3. 形态梯度 (提取边缘)
img_gradient = cv.morphologyEx(img, op=cv.MORPH_GRADIENT, kernel=kernel)
## 4. 顶帽 (Top Hat)
img_tophat = cv.morphologyEx(img, op=cv.MORPH_TOPHAT, kernel=kernel)
## 5. 黑帽 (Black Hat)
img_blackhat = cv.morphologyEx(img, op=cv.MORPH_BLACKHAT, kernel=kernel)
```

# 六、 图像梯度与边缘检测(Image Gradients and Edge Detection)

| 对比项   | 低通滤波 (LPF)                                    | 高通滤波 (HPF)                                      |
| ----- | --------------------------------------------- | ----------------------------------------------- |
| 保留的信号 | 低频（平缓区域）                                      | 高频（突变区域）                                        |
| 削弱的信号 | 高频（边缘、噪点）                                     | 低频（纯色背景）                                        |
| 视觉效果  | 图像变模糊、变柔和                                     | 图像出现轮廓、变锐利                                      |
| 典型应用  | 去噪、磨皮、平滑图像                                    | 边缘检测、目标轮廓提取、锐化                                  |
| 核的特点  | 核内权重总和通常为 1（保持整体亮度不变）                         | 核内权重总和通常为 0（平缓区域卷积结果为零）                         |
| 常用函数  | `cv.GaussianBlur`, `cv.blur`, `cv.medianBlur` | `cv.Laplacian`, `cv.Sobel`, `cv.filter2D`（自定义核） |

## 6.1 图像微分算子与梯度计算(Differential Operators and Gradient Calculation)
输出图像深度需设定为 64 位浮点型以保留负数梯度，拉普拉斯算子对噪声敏感需先进行高斯平滑。
### 6.1.1 Sobel 算子 (Sobel Operator)
Sobel 算子结合了高斯平滑和微分运算，对抗噪声能力较强。它可以分别计算 X 方向（水平边缘）和 Y 方向（垂直边缘）的梯度。
- `cv.Sobel(src, ddepth, dx, dy, ksize)`：计算图像的 Sobel 梯度。
    - `ddepth`：输出图像深度。通常使用 `cv.CV_64F` 以保留负值梯度，后续再取绝对值转回 `uint8`。
    - `dx, dy`：求导的阶数，`dx=1, dy=0` 表示求 X 方向梯度，`dx=0, dy=1` 表示求 Y 方向梯度。
    - `ksize`：Sobel 核的大小，必须为奇数。
- `cv.convertScaleAbs(src)`：将带有负值的梯度图像取绝对值，并转换为 `uint8` 格式，以便正常显示。
- `cv.addWeighted(src1, alpha, src2, beta, gamma)`：将 X 和 Y 方向的梯度图像按权重进行线性融合。

```Python
## 1. 计算 X 方向和 Y 方向的 Sobel 梯度
sobel_x = cv.Sobel(img, cv.CV_64F, dx=1, dy=0, ksize=3)
sobel_y = cv.Sobel(img, cv.CV_64F, dx=0, dy=1, ksize=3)
## 2. 取绝对值并转换回 uint8 类型
abs_x = cv.convertScaleAbs(sobel_x)
abs_y = cv.convertScaleAbs(sobel_y)
## 3. 按 1:1 的比例融合 X 和 Y 方向的边缘信息
sobel_xy = cv.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
```

### 6.1.2 Scharr 算子 (Scharr Operator)
Scharr 算子是 Sobel 算子的优化版本。当内核较小（如 3x3）时，Sobel 算子可能不够精确，Scharr 算子提供了比 Sobel 更精确的梯度计算。
- `cv.Scharr(src, ddepth, dx, dy)`：用法与 Sobel 类似，但不需要指定 `ksize`，默认就是 3x3，且拥有更高的边缘敏感度。

```Python
## 计算 Scharr 梯度并合并
scharr_x = cv.Scharr(img, cv.CV_64F, dx=1, dy=0)
scharr_y = cv.Scharr(img, cv.CV_64F, dx=0, dy=1)
abs_scharr_x = cv.convertScaleAbs(scharr_x)
abs_scharr_y = cv.convertScaleAbs(scharr_y)
scharr_xy = cv.addWeighted(abs_scharr_x, 0.5, abs_scharr_y, 0.5, 0)
```

### 6.1.3 拉普拉斯算子 (Laplacian Operator)
Laplacian 算子基于二阶导数计算，对噪声非常敏感，因此在调用前通常需要先对图像进行高斯平滑处理。它没有 X 和 Y 的方向之分，一次性计算出全向的边缘。
- `cv.Laplacian(src, ddepth, ksize)`：计算图像的拉普拉斯二阶导数。

```Python
## 计算 Laplacian 梯度并转换格式
laplacian = cv.Laplacian(img, cv.CV_64F, ksize=3)
laplacian_abs = cv.convertScaleAbs(laplacian)
```
## 6.2 Canny 边缘检测(Canny Edge Detection)
Canny 算法是一个多阶段的边缘检测算法（融合了高斯滤波去噪、梯度计算、非极大值抑制与双阈值过滤，输入为灰度图，输出为二值化边缘图），在实际应用中最常用。输出结果为干净的二值化边缘图。
- `cv.Canny(image, threshold1, threshold2)`：执行 Canny 边缘检测。
    - `threshold1`：低阈值。梯度值低于此阈值的边缘将被丢弃。
    - `threshold2`：高阈值。梯度值高于此阈值的被保留为强边缘。位于两者之间的像素，若与强边缘相连则保留，否则丢弃。

```Python
## 先进行高斯去噪
img_blurred = cv.GaussianBlur(img_gray, (5, 5), 2)
## Canny 边缘检测（输出直接为 uint8 的二值图，边缘为 255）
edges = cv.Canny(img_blurred, threshold1=50, threshold2=250)
```

# 七、 轮廓提取、直方图与模板匹配 Contour Extraction, Histogram and Template Matching
## 7.1 轮廓查找与绘制(Contour Finding and Drawing)

查找轮廓的前提必须是黑底白字的二值图或边缘图，绘制轮廓时建议在原图的彩色副本上进行操作。

#### 核心函数与参数
- cv.findContours(image, mode, method)：寻找二值图像中的物体轮廓。
	- image：输入的二值化图像（单通道，前景为白色 255，背景为黑色 0）。
	- mode：轮廓检索模式。常用 cv.RETR_TREE（检索所有轮廓并重建嵌套层次结构）或 cv.RETR_EXTERNAL（只检索最外层轮廓）。
	- method：轮廓逼近方法。常用 cv.CHAIN_APPROX_SIMPLE（仅保留拐点/端点坐标，压缩数据节省内存）或 cv.CHAIN_APPROX_NONE（保留所有轮廓点）。
	- 返回值：contours（包含所有轮廓点集的列表 [cnt1, cnt2, ...]）和 hierarchy（轮廓层级结构）。
- cv.drawContours(image, contours, contourIdx, color, thickness)：将轮廓绘制到图像上。
	- image：绘制的目标图像（建议使用三通道彩色图像，避免覆盖原二值图）。
	- contours：由 cv.findContours 获取的轮廓点集列表。
	- contourIdx：要绘制的轮廓索引。设为 -1 表示绘制所有轮廓；指定整数 i 表示只绘制第 i 个轮廓。
	- color：绘制颜色元组 (B, G, R)。
	- thickness：线条粗细。设为正整数表示线宽，设为 -1 或 cv.FILLED 表示填充闭合轮廓内部。
- cv.contourArea(contour, oriented=False)：计算单个轮廓包围的像素面积。
	- contour：单个轮廓点集矩阵（即 contours[i]）。
	- oriented：定向区域标志。默认 False 返回绝对值面积；若为 True 则根据轮廓方向（顺时针/逆时针）返回带正负号的面积。

#### 使用示例（查找轮廓、计算面积并绘制标注）

```Python
import cv2 as cv
import numpy as np

## 1. 读取并生成二值图像（灰度化 + 阈值分割）
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
_, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

## 2. 查找轮廓
contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

## 3. 在彩色副本上绘制轮廓并标注面积
bgr_img = cv.cvtColor(binary, cv.COLOR_GRAY2BGR)
for i, cnt in enumerate(contours):
    # 计算面积
    area = cv.contourArea(cnt)

    # 绘制第 i 个轮廓（绿色，线宽 2）
    cv.drawContours(bgr_img, contours, i, (0, 255, 0), 2)

    # 获取外接矩形以定位文本显示位置
    x, y, w, h = cv.boundingRect(cnt)
    cv.putText(bgr_img, f"Area: {int(area)}", (x, y - 5),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)

cv.imshow("Contours & Area", bgr_img)
cv.waitKey(0)
cv.destroyAllWindows()
```
## 7.2 轮廓几何属性与外接边界框(Contour Properties and Bounding Boxes)
必须先通过轮廓查找获取点集，最小外接旋转矩形提取的 4 个角点需转换为 64 位整数后方可绘制。
### 7.2.1 轮廓属性特征 (Contour Properties)
获取到轮廓后，可以计算其物理或几何属性，以便进行后续的筛选判断。
- `cv.contourArea(contour)`：计算该轮廓包围的面积。
- `cv.arcLength(contour, closed)`：计算轮廓的周长。`closed` 为 `True` 表示闭合曲线。

```Python
## 取出第一个轮廓
cnt = contours[0]
## 计算面积与周长
area = cv.contourArea(cnt)
perimeter = cv.arcLength(cnt, closed=True)
```
### 7.2.3. 外接边界矩形 (Bounding Rectangles)
常用于将检测到的不规则目标框选出来。分为标准正矩形和最小外接旋转矩形。
- **直立边界矩形**：`cv.boundingRect(contour)`
    计算一个包裹轮廓的、且边平行于 X/Y 轴的最小矩形。
    返回 `(x, y, w, h)`（左上角坐标及宽高）。
- **最小外接旋转矩形**：`cv.minAreaRect(contour)`
    计算包裹轮廓的面积最小的矩形，允许发生旋转。
    返回 `rect` 元组：`((中心点x, 中心点y), (宽度, 高度), 旋转角度)`。
- `cv.boxPoints(rect)`：根据旋转矩形的 `rect` 对象，提取出矩形的 4 个角点坐标（浮点型），通常需要转换为整数型 `np.int64` 后才能用于绘制。

```Python
## --- 1. 直立外接矩形 ---
x, y, w, h = cv.boundingRect(cnt)
## 在图像上画出绿色矩形框
cv.rectangle(bgr_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
## --- 2. 最小外接旋转矩形 ---
rect = cv.minAreaRect(cnt)
## 计算出 4 个角点并转为整数
box = cv.boxPoints(rect)
box = np.int64(box)
## 绘制旋转矩形（因为有 4 个点，相当于绘制多边形轮廓）
cv.drawContours(bgr_img, [box], 0, (0, 0, 255), 2)
## 计算面积占比：真实轮廓面积 / 最小外接矩形面积
area_rect = rect[1][0] * rect[1][1]
ratio = area / area_rect if area_rect > 0 else 0
```
### 7.2.4 凸包检测与绘制(Convex Hull)
凸包是能够完全包围轮廓点集的最小凸多边形（就像用橡皮筋紧绷在物体外围形成的形状），常用于形状分析、手势识别与缺陷检测。

#### 核心函数与参数
- cv.convexHull(points[, returnPoints])：计算点集的凸包。
	* points：输入的轮廓点集（如单个轮廓 cnt）。
	* returnPoints：默认为 True，返回凸包顶点的实际坐标；若设为 False，则返回顶点在原轮廓点集中的索引。

#### 绘制方法
* 方式 1（推荐）：使用 cv.polylines(img, [hull], isClosed=True, color, thickness) 直接绘制多边形。
* 方式 2：使用 cv.drawContours(img, [hull], -1, color, thickness) 绘制。

#### 使用示例（轮廓与凸包共同绘制）
```python
import cv2 as cv

## 1. 灰度化与二值化
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

## 2. 查找轮廓
contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

## 3. 创建三通道 BGR 可视化画布
result_img = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

for i, cnt in enumerate(contours):
    # 计算面积
    area = cv.contourArea(cnt)

    # 绘制原轮廓（绿色）
    cv.drawContours(result_img, contours, i, (0, 255, 0), 2)

    # 计算并绘制凸包（红色多边形）
    hull = cv.convexHull(cnt)
    cv.polylines(result_img, [hull], isClosed=True, color=(0, 0, 255), thickness=2)

    # 标注面积文本（安全边界处理）
    x, y, w, h = cv.boundingRect(cnt)
    text_y = max(y - 10, 15)
    cv.putText(result_img, f"Area: {int(area)}", (x, text_y),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv.LINE_AA)

cv.imshow("Contours and Convex Hull", result_img)
cv.waitKey(0)
cv.destroyAllWindows()
```
## 7.3.直方图计算与均衡化(Histogram Calculation and Equalization)
直方图均衡化仅支持 8 位单通道灰度图像，主要用于自动调整图像对比度以突出细节。

- `cv.calcHist(images, channels, mask, histSize, ranges)`：计算图像的像素直方图分布。
    - `images`：输入的图像列表，如 `[img]`。
    - `channels`：需要计算直方图的通道列表。对于灰度图设为 `[0]`。
    - `mask`：掩膜 (Mask) 图像。如果只计算特定区域的直方图，需提供掩膜；计算全图则设为 `None`。
    - `histSize`：直方图分成多少个区间（即 BIN 的数目），通常设为 `[256]`。
    - `ranges`：像素值的测量范围，通常是 `[0, 256]`。
- `cv.equalizeHist(src)`：直方图均衡化 (Histogram Equalization)，能自动调整图像的对比度，使过暗或过亮的图像细节更加清晰。

```python
import cv2 as cv
import matplotlib.pyplot as plt
## 1. 计算全图的灰度直方图
hist1 = cv.calcHist([img], channels=[0], mask=None, histSize=[256], ranges=[0, 256])
## 2. 计算带掩膜 (Mask) 区域的直方图
hist2 = cv.calcHist([masked_img], channels=[0], mask=mask, histSize=[256], ranges=[0, 256])
## 绘制直方图
plt.plot(hist1, color='red')
plt.plot(hist2, color='green')
plt.show()
## 3. 直方图均衡化（输入必须是单通道灰度图）
img_equalized = cv.equalizeHist(img)
```
## 7.4 连通域标记与统计分析(Connected Components Analysis)
连通域分析常用于对二值图像中的独立连通像素块进行编号、计数及几何特征提取，相比轮廓提取能更直接获取每个连通块的面积、外接矩形与质心坐标。

### 核心函数与参数
- cv.connectedComponentsWithStats(image, connectivity, ltype)：统计并标记二值图像中的连通区域。
	- image：输入的单通道 8 位二值图像（背景 0，前景 255）。
	- connectivity：连通性，可选 4（上下左右 4 邻域）或 8（包含对角线 8 邻域，默认推荐）。
	- ltype：输出标签图像的数据类型，默认为 cv.CV_32S。
	- 返回值 (num_labels, labels, stats, centroids)：
	    - num_labels：检测到的总连通域数量（**注意：背景固定为 Label 0**）。
	    - labels：与原图等大的标记矩阵，每个像素值为其所属连通域的 ID（0, 1, 2...）。
	    - stats：`[num_labels, 5]` 维度的统计数据矩阵，包含每个连通域的信息：
	        - `stats[i, cv.CC_STAT_LEFT]`：外接矩形左上角 X 坐标
	        - `stats[i, cv.CC_STAT_TOP]`：外接矩形左上角 Y 坐标
	        - `stats[i, cv.CC_STAT_WIDTH]`：外接矩形宽度
	        - `stats[i, cv.CC_STAT_HEIGHT]`：外接矩形高度
	        - `stats[i, cv.CC_STAT_AREA]`：连通域像素面积
	    - centroids：`[num_labels, 2]` 维度的浮点型矩阵，保存每个连通域质心的 `(x, y)` 坐标。

### 使用示例

```Python
import cv2 as cv
import numpy as np

## 1. 转灰度并二值化
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
_, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

## 2. 统计连通域信息
num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(binary, connectivity=8)

## 3. 遍历每个连通域（从 1 开始，跳过背景 Label 0）
result_img = img.copy()
for i in range(1, num_labels):
    x = stats[i, cv.CC_STAT_LEFT]
    y = stats[i, cv.CC_STAT_TOP]
    w = stats[i, cv.CC_STAT_WIDTH]
    h = stats[i, cv.CC_STAT_HEIGHT]
    area = stats[i, cv.CC_STAT_AREA]
    cx, cy = centroids[i]

    # 绘制外接矩形框与红色质心点
    cv.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv.circle(result_img, (int(cx), int(cy)), 4, (0, 0, 255), -1)

    # 标注 ID 和面积
    cv.putText(result_img, f"ID:{i} Area:{area}", (x, y - 5),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv.LINE_AA)

cv.imshow("Connected Components", result_img)
cv.waitKey(0)
cv.destroyAllWindows()
```
## 7.5 模板匹配与目标定位(Template Matching and Object Location)
滑动模板计算匹配度矩阵，不同匹配算法极值含义不同，需使用最值定位接口查找极值点坐标。
- `cv.matchTemplate(image, templ, method)`：在输入图像中滑动对比并匹配模板，输出匹配度矩阵（热力图）。
    - `image`：原始目标图像。
    - `templ`：用于匹配的小模板图像。
    - `method`：匹配算法。常见如 `cv.TM_CCOEFF` 或 `cv.TM_CCORR_NORMED` 等。部分算法值越大约匹配，部分算法值越小越匹配。
- `cv.minMaxLoc(src)`：在匹配度结果矩阵中寻找全局最小值和最大值，以及它们对应的坐标点位置。

```Python
## 进行模板匹配
res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
## 寻找匹配结果中的最值和位置
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
## 由于使用的是 cv.TM_CCOEFF_NORMED，最大值代表最匹配的位置
top_left = max_loc
## 根据模板的高(h)和宽(w)计算出右下角坐标
bottom_right = (top_left[0] + w, top_left[1] + h)
## 在原图上画出匹配的矩形框
cv.rectangle(img, top_left, bottom_right, color=[0, 0, 255], thickness=5)
```

# 八、 基于 scikit-image 的传统特征提取 Traditional Feature Extraction with scikit-image
## 8.1 基础图像处理(Basic Image Processing)
与 OpenCV 类似，`scikit-image` 也能进行基本的读取和转换操作，但它的接口和返回值可能略有不同。
- `ski_io.imread(filename)`：加载图像。
- `ski_color.rgb2gray(rgb)`：将 RGB 图像转换为灰度图像。
- `ski_transform.resize(image, output_shape)`：调整图像大小。

```Python
from skimage import color as ski_color
from skimage import io as ski_io
from skimage import transform as ski_transform
## 读取、转换与改变大小
img = ski_io.imread("./images/xiaoren.png")
img_gray = ski_color.rgb2gray(img)
img_resized = ski_transform.resize(img_gray, (100, 300))
```

## 8.2 传统图像特征提取(Traditional Feature Extraction)
用于提取 HOG、LBP 及 Harris 角点特征，提取到的特征数组展平后通常直接输入机器学习模型。
提取到的特征信息通常会展平为一维数组（通过 `.reshape(-1)`），然后输入到分类模型中进行机器学习。
- `ski_feature.hog(image)`：提取方向梯度直方图 (Histogram of Oriented Gradients, HOG) 特征。常用于物体检测（如行人检测）。
- `ski_feature.local_binary_pattern(image, P, R)`：提取局部二值模式 (Local Binary Pattern, LBP) 特征。用于纹理特征提取。
    - `P`：圆形邻域中的像素点个数。
    - `R`：圆的半径。
- `ski_feature.corner_harris(image)`：提取哈里斯角点 (Harris Corner) 特征。用于检测图像中的角点变化。

```Python
from skimage import feature as ski_feature
import numpy as np
## 1. 提取 HOG 特征
hog_feature = ski_feature.hog(img_resized)
## 2. 提取 LBP 纹理特征 (需要传入 uint8 类型的图像)
img_uint8 = np.uint8(img_resized)
lbp_feature = ski_feature.local_binary_pattern(img_uint8, P=8, R=0.5).reshape(-1)
## 3. 提取 Harris 角点特征
corner_harris_feature = ski_feature.corner_harris(img_resized).reshape(-1)
```
## 8.3 霍夫变换
### 8.3.1 基础霍夫直线检测 (Standard Hough Transform)
霍夫变换是一种在图像中检测几何形状（如直线、圆）的特征提取技术。它将图像空间中的点映射到极坐标参数空间 $(\rho, \theta)$，通过累加器（Voting/Accumulator）投票寻找交点最多的极坐标参数对来识别直线。

**核心极坐标公式**
$$\rho = x \cos\theta + y \sin\theta$$
* $\rho$：原点到直线的垂直距离。
* $\theta$：原点到直线的垂线与 X 轴的夹角（弧度）。

####  核心函数与参数
- cv.HoughLines(image, rho, theta, threshold)
	* image：输入的单通道二值图像（通常是经过 Canny 边缘检测后的图像）。
	* rho：累加器的距离分辨率，单位为像素（通常设为 1）。
	* theta：累加器的角度分辨率，单位为弧度（通常设为 np.pi/180，即 1°）。
	* threshold：累加器计数阈值。只有投票数超过此值的极坐标对 $(\rho, \theta)$ 才会被认定为直线。
	* 返回值：`lines`，维度为 `[N, 1, 2]` 的矩阵，每个元素为 `[rho, theta]`。

#### 极坐标转换为直角坐标画线步骤
1. $x_0 = \rho \cos\theta, \quad y_0 = \rho \sin\theta$（得到法向基准点）
2. $x_1 = \text{int}(x_0 + 1000 \cdot (-\sin\theta)), \quad y_1 = \text{int}(y_0 + 1000 \cdot \cos\theta)$
3. $x_2 = \text{int}(x_0 - 1000 \cdot (-\sin\theta)), \quad y_2 = \text{int}(y_0 - 1000 \cdot \cos\theta)$
4. 使用 `cv.line(img, (x1, y1), (x2, y2), color, thickness)` 绘制直线。

#### 代码示例
```python
import cv2 as cv
import numpy as np

## 1. 边缘检测
edges = cv.Canny(gray_img, 50, 150)

## 2. 基础霍夫直线检测
lines = cv.HoughLines(edges, 1, np.pi / 180, 100)

## 3. 坐标转换与绘制
if lines is not None:
    for line in lines:
        rho, theta = line[0]
        a, b = np.cos(theta), np.sin(theta)
        x0, y0 = a * rho, b * rho
        x1, y1 = int(x0 + 1000 * (-b)), int(y0 + 1000 * (a))
        x2, y2 = int(x0 - 1000 * (-b)), int(y0 - 1000 * (a))
        cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
```
### 8.3.2概率霍夫直线检测 (Probabilistic Hough Transform)
概率霍夫变换是标准霍夫变换的优化版本。它通过对边缘像素进行随机抽样，仅计算一部分点来代表整张图，极大地降低了计算复杂度。同时，它能直接输出每条线段的物理端点，避免了贯穿全图的无限长直线干扰。

### 核心函数与参数
cv.HoughLinesP(image, rho, theta, threshold[, lines[, minLineLength[, maxLineGap]]])
* image：输入的单通道二值边缘图像（如 Canny 检测结果）。
* rho：累加器的距离分辨率，单位为像素（通常设为 1）。
* theta：累加器的角度分辨率，单位为弧度（通常设为 np.pi/180，即 1°）。
* threshold：累加器投票阈值。高于此值的候选线段才会被保留。
* minLineLength：线段的最短长度。小于该像素长度的线段将被过滤（默认值为 0）。
* maxLineGap：同一线上断开点之间的最大允许间隔（像素）。小于该值的两段短线将被缝合为一条长线段（默认值为 0）。
* 返回值：`lines`，维度为 `[N, 1, 4]` 的矩阵，每个元素包含线段端点 `[x1, y1, x2, y2]`。

### 基础霍夫变换 (cv.HoughLines) vs 概率霍夫变换 (cv.HoughLinesP)

| 特性 | 基础霍夫变换 (HoughLines) | 概率霍夫变换 (HoughLinesP) |
|---|---|---|
| **计算效率** | 较低（遍历所有边缘像素点） | 较高（随机抽样部分像素点） |
| **输出格式** | 极坐标 `[rho, theta]` | 端点坐标 `[x1, y1, x2, y2]` |
| **绘制效果** | 贯穿整张图像的“无限长”直线 | 紧贴物体的真实“有界”线段 |
| **参数控制** | 无法过滤短线与间断 | 可设置最小线段长度与最大融合缝隙 |

### 代码示例
```python
import cv2 as cv

## 1. 边缘检测
edges = cv.Canny(gray_img, 50, 150)

## 2. 概率霍夫线段检测
lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=10)

## 3. 直接绘制检测出的线段
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
```
