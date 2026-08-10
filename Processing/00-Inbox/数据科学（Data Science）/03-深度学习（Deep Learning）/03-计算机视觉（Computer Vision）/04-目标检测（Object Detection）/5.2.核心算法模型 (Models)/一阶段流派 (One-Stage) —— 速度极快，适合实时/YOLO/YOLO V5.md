# YOLOv5：工业落地的工程标杆 (极致灵活与推理速度)

YOLOv5（2020年）推出时虽未立即发表正式论文，但凭借其基于 **PyTorch** 框架的极致易用性、开箱即用的工程友好性，迅速成为工业界落地的首选。它不仅继承了 YOLOv4 的诸多优秀血统（如 PANet、SPP 等），更从底层架构灵活性和推理机制上做出了深刻的工业级改良。

## 一、 YOLOv5 四大核心架构特性

1. **输入端 (Input)**：Mosaic（注：YOLOv5 作者 Glen Jocher 即为马赛克增强的创造者）/ 自适应锚框计算 (Auto-Anchor) / 自适应图像缩放 (Letterbox 优化)。
2. **骨干网络 (Backbone)**：Focus 切片操作 / CSP + DarkNet 融合架构。
3. **颈部网络 (Neck)**：FPN + PAN 混合特征金字塔 / SPP 模块。
4. **检测头与输出 (Head & Prediction)**：YOLOv3 通用检测层（每层通道数为 $3 \times (\text{Class} + 1 + 4) = 255$）/ 边框回归早期采用 GIoU Loss，分类与目标得分采用**二进制交叉熵与 Logits 损失 (BCEWithLogitsLoss)**，并支持通过参数开启 **Focal Loss**。

## 二、 输入端工程黑科技

1. **自适应锚框计算 (Auto-Anchor)**：YOLOv4 必须手动运行 K-Means 脚本单独计算锚框。YOLOv5 将该功能无缝集成进训练管道，每次训练开始时，模型会自动根据当前自定义数据集的目标尺寸分布，动态学习并更新最优的 Anchor 尺寸。
![[YOLO V5-20260727113310641.png]]
2. **自适应图像缩放 (Letterbox 智能填充)**：传统等比例缩放会在长条形图像四周填充大量无意义的黑边，拖慢推理。YOLOv5 的 Letterbox 机制能自动计算最小像素损失，补齐**最少量的灰色边框**（取通道均值常数 114）。该工程优化**仅在推理预测时生效**，极大地减少了前向传播的无效计算，显著拉高了实际运行的 FPS。

## 三、 骨干网络变革：Focus 结构与模型高度可定制

1. **Focus 切片操作**：在网络开局，在一张 $416\times416\times3$ 的图像上每隔一个像素采样，切分成 4 个 $208\times208\times3$ 的低分辨率特征图，并在通道方向上 Concat 成 $208\times208\times12$ 的特征图，最后通过卷积输出。**其本质是以空间降采样换取通道升维**，在不粗暴丢失任何底层几何位置信息的前提下，极大地为后续特征提取降低了计算量。
2. **极其简洁的 YAML 缩放控制机制**：YOLOv5s、m、l、x 四种模型的网络拓扑结构完全一致，Ultralytics 仅通过配置文件中的两个全局参数控制模型的体量：
    
    - **`depth_multiple` (深度因子)**：控制 Bottleneck 结构的重复堆叠次数。例如 `v5s` 为 0.33，`v5x` 为 1.33，意味着 `v5x` 的深度是 `v5s` 的 4 倍。
    - **`width_multiple` (宽度因子)**：控制特征图卷积核的数量（通道数）。例如 `v5s` 为 0.5，`v5x` 为 1.25。
    - **效果**：这使得 YOLOv5s 模型体积压缩至惊人的 **27MB** 左右，极其利于移动端边缘部署，而超巨型网络 `v5x` 则专攻高精度上限。

## 四、 激活函数与优化器选择

- **激活函数**：为了兼顾推理速度，YOLOv5 在中间隐藏层放弃了昂贵的 Mish，改用更轻量高效的 **LeakyReLU**，最后检测层采用 **Sigmoid**。
- **优化器解耦**：预设了 **SGD** 与 **Adam**。官方建议：训练较小的自定义数据集时，选择 **Adam** 能更平滑快速地收敛；而在大规模数据集上训练时，**SGD** 的最终泛化效果和上限比 Adam 更好。

## 五、 推理效率：默认批处理推理 (Batch Inference)

在单张图（Batch Size=1）推理时，YOLOv4 约 22ms，YOLOv5s 约 20ms，差距不大。但 YOLOv5 在工程上**默认实现了批处理推理（如默认 Batch Size=36）**，通过底层并行计算并将总时间均摊，其单张图片的等效推理时间能飙升至惊人的 **7ms（即 140 FPS）**，这也是其在工业界实时检测落地中无敌的核心技术原因。

# 💡 YOLOv4 vs YOLOv5 核心对比卡片

|**维度**|**YOLOv4 方案**|**YOLOv5 升级方案**|
|---|---|---|
|**开发框架**|基于 C 语言的 Darknet（高定制化，配置略繁琐）|基于 **PyTorch**（代码极易读，工业生产极其友好）|
|**模型体积**|约 **245 MB**（深重）|**27MB** (`v5s`) ～ **367MB** (`v5x`) 可弹性缩放|
|**激活函数**|Mish 激活函数（追求精度，计算稍显昂贵）|LeakyReLU + Sigmoid（轻量高效，推理极快）|
|**训练与推理速度**|训练相对较慢；不支持默认批处理推理|训练速度飞快；**自适应 Letterbox + 默认 Batch 推理**，可达 140 FPS|
|**参数调节**|锚框需要手动 K-Means 聚类调整|**Auto-Anchor** 自动学习，`depth/width_multiple` 自由控宽窄深浅|
|**损失函数**|边界框采用 **CIoU Loss**|边界框采用 **GIoU Loss**，分类采用 **BCEWithLogitsLoss**（可选 Focal Loss）|

