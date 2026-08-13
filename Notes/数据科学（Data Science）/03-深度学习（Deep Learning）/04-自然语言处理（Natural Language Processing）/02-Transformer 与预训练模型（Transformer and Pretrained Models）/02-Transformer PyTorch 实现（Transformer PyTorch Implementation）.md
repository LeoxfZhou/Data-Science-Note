---
title: "从零实现 Transformer 编码器与解码器（Transformer Encoder and Decoder from Scratch）"
tags:
  - data-science/nlp
status: published
created: 2026-08-13
published_at: 2026-08-13
---
# 从零实现 Transformer 编码器与解码器（Transformer Encoder and Decoder from Scratch）

## 输入部分实现
### 1 输入部分介绍

输入部分包含:

- 源文本嵌入层及其位置编码器
- 目标文本嵌入层及其位置编码器

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）-20260813120000117.png]]

### 2 文本嵌入层的作用

- 无论是源文本嵌入还是目标文本嵌入，都是为了将文本中词汇的数字表示转变为向量表示, 希望在这样的高维空间捕捉词汇间的关系.
- 文本嵌入层的代码分析:

```python
# 导入必备的工具包
import torch

# 预定义的网络层torch.nn, 工具开发者已经帮助我们开发好的一些常用层,
# 比如，卷积层, lstm层, embedding层等, 不需要我们再重新造轮子.
import torch.nn as nn

# 数学计算工具包
import math

# torch中变量封装函数Variable.
from torch.autograd import Variable
```

```python
# Embeddings类 实现思路分析
# 1 init函数 (self, d_model, vocab)
    # 设置类属性 定义词嵌入层 self.lut层
# 2 forward(x)函数
    # self.lut(x) * math.sqrt(self.d_model)
class Embeddings(nn.Module):
    def __init__(self, d_model, vocab):
        # 参数d_model 每个词汇的特征尺寸 词嵌入维度
        # 参数vocab   词汇表大小
        super(Embeddings, self).__init__()
        self.d_model = d_model
        self.vocab = vocab

        # 定义词嵌入层
        self.lut = nn.Embedding(self.vocab, self.d_model)

    def forward(self, x):
        # 将x传给self.lut并与根号下self.d_model相乘作为结果返回
        # x经过词嵌入后 增大x的值, 词嵌入后的embedding_vector+位置编码信息,值量纲差差不多
        return self.lut(x) * math.sqrt(self.d_model)
```

- nn.Embedding演示:

```text
>>> embedding = nn.Embedding(10, 3)
>>> input = torch.LongTensor([[1,2,4,5],[4,3,2,9]])
>>> embedding(input)
tensor([[[-0.0251, -1.6902,  0.7172],
         [-0.6431,  0.0748,  0.6969],
         [ 1.4970,  1.3448, -0.9685],
         [-0.3677, -2.7265, -0.1685]],

        [[ 1.4970,  1.3448, -0.9685],
         [ 0.4362, -0.4004,  0.9400],
         [-0.6431,  0.0748,  0.6969],
         [ 0.9124, -2.3616,  1.1151]]])

>>> embedding = nn.Embedding(10, 3, padding_idx=0)
>>> input = torch.LongTensor([[0,2,0,5]])
>>> embedding(input)
tensor([[[ 0.0000,  0.0000,  0.0000],
         [ 0.1535, -2.0309,  0.9315],
         [ 0.0000,  0.0000,  0.0000],
         [-0.1655,  0.9897,  0.0635]]])
```

> - 调用

```python
def dm_test_Embeddings():
    d_model = 512   # 词嵌入维度是512维
    vocab = 1000    # 词表大小是1000
    # 实例化词嵌入层
    my_embeddings = Embeddings(d_model, vocab)
    x = Variable(torch.LongTensor([[100,2,421,508],[491,998,1,221]]))
    embed = my_embeddings(x)
    print('embed.shape', embed.shape, '\nembed--->\n',embed)
```

> - 输出效果

```text
embed.shape torch.Size([2, 4, 512])
embed--->
 tensor([[[-19.0429, -44.2167,   2.6662,  ..., -21.1199, -36.5275, -15.6872],
         [-25.4621,  25.6046, -45.5382,  ...,  43.7159,   0.9437,  -3.1733],
         [-15.7487,   8.1787, -20.6409,  ...,  -8.7201,  -3.2585, -22.1298],
         [ 21.5044,   2.0660,  -1.4059,  ...,  -6.3673,   3.4387, -22.4600]],

        [[ 15.7010,   2.6187,  14.1192,  ..., -19.1751,  10.5954,   9.1155],
         [-21.5745,   9.6403,  17.9778,  ...,   2.3668,  30.1526, -30.3724],
         [-17.6655,  33.6687,  19.3059,  ..., -10.6276,  -0.8653,  10.0715],
         [ 12.9400, -23.6355,  -2.4750,  ...,  19.1028,   6.6492, -45.1315]]],
       grad_fn=<MulBackward0>)
```

### 3 位置编码（Positional Encoding）器的作用

因为在Transformer的编码器结构中, 并没有针对词汇位置信息的处理，因此需要在Embedding层后加入位置编码器，将词汇位置不同可能会产生不同语义的信息加入到词嵌入张量中, 以弥补位置信息的缺失.

#### 3.1 位置编码（Positional Encoding）器的代码分析

```python
# 位置编码器类PositionalEncoding 实现思路分析
# 1 init函数  (self, d_model, dropout, max_len=5000)
#   super()函数 定义层self.dropout
#   定义位置编码矩阵pe  定义位置列-矩阵position 定义变化矩阵div_term
#   套公式div_term = torch.exp(torch.arange(0, d_model, 2) * -(math.log(10000.0)/d_model))
#   位置列-矩阵 * 变化矩阵 阿达码积my_matmulres
#   给pe矩阵偶数列奇数列赋值 pe[:, 0::2] pe[:, 1::2]
#   pe矩阵注册到模型缓冲区 pe.unsqueeze(0)三维 self.register_buffer('pe', pe)
# 2 forward(self, x) 返回self.dropout(x)
#   给x数据添加位置特征信息 x = x + Variable( self.pe[:,:x.size()[1]], requires_grad=False)

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout, max_len=5000):
        # 参数d_model 词嵌入维度 eg: 512个特征
        # 参数max_len 单词token个数 eg: 60个单词
        super(PositionalEncoding, self).__init__()

        # 定义dropout层
        self.dropout = nn.Dropout(p=dropout)

        # 思路：位置编码矩阵 + 特征矩阵 相当于给特征增加了位置信息
        # 定义位置编码矩阵PE eg pe[60, 512], 位置编码矩阵和特征矩阵形状是一样的
        pe = torch.zeros(max_len, d_model)

        # 定义位置列-矩阵position  数据形状[max_len,1] eg: [0,1,2,3,4...60]^T
        position = torch.arange(0, max_len).unsqueeze(1)
        # print('position--->', position.shape, position)

        # 定义变化矩阵div_term [1,256]
        # torch.arange(start=1, end=512, 2)结果并不包含end。在start和end之间做一个等差数组 [0, 2, 4, 6 ... 510]
        div_term = torch.exp(torch.arange(0, d_model, 2) * -(math.log(10000.0) / d_model))

        # 位置列-矩阵 @ 变化矩阵 做矩阵运算 [60*1]@ [1*256] ==> 60 *256
        # 矩阵相乘也就是行列对应位置相乘再相加，其含义，给每一个列属性（列特征）增加位置编码信息
        my_matmulres = position * div_term
        # print('my_matmulres--->', my_matmulres.shape, my_matmulres)

        # 给位置编码矩阵奇数列，赋值sin曲线特征
        pe[:, 0::2] = torch.sin(my_matmulres)
        # 给位置编码矩阵偶数列，赋值cos曲线特征
        pe[:, 1::2] = torch.cos(my_matmulres)

        # 形状变化 [60,512]-->[1,60,512]
        pe = pe.unsqueeze(0)

        # 把pe位置编码矩阵 注册成模型的持久缓冲区buffer; 模型保存再加载时，可以根模型参数一样，一同被加载
        # 什么是buffer: 对模型效果有帮助的，但是却不是模型结构中超参数或者参数，不参与模型训练
        self.register_buffer('pe', pe)

    def forward(self, x):
        # 注意：输入的x形状2*4*512  pe是1*60*512 形状 如何进行相加
        # 只需按照x的单词个数 给特征增加位置信息
        x = x + Variable( self.pe[:,:x.size()[1]], requires_grad=False)
        return self.dropout(x)
```

- nn.Dropout演示

```text
>>> m = nn.Dropout(p=0.2)
>>> input = torch.randn(4, 5)
>>> output = m(input)
>>> output
Variable containing:
 0.0000 -0.5856 -1.4094  0.0000 -1.0290
 2.0591 -1.3400 -1.7247 -0.9885  0.1286
 0.5099  1.3715  0.0000  2.2079 -0.5497
-0.0000 -0.7839 -1.2434 -0.1222  1.2815
[torch.FloatTensor of size 4x5]
```

- torch.unsqueeze演示

```text
>>> x = torch.tensor([1, 2, 3, 4])
>>> torch.unsqueeze(x, 0)
tensor([[ 1,  2,  3,  4]])
>>> torch.unsqueeze(x, 1)
tensor([[ 1],
        [ 2],
        [ 3],
        [ 4]])
```

> - 调用

```python
def dm_test_PositionalEncoding():

    d_model = 512  # 词嵌入维度是512维
    vocab = 1000  # 词表大小是1000

    # 1 实例化词嵌入层
    my_embeddings = Embeddings(d_model, vocab)

    # 2 让数据经过词嵌入层 [2,4] --->[2,4,512]
    x = Variable(torch.LongTensor([[100, 2, 421, 508], [491, 998, 1, 221]]))
    embed = my_embeddings(x)
    # print('embed--->', embed.shape)

    # 3 创建pe位置矩阵 生成位置特征数据[1,60,512]
    my_pe = PositionalEncoding(d_model=d_model, dropout=0.1, max_len=60)

    # 4 给词嵌入数据embed 添加位置特征 [2,4,512] ---> [2,4,512]
    pe_result = my_pe(embed)
    print('pe_result.shape--->', pe_result.shape)
    print('pe_result--->', pe_result)
```

> - 输出效果

```text
pe_result.shape---> torch.Size([2, 4, 512])
pe_result---> tensor([[[ -6.3490, -19.3785,  -2.8700,  ..., -23.4560, -31.7405,   9.0657],
         [-27.7453,  19.5398,  62.4924,  ...,  -7.7443,  12.3955, -29.1615],
         [ 80.8307,   4.9565,  -0.7523,  ...,   8.2715,  26.7639,  -6.9124],
         [ 13.3252, -21.8653,   0.0000,  ...,  -8.4563,  17.7678,   9.6917]],

        [[  5.2631,  22.0867,  15.3600,  ...,  80.5963,   2.4491, -36.0901],
         [-19.0809,  67.3568,  10.3016,  ...,  -5.6103, -14.2998, -51.2010],
         [-31.1153,  44.8199,  -6.9740,  ...,  39.6247,  33.6903,  18.5471],
         [ 13.7074,  26.4221, -27.3353,  ...,  24.1987,  29.1897, -20.5858]]],
       grad_fn=<MulBackward0>)
```

