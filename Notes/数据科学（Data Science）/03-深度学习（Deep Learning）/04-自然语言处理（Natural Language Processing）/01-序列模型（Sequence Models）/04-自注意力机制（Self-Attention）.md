---
title: "自注意力机制的推导与代码实现（Self-Attention Derivation and Implementation）"
tags:
  - data-science/nlp
status: published
created: 2026-08-13
published_at: 2026-08-13
---
# 自注意力机制的推导与代码实现（Self-Attention Derivation and Implementation）

## Self attention演变过程
> [!tip] 大白话理解（Plain-language Intuition）
> 自注意力像让句子中的每个词都向其他词提问：谁与我最相关？相关性变成权重，再用这些权重汇总信息。它能一步连接远距离词，但代价是标准实现对序列长度通常需要平方级注意力矩阵。
> [!tip] 大白话理解（Plain-language Intuition）
> 注意力机制像读长文时移动聚光灯：生成当前结果时，不平均依赖所有输入，而是根据当前查询把更高权重放到更相关的位置。权重表示当前计算中的相关程度，不等同于严格因果解释。
### 1 Self-attention介绍

Self-attention就本质上是一种特殊的attention。这种应用在transformer中最重要的结构之一。前面我们介绍了attention机制，它能够帮我们找到子序列和全局的attention的关系，也就是找到权重值 $w_i$ 。Self-attention向对于attention的变化，其实就是寻找权重值的 $w_i$ 过程不同。下面我们来看看self-attention的运算过程。

- 为了能够产生输出的向量 $y_i$ ，self-attention其实是对所有的输入做了一个加权平均的操作，这个公式和上面的attention是一致的。 $$ y_i = \sum w_{ij}x_j $$
- $j$ 代表整个序列的长度，并且 $j$ 个权重的相加之和等于1。值得一提的是，这里的 $w_{ij}$ 并不是一个需要神经网络学习的参数，它是来源于 $x_i$ 和 $x_j$ 的之间的计算的结果（这里 $w_{ij}$ 的计算发生了变化)。它们之间最简单的一种计算方式，就是使用点积的方式。

$$w_{ij}^\prime = x_{i}^Tx_j$$

> $x_i$ 和 $x_j$ 是一对输入和输出。对于下一个输出的向量 $y_{i+1}$ ，我们有一个全新的输入序列和一个不同的权重值。

- 这个点积的输出的取值范围在负无穷和正无穷之间，所以我们要使用一个 $softmax$ 把它映射到 ![公式](https://www.zhihu.com/equation?tex=%5B0%2C1%5D) 之间，并且要确保它们对于整个序列而言的和为1。 $$ w_{ij} = \frac{exp\;w_{ij}^{\prime}}{\sum_j exp\;w_{ij}^{\prime}} $$
- 以上这些就是self-attention最基本的操作.

### 2 Self-attention和Attention使用方法

根据他们之间的重要区别, 可以区分在不同任务中的使用方法:

- 在神经网络中，通常来说你会有输入层（input），应用激活函数后的输出层（output），在RNN当中你会有状态（state）。如果attention (AT) 被应用在某一层的话，它更多的是被应用在输出或者是状态层上，而当我们使用self-attention（SA），这种注意力的机制更多的实在关注input上。
- Attention (AT) 经常被应用在从编码器（encoder）转换到解码器（decoder）。比如说，解码器的神经元会接受一些AT从编码层生成的输入信息。在这种情况下，AT连接的是**两个不同的组件**（component），编码器和解码器。但是如果我们用**SA**，它就不是关注的两个组件，它只是在关注你应用的**那一个组件**。那这里他就不会去关注解码器了，就比如说在Bert中，使用的情况，我们就没有解码器。
- SA可以在一个模型当中被多次的、独立的使用（比如说在Transformer中，使用了18次；在Bert当中使用12次）。但是，AT在一个模型当中经常只是被使用一次，并且起到连接两个组件的作用。
- **SA比较擅长在一个序列当中，寻找不同部分之间的关系** 。比如说，在词法分析的过程中，能够帮助去理解不同词之间的关系。 **AT却更擅长寻找两个序列之间的关系** ，比如说在翻译任务当中，原始的文本和翻译后的文本。这里也要注意，在翻译任务重，SA也很擅长，比如说Transformer。
- AT可以连接两种不同的模态，比如说图片和文字。SA更多的是被应用在同一种模态上，但是如果一定要使用SA来做的话，也可以将不同的模态组合成一个序列，再使用SA。
- 其实有时候大部分情况，SA这种结构更加的general，在很多任务作为降维、特征表示、特征交叉等功能尝试着应用，很多时候效果都不错。

## Self attention机制的代码实现
### 1 Self-attetion实现步骤

- 这里我们实现的注意力机制是现在比较流行的点积相乘的注意力机制
- self-attention机制的实现步骤
  - 第一步: 准备输入
  - 第二步: 初始化参数
  - 第三步: 获取key，query和value
  - 第四步: 给input1计算attention score
  - 第五步: 计算softmax
  - 第六步: 给value乘上score
  - 第七步: 给value加权求和获取output1
  - 第八步: 重复步骤4-7，获取output2，output3

#### 1.1 准备输入

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/04-自注意力机制（Self-Attention）/04-自注意力机制（Self-Attention）-20260813120000087.png]]

