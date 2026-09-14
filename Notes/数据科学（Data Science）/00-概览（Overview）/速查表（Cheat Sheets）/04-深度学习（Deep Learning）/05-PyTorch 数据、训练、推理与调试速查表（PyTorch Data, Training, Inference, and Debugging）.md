---
title: "PyTorch 数据、训练、推理与调试速查表（PyTorch Data, Training, Inference, and Debugging Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - pytorch/workflow
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "Python 3.11+；PyTorch 2.x；Torchvision/TorchText/TorchAudio 需匹配 torch；DeepSpeed 0.15+"
---
# PyTorch 数据、训练、推理与调试速查表（PyTorch Data, Training, Inference, and Debugging Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
完整闭环包括 Dataset/DataLoader、训练、验证、checkpoint、推理、性能剖析与确定性设置。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 2. 配套包与诊断工具（Companion Packages and Diagnostics）
### 2.1 TorchText（TorchText）
- **安装包（Distribution）**：`torchtext`。
- **导入模块（Import Module）**：`torchtext`。
- **安装命令（Installation）**：按 PyTorch 兼容矩阵安装与 `torch` 匹配的版本。
- **用途（Purpose）**：文本数据集、词表和既有 NLP 数据处理组件；新项目需注意其维护状态和版本兼容性。
- **正式笔记（Detailed Note）**：[[01-PyTorch 数据集、变换与加载器（PyTorch Datasets, Transforms, and DataLoaders）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建词表|`vocab(counter, specials=['<unk>'])`|返回 Vocab 并分配 token ID|
|默认索引|`vocabulary.set_default_index(index)`|原地设置未知词回退 ID|
|批量查 ID|`vocabulary(tokens)`|返回整数 ID 列表|

```python
from torchtext.vocab import vocab
from collections import Counter

tokens = vocab(Counter({"data": 2, "science": 1}), specials=["<unk>"])
tokens.set_default_index(tokens["<unk>"])
print(tokens(["data", "missing"]))  # 输出: [1, 0]
```
### 2.2 TorchAudio（TorchAudio）
- **安装包（Distribution）**：`torchaudio`。
- **导入模块（Import Module）**：`torchaudio`。
- **安装命令（Installation）**：按 PyTorch 兼容矩阵安装与 `torch` 匹配的版本。
- **用途（Purpose）**：音频读取、特征变换、数据集和预训练音频管线。
- **正式笔记（Detailed Note）**：[[01-PyTorch 数据集、变换与加载器（PyTorch Datasets, Transforms, and DataLoaders）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|读取音频|`torchaudio.load(path)`|返回 `[channels,time]` 波形与采样率|
|保存音频|`torchaudio.save(path, waveform, sample_rate)`|写音频文件|
|Mel 频谱|`torchaudio.transforms.MelSpectrogram(...)`|返回可调用变换模块|
|重采样|`torchaudio.functional.resample(waveform, orig_freq, new_freq)`|返回新波形张量|

```python
import torch
import torchaudio

waveform = torch.zeros(1, 16000)
mel = torchaudio.transforms.MelSpectrogram(sample_rate=16000, n_mels=40)(waveform)
print(mel.shape[0], mel.shape[1])  # 输出: 1 40
```
### 2.3 TorchInfo 模型摘要（TorchInfo Model Summary）
- **安装包（Distribution）**：`torchinfo`。
- **导入模块（Import Module）**：`torchinfo`。
- **安装命令（Installation）**：`python -m pip install -U torchinfo`。
- **用途（Purpose）**：根据输入尺寸统计层级输出形状与参数量。
- **正式笔记（Detailed Note）**：[[02-PyTorch 模型工程结构与环境（PyTorch Model Engineering Structure and Environment）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|生成摘要|`summary(model, input_size=..., dtypes=..., device=..., verbose=0)`|运行一次模拟前向并返回 ModelStatistics|
|参数总数|`report.total_params`|返回整数|
|可训练参数|`report.trainable_params`|返回整数|

```python
from torch import nn
from torchinfo import summary

model = nn.Sequential(nn.Linear(4, 2), nn.ReLU())
report = summary(model, input_size=(1, 4), verbose=0)
print(report.total_params)  # 输出: 10
```
### 2.4 TensorBoard（TensorBoard）
- **安装包（Distribution）**：`tensorboard`。
- **导入模块（Import Module）**：训练端通常从 `torch.utils.tensorboard` 导入 `SummaryWriter`；查看器命令为 `tensorboard`。
- **安装命令（Installation）**：`python -m pip install -U tensorboard`。
- **用途（Purpose）**：记录标量、图、直方图、图像和嵌入，并在浏览器查看。
- **正式笔记（Detailed Note）**：[[04-PyTorch 训练与评估循环（PyTorch Training and Evaluation Loops）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建写入器|`SummaryWriter(log_dir)`|创建事件目录/文件并返回写入器|
|记录标量|`writer.add_scalar(tag, value, step)`|追加事件|
|记录图像|`writer.add_image(tag, image, step, dataformats='CHW')`|追加图像事件|
|关闭|`writer.close()`|刷新缓冲并关闭文件|

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("runs/demo")
writer.add_scalar("loss/train", 0.25, global_step=1)
writer.close()
# 会在 runs/demo 写事件文件；使用 tensorboard --logdir runs 启动本地查看器。
```
### 2.5 DeepSpeed（DeepSpeed）
- **安装包（Distribution）**：`deepspeed`。
- **导入模块（Import Module）**：`deepspeed`。
- **安装命令（Installation）**：`python -m pip install -U deepspeed`，安装前核对 CUDA、PyTorch 和编译工具链。
- **用途（Purpose）**：ZeRO 分片、混合精度、分布式训练、检查点和大模型内存优化。
- **正式笔记（Detailed Note）**：[[04-DeepSpeed 分布式训练、ZeRO 与混合精度（DeepSpeed Distributed Training, ZeRO, and Mixed Precision）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|环境诊断|`ds_report`|打印可用/缺失算子与系统兼容性|
|初始化|`deepspeed.initialize(model=model, model_parameters=..., config=config)`|返回引擎、优化器、数据加载器和调度器|
|反向传播|`engine.backward(loss)`|执行含缩放/通信的反向传播|
|更新|`engine.step()`|更新参数并处理梯度累积|
|保存检查点|`engine.save_checkpoint(path, tag=...)`|各 rank 写分片与客户端状态|
|加载检查点|`engine.load_checkpoint(path, tag=...)`|恢复分片状态并返回路径/客户端状态|

```python
import deepspeed

config = {
    "train_micro_batch_size_per_gpu": 2,
    "gradient_accumulation_steps": 4,
    "zero_optimization": {"stage": 2},
    "bf16": {"enabled": True},
}
print(config["train_micro_batch_size_per_gpu"] * config["gradient_accumulation_steps"])  # 输出: 8（单 GPU 有效批量）
# 多 GPU 时还需乘数据并行进程数；真正初始化会占用设备并建立分布式状态。
```
- **精度边界（Precision Boundary）**：BF16 需要硬件支持；FP16 常需动态损失缩放。模型权重、输入和算子数据类型不匹配时会报错或发生额外转换。
- **ZeRO 选型（ZeRO Selection）**：Stage 1 分片优化器状态，Stage 2 再分片梯度，Stage 3 再分片参数；内存收益越高，通信和检查点复杂度通常越高。
## Dataset 与 DataLoader（Data Pipeline）
Dataset 定义单样本，DataLoader 负责批处理、打乱和多进程加载。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|映射式数据集|`class D(Dataset): __len__; __getitem__`|按索引返回单样本|
|流式数据集|`class D(IterableDataset): __iter__`|返回样本迭代器|
|批加载|`DataLoader(ds,batch_size=32,shuffle=True)`|返回批次迭代器|
|自定义合批|`collate_fn(batch)`|返回模型所需批结构|
|多进程|`num_workers=n`|创建加载子进程|
|锁页内存|`pin_memory=True`|CPU 到 CUDA 异步拷贝更高效|
|丢弃尾批|`drop_last=True`|训练批大小固定|
|采样器|`WeightedRandomSampler(weights,num_samples)`|返回索引采样器|
|拆分|`random_split(dataset,lengths,generator=g)`|返回 Subset 列表|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torch.utils.data import DataLoader,TensorDataset
ds=TensorDataset(torch.arange(6),torch.arange(6)*2)
loader=DataLoader(ds,batch_size=4,shuffle=False)
x,y=next(iter(loader)); print(x.tolist(),y.tolist())
# 期望输出:
# [0, 1, 2, 3] [0, 2, 4, 6]
```
## 训练、验证与 Checkpoint（Training and Checkpointing）
保存模型、优化器、调度器、epoch、最佳指标和随机状态，才能可靠续训。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|训练态|`model.train()`|启用 Dropout/BatchNorm 训练行为|
|评估态|`model.eval()`|启用确定性评估行为|
|混合精度|`with torch.autocast(device_type='cuda')`|:块内自动选择低精度|
|梯度缩放|`scaler.scale(loss).backward()`|缩放反向梯度|
|更新缩放|`scaler.step(opt); scaler.update()`|安全更新并调节 scale|
|验证禁梯度|`with torch.inference_mode()`|:减少图与版本计数开销|
|保存 checkpoint|`torch.save({'model':..., 'optimizer':..., 'epoch':...},path)`|写文件|
|恢复|`checkpoint=torch.load(path,weights_only=True)`|返回字典|
|早停|`保存最佳 val 指标对应权重`|产生最佳 checkpoint|
|累计梯度|`loss=loss/accum_steps; backward; 每 N 步 step`|模拟更大批次|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
from torch import nn
m=nn.Linear(1,1); opt=torch.optim.SGD(m.parameters(),lr=.1)
x=torch.tensor([[1.]]); y=torch.tensor([[2.]])
m.train(); opt.zero_grad(); loss=nn.MSELoss()(m(x),y); loss.backward(); opt.step()
m.eval(); print(loss.ndim, m.training)
# 期望输出:
# 0 False
```
## 推理、批处理与导出（Inference, Batching, and Export）
推理必须复用训练预处理并稳定返回 schema。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|单批推理|`with inference_mode(): logits=model(batch)`|返回 Tensor|
|类别|`logits.argmax(dim=-1)`|返回整数索引|
|概率|`logits.softmax(dim=-1)`|返回概率 Tensor|
|Top-k|`torch.topk(prob,k,dim=-1)`|返回 values 与 indices|
|CPU 输出|`tensor.detach().cpu().numpy()`|返回 NumPy 数组|
|编译|`torch.compile(model,mode='default')`|返回优化模块，需核对图中断|
|导出程序|`torch.export.export(model,args)`|返回 ExportedProgram|
|ONNX 导出|`torch.onnx.export(model,args,path,...)`|写模型文件|
|动态批处理|`队列聚合到 max_batch 或 timeout`|提高吞吐但增加等待|
|量化|`torch.ao.quantization / torchao`|降低内存与推理成本，接口随版本演化|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
logits=torch.tensor([[1.,3.,2.]])
p=logits.softmax(-1); values,indices=p.topk(2,-1)
print(indices.tolist())
print(round(p.sum().item(),6))
# 期望输出:
# [[1, 2]]
# 1.0
```
## DeepSpeed、ZeRO 与混合精度（DeepSpeed, ZeRO, and Mixed Precision）
DeepSpeed 把模型、优化器、梯度累积和分布式通信封装为训练引擎（Engine）。ZeRO（Zero Redundancy Optimizer）把每张 GPU 上重复保存的训练状态拆分到多个进程，以换取更低的单卡显存占用。

|功能（Operation）|实际写法（Python / Command Usage）|返回值与状态变化|
|---|---|---|
|初始化引擎|`deepspeed.initialize(model=model, model_parameters=model.parameters(), config=cfg)`|返回引擎、优化器、数据加载器和调度器等对象|
|前向传播|`loss = engine(**batch).loss`|返回损失张量；由引擎管理模型设备|
|反向传播|`engine.backward(loss)`|累积梯度并执行混合精度缩放等逻辑|
|参数更新|`engine.step()`|在梯度累积边界更新参数、学习率和内部状态|
|ZeRO Stage 1|`zero_optimization.stage=1`|只分片优化器状态|
|ZeRO Stage 2|`zero_optimization.stage=2`|继续分片梯度，进一步降低显存|
|ZeRO Stage 3|`zero_optimization.stage=3`|继续分片模型参数，显存最低但通信和配置更复杂|
|有效批量大小|`micro_batch × accumulation × data_parallel_world_size`|得到一次优化器更新使用的总样本数|
|启用 FP16|`fp16.enabled=true`|以半精度训练并通常启用动态损失缩放|
|启用 BF16|`bf16.enabled=true`|使用更大指数范围；要求硬件支持|
|环境报告|`ds_report`|输出 DeepSpeed 扩展、依赖与加速器可用性|
|分布式启动|`deepspeed --num_gpus=4 train.py --deepspeed ds.json`|启动多进程训练，有 GPU 与文件副作用|
|保存检查点|`engine.save_checkpoint(path, tag=tag)`|各进程协同写入分片状态|
|恢复检查点|`engine.load_checkpoint(path, tag=tag)`|恢复模型、优化器和训练进度并返回加载信息|

### 最小引擎训练循环（Minimal Engine Training Loop）
```python
for batch in train_loader:
    outputs = engine(**batch)
    loss = outputs.loss
    engine.backward(loss)
    engine.step()
# 训练会更新模型与优化器状态；损失值取决于模型、数据和随机种子。
```
### 选型与排错（Selection and Troubleshooting）
- **先 Stage 2，后 Stage 3**：模型在 Stage 2 能放下时优先使用较简单的配置；只有参数本身成为主要显存瓶颈时再考虑 Stage 3。
- **批量大小不一致**：确认 `train_batch_size = train_micro_batch_size_per_gpu × gradient_accumulation_steps × data_parallel_world_size`，不要把微批量误当全局批量。
- **数据类型错误**：输入张量、模型参数和算子必须支持所选精度；FP16 与 BF16 不应同时启用，整数标签不能盲目转换为浮点半精度。
- **扩展编译失败**：先运行 `ds_report`，再核对 PyTorch、CUDA、编译器和驱动版本；未使用的可选扩展显示不可用不一定阻止训练。
- **保存后不能恢复**：所有 rank 必须参与检查点调用，并同时保存优化器、调度器、随机状态和数据进度；ZeRO 分片不能只复制单个 rank 文件。
- **公平比较**：比较普通 PyTorch 与 DeepSpeed 时固定模型、数据、有效批量大小、精度、预热轮次和同步计时方式。
## 调试、性能与确定性（Debugging, Performance, and Determinism）
先确认正确性，再剖析热点；同步计时 GPU。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|固定 CPU seed|`torch.manual_seed(seed)`|设置 CPU 及 CUDA 默认生成器种子|
|确定性算法|`torch.use_deterministic_algorithms(True)`|不确定操作抛错或警告|
|检查有限值|`torch.isfinite(x).all()`|返回布尔 Tensor|
|异常检测|`torch.autograd.set_detect_anomaly(True)`|增强反向诊断并变慢|
|梯度范数|`torch.nn.utils.clip_grad_norm_(params,inf)`|返回总范数且不裁剪|
|性能剖析|`torch.profiler.profile(...)`|返回 profiler 上下文|
|GPU 同步|`torch.cuda.synchronize()`|等待 CUDA 工作完成|
|峰值显存|`torch.cuda.max_memory_allocated()`|返回字节数|
|模型摘要|`逐层 hook 记录 shape`|返回自定义结构|
|小批过拟合|`在极小固定批次训练到近零损失`|验证模型、损失和优化链路|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import torch
x=torch.tensor([1.,float("nan")])
print(torch.isfinite(x).tolist())
print(torch.isfinite(x).all().item())
# 期望输出:
# [True, False]
# False
```
## 高频工作模式（Common Workflows）
- **基线（Baseline）**：先用最小可解释模型和极小数据过拟合测试，确认数据、损失和指标链路正确。
- **训练（Training）**：固定随机种子，记录数据版本、超参数、权重、指标与环境。
- **验证（Validation）**：验证集只用于选型与调参，最终测试集只评估一次。
- **推理（Inference）**：冻结随机行为、关闭梯度、统一预处理并验证输出 schema。
- **性能（Performance）**：先测量数据加载、计算、通信与后处理，再针对瓶颈优化。
- **上线（Production）**：增加输入校验、超时、批处理、监控、回滚和隐私保护。
## 常见错误与排查（Common Errors and Troubleshooting）
- **维度错误**：记录每个关键张量的 `shape/dtype/device`，按模块契约逐层核对。
- **训练不稳定**：检查输入归一化、标签范围、损失配对、学习率、梯度范数和 NaN/Inf。
- **指标虚高**：排查数据泄漏、重复样本、错误划分、阈值选择和只看单一平均指标。
- **推理漂移**：确保训练与服务使用同一 tokenizer、类别表、归一化统计和模型版本。
- **资源泄漏**：及时关闭文件、图像、客户端与进程；长任务持续观察 CPU/GPU/内存。
- **版本漂移**：固定主要依赖并以官方迁移说明处理弃用，不静默忽略警告。
## 相关详细笔记（Detailed Notes）
- [[01-PyTorch 数据集、变换与加载器（PyTorch Datasets, Transforms, and DataLoaders）]]
- [[02-PyTorch 模型工程结构与环境（PyTorch Model Engineering Structure and Environment）]]
- [[04-PyTorch 训练与评估循环（PyTorch Training and Evaluation Loops）]]
- [[05-PyTorch 模型持久化与推理（PyTorch Model Persistence and Inference）]]
- [[01-PyTorch 张量基础（PyTorch Tensor Fundamentals）]]
- [[02-PyTorch 自动微分与神经网络组件（PyTorch Autograd and Neural Network Components）]]
- [[03-PyTorch 线性回归实战（PyTorch Linear Regression）]]
- [[04-PyTorch 全连接网络与手机价格分类实践（PyTorch MLP and Phone-price Classification）]]
- [[04-DeepSpeed 分布式训练、ZeRO 与混合精度（DeepSpeed Distributed Training, ZeRO, and Mixed Precision）]]
- [[02-Transformer PyTorch 实现（Transformer PyTorch Implementation）]]
- [[04-HanLP 本地推理与 RESTful 调用（HanLP Native and RESTful Usage）]]
- [[02-FastAPI 机器学习推理服务模板（FastAPI ML Inference Service Template）]]
- [[03-Flask 机器学习推理服务模板（Flask ML Inference Service Template）]]
## 官方参考（Official References）
- [PyTorch Data 文档](https://docs.pytorch.org/docs/stable/data.html)
- [TorchAudio 文档](https://docs.pytorch.org/audio/stable/)
- [DeepSpeed 入门文档](https://www.deepspeed.ai/getting-started/)
- [PyTorch 文档](https://docs.pytorch.org/docs/stable/)
