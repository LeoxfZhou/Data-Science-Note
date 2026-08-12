---
title: YOLOv8 自定义目标检测项目模板（YOLOv8 Custom Detection Project Template）
tags:
  - data-science/deep-learning/templates/yolov8
  - data-science/deep-learning/computer-vision/object-detection
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# YOLOv8 自定义目标检测项目模板（YOLOv8 Custom Detection Project Template）
## 1. 模板目标与适用范围（Goal and Scope）
这份模板用于快速建立 YOLOv8 自定义目标检测项目。第一次使用只需准备数据集 YAML、选择预训练权重、指定推理来源，即可依次训练、验证、推理或导出；熟悉后再打开可选参数。
- **适用任务（Applicable Task）**：轴对齐边界框目标检测（Object Detection）。
- **适用流程（Workflow）**：迁移学习微调、独立验证、图片/文件夹/视频推理、ONNX/TensorRT/其他官方支持格式导出。
- **不直接覆盖（Not Covered Directly）**：实例分割、姿态估计、旋转框、跟踪与生产服务 API；这些任务的结果对象和指标不同，应派生独立模板。
- **核心原则（Core Principle）**：最小路径先跑通，再一次只改变一组参数，并记录版本、数据划分与输出目录。
## 2. 三分钟最小入口（Three-minute Minimal Entry）
### 2.1 安装与环境检查（Installation and Environment Check）
创建独立虚拟环境后安装依赖。可复现项目应把实际成功版本写进 lock file；下面的范围表达 API 家族，不承诺任意组合都兼容。
```bash
python -m pip install --upgrade pip
python -m pip install "ultralytics>=8.2,<9" torch torchvision
python -c "import torch, ultralytics; print('ultralytics:', ultralytics.__version__); print('CUDA:', torch.cuda.is_available())"
# 代表性输出（具体版本与 CUDA 状态依环境而变）：
# ultralytics: 8.x.x
# CUDA: True
```
> [!warning] 依赖匹配（Dependency Compatibility）
> 不要只凭 CUDA Toolkit 版本安装 PyTorch。驱动、PyTorch wheel 所带 CUDA runtime、操作系统和 GPU 架构需要匹配；优先使用 PyTorch 官方安装选择器生成命令。
### 2.2 只改三个路径（Change Only Three Paths）
```python
from pathlib import Path

from ultralytics import YOLO

# 1. 数据集 YAML：告诉框架训练/验证图片在哪里、有哪些类别。
DATA_YAML = Path("datasets/my_dataset.yaml")
# 2. 预训练权重：`n` 最轻，适合先验证流程；确认无误后再换 s/m/l/x。
WEIGHTS = Path("weights/yolov8n.pt")
# 3. 推理来源：可换成图片、目录、视频或摄像头索引 0。
SOURCE = Path("images/example.jpg")

if not DATA_YAML.is_file():
    raise FileNotFoundError(f"数据集配置不存在: {DATA_YAML.resolve()}")
if not WEIGHTS.is_file():
    raise FileNotFoundError(f"模型权重不存在: {WEIGHTS.resolve()}")

model = YOLO(str(WEIGHTS))

# 最小 smoke test 先训练 1 个 epoch；确认数据与环境无误后再增大 epochs。
train_result = model.train(
    data=str(DATA_YAML),
    epochs=1,
    imgsz=640,
    batch=-1,       # 自动估算约 60% GPU 显存；不支持时改为明确整数，例如 8。
    device=None,    # 让 Ultralytics 自动选择；需要固定 GPU 时改为 0。
    project="runs/detect",
    name="smoke_test",
    exist_ok=False, # 避免无意覆盖同名实验；重跑时换 name。
)

best_weight = Path(train_result.save_dir) / "weights" / "best.pt"
if not best_weight.is_file():
    raise FileNotFoundError(f"训练结束但未找到 best.pt: {best_weight}")

best_model = YOLO(str(best_weight))
metrics = best_model.val(data=str(DATA_YAML), split="val")
print(f"mAP50: {metrics.box.map50:.4f}")
print(f"mAP50-95: {metrics.box.map:.4f}")

# `save=True` 会写文件，输出目录由 project/name 控制；这是外部副作用示例。
best_model.predict(
    source=str(SOURCE),
    conf=0.25,
    iou=0.45,
    save=True,
    project="runs/detect",
    name="smoke_predict",
    exist_ok=False,
)
```
> [!tip] 大白话理解（Plain-language Intuition）
> 先用最小模型和 1 个 epoch 检查“图片能读、标签能配、GPU 能跑、结果能保存”。这一关失败时，跑 100 个 epoch 只会更晚发现问题。
## 3. 推荐项目结构（Recommended Project Layout）
```text
yolov8_project/
├── datasets/
│   ├── my_dataset.yaml
│   └── my_dataset/
│       ├── images/
│       │   ├── train/
│       │   ├── val/
│       │   └── test/             # 可选
│       └── labels/
│           ├── train/
│           ├── val/
│           └── test/             # 可选
├── images/                        # 临时推理输入
├── weights/                       # 初始权重或手工选定权重
├── runs/                          # 训练、验证、预测输出；通常不提交大权重
├── yolo_project.py                # 下文完整入口
└── requirements-lock.txt          # 记录实际验证成功的精确版本
```
- 图片与标签基名必须一致，例如 `images/train/001.jpg` 对应 `labels/train/001.txt`。
- `runs/` 由框架生成；不要把训练输出和输入数据混在同一目录。
- 权重可能很大，上传 GitHub 前使用 Git LFS 或忽略规则，并确认许可证与隐私范围。
## 4. 数据集配置与标签契约（Dataset and Label Contract）
### 4.1 `my_dataset.yaml`
```yaml
# 相对路径的解析行为可能受 Ultralytics 版本与运行目录影响；稳定项目可使用绝对路径。
path: /absolute/path/to/yolov8_project/datasets/my_dataset
train: images/train
val: images/val
test: images/test  # 可选；没有测试集时删除本行。

# 键必须与标签文件中的 class_id 对应，并从 0 连续编号。
names:
  0: license_plate
  1: flower
  2: defect
```
上面的 `names` 数量即检测类别数；无需为了旧版示例重复添加 `nc`，若所用版本或外部工具明确要求，再保证 `nc` 与 `names` 长度一致。
### 4.2 YOLO 检测标签（YOLO Detection Label）
每个目标占一行：
```text
<class_id> <x_center> <y_center> <width> <height>
```
- `x_center`、`y_center`、`width`、`height` 均相对原图宽高归一化到 `[0,1]`。
- 空场景图片可以没有对应标签文件或使用空文件；具体数据加载行为要用当前版本做 smoke test。
- 坐标越界、负宽高、未知类别、图片与标签缺配会造成训练错误或静默污染指标。
- VOC XML、COCO JSON 和 LabelMe JSON 不能直接冒充 YOLO TXT；转换后应抽样可视化框，而不是只检查文件是否生成。
### 4.3 划分数据集时防止泄漏（Prevent Data Leakage）
- 同一视频的相邻帧、同一患者/设备/场景的高度相似样本应按组划分，避免训练与验证近重复。
- 类别分布、目标尺寸与场景分布应在 train/val/test 间合理覆盖。
- 增强后的派生图片应与其原图处于同一划分。
## 5. 完整单文件模板（Complete Single-file Template）
下面的 `yolo_project.py` 用一个配置类和四个模式完成训练、验证、推理和导出。默认值偏安全：不覆盖已有实验、不自动多卡、不静默退回全新训练。
```python
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
from ultralytics import YOLO


@dataclass(frozen=True)
class ProjectConfig:
    """集中保存会影响实验语义的路径和参数，避免散落在四个函数中。"""

    data_yaml: Path = Path("datasets/my_dataset.yaml")
    pretrained_weights: Path = Path("weights/yolov8n.pt")
    deploy_weights: Path = Path("runs/detect/experiment/weights/best.pt")
    source: str = "images/example.jpg"
    project: Path = Path("runs/detect")
    run_name: str = "experiment"

    epochs: int = 100
    imgsz: int = 640
    batch: int | float = -1
    val_batch: int = 16
    device: int | str | list[int] | None = None
    workers: int = 4
    patience: int = 20

    conf: float = 0.25
    nms_iou: float = 0.45
    export_format: str = "onnx"


CFG = ProjectConfig()


def require_file(path: Path, purpose: str) -> Path:
    """尽早报告准确路径，避免框架在深层调用中给出难定位的报错。"""
    if not path.is_file():
        raise FileNotFoundError(f"{purpose}不存在: {path.resolve()}")
    return path


def require_exists(path: Path, purpose: str) -> Path:
    """导出结果可能是单文件或目录，因此这里只要求路径存在。"""
    if not path.exists():
        raise FileNotFoundError(f"{purpose}不存在: {path.resolve()}")
    return path


def describe_environment() -> None:
    """打印设备事实，不自行把所有 GPU 组成多卡任务。"""
    print(f"PyTorch: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Visible GPUs: {torch.cuda.device_count()}")
        for index in range(torch.cuda.device_count()):
            print(f"  GPU {index}: {torch.cuda.get_device_name(index)}")


def train(*, resume_from: Path | None = None) -> Path:
    """训练并返回最佳权重路径；恢复训练与新实验使用不同入口。"""
    require_file(CFG.data_yaml, "数据集 YAML")

    if resume_from is not None:
        # 恢复必须加载 last.pt；checkpoint 内含优化器、epoch 等状态。
        # 如果找不到断点，直接失败比静默改成新实验更可复现。
        checkpoint = require_file(resume_from, "断点权重")
        model = YOLO(str(checkpoint))
        result = model.train(resume=True)
    else:
        weights = require_file(CFG.pretrained_weights, "预训练权重")
        model = YOLO(str(weights))
        result = model.train(
            data=str(CFG.data_yaml),
            epochs=CFG.epochs,
            imgsz=CFG.imgsz,
            batch=CFG.batch,
            device=CFG.device,
            workers=CFG.workers,
            patience=CFG.patience,
            project=str(CFG.project),
            name=CFG.run_name,
            exist_ok=False, # False 防止同名目录被复用；新实验应更换 run_name。
            plots=True,
            amp=True,       # 可选：GPU 常能省显存/提速；出现数值问题时对比关闭后的结果。
            # freeze=10,    # 可选：极小数据集可冻结前 N 层；代价是领域差异大时适应不足。
            # cos_lr=True,  # 可选：余弦学习率；适合完整训练，不保证短 smoke test 更好。
            # close_mosaic=10, # 可选：末尾关闭 Mosaic，让最终阶段贴近自然图像分布。
        )

    best = Path(result.save_dir) / "weights" / "best.pt"
    return require_file(best, "训练生成的最佳权重")


def validate(weights: Path | None = None) -> dict[str, Any]:
    """在固定划分上验证，返回便于日志或 API 使用的普通字典。"""
    model_path = require_file(weights or CFG.deploy_weights, "待验证权重")
    require_file(CFG.data_yaml, "数据集 YAML")
    model = YOLO(str(model_path))
    metrics = model.val(
        data=str(CFG.data_yaml),
        split="val",
        imgsz=CFG.imgsz,
        batch=CFG.val_batch,
        device=CFG.device,
        project=str(CFG.project),
        name=f"{CFG.run_name}_val",
        exist_ok=False,
        plots=True,
        # conf=0.001, # 可选：评估通常需要低阈值扫完整 PR 曲线，不要照搬推理阈值 0.25。
        # save_json=True, # 可选：COCO 协议或外部评测需要 JSON 时开启，会写文件。
    )
    summary = {
        "precision": float(metrics.box.mp),
        "recall": float(metrics.box.mr),
        "map50": float(metrics.box.map50),
        "map50_95": float(metrics.box.map),
        "per_class_map50_95": [float(value) for value in metrics.box.maps],
    }
    for key, value in summary.items():
        print(f"{key}: {value}")
    return summary


def predict(weights: Path | None = None) -> int:
    """流式处理结果，避免长视频的所有帧结果同时滞留内存。"""
    model_path = require_file(weights or CFG.deploy_weights, "待推理权重")
    model = YOLO(str(model_path))
    result_stream = model.predict(
        source=CFG.source,
        imgsz=CFG.imgsz,
        device=CFG.device,
        conf=CFG.conf,
        iou=CFG.nms_iou,
        stream=True,     # 长视频/摄像头优先生成器；单图也可正常遍历。
        save=True,
        save_txt=True,
        project=str(CFG.project),
        name=f"{CFG.run_name}_predict",
        exist_ok=False,
        # save_crop=True, # 可选：需要分类复核或下游 OCR 时保存目标裁剪图；会增加 I/O。
        # classes=[0, 2], # 可选：只保留指定 class_id；上线前核对 names 映射。
        # agnostic_nms=True, # 可选：跨类别抑制；类别易混淆时可能误删真实框。
    )

    processed = 0
    for result in result_stream:
        processed += 1
        boxes = result.boxes
        print(f"{result.path}: detections={len(boxes)}")
        for cls_id, score, xyxy in zip(boxes.cls, boxes.conf, boxes.xyxy):
            class_index = int(cls_id.item())
            class_name = result.names[class_index]
            coords = [round(float(value), 2) for value in xyxy.tolist()]
            print(f"  class={class_name}, score={float(score):.3f}, xyxy={coords}")
    return processed


def export(weights: Path | None = None) -> Path:
    """按目标格式构造参数；只给 ONNX 传递 ONNX 专用配置。"""
    model_path = require_file(weights or CFG.deploy_weights, "待导出权重")
    model = YOLO(str(model_path))
    common_args: dict[str, Any] = {
        "format": CFG.export_format,
        "imgsz": CFG.imgsz,
        "device": CFG.device,
    }

    if CFG.export_format == "onnx":
        common_args.update(
            dynamic=False, # 固定形状常更易优化；确需变尺寸/批次且后端支持时改 True。
            simplify=True, # 用 onnxslim 简化图；仍需做导出前后数值对齐测试。
            opset=None,    # 让当前 Ultralytics 选支持版本；旧后端要求特定 opset 时再固定。
            nms=False,     # 图外 NMS 更灵活；若改 True，确认部署端不会重复 NMS。
        )
    elif CFG.export_format == "engine":
        common_args.update(
            dynamic=False,
            # quantize=16, # 新版参数；旧版可能使用 half=True。只在目标 GPU 实测后开启。
            # workspace=None, # TensorRT 自动分配；受限设备应设置可接受 GiB。
        )

    exported = Path(model.export(**common_args))
    return require_exists(exported, "导出产物")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 自定义检测项目模板")
    parser.add_argument(
        "mode",
        choices=("env", "train", "resume", "val", "predict", "export", "all"),
        help="只运行一个阶段，或用 all 依次执行训练、验证、推理和导出。",
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        help="resume 模式必填，指向上次运行生成的 last.pt。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.mode == "env":
        describe_environment()
    elif args.mode == "train":
        print(train())
    elif args.mode == "resume":
        if args.checkpoint is None:
            raise ValueError("resume 模式必须提供 --checkpoint path/to/last.pt")
        print(train(resume_from=args.checkpoint))
    elif args.mode == "val":
        validate()
    elif args.mode == "predict":
        print(f"processed={predict()}")
    elif args.mode == "export":
        print(export())
    else:
        # all 模式把刚训练出的 best.pt 显式传给后续步骤，避免误用旧 deploy_weights。
        best = train()
        validate(best)
        print(f"processed={predict(best)}")
        print(export(best))


if __name__ == "__main__":
    main()
```
### 5.1 运行命令（Run Commands）
```bash
python yolo_project.py env
python yolo_project.py train
python yolo_project.py resume --checkpoint runs/detect/experiment/weights/last.pt
python yolo_project.py val
python yolo_project.py predict
python yolo_project.py export
python yolo_project.py all
```
训练、验证、推理和导出均会读取数据、权重或写入产物，输出依赖环境，不添加伪造的固定 Expected Output。
## 6. 关键参数：作用、场景与代价（Parameters, Scenarios, and Trade-offs）
### 6.1 训练参数（Training Arguments）