#### 3.2 绘制词汇向量中特征的分布曲线

```python
import matplotlib.pyplot as plt
import numpy as np

# 绘制PE位置特征sin-cos曲线
def dm_draw_PE_feature():

    # 1 创建pe位置矩阵[1,5000,20]，每一列数值信息：奇数列sin曲线 偶数列cos曲线
    my_pe = PositionalEncoding(d_model=20, dropout=0)
    print('my_positionalencoding.shape--->', my_pe.pe.shape)

    # 2 创建数据x[1,100,20], 给数据x添加位置特征  [1,100,20] ---> [1,100,20]
    y = my_pe(Variable(torch.zeros(1, 100, 20)))
    print('y--->', y.shape)

    # 3 画图 绘制pe位置矩阵的第4-7列特征曲线
    plt.figure(figsize=(20, 20))
    # 第0个句子的，所有单词的，绘制4到8维度的特征 看看sin-cos曲线变化
    plt.plot(np.arange(100), y[0, :, 4:8].numpy())
    plt.legend(["dim %d" %p for p in [4,5,6,7]])
    plt.show()

    # print('直接查看pe数据形状--->', my_pe.pe.shape) # [1,5000,20]
    # 直接绘制pe数据也是ok
    # plt.figure(figsize=(20, 20))
    # # 第0个句子的，所有单词的，绘制4到8维度的特征 看看sin-cos曲线变化
    # plt.plot(np.arange(100), my_pe.pe[0,0:100, 4:8])
    # plt.legend(["dim %d" %p for p in [4,5,6,7]])
    # plt.show()
```

> - 输出效果:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）-20260813120000110.png]]

> - 效果分析
> - 每条颜色的曲线代表某一个词汇中的特征在不同位置的含义
> - 保证同一词汇随着所在位置不同它对应位置嵌入向量会发生变化
> - 正弦波和余弦波的值域范围都是1到-1这又很好的控制了嵌入数值的大小, 有助于梯度的快速计算

## 编码器（Encoder）部分实现
### 1 编码器（Encoder）介绍

编码器部分: * 由N个编码器层堆叠而成 * 每个编码器层由两个子层连接结构组成 * 第一个子层连接结构包括一个多头自注意力子层和规范化层以及一个残差连接 * 第二个子层连接结构包括一个前馈全连接子层和规范化层以及一个残差连接

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）-20260813120000119.png]]

### 2 掩码张量
#### 2.1 掩码张量介绍

- 掩代表遮掩，码就是我们张量中的数值，它的尺寸不定，里面一般只有1和0的元素，代表位置被遮掩或者不被遮掩，至于是0位置被遮掩还是1位置被遮掩可以自定义，因此它的作用就是让另外一个张量中的一些数值被遮掩，也可以说被替换, 它的表现形式是一个张量.

#### 2.2 掩码张量的作用

- 在transformer中, 掩码张量的主要作用在应用attention(将在下一小节讲解)时，有一些生成的attention张量中的值计算有可能已知了未来信息而得到的，未来信息被看到是因为训练时会把整个输出结果都一次性进行Embedding，但是理论上解码器的的输出却不是一次就能产生最终结果的，而是一次次通过上一次结果综合得出的，因此，未来的信息可能被提前利用. 所以，我们会进行遮掩. 关于解码器的有关知识将在后面的章节中讲解.

#### 2.3 生成掩码张量的代码分析

- 上三角矩阵和np.triu函数演示

```text
# 上三角矩阵：下面矩阵中0组成的形状为上三角矩阵
'''
[[[0. 1. 1. 1. 1.]
  [0. 0. 1. 1. 1.]
  [0. 0. 0. 1. 1.]
  [0. 0. 0. 0. 1.]
  [0. 0. 0. 0. 0.]]]

# nn.triu()函数功能介绍
# def triu（m, k）
    # m：表示一个矩阵
    # K：表示对角线的起始位置（k取值默认为0）
    # return: 返回函数的上三角矩阵
'''

def dm_test_nptriu():
    # 测试产生上三角矩阵
    print(np.triu([[1, 1, 1, 1, 1],
                   [2, 2, 2, 2, 2],
                   [3, 3, 3, 3, 3],
                   [4, 4, 4, 4, 4],
                   [5, 5, 5, 5, 5]], k=1))
    print(np.triu([[1, 1, 1, 1, 1],
                   [2, 2, 2, 2, 2],
                   [3, 3, 3, 3, 3],
                   [4, 4, 4, 4, 4],
                   [5, 5, 5, 5, 5]], k=0))
    print(np.triu([[1, 1, 1, 1, 1],
                   [2, 2, 2, 2, 2],
                   [3, 3, 3, 3, 3],
                   [4, 4, 4, 4, 4],
                   [5, 5, 5, 5, 5]], k=-1))

# 结果输出：
[[0 1 1 1 1]
 [0 0 2 2 2]
 [0 0 0 3 3]
 [0 0 0 0 4]
 [0 0 0 0 0]]

[[1 1 1 1 1]
 [0 2 2 2 2]
 [0 0 3 3 3]
 [0 0 0 4 4]
 [0 0 0 0 5]]

[[1 1 1 1 1]
 [2 2 2 2 2]
 [0 3 3 3 3]
 [0 0 4 4 4]
 [0 0 0 5 5]]
```

> - 生成掩码函数

```python
# 下三角矩阵作用: 生成字符时,希望模型不要使用当前字符和后面的字符。
    # 使用遮掩mask，防止未来的信息可能被提前利用
    # 实现方法： 1 - 上三角矩阵
# 函数 subsequent_mask 实现分析
# 产生上三角矩阵 np.triu(m=np.ones((1, size, size)), k=1).astype('uint8')
# 返回下三角矩阵 torch.from_numpy(1 - my_mask )
def subsequent_mask(size):
    # 产生上三角矩阵 产生一个方阵
    subsequent_mask = np.triu(m = np.ones((1, size, size)), k=1).astype('uint8')
    # 返回下三角矩阵
    return torch.from_numpy(1 - subsequent_mask)
```

> - 调用

```python
def dm_test_subsequent_mask():
    # 产生5*5的下三角矩阵
    size = 5
    sm = subsequent_mask(size)
    print('下三角矩阵--->\n', sm)
```

> - 输出效果

```text
下三角矩阵--->
 tensor([[[1, 0, 0, 0, 0],
         [1, 1, 0, 0, 0],
         [1, 1, 1, 0, 0],
         [1, 1, 1, 1, 0],
         [1, 1, 1, 1, 1]]], dtype=torch.uint8)
```

#### 2.4 掩码张量的可视化

```text
plt.figure(figsize=(5,5))
plt.imshow(subsequent_mask(20)[0])
plt.show()
```

> - 输出效果:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）-20260813120000111.png]]

> - 效果分析:
> - 通过观察可视化方阵, 黄色是1的部分, 这里代表被遮掩, 紫色代表没有被遮掩的信息, 横坐标代表目标词汇的位置, 纵坐标代表可查看的位置;
> - 我们看到, 在0的位置我们一看望过去都是黄色的, 都被遮住了，1的位置一眼望过去还是黄色, 说明第一次词还没有产生, 从第二个位置看过去, 就能看到位置1的词, 其他位置看不到, 以此类推.

#### 2.5 掩码张量总结

- 学习了什么是掩码张量:
  - 掩代表遮掩，码就是我们张量中的数值，它的尺寸不定，里面一般只有1和0的元素，代表位置被遮掩或者不被遮掩，至于是0位置被遮掩还是1位置被遮掩可以自定义，因此它的作用就是让另外一个张量中的一些数值被遮掩, 也可以说被替换, 它的表现形式是一个张量.
- 学习了掩码张量的作用:
  - 在transformer中, 掩码张量的主要作用在应用attention(将在下一小节讲解)时，有一些生成的attetion张量中的值计算有可能已知量未来信息而得到的，未来信息被看到是因为训练时会把整个输出结果都一次性进行Embedding，但是理论上解码器的的输出却不是一次就能产生最终结果的，而是一次次通过上一次结果综合得出的，因此，未来的信息可能被提前利用. 所以，我们会进行遮掩. 关于解码器的有关知识将在后面的章节中讲解.
- 学习并实现了生成向后遮掩的掩码张量函数: subsequent_mask
  - 它的输入是size, 代表掩码张量的大小.
  - 它的输出是一个最后两维形成1方阵的下三角阵.
  - 最后对生成的掩码张量进行了可视化分析, 更深一步理解了它的用途.

### 3 注意力机制（Attention Mechanism）
> [!tip] 大白话理解（Plain-language Intuition）
> 注意力机制像读长文时移动聚光灯：生成当前结果时，不平均依赖所有输入，而是根据当前查询把更高权重放到更相关的位置。权重表示当前计算中的相关程度，不等同于严格因果解释。

我们这里使用的注意力的计算规则: $$ Attention(Q,K,V)=Softmax(\frac{Q\cdot K^T}{\sqrt{d_{k}}})\cdot V $$

#### 3.1 注意力计算规则的代码分析

```python
# 自注意力机制函数attention 实现思路分析
# attention(query, key, value, mask=None, dropout=None)
# 1 求查询张量特征尺寸大小 d_k
# 2 求查询张量q的权重分布socres  q@k^T /math.sqrt(d_k)
# 形状[2,4,512] @ [2,512,4] --->[2,4,4]
# 3 是否对权重分布scores进行 scores.masked_fill(mask == 0, -1e9)
# 4 求查询张量q的权重分布 p_attn F.softmax()
# 5 是否对p_attn进行dropout if dropout is not None:
# 6 求查询张量q的注意力结果表示 [2,4,4]@[2,4,512] --->[2,4,512]
# 7 返回q的注意力结果表示 q的权重分布

def attention(query, key, value, mask=None, dropout=None):
    # query, key, value：代表注意力的三个输入张量
    # mask：代表掩码张量
    # dropout：传入的dropout实例化对象

    # 1 求查询张量特征尺寸大小
    d_k = query.size()[-1]

    # 2 求查询张量q的权重分布socres  q@k^T /math.sqrt(d_k)
    # [2,4,512] @ [2,512,4] --->[2,4,4]
    scores =  torch.matmul(query, key.transpose(-2, -1) ) / math.sqrt(d_k)

   # 3 是否对权重分布scores 进行 masked_fill
    if mask is not None:
        # 根据mask矩阵0的位置 对sorces矩阵对应位置进行掩码
        scores = scores.masked_fill(mask == 0, -1e9)

    # 4 求查询张量q的权重分布 softmax
    p_attn = F.softmax(scores, dim=-1)

    # 5 是否对p_attn进行dropout
    if dropout is not None:
        p_attn = dropout(p_attn)

    # 返回 查询张量q的注意力结果表示 bmm-matmul运算, 注意力查询张量q的权重分布p_attn
    # [2,4,4]*[2,4,512] --->[2,4,512]
    return torch.matmul(p_attn, value), p_attn
```

- tensor.masked_fill演示:

