---
title: "Optional 扩展技能（Optional Advanced Skills）"
aliases:
  - "Optional Advanced Skills"
tags:
  - career/llm-application-engineer
  - interview/optional
status: published
created: 2026-08-27
updated: 2026-08-27
---
# Optional 扩展技能（Optional Advanced Skills）
> [!tip] 导航（Navigation）
> [[00-概览（Overview）]]｜主线终点：[[10-S9 项目、面试与求职表达（Projects, Interviews and Job Search）]]｜[[大模型应用工程师学习计划]]
## 1. Java、Spring Boot 与 Python AI 服务（Java, Spring Boot, and Python AI Services）
### 概念与原理（Concept and Mechanism）
- Java 集合、异常、泛型和并发是 Spring 服务基础；Spring Boot 通过自动配置、依赖注入和约定减少服务初始化代码。
- Java AI 网关可负责认证、订单或企业业务，Python 服务负责模型、数据和推理。两者通过版本化 HTTP/gRPC 契约通信，不共享进程内对象。
- JPA 适合实体与关系映射，MyBatis 适合需要显式控制 SQL 的场景；选择取决于查询复杂度、团队习惯和可观测性要求。

### 最小代码示例（Minimal Example）
```java
public record InferenceRequest(String prompt, int maxTokens) {
    public InferenceRequest {
        if (prompt == null || prompt.isBlank()) {
            throw new IllegalArgumentException("prompt must not be blank");
        }
        if (maxTokens < 1 || maxTokens > 2048) {
            throw new IllegalArgumentException("maxTokens is out of range");
        }
    }
}
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：Java 服务调用 Python 模型服务时如何避免强耦合？**

**参考答案：**定义独立版本化 Schema、超时、错误码和幂等语义；通过客户端适配层隔离传输细节；使用契约测试验证两端兼容。不要让 Java 代码依赖 Python 内部类名或未版本化的任意 JSON。

## 2. vLLM 与推理服务（vLLM and Model Serving）
### 概念与原理（Concept and Mechanism）
- vLLM 面向大语言模型高吞吐推理，核心目标是高效管理模型权重、请求批处理和键值缓存（Key-Value Cache, KV Cache）。
- 连续批处理（Continuous Batching）在已有请求生成过程中动态加入新请求，减少 GPU 空闲；调度仍需在吞吐、公平性和单请求延迟之间权衡。

### 最小代码示例（Minimal Example）
```python
from vllm import LLM, SamplingParams

model = LLM(model="your-model-id")
outputs = model.generate(
    ["用一句话解释 RAG。"],
    SamplingParams(temperature=0.2, max_tokens=64),
)
print(outputs[0].outputs[0].text)
```
该示例会下载或加载模型并占用显存，输出依赖模型、版本、硬件与采样实现。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么连续批处理能提高吞吐？**

**参考答案：**不同请求生成长度不同，静态批次必须等待最长请求完成；连续批处理可在请求结束后立即释放槽位并加入新请求，提高 GPU 计算与显存利用率，但调度和尾延迟需要额外控制。

## 3. KV Cache、显存、吞吐与延迟（KV Cache, VRAM, Throughput, and Latency）
### 概念与原理（Concept and Mechanism）
- 自回归生成每一步都需要此前 Token 的注意力键和值。KV Cache 保存这些中间结果，避免反复计算历史 Token，但显存随并发、序列长度、层数、头数和精度增长。
- 吞吐量（Throughput）衡量单位时间完成的 Token 或请求，延迟（Latency）衡量单请求等待。增大批次通常提高吞吐，但可能增加排队和首 Token 延迟。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：模型权重已经能放入 GPU，为什么仍会 OOM？**

**参考答案：**运行还需要 KV Cache、激活、临时工作区和框架开销；长上下文与高并发会显著扩大 KV Cache。容量估算不能只看权重文件大小。

## 4. 量化（Quantization）
### 概念与原理（Concept and Mechanism）
- 量化用更少位数表示权重、激活或 KV Cache，以减少内存与带宽，有时提高吞吐；代价可能是精度下降、校准成本、算子限制和硬件兼容问题。
- 权重量化不等于 KV Cache 量化，也不保证所有硬件都加速。必须用目标任务、延迟、吞吐和显存实测。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：4-bit 模型一定比 16-bit 模型快吗？**

**参考答案：**不一定。它通常更省显存，但速度取决于量化格式、反量化开销、内核、批次和硬件支持；某些配置只是把模型放得下，不会获得更高吞吐。

## 5. Kubernetes 基础（Kubernetes Fundamentals）
### 概念与原理（Concept and Mechanism）
- Pod 是调度单元，Deployment 管理无状态副本与滚动更新，Service 提供稳定访问，ConfigMap/Secret 注入配置，PersistentVolume 支撑持久数据。
- GPU 推理还涉及节点标签、设备插件、资源请求、模型加载时间、就绪检查和滚动升级容量。Kubernetes 解决编排问题，不自动解决模型质量和成本。

### 最小代码示例（Minimal Example）
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: llm-api
  template:
    metadata:
      labels:
        app: llm-api
    spec:
      containers:
        - name: api
          image: example/llm-api:1.0.0
          ports:
            - containerPort: 8000
```
部署会创建集群资源，结果依赖镜像、集群和权限配置。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么模型服务的就绪检查可能需要更长时间？**

