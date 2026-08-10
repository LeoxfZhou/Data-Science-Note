## 环境配置
## 🛠️ 第一阶段：服务器环境检查

在正式安装前，先确认你的显卡驱动和 PyTorch 环境是健康的。

```bash
# 1. 检查显卡状态和 CUDA 版本（确保你的 4080 Super 正常挂载）
nvidia-smi

# 2. 验证 PyTorch 是否能成功调用 GPU 加速
python -c "import torch; print('CUDA是否可用:', torch.cuda.is_available()); print('显卡名称:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else '无')"
```

_💡 看到输出 `CUDA是否可用: True` 和 `显卡名称: NVIDIA GeForce RTX 4080 SUPER` 就代表底层绝对健康！_

## 📦 第二阶段：核心依赖包安装

AutoDL 已经内置了主流的深度学习环境，你只需要补齐 YOLOv8 和导出部署所需的第三方包即可。

```bash
# 1. 升级 pip 到最新版本（防止某些新包因为 pip 版本过老安装失败）
python -m pip install --upgrade pip

# 2. 安装 Ultralytics（YOLOv8 官方核心库）
pip install ultralytics

# 3. 安装模型导出与部署所需的包（ONNX、ONNX 运行时、模型精简工具）
pip install onnx onnxruntime onnxslim
```

## 📂 第三阶段：工业级项目目录规范初始化

深度学习项目最忌讳文件乱放。为了配合我们之前写的模块化 Python 代码，请在你的项目根目录（例如 `/root/autodl-tmp/yolov8`）下，一键创建标准的文件夹结构：

```bash
# 切换到你的项目主目录下
cd /root/autodl-tmp/yolov8

# 一键创建标准文件夹
mkdir -p configs images datasets runs
```

### 📁 目录结构说明书

规范化后的项目目录长这样，非常清晰：

- **`configs/`**：存放官方或自定义的权重文件（如 `yolov8n.pt`）以及网络结构配置文件（`.yaml`）。
- **`images/`**：存放你用于临时测试预测的单张图片或视频（如 `bus.jpg`）。
- **`datasets/`**：存放你未来真正要大训的私有数据集（内含 `train`、`val` 文件夹及数据集映射 `yaml` 文件）。
- **`runs/`**：自动生成。所有的训练结果、评估图表、导出的 ONNX 模型都会乖乖地归类在这里。

## 📥 第四阶段：预训练权重备货

为了防止运行代码时因为网络问题导致模型下载卡死，强烈建议提前把官方的预训练权重下载并放到 `configs/` 文件夹下。

```bash
# 切换到配置文件夹
cd /root/autodl-tmp/yolov8/configs

# 使用 wget 直接从官方下载最常用的 Nano 级别权重（适合快速跑通流程）
wget https://github.com/ultralytics/assets/releases/download/v8.4.0/yolov8n.pt

# （可选）如果你以后想训大模型，可以把 Small 和 Medium 级别也顺手存下来
# wget https://github.com/ultralytics/assets/releases/download/v8.4.0/yolov8s.pt
# wget https://github.com/ultralytics/assets/releases/download/v8.4.0/yolov8m.pt

# 切回项目根目录
cd /root/autodl-tmp/yolov8
```

## 🚀 环境准备完毕！开始模块化实战

到这一步，你的服务器环境、目录结构、预训练权重已经全部处于**完全体状态**。

你只需要把之前为你整理的 4 个模块化代码文件（`1_train.py`, `2_val.py`, `3_predict.py`, `4_export.py`）放进项目根目录下，就可以在终端用最优雅的方式一行行执行了：

```bash
python 1_train.py    # 启动 GPU 训练
python 2_val.py      # 评估模型精度
python 3_predict.py  # 提取数据推理
python 4_export.py   # 导出 ONNX 部署
```

## 代码
### 🛠️ 模块一：`1_train.py`（万能模型训练模块）

**核心功能**：支持自由切换官方权重迁移学习、支持切换自定义数据集、集成了常用的训练调优超参数。