```text
>>> input = Variable(torch.randn(5, 5))
>>> input
Variable containing:
 2.0344 -0.5450  0.3365 -0.1888 -2.1803
 1.5221 -0.3823  0.8414  0.7836 -0.8481
-0.0345 -0.8643  0.6476 -0.2713  1.5645
 0.8788 -2.2142  0.4022  0.1997  0.1474
 2.9109  0.6006 -0.6745 -1.7262  0.6977
[torch.FloatTensor of size 5x5]

>>> mask = Variable(torch.zeros(5, 5))
>>> mask
Variable containing:
 0  0  0  0  0
 0  0  0  0  0
 0  0  0  0  0
 0  0  0  0  0
 0  0  0  0  0
[torch.FloatTensor of size 5x5]

>>> input.masked_fill(mask == 0, -1e9)
Variable containing:
-1.0000e+09 -1.0000e+09 -1.0000e+09 -1.0000e+09 -1.0000e+09
-1.0000e+09 -1.0000e+09 -1.0000e+09 -1.0000e+09 -1.0000e+09
-1.0000e+09 -1.0000e+09 -1.0000e+09 -1.0000e+09 -1.0000e+09
-1.0000e+09 -1.0000e+09 -1.0000e+09 -1.0000e+09 -1.0000e+09
-1.0000e+09 -1.0000e+09 -1.0000e+09 -1.0000e+09 -1.0000e+09
[torch.FloatTensor of size 5x5]
```

> - 调用

```python
def dm_test_attention():

    d_model = 512   # 词嵌入维度是512维
    vocab = 1000    # 词表大小是1000

    # 输入x 是一个使用Variable封装的长整型张量, 形状是2 x 4
    x = Variable(torch.LongTensor([[100, 2, 421, 508], [491, 998, 1, 221]]))
    my_embeddings =  Embeddings(d_model, vocab)
    x = my_embeddings(x)

    dropout = 0.1   # 置0比率为0.1
    max_len = 60    # 句子最大长度

    my_pe = PositionalEncoding(d_model, dropout, max_len)
    pe_result = my_pe(x)

    query = key = value = pe_result # torch.Size([2, 4, 512])
    attn1, p_attn1 = attention(query, key, value)
    print('编码阶段 对注意力权重分布 不做掩码')
    print('注意力权重 p_attn1--->',p_attn1.shape, '\n', p_attn1)  # torch.Size([2, 4, 4])
    print('注意力表示结果 attn1--->', attn1.shape, '\n', attn1)  # torch.Size([2, 4, 512])

    print('*' * 50)
    print('编码阶段 对注意力权重分布 做掩码')
    mask = Variable(torch.zeros(2, 4, 4))
    attn2, p_attn2 = attention(query, key, value, mask=mask)
    print("注意力权重 p_attn2--->", p_attn2.shape, '\n',p_attn2)
    print("注意力表示结果 attn2--->", attn2.shape, '\n', attn2)
```

> - 对注意力权重分布不做掩码

```text
编码阶段 对注意力权重分布 不做掩码
注意力权重 p_attn1---> torch.Size([2, 4, 4])
 tensor([[[1., 0., 0., 0.],
         [0., 1., 0., 0.],
         [0., 0., 1., 0.],
         [0., 0., 0., 1.]],

        [[1., 0., 0., 0.],
         [0., 1., 0., 0.],
         [0., 0., 1., 0.],
         [0., 0., 0., 1.]]], grad_fn=<SoftmaxBackward0>)
注意力表示结果 attn1---> torch.Size([2, 4, 512])
 tensor([[[ 44.7449,  54.3616,  26.8261,  ...,  19.0635, -18.6284,  31.5430],
         [-15.6625,  22.7993,   0.8864,  ...,   5.7670, -13.6669, -24.4659],
         [  7.5418,  37.0576, -16.9318,  ...,  44.9160,  14.9246,   3.9773],
         [ 12.6941,   7.1106, -16.8938,  ...,  41.8852,  -1.2939, -23.8751]],

        [[ 35.8076, -28.2593,   0.0000,  ..., -18.0751,  -7.6109, -18.9212],
         [  0.0000,  13.4511,  60.3647,  ...,  -3.1866, -30.1779,  22.9219],
         [-24.6156,  31.9683,  -2.5262,  ..., -24.2111,  -2.0382,   6.7247],
         [ 33.4411, -20.6284,  -4.9740,  ...,  11.4844,   0.0000,   7.1890]]],
       grad_fn=<UnsafeViewBackward0>)
```

#### 3.2 带有mask的输入参数

> - 带有mask的输出效果

```text
**************************************************
编码阶段 对注意力权重分布 做掩码
注意力权重 p_attn2---> torch.Size([2, 4, 4])
 tensor([[[0.2500, 0.2500, 0.2500, 0.2500],
         [0.2500, 0.2500, 0.2500, 0.2500],
         [0.2500, 0.2500, 0.2500, 0.2500],
         [0.2500, 0.2500, 0.2500, 0.2500]],

        [[0.2500, 0.2500, 0.2500, 0.2500],
         [0.2500, 0.2500, 0.2500, 0.2500],
         [0.2500, 0.2500, 0.2500, 0.2500],
         [0.2500, 0.2500, 0.2500, 0.2500]]], grad_fn=<SoftmaxBackward0>)
注意力表示结果 attn2---> torch.Size([2, 4, 512])
 tensor([[[12.3296, 30.3323, -1.5283,  ..., 27.9079, -4.6661, -3.2052],
         [12.3296, 30.3323, -1.5283,  ..., 27.9079, -4.6661, -3.2052],
         [12.3296, 30.3323, -1.5283,  ..., 27.9079, -4.6661, -3.2052],
         [12.3296, 30.3323, -1.5283,  ..., 27.9079, -4.6661, -3.2052]],

        [[11.1583, -0.8671, 13.2161,  ..., -8.4971, -9.9567,  4.4786],
         [11.1583, -0.8671, 13.2161,  ..., -8.4971, -9.9567,  4.4786],
         [11.1583, -0.8671, 13.2161,  ..., -8.4971, -9.9567,  4.4786],
         [11.1583, -0.8671, 13.2161,  ..., -8.4971, -9.9567,  4.4786]]],
       grad_fn=<UnsafeViewBackward0>)
```

#### 3.3 注意力机制（Attention Mechanism）总结

- 学习并实现了注意力计算规则的函数: attention
  - 它的输入就是Q，K，V以及mask和dropout, mask用于掩码, dropout用于随机置0.
  - 它的输出有两个, query的注意力表示以及注意力张量.

### 4 多头注意力机制（Attention Mechanism）
#### 4.1 多头注意力机制（Attention Mechanism）概念

- 从多头注意力的结构图中，貌似这个所谓的多个头就是指多组线性变换层，其实并不是，我只有使用了一组线性变化层，即三个变换张量对Q，K，V分别进行线性变换，这些变换不会改变原有张量的尺寸，因此每个变换矩阵都是方阵，得到输出结果后，多头的作用才开始显现，每个头开始从词义层面分割输出的张量，也就是每个头都想获得一组Q，K，V进行注意力机制的计算，但是句子中的每个词的表示只获得一部分，也就是只分割了最后一维的词嵌入向量. 这就是所谓的多头，将每个头的获得的输入送到注意力机制中, 就形成多头注意力机制.

#### 4.2 多头注意力机制（Attention Mechanism）结构图

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）-20260813120000112.png]]

#### 4.3 多头注意力机制（Attention Mechanism）的作用

- 这种结构设计能让每个注意力机制去优化每个词汇的不同特征部分，从而均衡同一种注意力机制可能产生的偏差，让词义拥有来自更多元的表达，实验表明可以从而提升模型效果.

#### 4.4 多头注意力机制（Attention Mechanism）的代码实现

```python
# 多头注意力机制类 MultiHeadedAttention 实现思路分析
# 1 init函数  (self, head, embedding_dim, dropout=0.1)
    # 每个头特征尺寸大小self.d_k  多少个头self.head  线性层列表self.linears
    # self.linears = clones(nn.Linear(embedding_dim, embedding_dim), 4)
    # 注意力权重分布self.attn=None  dropout层self.dropout
# 2 forward(self, query, key, value, mask=None)
    # 2-1 掩码增加一个维度[8,4,4] -->[1,8,4,4] 求多少批次batch_size
    # 2-2 数据经过线性层 切成8个头,view(batch_size, -1, self.head, self.d_k), transpose(1,2)数据形状变化
    #     数据形状变化[2,4,512] ---> [2,4,8,64] ---> [2,8,4,64]
    # 2-3 24个头 一起送入到attention函数中求 x, self.attn
    # attention([2,8,4,64],[2,8,4,64],[2,8,4,64],[1,8,4,4]) ==> x[2,8,4,64], self.attn[2,8,4,4]]
    # 2-4 数据形状再变化回来 x.transpose(1,2).contiguous().view(,,)
    # 数据形状变化 [2,8,4,64] ---> [2,4,8,64] ---> [2,4,512]
    # 2-5 返回最后线性层结果 return self.linears[-1](x)

# 深度copy模型 输入模型对象和copy的个数 存储到模型列表中
def clones(module, N):
    return nn.ModuleList([copy.deepcopy(module) for _ in range(N)])

class MultiHeadedAttention(nn.Module):

    def __init__(self, head, embedding_dim, dropout=0.1):

        super(MultiHeadedAttention, self).__init__()
        # 确认数据特征能否被被整除 eg 特征尺寸256 % 头数8
        assert embedding_dim % head == 0
        # 计算每个头特征尺寸 特征尺寸256 // 头数8 = 64
        self.d_k = embedding_dim // head
        # 多少头数
        self.head = head
        # 四个线性层
        self.linears = clones(nn.Linear(embedding_dim, embedding_dim), 4)
        # 注意力权重分布
        self.attn = None
        # dropout层
        self.dropout = nn.Dropout(p = dropout)

    def forward(self, query, key, value, mask=None):

        # 若使用掩码，则掩码增加一个维度[8,4,4] -->[1,8,4,4]
        if mask is not None:
            mask = mask.unsqueeze(0)

        # 求数据多少行 eg:[2,4,512] 则batch_size=2
        batch_size = query.size()[0]

        # 数据形状变化[2,4,512] ---> [2,4,8,64] ---> [2,8,4,64]
        # 4代表4个单词 8代表8个头 让句子长度4和句子特征64靠在一起 更有利捕捉句子特征
        query, key, value = [model(x).view(batch_size, -1, self.head, self.d_k).transpose(1,2)
            for model, x in zip(self.linears, (query, key, value) ) ]

        # myoutptlist_data = []
        # for model, x in zip(self.linears, (query, key, value)):
        #     print('x--->', x.shape) # [2,4,512]
        #     myoutput = model(x)
        #     print('myoutput--->',  myoutput.shape)  # [2,4,512]
        #     # [2,4,512] --> [2,4,8,64] --> [2,8,4,64]
        #     tmpmyoutput = myoutput.view(batch_size, -1,  self.head, self.d_k).transpose(1, 2)
        #     myoutptlist_data.append( tmpmyoutput )
        # mylen = len(myoutptlist_data)   # mylen:3
        # query = myoutptlist_data[0]     # [2,8,4,64]
        # key = myoutptlist_data[1]       # [2,8,4,64]
        # value = myoutptlist_data[2]     # [2,8,4,64]

        # 注意力结果表示x形状 [2,8,4,64] 注意力权重attn形状：[2,8,4,4]
        # attention([2,8,4,64],[2,8,4,64],[2,8,4,64],[1,8,4,4]) ==> x[2,8,4,64], self.attn[2,8,4,4]]
        x, self.attn = attention(query, key, value, mask=mask, dropout=self.dropout)

        # 数据形状变化 [2,8,4,64] ---> [2,4,8,64] ---> [2,4,512]
        x = x.transpose(1,2).contiguous().view(batch_size, -1, self.head*self.d_k)

        # 返回最后变化后的结果 [2,4,512]---> [2,4,512]
        return self.linears[-1](x)
```