```python
# 这里我们随机设置三个输入, 每个输入的维度是一个4维向量
import torch
x = [
  [1, 0, 1, 0], # Input 1
  [0, 2, 0, 2], # Input 2
  [1, 1, 1, 1]  # Input 3
]
x = torch.tensor(x, dtype=torch.float32)
```

#### 1.2 初始化参数

```text
# 每一个输入都有三个表示，分别为key（橙黄色）query（红色）value（紫色）。比如说，每一个表示我们希望是一个3维的向量。由于输入是4维，所以我们的参数矩阵为 4*3 维。
# 为了能够获取这些表示，每一个输入（绿色）要和key，query和value相乘，在例子中，我们使用如下的方式初始化这些参数。
w_key = [
  [0, 0, 1],
  [1, 1, 0],
  [0, 1, 0],
  [1, 1, 0]
]
w_query = [
  [1, 0, 1],
  [1, 0, 0],
  [0, 0, 1],
  [0, 1, 1]
]
w_value = [
  [0, 2, 0],
  [0, 3, 0],
  [1, 0, 3],
  [1, 1, 0]
]
w_key = torch.tensor(w_key, dtype=torch.float32)
w_query = torch.tensor(w_query, dtype=torch.float32)
w_value = torch.tensor(w_value, dtype=torch.float32)

print("w_key: \n", w_key)
print("w_query: \n", w_query)
print("w_value: \n", w_value)
```

- 输出效果

```text
w_key:
 tensor([[0., 0., 1.],
        [1., 1., 0.],
        [0., 1., 0.],
        [1., 1., 0.]])
w_query:
 tensor([[1., 0., 1.],
        [1., 0., 0.],
        [0., 0., 1.],
        [0., 1., 1.]])
w_value:
 tensor([[0., 2., 0.],
        [0., 3., 0.],
        [1., 0., 3.],
        [1., 1., 0.]])
```

#### 1.3 获取key，query和value

* 使用向量化获取keys的值

```text
               [0, 0, 1]
[1, 0, 1, 0]   [1, 1, 0]   [0, 1, 1]
[0, 2, 0, 2] x [0, 1, 0] = [4, 4, 0]
[1, 1, 1, 1]   [1, 1, 0]   [2, 3, 1]
```

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/04-自注意力机制（Self-Attention）/04-自注意力机制（Self-Attention）-20260813120000090.webp]]

- 使用向量化获取values的值

```text
               [0, 2, 0]
[1, 0, 1, 0]   [0, 3, 0]   [1, 2, 3]
[0, 2, 0, 2] x [1, 0, 3] = [2, 8, 0]
[1, 1, 1, 1]   [1, 1, 0]   [2, 6, 3]
```

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/04-自注意力机制（Self-Attention）/04-自注意力机制（Self-Attention）-20260813120000091.gif]]

- 使用向量化获取querys的值

```text
               [1, 0, 1]
[1, 0, 1, 0]   [1, 0, 0]   [1, 0, 2]
[0, 2, 0, 2] x [0, 0, 1] = [2, 2, 2]
[1, 1, 1, 1]   [0, 1, 1]   [2, 1, 3]
```

```text
# 将query key  value分别进行计算
keys = x @ w_key
querys = x @ w_query
values = x @ w_value
print("Keys: \n", keys)
print("Querys: \n", querys)
print("Values: \n", values)
```

- 输出效果