```python
# -*- coding: utf-8 -*-
from ultralytics import YOLO

def universal_train_pipeline():
    # ==========================================
    # 1. 模型初始化阶段（二选一）
    # ==========================================
    # 情况 A（最常用）：加载官方预训练权重进行迁移学习，上手快、效果好
    model = YOLO("configs/yolov8n.pt")
    
    # 情况 B（选配）：从零开始构建纯净网络结构（不含任何预训练权重），适合魔改网络或巨大数据集
    # model = YOLO("configs/yolov8n.yaml") 

    # ==========================================
    # 2. 启动训练阶段
    # ==========================================
    results = model.train(
        # ---- 必填/核心参数 ----
        data="coco8.yaml",          # 数据集配置文件（换成你自己的数据集时，改为你的自定义 xxx.yaml 路径）
        epochs=10,                  # 训练总轮数（实际大训建议 100-300 轮）
        imgsz=640,                  # 训练时输入的图片分辨率
        batch=16,                   # 批大小。4080 Super(32GB) 跑 8n 可以加大到 32 或 64
        device=0,                   # 【核心】指定GPU加速。0代表第一块显卡；如果要用CPU，改为 'cpu'
        name="yolov8n_custom",      # 实验的子文件夹名称，删除了 project 参数，YOLO会乖乖保存在 runs/detect/ 下
        
        # ---- 选配/进阶优化参数（需要时解除注释即可） ----
        workers=4,                  # 数据加载的线程数。配置越高读图越快，Windows建议0，Linux服务器建议4或8
        # optimizer="AdamW",        # 优化器选择。默认自动选择，可选: SGD, Adam, AdamW, RMSProp
        # lr0=0.01,                 # 初始学习率。默认 0.01
        # cos_lr=True,              # 启用余弦退火学习率策略，可以让训练后期收敛更平滑
        # close_mosaic=10,          # 在训练结束前最后 10 轮关闭 Mosaic 数据增强，能显著提升最终精度
        # resume=True,              # 断点续训开关。如果训练意外中断，开启此项能从上一次的 last.pt 接着练
        # amp=True,                 # 混合精度训练开关。默认开启，能省显存并加速，4080必开
    )
    
    # 动态获取并打印最终的权重保存路径，防止套娃迷路
    print("=" * 60)
    print(f"训练成功！最佳权重保存在: {results.save_dir}/weights/best.pt")
    print("=" * 60)

if __name__ == '__main__':
    universal_train_pipeline()
```

### 📊 模块二：`2_val.py`（严谨模型评估模块）

**核心功能**：在指定的验证集或测试集上跑指标，输出学术论文或汇报所需的各项核心精度数据。

```python
# -*- coding: utf-8 -*-
from ultralytics import YOLO

def universal_val_pipeline():
    # ==========================================
    # 1. 加载待评估的模型
    # ==========================================
    # 这里填入你真正练出来的最佳权重路径
    model_path = "./runs/detect/yolov8n_custom/weights/best.pt"
    model = YOLO(model_path)

    # ==========================================
    # 2. 启动评估
    # ==========================================
    metrics = model.val(
        # ---- 核心参数 ----
        data="coco8.yaml",          # 指定评估的数据集
        device=0,                   # 同样用 4080 GPU 加速评估
        split="val",                # 指定跑哪个数据集划分。可选: 'train', 'val', 'test'
        
        # ---- 选配/高级测试参数（需要时解除注释） ----
        # conf=0.25,                # 置信度过滤阈值，低于这个分数的框直接过滤，默认 0.001 跑全量指标
        # iou=0.6,                  # NMS（非极大值抑制）的 IoU 阈值
        # save_json=True,           # 是否保存 COCO 格式的 json 结果文件，方便用于其他复杂的指标评测
        # save_txt=True,            # 是否把模型预测的标签结果以 txt 格式保存下来
    )
    
    # ==========================================
    # 3. 指标优雅解析与打印
    # ==========================================
    print("\n" + "模型评估技术指标简报 ")
    print("-" * 50)
    print(f"平均精度 mAP50 (阈值0.5下的IOU精度):    {metrics.box.map50:.4f}")
    print(f"严谨精度 mAP50-95 (学术界通用主指标):  {metrics.box.map:.4f}")
    print(f"精准率 Precision (查准率):            {metrics.box.mp:.4f}")
    print(f"召回率 Recall (查全率):               {metrics.box.mr:.4f}")
    print("-" * 50)

if __name__ == '__main__':
    universal_val_pipeline()
```