|参数（Argument）|作用（Purpose）|何时调整（When to Change）|代价与风险（Trade-off / Risk）|
|---|---|---|---|
|`epochs`|最大训练轮数|验证指标仍在持续提高时增加|过大增加时间；配合 `patience`，但早停依据要看版本|
|`batch`|每次参数更新的样本数|显存允许时增大；`-1` 可自动估算|大批次占显存并改变优化动态；自动估算也需实测|
|`imgsz`|训练/验证输入尺寸|小目标多或细节重要时提高|计算和显存近似随像素数快速增加，延迟变高|
|`device`|CPU/GPU/MPS/多卡选择|固定硬件复现或显式多卡时设置|多卡会改变启动方式、worker 和有效批大小|
|`workers`|每个进程的数据加载 worker|GPU 等待数据时逐步增加|过大耗内存；Windows/Jupyter 常需设 0 排错|
|`patience`|早停等待轮数|数据小、易过拟合时调小；指标波动大时调大|过小可能在暂时平台期提前停止|
|`freeze`|冻结前 N 层或指定层|极小数据、主干特征可迁移时|领域差异大时欠拟合；冻结范围必须查模型层索引|
|`amp`|自动混合精度训练|支持的 GPU 通常开启|少数算子/数据会数值不稳；异常时用 FP32 对照|
|`close_mosaic`|最后若干 epoch 关闭 Mosaic|希望末期贴近自然样本分布|训练轮数太短时关闭窗口占比过大|
|`resume`|恢复优化器、epoch 等完整状态|训练被中断后从 `last.pt` 继续|不能把 `best.pt` 微调等同于完整恢复|
|`exist_ok`|允许复用同名输出目录|明确需要覆盖/续写且已备份时|容易混合实验或覆盖结果，默认保持 `False`|
### 6.2 推理参数（Prediction Arguments）

