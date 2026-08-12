---
title: YOLOv5 架构、训练与部署边界（YOLOv5 Architecture, Training, and Deployment）
tags:
  - data-science/deep-learning/computer-vision/object-detection/yolov5
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# YOLOv5 架构、训练与部署边界（YOLOv5 Architecture, Training, and Deployment）

YOLOv5（2020年）推出时虽未立即发表正式论文，但凭借其基于 **PyTorch** 框架的极致易用性、开箱即用的工程友好性，迅速成为工业界落地的首选。它不仅继承了 YOLOv4 的诸多优秀血统（如 PANet、SPP 等），更从底层架构灵活性和推理机制上做出了深刻的工业级改良。

## 一、 YOLOv5 四大核心架构特性

1. **输入端 (Input)**：Mosaic、自适应锚框计算（AutoAnchor）、Letterbox 与其他数据增强；Mosaic 在 YOLOv5 之前已由 YOLOv4 论文公开采用，不能归为 YOLOv5 作者独创。
2. **骨干网络 (Backbone)**：CSP/C3 体系；早期版本使用 Focus，YOLOv5 v6.0 起把 Focus 替换为等效的 `6×6`、步长 2 卷积。
3. **颈部网络 (Neck)**：FPN + PAN 路径与空间金字塔池化；v6.0 起用更快的 SPPF 替代 SPP。
4. **检测头与输出 (Head & Prediction)**：YOLOv3 通用检测层（每层通道数为 $3 \times (\text{Class} + 1 + 4) = 255$）/ 边框回归早期采用 GIoU Loss，分类与目标得分采用**二进制交叉熵与 Logits 损失 (BCEWithLogitsLoss)**，并支持通过参数开启 **Focal Loss**。

## 二、 输入端工程黑科技

1. **自适应锚框计算 (Auto-Anchor)**：YOLOv4 必须手动运行 K-Means 脚本单独计算锚框。YOLOv5 将该功能无缝集成进训练管道，每次训练开始时，模型会自动根据当前自定义数据集的目标尺寸分布，动态学习并更新最优的 Anchor 尺寸。
![[09-YOLOv5 架构、训练与部署边界（YOLOv5 Architecture, Training, and Deployment）-20260727113310641.png]]
2. **Letterbox 等比例缩放与填充 (Letterbox Resize and Padding)**：保持长宽比缩放，再以常数 114 填充到模型步长兼容的尺寸。训练加载器和推理预处理都可能使用 Letterbox；推理时的 `auto` 最小矩形策略是否启用取决于 API、批处理形状与导出方式，并非“只在推理生效”。
> [!tip] 大白话理解（Plain-language Intuition）
> 直接把长图拉成正方形会把目标压扁；Letterbox 像按比例缩放照片后给空白处加边框。这样几何不变形，但部署端必须使用与训练/验证一致的缩放和坐标还原规则。

## 三、 骨干网络变革：Focus 结构与模型高度可定制

1. **早期 Focus 切片操作**：输入按奇偶行列切成 4 组并沿通道拼接，相当于空间到深度（Space-to-depth）重排后卷积。它不直接丢像素，但后续卷积仍会压缩信息。YOLOv5 v6.0/6.1 已用 `6×6 Conv2d` 替代 Focus，速度与部署兼容性更好。
2. **极其简洁的 YAML 缩放控制机制**：YOLOv5s、m、l、x 四种模型的网络拓扑结构完全一致，Ultralytics 仅通过配置文件中的两个全局参数控制模型的体量：
    
    - **`depth_multiple` (深度因子)**：控制 Bottleneck 结构的重复堆叠次数。例如 `v5s` 为 0.33，`v5x` 为 1.33，意味着 `v5x` 的深度是 `v5s` 的 4 倍。
    - **`width_multiple` (宽度因子)**：控制特征图卷积核的数量（通道数）。例如 `v5s` 为 0.5，`v5x` 为 1.25。
    - **效果**：这使得 YOLOv5s 模型体积压缩至惊人的 **27MB** 左右，极其利于移动端边缘部署，而超巨型网络 `v5x` 则专攻高精度上限。

## 四、 激活函数与训练策略

- **激活函数（Activation）**：YOLOv5 早期配置曾使用 Leaky ReLU，后续主流版本使用 SiLU；检测输出再按分支应用 Sigmoid。必须结合仓库 tag 与模型 YAML 判断，不能统一写成 Leaky ReLU。
- **优化器（Optimizer）**：仓库支持 SGD、Adam、AdamW 等，默认和 `--optimizer` 选项随版本变化。小数据集不等于 Adam 必然更好，大数据集也不保证 SGD 必然达到更高上限；应固定数据划分并比较验证指标、收敛与资源成本。
- **其他策略（Other Strategies）**：多尺度训练、预热（Warmup）、学习率调度、指数移动平均（Exponential Moving Average, EMA）、自动混合精度（Automatic Mixed Precision, AMP）和超参数演化共同影响结果。

