---
title: 反向传播与链式法则（Backpropagation and the Chain Rule）
tags:
  - data-science/deep-learning/backpropagation
  - data-science/deep-learning/calculus
status: published
created: 2026-08-11
published_at: 2026-08-12
---
# 反向传播与链式法则（Backpropagation and the Chain Rule）
## 1. 两个阶段（Two Phases）
1. 正向传播（Forward Propagation）：逐层计算净输入、激活与最终损失。
2. 反向传播（Backpropagation）：从损失出发，按计算图逆序应用链式法则，得到所有参数梯度。
- BP 本身负责高效求梯度；梯度下降或 Adam 等优化器负责使用梯度更新参数。
## 2. 三层全连接网络（Three-layer Fully Connected Network）
对输入 $x_i$、隐层权重 $v_{ij}$、输出层权重 $w_{jk}$：
$$
net_j=\sum_i v_{ij}x_i+b_j,\quad h_j=f(net_j)
$$
$$
net_k=\sum_j w_{jk}h_j+b_k,\quad y_k=g(net_k)
$$
使用均方误差：
$$
E=\frac12\sum_k(t_k-y_k)^2
$$
## 3. 输出层梯度（Output-layer Gradient）
$$
\frac{\partial E}{\partial w_{jk}}=
\frac{\partial E}{\partial y_k}
\frac{\partial y_k}{\partial net_k}
\frac{\partial net_k}{\partial w_{jk}}
$$
定义输出误差信号（Output Delta）：
$$
\delta_k^o=\frac{\partial E}{\partial net_k}
=(y_k-t_k)g'(net_k)
$$
因为 $\partial net_k/\partial w_{jk}=h_j$：
$$
\frac{\partial E}{\partial w_{jk}}=\delta_k^o h_j,qquad
\frac{\partial E}{\partial b_k}=\delta_k^o
$$
## 4. 隐层梯度（Hidden-layer Gradient）
隐层单元 $h_j$ 影响所有相连输出，因此分支梯度必须求和：
$$
\frac{\partial E}{\partial h_j}=\sum_k\delta_k^o w_{jk}
$$
定义隐层误差信号（Hidden Delta）：
$$
\delta_j^h=\left(\sum_k\delta_k^o w_{jk}\right)f'(net_j)
$$
因而：
$$
\frac{\partial E}{\partial v_{ij}}=\delta_j^h x_i,qquad
\frac{\partial E}{\partial b_j}=\delta_j^h
$$
- 直观上，前层接收后层 Delta 经连接权重加权后的总“责任”，再乘本层局部导数。
## 5. 数字演算设定（Numerical Example Setup）
- 输入：$i_1=5,i_2=10$。
- 隐层偏置：$b_1=0.35$；输出层偏置：$b_2=0.65$。
- 目标：$t=(0.01,0.99)$；学习率：$\eta=0.5$；全网络使用 Sigmoid。
- 输入到 3 个隐层单元的权重：$(w_1,w_2)=(0.1,0.15)$、$(w_3,w_4)=(0.2,0.25)$、$(w_5,w_6)=(0.3,0.35)$。
- 隐层到 2 个输出单元的权重：$(w_7,w_8)=(0.4,0.45)$、$(w_9,w_{10})=(0.5,0.55)$、$(w_{11},w_{12})=(0.6,0.65)$。
## 6. 正向传播数字（Forward-pass Numbers）
对第一个隐层单元：
$$
net_{h1}=0.1×5+0.15×10+0.35=2.35,qquad out_{h1}\approx0.912934
$$
其余隐层输出：$out_{h2}\approx0.979164$，$out_{h3}\approx0.995275$。
对第一个输出：
$$
net_{o1}=0.4out_{h1}+0.5out_{h2}+0.6out_{h3}+0.65\approx2.101921
$$
得 $out_{o1}\approx0.891090$，$out_{o2}\approx0.904330$，总误差约 $E\approx0.391829$。
## 7. 输出权重 $w_7$（Output Weight $w_7$）
$$
\frac{\partial E}{\partial out_{o1}}=0.891090-0.01=0.881090
$$
$$
\sigma'(net_{o1})=0.891090(1-0.891090)\approx0.097049
$$
$$
\frac{\partial E}{\partial w_7}\approx0.881090×0.097049×0.912934\approx0.078064
$$
$$
w_7^+=0.4-0.5×0.078064\approx0.360968
$$
## 8. 输入权重 $w_1$ 与更新顺序（Input Weight $w_1$ and Update Ordering）
- 标准 BP 在一次前向/反向中先计算所有梯度，再由优化器统一更新；计算 $w_1$ 梯度时必须使用前向时的旧后层权重。
- 原幻灯片按串行手算路径先更新 $w_7$，再用新值计算 $w_1$，得到汇总梯度约 $0.011204$ 和 $w_1^+\approx0.094534$。该数字属于串行变体，不能与标准并行梯度混称。
- 若实现中边算边改参数，后续梯度对应的已不是同一个参数状态，可能导致结果偏差或不收敛。
## 9. 教学串行更新结果（Teaching Sequential-update Results）

