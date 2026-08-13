---
title: "Transformer 架构、子模块与并行性（Transformer Architecture, Components, and Parallelism）"
tags:
  - data-science/nlp
status: published
created: 2026-08-13
published_at: 2026-08-13
---
# Transformer 架构、子模块与并行性（Transformer Architecture, Components, and Parallelism）

## Transformer背景介绍
> [!tip] 大白话理解（Plain-language Intuition）
> Transformer 把序列建模的主要工作交给注意力和逐位置前馈网络。训练时整段序列可用矩阵并行计算；自回归生成时仍必须逐 token 产生，因此训练并行不等于推理也完全并行。
### 1 Transformer的诞生

Transformer 由 Vaswani 等人在 2017 年论文《Attention Is All You Need》中提出，最初面向神经机器翻译（Neural Machine Translation, NMT）。2018 年的 BERT 随后采用双向 Transformer 编码器（Encoder）进行预训练，并推动该架构广泛迁移到自然语言理解任务。

- Transformer 论文：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- BERT 论文：[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)

### 2 Transformer的优势

相比之前占领市场的LSTM和GRU模型，Transformer有两个显著的优势:

```text
1、Transformer能够利用分布式GPU进行并行训练，提升模型训练效率.
2、在分析预测更长的文本时, 捕捉间隔较长的语义关联效果更好.
```

下面是一张在测评比较图:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000096.png]]

### 3 Transformer的市场

在著名的SOTA机器翻译榜单上, 几乎所有排名靠前的模型都使用Transformer,

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000097.png]]

其基本上可以看作是工业界的风向标, 市场空间自然不必多说！

## 认识Transformer架构
### 1 Transformer模型的作用

- 基于seq2seq架构的transformer模型可以完成NLP领域研究的典型任务, 如机器翻译, 文本生成等. 同时又可以构建预训练语言模型，用于不同任务的迁移学习.
- 在接下来的架构分析中, 我们将假设使用Transformer模型架构处理从一种语言文本到另一种语言文本的翻译工作, 因此很多命名方式遵循NLP中的规则. 比如: Embeddding层将称作文本嵌入层, Embedding层产生的张量称为词嵌入张量, 它的最后一维将称作词向量等.

### 2 Transformer总体架构图

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000098.png]]

#### 2.1 Transformer总体架构

- 输入部分
- 输出部分
- 编码器部分
- 解码器部分

#### 2.2 输入部分包含

- 源文本嵌入层及其位置编码器
- 目标文本嵌入层及其位置编码器

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000099.png]]

#### 2.3 输出部分包含

- 线性层
- softmax层

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000100.png]]

#### 2.4 编码器（Encoder）部分

- 由N个编码器层堆叠而成
- 每个编码器层由两个子层连接结构组成
- 第一个子层连接结构包括一个多头自注意力子层和规范化层以及一个残差连接
- 第二个子层连接结构包括一个前馈全连接子层和规范化层以及一个残差连接

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000101.png]]

#### 2.5 解码器（Decoder）部分

- 由N个解码器层堆叠而成
- 每个解码器层由三个子层连接结构组成
- 第一个子层连接结构包括一个多头自注意力子层和规范化层以及一个残差连接
- 第二个子层连接结构包括一个多头注意力子层和规范化层以及一个残差连接
- 第三个子层连接结构包括一个前馈全连接子层和规范化层以及一个残差连接

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000102.png]]

## Transformer 各子模块作用
### 1 Encoder模块
#### 1.1 Encoder模块的结构和作用:

- 经典的Transformer结构中的Encoder模块包含6个Encoder Block.
- 每个Encoder Block包含一个多头自注意力层, 和一个前馈全连接层.

#### 1.2 关于Encoder Block

- 在Transformer架构中, 6个一模一样的Encoder Block层层堆叠在一起, 共同组成完整的Encoder, 因此剖析一个Block就可以对整个Encoder的内部结构有清晰的认识.

#### 1.3 多头自注意力层(self-attention)
> [!tip] 大白话理解（Plain-language Intuition）
> 自注意力像让句子中的每个词都向其他词提问：谁与我最相关？相关性变成权重，再用这些权重汇总信息。它能一步连接远距离词，但代价是标准实现对序列长度通常需要平方级注意力矩阵。
> [!tip] 大白话理解（Plain-language Intuition）
> 注意力机制像读长文时移动聚光灯：生成当前结果时，不平均依赖所有输入，而是根据当前查询把更高权重放到更相关的位置。权重表示当前计算中的相关程度，不等同于严格因果解释。

