---
title: DeepSpeed 分布式训练、ZeRO 与混合精度（DeepSpeed Distributed Training, ZeRO, and Mixed Precision）
tags:
  - data-science/deep-learning/deepspeed
  - distributed-training
status: published
created: 2026-09-10
published_at: 2026-09-10
verified_at: 2026-09-10
---
# DeepSpeed 分布式训练、ZeRO 与混合精度（DeepSpeed Distributed Training, ZeRO, and Mixed Precision）
## 1. DeepSpeed 解决什么问题
DeepSpeed 是分布式深度学习训练优化库，主要价值包括数据并行（Data Parallelism）、ZeRO 显存优化、混合精度（Mixed Precision）、梯度累积（Gradient Accumulation）、通信优化和状态卸载（Offload）。
- 适合：模型或优化器状态超出单卡显存、多 GPU 训练、长时间训练、显存或通信成为瓶颈。
- 通常不必使用：小模型、单 GPU 普通训练、仅推理、RAG 编排或简单云 API 调用。
- DeepSpeed 不等于 ZeRO；ZeRO 是 DeepSpeed 可选的显存优化功能之一。
> [!tip] 大白话理解（Plain-language Intuition）
> 普通数据并行像每个工人都保存一整套工具、说明书和中间记录，只是处理不同数据。ZeRO 会把重复保存的重物拆开分给工人，需要时再通信取回，从而让更大的模型装进多张卡。
## 2. 训练状态与 ZeRO 阶段
混合精度 Adam 类训练常同时保存参数、梯度、主参数副本和优化器状态。ZeRO 按阶段切分这些重复状态：

|阶段|切分内容|显存节省|主要代价|
|---|---|---|---|
|Stage 0|不启用 ZeRO|无 ZeRO 节省|实现最简单|
|Stage 1|优化器状态（Optimizer States）|减少优化器副本|更新时需要通信|
|Stage 2|优化器状态 + 梯度（Gradients）|进一步节省|通信和实现复杂度增加|
|Stage 3|优化器状态 + 梯度 + 参数（Parameters）|节省最多，可训练更大模型|参数按需聚合，通信与调试成本最高|