# 🛠️ YOLOv5 工业级全平台部署实战指南

YOLOv5 原生基于 PyTorch 编写，因此其权重格式为 `.pt`。为了将其部署到各种硬件设备（服务器、端侧设备、手机端、嵌入式），通常需要将其转换为更加通用且经过硬件加速优化的通用中间格式（如 ONNX、CoreML）。

下面是企业最常用的三种黄金部署路线：

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

## 路线一：将 `.pt` 转换为通用标准 `ONNX` 格式

无论你打算部署到哪个平台，第一步通常都是导出为 **ONNX** 格式。YOLOv5 官方仓库直接集成了 `export.py` 脚本，转换非常傻瓜化。

1. **环境准备**：
    
    Bash
    
    ```
    pip install onnx text-table coremltools tensorflow
    ```
    
2. **执行转换脚本**：
    
    Bash
    
    ```
    # 导出为标准的 ONNX 格式（包含动态 Batch 尺寸，方便后续批处理推理）
    python export.py --weights yolov5s.pt --include onnx --dynamic
    ```
    
    _运行完毕后，在同级目录下会生成一个 `yolov5s.onnx` 文件。你可以使用网页工具 **Netron** 打开它，直接可视化检查模型输入输出的通道和尺寸。_

## 路线二：高实时性服务器部署 (OpenCV DNN & TensorRT)

1. **使用 OpenCV DNN 模块直接读取推理**：
    
    如果你的后台系统使用 C++ 或 Python 且不想安装沉重的 PyTorch，ONNX 导出后可以直接用 OpenCV 原生加载：
    
    Python
    
    ```
    import cv2
    # 直接加载 ONNX 模型
    net = cv2.dnn.readNetFromONNX("yolov5s.onnx")
    
    # 构建输入 blob (按照 Letterbox 取均值 114 的思路缩放)
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (640, 640), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward() # 获得推理结果，后续再进行传统 NMS 过滤即可
    ```
    
2. **使用 TensorRT 实现英伟达 GPU 极限加速**：
    
    在需要极高 FPS 的服务器端，会将 ONNX 进一步转换为 TensorRT 的 `.engine` 文件。
    
    Bash
    
    ```
    # 使用英伟达自带的 trtexec 工具直接将 ONNX 转化为 TensorRT 引擎
    trtexec --onnx=yolov5s.onnx --saveEngine=yolov5s.engine --fp16
    ```
    
    _开启 `--fp16` 半精度量化后，YOLOv5s 的推理时延可以轻松被压低到数毫秒以内。_

## 路线三：移动端端侧部署 (Android & iOS)

由于 YOLOv5 模型的轻量性（特别是 `v5s`），极其适合在手机上做实时检测。

### 1. 部署至 iOS 苹果生态 (CoreML 路线)

通过修改 `export.py` 的参数，可以直接生成苹果原生支持的格式：

Bash

```
python export.py --weights yolov5s.pt --include coreml
```

- **部署步骤**：
    
    1. 转换后得到 `yolov5s.mlmodel` 文件。
    2. 打开 Xcode 项目，将该文件拖入项目中，Xcode 会自动为其生成 Swift / Objective-C 的调用类。
    3. 配合苹果的 `Vision` 框架，直接传入手机摄像头的 `CVPixelBuffer` 画面流，即可实现手机端硬件 NPU 加速的超流畅目标检测。

### 2. 部署至 Android 安卓生态 (ONNX -> NCNN / TFLite 路线)

对于安卓设备，通常有两条好走的路线：

- **第一条路：TFLite 路线**：
    
    Bash
    
    ```
    # 直接导出为 tensorflow lite 格式
    python export.py --weights yolov5s.pt --include tflite
    ```
    
    生成 `yolov5s.tflite` 后，直接放入 Android Studio 中，配合 Android 的 TensorFlow Lite Interpreter 库进行加载。
    
- **第二条路：腾讯 NCNN 强力加速路线（极度推荐）**：
    
    在手机端，腾讯开源的 NCNN 框架对各种手机 CPU/GPU 的汇编级优化做到了极致：
    
    1. 使用工具 `onnx2ncnn` 将生成的 `yolov5s.onnx` 转换为 NCNN 的模型描述文件 `yolov5s.param` 和权重文件 `yolov5s.bin`。
    2. 使用 NCNN 提供的 `ncnnoptimize` 工具对模型进行全网剪枝和 FP16 定点量化。
    3. 将生成的两个文件放入 Android 工程中，通过配置 NCNN 的 C++ 接口即可在各类中低端安卓手机上实现实时检测。

## ⚠️ 工业级部署避坑指南

1. **输入与输出尺寸的一致性**：在执行 `export.py` 时，务必通过 `--img` 参数指定你在训练时所使用的分辨率（如 `640` 或 `320`），确保部署推理时的输入尺寸与模型契合，否则会导致严重的精度滑坡。
2. **后处理 NMS 移出模型**：在导出移动端模型时，建议**不要**把非极大值抑制（NMS）硬编码进模型内部。由于手机端硬件对 NMS 这种密集的条件判断逻辑支持不佳，将 NMS 留在外面用 C++/Swift 原生编写，整体运行效率会大幅提升。