**参考答案：**进程启动后还要加载权重、分配显存和预热内核。如果过早接流量会大量失败；就绪检查应在模型真正可服务后成功，同时避免因短暂下游故障反复重启进程。

## 6. 数学基础（Mathematical Foundations）
### 概念与原理（Concept and Mechanism）
- 线性代数重点包括向量、矩阵乘法、线性变换、范数、特征分解和低秩近似；概率统计重点包括条件概率、期望、方差、最大似然、交叉熵、抽样与置信区间。
- 面试中应把公式与模型行为连接，例如点积注意力、余弦相似度、交叉熵和 LoRA 低秩分解。

### 最小代码示例（Minimal Example）
```python
import numpy as np

matrix = np.array([[1.0, 2.0], [3.0, 4.0]])
vector = np.array([1.0, 0.0])
print((matrix @ vector).tolist())  # 输出: [1.0, 3.0]
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：矩阵乘法在神经网络中表达什么？**

**参考答案：**线性层通过矩阵把输入特征组合并映射到新空间；每个输出维度是输入与一组权重的加权和。非线性激活使多层网络不退化为单个线性变换。

## 7. Hugging Face Trainer（Hugging Face Trainer）
### 概念与原理（Concept and Mechanism）
- `Trainer` 封装批处理、前向、损失、反向、优化、评估、保存和分布式训练。它减少样板代码，但用户仍需理解数据整理、模型输出契约、指标、检查点和训练参数。

### 最小代码示例（Minimal Example）
```python
from transformers import Trainer, TrainingArguments

arguments = TrainingArguments(
    output_dir="./checkpoints",
    per_device_train_batch_size=2,
    num_train_epochs=1,
)
trainer = Trainer(model=model, args=arguments, train_dataset=train_dataset)
```
示例依赖预先定义的 `model` 与 `train_dataset`，训练会写入检查点并消耗计算资源。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：使用 Trainer 是否意味着不需要懂训练循环？**

**参考答案：**不是。出现 Loss 异常、Padding 错误、梯度累积、指标偏差或检查点问题时，必须理解它封装的前向、反向、批次和评估流程才能定位。

## 8. LoRA 与 QLoRA（LoRA and QLoRA）
### 概念与原理（Concept and Mechanism）
- 低秩适配（Low-Rank Adaptation, LoRA）冻结基础权重，在目标线性层加入两个低秩矩阵，训练参数量显著减少。
- QLoRA 通常把基础模型以低位权重加载并在其上训练 LoRA 适配器，进一步降低显存；量化基础权重通常保持冻结，计算精度与量化格式仍需配置。

> [!tip] 大白话理解（Plain-language Intuition）
> 全量微调像重写整本书，LoRA 像在关键章节增加一组可训练批注；QLoRA 还把原书压缩保存，从而减少显存，但批注是否有效仍要通过任务评测验证。

### 最小代码示例（Minimal Example）
```python
from peft import LoraConfig, TaskType, get_peft_model

