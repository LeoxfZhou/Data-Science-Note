---
title: 人工神经网络与前向传播（Artificial Neural Networks and Forward Propagation）
aliases:
  - Neural Network Fundamentals
  - Multilayer Perceptron
tags:
  - data-science/deep-learning/fundamentals
  - data-science/deep-learning/neural-network
status: published
created: 2026-08-11
published_at: 2026-08-12
---
# 人工神经网络与前向传播（Artificial Neural Networks and Forward Propagation）
## 1. 定义与定位（Definition and Positioning）
- 人工神经网络（Artificial Neural Network, ANN）是由可学习连接组成的计算模型；神经元也称节点（Node）或单元（Unit）。
- 网络通过前向传播（Forward Propagation）把输入逐层变换为预测，再由损失函数（Loss Function）衡量预测与目标的差异。
- “仿生”只提供直觉：树突可类比输入，突触强度可类比权重，细胞体可类比聚合与激活，轴突可类比输出；真实生物神经系统比该模型复杂得多。
## 2. 人工神经元（Artificial Neuron）
### 2.1 仿射变换与激活（Affine Transformation and Activation）
对输入向量 $\mathbf{x}$、权重 $\mathbf{w}$ 和偏置 $b$：
$$
z=\mathbf{w}^{\mathsf T}\mathbf{x}+b,\qquad a=f(z)
$$
- **内部状态值（Pre-activation）** $z$：输入的加权和加偏置。
- **激活值（Activation）** $a$：$z$ 经激活函数（Activation Function）后的输出。
- 反向传播中还会出现激活梯度 $\partial L/\partial a$ 与内部状态梯度 $\partial L/\partial z$；二者由链式法则连接。
### 2.2 权重与偏置（Weight and Bias）
- 权重决定每个输入对当前单元的贡献方向与强度。
- 偏置平移决策边界，使神经元不必被迫经过原点。
- 输入数据不是模型参数；参数由训练更新，输入只参与当前前向计算。
## 3. 感知器（Perceptron）
- 经典感知器对加权和应用阶跃函数（Step Function），输出离散类别，适合线性可分二分类。
- 单个感知器可表达逻辑与（AND）和逻辑或（OR），不能表达异或（XOR）这类线性不可分关系。
- 阶跃函数不连续、几乎处处梯度为 0，不能直接用现代梯度下降完成平滑的小步优化。
- 感知器（Perceptron）与支持向量机（Support Vector Machine, SVM）都是线性判别模型，但二者的目标函数、间隔原则和训练算法不同，不存在简单的等同或包含关系。
## 4. 可微神经元与非线性（Differentiable Neurons and Nonlinearity）
- Sigmoid 神经元把离散阶跃替换为连续可微映射，使参数的小变化通常对应输出的小变化。
$$
\sigma(z)=\frac{1}{1+e^{-z}}
$$
- 若层间没有非线性，任意多个仿射层仍可合并为一个仿射层：
$$
W_2(W_1x+b_1)+b_2=(W_2W_1)x+(W_2b_1+b_2)
$$
- 因此网络深度只有与非线性、归一化、门控或其他非仿射操作结合时，才会扩展可表达函数族。
## 5. 前馈全连接网络（Feedforward Fully Connected Network）
### 5.1 层级组成（Layer Composition）
- **输入层（Input Layer）**：接收图像、文本、声音或表格特征；通常不把输入本身算作有参数的计算层。
- **隐藏层（Hidden Layer）**：执行仿射变换与非线性特征变换。
- **输出层（Output Layer）**：按任务产生回归值、二分类 Logit 或多分类 Logits。
- 前馈网络的信息沿输入到输出方向传播；同一标准全连接层内的神经元互不连接，相邻层之间通常全连接。
### 5.2 张量形状（Tensor Shape）
- 对批量输入 $X\in\mathbb{R}^{N\times d_{in}}$、权重 $W\in\mathbb{R}^{d_{out}\times d_{in}}$、偏置 $b\in\mathbb{R}^{d_{out}}$：
$$
Z=XW^{\mathsf T}+b\in\mathbb{R}^{N\times d_{out}}
$$
- `nn.Linear` 允许任意前导维度，只要求输入最后一维等于 `in_features`；“全连接层只能接收二维数据”不是该 API 的限制。

> [!tip] 大白话理解（Plain-language Intuition）
> 一层神经网络可以想成“先按权重给每个输入打分并求和，再通过激活函数决定这个分数怎样传下去”。多层网络就是反复执行这个过程：前面的层逐步提取特征，后面的层再利用这些特征完成预测。
### 5.3 参数量（Parameter Count）
- 一个 `Linear(d_in, d_out)` 含 $d_{out}d_{in}$ 个权重；若启用偏置，再加 $d_{out}$ 个参数。
- 对 `3 → 3 → 2 → 2` 网络：$3×3+3=12$，$2×3+2=8$，$2×2+2=6$，总计 26 个可训练参数。
```python
from torch import nn

model = nn.Sequential(
    nn.Linear(3, 3),
    nn.Sigmoid(),
    nn.Linear(3, 2),
    nn.ReLU(),
    nn.Linear(2, 2),
)
print(sum(parameter.numel() for parameter in model.parameters()))  # 26
```
## 6. 深度、宽度与容量（Depth, Width, and Capacity）
- 浅层网络（Shallow Network）通常只有少量隐藏层；深度神经网络（Deep Neural Network, DNN）包含更多层级变换，但没有统一的“超过几层”定义。
- 万能逼近定理（Universal Approximation Theorem）在特定激活和紧致域等条件下说明足够宽的单隐藏层网络可以逼近连续函数；它不说明所需宽度、训练算法、样本复杂度或泛化质量。
- 深层网络可通过层级复用更高效地表达某些组合结构，例如视觉中从边缘到局部再到对象。
- 增加深度或宽度提高容量（Capacity），同时可能增加优化难度、计算成本与过拟合风险；容量必须与数据量、噪声、正则化和任务结构共同选择。
- 高维图像若直接展平送入全连接网络，会产生大量参数并丢失空间局部性；卷积神经网络（Convolutional Neural Network, CNN）利用局部连接与参数共享更合适。
## 7. 训练闭环（Training Loop Concept）
1. 前向传播得到预测。
2. 损失函数比较预测与目标。
3. 反向传播计算每个参数的梯度。
4. 优化器按梯度和状态更新参数。
5. 重复多个批次（Batch）与轮次（Epoch），并用验证集监测泛化。
## 8. 关联笔记（Related Notes）
- [[04-神经网络损失函数与输出契约（Neural Network Loss Functions and Output Contracts）]]
- [[05-反向传播与链式法则（Backpropagation and the Chain Rule）]]
- [[06-梯度下降、优化器与学习率调度（Gradient Descent, Optimizers, and Learning-rate Scheduling）]]
