```python
# -*- coding: utf-8 -*-
"""
YOLOv8 工业级迁移学习微调通用模板
适用场景：基于预训练权重，在自定义中小规模数据集（100~5000张图片）上进行目标检测微调（如车牌、花卉、缺陷检测等）。

环境依赖与安装命令：
    pip install ultralytics==8.2.0 torch==2.2.0 torchvision==0.17.0 opencv-python==4.9.0.80

================================================================================
【数据集准备说明】
================================================================================
1. YOLO 格式目录结构要求（图片与标注文件名必须完全一致，如 001.jpg 对应 001.txt）：
   my_dataset/
   ├── data.yaml              <-- 数据集配置文件
   ├── train/
   │   ├── images/            <-- 存放训练集图片 (jpg, png, bmp 等)
   │   └── labels/            <-- 存放训练集 TXT 格式标注文件
   └── val/
       ├── images/            <-- 存放验证集图片
       └── labels/            <-- 存放验证集 TXT 格式标注文件

2. 标注文件 (TXT) 格式示例：
   每行代表一个目标：<类别ID> <x_center> <y_center> <width> <height>
   注意：所有坐标必须是归一化到 0~1 之间的浮点数。

3. data.yaml 配置文件示例：
   -----------------------------------------------------------------------------
   path: /absolute/path/to/my_dataset  # 数据集根目录绝对路径（使用绝对路径可防找不到文件）
   train: train/images                 # 训练集图片相对于 path 的路径
   val: val/images                     # 验证集图片相对于 path 的路径
   
   nc: 3                               # 你的自定义数据集类别总数
   names:
     0: license_plate                  # 类别0名称
     1: flower                         # 类别1名称
     2: defect                         # 类别2名称
   -----------------------------------------------------------------------------

4. 格式转换提示：
   - 如果你的原始标注是 VOC (XML) 或 COCO (JSON) 格式，无法直接填入此处。
   - 推荐使用转换工具：`labelme2yolo` 库，或者在 Roboflow 平台上载并直接导出为 YOLOv8 格式。

5. 常见开源数据集下载渠道：
   - Roboflow Universe (https://universe.roboflow.com/)：包含大量已标记好的 YOLO 格式数据集。
   - Kaggle (https://www.kaggle.com/)：搜索相关图像检测任务。
   - Ultralytics HUB：官方提供的一站式数据集与模型管理平台。
"""

import os
import sys
import torch
from ultralytics import YOLO

# ==============================================================================
# 【配置集中化管理】 - 全局超参数与路径配置
# ==============================================================================
CONFIG = {
    # ------------------- [必须修改] 数据与核心路径 -------------------
    # [必须修改] 你的自定义数据集配置文件 data.yaml 的路径
    "DATA_YAML": "my_dataset/data.yaml",
    
    # [必须修改] 用于推理/预测的测试源。支持：单张图片路径、图片文件夹路径、视频路径或摄像头ID(如 0)
    "SOURCE_PATH": "my_dataset/val/images",

    # ------------------- [可选调整] 模型与迁移学习 -------------------
    # [可选调整] 预训练模型大小，可选：'n' (纳米级), 's' (轻量级), 'm' (中型), 'l' (大型), 'x' (超大型)
    # 影响：模型越大精度越高，但训练和推理速度越慢，显存开销剧增。中小数据集微调推荐首选 's' 或 'm'
    "MODEL_SIZE": "s",
    
    # [可选调整] 预训练权重基础名称或本地路径。默认自动联网下载官方权重
    # 微调核心：以官方在 COCO 上训练好的权重为起点，继承提取边缘、色彩等通用特征的能力
    "PRETRAINED_WEIGHTS": "yolov8s.pt",
    
    # [可选调整] 自定义训练好的权重路径。用于独立验证、连续推理或模型导出阶段
    # 注意：训练完成后，请将其修改为具体产出的最好权重，例如 "runs/detect/my_finetune_project/weights/best.pt"
    "DEPLOY_WEIGHTS": "yolov8s.pt",

    # ------------------- [可选调整] 训练超参数（基于 8GB 显存优化） -------------------
    # [可选调整] 微调训练的总轮数。中小规模数据集迁移学习通常 50 ~ 150 轮即可收敛
    "EPOCHS": 100,
    
    # [可选调整] 批次大小 (Batch Size)。每批读入显卡的图片数量
    # 影响：增大能加快训练并使梯度稳定，但太大会导致显存溢出 (OOM)。8GB 显存建议设为 16 或 32
    "BATCH_SIZE": 16,
    
    # [可选调整] 输入网络的图像分辨率。必须是 32 的倍数。默认 640
    # 影响：增大该值可以显著提升对细小目标的检测精度，但会成倍消耗显存并降低速度。8GB 显存微调不建议超过 640
    "IMAGE_SIZE": 640,
    
    # [可选调整] 计算设备选择。'0' 代表第一块 GPU，'0,1' 代表双卡多 GPU 分布式训练，'cpu' 代表纯 CPU 训练
    # 影响：若设为 None，程序会自动检测并优先选择 GPU 加速
    "DEVICE": None,
    
    # [可选调整] 数据加载的线程数 (DataLoader workers)。
    # 影响：过大可能导致内存溢出或 Windows 系统报错，过小会导致 GPU 等待数据。Windows 推荐 0 或 2，Linux 推荐 4 或 8
    "WORKERS": 4,
    
    # [可选调整] 早停机制 (Early Stopping)。如果连续 N 轮验证集损失没有改善，则提前终止训练以防过拟合
    "PATIENCE": 20,
    
    # [可选] 断点续训开关。若训练中途因断电或异常中断，设为 True 会自动寻找上次中断的 checkpoint (last.pt) 继续训练
    "RESUME": False,

    # ------------------- [可选调整] 输出及部署 -------------------
    # [可选调整] 保存所有训练日志、图表与权重的根目录名称
    "PROJECT_NAME": "runs/detect",
    
    # [可选调整] 本次微调任务的子文件夹名称，结果最终保存在 PROJECT_NAME/RUNS_DIR 下
    "RUNS_DIR": "my_finetune_project",
    
    # [可选调整] 模型导出目标格式，可选：'onnx', 'torchscript', 'engine' (TensorRT)
    # 影响：'onnx' 通用性最强，'engine' 在英伟达边缘设备（如 Jetson）上推理速度最快
    "EXPORT_FORMAT": "onnx"
}


# ==============================================================================
# 【核心功能函数实现】
# ==============================================================================

def get_device():
	"""
	智能设备检测函数，返回 YOLO 可接受的 device 参数（字符串）
	"""
	# 1. 如果用户显式指定了设备，直接使用（信任用户的配置）
	if CONFIG["DEVICE"] is not None:
		return str(CONFIG["DEVICE"]) # 统一转成字符串
	# 2. 用户未指定，自动检测
	if torch.cuda.is_available():
		gpu_count = torch.cuda.device_count()
		if gpu_count > 1:
		# 多卡：返回 "0,1,2,..."
			return ",".join([str(i) for i in range(gpu_count)])
		else:
		# 单卡：返回 "0"
			return "0"
	else:
		# 没有 GPU：强制使用 CPU
		return "cpu"


def train(device_setting):
    """
    1. 迁移学习微调训练函数
    """
    print("\n" + "="*30 + " 步骤 1: 启动 YOLOv8 迁移学习微调 " + "="*30)
    
    # 数据集路径防错校验
    if not os.path.exists(CONFIG["DATA_YAML"]):
        raise FileNotFoundError(f"[错误] 未找到数据集配置文件: {CONFIG['DATA_YAML']}，请检查路径！")

    # 判断是全新微调还是断点续训
    if CONFIG["RESUME"]:
        # [可选] 断点续训场景：加载上一次中断时的末尾权重
        checkpoint_path = os.path.join(CONFIG["PROJECT_NAME"], CONFIG["RUNS_DIR"], "weights", "last.pt")
        if os.path.exists(checkpoint_path):
            print(f"[提示] 检测到中断存档，正在从断点恢复训练: {checkpoint_path}")
            model = YOLO(checkpoint_path)
        else:
            print(f"[警告] 未找到断点文件 {checkpoint_path}，将采用标准预训练权重开始全新训练。")
            model = YOLO(CONFIG["PRETRAINED_WEIGHTS"])
    else:
        # 标准微调场景：加载官方预训练权重作为网络底座
        print(f"[提示] 成功加载预训练权重基底: {CONFIG['PRETRAINED_WEIGHTS']}")
        model = YOLO(CONFIG["PRETRAINED_WEIGHTS"])

    # 触发微调训练流程
    # 核心超参数全部由顶部 CONFIG 字典统一驱动，实现逻辑解耦
    model.train(
        data=CONFIG["DATA_YAML"],
        epochs=CONFIG["EPOCHS"],
        batch=CONFIG["BATCH_SIZE"],
        imgsz=CONFIG["IMAGE_SIZE"],
        device=device_setting,
        workers=CONFIG["WORKERS"],
        patience=CONFIG["PATIENCE"],
        resume=CONFIG["RESUME"],
        project=CONFIG["PROJECT_NAME"],
        name=CONFIG["RUNS_DIR"],
        plots=True,          # 自动绘制损失曲线、PR曲线、混淆矩阵等评估图表
        exist_ok=True,       # 若目标文件夹已存在则直接覆盖/追加，不报错中断
        freeze=None          # [可选] 若数据集极小(<100张)，可填入整数(如10)冻结前N层骨干网络，防过拟合
    )
    print(f"[成功] 微调结束！最佳权重已保存至: {CONFIG['PROJECT_NAME']}/{CONFIG['RUNS_DIR']}/weights/best.pt")


def validate(device_setting):
    """
    2. 验证集精度评估函数
    """
    print("\n" + "="*30 + " 步骤 2: 在验证集上评估模型精度 " + "="*30)
    
    # 实例化需要评估的模型权重
    print(f"[提示] 正在加载待评估的权重: {CONFIG['DEPLOY_WEIGHTS']}")
    model = YOLO(CONFIG["DEPLOY_WEIGHTS"])
    
    # 在验证集上跑一遍前向传播，计算工业级精度指标
    metrics = model.val(
        data=CONFIG["DATA_YAML"],
        imgsz=CONFIG["IMAGE_SIZE"],
        batch=CONFIG["BATCH_SIZE"],
        device=device_setting,
        project=CONFIG["PROJECT_NAME"],
        name=f"{CONFIG['RUNS_DIR']}_val",
        plots=True
    )
    
    # 从指标对象中提取并格式化打印四大核心指标
    print("\n" + "-"*20 + " 模型综合精度报告 " + "-"*20)
    print(f"Precision (精确率) : {metrics.results_dict['metrics/precision(B)']:.4f} (预测为正样本中实际为正的比例)")
    print(f"Recall    (召回率) : {metrics.results_dict['metrics/recall(B)']:.4f} (所有实际为正样本中被预测出来的比例)")
    print(f"mAP50     (平均精度) : {metrics.results_dict['metrics/mAP50(B)']:.4f} (IoU阈值为0.5时的mAP，常用于目标识别考核)")
    print(f"mAP50-95  (严苛精度) : {metrics.results_dict['metrics/mAP50-95(B)']:.4f} (在不同IoU阈值下的平均值，反映定位精准度)")
    print("-"*58)


def predict(device_setting):
    """
    3. 核心推理与可视化预测函数
    """
    print("\n" + "="*30 + " 步骤 3: 启动模型推理与可视化预测 " + "="*30)
    
    model = YOLO(CONFIG["DEPLOY_WEIGHTS"])
    
    # 执行预测推理
    results = model.predict(
        source=CONFIG["SOURCE_PATH"],
        imgsz=CONFIG["IMAGE_SIZE"],
        device=device_setting,
        save=True,             # 自动将画有预测边界框、置信度标签的图片/视频保存到本地
        save_txt=True,         # 自动将预测出来的目标坐标保存为标准 YOLO 格式的 TXT 文件
        conf=0.25,             # 置信度阈值。低于 0.25 的检测框会被过滤，工业部署时可根据实际调整
        iou=0.45,              # NMS(非极大值抑制)的IoU阈值。越小对重叠目标的重叠框消除越狠
        project=CONFIG["PROJECT_NAME"],
        name=f"{CONFIG['RUNS_DIR']}_predict"
    )
    
    print(f"[成功] 推理完成！本次共处理 {len(results)} 个输入源，可视化结果已保存至上述 predict 文件夹中。")


def export():
    """
    4. 模型导出与部署转换函数
    """
    print("\n" + "="*30 + " 步骤 4: 导出轻量化/加速部署模型 " + "="*30)
    
    model = YOLO(CONFIG["DEPLOY_WEIGHTS"])
    
    print(f"[提示] 正在将 .pt 格式权重转换为 {CONFIG['EXPORT_FORMAT']} 格式...")
    # 导出模型，以便后续使用 C++、TensorRT 或 ONNXRuntime 进行高吞吐量工业部署
    exported_path = model.export(
        format=CONFIG["EXPORT_FORMAT"],
        imgsz=CONFIG["IMAGE_SIZE"]
    )
    print(f"[成功] 模型导出完毕！部署文件路径: {exported_path}")


# ==============================================================================
# 【主入口与多模式一键控制开关】
# ==============================================================================
if __name__ == "__main__":
    # 执行模式切换：可选 'quick' (快速流水线模式) 或 'split' (手动拆分模式)
    # 建议：初次使用或者重新训练时，选择 'quick' 跑通全流程；
    #      当模型训练完毕后，若只想单独调试推理或导出，请切换为 'split' 并配合下方布尔开关使用。
    RUN_MODE = "quick" 
    
    # 当且仅当 RUN_MODE = "split" 时，以下独立布尔开关才会生效
    RUN_TRAIN    = True   # 是否单独触发训练
    RUN_VALIDATE = False  # 是否单独触发验证
    RUN_PREDICT  = False  # 是否单独触发推理
    RUN_EXPORT   = False  # 是否单独触发导出

    # 自动获取最佳计算设备环境 (GPU / CPU)
    current_device = get_device()

    if RUN_MODE == "quick":
        print("[工作模式提示] 当前处于: 快速流水线模式 (一键顺次执行 训练 -> 验证 -> 导出)")
        
        # 1. 运行微调训练
        train(device_setting=current_device)
        
        # 【工业级联动优化】训练结束后，自动将部署权重更新为刚刚热腾腾产出的最佳权重 best.pt
        generated_best_weight = os.path.join(CONFIG["PROJECT_NAME"], CONFIG["RUNS_DIR"], "weights", "best.pt")
        if os.path.exists(generated_best_weight):
            CONFIG["DEPLOY_WEIGHTS"] = generated_best_weight
            print(f"[智能联动] 已自动将后续验证与导出的权重路径更新为最佳权重: {generated_best_weight}")
        
        # 2. 自动运行验证评估
        validate(device_setting=current_device)
        
        # 3. 自动导出为部署格式
        export()

    elif RUN_MODE == "split":
        print("[工作模式提示] 当前处于: 手动拆分模式 (根据布尔开关精细控制各步骤)")
        
        if RUN_TRAIN:
            train(device_setting=current_device)
            # 智能联动，防止用户忘记改 DEPLOY_WEIGHTS
            generated_best_weight = os.path.join(CONFIG["PROJECT_NAME"], CONFIG["RUNS_DIR"], "weights", "best.pt")
            if os.path.exists(generated_best_weight):
                CONFIG["DEPLOY_WEIGHTS"] = generated_best_weight

        if RUN_VALIDATE:
            validate(device_setting=current_device)

        if RUN_PREDICT:
            predict(device_setting=current_device)

        if RUN_EXPORT:
            export()

    print("\n" + "="*30 + " 所有指定任务顺利执行完毕 " + "="*30)
```

### 如果config跨文件
```python
current_dir = os.path.dirname(os.path.abspath(__file__)) 
# 获取 yolo_training 绝对路径 
project_root = os.path.abspath(os.path.join(current_dir, '..')) 
# 找到父目录 v8_PlateRecognition 
if project_root not in sys.path: sys.path.insert(0, project_root) 
# 现在可以优雅地跨文件夹导入了！ 
from configs.config import CONFIG, get_device
```