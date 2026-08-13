---
title: "RNN、LSTM 与 GRU 原理及 PyTorch 接口（RNN, LSTM, GRU, and PyTorch APIs）"
tags:
  - data-science/nlp
status: published
created: 2026-08-13
published_at: 2026-08-13
---
# RNN、LSTM 与 GRU 原理及 PyTorch 接口（RNN, LSTM, GRU, and PyTorch APIs）

### 词嵌入层
> [!tip] 大白话理解（Plain-language Intuition）
> 词向量不是给词贴一个编号，而是把词放到一个可计算的坐标空间里；经常出现在相似上下文中的词会被放得更近。这样模型才能用距离和方向表达语义关系。

> 在 **RNN（Recurrent Neural Network）** 中，**词嵌入层（Word Embedding Layer）** 是处理自然语言数据的关键组成部分。它将输入的离散单词（通常是词汇表中的索引）转换为连续的、低维的向量表示，从而使得神经网络能够理解和处理这些词汇的语义信息。

#### 词嵌入层作用

词嵌入层的主要目的是**将每个词映射为一个固定长度的向量（将文本转换为向量）**，这些向量能够捕捉词与词之间的语义关系。

传统的文本表示方法（如one-hot编码）无法反映单词之间的相似性，因为在one-hot编码中，每个单词都被表示为一个**高维稀疏向量**，而词嵌入通过**低维稠密向量**表示单词，能够更好地捕捉词汇之间的语义相似性。

词嵌入层首先会根据输入的词的数量构建一个**词向量矩阵**，例如: 我们有 100 个词，每个词希望转换成 128 维度的向量，那么构建的矩阵形状即为: 100*128，输入的每个词都对应了一个该矩阵中的一个向量。

![[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-1734747074293.png|409]]

**词嵌入层在RNN中的作用**：

- **输入表示**：RNN通常用于处理序列数据。在处理文本时，RNN的输入是由单词构成的序列。由于神经网络不能直接处理离散的单词标识符（如整数索引或字符），因此需要通过词嵌入层将每个单词转换为一个固定长度的稠密向量。这些向量作为RNN的输入，帮助RNN理解词语的语义。
- **降低维度**：词嵌入层将原本高维的稀疏表示（如one-hot编码）转化为低维的稠密向量，减少了计算量，同时保持了词汇之间的语义关系。
- **捕捉语义相似性**：通过训练，词嵌入能够学习到词语之间的关系。例如，语义相似的词（如“猫”和“狗”）在向量空间中会比较接近，而语义不相关的词（如“猫”和“汽车”）则会较为遥远。

####  词嵌入层工作流程

- **初始化词向量**：词嵌入层的初始词向量通常会使用随机初始化或者通过加载预训练的词向量（如Word2Vec或GloVe）进行初始化。
- **输入索引**：每个单词在词汇表中都有一个唯一的索引。输入文本（例如一个句子）会先被分词，然后每个单词会被转换为相应的索引。
- **查找词向量**：词嵌入层将这些单词索引映射为对应的词向量。这些词向量是一个低维稠密向量，表示该词的语义。
- **输入到RNN**：这些词向量作为RNN的输入，RNN处理它们并根据上下文生成一个序列的输出。

#### 词嵌入层使用

在PyTorch中，我们可以**使用 nn.Embedding 词嵌入层来实现输入词的向量化**。

nn.Embedding 对象构建时，最主要有两个参数:

- num_embeddings：表示**词的数量**
- embedding_dim：表示**用多少维的向量来表示每个词**

```python
nn.Embedding(num_embeddings=10, embedding_dim=4)
```

接下来，我们将会学习如何将词转换为词向量，其步骤如下:

1. 先将语料进行分词，构建词与索引的映射，我们可以把这个映射叫做词表，词表中每个词都对应了一个唯一的索引；
2. 然后使用 nn.Embedding 构建词嵌入矩阵，词索引对应的向量即为该词对应的数值化后的向量表示。

例如，我们的文本数据为: "北京冬奥的进度条已经过半，不少外国运动员在完成自己的比赛后踏上归途。"，接下来，我们看下如何使用词嵌入层将其进行转换为向量表示，步骤如下：

```python
import torch
import torch.nn as nn
import jieba # pip install jieba -i https://pypi.mirrors.ustc.edu.cn/simple/

if __name__ == '__main__':
    # 0.文本数据
    text = '北京冬奥的进度条已经过半，不少外国运动员在完成自己的比赛后踏上归途。'
    # 1. 文本分词
    words = jieba.lcut(text)
    print('文本分词:', words)
    # 2.分词去重并保留原来的顺序获取所有的词语
    unique_words = list(set(words))
    print("去重后词的个数:\n",len(unique_words))
    # 3. 构建词嵌入层
    # num_embeddings: 表示词的总数量
    # embedding_dim: 表示词嵌入的维度
    embed = nn.Embedding(num_embeddings=len(unique_words), embedding_dim=4)
    print("词嵌入的结果：\n",embed)
    # 4. 词语的词向量表示
    for i, word in enumerate(unique_words):
        # 获得词嵌入向量
        word_vec = embed(torch.tensor(i))
        print('%s\t' % word, word_vec)
```

**输出结果：**

```text
文本分词: ['北京', '冬奥', '的', '进度条', '已经', '过半', '，', '不少', '外国', '运动员', '在', '完成', '自己', '的', '比赛', '后', '踏上', '归途', '。']
去重后词的个数:
 18
词嵌入的结果：
 Embedding(18, 4)
 北京	 tensor([-1.8043,  1.7860, -0.7821, -0.3167], grad_fn=<EmbeddingBackward0>)
  的	 tensor([-1.4856, -0.5639,  0.2745,  0.1087], grad_fn=<EmbeddingBackward0>)
 冬奥	 tensor([ 0.6969, -0.5615,  1.6524, -0.2651], grad_fn=<EmbeddingBackward0>)
 自己	 tensor([1.7163, 0.9710, 0.0193, 1.4562], grad_fn=<EmbeddingBackward0>)
 不少	 tensor([ 0.8770, -1.0347,  0.4939,  1.6718], grad_fn=<EmbeddingBackward0>)
 归途	 tensor([ 0.0619,  0.0355, -1.6510,  0.8121], grad_fn=<EmbeddingBackward0>)
 比赛	 tensor([-1.7128,  0.0681,  2.4199,  0.2714], grad_fn=<EmbeddingBackward0>)
进度条	 tensor([-0.6706,  0.4089, -0.5371,  0.1093], grad_fn=<EmbeddingBackward0>)
 外国	 tensor([ 0.5665, -0.3168, -0.2065,  0.7682], grad_fn=<EmbeddingBackward0>)
 完成	 tensor([ 1.4640, -0.2800, -0.2242, -0.3790], grad_fn=<EmbeddingBackward0>)
 过半	 tensor([ 1.8026,  0.9831, -0.7177,  0.6779], grad_fn=<EmbeddingBackward0>)
 踏上	 tensor([-1.0745, -0.2610, -1.5350, -0.1767], grad_fn=<EmbeddingBackward0>)
运动员	 tensor([1.8748, 0.2093, 1.9471, 0.3893], grad_fn=<EmbeddingBackward0>)
  ，	 tensor([-1.2841, -0.0675, -0.1263, -0.6892], grad_fn=<EmbeddingBackward0>)
  在	 tensor([ 0.6202, -0.0106,  1.0504,  0.0299], grad_fn=<EmbeddingBackward0>)
 已经	 tensor([2.4461, 0.2113, 0.9387, 0.1680], grad_fn=<EmbeddingBackward0>)
  后	 tensor([-1.1989,  0.8727, -0.9484,  0.0578], grad_fn=<EmbeddingBackward0>)
  。	 tensor([0.4020, 0.7357, 0.3571, 1.2355], grad_fn=<EmbeddingBackward0>)
```