首先来看self-attention的计算规则图:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000107.png]]

> - 上述attention可以被描述为将query和key-value键值对的一组集合映射到输出, 输出被计算为values的加权和, 其中分配给每个value的权重由query与对应key的相似性函数计算得来. 这种attention的形式被称为Scaled Dot-Product Attention, 对应的数学公式形式如下:

$$Attention(Q,K,V)=Softmax(\frac{Q\cdot K^T}{\sqrt{d_{k}}})\cdot V$$

> - 所谓的多头self-attention层, 则是先将Q, K, V经过参数矩阵进行映射, 再做self-attention, 最后将结果拼接起来送入一个全连接层即可.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000104.png]]

上述的多头self-attention, 对应的数学公式形式如下:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000103.png]]

多头self-attention层的作用: 实验结果表明, Multi-head可以在更细致的层面上提取不同head的特征, 总体计算量和单一head相同的情况下, 提取特征的效果更佳.

- 前馈全连接层模块
  - 前馈全连接层模块, 由两个线性变换组成, 中间有一个Relu激活函数, 对应的数学公式形式如下: $$ FFN(x)=\max(0,xW_1+b_1)W_2+b_2 $$

> - 注意: 原版论文中的前馈全连接层, 输入和输出的维度均为d_model = 512, 层内的连接维度d_ff = 2048, 均采用4倍的大小关系.
> - 前馈全连接层的作用: 单纯的多头注意力机制并不足以提取到理想的特征, 因此增加全连接层来提升网络的能力.

#### 1.4 Decoder模块

- Decoder模块的结构和作用:
  - 经典的Transformer结构中的Decoder模块包含6个Decoder Block.
  - 每个Decoder Block包含三个子层.
    - 一个多头self-attention层
    - 一个Encoder-Decoder attention层
    - 一个前馈全连接层
- Decoder Block中的多头self-attention层
  - Decoder中的多头self-attention层与Encoder模块一致, 但需要注意的是Decoder模块的多头self-attention需要做look-ahead-mask, 因为在预测的时候"不能看见未来的信息", 所以要将当前的token和之后的token全部mask.
- Decoder Block中的Encoder-Decoder attention层
  - 这一层区别于自注意力机制的Q = K = V, 此处矩阵Q来源于Decoder端经过上一个Decoder Block的输出, 而矩阵K, V则来源于Encoder端的输出, 造成了Q != K = V的情况.
  - 这样设计是为了让Decoder端的token能够给予Encoder端对应的token更多的关注.
- Decoder Block中的前馈全连接层
  - 此处的前馈全连接层和Encoder模块中的完全一样.
- Decoder Block中有2个注意力层的作用: 多头self-attention层是为了拟合Decoder端自身的信息, 而Encoder-Decoder attention层是为了整合Encoder和Decoder的信息.

#### 1.5 Add & Norm模块

- Add & Norm模块接在每一个Encoder Block和Decoder Block中的每一个子层的后面. 具体来说Add表示残差连接, Norm表示LayerNorm.
  - 对于每一个Encoder Block, 里面的两个子层后面都有Add & Norm.
  - 对于每一个Decoder Block, 里面的三个子层后面都有Add & Norm.
  - 具体的数学表达形式为: LayerNorm(x + Sublayer(x)), 其中Sublayer(x)为子层的输出.
- Add残差连接的作用: 和其他神经网络模型中的残差连接作用一致, 都是为了将信息传递的更深, 增强模型的拟合能力. 试验表明残差连接的确增强了模型的表现.
- Norm的作用: 随着网络层数的额增加, 通过多层的计算后参数可能会出现过大, 过小, 方差变大等现象, 这会导致学习过程出现异常, 模型的收敛非常慢. 因此对每一层计算后的数值进行规范化可以提升模型的表现.

#### 1.6 位置编码（Positional Encoding）器Positional Encoding

- Transformer中直接采用正弦函数和余弦函数来编码位置信息, 如下图所示: $$ PE_{(pos, 2i)}=\sin(\frac{pos} {10000^{\frac{2i}{d_{model}}}})\\ PE_{(pos, 2i+1)}=\cos(\frac{pos} {10000^{\frac{2i}{d_{model}}}})\\ $$
- 需要注意: 三角函数应用在此处的一个重要的优点, 因为对于任意的PE(pos+k), 都可以表示为PE(pos)的线性函数, 大大方便计算. 而且周期性函数不受序列长度的限制, 也可以增强模型的泛化能力. $$ \sin(\alpha+\beta)=\sin(\alpha)\cos(\beta)+\cos(\alpha)\sin(\beta)\\ \cos(\alpha+\beta)=\cos(\alpha)\cos(\beta)-\sin(\alpha)\sin(\beta) $$