- tensor.view演示:

```text
>>> x = torch.randn(4, 4)
>>> x.size()
torch.Size([4, 4])
>>> y = x.view(16)
>>> y.size()
torch.Size([16])
>>> z = x.view(-1, 8)  # the size -1 is inferred from other dimensions
>>> z.size()
torch.Size([2, 8])

>>> a = torch.randn(1, 2, 3, 4)
>>> a.size()
torch.Size([1, 2, 3, 4])
>>> b = a.transpose(1, 2)  # Swaps 2nd and 3rd dimension
>>> b.size()
torch.Size([1, 3, 2, 4])
>>> c = a.view(1, 3, 2, 4)  # Does not change tensor layout in memory
>>> c.size()
torch.Size([1, 3, 2, 4])
>>> torch.equal(b, c)
False
```

- torch.transpose演示:

```text
>>> x = torch.randn(2, 3)
>>> x
tensor([[ 1.0028, -0.9893,  0.5809],
        [-0.1669,  0.7299,  0.4942]])
>>> torch.transpose(x, 0, 1)
tensor([[ 1.0028, -0.1669],
        [-0.9893,  0.7299],
        [ 0.5809,  0.4942]])
```

> - 函数调用

```python
# 测试多头注意力机制
def dm_test_MultiHeadedAttention():

    d_model = 512  # 词嵌入维度是512维
    vocab = 1000  # 词表大小是1000
    # 输入x 是一个使用Variable封装的长整型张量, 形状是2 x 4
    x = Variable(torch.LongTensor([[100, 2, 421, 508], [491, 998, 1, 221]]))

    my_embeddings = Embeddings(d_model, vocab)
    x = my_embeddings(x)

    dropout = 0.1  # 置0比率为0.1
    max_len = 60   # 句子最大长度
    my_pe = PositionalEncoding(d_model, dropout, max_len)
    pe_result = my_pe(x)

    head = 8  # 头数head
    query = key = value = pe_result  # torch.Size([2, 4, 512])

    # 输入的掩码张量mask
    mask = Variable(torch.zeros(8, 4, 4))
    my_mha = MultiHeadedAttention(head, d_model, dropout)
    x = my_mha(query, key, value, mask)
    print('多头注意机制后的x', x.shape, '\n', x)
    print('多头注意力机制的注意力权重分布', my_mha.attn.shape)
```

> - 输出效果

```text
多头注意机制后的x torch.Size([2, 4, 512])
tensor([[[-2.9384,  2.5006, -0.8888,  ..., -6.1134, -6.5651, -5.7406],
         [-0.9007,  0.9144, -1.2935,  ..., -6.6897, -6.7292, -6.2146],
         [-3.5213,  1.2106, -4.2973,  ..., -5.6040, -7.7500, -2.3606],
         [-1.3711,  4.1226, -3.8623,  ..., -6.0207, -8.6360, -4.6519]],

        [[ 6.1754,  3.4284, -5.4673,  ..., -7.7355, -6.7766, -4.9681],
         [ 5.4382,  6.4217, -4.3761,  ..., -8.3668, -3.1675, -6.6081],
         [ 9.0191,  3.2935, -4.4196,  ..., -5.2750, -5.3374, -5.1187],
         [ 5.8635,  4.2653, -4.7956,  ..., -9.4884, -8.6182, -4.5732]]],
       grad_fn=<AddBackward0>)
多头注意力机制的注意力权重分布 torch.Size([2, 8, 4, 4])
```

#### 4.5 多头注意力机制（Attention Mechanism）总结

- 学习了什么是多头注意力机制:
  - 每个头开始从词义层面分割输出的张量，也就是每个头都想获得一组Q，K，V进行注意力机制的计算，但是句子中的每个词的表示只获得一部分，也就是只分割了最后一维的词嵌入向量. 这就是所谓的多头.将每个头的获得的输入送到注意力机制中, 就形成了多头注意力机制.
- 学习了多头注意力机制的作用:
  - 这种结构设计能让每个注意力机制去优化每个词汇的不同特征部分，从而均衡同一种注意力机制可能产生的偏差，让词义拥有来自更多元的表达，实验表明可以从而提升模型效果.
- 学习并实现了多头注意力机制的类: MultiHeadedAttention
  - 因为多头注意力机制中需要使用多个相同的线性层, 首先实现了克隆函数clones.
  - clones函数的输入是module，N，分别代表克隆的目标层，和克隆个数.
  - clones函数的输出是装有N个克隆层的Module列表.
  - 接着实现MultiHeadedAttention类, 它的初始化函数输入是h, d_model, dropout分别代表头数，词嵌入维度和置零比率.
  - 它的实例化对象输入是Q, K, V以及掩码张量mask.
  - 它的实例化对象输出是通过多头注意力机制处理的Q的注意力表示.

### 5 前馈全连接层
#### 5.1 前馈全连接层

- 在Transformer中前馈全连接层就是具有两层线性层的全连接网络.
- 前馈全连接层的作用:
  - 考虑注意力机制可能对复杂过程的拟合程度不够, 通过增加两层网络来增强模型的能力.

#### 5.2 前馈全连接层的代码分析

```python
# 前馈全连接层 PositionwiseFeedForward 实现思路分析
# 1 init函数  (self,  d_model, d_ff, dropout=0.1):
   # 定义线性层self.w1 self.w2, self.dropout层
# 2 forward(self, x)
   # 数据经过self.w1(x) -> F.relu() ->self.dropout() ->self.w2 返回

class PositionwiseFeedForward(nn.Module):
    def __init__(self,  d_model, d_ff, dropout=0.1):
        # d_model  第1个线性层输入维度
        # d_ff     第2个线性层输出维度
        super(PositionwiseFeedForward, self).__init__()
        # 定义线性层w1 w2 dropout
        self.w1 = nn.Linear(d_model, d_ff)
        self.w2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(p= dropout)

    def forward(self, x):
        # 数据依次经过第1个线性层 relu激活层 dropout层，然后是第2个线性层
        return  self.w2(self.dropout(F.relu(self.w1(x))))
```

- ReLU函数公式: ReLU(x)=max(0, x)
- ReLU函数图像:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）-20260813120000121.png]]

> - 函数调用

```python
def dm_test_PositionwiseFeedForward():
    d_model = 512  # 词嵌入维度是512维
    vocab = 1000  # 词表大小是1000
    # 输入x 是一个使用Variable封装的长整型张量, 形状是2 x 4
    x = Variable(torch.LongTensor([[100, 2, 421, 508], [491, 998, 1, 221]]))

    my_embeddings = Embeddings(d_model, vocab)
    x = my_embeddings(x)

    dropout = 0.1  # 置0比率为0.1
    max_len = 60  # 句子最大长度
    my_pe = PositionalEncoding(d_model, dropout, max_len)
    pe_result = my_pe(x)

    head = 8  # 头数head
    query = key = value = pe_result  # torch.Size([2, 4, 512])

    # 输入的掩码张量mask
    mask = Variable(torch.zeros(8, 4, 4))
    my_mha = MultiHeadedAttention(head, d_model, dropout)
    x = my_mha(query, key, value, mask)

    # 测试前馈全链接层
    my_PFF = PositionwiseFeedForward(d_model=512, d_ff=64, dropout=0.1)
    ff_result = my_PFF(x)
    print('x--->', ff_result.shape, ff_result)
```

> - 输出效果

```text
x---> torch.Size([2, 4, 512]) tensor([[[-0.1989,  0.5191,  1.3063,  ...,  0.1391, -0.8836,  0.5450],
         [-0.2717,  0.6541,  0.9768,  ..., -0.1452, -0.8929,  0.9798],
         [-0.3297, -0.1791,  0.8489,  ...,  0.6890, -1.0303,  1.1638],
         [ 0.0308, -0.2209,  1.3144,  ..., -0.6433, -1.1207,  0.6042]],

        [[-1.3265, -1.3563,  0.6005,  ..., -0.4166,  0.1078, -0.0522],
         [-0.2736, -2.5544,  1.3333,  ..., -0.1704, -0.3514, -0.1901],
         [-0.0454, -1.1244,  1.4875,  ..., -0.5366, -0.0143,  0.1453],
         [-1.2958, -1.6615,  0.4268,  ..., -0.5896,  0.1486,  0.1122]]],
       grad_fn=<AddBackward0>)
```

#### 5.3 前馈全连接层总结

- 学习了什么是前馈全连接层:
  - 在Transformer中前馈全连接层就是具有两层线性层的全连接网络.
- 学习了前馈全连接层的作用:
  - 考虑注意力机制可能对复杂过程的拟合程度不够, 通过增加两层网络来增强模型的能力.
- 学习并实现了前馈全连接层的类: PositionwiseFeedForward
  - 它的实例化参数为d_model, d_ff, dropout, 分别代表词嵌入维度, 线性变换维度, 和置零比率.
  - 它的输入参数x, 表示上层的输出.
  - 它的输出是经过2层线性网络变换的特征表示.

### 6 规范化层
#### 6.1 规范化层的作用

- 它是所有深层网络模型都需要的标准网络层，因为随着网络层数的增加，通过多层的计算后参数可能开始出现过大或过小的情况，这样可能会导致学习过程出现异常，模型可能收敛非常的慢. 因此都会在一定层数后接规范化层进行数值的规范化，使其特征数值在合理范围内.

#### 6.2 规范化层的代码实现

```python
# 规范化层 LayerNorm 实现思路分析
# 1 init函数  (self, features, eps=1e-6):
   # 定义线性层self.a2 self.b2, nn.Parameter(torch.ones(features))
# 2 forward(self, x) 返回标准化后的结果
    # 对数据求均值 保持形状不变 x.mean(-1, keepdims=True)
    # 对数据求方差 保持形状不变 x.std(-1, keepdims=True)
    # 对数据进行标准化变换 反向传播可学习参数a2 b2
    # eg self.a2 * (x-mean)/(std + self.eps) + self.b2

class LayerNorm(nn.Module):

    def __init__(self, features, eps=1e-6):
        # 参数features 待规范化的数据
        # 参数 eps=1e-6 防止分母为零

        super(LayerNorm, self).__init__()

        # 定义a2 规范化层的系数 y=kx+b中的k
        self.a2 = nn.Parameter(torch.ones(features))

        # 定义b2 规范化层的系数 y=kx+b中的b
        self.b2 = nn.Parameter(torch.zeros(features))

        self.eps = eps

    def forward(self, x):

        # 对数据求均值 保持形状不变
        # [2,4,512] -> [2,4,1]
        mean = x.mean(-1,keepdims=True)

        # 对数据求方差 保持形状不变
        # [2,4,512] -> [2,4,1]
        std = x.std(-1, keepdims=True)

        # 对数据进行标准化变换 反向传播可学习参数a2 b2
        # 注意 * 表示对应位置相乘 不是矩阵运算
        y = self.a2 * (x-mean)/(std + self.eps) + self.b2
        return  y
```