### 循环网络层

文本数据是具有序列特性的，例如: "我爱你", 这串文本就是具有序列关系的，"爱" 需要在 "我" 之后，"你" 需要在 "爱" 之后, 如果颠倒了顺序，那么可能就会表达不同的意思。

为了表示出数据的序列关系，我们需要使用循环神经网络(Recurrent Nearal Networks, RNN) 来对数据进行建模，RNN 是一个具有记忆功能的网络，它作用于处理带有序列特点的样本数据。

####  RNN网络层原理
> [!tip] 大白话理解（Plain-language Intuition）
> RNN 像一边读句子、一边维护便签：每读一个词就用当前词更新便签，再把新便签传给下一步。句子很长时，早期信息会经过太多次更新而逐渐变弱。

当我们希望使用循环网络来对 "我爱你" 进行语义提取时，RNN计算过程是什么样的呢？

> [!warning] 原始附件缺失（Missing Source Attachments）
> 以下章节保留了原始笔记的 `01.png`、`02.png`、`03.png` 与 `05.png` 引用，但这些文件未随来源资料进入 Vault，暂时无法显示。正文推导和其他现存图示不受影响；补回同名原图后引用会自动恢复。

上图中h表示==隐藏状态==，隐藏状态保存了**序列数据中的历史信息**，并将这些信息传递给下一个时间步，从而允许RNN处理和预测序列数据中的元素。

每一次的输入都会包含两个值：**上一个时间步的隐藏状态、当前状态的输入值x**

每一次的输出都会包含两个值：**输出当前时间步的隐藏状态、当前时间步的预测结果y**

**隐藏状态作用：**

- **记忆功能**：隐藏状态就像RNN的记忆，它能够在不同的时间步之间传递信息。当一个新的输入进入网络时，当前的隐藏状态会结合这个新输入来生成新的隐藏状态。
- **上下文理解**：由于隐藏状态携带了过去的信息，它可以用于理解和生成与上下文相关的输出。这对于语言模型、机器翻译等任务尤其重要。
- **连接不同时间步**：隐藏状态通过网络内部的循环连接将各个时间步连接起来，使得网络可以处理变长的序列数据。

上图中，为了更加容易理解，虽然画了 3 个神经元, 但是实际上只有一个神经元，"我爱你" 三个字是重复输入到同一个神经元中。

![[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260328152704897.gif]]

我们举个例子来理解上图的工作过程，假设我们要实现文本生成，也就是输入 "我爱" 这两个字，来预测出 "你"，其如下图所示:

将上图展开成不同时间步的形式，如下图所示:

首先初始化出第一个隐藏状态，一般都是全0的一个向量，然后将 "我" 进行词嵌入，转换为向量的表示形式，送入到第一个时间步，然后输出隐藏状态 h1，然后将 h1 和 "爱" 输入到第二个时间步，得到隐藏状态 h2, 将 h2 送入到全连接网络，得到 "你" 的预测概率。

**RNN神经元内部是如何计算的呢？**

**1. 计算隐藏状态：**每个时间步的隐藏状态$$h_t$$是根据当前输入$$x_t$$和前一时刻的隐藏状态$$h_{t-1}$$计算的。

![[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-1734749643694.png|585]]

上述公式中:

- $$W_{ih}$$ 表示输入数据的权重
- $$b_{ih}​$$ 表示输入数据的偏置
- $$W_{hh}​$$ 表示输入隐藏状态的权重
- $$b_{hh}$$ 表示输入隐藏状态的偏置
- $$h_{t-1}$$ 表示输入隐藏状态
- $$h_t​$$ 表示输出隐藏状态

最后对输出的结果使用tanh激活函数进行计算，得到该神经元你的输出隐藏状态。

**2. 计算当前时刻的输出：**网络的输出$$y_t$$是当前时刻的隐藏状态经过一个线性变换得到的。

​			$$y_t=W_{hy}h_t+b_y​$$

- $$y_t​$$ 是当前时刻的输出（通常是一个向量，表示当前时刻的预测值，RNN层的预测值）
- $$h_t​$$ 是当前时刻的隐藏状态
- $$W_{hy}$$ 是从隐藏状态到输出的权重矩阵
- $$b_y$$ 是输出层的偏置项

**3. 词汇表映射**：输出$$y_t$$是一个**向量**，该向量经过**全连接层**后输出得到最终预测结果$$y_{pred}$$，$$y_{pred}$$中每个元素代表当前时刻生成词汇表中某个词的得分（或概率，通过激活函数：如**softmax**）。==词汇表有多少个词，$$y_{pred}$$就有多少个元素值，最大元素值对应的词就是当前时刻预测生成的词。==

**神经元工作机制总结：**

- **接收输入**：每个RNN神经元接收来自输入数据$$x_t$$和前一时刻的隐藏状态$$h_{t-1}$$。
- **更新隐藏状态**：神经元通过一个加权和（由权重矩阵和偏置项组成）更新当前时刻的隐藏状态$$h_t​$$，该隐藏状态包含了来自过去的记忆以及当前输入的信息。
- **输出计算**：基于当前隐藏状态$$h_t​$$，神经元生成当前时刻的输出$$y_t​$$，该输出可以用于任务的最终预测。

  ![[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-1735401373292.png]]

**文本生成示例：**