## Transformer Decoder模块
### 1 Decoder端的输入解析
#### 1.1 Decoder端的架构

Transformer原始论文中的Decoder模块是由N=6个相同的Decoder Block堆叠而成, 其中每一个Block是由3个子模块构成, 分别是多头self-attention模块, Encoder-Decoder attention模块, 前馈全连接层模块.

- 6个Block的输入不完全相同:
  - 最下面的一层Block接收的输入是经历了MASK之后的Decoder端的输入 + Encoder端的输出.
  - 其他5层Block接收的输入模式一致, 都是前一层Block的输出 + Encoder端的输出.

#### 1.2 Decoder在训练阶段的输入解析

- 从第二层Block到第六层Block的输入模式一致, 无需特殊处理, 都是固定操作的循环处理.
- 聚焦在第一层的Block上: 训练阶段每一个time step的输入是上一个time step的输入加上真实标签序列向后移一位. 具体来说, 假设现在的真实标签序列等于"How are you?", 当time step=1时, 输入张量为一个特殊的token, 比如"SOS"; 当time step=2时, 输入张量为"SOS How"; 当time step=3时, 输入张量为"SOS How are", 以此类推...
- 注意: 在真实的代码实现中, 训练阶段不会这样动态输入, 而是一次性的把目标序列全部输入给第一层的Block, 然后通过多头self-attention中的MASK机制对序列进行同样的遮掩即可.

#### 1.3 Decoder在预测阶段的输入解析

- 同理于训练阶段, 预测时从第二层Block到第六层Block的输入模式一致, 无需特殊处理, 都是固定操作的循环处理.
- 聚焦在第一层的Block上: 因为每一步的输入都会有Encoder的输出张量, 因此这里不做特殊讨论, 只专注于纯粹从Decoder端接收的输入. 预测阶段每一个time step的输入是从time step=0, input_tensor="SOS"开始, 一直到上一个time step的预测输出的累计拼接张量. 具体来说:
  - 当time step=1时, 输入的input_tensor="SOS", 预测出来的输出值是output_tensor="What";
  - 当time step=2时, 输入的input_tensor="SOS What", 预测出来的输出值是output_tensor="is";
  - 当time step=3时, 输入的input_tensor="SOS What is", 预测出来的输出值是output_tensor="the";
  - 当time step=4时, 输入的input_tensor="SOS What is the", 预测出来的输出值是output_tensor="matter";
  - 当time step=5时, 输入的input_tensor="SOS What is the matter", 预测出来的输出值是output_tensor="?";
  - 当time step=6时, 输入的input_tensor="SOS What is the matter ?", 预测出来的输出值是output_tensor="EOS", 代表句子的结束符, 说明解码结束, 预测结束.

## Self attention机制详解
### 1 Self-attention的机制和原理

self-attention是一种通过自身和自身进行关联的attention机制, 从而得到更好的representation来表达自身.

self-attention是attention机制的一种特殊情况，在self-attention中, Q=K=V, 序列中的每个单词(token)都和该序列中的其他所有单词(token)进行attention规则的计算.

attention机制计算的特点在于, 可以直接跨越一句话中不同距离的token, 可以远距离的学习到序列的知识依赖和语序结构.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000109.png]]

> - 从上图中可以看到, self-attention可以远距离的捕捉到语义层面的特征(its的指代对象是Law).
> - 应用传统的RNN, LSTM, 在获取长距离语义特征和结构特征的时候, 需要按照序列顺序依次计算, 距离越远的联系信息的损耗越大, 有效提取和捕获的可能性越小.
> - 但是应用self-attention时, 计算过程中会直接将句子中任意两个token的联系通过一个计算步骤直接联系起来,

关于self-attention为什么要使用(Q, K, V)三元组而不是其他形式:

- 首先一条就是从分析的角度看, 查询Query是一条独立的序列信息, 通过关键词Key的提示作用, 得到最终语义的真实值Value表达, 数学意义更充分, 完备.
- 这里不使用(K, V)或者(V)没有什么必须的理由, 也没有相关的论文来严格阐述比较试验的结果差异, 所以可以作为开放性问题未来去探索, 只要明确在经典self-attention实现中用的是三元组就好.

self-attention公式中的归一化有什么作用? 为什么要添加scaled?

