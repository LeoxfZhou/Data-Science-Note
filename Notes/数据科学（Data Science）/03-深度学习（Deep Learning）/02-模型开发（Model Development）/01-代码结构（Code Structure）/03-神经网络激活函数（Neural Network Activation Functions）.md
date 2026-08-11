---
title: 神经网络激活函数（Neural Network Activation Functions）
aliases:
  - Neural Network Activation Functions
tags:
  - data-science/deep-learning/activation
  - data-science/deep-learning/pytorch
status: published
created: 2026-08-11
published_at: 2026-08-11
---
# 神经网络激活函数（Neural Network Activation Functions）
## 1. 为什么需要激活函数（Why Activation Functions Are Needed）
- 卷积层和全连接层核心都是仿射变换（Affine Transformation）$Wx+b$。
- 多个没有非线性激活的仿射层复合后仍是一个仿射变换，深度无法增加函数类别的表达能力。
- 激活函数（Activation Function）逐元素引入非线性，使网络能够逼近复杂决策边界。
- 标准逐元素激活通常保持张量形状不变，并对每个位置独立计算；这条性质不自动适用于 GLU、Maxout 等会切分或聚合通道的特殊激活结构。
## 2. 选择维度（Selection Criteria）

|维度（Criterion）|需要关注的问题|
|---|---|
|输出范围（Output Range）|是否有界、是否以 0 为中心、是否符合输出层语义|
|导数（Derivative）|是否在常用区间饱和、负半轴是否保留梯度|
|计算成本（Computational Cost）|是否需要指数运算，是否影响大规模推理|
|平滑性（Smoothness）|拐点或导数不连续是否影响特定优化任务|
|稀疏性（Sparsity）|是否产生大量 0 激活|
|数值稳定性（Numerical Stability）|极大或极小输入是否溢出、下溢或饱和|
|部署约束（Deployment Constraint）|量化、移动端和算子后端是否高效支持|