假设我们使用RNN进行**文本生成**，输入是一个初始词语或一段上下文（例如，“m”）。RNN会通过隐藏状态逐步生成下一个词的概率分布，然后根据概率选择最可能的下一个词。

![[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260328152704508.png]]

1. 输入：“m” → 词向量输入$$x_1$$（对应“m”）
2. 初始化隐藏状态$$h_0​$$，一般初始值为0
3. 隐藏状态更新$$h_1​$$，并计算输出$$y_1​$$
4. 经过全连接层输出层计算输出$$y_{pred}​$$，使用softmax函数将$$y_{pred}​$$转换为概率分布
5. 选择概率最高的词作为输出词（例如“a”）
6. 输入新的词“a”，继续处理下一个时间步，直到生成完整的词或句子

**小结：**在循环神经网络中，**词与输出的对应关系**通常通过以下几个步骤建立

1. **词嵌入**：将词转化为向量表示（词向量）。
2. **RNN处理**：通过RNN层逐步处理词向量，生成每个时间步的隐藏状态。
3. **输出映射**：通过线性变换将隐藏状态映射到输出，通常是一个词汇表中的词的概率分布。

####  PyTorch RNN层的使用

- API介绍

  ```text
  RNN = nn.RNN(input_size, hidden_size，num_layers)
  ```

  参数意义是：

  - input_size：输入数据的维度，一般设为词向量的维度
  - hidden_size：隐藏层h的维度，也是当前层神经元的输出维度
  - num_layers: 隐藏层h的层数，默认为1
- 输入数据和输出结果

  将RNN实例化就可以将数据送入其中进行处理，处理的方式如下所示：

  ```python
  output, hn = RNN(x, h0)
  ```

  - **输入数据：主要包括词嵌入的x 、初始的隐藏层h0**
    - x的表示形式为[seq_len, batch, input_size]，即[句子的长度，batch的大小，词向量的维度]
    - h0的表示形式为[num_layers, batch, hidden_size]，即[隐藏层的层数，batch的大小，隐藏层h的维度]
  - **输出结果：主要包括输出结果output,最后一层的hn**
    - output的表示形式与输入x类似，为[seq_len, batch, input_size]，即[句子的长度，batch的大小，输出向量的维度]
    - hn的表示形式与输入h0一样，为[num_layers, batch, hidden_size]，即[隐藏层的层数，batch的大，隐藏层h的维度]
- API使用

  ```python
  import torch
  import torch.nn as nn

  #  RNN层送入批量数据
  def test():
      # 词向量维度 128, 隐藏向量维度 256
      rnn = nn.RNN(input_size=128, hidden_size=256)
      # 第一个数字: 表示句子长度,也就是词语个数
      # 第二个数字: 批量个数，也就是句子的个数
      # 第三个数字: 词向量维度
      inputs = torch.randn(5, 32, 128)
      hn = torch.zeros(1, 32, 256)
      # 获取输出结果
      output, hn = rnn(inputs, hn)
      print("输出向量的维度：\n",output.shape)
      print("隐藏层输出的维度：\n",hn.shape)

  if __name__ == '__main__':
      test()
  ```

  **输出结果：**

  ```text
  输出向量的维度：
   torch.Size([5, 32, 256])
  隐藏层输出的维度：
   torch.Size([1, 32, 256])
  ```

### 文本生成案例

文本生成任务是一种常见的自然语言处理任务，输入一个开始词能够预测出后面的词序列。本案例将会使用循环神经网络来实现周杰伦歌词生成任务。

![[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-1734750013375.png]]

#### 导入工具包

```python
import torch
import jieba
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
import time
```

#### 数据集

我们收集了周杰伦从第一张专辑《Jay》到第十张专辑《跨时代》中的歌词，来训练神经网络模型，当模型训练好后，我们就可以用这个模型来创作歌词。数据集如下：

```python
想要有直升机
想要和你飞到宇宙去
想要和你融化在一起
融化在宇宙里
我每天每天每天在想想想想著你
这样的甜蜜
让我开始相信命运
感谢地心引力
让我碰到你
漂亮的让我面红的可爱女人
...
```

该数据集共有 5819 行文本。

#### 构建词表

在进行自然语言处理任务之前，首要做的就是构建词表。

所谓的词表就是将语料进行分词，然后给每一个词分配一个唯一的编号，便于我们送入词嵌入层。

![[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-1734750711996.png]]

接下来, 我们对周杰伦歌词的数据进行处理构建词表，具体流程如下：

- 获取文本数据
- 分词，并进行去重
- 构建词表

```python
# 获取数据，并进行分词，构建词表
def build_vocab():
    # 数据集位置
    file_name = 'data/jaychou_lyrics.txt'
    # 分词结果存储位置
    # 唯一词列表
    unique_words = []
    # 每行文本分词列表
    all_words = []
    # 遍历数据集中的每一行文本
    for line in open(file_name, 'r', encoding='utf-8'):
        # 使用jieba分词,分割结果是一个列表
        words = jieba.lcut(line)
        # print(words)
        # 所有的分词结果存储到all_words，其中包含重复的词组
        all_words.append(words)
        # 遍历分词结果，去重后存储到unique_words
        for word in words:
            if word not in unique_words:
                unique_words.append(word)
    # 语料中词的数量
    word_count = len(unique_words)
    # 词到索引映射
    word_to_index = {word: idx for idx, word in enumerate(unique_words)}
    # 歌词文本用词表索引表示
    corpus_idx = []
    # 遍历每一行的分词结果
    for words in all_words:
        temp = []
        # 获取每一行的词，并获取相应的索引
        for word in words:
            temp.append(word_to_index[word])
        # 在每行词之间添加空格隔开
        temp.append(word_to_index[' '])
        # 获取当前文档中每个词对应的索引
        corpus_idx.extend(temp)
    return unique_words, word_to_index, word_count, corpus_idx

if __name__ == "__main__":
    # 获取数据
    unique_words, word_to_index, unique_word_count, corpus_idx = build_vocab()
    print("词的数量：\n",unique_word_count)
    print("去重后的词:\n",unique_words)
    print("每个词的索引：\n",word_to_index)
    print("当前文档中每个词对应的索引：\n",corpus_idx)
```

我们的词典主要包含了:

- unique_words: 存储了每个词
- word_to_index: 存储了词到编号的映射

  ![[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-1734751188623.png]]

#### 构建数据集对象

我们在训练的时候，为了便于读取语料，并送入网络，所以我们会构建一个Dataset对象