单 GPU 可以学习 API 和配置，但无法体现“把状态分到多卡”的核心收益。实际显存还包含激活、缓冲区、通信工作区、碎片和临时张量，不能只用参数量推断峰值显存。
## 3. 有效批次大小（Effective Batch Size）
$$
B_{effective}=B_{micro}\times N_{data\ parallel}\times N_{accumulation}
$$
- `train_micro_batch_size_per_gpu`：每张 GPU 单次前向/反向处理的样本数。
- 数据并行规模（Data-parallel World Size）：并行参与训练的 GPU 进程数。
- `gradient_accumulation_steps`：累积多少个微批次后执行一次参数更新。
> [!tip] 大白话理解（Plain-language Intuition）
> 显存一次只能装 8 个样本时，可以连续算 4 次、先把梯度攒起来再更新，效果近似一次看 32 个样本；多卡时还要乘上卡数。
改变有效批次大小通常需要重新评估学习率、调度器、日志步数和评估频率，不能只改累积步数。
## 4. 从 PyTorch 训练循环迁移
核心变化是用 DeepSpeed Engine 包装模型，并让 Engine 接管反向传播与更新。
```python
import deepspeed

model = build_model()
train_loader = build_train_loader()

engine, optimizer, _, scheduler = deepspeed.initialize(
    model=model,
    model_parameters=model.parameters(),
    config="ds_config.json",
)

for inputs, labels in train_loader:
    inputs = inputs.to(engine.device)
    labels = labels.to(engine.device)

    logits = engine(inputs)
    loss = compute_loss(logits, labels)
    engine.backward(loss)
    engine.step()
```
示例省略了具体模型与数据，不产生固定输出。`engine.step()` 会根据配置决定是否到达梯度累积边界并真正更新参数。
### 4.1 必须理解的对象
- `engine.module`：被包装的原始模型。
- `engine.device`：当前进程使用的设备。
- `engine.backward(loss)`：替代普通 `loss.backward()`，让 DeepSpeed 处理缩放、分区和通信。
- `engine.step()`：替代手工 `optimizer.step()`、`scheduler.step()` 和清零流程的常见组合。
- 返回的优化器和调度器是否为空，取决于它们由配置创建还是由调用方传入。
## 5. 最小配置与字段关系
```json
{
  "train_micro_batch_size_per_gpu": 8,
  "gradient_accumulation_steps": 4,
  "optimizer": {
    "type": "AdamW",
    "params": {
      "lr": 0.0001,
      "weight_decay": 0.01
    }
  },
  "fp16": {
    "enabled": true
  },
  "zero_optimization": {
    "stage": 2
  }
}
```
配置控制训练行为，不提供固定控制台输出。
- 不要同时在 Python 和 JSON 中定义互相冲突的优化器、批次或调度器设置。
- 某些集成支持用 `"auto"` 让上层框架填入值；纯 DeepSpeed 配置是否支持应按版本核对。
- 配置中的批次乘积必须与启动的进程数一致，否则可能在初始化时报错。
## 6. FP16、BF16 与数据类型一致性
- FP16 节省显存并可能提高吞吐，但数值范围较窄，通常需要损失缩放（Loss Scaling）。
- BF16 与 FP32 具有相近指数范围，稳定性通常更好，但需要硬件支持。
- 输入浮点张量应与模型计算类型一致；分类标签通常仍为 `torch.long`，不能机械转换为 FP16。
```python
import torch

parameter_dtype = next(engine.module.parameters()).dtype
inputs = inputs.to(device=engine.device, dtype=parameter_dtype)
labels = labels.to(device=engine.device, dtype=torch.long)
```
若模型权重为 Half、输入仍为 Float，线性层或卷积可能报 `mat1 and mat2 must have the same dtype` 一类错误。修复时检查模型、输入、自动混合精度上下文和自定义算子，不要把所有张量统一强转为半精度。
## 7. 启动与环境检查
```bash
ds_report
deepspeed --num_gpus=2 train.py --deepspeed_config ds_config.json
```
这些命令依赖具体硬件和环境，不提供固定输出。
- `ds_report` 用于报告 PyTorch、CUDA、编译器和 DeepSpeed 可选算子状态。
- 多个可选算子显示未预编译不等于核心框架不可用；某些算子会在实际需要时即时编译（JIT Compilation）。
- `nvcc`、驱动支持的 CUDA、PyTorch 构建所用 CUDA 和系统工具链是不同层次，必须分别核对。
- 本机没有 CUDA 时不应假装完成 GPU 训练验证；可做静态检查或 CPU 验证，并在 GPU 环境进行最终测试。
## 8. 评估、保存与恢复
- 评估时使用 `engine.eval()` 和 `torch.inference_mode()`；完成后恢复 `engine.train()`。
- 分区训练中不要假设每个进程都持有完整参数；保存检查点应使用 DeepSpeed 提供的检查点接口。
- ZeRO Stage 3 导出完整权重可能需要聚合分区参数，会增加内存和时间。
- 恢复训练除模型权重外还需要优化器、调度器、随机状态、全局步数和数据采样状态。
- 只在主进程打印、写日志或保存非分布式工件，避免多进程竞争与重复输出。
## 9. 公平基准（Fair Benchmark）
比较普通 PyTorch 与 DeepSpeed 时保持一致：模型、数据、随机种子、有效批次、精度、优化器、学习率调度、预热轮数和测量区间。
- 吞吐：样本/秒或 Token/秒。
- 峰值显存：按每张卡记录，并注明是否包含初始化峰值。
- 收敛：比较相同步数或相同 Token 下的训练/验证指标。
- 通信：多卡扩展效率，不只看单卡速度。
小模型单 GPU 中，初始化、封装和通信开销可能使 DeepSpeed 更慢；这不是框架失败，而是应用场景不匹配。
## 10. 常见失败模式
1. `CUDA out of memory`：先记录峰值来源，再减小微批次、启用累积/检查点或提高 ZeRO 阶段。
2. 数据类型不匹配：检查输入、权重、归一化层、自定义损失和标签类型。
3. 配置批次不一致：核对微批次、累积步数、数据并行规模与总批次。
4. 多进程挂起：检查所有 Rank 是否走过相同集合通信路径，以及网络、端口和 NCCL 日志。
5. 可选算子编译失败：核对编译器、CUDA Toolkit、PyTorch ABI 和写权限；若当前训练不使用该算子，不要误诊为全部 DeepSpeed 不可用。
6. 云 GPU 成本失控：训练完成或排错暂停时停止计费实例，检查持久化盘与快照是否单独计费。
## 11. 参考资料
- [DeepSpeed Getting Started](https://www.deepspeed.ai/getting-started/)
- [DeepSpeed ZeRO 教程](https://www.deepspeed.ai/tutorials/zero/)
- [[02-PyTorch 自动微分与神经网络组件（PyTorch Autograd and Neural Network Components）]]
- [[02-模型欠拟合、过拟合与泛化（Model Underfitting, Overfitting, and Generalization）]]
