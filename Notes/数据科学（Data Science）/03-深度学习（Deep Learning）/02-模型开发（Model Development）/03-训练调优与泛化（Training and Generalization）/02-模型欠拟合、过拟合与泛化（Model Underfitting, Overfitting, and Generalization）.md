---
title: 模型欠拟合、过拟合与泛化（Model Underfitting, Overfitting, and Generalization）
aliases:
  - Model Generalization
  - Underfitting and Overfitting
tags:
  - data-science/deep-learning/generalization
  - data-science/model-training
status: published
created: 2026-08-11
published_at: 2026-08-11
---
# 模型欠拟合、过拟合与泛化（Model Underfitting, Overfitting, and Generalization）
## 1. 泛化诊断（Generalization Diagnosis）

|状态（State）|训练集表现（Training Performance）|验证/测试表现（Validation/Test Performance）|典型性质（Typical Property）|
|---|---|---|---|
|欠拟合（Underfitting）|差|差|高偏差（High Bias），模型或训练不足|
|适当拟合（Appropriate Fit）|好|接近训练集且可接受|偏差与方差平衡|
|过拟合（Overfitting）|很好|明显差于训练集|高方差（High Variance），记忆噪声|

- 测试集应只用于最终无偏评估；日常诊断使用验证集。
- “训练误差高/低”必须相对于任务基线、数据噪声和可达到上限判断。
## 2. 欠拟合原因与对策（Underfitting Causes and Remedies）
### 2.1 模型容量不足（Insufficient Model Capacity）
- 网络层数、宽度、通道数或特征交互不足，假设空间无法表达目标规律。
- 增加深度、宽度、通道或更合适架构，但先确认数据和优化没有错误。
### 2.2 预处理与特征提取不足（Insufficient Preprocessing or Features）
- 特征量纲差异、未归一化、颜色或尺寸处理不一致会增加优化难度。
- 改善标准化、输入质量和卷积/特征设计。
### 2.3 训练未收敛（Insufficient Optimization）
- epoch 太少、学习率过小、调度不合理或优化器配置不匹配。
- 延长训练、绘制损失曲线、调学习率并检查梯度，而不是立即增大模型。
### 2.4 梯度异常（Gradient Pathology）
- 初始化不当、饱和激活、过深链路或缺少残差/归一化导致梯度消失或爆炸。
- 选择 Xavier/Kaiming、ReLU 族、BatchNorm 或残差连接，并监控梯度范数。
### 2.5 正则化过强（Excessive Regularization）
- 过大 weight decay、过高 Dropout 概率、过强数据增强会限制拟合能力。
- 逐项减弱正则化，通过验证集区分“拟合不足”和“泛化改善”。
## 3. 过拟合原因（Overfitting Causes）
- 模型容量相对于有效数据量过大。
- 训练数据少、标签噪声高或分布覆盖不足。
- 训练过久，模型开始记忆训练噪声。
- 数据泄漏（Data Leakage）让训练/验证指标失真。
- 训练与部署分布偏移（Distribution Shift）。
## 4. L2 正则化与权重衰减（L2 Regularization and Weight Decay）
### 4.1 目标函数（Objective）
$$
L_{new}=L_{data}+\frac{\lambda}{2}\sum_i w_i^2
$$
- 惩罚大权重，倾向于更平滑、较低复杂度的决策函数。
- 通常不对偏置和归一化层缩放/偏移参数机械施加相同衰减；可通过参数组细分。
- SGD 中经典 L2 惩罚与 weight decay 可对应；Adam 等自适应优化器中，耦合 L2 与解耦权重衰减的行为不同，常用 AdamW 表达解耦方案。
```python
import torch
from torch import nn

model = nn.Linear(8, 2)
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=1e-3,
    weight_decay=1e-2,
)
print(type(optimizer).__name__)  # 输出: AdamW
```
## 5. Dropout
### 5.1 机制（Mechanism）
- 训练时以概率 $p$ 独立将部分元素置 0，并对保留元素按 $1/(1-p)$ 缩放，使期望尺度保持不变。
- 评估模式中 Dropout 是恒等映射，因此必须正确调用 `model.train()`/`model.eval()`。
- 随机子网络可减少特征共适应（Co-adaptation），具有类似集成的正则化效果。
### 5.2 回归任务边界（Regression Boundary）
- 没有“使用 MSE/L2 损失就绝对禁止 Dropout”的普遍规则。
- 但直接在连续输出层前随机丢弃输出或关键低维表示，可能引入尺度噪声、降低精确回归稳定性。
- 更稳妥做法是在隐藏层小比例试验，并通过验证误差、校准和重复运行判断；若训练与验证都变差应降低或移除。
```python
import torch
from torch import nn

dropout = nn.Dropout(p=0.5)
x = torch.ones(1000)
dropout.train()
training_output = dropout(x)
dropout.eval()
evaluation_output = dropout(x)
print(evaluation_output.equal(x))  # 输出: True
print(training_output.shape)       # 输出: torch.Size([1000])
```
## 6. 数据增强（Data Augmentation）
- 图像可用旋转、裁剪、翻转、颜色抖动等标签保持变换生成新观察。
- 增强不是简单“降低噪声占比”；其核心是编码任务不变性并扩大有效数据分布。
- 不保持标签语义的增强会制造标签噪声，例如文字垂直翻转、检测框未同步变换。
- 训练与推理增强边界见 [[01-PyTorch 数据集、变换与加载器（PyTorch Datasets, Transforms, and DataLoaders）]]。
## 7. 提前停止（Early Stopping）
- 同时跟踪训练和验证指标；验证性能连续若干轮未改善时停止。
- **patience** 控制允许连续不改善的 epoch 数；**min_delta** 控制最小有效改善。
- 应恢复最佳验证 checkpoint，而不是直接使用最后一轮权重。
- 多次试验反复选择验证集会对验证集过拟合，最终仍需独立测试集。
## 8. 归一化层的泛化效应（Generalization Effects of Normalization）
- BatchNorm 使用 mini-batch 统计时引入随机性，可能产生轻量正则化效果，但其主要职责是改善优化和信号尺度。
- 小 batch 的统计不稳定时可考虑 GroupNorm（Group Normalization, GN）或 LayerNorm（Layer Normalization, LN）。
- 序列模型常用 LayerNorm；风格迁移常见 InstanceNorm（Instance Normalization, IN）；具体选择取决于张量轴和任务。
- 不应把 BatchNorm 当作 Dropout 的普遍替代品，二者机制不同。
## 9. CNN 完整工作流（Complete CNN Workflow）
```text
数据输入
  → 去均值与标准化：平衡特征尺度、改善优化
  → 数据增强：编码不变性、抑制过拟合
卷积层
  → 局部感受野与参数共享：降低参数量、提取多通道特征
激活层
  → 引入非线性；ReLU 死区时评估 LeakyReLU/ELU
归一化层
  → 稳定信号尺度；按 batch 和任务选择 BN/LN/IN/GN
池化或步幅卷积
  → 下采样空间维度；Max/Avg 的信息偏好不同
初始化与训练
  → 激活匹配的 Xavier/Kaiming、损失、优化器与验证
泛化与输出
  → weight decay、Dropout、增强、Early Stopping 与任务后处理
```
## 10. 决策矩阵（Decision Matrix）