```python
class LyricsDataset(torch.utils.data.Dataset):
	def __init__(self, corpus_idx, num_chars):
		# 文档数据中词的索引
		self.corpus_idx = corpus_idx
		# 每个句子中词的个数
		self.num_chars = num_chars
		# 文档数据中词的数量，不去重
		self.word_count = len(self.corpus_idx)
		# 句子数量
		self.number = self.word_count // self.num_chars

	# len(obj)时自动调用此方法
	def __len__(self):
		# 返回句子数量
		return self.number

	# obj[idx]时自动调用此方法
	def __getitem__(self, idx):
		# idx指词的索引，并将其修正索引值到文档的范围里面
		"""
		我 爱你 中国 , 亲爱 的 母亲
		word_count: 7
		num_chars: 2 一个句子由num_chars个词组成
		word_count-num_chars-2: 7-2-1=4  -1:网络预测结果y在x上后移一个词取值-1
		idx=5->start=4
		"""
		start = min(max(idx, 0), self.word_count - self.num_chars - 1)
		end = start + self.num_chars
		# 输入值
		x = self.corpus_idx[start: end]
		# 网络预测结果（目标值）
		y = self.corpus_idx[start + 1: end + 1]
		# 返回结果
		return torch.tensor(x), torch.tensor(y)

if __name__ == "__main__":
	# 获取数据
	unique_words, word_to_index, unique_word_count, corpus_idx = build_vocab()
	# 数据获取实例化
	dataset = LyricsDataset(corpus_idx, 5)
	# 查看句子数量
	print('句子数量：', len(dataset))
	# x, y = dataset.__getitem__(0)
	x, y = dataset[0]
	print("网络输入值：", x)
	print("目标值：", y)
```

**输出结果：**

```text
句子数量： 9827
网络输入值： tensor([ 0,  1,  2,  3, 40])
目标值： tensor([ 1,  2,  3, 40,  0])
```

#### 构建网络模型

我们用于实现《歌词生成》的网络模型，主要包含了三个层:

- 词嵌入层: 用于将语料转换为词向量
- 循环网络层: 提取句子语义
- 全连接层: 输出对词典中每个词的预测概率

```python
# 模型构建
class TextGenerator(nn.Module):
    def __init__(self, unique_word_count):
        super(TextGenerator, self).__init__()
        # 初始化词嵌入层: 语料中词的数量, 词向量的维度为128
        self.ebd = nn.Embedding(unique_word_count, 128)
        # 循环网络层: 词向量维度128, 隐藏向量维度256, 网络层数1
        self.rnn = nn.RNN(128, 256, 1)
        # 输出层: 特征向量维度256与隐藏向量维度相同, 词表中词的个数
        self.out = nn.Linear(256, unique_word_count)

    def forward(self, inputs, hidden):
        # 输出维度: (batch, seq_len, 词向量维度128)
        # batch：句子数量
        # seq_len： 句子长度， 每个句子由多少个词 词数量
        embed = self.ebd(inputs)
        # rnn层x的表示形式为(seq_len, batch, 词向量维度128)
        # output的表示形式与输入x类似，为(seq_len, batch, 词向量维度256)
        # 前后的hidden形状要一样, 所以DataLoader加载器的batch数要能被整数
        output, hidden = self.rnn(embed.transpose(0, 1), hidden)
        # 全连接层输入二维数据， 词数量*词维度
        # 输入维度: (seq_len*batch, 词向量维度256)
        # 输出维度: (seq_len*batch, 语料中词的数量)
        # output: 每个词的分值分布，后续结合softmax输出概率分布
        output = self.out(output.reshape(shape=(-1, output.shape[-1])))
        # 网络输出结果
        return output, hidden

    def init_hidden(self, bs):
        # 隐藏层的初始化:[网络层数, batch, 隐藏层向量维度]
        return torch.zeros(1, bs, 256)

if __name__ == "__main__":
	# 获取数据
	unique_words, word_to_index, unique_word_count, corpus_idx = build_vocab()
	model = TextGenerator(unique_word_count)
	for named, parameter in model.named_parameters():
		print(named)
		print(parameter)
```

#### 构建训练函数

前面的准备工作完成之后, 我们就可以编写训练函数。训练函数主要负责编写数据迭代、送入网络、计算损失、反向传播、更新参数，其流程基本较为固定。

由于我们要实现文本生成，文本生成本质上，输入一串文本，预测下一个文本，也属于分类问题，所以，我们使用多分类交叉熵损失函数。优化方法我们学习过 SGB、AdaGrad、Adam 等，在这里我们选择学习率、梯度自适应的 Adam 算法作为我们的优化方法。

训练完成之后，我们使用 torch.save 方法将模型持久化存储。

```text
def train():
	# 构建词典
	unique_words, word_to_index, unique_word_count, corpus_idx = build_vocab()
	# 数据集 LyricsDataset对象，并实现了 __getitem__ 方法
	lyrics = LyricsDataset(corpus_idx=corpus_idx, num_chars=32)
	# 查看句子数量
	# print(lyrics.number)
	# 初始化模型
	model = TextGenerator(unique_word_count)
	# 数据加载器 DataLoader对象，并将lyrics dataset对象传递给它
	lyrics_dataloader = DataLoader(lyrics, shuffle=True, batch_size=5)
	# 损失函数
	criterion = nn.CrossEntropyLoss()
	# 优化方法
	optimizer = optim.Adam(model.parameters(), lr=1e-3)
	# 训练轮数
	epoch = 10
	for epoch_idx in range(epoch):
		# 训练时间
		start = time.time()
		iter_num = 0  # 迭代次数
		# 训练损失
		total_loss = 0.0
		# 遍历数据集 DataLoader 会在后台调用 dataset.__getitem__(index) 来获取每个样本的数据和标签，并将它们组合成一个 batch
		for x, y in lyrics_dataloader:
			# 隐藏状态的初始化
			hidden = model.init_hidden(bs=5)
			# 模型计算
			output, hidden = model(x, hidden)
			# 计算损失
			# y形状为(batch, seq_len), 需要转换成一维向量->160个词的下标索引
            # output形状为(seq_len, batch, 词向量维度)
            # 需要先将y进行维度交换(和output保持一致)再改变形状
            y = torch.transpose(y, 0, 1).reshape(shape=(-1,))
			loss = criterion(output, y)
			optimizer.zero_grad()
			loss.backward()
			optimizer.step()
			iter_num += 1  # 迭代次数加1
			total_loss += loss.item()
		# 打印训练信息
		print('epoch %3s loss: %.5f time %.2f' % (epoch_idx + 1, total_loss / iter_num, time.time() - start))
	# 模型存储
	torch.save(model.state_dict(), 'model/lyrics_model_%d.pth' % epoch)

if __name__ == "__main__":
	train()
```

**输出结果：**