## 五、 推理效率：默认批处理推理 (Batch Inference)

在单张图（Batch Size=1）推理时，YOLOv4 约 22ms，YOLOv5s 约 20ms，差距不大。但 YOLOv5 在工程上**默认实现了批处理推理（如默认 Batch Size=36）**，通过底层并行计算并将总时间均摊，其单张图片的等效推理时间能飙升至惊人的 **7ms（即 140 FPS）**，这也是其在工业界实时检测落地中无敌的核心技术原因。

## 五、 YOLOv4 与 YOLOv5 对比（YOLOv4 vs YOLOv5）

|**维度**|**YOLOv4 方案**|**YOLOv5 升级方案**|
|---|---|---|
|**开发框架**|基于 C 语言的 Darknet（高定制化，配置略繁琐）|基于 **PyTorch**（代码极易读，工业生产极其友好）|
|**模型体积**|约 **245 MB**（深重）|**27MB** (`v5s`) ～ **367MB** (`v5x`) 可弹性缩放|
|**激活函数**|主干 Mish，其他部分按配置|早期 Leaky ReLU，后续主流 SiLU；输出分支使用 Sigmoid|
|**训练与推理速度**|取决于 Darknet 配置、硬件和输入|取决于 tag、模型尺度、硬件、批大小与输入；不保留无协议 FPS|
|**参数调节**|锚框需要手动 K-Means 聚类调整|**Auto-Anchor** 自动学习，`depth/width_multiple` 自由控宽窄深浅|
|**损失函数**|边界框采用 CIoU Loss|历史版本发生过变化；主流版本使用 CIoU 类边框损失，分类与目标性使用 BCE，可按版本配置 Focal Loss|

## 六、 YOLOv5 跨平台部署流程（Cross-platform Deployment）

YOLOv5 原生基于 PyTorch 编写，因此其权重格式为 `.pt`。为了将其部署到各种硬件设备（服务器、端侧设备、手机端、嵌入式），通常需要将其转换为更加通用且经过硬件加速优化的通用中间格式（如 ONNX、CoreML）。

常见部署路线如下：

```
                         ┌──────────────┐
                         │ YOLOv5 (.pt) │
                         └──────┬───────┘
                                │
                      export.py │ (模型转换)
                                ▼
                         ┌──────────────┐
                         │  ONNX 模型   │
                         └─┬──────────┬─┘
                           │          │
    ┌──────────────────────┘          └──────────────────────┐
    ▼                                                        ▼
【服务器/边缘端加速】                                     【移动端端侧部署】
 1. ONNX Runtime 推理                                     1. 转换为 CoreML -> iOS 部署
 2. 转换为 TensorRT -> 英伟达 GPU 部署                    2. 转换为 NCNN/TFLite -> Android 部署
 3. OpenCV DNN 模块直接读取
```

### 6.1 将 `.pt` 导出为 ONNX

无论你打算部署到哪个平台，第一步通常都是导出为 **ONNX** 格式。YOLOv5 官方仓库直接集成了 `export.py` 脚本，转换非常傻瓜化。

1. **环境准备**：
    
    ```bash
    pip install onnx text-table coremltools tensorflow
    ```
    
2. **执行转换脚本**：
    
    ```bash
    # 导出为标准的 ONNX 格式（包含动态 Batch 尺寸，方便后续批处理推理）
    python export.py --weights yolov5s.pt --include onnx --dynamic
    ```
    
    _运行完毕后，在同级目录下会生成一个 `yolov5s.onnx` 文件。你可以使用网页工具 **Netron** 打开它，直接可视化检查模型输入输出的通道和尺寸。_

### 6.2 服务器部署（OpenCV DNN and TensorRT）

1. **使用 OpenCV DNN 模块直接读取推理**：
    
    如果你的后台系统使用 C++ 或 Python 且不想安装沉重的 PyTorch，ONNX 导出后可以直接用 OpenCV 原生加载：
    