### 2 Self-attention中的归一化概述

- 训练上的意义: 随着词嵌入维度d_k的增大, q * k 点积后的结果也会增大, 在训练时会将带有饱和区间的激活函数（比如：sigmoid激活函数、tanh激活函数、逻辑回归softmax）推入梯度非常小的区域, 可能出现梯度消失的现象, 造成模型收敛困难.
- 数学上的意义: 假设q和k的统计变量是满足标准正态分布的独立随机变量, 意味着q和k满足均值为0, 方差为1. 那么q和k的点积结果就是均值为0, 方差为d_k, 为了抵消这种方差被放大d_k倍的影响, 在计算中主动将点积缩放1/sqrt(d_k), 这样点积后的结果依然满足均值为0, 方差为1.

### 3 softmax的梯度变化

这里我们分3个步骤来解释softmax的梯度问题:

- 第一步: softmax函数的输入分布是如何影响输出的.
- 第二步: softmax函数在反向传播的过程中是如何梯度求导的.
- 第三步: softmax函数出现梯度消失现象的原因.

#### 3.1 softmax函数的输入分布是如何影响输出的

- 对于一个输入向量x, softmax函数将其做了一个归一化的映射, 首先通过自然底数e将输入元素之间的差距先"拉大", 然后再归一化为一个新的分布. 在这个过程中假设某个输入x中最大的元素下标是k, 如果输入的数量级变大(就是x中的每个分量绝对值都很大), 那么在数学上会造成y_k的值非常接近1.
- 具体用一个例子来演示, 假设输入的向量x = [a, a, 2a], 那么随便给几个不同数量级的值来看看对y3产生的影响

```text
a = 1时,   y3 = 0.5761168847658291  # e^2 / (e^1 + e^1 + e^2))
a = 10时,  y3 = 0.9999092083843412  # e^20 / (e^10 + e^10 + e^20))
a = 100时, y3 = 1.0                 # e^200 / (e^100 + e^100 + e^200))
```

> - 采用一段实例代码将a在不同取值下, 对应的y3全部画出来, 以曲线的形式展示:

```python
from math import exp
from matplotlib import pyplot as plt
import numpy as np
f = lambda x: exp(x * 2) / (exp(x) + exp(x) + exp(x * 2))
x = np.linspace(0, 100, 100)
y_3 = [f(x_i) for x_i in x]
plt.plot(x, y_3)
plt.show()
```

> - 得到如下的曲线:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000105.png]]

> - 从上图可以很清楚的看到输入元素的数量级对softmax最终的分布影响非常之大
> - 结论： 在输入元素的数量级较大时，softmax函数几乎将全部的概率分布都分配给了最大值分量所对应的标签。通俗的讲：数据的方差变大（离散程度变大），最大值强占了所有概率。

#### 3.2 softmax函数在反向传播的过程中是如何梯度求导的

softmax函数在反向传播中容易梯度消失，所以要看一看softmax函数在反向传播中是如何求导的。

首先定义神经网络的输入和输出:

$$设X=[x_1,x_2,\cdots,x_n],Y=softmax(X)=[y_1,y_2,\cdots,y_n]\\\\
则y_i=\frac{e^{x_i}}{\sum_{j=1}^{n}e^{x_j}},显然\sum_{i=1}^{n}y_i=1$$

反向传播就是输出端的损失函数对输入端求偏导的过程, 这里要分两种情况, 第一种如下所示:

$$\begin{align*}
(1)当i=j时\\\\
\frac{\partial{y_i}}{\partial{x_j}} &= \frac{\partial{y_i}}{\partial{x_i}}\\\\
&= \frac{\partial}{\partial{x_i}}{(\frac{e^{x_i}}{\sum_k e^{x_k}})} \\\\
&= \frac{(e^{x_i})^{\prime} (\sum_k e^{x_k}) - e^{x_i}(\sum_ke^{x_k})^{\prime}}{(\sum_ke^{x_k})^2}\\\\
&=\frac{e^{x_i}\cdot(\sum_ke^{x_k})-e^{x_i}\cdot e^{x_i}}{(\sum_ke^{x_k})^2}\\\\
&=\frac{e^{x_i}\cdot(\sum_ke^{x_k})}{(\sum_ke^{x_k})^2}-\frac{e^{x_i}\cdot e^{x_i}}{(\sum_ke^{x_k})^2}\\\\
&=\frac{e^{x_i}}{\sum_ke^{x_k}}-\frac{e^{x_i}}{\sum_ke^{x_k}}\cdot \frac{ e^{x_i}}{\sum_ke^{x_k}}\\\\
&=y_i-y_i\cdot y_i \\\\
&=y_i(1-y_i)
\end{align*}$$

