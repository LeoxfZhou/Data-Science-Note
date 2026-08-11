---
title: 神经网络参数初始化与梯度流（Neural Network Initialization and Gradient Flow）
aliases:
  - Weight Initialization and Gradient Flow
tags:
  - data-science/deep-learning/initialization
  - data-science/deep-learning/optimization
status: published
created: 2026-08-11
published_at: 2026-08-11
---
# 神经网络参数初始化与梯度流（Neural Network Initialization and Gradient Flow）
## 1. 初始化目标（Initialization Objectives）
- 前向传播（Forward Propagation）中，各层激活方差不要随深度指数衰减或膨胀。
- 反向传播（Backward Propagation）中，各层梯度方差保持可训练尺度。
- 打破同层神经元对称性（Symmetry），使不同神经元学习不同特征。
- 与激活函数、fan-in/fan-out、残差结构和归一化层匹配。
- 初始化不能替代学习率、数据尺度、归一化、残差连接和梯度裁剪等训练设计。
## 2. 失败模式（Failure Modes）
### 2.1 梯度消失（Vanishing Gradient）
- 多层链式法则持续乘以绝对值小于 1 的导数或权重尺度，靠近输入端的梯度可能指数衰减。
- 结果包括底层参数几乎不更新、损失下降慢和长期停滞。
### 2.2 梯度爆炸（Exploding Gradient）
- 多层乘积持续放大梯度，可能产生巨大更新、损失震荡、无穷值（Infinity）或非数（Not a Number, NaN）。
- 靠近输入的层经历更长链路，但实际受影响程度还取决于结构、残差和归一化，不能仅凭层位置判断。
### 2.3 收敛缓慢（Slow Convergence）
- 激活尺度过小、过大或高度不平衡会让优化器在不良曲率区域缓慢移动。
## 3. 朴素初始化的问题（Problems with Naive Initialization）
### 3.1 全零或同一常数权重（Zero or Identical Constant Weights）
- 同层神经元权重完全相同，会得到相同输出与梯度，训练后仍保持对称，无法学习多样特征。
- “权重不能全零”不等于“偏置不能初始化为零”；卷积层和线性层偏置设为 0 通常是合理做法。
### 3.2 过小高斯权重（Tiny Gaussian Weights）
- 例如深层网络所有权重都取 $\mathcal{N}(0,0.01^2)$，信号方差可能逐层收缩。
- 深度、fan-in 与激活共同决定结果，不能把 0.01 视为所有结构都失败的固定阈值。
### 3.3 过大高斯权重（Large Gaussian Weights）
- Sigmoid/Tanh 输入可能进入饱和区，导数接近 0。
- ReLU 网络中激活和梯度可能放大，造成数值不稳定。
## 4. fan-in 与 fan-out
- **fan-in**：每个输出单元接收的输入连接数，影响前向激活方差。
- **fan-out**：每个输入单元连接到的输出数，影响反向梯度方差。
- 对线性层权重形状 `[fan_out, fan_in]`，两个值直观可见；卷积权重还要乘卷积核空间面积。
- PyTorch 初始化 API 按其假定权重布局计算 fan；若手工以转置方式使用权重，需要核对官方说明。
## 5. Xavier（Glorot）初始化
### 5.1 方差目标（Variance Objective）
理想化独立同分布假设下，为兼顾前向与反向尺度：
$$
\operatorname{Var}(W)=\frac{2}{fan_{in}+fan_{out}}
$$
Xavier 正态分布的标准差为：
$$
\operatorname{std}=gain\sqrt{\frac{2}{fan_{in}+fan_{out}}}
$$
Xavier 均匀分布边界为：
$$
W\sim U\left(-gain\sqrt{\frac{6}{fan_{in}+fan_{out}}},\ gain\sqrt{\frac{6}{fan_{in}+fan_{out}}}\right)
$$
### 5.2 适用激活（Applicable Activations）
- 适合线性、Tanh 和一些近似对称激活；应通过 `nn.init.calculate_gain()` 选择增益。
- 深层 ReLU 会把负半轴置零，Xavier 的理想方差假设不再匹配，常改用 Kaiming。
- 来源用 $\operatorname{Var}(\operatorname{ReLU}(x))\approx\frac12\operatorname{Var}(x)$ 推导 $0.5^L$ 衰减。这是对零均值对称输入的简化直觉，真实网络受均值偏移、权重、归一化和残差影响。
## 6. Kaiming（He）初始化
### 6.1 ReLU 正态形式（Normal Form for ReLU）
$$
\operatorname{Var}(W)=\frac{2}{fan_{in}},\qquad
W\sim\mathcal{N}\left(0,\sqrt{\frac{2}{fan_{in}}}\right)
$$
### 6.2 ReLU 均匀形式（Uniform Form for ReLU）
在简化增益下：
$$
W\sim U\left(-\sqrt{\frac{6}{fan_{in}}},\sqrt{\frac{6}{fan_{in}}}\right)
$$
### 6.3 LeakyReLU 修正（LeakyReLU Adjustment）
负斜率为 $\alpha$ 时：
$$
\operatorname{Var}(W)=\frac{2}{(1+\alpha^2)fan_{in}}
$$
- PyTorch `kaiming_*` 的 **a** 参数应传 LeakyReLU 负斜率，**nonlinearity** 应与实际激活一致。
- `mode='fan_in'` 优先保持前向方差，`mode='fan_out'` 优先保持反向梯度方差。
- Kaiming 改善 ReLU 族的初始信号传播，但不保证任意深度、数据和优化配置都稳定。
## 7. LeCun 初始化（LeCun Initialization）
$$
\operatorname{Var}(W)=\frac{1}{fan_{in}}
$$
- 常与线性或自归一化网络（Self-normalizing Neural Network）的 SELU 设计联系。
- PyTorch 没有统一命名的 `lecun_normal_` 公共函数时，可基于 fan-in 明确实现；SELU 网络还要求激活、AlphaDropout 和结构假设配套。
## 8. 方法对比（Method Comparison）