> - 函数调用

```python
# 规范化层测试
def dm_test_LayerNorm():
    embedding_dim = 512  # 词嵌入维度是512维
    vocab = 1000  # 词表大小是1000
    # 输入x 是一个使用Variable封装的长整型张量, 形状是2 x 4
    x = Variable(torch.LongTensor([[100, 2, 421, 508], [491, 998, 1, 221]]))

    emb = Embeddings(embedding_dim, vocab)
    embr = emb(x)

    dropout = 0.2
    max_len = 60  # 句子最大长度
    x = embr  # [2, 4, 512]
    pe = PositionalEncoding(embedding_dim, dropout, max_len)
    pe_result = pe(x)

    query = key = value = pe_result  # torch.Size([2, 4, 512])
    # 调用验证

    d_ff = 64
    head = 8

    # 多头注意力机制的输出 作为前馈全连接层的输入
    mask = Variable(torch.zeros(8, 4, 4))
    mha = MultiHeadedAttention(head, embedding_dim, dropout)
    mha_result = mha(query, key, value, mask)

    x = mha_result
    ff = PositionwiseFeedForward(embedding_dim, d_ff, dropout)
    ff_result = ff(x)

    features = d_model = 512
    eps = 1e-6
    x = ff_result
    ln = LayerNorm(features, eps)
    ln_result = ln(x)
    print('规范化层:', ln_result.shape, ln_result)
```

> - 输出效果

```text
规范化层: torch.Size([2, 4, 512]) tensor([[[ 1.1413, -0.0875,  1.9878,  ...,  0.4824,  1.2250, -0.5582],
         [ 0.3969,  0.0417,  0.6030,  ...,  0.6712,  0.0858, -0.7419],
         [ 0.1618, -0.4729,  1.1678,  ..., -0.4206,  0.2535,  1.0424],
         [ 0.2952, -0.1489,  0.7079,  ...,  0.5554,  0.3931,  0.4711]],

        [[ 0.8428,  0.9732, -1.2423,  ..., -1.1651, -1.3559,  1.0449],
         [ 1.4975, -0.2760, -0.9415,  ..., -0.2475, -1.1027,  0.8396],
         [ 0.5669,  1.0264, -0.6982,  ..., -0.5022, -0.7629,  0.7721],
         [ 1.2806, -0.3767, -0.0539,  ..., -0.4042, -0.4116,  0.3944]]],
       grad_fn=<AddBackward0>)
```

#### 6.3 规范化层总结

- 学习了规范化层的作用:
  - 它是所有深层网络模型都需要的标准网络层，因为随着网络层数的增加，通过多层的计算后参数可能开始出现过大或过小的情况，这样可能会导致学习过程出现异常，模型可能收敛非常的慢. 因此都会在一定层数后接规范化层进行数值的规范化，使其特征数值在合理范围内.
- 学习并实现了规范化层的类: LayerNorm
  - 它的实例化参数有两个, features和eps，分别表示词嵌入特征大小，和一个足够小的数.
  - 它的输入参数x代表来自上一层的输出.
  - 它的输出就是经过规范化的特征表示.

### 7 子层连接结构
#### 7.1 子层连接结构

- 如图所示，输入到每个子层以及规范化层的过程中，还使用了残差链接（跳跃连接），因此我们把这一部分结构整体叫做子层连接（代表子层及其链接结构），在每个编码器层中，都有两个子层，这两个子层加上周围的链接结构就形成了两个子层连接结构.
- 子层连接结构图:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）-20260813120000113.png]]

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）-20260813120000114.png]]

#### 7.2 子层连接结构的代码分析

```python
# 子层连接结构 子层(前馈全连接层 或者 注意力机制层)+ norm层 + 残差连接
# SublayerConnection实现思路分析
# 1 init函数  (self, size, dropout=0.1):
   # 定义self.norm层 self.dropout层, 其中LayerNorm(size)
# 2 forward(self, x, sublayer) 返回+以后的结果
    # 数据self.norm() -> sublayer()->self.dropout() + x

class SublayerConnection(nn.Module):
    def __init__(self, size, dropout=0.1):
        # 参数size 词嵌入维度尺寸大小
        # 参数dropout 置零比率

        super(SublayerConnection, self).__init__()
        # 定义norm层
        self.norm = LayerNorm(size)
        # 定义dropout
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, sublayer):
        # 参数x 代表数据
        # sublayer 函数入口地址 子层函数(前馈全连接层 或者 注意力机制层函数的入口地址)
        # 方式1 # 数据self.norm() -> sublayer()->self.dropout() + x
        myres = x + self.dropout(sublayer(self.norm(x)))
        # 方式2 # 数据sublayer() -> self.norm() ->self.dropout() + x
        # myres = x + self.dropout(self.norm(x.subtype(x)))
        return myres
```

> - 函数调用

```python
def dm_test_SublayerConnection():
    size = 512
    head = 8
    d_model = 512
    vocab = 1000  # 词表大小是1000
    # 输入x 是一个使用Variable封装的长整型张量, 形状是2 x 4
    x = Variable(torch.LongTensor([[100, 2, 421, 508], [491, 998, 1, 221]]))

    emb = Embeddings(d_model, vocab)
    embr = emb(x)

    dropout = 0.2
    max_len = 60  # 句子最大长度
    x = embr  # [2, 4, 512]
    pe = PositionalEncoding(d_model, dropout, max_len)
    pe_result = pe(x)

    x = pe_result
    mask = Variable(torch.zeros(8, 4, 4))

    # 多头自注意力子层
    self_attn = MultiHeadedAttention(head, d_model)
    sublayer = lambda x:self_attn(x, x, x, mask)

    # 子层链接结构
    sc = SublayerConnection(size, dropout)
    sc_result = sc(x, sublayer)
    print('sc_result.shape--->', sc_result.shape)
    print('sc_result--->', sc_result)
```

> - 输出效果

```text
sc_result.shape---> torch.Size([2, 4, 512])
sc_result---> tensor([[[-30.8925,  57.5868,  -6.7073,  ...,   2.2304,   0.0866, -25.0320],
         [ 19.7721,  -0.2945, -10.9359,  ...,  -0.1355,  -9.1049,  35.7419],
         [  0.1608,   3.0822,   0.1203,  ...,   2.9998,  40.5865,  12.3813],
         [  0.0765,  14.6370, -22.0670,  ...,   6.8273,   0.2928,  26.7776]],

        [[ -0.2359,  -0.0000, -26.8415,  ...,  10.3175, -25.3874,  20.8764],
         [ 23.7864,  -0.2481,  51.0186,  ...,  -7.8931,   9.0427,  -2.3697],
         [-21.1101,  -0.4014,  37.0955,  ..., -26.1717,  35.2731, -37.8626],
         [  7.5792,  21.9032, -18.7778,  ...,   4.6249, -33.6907,  22.5649]]],
       grad_fn=<AddBackward0>)
```

#### 7.3 子层连接结构总结

- 什么是子层连接结构:
  - 如图所示，输入到每个子层以及规范化层的过程中，还使用了残差链接（跳跃连接），因此我们把这一部分结构整体叫做子层连接（代表子层及其链接结构）, 在每个编码器层中，都有两个子层，这两个子层加上周围的链接结构就形成了两个子层连接结构.
- 学习并实现了子层连接结构的类: SublayerConnection
  - 类的初始化函数输入参数是size, dropout, 分别代表词嵌入大小和置零比率.
  - 它的实例化对象输入参数是x, sublayer, 分别代表上一层输出以及子层的函数表示.
  - 它的输出就是通过子层连接结构处理的输出.

### 8 编码器（Encoder）层
#### 8.1 编码器（Encoder）层的作用

- 作为编码器的组成单元, 每个编码器层完成一次对输入的特征提取过程, 即编码过程.
- 编码器层的构成图:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）-20260813120000115.png]]

#### 8.2 编码器（Encoder）层的代码分析

```python
# 编码器层类 EncoderLayer 实现思路分析
# init函数 (self, size, self_attn, feed_forward, dropout):
    # 实例化多头注意力层对象self_attn # 前馈全连接层对象feed_forward  size词嵌入维度512
    # clones两个子层连接结构 self.sublayer = clones(SublayerConnection(size,dropout),2)
# forward函数 (self, x, mask)
    # 数据经过子层连接结构1 self.sublayer[0](x, lambda x: self.self_attn(x, x, x, mask))
    # 数据经过子层连接结构2 self.sublayer[1](x, self.feed_forward)

class EncoderLayer(nn.Module):
    def __init__(self, size, self_atten, feed_forward, dropout):

        super(EncoderLayer, self).__init__()
        # 实例化多头注意力层对象
        self.self_attn = self_atten

        # 前馈全连接层对象feed_forward
        self.feed_forward = feed_forward

        # size词嵌入维度512
        self.size = size

        # clones两个子层连接结构 self.sublayer = clones(SublayerConnection(size,dropout),2)
        self.sublayer = clones(SublayerConnection(size, dropout) ,2)

    def forward(self, x, mask):

        # 数据经过第1个子层连接结构
        # 参数x：传入的数据  参数lambda x... : 子函数入口地址
        x = self.sublayer[0](x, lambda x:self.self_attn(x, x, x, mask))

        # 数据经过第2个子层连接结构
        # 参数x：传入的数据  self.feed_forward子函数入口地址
        x = self.sublayer[1](x, self.feed_forward)
        return  x
```

> - 函数调用

```python
def dm_test_EncoderLayer():

    d_model = 512
    vocab = 1000  # 词表大小是1000
    # 输入x 是一个使用Variable封装的长整型张量, 形状是2 x 4
    x = Variable(torch.LongTensor([[100, 2, 421, 508], [491, 998, 1, 221]]))

    emb = Embeddings(d_model, vocab)
    embr = emb(x)

    dropout = 0.2
    max_len = 60  # 句子最大长度
    x = embr  # [2, 4, 512]
    pe = PositionalEncoding(d_model, dropout, max_len)
    pe_result = pe(x)

    x = pe_result

    size = 512
    head = 8
    d_ff = 64

    # 实例化多头注意力机制类对象
    self_attn = MultiHeadedAttention(head, d_model)
    # 实例化前馈全连接层对象
    ff = PositionwiseFeedForward(d_model, d_ff, dropout)
    # mask数据
    mask = Variable(torch.zeros(8, 4, 4))

    # 实例化编码器层对象
    my_encoderlayer = EncoderLayer(size, self_attn, ff, dropout)

    # 数据通过编码层编码
    el_result = my_encoderlayer(x, mask)
    print('el_result.shape', el_result.shape, el_result)
```