第二种如下所示:

$$\begin{align*}
(2)当i\neq j时\\\\
\frac{\partial{y_i}}{\partial{x_j}} &= \frac{\partial}{\partial{x_j}}{(\frac{e^{x_i}}{\sum_k e^{x_k}})} \\\\
&= \frac{(e^{x_i})^{\prime} (\sum_k e^{x_k}) - e^{x_i}(\sum_ke^{x_k})^{\prime}}{(\sum_ke^{x_k})^2}\\\\
&= \frac{0\cdot (\sum_k e^{x_k}) - e^{x_i}\cdot e^{x_j}}{(\sum_ke^{x_k})^2}\\\\
&= -\frac{e^{x_i}\cdot e^{x_j}}{(\sum_ke^{x_k})^2}\\\\
&= -\frac{e^{x_i}}{\sum_ke^{x_k}}\cdot \frac{ e^{x_j}}{\sum_ke^{x_k}}\\\\
&=-y_i\cdot y_j
\end{align*}$$

经过对两种情况分别的求导计算, 可以得出最终的结论如下:

$$\begin{align*}
综上所述：\frac{\partial y_i}{\partial x_j} &=  \begin{cases} y_i-y_i\cdot y_i, & \text {i=j} \\\\ 0-y_i\cdot y_j, & \text{i $\neq$ j} \end{cases} \\\\
所以：\frac{\partial Y}{\partial X} &= diag(Y)-Y^T\cdot Y \;\;\;(当Y的shape为(1,n)时)
\end{align*}$$

把抽象的数学公式，映射成矩阵表示，见3.3节表示（i=j时，两个矩阵对角线 - 对角线 ；i!=j时，对应位置相减）。

#### 3.3 softmax函数出现梯度消失现象的原因

> - 根据第二步中softmax函数的求导结果, 可以将最终的结果以矩阵形式展开如下:

$$\frac{\partial g(X)}{\partial X}\approx \begin{bmatrix} \hat y_1 & 0 & \cdots & 0 \\ 0 & \hat y_2 & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & \hat y_d  \end{bmatrix} - \begin{bmatrix} \hat y_1^2 & \hat y_1 \hat y_2 & \cdots & \hat y_1 \hat y_d \\ \hat y_2 \hat y_1  & \hat y_2^2 & \cdots & \hat y_2 \hat y_d \\ \vdots & \vdots & \ddots & \vdots \\ \hat y_d \hat y_1 & \hat y_d \hat y_2 & \cdots & \hat y_d^2  \end{bmatrix}$$

> - 根据第一步中的讨论结果, 当输入x的分量值较大时, softmax函数会将大部分概率分配给最大的元素, 假设最大元素是x1, 那么softmax的输出分布将产生一个接近one-hot的结果张量y_ = [1, 0, 0,..., 0], 此时结果矩阵变为:

$$\frac{\partial g(X)}{\partial X}\approx \begin{bmatrix} 1 & 0 & \cdots & 0 \\\\ 0 & 0 & \cdots & 0 \\\\ \vdots & \vdots & \ddots & \vdots \\\\ 0 & 0 & \cdots & 0  \end{bmatrix} - \begin{bmatrix} 1 & 0 & \cdots & 0 \\\\ 0 & 0 & \cdots & 0 \\\\ \vdots & \vdots & \ddots & \vdots \\\\ 0 & 0 & \cdots & 0  \end{bmatrix}=0$$

> - 结论: 综上可以得出, 所有的梯度都消失为0(接近于0), 参数几乎无法更新, 模型收敛困难.

### 4 维度与点积大小的关系

- 针对为什么维度会影响点积的大小, 原始论文中有这样的一点解释如下:

```text
To illustrate why the dot products get large, assume that the components of q and k
are independent random variables with mean 0 and variance 1. Then their doct product,
q*k = (q1k1+q2k2+......+q(d_k)k(d_k)), has mean 0 and variance d_k.
```

> - 我们分两步对其进行一个推导, 首先就是假设向量q和k的各个分量是相互独立的随机变量, X = q_i, Y = k_i, X和Y各自有d_k个分量, 也就是向量的维度等于d_k, 有E(X) = E(Y) = 0, 以及D(X) = D(Y) = 1.
> - 可以得到E(XY) = E(X)E(Y) = 0 * 0 = 0
> - 同理, 对于D(XY)推导如下:

$$\begin{align*}
D(XY) & = E(X^2\cdot Y^2)-[E(XY)]^2 \\\\
&=E(X^2)E(Y^2)-[E(X)E(Y)]^2 \\\\
&=E(X^2-0^2)E(Y^2-0^2)-[E(X)E(Y)]^2 \\\\
&=E(X^2-[E(X)]^2)E(Y^2-[E(Y)]^2)-[E(X)E(Y)]^2 \\\\
&=D(X)D(Y)-[E(X)E(Y)]^2 \\\\
&=1 \times 1- (0 \times 0)^2 \\\\
&=1
\end{align*}$$

> - 根据期望和方差的性质, 对于互相独立的变量满足下式:

$$E(\sum_iZ_i) =\sum_iE(Z_i),\\\\
D(\sum_iZ_i) =\sum_iD(Z_i)$$

> - 上述公式，简读为：和的期望，等于期望的和；和的方差等于方差的和
> - 根据上面的公式, 可以很轻松的得出q*k的均值为E(qk) = 0, D(qk) = d_k.
> - 所以方差越大, 对应的qk的点积就越大, 这样softmax的输出分布就会更偏向最大值所在的分量.
> - 一个技巧就是将点积除以sqrt(d_k), 将方差在数学上重新"拉回1", 如下所示:

$$D(\frac{q\cdot k}{\sqrt{d_k}})=\frac{d_k}{(\sqrt{d_k})^2}=1$$

> - 最终的结论: 通过数学上的技巧将方差控制在1, 也就有效的控制了点积结果的发散, 也就控制了对应的梯度消失的问题!

## Multi head Attention详解
### 1 采用Multi-head Attention的原因

- 原始论文中提到进行Multi-head Attention的原因是将模型分为多个头, 可以形成多个子空间, 让模型去关注不同方面的信息, 最后再将各个方面的信息综合起来得到更好的效果.
- 多个头进行attention计算最后再综合起来, 类似于CNN中采用多个卷积核的作用, 不同的卷积核提取不同的特征, 关注不同的部分, 最后再进行融合.
- 直观上讲, 多头注意力有助于神经网络捕捉到更丰富的特征信息.

### 2 Multi-head Attention的计算方式

- Multi-head Attention和单一head的Attention唯一的区别就在于, 其对特征张量的最后一个维度进行了分割, 一般是对词嵌入的embedding_dim=512进行切割成head=8, 这样每一个head的嵌入维度就是512/8=64, 后续的Attention计算公式完全一致, 只不过是在64这个维度上进行一系列的矩阵运算而已.
- 在head=8个头上分别进行注意力规则的运算后, 简单采用拼接concat的方式对结果张量进行融合就得到了Multi-head Attention的计算结果.

## Transformer优势
### 1 Transformer的并行计算

对于Transformer比传统序列模型RNN/LSTM具备优势的第一大原因就是强大的并行计算能力.

- 对于RNN来说, 任意时刻t的输入是时刻t的输入x(t)和上一时刻的隐藏层输出h(t-1), 经过运算后得到当前时刻隐藏层的输出h(t), 这个h(t)也即将作为下一时刻t+1的输入的一部分. 这个计算过程是RNN的本质特征, RNN的历史信息是需要通过这个时间步一步一步向后传递的. 而这就意味着RNN序列后面的信息只能等到前面的计算结束后, 将历史信息通过hidden state传递给后面才能开始计算, 形成链式的序列依赖关系, 无法实现并行.
- 对于Transformer结构来说, 在self-attention层, 无论序列的长度是多少, 都可以一次性计算所有单词之间的注意力关系, 这个attention的计算是同步的, 可以实现并行.

### 2 Transformer架构的并行化过程
#### 2.1 Transformer架构中Encoder的并行化

首先Transformer的并行化主要体现在Encoder模块上.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000106.png]]

- 上图最底层绿色的部分, 整个序列所有的token可以并行的进行Embedding操作, 这一层的处理是没有依赖关系的.
- 自注意力层（Self-Attention Layer）需要先获得整段序列的嵌入，但同一层内所有位置的查询（Query）、键（Key）和值（Value）可以组成矩阵，一次计算全部位置间的注意力分数。因此训练阶段不存在 RNN 那种沿时间步逐个等待前一隐藏状态的递归依赖；层与层之间仍需顺序执行。
- 上图第三层蓝色的部分, 也就是前馈全连接层, 对于不同的向量z之间也是没有依赖关系的, 所以这一层是可以实现并行化处理的. 也就是所有的向量z输入Feed Forward网络的计算可以同步进行, 互不干扰.