|方法（Method）|典型方差（Typical Variance）|常见激活（Common Activation）|主要目的（Primary Goal）|
|---|---|---|---|
|LeCun|$1/fan_{in}$|Linear、SELU 配套结构|保持前向尺度|
|Xavier/Glorot|$2/(fan_{in}+fan_{out})$|Tanh、Linear、Sigmoid 邻近线性区|折中前向与反向方差|
|Kaiming/He|$2/fan_{in}$（ReLU）|ReLU、LeakyReLU|补偿负半轴截断造成的方差变化|

## 9. PyTorch API（PyTorch Initialization APIs）
### 9.1 常用函数（Common Functions）
- `nn.init.xavier_uniform_()`、`xavier_normal_()`。
- `nn.init.kaiming_uniform_()`、`kaiming_normal_()`。
- `nn.init.constant_()`、`zeros_()`、`ones_()`。
- `nn.init.calculate_gain(nonlinearity, param=None)`。
- 这些函数原地修改参数，并在 `torch.no_grad()` 语义下运行。
### 9.2 模块遍历初始化（Module-wise Initialization）
```python
import torch
from torch import nn


class InitializedNetwork(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv = nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.hidden = nn.Linear(64, 32)
        self.output = nn.Linear(32, 10)
        self.apply(self._initialize_module)

    @staticmethod
    def _initialize_module(module: nn.Module) -> None:
        if isinstance(module, nn.Conv2d):
            nn.init.kaiming_normal_(
                module.weight,
                mode="fan_in",
                nonlinearity="relu",
            )
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Linear):
            nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                nn.init.zeros_(module.bias)


network = InitializedNetwork()
print(network.conv.weight.shape)    # 输出: torch.Size([64, 3, 3, 3])
print(network.hidden.weight.shape)  # 输出: torch.Size([32, 64])
print(network.output.bias.sum().item())  # 输出: 0.0
```
> [!warning] 激活匹配（Activation Matching）
> 示例把卷积视为 ReLU 前层，因此使用 Kaiming；隐藏线性层示意使用 Xavier。真实模型应根据每一层之后的实际激活选择，而不是仅按“卷积/全连接”类型机械初始化。
## 10. 初始化诊断（Initialization Diagnostics）
- 前向 hook 记录每层激活均值、标准差、零比例和非有限值。
- 反向 hook 或训练日志记录梯度范数、最大值和非有限值。
- 检查不同深度层的尺度是否系统性衰减或膨胀。
- 先在一个 batch 上验证损失和梯度，再开始长训练。
- 参数初始化后不要意外再次调用框架默认 `reset_parameters()` 覆盖。
## 11. 常见错误（Common Errors）
- 所有权重初始化为同一常数，破坏对称性。
- Kaiming 的 `nonlinearity` 与实际激活不一致。
- LeakyReLU 使用非默认斜率，却忘记传给初始化 API。
- 把零偏置与零权重混为一谈。
- 认为初始化能单独消除所有梯度问题，忽略学习率、归一化、残差和数据尺度。
- 把公式中的方差误写为标准差；API 参数通常基于推导后的 bound/std。
## 参考资料（References）
- [`torch.nn.init` 官方文档](https://docs.pytorch.org/docs/stable/nn.init.html)
- [Understanding the Difficulty of Training Deep Feedforward Neural Networks](https://proceedings.mlr.press/v9/glorot10a.html)
- [Delving Deep into Rectifiers](https://arxiv.org/abs/1502.01852)
- [来源补充视频：Kaiming vs. Xavier](https://www.youtube.com/watch?v=r_GYQvnfP3M)