```python
from pathlib import Path

import cv2

model_path = Path("yolov5s.onnx")
image_path = Path("example.jpg")
if not model_path.is_file() or not image_path.is_file():
    raise FileNotFoundError("请先准备 ONNX 模型和输入图片")

net = cv2.dnn.readNetFromONNX(str(model_path))
image = cv2.imread(str(image_path))
if image is None:
    raise ValueError(f"OpenCV 无法解码图片: {image_path}")

# 这里只演示固定缩放与前向传播。生产部署应复用训练一致的 Letterbox，
# 并根据当前导出版本的输出契约完成解码、坐标还原和 NMS。
blob = cv2.dnn.blobFromImage(
    image,
    scalefactor=1 / 255.0,
    size=(640, 640),
    swapRB=True,
    crop=False,
)
net.setInput(blob)
outputs = net.forward()
print(type(outputs), getattr(outputs, "shape", None))
# 输出形状依 YOLOv5 tag、类别数和导出选项而变，不能写死。
```
    
2. **使用 TensorRT 实现英伟达 GPU 极限加速**：
    
    在需要极高 FPS 的服务器端，会将 ONNX 进一步转换为 TensorRT 的 `.engine` 文件。
    
    ```bash
    # 使用英伟达自带的 trtexec 工具直接将 ONNX 转化为 TensorRT 引擎
    trtexec --onnx=yolov5s.onnx --saveEngine=yolov5s.engine --fp16
    ```
    
    `--fp16` 使用半精度浮点构建引擎；能否降低延迟以及误差大小由目标 GPU、TensorRT 版本和算子决定，必须实测。

### 6.3 移动端部署（Android and iOS）

由于 YOLOv5 模型的轻量性（特别是 `v5s`），极其适合在手机上做实时检测。
### 1. 部署至 iOS 苹果生态 (CoreML 路线)

通过修改 `export.py` 的参数，可以直接生成苹果原生支持的格式：

```bash
python export.py --weights yolov5s.pt --include coreml
```

- **部署步骤**：
    
    1. 转换后得到 `yolov5s.mlmodel` 文件。
    2. 打开 Xcode 项目，将该文件拖入项目中，Xcode 会自动为其生成 Swift / Objective-C 的调用类。
    3. 配合苹果的 `Vision` 框架，直接传入手机摄像头的 `CVPixelBuffer` 画面流，即可实现手机端硬件 NPU 加速的超流畅目标检测。
### 2. 部署至 Android 安卓生态 (ONNX -> NCNN / TFLite 路线)

对于安卓设备，通常有两条好走的路线：

- **第一条路：TFLite 路线**：
    
    ```bash
    # 直接导出为 tensorflow lite 格式
    python export.py --weights yolov5s.pt --include tflite
    ```
    
    生成 `yolov5s.tflite` 后，直接放入 Android Studio 中，配合 Android 的 TensorFlow Lite Interpreter 库进行加载。
    
- **第二条路：腾讯 NCNN 强力加速路线（极度推荐）**：
    
    NCNN 为移动端 CPU/GPU 提供优化算子；是否优于 TFLite、CoreML 或 ONNX Runtime Mobile 必须在目标设备实测：
    
    1. 使用工具 `onnx2ncnn` 将生成的 `yolov5s.onnx` 转换为 NCNN 的模型描述文件 `yolov5s.param` 和权重文件 `yolov5s.bin`。
    2. 使用 `ncnnoptimize` 做图优化与存储精度转换；FP16 是半精度浮点，不是定点量化，也不能把该步骤称为“全网剪枝”。
    3. 将生成的两个文件放入 Android 工程中，通过配置 NCNN 的 C++ 接口即可在各类中低端安卓手机上实现实时检测。

## 七、 部署边界与排错（Deployment Boundaries and Troubleshooting）

1. **输入契约（Input Contract）**：导出尺寸不必机械等于训练中唯一尺寸，但预处理、步长、归一化、颜色通道、动态轴与坐标还原必须匹配导出图契约。固定尺寸通常更利于端侧优化，动态尺寸更灵活但并非所有后端都高效支持。
2. **输出契约（Output Contract）**：确认输出是原始检测头、已解码框还是含 NMS 的最终检测；不能在已有 NMS 时再次 NMS，也不能漏掉解码。
3. **NMS 放置（NMS Placement）**：图内 NMS 便于封装，图外 NMS 便于跨后端替换和调优；性能优劣取决于后端是否提供高效 NMS 算子，不能一律断言图外更快。
4. **数值精度（Numerical Precision）**：FP16、INT8 会改变速度、内存和精度；INT8 需要代表性校准数据，且应逐类验证 AP 与小目标召回率。
5. **版本固定（Version Pinning）**：保存 YOLOv5 commit/tag、PyTorch、ONNX opset 和部署后端版本；仅保存 `.pt` 不足以保证可复现。
## 八、 参考资料（References）
- [Ultralytics YOLOv5 Architecture](https://docs.ultralytics.com/yolov5/tutorials/architecture-description/)
- [ultralytics/yolov5](https://github.com/ultralytics/yolov5)