```text
epoch   1 loss: 1.84424 time 5.75
epoch   2 loss: 0.21154 time 5.91
epoch   3 loss: 0.12014 time 5.85
epoch   4 loss: 0.10625 time 5.73
epoch   5 loss: 0.10226 time 5.58
epoch   6 loss: 0.10009 time 5.65
epoch   7 loss: 0.09942 time 5.66
epoch   8 loss: 0.09783 time 5.66
epoch   9 loss: 0.09663 time 5.75
epoch  10 loss: 0.09568 time 5.77
```

#### 构建预测函数

从磁盘加载训练好的模型，进行预测。预测函数，输入第一个指定的词，我们将该词输入网路，预测出下一个词，再将预测的出的词再次送入网络，预测出下一个词，以此类推，知道预测出我们指定长度的内容。

```python
def predict(start_word, sentence_length):
    # 构建词典
    unique_words, word_to_index, unique_word_count, _ = build_vocab()
    # 构建模型
    model = TextGenerator(unique_word_count)
    # 加载参数
    model.load_state_dict(torch.load('model/lyrics_model_10.pth'))
    # 隐藏状态
    hidden = model.init_hidden(bs=1)
    # 将起始词转换为索引
    word_idx = word_to_index[start_word]
    # 产生的词的索引存放位置
    generate_sentence = [word_idx]
    # 遍历到句子长度，获取每一个词
    for _ in range(sentence_length):
        # 模型预测
        output, hidden = model(torch.tensor([[word_idx]]), hidden)
        # 获取预测结果
        word_idx = torch.argmax(output)
        generate_sentence.append(word_idx)
        # 根据产生的索引获取对应的词，并进行打印
    for idx in generate_sentence:
        print(unique_words[idx], end='')

if __name__ == '__main__':
    # 调用预测函数
    predict('分手', 50)
```

**输出结果：**

```text
分手的话像语言暴力
 我已无能为力再提起 决定中断熟悉
 周杰伦 周杰伦
 一步两步三步四步望著天 看星星
 一颗两颗三颗四颗 连成线背著背默默许下心愿
 看远方的星
```

## 认识RNN模型
### 1 什么是RNN模型

- RNN(Recurrent Neural Network), 中文称作循环神经网络, 它一般以序列数据为输入, 通过网络内部的结构设计有效捕捉序列之间的关系特征, 一般也是以序列形式进行输出.
- 一般单层神经网络结构:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000028.png]]

- RNN单层网络结构:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000042.gif]]

- 以时间步对RNN进行展开后的单层网络结构:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000040.gif]]

- RNN的循环机制使模型隐层上一时间步产生的结果, 能够作为当下时间步输入的一部分(当下时间步的输入除了正常的输入外还包括上一步的隐层输出)对当下时间步的输出产生影响.

### 2 RNN模型的作用

- 因为RNN结构能够很好利用序列之间的关系, 因此针对自然界具有连续性的输入序列, 如人类的语言, 语音等进行很好的处理, 广泛应用于NLP领域的各项任务, 如文本分类, 情感分析, 意图识别, 机器翻译等.
- 下面我们将以一个用户意图识别的例子进行简单的分析:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000049.gif]]

- 第一步: 用户输入了"What time is it ?", 我们首先需要对它进行基本的分词, 因为RNN是按照顺序工作的, 每次只接收一个单词进行处理.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000052.gif]]

- 第二步: 首先将单词"What"输送给RNN, 它将产生一个输出O1.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000051.gif]]

- 第三步: 继续将单词"time"输送给RNN, 但此时RNN不仅仅利用"time"来产生输出O2, 还会使用来自上一层隐层输出O1作为输入信息.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000053.gif]]

- 第四步: 重复这样的步骤, 直到处理完所有的单词.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000054.gif]]

- 第五步: 最后，将最终的隐层输出O5进行处理来解析用户意图.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000055.gif]]

### 3 RNN模型的分类

- 这里我们将从两个角度对RNN模型进行分类. 第一个角度是输入和输出的结构, 第二个角度是RNN的内部构造.
- 按照输入和输出的结构进行分类:
  - N vs N - RNN
  - N vs 1 - RNN
  - 1 vs N - RNN
  - N vs M - RNN
- 按照RNN的内部构造进行分类:
  - 传统RNN
  - LSTM
  - Bi-LSTM
  - GRU
  - Bi-GRU
- N vs N - RNN:
  - 它是RNN最基础的结构形式, 最大的特点就是: 输入和输出序列是等长的. 由于这个限制的存在, 使其适用范围比较小, 可用于生成等长度的合辙诗句.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000029.png]]

- N vs 1 - RNN:
  - 有时候我们要处理的问题输入是一个序列，而要求输出是一个单独的值而不是序列，应该怎样建模呢？我们只要在最后一个隐层输出h上进行线性变换就可以了，大部分情况下，为了更好的明确结果, 还要使用sigmoid或者softmax进行处理. 这种结构经常被应用在文本分类问题上.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000030.png]]

- 1 vs N - RNN:
  - 如果输入不是序列而输出为序列的情况怎么处理呢？我们最常采用的一种方式就是使该输入作用于每次的输出之上. 这种结构可用于将图片生成文字任务等.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000031.png]]

- N vs M - RNN:
  - 这是一种不限输入输出长度的RNN结构, 它由编码器和解码器两部分组成, 两者的内部结构都是某类RNN, 它也被称为seq2seq架构. 输入数据首先通过编码器, 最终输出一个隐含变量c, 之后最常用的做法是使用这个隐含变量c作用在解码器进行解码的每一步上, 以保证输入信息被有效利用.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000041.png]]

- seq2seq架构最早被提出应用于机器翻译, 因为其输入输出不受限制，如今也是应用最广的RNN模型结构. 在机器翻译, 阅读理解, 文本摘要等众多领域都进行了非常多的应用实践.
- 关于RNN的内部构造进行分类的内容我们将在后面使用单独的小节详细讲解.

## 传统RNN模型
### 1 传统RNN的内部结构图
#### 1.1 RNN结构分析

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000032.png]]

- 结构解释图:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000033.png]]

- 内部结构分析:
  - 我们把目光集中在中间的方块部分, 它的输入有两部分, 分别是h(t-1)以及x(t), 代表上一时间步的隐层输出, 以及此时间步的输入, 它们进入RNN结构体后, 会"融合"到一起, 这种融合我们根据结构解释可知, 是将二者进行拼接, 形成新的张量[x(t), h(t-1)], 之后这个新的张量将通过一个全连接层(线性层), 该层使用tanh作为激活函数, 最终得到该时间步的输出h(t), 它将作为下一个时间步的输入和x(t+1)一起进入结构体. 以此类推.
