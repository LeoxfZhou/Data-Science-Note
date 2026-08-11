---
title: PyTorch 模型持久化与推理（PyTorch Model Persistence and Inference）
aliases:
  - PyTorch Model Persistence
  - PyTorch Inference
tags:
  - data-science/deep-learning/pytorch
  - software-engineering/model-deployment
status: published
created: 2026-08-11
published_at: 2026-08-11
---
# PyTorch 模型持久化与推理（PyTorch Model Persistence and Inference）
## 1. 保存对象的层级（Serialization Levels）
### 1.1 `state_dict`（推荐）
- 模型 `state_dict` 是名称到参数张量与注册缓冲区（Registered Buffer）的映射。
- 它不保存 Python 类定义和 `forward()` 代码，因此加载前必须重新实例化兼容模型结构。
- 与保存整个模型对象相比，`state_dict` 更灵活、可移植，也更容易检查键名和迁移设备。
- 常见扩展名是 `.pt` 或 `.pth`；扩展名只是约定，不决定内容格式。
### 1.2 通用 checkpoint（General Checkpoint）
- 断点续训至少保存当前 epoch、模型状态和优化器状态。
- 还可保存学习率调度器（Scheduler）、梯度缩放器（Gradient Scaler）、最佳指标、类别映射、配置、随机状态和代码版本。
- 恢复训练时，保存方式与加载方式必须一一对应；只加载模型参数不能恢复优化器动量等训练状态。
### 1.3 整个模型对象（Whole Model Object）
- `torch.save(model, path)` 依赖 Python pickle 和原始类定义路径。
- 加载需要 `weights_only=False`，攻击面更大；只对可信文件使用。
- 官方最佳实践仍是保存 `state_dict`。