> - 输出效果

```text
el_result.shape torch.Size([2, 4, 512])
tensor([[[ 27.1315,  64.8418, -10.6292,  ..., -23.3170, -30.5543,  13.2727],
         [ -0.1474,  54.1129,   0.0000,  ...,  -0.1820, -35.7688, -15.1666],
         [ -0.0691,   8.3125,   7.3380,  ...,  40.2273, -10.4544, -14.1511],
         [ 34.2015, -25.0465, -31.5629,  ..., -42.4037, -35.9813,  44.9897]],

        [[ -8.8238,   0.0935, -13.7027,  ..., -20.9247, -19.9678,  -0.1526],
         [-18.8739,   0.3252,  28.1221,  ...,  34.7250,  -0.7414,   8.1599],
         [ 52.2108,  -0.6148, -16.3005,  ...,   3.1570, -15.0894,   0.9009],
         [-22.5749, -54.0201,   3.9647,  ...,  12.6702,  -0.2983,  13.6588]]],
       grad_fn=<AddBackward0>)
```

#### 8.3 编码器（Encoder）层总结

- 学习了编码器层的作用:
  - 作为编码器的组成单元, 每个编码器层完成一次对输入的特征提取过程, 即编码过程.
- 学习并实现了编码器层的类: EncoderLayer
  - 类的初始化函数共有4个, 别是size，其实就是我们词嵌入维度的大小. 第二个self_attn，之后我们将传入多头自注意力子层实例化对象, 并且是自注意力机制. 第三个是feed_froward, 之后我们将传入前馈全连接层实例化对象. 最后一个是置0比率dropout.
  - 实例化对象的输入参数有2个，x代表来自上一层的输出, mask代表掩码张量.
  - 它的输出代表经过整个编码层的特征表示.

### 9 编码器（Encoder）
#### 9.1 编码器（Encoder）的作用

- 编码器用于对输入进行指定的特征提取过程, 也称为编码, 由N个编码器层堆叠而成.
- 编码器的结构图:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）-20260813120000119.png]]

#### 9.2 编码器（Encoder）的代码分析

```python
# 编码器类 Encoder 实现思路分析
# init函数 (self, layer, N)
    # 实例化多个编码器层对象self.layers   通过方法clones(layer, N)
    # 实例化规范化层 self.norm = LayerNorm(layer.size)
# forward函数 (self, x, mask)
    # 数据经过N个层 x = layer(x, mask)
    #  返回规范化后的数据 return self.norm(x)

class Encoder(nn.Module):
    def __init__(self, layer, N):
        # 参数layer 1个编码器层
        # 参数 编码器层的个数

        super(Encoder, self).__init__()

        # 实例化多个编码器层对象
        self.layers = clones(layer, N)

        # 实例化规范化层
        self.norm = LayerNorm(layer.size)

    def forward(self, x, mask):
        # 数据经过N个层 x = layer(x, mask)
        for layer in self.layers:
            x = layer(x, mask)

        #  返回规范化后的数据 return self.norm(x)
        return self.norm(x)
```

> - 函数调用

```python
def dm_test_Encoder():
    d_model = 512
    vocab = 1000  # 词表大小是1000
    # 输入x 是一个使用Variable封装的长整型张量, 形状是2 x 4
    x = Variable(torch.LongTensor([[100, 2, 421, 508], [491, 998, 1, 221]]))
    # writeFile("dafdsafds")

    emb = Embeddings(d_model, vocab)
    embr = emb(x)

    dropout = 0.2
    max_len = 60  # 句子最大长度
    x = embr  # [2, 4, 512]
    pe = PositionalEncoding(d_model, dropout, max_len)
    pe_result = pe(x)
    x = pe_result  # 获取位置编码器层 编码以后的结果

    size = 512
    head = 8
    d_model = 512
    d_ff = 64
    c = copy.deepcopy
    attn = MultiHeadedAttention(head, d_model)
    dropout = 0.2
    ff = PositionwiseFeedForward(d_model, d_ff, dropout)
    layer = EncoderLayer(size, c(attn), c(ff), dropout)

    # 编码器中编码器层的个数N
    N = 6
    mask = Variable(torch.zeros(8, 4, 4))

    # 实例化编码器对象
    en = Encoder(layer, N)
    en_result = en(x, mask)
    print('en_result.shape--->', en_result.shape)
    print('en_result--->',en_result )
```

> - 输出效果

```text
en_result.shape---> torch.Size([2, 4, 512])
en_result---> tensor([[[-0.2184,  0.0614, -0.6718,  ..., -0.3551,  1.0668,  1.4026],
         [ 0.7157, -0.0899,  0.0247,  ..., -0.0708,  0.4524,  0.2722],
         [ 0.0519,  1.5825,  1.0757,  ..., -0.8435, -0.0662,  0.6865],
         [-0.0924,  0.0881, -0.1037,  ...,  1.4178, -0.0214,  0.5966]],

        [[-1.4012,  2.1713,  1.6771,  ..., -0.0964,  0.7202,  0.0828],
         [ 0.1039,  1.8749,  0.0414,  ...,  0.5602,  2.9122,  0.0356],
         [-0.1112, -0.5311,  0.4800,  ..., -0.0533, -0.8752,  0.5790],
         [ 0.6887, -0.9975,  0.0244,  ..., -0.2390, -0.9284,  0.8737]]],
       grad_fn=<AddBackward0>)
```

#### 9.3 编码器（Encoder）总结

- 学习了编码器的作用:
  - 编码器用于对输入进行指定的特征提取过程, 也称为编码, 由N个编码器层堆叠而成.
- 学习并实现了编码器的类: Encoder
  - 类的初始化函数参数有两个，分别是layer和N，代表编码器层和编码器层的个数.
  - forward函数的输入参数也有两个, 和编码器层的forward相同, x代表上一层的输出, mask代码掩码张量.
  - 编码器类的输出就是Transformer中编码器的特征提取表示, 它将成为解码器的输入的一部分.

## 解码器（Decoder）部分实现
### 1 解码器（Decoder）介绍

解码器部分:

- 由N个解码器层堆叠而成
- 每个解码器层由三个子层连接结构组成
- 第一个子层连接结构包括一个多头自注意力子层和规范化层以及一个残差连接
- 第二个子层连接结构包括一个多头注意力子层和规范化层以及一个残差连接
- 第三个子层连接结构包括一个前馈全连接子层和规范化层以及一个残差连接

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）-20260813120000120.png]]

- 说明:
- 解码器层中的各个部分，如，多头注意力机制，规范化层，前馈全连接网络，子层连接结构都与编码器中的实现相同. 因此这里可以直接拿来构建解码器层.

### 2 解码器（Decoder）层
#### 2.1 解码器（Decoder）层的作用

- 作为解码器的组成单元, 每个解码器层根据给定的输入向目标方向进行特征提取操作，即解码过程.

#### 2.2 解码器（Decoder）层的代码实现

```python
# 解码器层类 DecoderLayer 实现思路分析
# init函数 (self, size, self_attn, src_attn, feed_forward, dropout)
    # 词嵌入维度尺寸大小size 自注意力机制层对象self_attn 一般注意力机制层对象src_attn 前馈全连接层对象feed_forward
    # clones3子层连接结构 self.sublayer = clones(SublayerConnection(size,dropout),3)
# forward函数 (self, x, memory, source_mask, target_mask)
    # 数据经过子层连接结构1 self.sublayer[0](x, lambda x:self.self_attn(x, x, x, target_mask))
    # 数据经过子层连接结构2 self.sublayer[1](x, lambda x:self.src_attn(x, m, m, source_mask))
    # 数据经过子层连接结构3 self.sublayer[2](x, self.feed_forward)

class DecoderLayer(nn.Module):
    def __init__(self, size, self_attn, src_attn, feed_forward, dropout):
        super(DecoderLayer, self).__init__()
        # 词嵌入维度尺寸大小
        self.size = size
        # 自注意力机制层对象 q=k=v
        self.self_attn = self_attn
        # 一遍注意力机制对象 q!=k=v
        self.src_attn = src_attn
        # 前馈全连接层对象
        self.feed_forward = feed_forward
        # clones3子层连接结构
        self.sublayer = clones(SublayerConnection(size, dropout), 3)

    def forward(self, x, memory, source_mask, target_mask):
        m = memory
        # 数据经过子层连接结构1
        x = self.sublayer[0](x, lambda x:self.self_attn(x, x, x, target_mask))
        # 数据经过子层连接结构2
        x = self.sublayer[1](x, lambda x:self.src_attn (x, m, m, source_mask))
        # 数据经过子层连接结构3
        x = self.sublayer[2](x, self.feed_forward)
        return  x
```

> - 函数调用

```python
def dm_test_DecoderLayer():
    d_model = 512
    vocab = 1000  # 词表大小是1000
    # 输入x 是一个使用Variable封装的长整型张量, 形状是2 x 4
    x = Variable(torch.LongTensor([[100, 2, 421, 508], [491, 998, 1, 221]]))

    emb = Embeddings(d_model, vocab)
    embr = emb(x)

    dropout = 0.2
    max_len = 60  # 句子最大长度
    x = embr  # [2, 4, 512]
    pe = PositionalEncoding(d_model, dropout, max_len)
    pe_result = pe(x)
    x = pe_result  # 获取位置编码器层 编码以后的结果

    # 类的实例化参数与解码器层类似, 相比多出了src_attn, 但是和self_attn是同一个类.
    head = 8
    d_ff = 64
    size = 512
    self_attn = src_attn = MultiHeadedAttention(head, d_model, dropout)

    # 前馈全连接层也和之前相同
    ff = PositionwiseFeedForward(d_model, d_ff, dropout)
    x = pe_result

    # 产生编码器结果 # 注意此函数返回编码以后的结果 要有返回值
    en_result = dm_test_Encoder()
    memory = en_result
    mask = Variable(torch.zeros(8, 4, 4))
    source_mask = target_mask = mask

    # 实例化解码器层 对象
    dl = DecoderLayer(size, self_attn, src_attn, ff, dropout)

    # 对象调用
    dl_result = dl(x, memory, source_mask, target_mask)

    print(dl_result.shape)
    print(dl_result)
```

> - 输出效果

```text
torch.Size([2, 4, 512])
tensor([[[-27.4382,   0.6516,   6.6735,  ..., -42.2930, -44.9728,   0.1264],
         [-28.7835,  26.4919,  -0.5608,  ...,   0.5652,  -2.9634,   9.7438],
         [-19.6998,  13.5164,  45.8216,  ...,  23.9127,  22.0259,  34.0195],
         [ -0.1647,   0.2331, -36.4173,  ..., -20.0557,  29.4576,   2.5048]],

        [[ 29.1466,  50.7677,  26.4624,  ..., -39.1015, -27.9200,  19.6819],
         [-10.7069,  28.0897,  -0.4107,  ..., -35.7795,   9.6881,   0.3228],
         [ -6.9027, -16.0590,  -0.8897,  ...,   4.0253,   2.5961,  37.4659],
         [  9.8892,  32.7008,  -6.6772,  ..., -11.4273, -21.4676,  32.5692]]],
       grad_fn=<AddBackward0>)
```