## 3. Sigmoid
### 3.1 公式与导数（Formula and Derivative）
$$
\sigma(x)=\frac{1}{1+e^{-x}},\qquad \sigma'(x)=\sigma(x)(1-\sigma(x))
$$
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/01-代码结构（Code Structure）/03-神经网络激活函数（Neural Network Activation Functions）/03-神经网络激活函数（Neural Network Activation Functions）-20260508094950166.png|Sigmoid 函数图]]
### 3.2 特性与用途（Properties and Uses）
- 输出范围为 $(0,1)$，适合二分类或多标签任务中把 logits 转成概率。
- 输出不以 0 为中心，可能让相邻层梯度方向产生偏置式耦合。
- 当 $|x|$ 很大时导数趋近 0，称为梯度饱和（Gradient Saturation）；深层反向传播会因此出现梯度消失。
- 损失计算时优先使用 `BCEWithLogitsLoss` 直接接收 logits，而不是手工 Sigmoid 后再接 `BCELoss`。
## 4. Tanh
### 4.1 公式与导数（Formula and Derivative）
$$
\tanh(x)=\frac{e^x-e^{-x}}{e^x+e^{-x}},\qquad \frac{d}{dx}\tanh(x)=1-\tanh^2(x)
$$
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/01-代码结构（Code Structure）/03-神经网络激活函数（Neural Network Activation Functions）/03-神经网络激活函数（Neural Network Activation Functions）-20260508095016369.png|Tanh 函数图]]
### 4.2 特性与用途（Properties and Uses）
- 输出范围为 $(-1,1)$ 且以 0 为中心，常比 Sigmoid 更适合作为隐藏状态候选值。
- 大绝对值区域仍会饱和并导致梯度消失。
- 传统循环神经网络（Recurrent Neural Network, RNN）和门控结构中仍常见 Tanh，但深层前馈 CNN 通常使用 ReLU 族。
## 5. ReLU 与 ReLU6
### 5.1 ReLU 公式（ReLU Formula）
$$
\operatorname{ReLU}(x)=\max(0,x),\qquad
\operatorname{ReLU}'(x)=
\begin{cases}
1,&x>0\\
0,&x<0
\end{cases}
$$
- 在 $x=0$ 处数学导数不唯一，PyTorch 采用特定次梯度约定，通常为 0。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/01-代码结构（Code Structure）/03-神经网络激活函数（Neural Network Activation Functions）/03-神经网络激活函数（Neural Network Activation Functions）-20260508095047927.png|ReLU 函数图]]
### 5.2 优点（Advantages）
- 正半轴导数为 1，缓解 Sigmoid/Tanh 饱和造成的梯度消失。
- 只需比较与取值，计算成本低。
- 负输入输出 0，产生稀疏激活（Sparse Activation）。
### 5.3 死 ReLU（Dying ReLU）
- 如果某个神经元在训练样本上持续落入负区间，其梯度为 0，参数可能无法恢复，这才是常说的“死 ReLU”。
- 大学习率、偏置漂移、数据尺度和不合适初始化都可能增加风险；仅降低学习率不是唯一解。
- 可考虑 LeakyReLU、ELU、归一化、合适初始化和训练诊断。
### 5.4 ReLU6
$$
\operatorname{ReLU6}(x)=\min(\max(0,x),6)
$$
- ReLU6 把正输出限制在 6，历史上常见于移动端与量化友好架构。
- 它不是解决所有激活爆炸问题的通用手段；上界也会产生饱和区域。
## 6. LeakyReLU
### 6.1 公式与导数（Formula and Derivative）
$$
f(x)=
\begin{cases}
x,&x>0\\
\alpha x,&x\le 0
\end{cases},\qquad
f'(x)=
\begin{cases}
1,&x>0\\
\alpha,&x<0
\end{cases}
$$
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/01-代码结构（Code Structure）/03-神经网络激活函数（Neural Network Activation Functions）/03-神经网络激活函数（Neural Network Activation Functions）-20260508095142098.png|LeakyReLU 函数图]]
- 常见负斜率示例为 $\alpha=0.01$，但 PyTorch `nn.LeakyReLU` 的默认值和模型论文配置应以实际版本与架构为准。
- 负半轴保留非零梯度，可降低永久死亡风险。
- 是否优于 ReLU 依赖任务、初始化和网络设计，不能保证普遍提升。
## 7. ELU
### 7.1 公式（Formula）
$$
f(x)=
\begin{cases}
x,&x>0\\
\alpha(e^x-1),&x\le 0
\end{cases}
$$
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/02-模型开发（Model Development）/01-代码结构（Code Structure）/03-神经网络激活函数（Neural Network Activation Functions）/03-神经网络激活函数（Neural Network Activation Functions）-20260508095204948.png|ELU 函数图]]
- 负半轴平滑趋近 $-\alpha$，输出均值可能比 ReLU 更接近 0。
- 指数计算成本高于 ReLU/LeakyReLU；实际鲁棒性和速度需基准测试。
## 8. PyTorch 调用方式（PyTorch Invocation Styles）
### 8.1 模块式与函数式（Module and Functional Styles）
- `nn.ReLU()` 是 `nn.Module`，适合 `nn.Sequential`、模块树检查和配置驱动构建。
- `torch.nn.functional.relu()` 是函数式 API，适合在 `forward()` 中直接调用无状态运算。
- 二者对相同输入具有相同核心数学行为；模块实例更容易携带构造配置。
```python
import torch
from torch import nn
import torch.nn.functional as F

x = torch.tensor([[-1.0, 0.0, 2.0]])
module_result = nn.ReLU()(x)
functional_result = F.relu(x)
print(module_result.tolist())      # 输出: [[0.0, 0.0, 2.0]]
print(torch.equal(module_result, functional_result))  # 输出: True
```
### 8.2 `inplace=True` 风险
- `nn.ReLU(inplace=True)` 直接复用输入存储，可能减少部分内存分配。
- 原地修改会影响共享视图、残差分支或 autograd 保存的中间值，可能触发版本计数错误或改变后续分支输入。
- 只有经过显存分析且计算图确认安全时才启用；默认非原地写法更易维护。
## 9. MobileNet 中的激活设计（Activation Design in MobileNet）
### 9.1 MobileNet V1
- 深度可分离卷积（Depthwise Separable Convolution）通常由深度卷积（Depthwise Convolution）和逐点卷积（Pointwise Convolution）组成。
- 来源结构为 `Depthwise Conv → BatchNorm → ReLU → Pointwise Conv → BatchNorm → ReLU`。
### 9.2 MobileNet V2 线性瓶颈（Linear Bottleneck）
- MobileNet V2 的倒残差（Inverted Residual）在低维瓶颈输出处采用线性映射，而不是再用 ReLU 截断。
- 低维特征空间容量有限，ReLU 把负值置零可能不可逆地破坏信息；线性瓶颈用于尽量保存投影后的特征。
- 更准确的说法是“瓶颈投影层使用线性激活”，不是所有降维逐点卷积后都必须取消非线性。
## 10. 选择速查（Selection Guide）

|场景（Scenario）|常见选择（Typical Choice）|主要风险（Main Risk）|
|---|---|---|
|一般 CNN 隐藏层|ReLU|死 ReLU、非零中心|
|希望负半轴保留梯度|LeakyReLU、ELU|额外超参数或计算成本|
|二分类/多标签概率输出|Sigmoid|损失阶段应优先 logits 版本|
|有界、零中心状态|Tanh|大输入饱和|
|移动端有界激活|ReLU6|正半轴上界饱和|
|MobileNet V2 瓶颈投影|Linear|不能把线性误用为整个深层网络唯一激活|

## 11. 关联初始化（Initialization Pairing）
- Tanh/Sigmoid 常与 Xavier 初始化搭配，并根据激活选择增益（Gain）。
- ReLU/LeakyReLU 常与 Kaiming 初始化搭配，`nonlinearity` 与负斜率配置必须一致。
- 详见 [[01-神经网络参数初始化与梯度流（Neural Network Initialization and Gradient Flow）]]。
## 参考资料（References）
- [`torch.nn` 激活模块官方文档](https://docs.pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity)
- [MobileNetV2 原论文](https://arxiv.org/abs/1801.04381)