```text
Keys:
 tensor([[0., 1., 1.],
        [4., 4., 0.],
        [2., 3., 1.]])
Querys:
 tensor([[1., 0., 2.],
        [2., 2., 2.],
        [2., 1., 3.]])
Values:
 tensor([[1., 2., 3.],
        [2., 8., 0.],
        [2., 6., 3.]])
```

#### 1.4 给input1计算attention score

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/04-自注意力机制（Self-Attention）/04-自注意力机制（Self-Attention）-20260813120000092.gif]]

```text
# 为了获取input1的attention score，我们使用点乘来处理所有的key和query，包括它自己的key和value。这样我们就能够得到3个key的表示（因为我们有3个输入），我们就获得了3个attention score（蓝色）
            [0, 4, 2]
[1, 0, 2] x [1, 4, 3] = [2, 4, 4]
            [1, 0, 1]

# 注意: 这里我们只用input1举例.其他的输入的query和input1做相同的操作.
```

```text
attn_scores = querys @ keys.T
print(attn_scores)
```

- 输出效果

```text
tensor([[ 2.,  4.,  4.], # attention scores from Query 1
        [ 4., 16., 12.], # attention scores from Query 2
        [ 4., 12., 10.]])# attention scores from Query 3
```

#### 1.5 计算softmax

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/04-自注意力机制（Self-Attention）/04-自注意力机制（Self-Attention）-20260813120000093.gif]]

给attention score应用softmax。

```text
softmax([2, 4, 4]) = [0.0, 0.5, 0.5]
```

```python
from torch.nn.functional import softmax

attn_scores_softmax = softmax(attn_scores, dim=-1)
print(attn_scores_softmax)
attn_scores_softmax = [
  [0.0, 0.5, 0.5],
  [0.0, 1.0, 0.0],
  [0.0, 0.9, 0.1]
]
attn_scores_softmax = torch.tensor(attn_scores_softmax)
print(attn_scores_softmax)
```

- 输出效果

```text
tensor([[6.3379e-02, 4.6831e-01, 4.6831e-01],
        [6.0337e-06, 9.8201e-01, 1.7986e-02],
        [2.9539e-04, 8.8054e-01, 1.1917e-01]])
tensor([[0.0000, 0.5000, 0.5000],
        [0.0000, 1.0000, 0.0000],
        [0.0000, 0.9000, 0.1000]])
```

#### 1.6 给value乘上score

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/04-自注意力机制（Self-Attention）/04-自注意力机制（Self-Attention）-20260813120000094.gif]]

使用经过softmax后的attention score乘以它对应的value值（紫色），这样就得到了3个weighted values（黄色）。

```text
1: 0.0 * [1, 2, 3] = [0.0, 0.0, 0.0]
2: 0.5 * [2, 8, 0] = [1.0, 4.0, 0.0]
3: 0.5 * [2, 6, 3] = [1.0, 3.0, 1.5]
```

```text
weighted_values = values[:,None] * attn_scores_softmax.T[:,:,None]
print(weighted_values)
```

- 输出效果:

```text
tensor([[[0.0000, 0.0000, 0.0000],
         [0.0000, 0.0000, 0.0000],
         [0.0000, 0.0000, 0.0000]],

        [[1.0000, 4.0000, 0.0000],
         [2.0000, 8.0000, 0.0000],
         [1.8000, 7.2000, 0.0000]],

        [[1.0000, 3.0000, 1.5000],
         [0.0000, 0.0000, 0.0000],
         [0.2000, 0.6000, 0.3000]]])
```

#### 1.7 给value加权求和获取output1

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/04-自注意力机制（Self-Attention）/04-自注意力机制（Self-Attention）-20260813120000095.gif]]

把所有的weighted values（黄色）进行element-wise的相加。

[0.0, 0.0, 0.0]

+ [1.0, 4.0, 0.0]

+ [1.0, 3.0, 1.5]

------------------------

= [2.0, 7.0, 1.5] 得到结果向量[2.0, 7.0, 1.5]（深绿色）就是ouput1的和其他key交互的query representation

#### 1.8 重复步骤4-7，获取output2，output3

```text
outputs = weighted_values.sum(dim=0)
print(outputs)
```

- 输出效果

```text
tensor([[2.0000, 7.0000, 1.5000],
        [2.0000, 8.0000, 0.0000],
        [2.0000, 7.8000, 0.3000]])
```