#### 2.3 解码器（Decoder）层总结

- 学习了解码器层的作用:
  - 作为解码器的组成单元, 每个解码器层根据给定的输入向目标方向进行特征提取操作，即解码过程.
- 学习并实现了解码器层的类: DecoderLayer
  - 类的初始化函数的参数有5个, 分别是size，代表词嵌入的维度大小, 同时也代表解码器层的尺寸，第二个是self_attn，多头自注意力对象，也就是说这个注意力机制需要Q=K=V，第三个是src_attn，多头注意力对象，这里Q!=K=V， 第四个是前馈全连接层对象，最后就是droupout置0比率.
  - forward函数的参数有4个，分别是来自上一层的输入x，来自编码器层的语义存储变量mermory， 以及源数据掩码张量和目标数据掩码张量.
  - 最终输出了由编码器输入和目标数据一同作用的特征提取结果.

### 3 解码器（Decoder）
#### 3.1 解码器（Decoder）的作用

- 根据编码器的结果以及上一次预测的结果, 对下一次可能出现的'值'进行特征表示.

#### 3.2 解码器（Decoder）的代码分析

```python
# 解码器类 Decoder 实现思路分析
# init函数 (self, layer, N):
    # self.layers clones N个解码器层clones(layer, N)
    # self.norm 定义规范化层 LayerNorm(layer.size)
# forward函数 (self, x, memory, source_mask, target_mask)
    # 数据以此经过各个子层  x = layer(x, memory, source_mask, target_mask)
    # 数据最后经过规范化层  return self.norm(x)
    # 返回处理好的数据

class Decoder(nn.Module):

    def __init__(self, layer, N):
        # 参数layer 解码器层对象
        # 参数N 解码器层对象的个数

        super(Decoder, self).__init__()

        # clones N个解码器层
        self.layers = clones(layer, N)

        # 定义规范化层
        self.norm = LayerNorm(layer.size)

    def forward(self, x, memory, source_mask, target_mask):

        # 数据以此经过各个子层
        for layer in self.layers:
            x = layer(x, memory, source_mask, target_mask)

        # 数据最后经过规范化层
        return self.norm(x)
```

> - 函数调用

```python
# 测试 解码器
def dm_test_Decoder():
    d_model = 512
    vocab = 1000  # 词表大小是1000
    # 输入x 是一个使用Variable封装的长整型张量, 形状是2 x 4
    x = Variable(torch.LongTensor([[100, 2, 421, 508], [491, 998, 1, 221]]))

    emb = Embeddings(d_model, vocab)
    embr = emb(x)

    dropout = 0.2
    max_len = 60  # 句子最大长度
    x = embr  # [2, 4, 512]
    pe = PositionalEncoding(d_model, dropout, max_len)
    pe_result = pe(x)
    x = pe_result  # 获取位置编码器层 编码以后的结果

    # 分别是解码器层layer和解码器层的个数N
    size = 512
    d_model = 512
    head = 8
    d_ff = 64
    dropout = 0.2
    c = copy.deepcopy

    # 多头注意力对象
    attn = MultiHeadedAttention(head, d_model)

    # 前馈全连接层
    ff = PositionwiseFeedForward(d_model, d_ff, dropout)

    # 解码器层
    layer = DecoderLayer(d_model, c(attn), c(attn), c(ff), dropout)
    N = 6
    # 输入参数与解码器层的输入参数相同
    x = pe_result

    # 产生编码器结果
    en_result = demo238_test_Encoder()
    memory = en_result

    # 掩码对象
    mask = Variable(torch.zeros(8, 4, 4))

    # sorce掩码 target掩码
    source_mask = target_mask = mask

    # 创建 解码器 对象
    de = Decoder(layer, N)

    # 解码器对象 解码
    de_result = de(x, memory, source_mask, target_mask)
    print(de_result)
    print(de_result.shape)
```

> - 输出结果

```text
tensor([[[ 0.1853, -0.8858, -0.0393,  ..., -1.4989, -1.4008,  0.8456],
         [-1.0841, -0.0777,  0.0836,  ..., -1.5568,  1.4074, -0.0848],
         [-0.4107, -0.1306, -0.0069,  ..., -0.2370, -0.1259,  0.7591],
         [ 1.2895,  0.2655,  1.1799,  ..., -0.2413,  0.9087,  0.4055]],

        [[ 0.3645, -0.3991, -1.2862,  ..., -0.7078, -0.1457, -1.0457],
         [ 0.0146, -0.0639, -1.2143,  ..., -0.7865, -0.1270,  0.5623],
         [ 0.0685, -0.1465, -0.1354,  ...,  0.0738, -0.9769, -1.4295],
         [ 0.3168,  0.6305, -0.1549,  ...,  1.0969,  1.8775, -0.5154]]],
       grad_fn=<AddBackward0>)
torch.Size([2, 4, 512])
```

#### 3.3 解码器（Decoder）总结

- 学习了解码器的作用:
  - 根据编码器的结果以及上一次预测的结果, 对下一次可能出现的'值'进行特征表示.
- 学习并实现了解码器的类: Decoder
  - 类的初始化函数的参数有两个，第一个就是解码器层layer，第二个是解码器层的个数N.
  - forward函数中的参数有4个，x代表目标数据的嵌入表示，memory是编码器层的输出，src_mask, tgt_mask代表源数据和目标数据的掩码张量.
  - 输出解码过程的最终特征表示.

## 输出部分实现
### 1 输出部分介绍

- 输出部分包含:
  - 线性层
  - softmax层

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）-20260813120000118.png]]

### 2 线性层的作用

- 通过对上一步的线性变化得到指定维度的输出, 也就是转换维度的作用.

### 3 softmax层的作用

- 使最后一维的向量中的数字缩放到0-1的概率值域内, 并满足他们的和为1.

#### 3.1 线性层和softmax层的代码分析

```python
# 解码器类 Generator 实现思路分析
# init函数 (self, d_model, vocab_size)
    # 定义线性层self.project
# forward函数 (self, x)
    # 数据 F.log_softmax(self.project(x), dim=-1)

class Generator(nn.Module):
    def __init__(self, d_model, vocab_size):
        # 参数d_model 线性层输入特征尺寸大小
        # 参数vocab_size 线层输出尺寸大小
        super(Generator, self).__init__()
        # 定义线性层
        self.project = nn.Linear(d_model, vocab_size)

    def forward(self, x):
        # 数据经过线性层 最后一个维度归一化 log方式
        x = F.log_softmax(self.project(x), dim=-1)
        return x
```

- nn.Linear演示:

```text
>>> m = nn.Linear(20, 30)
>>> input = torch.randn(128, 20)
>>> output = m(input)
>>> print(output.size())
torch.Size([128, 30])
```

> - 函数调用

```text
if __name__ == '__main__':

    # 实例化output层对象
    d_model = 512
    vocab_size = 1000
    my_generator = Generator(d_model, vocab_size )

    # 准备模型数据
    x = torch.randn(2, 4, 512)

    # 数据经过out层
    gen_result = my_generator(x)
    print('gen_result--->', gen_result.shape, '\n', gen_result)
```

> - 输出效果

```text
gen_result---> torch.Size([2, 4, 1000])
 tensor([[[-6.5949, -7.0295, -6.5928,  ..., -7.4317, -7.5488, -6.4871],
         [-7.0481, -6.2352, -7.2797,  ..., -6.1491, -6.1621, -7.1798],
         [-8.1724, -7.0675, -8.2814,  ..., -6.0033, -7.1100, -7.6844],
         [-6.2466, -6.6074, -6.1852,  ..., -6.8373, -7.6600, -6.8578]],

        [[-7.7598, -7.4174, -6.2134,  ..., -7.8000, -6.9862, -6.9261],
         [-6.4790, -7.5458, -6.2342,  ..., -6.8340, -6.6827, -7.0287],
         [-7.2524, -7.2598, -7.0600,  ..., -7.5680, -6.9492, -6.7689],
         [-6.6260, -6.1928, -6.7045,  ..., -6.6323, -7.9005, -7.5397]]],
       grad_fn=<LogSoftmaxBackward0>)
```

## 模型构建
### 1 模型构建介绍

通过上面的小节, 我们已经完成了所有组成部分的实现, 接下来就来实现完整的编码器-解码器结构.

- Transformer总体架构图:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）/02-Transformer PyTorch 实现（Transformer PyTorch Implementation）-20260813120000116.png]]

### 2 编码器（Encoder）-解码器结构的代码实现

> EncoderDecoder函数完成编码解码的子任务，就是把编码和解码的流程进行封装实现。

```python
# 编码解码内部函数类 EncoderDecoder 实现分析
# init函数 (self, encoder, decoder, source_embed, target_embed, generator)
    # 5个成员属性赋值 encoder 编码器对象 decoder 解码器对象 source_embed source端词嵌入层对象
    # target_embed target端词嵌入层对象 generator 输出层对象
# forward函数 (self, source,  target, source_mask, target_mask)
    # 1 编码 s.encoder(self.src_embed(source), source_mask)
    # 2 解码 s.decoder(self.tgt_embed(target), memory, source_mask, target_mask)
    # 3 输出 s.generator()

# 使用EncoderDecoder类来实现编码器-解码器结构
class EncoderDecoder(nn.Module):
    def __init__(self, encoder, decoder, source_embed, target_embed, generator):
        """初始化函数中有5个参数, 分别是编码器对象, 解码器对象,
           源数据嵌入函数, 目标数据嵌入函数,  以及输出部分的类别生成器对象
        """
        super(EncoderDecoder, self).__init__()
        # 将参数传入到类中
        self.encoder = encoder
        self.decoder = decoder
        self.src_embed = source_embed
        self.tgt_embed = target_embed
        self.generator = generator

    def forward(self, source, target, source_mask, target_mask):
        """在forward函数中，有四个参数, source代表源数据, target代表目标数据,
           source_mask和target_mask代表对应的掩码张量"""

        # 在函数中, 将source, source_mask传入编码函数, 得到结果后,
        # 与source_mask，target，和target_mask一同传给解码函数
        return self.generator(self.decode(self.encode(source, source_mask),
                                          source_mask, target, target_mask))

    def encode(self, source, source_mask):
        """编码函数, 以source和source_mask为参数"""
        # 使用src_embed对source做处理, 然后和source_mask一起传给self.encoder
        return self.encoder(self.src_embed(source), source_mask)

    def decode(self, memory, source_mask, target, target_mask):
        """解码函数, 以memory即编码器的输出, source_mask, target, target_mask为参数"""
        # 使用tgt_embed对target做处理, 然后和source_mask, target_mask, memory一起传给self.decoder
        return self.decoder(self.tgt_embed(target), memory, source_mask, target_mask)
```

> - 实例化参数

```text
vocab_size = 1000
d_model = 512
encoder = en
decoder = de
source_embed = nn.Embedding(vocab_size, d_model)
target_embed = nn.Embedding(vocab_size, d_model)
generator = gen
```

> - 输入参数:

```text
# 假设源数据与目标数据相同, 实际中并不相同
source = target = Variable(torch.LongTensor([[100, 2, 421, 508], [491, 998, 1, 221]]))

# 假设src_mask与tgt_mask相同，实际中并不相同
source_mask = target_mask = Variable(torch.zeros(8, 4, 4))
```

> - 调用:

```text
ed = EncoderDecoder(encoder, decoder, source_embed, target_embed, generator)
ed_result = ed(source, target, source_mask, target_mask)
print(ed_result)
print(ed_result.shape)
```

> - 输出效果:

```text
tensor([[[ 0.2102, -0.0826, -0.0550,  ...,  1.5555,  1.3025, -0.6296],
         [ 0.8270, -0.5372, -0.9559,  ...,  0.3665,  0.4338, -0.7505],
         [ 0.4956, -0.5133, -0.9323,  ...,  1.0773,  1.1913, -0.6240],
         [ 0.5770, -0.6258, -0.4833,  ...,  0.1171,  1.0069, -1.9030]],

        [[-0.4355, -1.7115, -1.5685,  ..., -0.6941, -0.1878, -0.1137],
         [-0.8867, -1.2207, -1.4151,  ..., -0.9618,  0.1722, -0.9562],
         [-0.0946, -0.9012, -1.6388,  ..., -0.2604, -0.3357, -0.6436],
         [-1.1204, -1.4481, -1.5888,  ..., -0.8816, -0.6497,  0.0606]]],
       grad_fn=<AddBackward0>)
torch.Size([2, 4, 512])
```

- 接着将基于以上结构构建用于训练的模型.

### 3 Tansformer模型构建过程的代码分析

> make_model函数初始化一个一个组件对象（轮子对象），调用EncoderDecoder()函数

```python
# make_model函数实现思路分析
# 函数原型 (source_vocab, target_vocab, N=6, d_model=512, d_ff=2048, head=8, dropout=0.1)
# 实例化多头注意力层对象 attn
# 实例化前馈全连接对象ff
# 实例化位置编码器对象position
# 构建 EncoderDecoder对象(Encoder对象, Decoder对象,
    # source端输入部分nn.Sequential(),
    # target端输入部分nn.Sequential(),
    # 线性层输出Generator)
# 对模型参数初始化 nn.init.xavier_uniform_(p)
# 注意使用 c = copy.deepcopy
# 返回model

def make_model(source_vocab, target_vocab, N=6,
               d_model=512, d_ff=2048, head=8, dropout=0.1):
    c = copy.deepcopy
    # 实例化多头注意力层对象
    attn = MultiHeadedAttention(head=8, embedding_dim= 512, dropout=dropout)

    # 实例化前馈全连接对象ff
    ff = PositionwiseFeedForward(d_model=d_model, d_ff=d_ff, dropout=dropout)

    # 实例化 位置编码器对象position
    position = PositionalEncoding(d_model=d_model, dropout=dropout)

    # 构建 EncoderDecoder对象
    model = EncoderDecoder(
        # 编码器对象
        Encoder( EncoderLayer(d_model, c(attn), c(ff), dropout), N),
        # 解码器对象
        Decoder(DecoderLayer(d_model, c(attn), c(attn), c(ff),dropout), N),
        # 词嵌入层 位置编码器层容器
        nn.Sequential(Embeddings(d_model, source_vocab), c(position)),
        # 词嵌入层 位置编码器层容器
        nn.Sequential(Embeddings(d_model, target_vocab), c(position)),
        # 输出层对象
        Generator(d_model, target_vocab))

    for p in model.parameters():
        if p.dim() > 1:
            nn.init.xavier_uniform_(p)

    return model
```

- nn.init.xavier_uniform演示:

```text
# 结果服从均匀分布U(-a, a)
>>> w = torch.empty(3, 5)
>>> w = nn.init.xavier_uniform_(w, gain=nn.init.calculate_gain('relu'))
>>> w
tensor([[-0.7742,  0.5413,  0.5478, -0.4806, -0.2555],
        [-0.8358,  0.4673,  0.3012,  0.3882, -0.6375],
        [ 0.4622, -0.0794,  0.1851,  0.8462, -0.3591]])
```

> - 函数调用

```python
def dm_test_make_model():
    source_vocab = 500
    target_vocab = 1000
    N = 6

    my_transform_modelobj = make_model(source_vocab, target_vocab,
                                       N=6, d_model=512, d_ff=2048, head=8, dropout=0.1)
    print(my_transform_modelobj)

    # 假设源数据与目标数据相同, 实际中并不相同
    source = target = Variable(torch.LongTensor([[1, 2, 3, 8], [3, 4, 1, 8]]))

    # 假设src_mask与tgt_mask相同，实际中并不相同
    source_mask = target_mask = Variable(torch.zeros(8, 4, 4))  #
    mydata = my_transform_modelobj(source, target, source_mask, target_mask)
    print('mydata.shape--->', mydata.shape)
    print('mydata--->', mydata)
```

> - 输出效果1

```text
mydata.shape---> torch.Size([2, 4, 1000])
mydata---> tensor([[[-5.7188, -7.4484, -8.0710,  ..., -9.1009, -7.7561, -6.1054],
         [-6.7604, -8.1813, -8.1233,  ..., -7.7539, -8.1921, -7.0365],
         [-6.6139, -8.4309, -8.0176,  ..., -8.9429, -8.2295, -6.8527],
         [-6.6079, -8.4657, -8.2147,  ..., -8.8127, -6.9746, -6.1084]],

        [[-6.7538, -7.9822, -7.6833,  ..., -8.8334, -7.0283, -7.4291],
         [-6.7661, -7.6868, -8.0763,  ..., -8.6204, -7.7191, -7.6031],
         [-5.9538, -7.0344, -7.3635,  ..., -8.5833, -7.5199, -6.9852],
         [-6.6039, -8.2063, -8.2185,  ..., -8.5063, -6.9020, -7.1619]]],
       grad_fn=<LogSoftmaxBackward0>)
```

> - 输出效果2

```text
# 根据Transformer结构图构建的最终模型结构
EncoderDecoder(
  (encoder): Encoder(
    (layers): ModuleList(
      (0): EncoderLayer(
        (self_attn): MultiHeadedAttention(
          (linears): ModuleList(
            (0): Linear(in_features=512, out_features=512)
            (1): Linear(in_features=512, out_features=512)
            (2): Linear(in_features=512, out_features=512)
            (3): Linear(in_features=512, out_features=512)
          )
          (dropout): Dropout(p=0.1)
        )
        (feed_forward): PositionwiseFeedForward(
          (w_1): Linear(in_features=512, out_features=2048)
          (w_2): Linear(in_features=2048, out_features=512)
          (dropout): Dropout(p=0.1)
        )
        (sublayer): ModuleList(
          (0): SublayerConnection(
            (norm): LayerNorm(
            )
            (dropout): Dropout(p=0.1)
          )
          (1): SublayerConnection(
            (norm): LayerNorm(
            )
            (dropout): Dropout(p=0.1)
          )
        )
      )
      (1): EncoderLayer(
        (self_attn): MultiHeadedAttention(
          (linears): ModuleList(
            (0): Linear(in_features=512, out_features=512)
            (1): Linear(in_features=512, out_features=512)
            (2): Linear(in_features=512, out_features=512)
            (3): Linear(in_features=512, out_features=512)
          )
          (dropout): Dropout(p=0.1)
        )
        (feed_forward): PositionwiseFeedForward(
          (w_1): Linear(in_features=512, out_features=2048)
          (w_2): Linear(in_features=2048, out_features=512)
          (dropout): Dropout(p=0.1)
        )
        (sublayer): ModuleList(
          (0): SublayerConnection(
            (norm): LayerNorm(
            )
            (dropout): Dropout(p=0.1)
          )
          (1): SublayerConnection(
            (norm): LayerNorm(
            )
            (dropout): Dropout(p=0.1)
          )
        )
      )
    )
    (norm): LayerNorm(
    )
  )
  (decoder): Decoder(
    (layers): ModuleList(
      (0): DecoderLayer(
        (self_attn): MultiHeadedAttention(
          (linears): ModuleList(
            (0): Linear(in_features=512, out_features=512)
            (1): Linear(in_features=512, out_features=512)
            (2): Linear(in_features=512, out_features=512)
            (3): Linear(in_features=512, out_features=512)
          )
          (dropout): Dropout(p=0.1)
        )
        (src_attn): MultiHeadedAttention(
          (linears): ModuleList(
            (0): Linear(in_features=512, out_features=512)
            (1): Linear(in_features=512, out_features=512)
            (2): Linear(in_features=512, out_features=512)
            (3): Linear(in_features=512, out_features=512)
          )
          (dropout): Dropout(p=0.1)
        )
        (feed_forward): PositionwiseFeedForward(
          (w_1): Linear(in_features=512, out_features=2048)
          (w_2): Linear(in_features=2048, out_features=512)
          (dropout): Dropout(p=0.1)
        )
        (sublayer): ModuleList(
          (0): SublayerConnection(
            (norm): LayerNorm(
            )
            (dropout): Dropout(p=0.1)
          )
          (1): SublayerConnection(
            (norm): LayerNorm(
            )
            (dropout): Dropout(p=0.1)
          )
          (2): SublayerConnection(
            (norm): LayerNorm(
            )
            (dropout): Dropout(p=0.1)
          )
        )
      )
      (1): DecoderLayer(
        (self_attn): MultiHeadedAttention(
          (linears): ModuleList(
            (0): Linear(in_features=512, out_features=512)
            (1): Linear(in_features=512, out_features=512)
            (2): Linear(in_features=512, out_features=512)
            (3): Linear(in_features=512, out_features=512)
          )
          (dropout): Dropout(p=0.1)
        )
        (src_attn): MultiHeadedAttention(
          (linears): ModuleList(
            (0): Linear(in_features=512, out_features=512)
            (1): Linear(in_features=512, out_features=512)
            (2): Linear(in_features=512, out_features=512)
            (3): Linear(in_features=512, out_features=512)
          )
          (dropout): Dropout(p=0.1)
        )
        (feed_forward): PositionwiseFeedForward(
          (w_1): Linear(in_features=512, out_features=2048)
          (w_2): Linear(in_features=2048, out_features=512)
          (dropout): Dropout(p=0.1)
        )
        (sublayer): ModuleList(
          (0): SublayerConnection(
            (norm): LayerNorm(
            )
            (dropout): Dropout(p=0.1)
          )
          (1): SublayerConnection(
            (norm): LayerNorm(
            )
            (dropout): Dropout(p=0.1)
          )
          (2): SublayerConnection(
            (norm): LayerNorm(
            )
            (dropout): Dropout(p=0.1)
          )
        )
      )
    )
    (norm): LayerNorm(
    )
  )
  (src_embed): Sequential(
    (0): Embeddings(
      (lut): Embedding(11, 512)
    )
    (1): PositionalEncoding(
      (dropout): Dropout(p=0.1)
    )
  )
  (tgt_embed): Sequential(
    (0): Embeddings(
      (lut): Embedding(11, 512)
    )
    (1): PositionalEncoding(
      (dropout): Dropout(p=0.1)
    )
  )
  (generator): Generator(
    (proj): Linear(in_features=512, out_features=11)
  )
)
```