### 🔮 模块三：`3_predict.py`（多功能生产环境推理模块）

**核心功能**：支持图片、视频、文件夹等多种输入源；**彻底剥离了 `cv.imshow` 等导致云服务器崩溃的 GUI 代码**，采用纯文件保存，并展示了如何安全地解包坐标用于业务开发。

```python
# -*- coding: utf-8 -*-
import os
from ultralytics import YOLO

def universal_predict_pipeline():
    # 1. 加载模型
    model = YOLO("./configs/yolov8n.pt")

    # ==========================================
    # 输入源切换（多选一，修改这里的 source 变量即可）
    # ==========================================
    source_img = "./images/bus.jpg"          # 单张图片
    # source_folder = "./images"             # 整个文件夹的图片
    # source_video = "./images/test.mp4"     # 视频文件

    # 2. 执行模型推理
    results = model(
        source=source_img, 
        device=0,                            # 使用GPU推理
        
        # ---- 常用选配预测控制 ----
        conf=0.25,                           # 置信度阈值，过滤掉低分数的无用预测
        # iou=0.45,                          # 重叠框过滤阈值
        # save_txt=False,                    # 是否把检测到的框坐标存为独立txt文本
        # save_crop=False,                   # 是否把检测到的物体从原图里裁剪下来并分类保存
    )

    # 3. 逐张图解析结果（适应单图或多图批处理）
    for i, result in enumerate(results):
        # 3.1 安全保存画好框的可视化成品图到硬盘
        out_name = f"./images/predict_result_{i}.jpg"
        result.save(filename=out_name)
        print(f"第 {i+1} 张图的检测效果图已安全存入: {out_name}")

        # 3.2 提取具体的数值，供二次业务开发使用
        boxes = result.boxes
        if len(boxes) == 0:
            print("未在此图像中检测到任何目标。")
            continue
            
        print(f"\n --- 第 {i+1} 张图的业务解析数据 ---")
        # 转换为列表形式，方便 Python 逻辑处理
        labels = boxes.cls.tolist()          # 类别ID
        scores = boxes.conf.tolist()         # 置信度分数
        
        # 打印当前图里检测到了什么
        for idx, (lbl, scr) in enumerate(zip(labels, scores)):
            # result.names 是模型内置的 ID 到名称的映射字典
            class_name = result.names[int(lbl)]
            print(f" ➔ 目标 [{idx}]: 类别={class_name} (ID={int(lbl)}), 置信度={scr:.2%}")

        # 绝对像素坐标矩阵 xyxy (每一行代表一个物体: x_min, y_min, x_max, y_max)
        print(f" ➔ 边界框绝对像素坐标矩阵 (Tensor):\n{boxes.xyxy}\n")

if __name__ == '__main__':
    universal_predict_pipeline()
```

### 📦 模块四：`4_export.py`（端侧部署与模型转换模块）

**核心功能**：剥离 PyTorch 的动态运行环境，将网络固化为速度更快的静态推理引擎格式，为 C++ 部署或前端部署做准备。