- 内部结构过程演示:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000043.gif]]

- 根据结构分析得出内部计算公式: $$ h_t = tanh(W_t[X_t, h_{t-1}] + b_t) $$
- 激活函数tanh的作用:
  - 用于帮助调节流经网络的值, tanh函数将值压缩在-1和1之间.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000044.gif]]

#### 1.2 使用Pytorch构建RNN模型

- 位置: 在torch.nn工具包之中, 通过torch.nn.RNN可调用
- nn.RNN使用示例1:

```text
import torch
import torch.nn as nn

def  dm_rnn_for_base():
    '''
    第一个参数：input_size(输入张量x的维度)
    第二个参数：hidden_size(隐藏层的维度， 隐藏层的神经元个数)
    第三个参数：num_layer(隐藏层的数量)
    '''
    rnn = nn.RNN(5, 6, 1) #A

    '''
    第一个参数：sequence_length(输入序列的长度)
    第二个参数：batch_size(批次的样本数量)
    第三个参数：input_size(输入张量的维度)
    '''
    input = torch.randn(1, 3, 5) #B

    '''
    第一个参数：num_layer * num_directions(层数*网络方向)
    第二个参数：batch_size(批次的样本数)
    第三个参数：hidden_size(隐藏层的维度， 隐藏层神经元的个数)
    '''
    h0 = torch.randn(1, 3, 6) #C

    # [1,3,5],[1,3,6] ---> [1,3,6],[1,3,6]
    output, hn = rnn(input, h0)

    print('output--->',output.shape, output)
    print('hn--->',hn.shape, hn)
    print('rnn模型--->', rnn)

# 程序运行效果如下：
output---> torch.Size([1, 3, 6]) tensor([[[ 0.8947, -0.6040,  0.9878, -0.1070, -0.7071, -0.1434],
         [ 0.0955, -0.8216,  0.9475, -0.7593, -0.8068, -0.5549],
         [-0.1524,  0.7519, -0.1985,  0.0937,  0.2009, -0.0244]]],
       grad_fn=<StackBackward0>)

hn---> torch.Size([1, 3, 6]) tensor([[[ 0.8947, -0.6040,  0.9878, -0.1070, -0.7071, -0.1434],
         [ 0.0955, -0.8216,  0.9475, -0.7593, -0.8068, -0.5549],
         [-0.1524,  0.7519, -0.1985,  0.0937,  0.2009, -0.0244]]],
       grad_fn=<StackBackward0>)

rnn模型---> RNN(5, 6)
```

- nn.RNN使用示例2

```text
# 输入数据长度发生变化
def  dm_rnn_for_sequencelen():
    '''
    第一个参数：input_size(输入张量x的维度)
    第二个参数：hidden_size(隐藏层的维度， 隐藏层的神经元个数)
    第三个参数：num_layer(隐藏层的数量)
    '''
    rnn = nn.RNN(5, 6, 1) #A
    '''
    第一个参数：sequence_length(输入序列的长度)
    第二个参数：batch_size(批次的样本数量)
    第三个参数：input_size(输入张量的维度)
    '''
    input = torch.randn(20, 3, 5) #B
    '''
    第一个参数：num_layer * num_directions(层数*网络方向)
    第二个参数：batch_size(批次的样本数)
    第三个参数：hidden_size(隐藏层的维度， 隐藏层神经元的个数)
    '''
    h0 = torch.randn(1, 3, 6) #C

    # [20,3,5],[1,3,6] --->[20,3,6],[1,3,6]
    output, hn = rnn(input, h0)  #

    print('output--->', output.shape)
    print('hn--->', hn.shape)
    print('rnn模型--->', rnn)

# 程序运行效果如下：
output---> torch.Size([20, 3, 6])
hn---> torch.Size([1, 3, 6])
rnn模型---> RNN(5, 6)
```

- nn.RNN使用示例3

```text
def dm_run_for_hiddennum():
    '''
    第一个参数：input_size(输入张量x的维度)
    第二个参数：hidden_size(隐藏层的维度， 隐藏层的神经元个数)
    第三个参数：num_layer(隐藏层的数量)
    '''
    rnn = nn.RNN(5, 6, 2)  # A 隐藏层个数从1-->2 下面程序需要修改的地方？
    '''
    第一个参数：sequence_length(输入序列的长度)
    第二个参数：batch_size(批次的样本数量)
    第三个参数：input_size(输入张量的维度)
    '''
    input = torch.randn(1, 3, 5)  # B
    '''
    第一个参数：num_layer * num_directions(层数*网络方向)
    第二个参数：batch_size(批次的样本数)
    第三个参数：hidden_size(隐藏层的维度， 隐藏层神经元的个数)
    '''
    h0 = torch.randn(2, 3, 6)  # C

    output, hn = rnn(input, h0)  #
    print('output-->', output.shape, output)
    print('hn-->', hn.shape, hn)
    print('rnn模型--->', rnn)  # nn模型---> RNN(5, 6, num_layers=11)

    # 结论：若只有一个隐藏次 output输出结果等于hn
    # 结论：如果有2个隐藏层，output的输出结果有2个，hn等于最后一个隐藏层

# 程序运行效果如下：
output--> torch.Size([1, 3, 6]) tensor([[[ 0.4987, -0.5756,  0.1934,  0.7284,  0.4478, -0.1244],
         [ 0.6753,  0.5011, -0.7141,  0.4480,  0.7186,  0.5437],
         [ 0.6260,  0.7600, -0.7384, -0.5080,  0.9054,  0.6011]]],
       grad_fn=<StackBackward0>)
hn--> torch.Size([2, 3, 6]) tensor([[[ 0.4862,  0.6872, -0.0437, -0.7826, -0.7136, -0.5715],
         [ 0.8942,  0.4524, -0.1695, -0.5536, -0.4367, -0.3353],
         [ 0.5592,  0.0444, -0.8384, -0.5193,  0.7049, -0.0453]],

        [[ 0.4987, -0.5756,  0.1934,  0.7284,  0.4478, -0.1244],
         [ 0.6753,  0.5011, -0.7141,  0.4480,  0.7186,  0.5437],
         [ 0.6260,  0.7600, -0.7384, -0.5080,  0.9054,  0.6011]]],
       grad_fn=<StackBackward0>)
rnn模型---> RNN(5, 6, num_layers=2)
```

#### 1.3 传统RNN优缺点
##### 1 传统RNN的优势

- 由于内部结构简单, 对计算资源要求低, 相比之后我们要学习的RNN变体:LSTM和GRU模型参数总量少了很多, 在短序列任务上性能和效果都表现优异.