#### 2.2 Transformer架构中Decoder的并行化

其次Transformer的并行化也部分的体现在Decoder模块上.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000108.png]]

- Decoder模块在训练阶段采用了并行化处理. 其中Self-Attention和Encoder-Decoder Attention两个子层的并行化也是在进行矩阵乘法, 和Encoder的理解是一致的. 在进行Embedding和Feed Forward的处理时, 因为各个token之间没有依赖关系, 所以也是可以完全并行化处理的, 这里和Encoder的理解也是一致的.
- Decoder模块在预测阶段基本上不认为采用了并行化处理. 因为第一个time step的输入只是一个"SOS", 后续每一个time step的输入也只是依次添加之前所有的预测token.
- 注意: 最重要的区别是训练阶段目标文本如果有20个token, 在训练过程中是一次性的输入给Decoder端, 可以做到一些子层的并行化处理. 但是在预测阶段, 如果预测的结果语句总共有20个token, 则需要重复处理20次循环的过程, 每次的输入添加进去一个token, 每次的输入序列比上一次多一个token, 所以不认为是并行处理.

### 3 Transformer的特征抽取能力

对于Transformer比传统序列模型RNN/LSTM具备优势的第二大原因就是强大的特征抽取能力.

- Transformer因为采用了Multi-head Attention结构和计算机制, 拥有比RNN/LSTM更强大的特征抽取能力, 这里并不仅仅由理论分析得来, 而是大量的试验数据和对比结果, 清楚的展示了Transformer的特征抽取能力远远胜于RNN/LSTM.
- 注意: 不是越先进的模型就越无敌, 在很多具体的应用中RNN/LSTM依然大有用武之地, 要具体问题具体分析.

### 4 为什么说Transformer可以代替seq2seq?
> [!tip] 大白话理解（Plain-language Intuition）
> 编码器先把输入序列整理成表示，解码器再按步骤生成输出。若只靠一个固定长度向量传递整句信息，长句容易形成信息瓶颈；注意力机制让解码器在每一步重新查看编码器的全部位置。
#### 4.1 seq2seq的两大缺陷

- seq2seq架构的第一大缺陷是将Encoder端的所有信息压缩成一个固定长度的语义向量中, 用这个固定的向量来代表编码器端的全部信息. 这样既会造成信息的损耗, 也无法让Decoder端在解码的时候去用注意力聚焦哪些是更重要的信息.
- seq2seq架构的第二大缺陷是无法并行, 本质上和RNN/LSTM无法并行的原因一样.

#### 4.2 Transformer的改进

- Transformer架构同时解决了seq2seq的两大缺陷, 既可以并行计算, 又应用Multi-head Attention机制来解决Encoder固定编码的问题, 让Decoder在解码的每一步可以通过注意力去关注编码器输出中最重要的那些部分.

## Transformer 各子模块作用 formd公式bak
### 1 Encoder模块
#### 1.1 Encoder模块的结构和作用:

- 经典的Transformer结构中的Encoder模块包含6个Encoder Block.
- 每个Encoder Block包含一个多头自注意力层, 和一个前馈全连接层.

#### 1.2 关于Encoder Block

- 在Transformer架构中, 6个一模一样的Encoder Block层层堆叠在一起, 共同组成完整的Encoder, 因此剖析一个Block就可以对整个Encoder的内部结构有清晰的认识.

#### 1.3 多头自注意力层(self-attention)

首先来看self-attention的计算规则图:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000107.png]]

> - 上述attention可以被描述为将query和key-value键值对的一组集合映射到输出, 输出被计算为values的加权和, 其中分配给每个value的权重由query与对应key的相似性函数计算得来. 这种attention的形式被称为Scaled Dot-Product Attention, 对应的数学公式形式如下:

$$Attention(Q,K,V)=Softmax(\frac{Q\cdot K^T}{\sqrt{d_{k}}})\cdot V$$

> - 所谓的多头self-attention层, 则是先将Q, K, V经过参数矩阵进行映射, 再做self-attention, 最后将结果拼接起来送入一个全连接层即可.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000104.png]]

上述的多头self-attention, 对应的数学公式形式如下:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/01-Transformer 架构与注意力（Transformer Architecture and Attention）/01-Transformer 架构与注意力（Transformer Architecture and Attention）-20260813120000103.png]]