```python
# -*- coding: utf-8 -*-
from ultralytics import YOLO

def universal_export_pipeline():
    # 1. 加载要导出的 PyTorch 模型权重
    model = YOLO("./configs/yolov8n.pt")

    # ==========================================
    # 2. 启动模型格式导出
    # ==========================================
    success_path = model.export(
        # ---- 核心目标格式（切换此处即可转换不同格式） ----
        format="onnx",        # 最通用的格式。可选: 'onnx', 'engine'(TensorRT), 'tflite', 'ncnn'
        
        # ---- 选配/性能优化控制 ----
        imgsz=640,            # 固定的输入分辨率[cite: 8]
        dynamic=True,         # 开启动态 Batch Size 和尺寸支持，部署时输入尺寸更灵活
        simplify=True,        # 【强烈推荐】开启 ONNX 算子融合与消除，精简网络以提升推理速度
        opset=12,             # 指定 ONNX 算子集版本，12 或 13 兼容性最佳[cite: 8]
        
        # half=True,          # 导出为 FP16 半精度（仅部分格式如 TensorRT/CoreML 支持，能减小一半体积）
    )
    
    print("\n" + "模型格式转换圆满成功！ ")
    print("-" * 50)
    print(f"转换后的静态部署文件保存在: {success_path}")
    print("提示：你可以将该文件下载至本地，使用 https://netron.app 网站可视化查看网络结构。")
    print("-" * 50)

if __name__ == '__main__':
    universal_export_pipeline()
```

## yaml文件
### 🛠️ 第一步：检查你的文件夹结构

请双击点开你的 `images` 和 `labels` 文件夹，确认它们的内部结构是否符合 YOLOv8 的工业标准：

```Plaintext
datasets/coco8/
├── images/
│   ├── train/  （放训练集的图片，比如 001.jpg, 002.jpg）
│   └── val/    （放验证集的图片，比如 003.jpg）
└── labels/
    ├── train/  （放训练集的标签 txt，名字必须和 images/train 下的图片一一对应）
    └── val/    （放验证集的标签 txt，名字必须和 images/val 下的图片一一对应）
```

> **💡 注意**：如果你的 `images` 内部直接就是图片，没有分 `train` 和 `val` 文件夹，请在 `images` 和 `labels` 内部各自新建 `train` 和 `val` 文件夹，然后把图片和对应的 txt 标签按一定比例（比如 8:2）分别放进去。

### 📝 第二步：手写你的专属 `my_dataset.yaml`

1. 在你的项目根目录下（或者任意你喜欢的地方，比如 `datasets/` 文件夹下），右键选择 **New File（新建文件）**。
2. 命名为 **`my_dataset.yaml`**。
3. 把下面这段标准的配置模板复制进去，并根据你的实际情况修改：

```YAML
# 1. 填入你数据集的绝对根路径（AutoDL 上的路径）
path: /root/autodl-tmp/yolov8/datasets/coco8

# 2. 填入训练集和验证集图片相对于上面 path 的相对路径
train: images/train
val: images/val

# 3. 目标检测的类别映射字典（【核心】根据你自己的数据集来改）
names:
  0: person       # 如果你的标签里 0 代表人
  1: bicycle      # 1 代表自行车
  2: car          # 2 代表汽车
  # ... 有几个类别就往下写几个，注意冒号后面要有一个空格
```

### 🚀 第三步：在模块化代码中替换使用

建好这个文件后，回到你的 `1_train.py` 脚本里，把 `data` 参数直接换成你刚刚写好的这个 `.yaml` 文件的路径即可：

```Python
results = model.train(
    data="my_dataset.yaml",  # 换成你刚才新建的文件名（如果不在根目录，写相对路径如 datasets/my_dataset.yaml）
    epochs=10,
    imgsz=640,
    batch=16,
    device=0,
    name="yolov8n_my_data"
)
```

###  学习与实战建议

这四个文件创建完毕后，你手头就握有一套**标准化、工业级**的目标检测流水线了。

- **第一步**：以后老师给你任何图像检测任务，你只需要编写或修改一个 `dataset.yaml` 配置文件，指明图片路径，直接运行 `1_train.py` 即可开训。
- **第二步**：训练结束后，用 `2_val.py` 评估论文指标。
- **第三步**：如果做演示系统（比如搞个网页界面或者报警器），在后端脚本里引入 `3_predict.py` 的解析逻辑。
    