|参数（Parameter）|初始值|串行更新值|参数（Parameter）|初始值|串行更新值|
|---|---:|---:|---|---:|---:|
|$w_1$|0.10|0.094534|$w_7$|0.40|0.360968|
|$w_2$|0.15|0.139069|$w_8$|0.45|0.453383|
|$w_3$|0.20|0.198211|$w_9$|0.50|0.458137|
|$w_4$|0.25|0.246422|$w_{10}$|0.55|0.553629|
|$w_5$|0.30|0.299497|$w_{11}$|0.60|0.557448|
|$w_6$|0.35|0.348993|$w_{12}$|0.65|0.653688|
> [!warning] 数字边界（Numerical Boundary）
> 该表采用“计算一个参数的梯度后立即写回”的教学串行路径，因此后续梯度可能读取已更新参数。标准框架的一次 `backward()` 会基于同一份前向状态计算全部梯度，再统一更新参数；两种顺序的数值可能不同。
## 10. 多轮迭代示意（Multi-step Illustration）
- 第 10 次串行迭代输出：$(0.662866,0.908195)$。
- 第 100 次输出：$(0.073889,0.945864)$。
- 第 1000 次输出：$(0.022971,0.977675)$，逐渐接近目标 $(0.01,0.99)$。
- 这些值依赖固定样本、初始化、学习率、损失和串行/并行更新定义，不能推广为一般收敛保证。
## 11. 输出层与工程边界（Output-layer and Engineering Boundaries）
- 输出层是否带激活取决于损失接口：回归常直接输出连续值；交叉熵训练接 Logits；概率仅在推理或需要概率的接口处转换。
- 教学题可能给输出层指定 Sigmoid 与 MSE，用于完整链式求导；这不是现代多分类训练的默认最佳组合。
- 自动微分（Automatic Differentiation）按计算图求同一目标的精确机器梯度，但仍应理解形状、归约和梯度累积语义。
## 12. 反向传播图示（Backpropagation Diagrams）

> [!tip] 大白话理解（Plain-language Intuition）
> 前向传播是在问“按当前参数，答案是多少”；反向传播是在追责：“最终误差里，每个中间量和参数分别贡献了多少”。链式法则像沿着计算图从结果往回逐段乘影响系数，最后得到每个参数应该往哪个方向改、改多少。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/01-基础理论（Fundamentals）/03-反向传播与链式法则（Backpropagation and the Chain Rule）/05-反向传播与链式法则（Backpropagation and the Chain Rule）-20260716111721850.png]]
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/01-基础理论（Fundamentals）/03-反向传播与链式法则（Backpropagation and the Chain Rule）/05-反向传播与链式法则（Backpropagation and the Chain Rule）-20260716112216250.png]]
## 参考资料（References）
- [Rumelhart、Hinton 与 Williams：Learning representations by back-propagating errors](https://www.nature.com/articles/323533a0)
- [PyTorch 自动微分官方教程](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)