|参数（Argument）|作用（Purpose）|适用场景（Scenario）|风险（Risk）|
|---|---|---|---|
|`conf`|最低类别置信度|误报成本高时提高；漏检成本高时降低|必须在独立验证集按业务代价选择|
|`iou`|NMS 重叠阈值|拥挤目标可尝试提高；重复框多可降低|过低误删相邻实例，过高保留重复框|
|`classes`|只保留指定类别|下游只关心部分类别|类别 ID 与模型 `names` 不一致会过滤错对象|
|`agnostic_nms`|不同类别之间也相互抑制|类别互斥、重复跨类框严重时|多标签或相邻异类目标可能被误删|
|`stream`|逐个生成结果|长视频、摄像头、大目录|生成器只能按需消费，不能先 `len(results)`|
|`save_txt`|保存预测标签|离线分析、伪标签|会产生大量文件；坐标格式和置信度选项要核对|
|`save_crop`|保存每个目标裁剪|OCR、人工复核、二阶段分类|增加磁盘 I/O，且裁剪包含的上下文有限|
### 6.3 导出参数（Export Arguments）

|参数（Argument）|作用（Purpose）|何时开启（When to Enable）|验证要求（Validation Requirement）|
|---|---|---|---|
|`format`|选择 ONNX、TensorRT、CoreML、TFLite、NCNN 等|由目标运行时决定|查官方格式支持表和目标设备版本|
|`dynamic`|允许动态批次或尺寸|输入变化且后端优化器支持时|测试多个形状；TensorRT 还涉及 optimization profile|
|`simplify`|简化中间图|ONNX 等支持格式|比较简化前后数值与运行时兼容性|
|`opset`|固定 ONNX 算子集|旧解析器只支持特定版本|用目标 ONNX Runtime/TensorRT 实际加载|
|`nms`|把 NMS 放进导出图|部署端不想实现后处理且格式支持时|确认输出契约，避免重复或遗漏 NMS|
|`quantize`|请求 FP16/INT8 等精度|后端和硬件支持且需降低延迟/体积|INT8 用代表性数据校准并重测逐类 AP/召回|
|`workspace`|TensorRT 构建工作空间上限|设备内存受限或需要更强 tactic 搜索|构建内存与运行内存不同，目标设备实测|
## 7. 结果对象解析（Results Object Parsing）
### 7.1 边界框字段（Bounding-box Fields）
- `result.boxes.xyxy`：绝对像素坐标，形状 `(N,4)`，顺序为 `x1,y1,x2,y2`。
- `result.boxes.xywh`：绝对像素中心格式。
- `result.boxes.xyxyn` / `xywhn`：相对原图归一化坐标。
- `result.boxes.conf`：每个检测置信度，形状 `(N,)`。
- `result.boxes.cls`：浮点张量存储的类别 ID，查 `result.names` 前转为 `int`。
- `result.path`：当前输入路径；批量推理时不要假设所有结果来自同一文件。
### 7.2 无检测结果（No Detection）
`len(result.boxes)==0` 是正常业务状态，不应当作程序异常。下游需要明确选择：返回空列表、记录未检测、触发复检，还是降低阈值后二次推理。
## 8. 训练—验证—部署验收清单（Acceptance Checklist）
### 8.1 数据验收（Data Acceptance）
- [ ] 图片可解码，标签基名与图片匹配。
- [ ] 类别 ID 均在 `names` 范围内，坐标归一化且宽高为正。
- [ ] 随机可视化至少几十张图，检查框、类别和方向。
- [ ] 按主体/视频/场景分组防止数据泄漏。
- [ ] 验证集包含关键类别、目标尺寸、遮挡和业务难例。
### 8.2 训练验收（Training Acceptance）
- [ ] 先完成 1 epoch smoke test，再启动长训练。
- [ ] 保存依赖版本、随机种子、数据版本、模型权重来源和命令。
- [ ] 同时观察训练/验证损失、Precision、Recall、mAP50、mAP50-95 与逐类指标。
- [ ] 检查混淆矩阵、PR 曲线、漏检、误检和标注质量，不只看单一 mAP。
- [ ] `best.pt` 与 `last.pt` 职责分开：前者用于最佳验证权重，后者用于完整断点恢复。
### 8.3 导出验收（Export Acceptance）
- [ ] 用同一组样本比较 `.pt` 与导出模型的预处理、框坐标、类别、分数和 NMS 结果。
- [ ] 在目标硬件测预热后延迟、吞吐、峰值内存和模型加载时间。
- [ ] 分别测试空目标、密集目标、小目标、极端长宽比、不同分辨率和损坏输入。
- [ ] 确认动态形状、批大小、FP16/INT8 与部署后端的真实支持范围。
- [ ] 记录输入输出张量名称、形状、dtype、颜色顺序、归一化和坐标还原公式。
## 9. 常见错误与排查（Common Errors and Troubleshooting）
### 9.1 找不到数据或标签（Missing Dataset or Labels）
- 先打印 YAML 绝对路径与当前工作目录。
- 检查 `path` 与 `train/val/test` 的拼接结果。
- 检查大小写、中文路径、容器挂载路径和软链接。
- 抽样检查图片与标签基名，不只统计文件数量。
### 9.2 CUDA 不可用或显存溢出（CUDA Unavailable or OOM）
- `nvidia-smi` 正常不代表 PyTorch wheel 一定能使用 CUDA；检查 `torch.cuda.is_available()`。
- OOM 时依次降低 `batch`、`imgsz`、缓存与 worker；不要先删掉验证或混合不同实验。
- 多 GPU 不是自动“更省显存”的开关，需检查分布式启动、每卡 batch 与通信。
### 9.3 断点续训没有继续（Resume Did Not Resume）
- 使用同一次运行的 `last.pt`，不要只加载 `best.pt` 后又宣称恢复了优化器状态。
- 检查 checkpoint、Ultralytics 版本与训练参数兼容性。
- 若只想以旧权重开始新实验，加载权重但不要使用 `resume=True`，并换新的 `name`。
### 9.4 指标好但业务效果差（Good Metrics, Poor Product Behavior）
- 检查验证集泄漏、场景覆盖不足和类别不平衡。
- 查看逐类、小/中/大目标与业务难例，不只看总体 mAP。
- 根据误报/漏报代价选择 `conf` 和 NMS `iou`，评估阈值与部署阈值职责不同。
- 检查部署预处理与训练验证是否一致。
### 9.5 导出模型结果不一致（Export Mismatch）
- 先比较 NMS 前原始输出，再逐步加入解码与 NMS。
- 检查 RGB/BGR、`0–255` 到 `0–1`、Letterbox 填充、输入布局 NCHW/NHWC 和 dtype。
- 检查导出图是否内置 NMS、动态轴是否受后端支持、opset 是否匹配。
- 量化模型需要逐层或逐输出比较，并用代表性校准数据重建 INT8 引擎。
## 10. 拆分成多文件（Optional Multi-file Layout）
当单文件稳定后，可拆成：
```text
yolov8_project/
├── config.py
├── train.py
├── validate.py
├── predict.py
├── export.py
└── common.py
```
优先使用包内相对导入或从项目根目录以模块运行，例如 `python -m yolov8_project.train`。若必须支持临时脚本，可用 `Path(__file__).resolve().parent` 计算根目录；尽量不要长期修改 `sys.path`，否则同名模块和不同启动目录会产生隐蔽导入错误。
```python
from pathlib import Path

# `__file__` 指向当前配置文件；resolve() 消除相对段和符号链接歧义。
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_YAML = PROJECT_ROOT / "datasets" / "my_dataset.yaml"
WEIGHTS_DIR = PROJECT_ROOT / "weights"
RUNS_DIR = PROJECT_ROOT / "runs" / "detect"
```
## 11. 参考资料（References）
- [Ultralytics Train Mode](https://docs.ultralytics.com/modes/train/)
- [Ultralytics Validation Mode](https://docs.ultralytics.com/modes/val/)
- [Ultralytics Predict Mode](https://docs.ultralytics.com/modes/predict/)
- [Ultralytics Export Mode](https://docs.ultralytics.com/modes/export/)
- [Ultralytics Dataset Format](https://docs.ultralytics.com/datasets/detect/)