config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],
)
peft_model = get_peft_model(base_model, config)
```
示例依赖兼容的 `base_model`；目标模块名称因模型架构而异，必须检查实际模块。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：LoRA 的秩 `r` 越大越好吗？**

**参考答案：**不一定。更大 `r` 增加表达能力、训练参数、显存和过拟合风险；应依据任务复杂度、数据量和评测选择。目标层、学习率和数据质量同样重要。

## 9. SFT 数据、微调评测与 DeepSpeed（SFT Data, Fine-tuning Evaluation, and DeepSpeed）
### 概念与原理（Concept and Mechanism）
- 监督微调（Supervised Fine-tuning, SFT）数据应包含清晰任务、输入和理想回答，去重、脱敏并控制模板一致性。训练/验证/测试按来源隔离，避免近重复泄漏。
- 微调前后必须在独立任务集比较质量、安全、格式遵循、遗忘、延迟和成本；训练 Loss 下降不等于实际应用提升。
- DeepSpeed 通过 ZeRO 等技术在设备间分片优化器状态、梯度和参数，降低单卡内存，但增加通信、配置和故障排查复杂度。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：什么时候不应该微调？**

**参考答案：**知识频繁变化、数据量和质量不足、问题可通过 RAG 或 Prompt 解决、缺少可靠评测或无法承担训练运维成本时不应急于微调。先建立基线和评测，再证明微调必要。

## 10. 论文阅读与实验复现（Paper Reading and Experiment Reproduction）
### 方法（Method）
- 先明确研究问题、基线、核心方法、假设和主要结论，再读公式与实现细节。
- 区分论文报告配置与代码仓库默认配置；记录数据版本、随机种子、硬件、依赖、指标计算和偏差。
- 复现失败也要报告与论文的差异和排查证据，不能只挑选成功结果。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：复现实验结果低于论文，如何排查？**

**参考答案：**依次核对数据处理、划分、模型和检查点、超参数、训练步数、指标实现、随机性、依赖版本和硬件精度；先复现更小基线，再逐步接近论文配置。

## 11. Dify、Coze、LangChain 与 LlamaIndex（Low-code and RAG Platforms）
### 概念与原理（Concept and Mechanism）
- Dify/Coze 提供可视化编排、模型连接和发布能力；LangChain/LlamaIndex 提供代码层组件与工作流抽象。深入学习应能解释它们封装的解析、检索、状态、工具、追踪和部署步骤。
- 同时掌握多个框架的目标不是记忆 API，而是比较数据契约、可测试性、可观测性、版本稳定性和供应商锁定。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：你如何证明自己不是只会拖拽平台？**

**参考答案：**展示同一任务的代码基线，解释平台节点映射到哪些解析、检索、模型和工具接口，并能定位一次失败在平台内外的具体边界。

## 12. 多模型供应商与复杂多 Agent（Multiple Providers and Multi-agent Systems）
### 概念与原理（Concept and Mechanism）
- 多供应商接入需要能力发现、错误映射、价格与速率限制、模型版本和数据边界；不能静默假设参数完全等价。
- 多 Agent 把职责分配给多个模型角色，会增加消息、状态、一致性、成本和评测难度。只有可证明的角色分工和并行收益才值得采用。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：多 Agent 为什么不一定比单 Agent 好？**

**参考答案：**多个 Agent 可能重复工作、传播错误、产生冲突并增加 Token 与延迟。应先用单 Agent 或固定工作流建立基线，再用任务成功率、成本和延迟证明多 Agent 的增益。

## 13. ViT 与扩展算法（Vision Transformer and Advanced Algorithms）
### ViT（Vision Transformer）
- ViT 把图像切成 Patch，映射为 Token 序列并使用 Transformer 编码。位置编码保留空间顺序，分类 Token 或池化表示用于分类。
- **面试问题：ViT 为什么通常更依赖数据或预训练？**
- **参考答案：**CNN 内置局部性和平移相关归纳偏置，ViT 的结构先验更弱，需要更多数据学习这些规律；大规模预训练后，ViT 可获得强表征能力。
- **相关笔记**：[[01-Transformer 架构与注意力（Transformer Architecture and Attention）]]。

### 动态规划、图与并查集（Dynamic Programming, Graphs, and Disjoint Sets）
- 动态规划通过状态、转移和计算顺序复用重叠子问题；图算法处理节点关系与路径；并查集高效维护动态连通分量。
- **面试问题：什么时候使用动态规划？**
- **参考答案：**问题具有可定义状态、重叠子问题和最优子结构，并能从较小状态转移到目标状态时适合；如果状态无法完整表达未来决策，转移就可能错误。
- **相关笔记**：[[07-优先队列、堆与并查集（Priority Queues, Heaps, and Disjoint Sets）]]、[[10-图结构、遍历与最短路径（Graphs, Traversal, and Shortest Paths）]]、[[11-贪心、动态规划与分治（Greedy, Dynamic Programming, and Divide and Conquer）]]。

## 参考资料（References）
- [[大模型应用工程师学习计划]]
- [vLLM 官方文档](https://docs.vllm.ai/)
- [Hugging Face Trainer](https://huggingface.co/docs/transformers/trainer)
- [Hugging Face PEFT](https://huggingface.co/docs/peft/en/index)
- [Hugging Face PEFT 量化指南](https://huggingface.co/docs/peft/developer_guides/quantization)