> [!tip] 大白话理解（Plain-language Intuition）
> `state_dict` 像只保存模型已经学到的“参数表”，加载时还需要同一套模型结构；checkpoint 则像游戏存档，除了角色属性，还保存训练轮数、优化器动量和其他继续训练所需状态。只保存参数能做推理，但不一定能无缝接着训练。
## 2. 保存权重与 checkpoint（Saving Weights and Checkpoints）
### 2.1 仅保存模型权重（Model Weights Only）
```python
from pathlib import Path
import torch


def save_model_weights(model, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), target)


# save_model_weights(model, "artifacts/best_model.pth")
```
该示例写入文件，属于文件 I/O（File I/O），不附固定输出。
### 2.2 保存断点（Checkpoint）
```python
from pathlib import Path
import torch


def save_checkpoint(
    path: str | Path,
    epoch: int,
    model,
    optimizer,
    best_accuracy: float,
    scheduler=None,
) -> None:
    checkpoint = {
        "epoch": epoch,
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict(),
        "best_accuracy": best_accuracy,
    }
    if scheduler is not None:
        checkpoint["scheduler_state"] = scheduler.state_dict()
    torch.save(checkpoint, Path(path))
```
### 2.3 最佳权重快照（Best-weight Snapshot）
- `best_state = model.state_dict()` 返回的映射值仍引用模型状态；后续训练可能使“最佳状态”跟着变化。
- 立即 `torch.save(model.state_dict(), path)`，或在内存中使用 `copy.deepcopy(model.state_dict())`。
## 3. 加载权重（Loading Weights）
### 3.1 安全加载流程（Safe Loading Flow）
```python
from pathlib import Path
import torch


def load_model_weights(model, path: str | Path, device: torch.device):
    state_dict = torch.load(
        Path(path),
        map_location=device,
        weights_only=True,
    )
    incompatible = model.load_state_dict(state_dict, strict=True)
    model.to(device)
    model.eval()
    return incompatible
```
该示例读取文件，结果取决于 checkpoint 与模型结构。
### 3.2 `map_location`
- `map_location="cpu"` 可先把存储加载到 CPU，避免保存于 GPU 的张量直接占用 GPU 显存。
- 也可传 `torch.device`、设备映射字典或函数，处理跨 GPU 编号迁移。
- 加载到 CPU 后再 `model.to(device)` 通常更容易控制显存峰值。
### 3.3 `strict=True/False`
- `strict=True` 要求状态字典键与模型参数/缓冲区键完全匹配，能及早发现结构错误。
- `strict=False` 允许缺失键（Missing Keys）和意外键（Unexpected Keys），适合迁移学习或替换分类头，但不会自动证明形状和语义正确。
- 必须检查 `load_state_dict()` 返回的 `missing_keys` 与 `unexpected_keys`，不能静默忽略。
### 3.4 `weights_only` 与不可信文件（Untrusted Files）
- PyTorch 2.6 起，未显式传 `pickle_module` 时，`torch.load` 默认使用 `weights_only=True`。
- 该模式限制可构造对象，缩小任意代码执行风险，但不保证抵御拒绝服务或恶意张量造成的所有下游风险。
- 旧 checkpoint 若保存整个 `nn.Module`，可能必须使用 `weights_only=False`；仅对来源可信且经过校验的文件这样做。
## 4. 恢复训练（Resume Training）
```python
import torch


def restore_training_state(
    checkpoint_path,
    model,
    optimizer,
    device,
    scheduler=None,
):
    checkpoint = torch.load(
        checkpoint_path,
        map_location=device,
        weights_only=True,
    )
    model.load_state_dict(checkpoint["model_state"])
    optimizer.load_state_dict(checkpoint["optimizer_state"])
    if scheduler is not None and "scheduler_state" in checkpoint:
        scheduler.load_state_dict(checkpoint["scheduler_state"])
    start_epoch = int(checkpoint["epoch"]) + 1
    best_accuracy = float(checkpoint.get("best_accuracy", float("-inf")))
    return start_epoch, best_accuracy
```
- 恢复优化器后，检查其状态张量所在设备；复杂跨设备场景可能需要显式迁移。
- 必须同时恢复数据划分、类别映射、随机状态和超参数，才能接近原训练轨迹。
## 5. 推理预处理（Inference Preprocessing）
### 5.1 与训练对齐（Train-inference Alignment）
- 颜色空间、通道数、图像尺寸、插值方式、dtype、像素范围和 Normalize 参数必须与训练一致。
- 不执行随机水平/垂直翻转、随机旋转、随机裁剪等训练增强，除非明确使用测试时增强（Test-time Augmentation, TTA）。
- 带 Alpha 通道 PNG 和灰度图可统一转换为 RGB；这属于输入契约防御，不等于可以忽略所有损坏文件。
### 5.2 增加批次维（Adding the Batch Dimension）
```python
import torch

image_tensor = torch.zeros((3, 224, 224))
input_batch = image_tensor.unsqueeze(0)
print(input_batch.shape)  # 输出: torch.Size([1, 3, 224, 224])
```
- 单张图通常从 `[C,H,W]` 变为 `[1,C,H,W]`。
- 推理服务可将多请求组成动态批次，提高 GPU 利用率，但会引入排队延迟和更复杂的错误隔离。
## 6. 分类预测与后处理（Classification Prediction and Post-processing）
```python
import torch


def predict_class(model, input_batch: torch.Tensor) -> tuple[int, float]:
    model.eval()
    with torch.inference_mode():
        logits = model(input_batch)
        probabilities = torch.softmax(logits, dim=1)
        confidence, predicted = probabilities.max(dim=1)
    return predicted.item(), confidence.item()
```
- `softmax(logits, dim=1)` 把单标签多分类 logits 转为各类别概率。
- `argmax(logits, dim=1)` 与 `argmax(softmax(logits), dim=1)` 类别相同；只有展示置信度时才需要 Softmax。
- 多标签任务应对每个类别使用 Sigmoid 和独立阈值，不使用互斥 Softmax。
- 类别索引必须通过训练时保存的 `class_to_idx` 反映射为业务标签。
- Softmax 数值不是天然校准置信度；高风险决策需要校准、阈值、拒识和分布外检测。
## 7. 部署架构考虑（Deployment Architecture Considerations）
- 模型应在服务启动时加载一次并复用，避免每请求重新读权重。
- FastAPI/Flask 请求层负责校验与协议转换，模型推理层保持同步、无隐藏网络副作用，并由线程池、进程或专用推理 worker 调度。
- GPU 运算的吞吐、延迟和并发受批次、内存、预处理、同步点和模型结构共同影响；不能只凭异步路由声称高并发。
- 检测与 OCR 两阶段系统可拆为独立服务，也可在单进程流水线执行。服务拆分提高独立扩展和故障隔离，但增加网络延迟、序列化、重试和一致性成本。
- PyTorch 模型可导出 ONNX 并由 ONNX Runtime 推理，但必须验证算子兼容、动态轴、数值误差和前后处理一致性。
## 8. 常见错误与安全边界（Common Errors and Security Boundaries）

|错误（Error）|影响（Impact）|修正（Fix）|
|---|---|---|
|把路径传给 `load_state_dict()`|API 类型错误|先 `torch.load()` 得到字典|
|加载后忘记 `eval()`|Dropout/BatchNorm 推理不一致|加载完成后显式 `model.eval()`|
|只 `eval()` 不关闭梯度|浪费内存与计算|使用 `inference_mode()`/`no_grad()`|
|训练与推理 Normalize 不一致|分布偏移与精度下降|保存并复用预处理配置|
|`strict=False` 后忽略返回值|部分层未加载却未发现|审计 missing/unexpected keys|
|从未知来源 `weights_only=False`|可能执行恶意 pickle 代码|仅加载可信制品，优先 state_dict|
|只保存模型而想断点续训|优化器动量和 epoch 丢失|保存完整 checkpoint|
|服务关闭时只调用 `empty_cache()`|活跃张量引用仍占显存|释放模型引用并正确结束 worker；缓存清理不是对象释放|

## 参考资料（References）
- [PyTorch 保存与加载模型官方教程](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)
- [`torch.load` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.load.html)
- [PyTorch 序列化语义](https://docs.pytorch.org/docs/stable/notes/serialization.html)