##### 2 传统RNN的缺点

- 传统RNN在解决长序列之间的关联时, 通过实践，证明经典RNN表现很差, 原因是在进行反向传播的时候, 过长的序列导致梯度的计算异常, 发生梯度消失或爆炸.

##### 3 梯度消失或爆炸介绍

根据反向传播算法和链式法则, 梯度的计算可以简化为以下公式

$$D_n=\sigma^{\prime}(z_1)w_1\cdot\sigma^{\prime}(z_2)w_2\cdot_{\cdots}\cdot\sigma^{\prime}(z_n)w_n$$

- 其中sigmoid的导数值域是固定的, 在[0, 0.25]之间, 而一旦公式中的w也小于1, 那么通过这样的公式连乘后, 最终的梯度就会变得非常非常小, 这种现象称作梯度消失. 反之, 如果我们人为的增大w的值, 使其大于1, 那么连乘够就可能造成梯度过大, 称作梯度爆炸.
- 梯度消失或爆炸的危害:
  - 如果在训练过程中发生了梯度消失，权重无法被更新，最终导致训练失败; 梯度爆炸所带来的梯度过大，大幅度更新网络参数，在极端情况下，结果会溢出（NaN值）.

## LSTM模型
> [!tip] 大白话理解（Plain-language Intuition）
> LSTM 给这张便签增加了受控的擦除、写入和读取开关。门控不是魔法记忆，而是让梯度和信息有一条更稳定的通道，因此比普通 RNN 更能处理长依赖。
### 1 LSTM介绍

LSTM（Long Short-Term Memory）也称长短时记忆结构, 它是传统RNN的变体, 与经典RNN相比能够有效捕捉长序列之间的语义关联, 缓解梯度消失或爆炸现象. 同时LSTM的结构更复杂, 它的核心结构可以分为四个部分去解析:

- 遗忘门
- 输入门
- 细胞状态
- 输出门

### 2 LSTM的内部结构图
#### 2.1 LSTM结构分析

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000034.png]]

- 结构解释图:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000033.png]]

- 遗忘门部分结构图与计算公式:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000035.png]]

- 遗忘门结构分析:
  - 与传统RNN的内部结构计算非常相似, 首先将当前时间步输入x(t)与上一个时间步隐含状态h(t-1)拼接, 得到[x(t), h(t-1)], 然后通过一个全连接层做变换, 最后通过sigmoid函数进行激活得到f(t), 我们可以将f(t)看作是门值, 好比一扇门开合的大小程度, 门值都将作用在通过该扇门的张量, 遗忘门门值将作用的上一层的细胞状态上, 代表遗忘过去的多少信息, 又因为遗忘门门值是由x(t), h(t-1)计算得来的, 因此整个公式意味着根据当前时间步输入和上一个时间步隐含状态h(t-1)来决定遗忘多少上一层的细胞状态所携带的过往信息.
- 遗忘门内部结构过程演示:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000045.gif]]

- 激活函数sigmiod的作用:
  - 用于帮助调节流经网络的值, sigmoid函数将值压缩在0和1之间.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000046.gif]]

- 输入门部分结构图与计算公式:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000036.png]]

- 输入门结构分析:
  - 我们看到输入门的计算公式有两个, 第一个就是产生输入门门值的公式, 它和遗忘门公式几乎相同, 区别只是在于它们之后要作用的目标上. 这个公式意味着输入信息有多少需要进行过滤. 输入门的第二个公式是与传统RNN的内部结构计算相同. 对于LSTM来讲, 它得到的是当前的细胞状态, 而不是像经典RNN一样得到的是隐含状态.
- 输入门内部结构过程演示:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000047.gif]]

- 细胞状态更新图与计算公式:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000037.png]]

- 细胞状态更新分析:
  - 细胞更新的结构与计算公式非常容易理解, 这里没有全连接层, 只是将刚刚得到的遗忘门门值与上一个时间步得到的C(t-1)相乘, 再加上输入门门值与当前时间步得到的未更新C(t)相乘的结果. 最终得到更新后的C(t)作为下一个时间步输入的一部分. 整个细胞状态更新过程就是对遗忘门和输入门的应用.
- 细胞状态更新过程演示:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000048.gif]]

- 输出门部分结构图与计算公式:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000038.png]]

- 输出门结构分析:
  - 输出门部分的公式也是两个, 第一个即是计算输出门的门值, 它和遗忘门，输入门计算方式相同. 第二个即是使用这个门值产生隐含状态h(t), 他将作用在更新后的细胞状态C(t)上, 并做tanh激活, 最终得到h(t)作为下一时间步输入的一部分. 整个输出门的过程, 就是为了产生隐含状态h(t).
- 输出门内部结构过程演示:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000050.gif]]

#### 2.2 Bi-LSTM介绍

Bi-LSTM即双向LSTM, 它没有改变LSTM本身任何的内部结构, 只是将LSTM应用两次且方向不同, 再将两次得到的LSTM结果进行拼接作为最终输出.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000039.png]]

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000039.png]]

- Bi-LSTM结构分析:
  - 我们看到图中对"我爱中国"这句话或者叫这个输入序列, 进行了从左到右和从右到左两次LSTM处理, 将得到的结果张量进行了拼接作为最终输出. 这种结构能够捕捉语言语法中一些特定的前置或后置特征, 增强语义关联,但是模型参数和计算复杂度也随之增加了一倍, 一般需要对语料和计算资源进行评估后决定是否使用该结构.

#### 2.3 使用Pytorch构建LSTM模型

- 位置: 在torch.nn工具包之中, 通过torch.nn.LSTM可调用.
- nn.LSTM类初始化主要参数解释:
  - input_size: 输入张量x中特征维度的大小.
  - hidden_size: 隐层张量h中特征维度的大小.
  - num_layers: 隐含层的数量.
  - bidirectional: 是否选择使用双向LSTM, 如果为True, 则使用; 默认不使用.
- nn.LSTM类实例化对象主要参数解释:
  - input: 输入张量x.
  - h0: 初始化的隐层张量h.
  - c0: 初始化的细胞状态张量c.
- nn.LSTM使用示例:

```text
# 定义LSTM的参数含义: (input_size, hidden_size, num_layers)
# 定义输入张量的参数含义: (sequence_length, batch_size, input_size)
# 定义隐藏层初始张量和细胞初始状态张量的参数含义:
# (num_layers * num_directions, batch_size, hidden_size)

>>> import torch.nn as nn
>>> import torch
>>> rnn = nn.LSTM(5, 6, 2)
>>> input = torch.randn(1, 3, 5)
>>> h0 = torch.randn(2, 3, 6)
>>> c0 = torch.randn(2, 3, 6)
>>> output, (hn, cn) = rnn(input, (h0, c0))
>>> output
tensor([[[ 0.0447, -0.0335,  0.1454,  0.0438,  0.0865,  0.0416],
         [ 0.0105,  0.1923,  0.5507, -0.1742,  0.1569, -0.0548],
         [-0.1186,  0.1835, -0.0022, -0.1388, -0.0877, -0.4007]]],
       grad_fn=<StackBackward>)
>>> hn
tensor([[[ 0.4647, -0.2364,  0.0645, -0.3996, -0.0500, -0.0152],
         [ 0.3852,  0.0704,  0.2103, -0.2524,  0.0243,  0.0477],
         [ 0.2571,  0.0608,  0.2322,  0.1815, -0.0513, -0.0291]],

        [[ 0.0447, -0.0335,  0.1454,  0.0438,  0.0865,  0.0416],
         [ 0.0105,  0.1923,  0.5507, -0.1742,  0.1569, -0.0548],
         [-0.1186,  0.1835, -0.0022, -0.1388, -0.0877, -0.4007]]],
       grad_fn=<StackBackward>)
>>> cn
tensor([[[ 0.8083, -0.5500,  0.1009, -0.5806, -0.0668, -0.1161],
         [ 0.7438,  0.0957,  0.5509, -0.7725,  0.0824,  0.0626],
         [ 0.3131,  0.0920,  0.8359,  0.9187, -0.4826, -0.0717]],

        [[ 0.1240, -0.0526,  0.3035,  0.1099,  0.5915,  0.0828],
         [ 0.0203,  0.8367,  0.9832, -0.4454,  0.3917, -0.1983],
         [-0.2976,  0.7764, -0.0074, -0.1965, -0.1343, -0.6683]]],
       grad_fn=<StackBackward>)
```

#### 2.4 LSTM优缺点

- LSTM优势: LSTM的门结构能够有效减缓长序列问题中可能出现的梯度消失或爆炸, 虽然并不能杜绝这种现象, 但在更长的序列问题上表现优于传统RNN.
- LSTM缺点: 由于内部结构相对较复杂, 因此训练效率在同等算力下较传统RNN低很多.

## GRU模型
> [!tip] 大白话理解（Plain-language Intuition）
> GRU 把 LSTM 的若干开关合并成更简洁的更新规则：参数更少、计算更轻，但仍能决定旧信息保留多少、新信息写入多少。
### 1 GRU介绍

GRU（Gated Recurrent Unit）也称门控循环单元结构, 它也是传统RNN的变体, 同LSTM一样能够有效捕捉长序列之间的语义关联, 缓解梯度消失或爆炸现象. 同时它的结构和计算要比LSTM更简单, 它的核心结构可以分为两个部分去解析:

- 更新门
- 重置门

### 2 GRU的内部结构图
#### 2.1 GRU结构分析

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000056.png]]

- 结构解释图:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000033.png]]

- GRU的更新门和重置门结构图:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）/01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）-20260813120000057.png]]

- 内部结构分析:
  - 和之前分析过的LSTM中的门控一样, 首先计算更新门和重置门的门值, 分别是z(t)和r(t), 计算方法就是使用X(t)与h(t-1)拼接进行线性变换, 再经过sigmoid激活. 之后重置门门值作用在了h(t-1)上, 代表控制上一时间步传来的信息有多少可以被利用. 接着就是使用这个重置后的h(t-1)进行基本的RNN计算, 即与x(t)拼接进行线性变化, 经过tanh激活, 得到新的h(t). 最后更新门的门值会作用在新的h(t)，而1-门值会作用在h(t-1)上, 随后将两者的结果相加, 得到最终的隐含状态输出h(t), 这个过程意味着更新门有能力保留之前的结果, 当门值趋于1时, 输出就是新的h(t), 而当门值趋于0时, 输出就是上一时间步的h(t-1).

#### 2.2 Bi-GRU介绍

Bi-GRU与Bi-LSTM的逻辑相同, 都是不改变其内部结构, 而是将模型应用两次且方向不同, 再将两次得到的LSTM结果进行拼接作为最终输出. 具体参见上小节中的Bi-LSTM.

#### 2.3 使用Pytorch构建GRU模型

- 位置: 在torch.nn工具包之中, 通过torch.nn.GRU可调用.
- nn.GRU类初始化主要参数解释:
  - input_size: 输入张量x中特征维度的大小.
  - hidden_size: 隐层张量h中特征维度的大小.
  - num_layers: 隐含层的数量.
    - bidirectional: 是否选择使用双向LSTM, 如果为True, 则使用; 默认不使用.
- nn.GRU类实例化对象主要参数解释:
  - input: 输入张量x.
    - h0: 初始化的隐层张量h.
- nn.GRU使用示例:

```text
>>> import torch
>>> import torch.nn as nn
>>> rnn = nn.GRU(5, 6, 2)
>>> input = torch.randn(1, 3, 5)
>>> h0 = torch.randn(2, 3, 6)
>>> output, hn = rnn(input, h0)
>>> output
tensor([[[-0.2097, -2.2225,  0.6204, -0.1745, -0.1749, -0.0460],
         [-0.3820,  0.0465, -0.4798,  0.6837, -0.7894,  0.5173],
         [-0.0184, -0.2758,  1.2482,  0.5514, -0.9165, -0.6667]]],
       grad_fn=<StackBackward>)
>>> hn
tensor([[[ 0.6578, -0.4226, -0.2129, -0.3785,  0.5070,  0.4338],
         [-0.5072,  0.5948,  0.8083,  0.4618,  0.1629, -0.1591],
         [ 0.2430, -0.4981,  0.3846, -0.4252,  0.7191,  0.5420]],

        [[-0.2097, -2.2225,  0.6204, -0.1745, -0.1749, -0.0460],
         [-0.3820,  0.0465, -0.4798,  0.6837, -0.7894,  0.5173],
         [-0.0184, -0.2758,  1.2482,  0.5514, -0.9165, -0.6667]]],
       grad_fn=<StackBackward>)
```

#### 2.4 GRU优缺点

- GRU的优势:
  - GRU和LSTM作用相同, 在捕捉长序列语义关联时, 能有效抑制梯度消失或爆炸, 效果都优于传统RNN且计算复杂度相比LSTM要小.
- GRU的缺点:
  - GRU仍然不能完全解决梯度消失问题, 同时其作用RNN的变体, 有着RNN结构本身的一大弊端, 即不可并行计算, 这在数据量和模型体量逐步增大的未来, 是RNN发展的关键瓶颈.