|症状（Symptom）|优先检查与方案（Priority Checks and Remedies）|原理（Rationale）|
|---|---|---|
|网络加深后不收敛|梯度/激活统计、Kaiming、BatchNorm、残差连接|稳定前向与反向信号路径|
|batch size 只有 2 或 4|评估 GroupNorm 或 LayerNorm|减少对 batch 统计的依赖|
|训练好、验证差|数据泄漏检查、增强、weight decay、Dropout、Early Stopping|降低方差并扩大有效数据覆盖|
|训练和验证都差|先排查代码/数据，再增大容量、延长训练、调学习率|避免把优化错误误判为容量不足|
|回归损失不下降|检查输出/目标形状、尺度、学习率和输出附近 Dropout|防止广播、尺度噪声与不稳定更新|
|分类头参数过大|全局平均池化（Global Average Pooling）|把 $H×W$ 压缩为 $1×1$，降低全连接参数|

## 11. 泛化实验原则（Generalization Experiment Principles）
- 每次只改变少量变量，记录随机种子、数据划分、版本和硬件。
- 同时绘制训练/验证损失和主要指标，不能只看一个最终数字。
- 报告多次运行均值与波动，避免把单次随机优势当成结论。
- 保留最简单基线，确认复杂策略带来可重复增益。
## 参考资料（References）
- [`torch.nn.Dropout` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.Dropout.html)
- [PyTorch 正则化与优化基础教程](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