$$MultiHead(Q,K,V)=Concat(head_1,\cdots , head_h)W^O\\\\
where \; head_i= Attention(QW_{i}^{Q},KW_{i}^{K},VW_{i}^{V})\\\\
其中\; W_{i}^Q \in \Bbb{R}^{d_{model}\times d_k} ,W_{i}^K \in \Bbb{R}^{d_{model}\times d_k} , W_{i}^V \in \Bbb{R}^{d_{model}\times d_v} ,W_{i}^O \in \Bbb{R}^{hd_v\times d_{model}}$$

多头self-attention层的作用: 实验结果表明, Multi-head可以在更细致的层面上提取不同head的特征, 总体计算量和单一head相同的情况下, 提取特征的效果更佳.

- 前馈全连接层模块
  - 前馈全连接层模块, 由两个线性变换组成, 中间有一个Relu激活函数, 对应的数学公式形式如下: $$ FFN(x)=\max(0,xW_1+b_1)W_2+b_2 $$

> - 注意: 原版论文中的前馈全连接层, 输入和输出的维度均为d_model = 512, 层内的连接维度d_ff = 2048, 均采用4倍的大小关系.
> - 前馈全连接层的作用: 单纯的多头注意力机制并不足以提取到理想的特征, 因此增加全连接层来提升网络的能力.

#### 1.4 Decoder模块

- Decoder模块的结构和作用:
  - 经典的Transformer结构中的Decoder模块包含6个Decoder Block.
  - 每个Decoder Block包含三个子层.
    - 一个多头self-attention层
    - 一个Encoder-Decoder attention层
    - 一个前馈全连接层
- Decoder Block中的多头self-attention层
  - Decoder中的多头self-attention层与Encoder模块一致, 但需要注意的是Decoder模块的多头self-attention需要做look-ahead-mask, 因为在预测的时候"不能看见未来的信息", 所以要将当前的token和之后的token全部mask.
- Decoder Block中的Encoder-Decoder attention层
  - 这一层区别于自注意力机制的Q = K = V, 此处矩阵Q来源于Decoder端经过上一个Decoder Block的输出, 而矩阵K, V则来源于Encoder端的输出, 造成了Q != K = V的情况.
  - 这样设计是为了让Decoder端的token能够给予Encoder端对应的token更多的关注.
- Decoder Block中的前馈全连接层
  - 此处的前馈全连接层和Encoder模块中的完全一样.
- Decoder Block中有2个注意力层的作用: 多头self-attention层是为了拟合Decoder端自身的信息, 而Encoder-Decoder attention层是为了整合Encoder和Decoder的信息.

#### 1.5 Add & Norm模块

- Add & Norm模块接在每一个Encoder Block和Decoder Block中的每一个子层的后面. 具体来说Add表示残差连接, Norm表示LayerNorm.
  - 对于每一个Encoder Block, 里面的两个子层后面都有Add & Norm.
  - 对于每一个Decoder Block, 里面的三个子层后面都有Add & Norm.
  - 具体的数学表达形式为: LayerNorm(x + Sublayer(x)), 其中Sublayer(x)为子层的输出.
- Add残差连接的作用: 和其他神经网络模型中的残差连接作用一致, 都是为了将信息传递的更深, 增强模型的拟合能力. 试验表明残差连接的确增强了模型的表现.
- Norm的作用: 随着网络层数的额增加, 通过多层的计算后参数可能会出现过大, 过小, 方差变大等现象, 这会导致学习过程出现异常, 模型的收敛非常慢. 因此对每一层计算后的数值进行规范化可以提升模型的表现.

#### 1.6 位置编码（Positional Encoding）器Positional Encoding

- Transformer中直接采用正弦函数和余弦函数来编码位置信息, 如下图所示: $$ PE_{(pos, 2i)}=\sin(\frac{pos} {10000^{\frac{2i}{d_{model}}}})\\ PE_{(pos, 2i+1)}=\cos(\frac{pos} {10000^{\frac{2i}{d_{model}}}})\\ $$
- 需要注意: 三角函数应用在此处的一个重要的优点, 因为对于任意的PE(pos+k), 都可以表示为PE(pos)的线性函数, 大大方便计算. 而且周期性函数不受序列长度的限制, 也可以增强模型的泛化能力. $$ \sin(\alpha+\beta)=\sin(\alpha)\cos(\beta)+\cos(\alpha)\sin(\beta)\\ \cos(\alpha+\beta)=\cos(\alpha)\cos(\beta)-\sin(\alpha)\sin(\beta) $$
