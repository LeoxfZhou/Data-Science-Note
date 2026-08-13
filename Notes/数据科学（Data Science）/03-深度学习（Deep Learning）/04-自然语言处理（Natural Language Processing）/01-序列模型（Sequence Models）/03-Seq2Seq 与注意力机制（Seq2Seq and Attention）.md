---
title: "Seq2Seq、编码器-解码器与注意力机制（Seq2Seq, Encoder-Decoder, and Attention）"
tags:
  - data-science/nlp
status: published
created: 2026-08-13
published_at: 2026-08-13
---
# Seq2Seq、编码器-解码器与注意力机制（Seq2Seq, Encoder-Decoder, and Attention）

## 注意力机制（Attention Mechanism）介绍1
> [!tip] 大白话理解（Plain-language Intuition）
> 注意力机制像读长文时移动聚光灯：生成当前结果时，不平均依赖所有输入，而是根据当前查询把更高权重放到更相关的位置。权重表示当前计算中的相关程度，不等同于严格因果解释。
### 1. 注意力机制（Attention Mechanism）的由来，解决了什么问题？

- 在认识注意力之前，我们先简单了解下机器翻译任务：

> 例子：seq2seq(Sequence to Sequence))架构翻译任务

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000067.png]]

- seq2seq模型架构包括三部分，分别是encoder(编码器)、decoder(解码器)、中间语义张量c。
- 图中表示的是一个中文到英文的翻译：欢迎 来 北京 → welcome to BeiJing。编码器首先处理中文输入"欢迎 来 北京"，通过GRU模型获得每个时间步的输出张量，最后将它们拼接成一个中间语义张量c；接着解码器将使用这个中间语义张量c以及每一个时间步的隐层张量, 逐个生成对应的翻译语言
- 早期在解决机器翻译这一类seq2seq问题时，通常采用的做法是利用一个编码器(Encoder)和一个解码器(Decoder)构建端到端的神经网络模型，但是基于编码解码的神经网络存在两个问题：
- 问题1：如果翻译的句子很长很复杂，比如直接一篇文章输进去，模型的计算量很大，并且模型的准确率下降严重。
- 问题2：在翻译时，可能在不同的语境下，同一个词具有不同的含义，但是网络对这些词向量并没有区分度，没有考虑词与词之间的相关性，导致翻译效果比较差。
- 针对这样的问题，注意力机制被提出。

---

### 2. 什么是注意力机制（Attention Mechanism）

- 注意力机制早在上世纪九十年代就有研究，最早注意力机制应用在视觉领域，后来伴随着2017年Transformer模型结构的提出，注意力机制在NLP,CV相关问题的模型网络设计上被广泛应用。“注意力机制”实际上就是想将人的感知方式、注意力的行为应用在机器上，让机器学会去感知数据中的重要和不重要的部分。
- 举例说明：当我们看到下面这张图时，短时间内大脑可能只对图片中的“锦江饭店”有印象，即注意力集中在了“锦江饭店”处。短时间内，大脑可能并没有注意到锦江饭店上面有一串电话号码，下面有几个行人，后面还有“喜运来大酒家”等信息。

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000068.png]]

- 所以，大脑在短时间内处理信息时，主要将图片中最吸引人注意力的部分读出来了，大脑注意力只关注吸引人的部分, 类似下图所示.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000069.png]]

- 同样的如果我们在机器翻译中，我们要让机器注意到每个词向量之间的相关性，有侧重地进行翻译，模拟人类理解的过程。

---

### 3. 注意力机制（Attention Mechanism）分类以及如何实现

- 通俗来讲就是对于模型的每一个输入项，可能是图片中的不同部分，或者是语句中的某个单词分配一个权重，这个权重的大小就代表了我们希望模型对该部分一个关注程度。这样一来，通过权重大小来模拟人在处理信息的注意力的侧重，有效的提高了模型的性能，并且一定程度上降低了计算量。
- 深度学习中的注意力机制通常可分为三类: 软注意（全局注意）、硬注意（局部注意）和自注意（内注意）
- 软注意机制(Soft/Global Attention: 对每个输入项的分配的权重为0-1之间，也就是某些部分关注的多一点，某些部分关注的少一点，因为对大部分信息都有考虑，但考虑程度不一样，所以相对来说计算量比较大。
- 硬注意机制(Hard/Local Attention,[了解即可]): 对每个输入项分配的权重非0即1，和软注意不同，硬注意机制只考虑那部分需要关注，哪部分不关注，也就是直接舍弃掉一些不相关项。优势在于可以减少一定的时间和计算成本，但有可能丢失掉一些本应该注意的信息。
- 自注意力机制( Self/Intra Attention): 对每个输入项分配的权重取决于输入项之间的相互作用，即通过输入项内部的"表决"来决定应该关注哪些输入项。和前两种相比，在处理很长的输入时，具有并行计算的优势。

---

#### 3.1 Soft Attention (最常见)

- 需要注意：注意力机制是一种通用的思想和技术，不依赖于任何模型，换句话说，注意力机制可以用于任何模型。我们这里只是以文本处理领域的Encoder-Decoder框架为例进行理解。这里我们分别以普通Encoder-Decoder框架以及加Attention的Encoder-Decoder框架分别做对比。

---

##### 3.1.1 普通Encoder-Decoder框架

- 下图1是Encoder-Decoder框架的一种抽象表示方式：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000070.png]]

- 上图图例可以把它看作由一个句子（或篇章）生成另外一个句子（或篇章）的通用处理模型。对于句子对 ，我们的目标是给定输入句子Source，期待通过Encoder-Decoder框架来生成目标句子Target。Source和Target可以是同一种语言，也可以是两种不同的语言。而Source和Target分别由各自的单词序列构成： $$ Source = \langle X_1,X_2 \cdots X_m \rangle \\ Target = \langle y_1,y_2 \cdots y_n \rangle $$
- encoder顾名思义就是对输入句子Source进行编码，将输入句子通过非线性变换转化为中间语义表示C： $$ C = F(X_1,X_2 \cdots X_m) $$
- 对于解码器Decoder来说，其任务是根据句子Source的中间语义表示C和之前已经生成的历史信息,y_1, y_2…y_i-1来生成i时刻要生成的单词y_i $$ y_i = G(C,y_1,y_2 \cdots y_{i-1}) $$
- 上述图中展示的Encoder-Decoder框架是没有体现出“注意力模型”的，所以可以把它看作是注意力不集中的分心模型。为什么说它注意力不集中呢？请观察下目标句子Target中每个单词的生成过程如下： $$ y_1 = f(C) \\ y_2 = f(C, y_1) \\ y_3 = f(C, y_1, y_2) $$
- 其中f是Decoder的非线性变换函数。从这里可以看出，在生成目标句子的单词时，不论生成哪个单词，它们使用的输入句子Source的语义编码C都是一样的，没有任何区别。而语义编码C又是通过对source经过Encoder编码产生的，因此对于target中的任何一个单词，source中任意单词对某个目标单词y_i来说影响力都是相同的，这就是为什么说图1中的模型没有体现注意力的原因。

---

##### 3.1.2 加Attention的Encoder-Decoder框架

- 举例说明，为何添加Attention:
- 比如机器翻译任务，输入source为：Tom chase Jerry，输出target为：“汤姆”，“追逐”，“杰瑞”。在翻译“Jerry”这个中文单词的时候，普通Encoder-Decoder框架中，source里的每个单词对翻译目标单词“杰瑞”贡献是相同的，很明显这里不太合理，显然“Jerry”对于翻译成“杰瑞”更重要。
- 如果引入Attention模型，在生成“杰瑞”的时候，应该体现出英文单词对于翻译当前中文单词不同的影响程度，比如给出类似下面一个概率分布值：（Tom,0.3）(Chase,0.2) (Jerry,0.5).每个英文单词的概率代表了翻译当前单词“杰瑞”时，注意力分配模型分配给不同英文单词的注意力大小。
- 因此，基于上述例子所示, 对于target中任意一个单词都应该有对应的source中的单词的注意力分配概率.而且，由于注意力模型的加入，原来在生成target单词时候的中间语义C就不再是固定的，而是会根据注意力概率变化的C，加入了注意力模型的Encoder-Decoder框架就变成了下图2所示：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000071.png]]

- 即生成目标句子单词的过程成了下面的形式： $$ y_1 = f1(C_1) \\ y_2 = f1(C_2, y_1) \\ y_3 = f1(C_3, y_1, y_2) $$
- 而每个Ci可能对应着不同的源语句子单词的注意力分配概率分布，比如对于上面的英汉翻译来说，其对应的信息可能如下: $$ C_{Tom}=g(0.6*f2(Tom), 0.2*f2(Chase), 0.2*f2(Jerry)) \\ C_{Chase}=g(0.2*f2(Tom), 0.7*f2(Chase), 0.1*f2(Jerry)) \\ C_{Jerry}=g(0.3*f2(Tom), 0.2*f2(Chase), 0.5*f2(Jerry)) $$
- f2函数代表Encoder对输入英文单词的某种变换函数，比如如果Encoder是用的RNN模型的话，这个f2函数的结果往往是某个时刻输入后隐层节点的状态值；g代表Encoder根据单词的中间表示合成整个句子中间语义表示的变换函数，一般的做法中，g函数就是对构成元素加权求和，即下列公式

$$C_i = \sum_{j=1}^{L_x}a_{ij}h_j$$

- Lx代表输入句子source的长度, a_ij代表在Target输出第i个单词时source输入句子中的第j个单词的注意力分配系数, 而hj则是source输入句子中第j个单词的语义编码, 假设Ci下标i就是上面例子所说的'汤姆', 那么Lx就是3, h1=f('Tom'), h2=f('Chase'),h3=f('jerry')分别输入句子每个单词的语义编码, 对应的注意力模型权值则分别是0.6, 0.2, 0.2, 所以g函数本质上就是加权求和函数, 如果形象表示的话, 翻译中文单词'汤姆'的时候, 数学公式对应的中间语义表示Ci的形成过程类似下图3:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000072.png]]

---

##### 3.1.3 如何得到注意力概率分布

- 为了便于说明，我们假设Encoder-Decoder框架中，Encoder和Decoder都采用RNN模型，如下图4所示：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000073.png]]

- 那么注意力分配概率分布值的通用计算过程如下：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000074.png]]

- 上图中h_i表示Source中单词j对应的隐层节点状态h_j，H_i表示Target中单词i的隐层节点状态，注意力计算的是Target中单词i对Source中每个单词对齐可能性，即F(h_j,H_i-1)，而函数F可以用不同的方法，然后函数F的输出经过softmax进行归一化就得到了注意力分配概率分布。
- 上面就是经典的Soft Attention模型的基本思想，区别只是函数F会有所不同。

---

##### 3.1.4 Attention机制的本质思想

- 其实Attention机制可以看作，Target中每个单词是对Source每个单词的加权求和，而权重是Source中每个单词对Target中每个单词的重要程度。因此，Attention的本质思想会表示成下图：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000075.png]]

- 将Source中的构成元素看作是一系列的 数据对，给定Target中的某个元素Query，通过计算Query和各个Key的相似性或者相关性，即权重系数；然后对Value进行加权求和，并得到最终的Attention数值。将本质思想表示成公式如下：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000076.png]]

- 深度学习中的注意力机制中提到：Source 中的 Key 和 Value 合二为一，指向的是同一个东西，也即输入句子中每个单词对应的语义编码，所以可能不容易看出这种能够体现本质思想的结构。因此，Attention计算转换为下面3个阶段。
- 输入由三部分构成：Query、Key和Value。其中，(Key, Value)是具有相互关联的KV对，Query是输入的“问题”，Attention可以将Query转化为与Query最相关的向量表示。
- Attention的计算主要分3步，如下图所示。

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000077.png]]

- Attention 3步计算过程Attention3步计算过程
- 第一步：Query和Key进行相似度计算，得到Attention Score；
- 第二步：对Attention Score进行Softmax归一化，得到权值矩阵；
- 第三步：权重矩阵与Value进行加权求和计算。
- Query、Key和Value的含义是什么呢？我们以刚才大脑读图为例。Value可以理解为人眼视网膜对整张图片信息的原始捕捉，不受“注意力”所影响。我们可以将Value理解为像素级别的信息，那么假设只要一张图片呈现在人眼面前，图片中的像素都会被视网膜捕捉到。Key与Value相关联，Key是图片原始信息所对应的关键性提示信息，比如“锦江饭店”部分是将图片中的原始像素信息抽象为中文文字和牌匾的提示信息。一个中文读者看到这张图片时，读者大脑有意识地向图片获取信息，即发起了一次Query，Query中包含了读者的意图等信息。在一次读图过程中，Query与Key之间计算出Attention Score，得到最具有吸引力的部分，并只对具有吸引力的Value信息进行提取，反馈到大脑中。就像上面的例子中，经过大脑的注意力机制的筛选，一次Query后，大脑只关注“锦江饭店”的牌匾部分。
- 再以一个搜索引擎的检索为例。使用某个Query去搜索引擎里搜索，搜索引擎里面有好多文章，每个文章的全文可以被理解成Value；文章的关键性信息是标题，可以将标题认为是Key。搜索引擎用Query和那些文章们的标题（Key）进行匹配，看看相似度（计算Attention Score)。我们想得到跟Query相关的知识，于是用这些相似度将检索的文章Value做一个加权和，那么就得到了一个新的信息，新的信息融合了相关性强的文章们，而相关性弱的文章可能被过滤掉。

---

#### 3.2 Hard Attention

- 在3.1章节我们使用了一种软性注意力的方式进行Attention机制，它通过注意力分布来加权求和融合各个输入向量。而硬性注意力（Hard Attention）机制则不是采用这种方式，它是根据注意力分布选择输入向量中的一个作为输出。这里有两种选择方式：
- 选择注意力分布中，分数最大的那一项对应的输入向量作为Attention机制的输出。
- 根据注意力分布进行随机采样，采样结果作为Attention机制的输出。
- 硬性注意力通过以上两种方式选择Attention的输出，这会使得最终的损失函数与注意力分布之间的函数关系不可导，导致无法使用反向传播算法训练模型，硬性注意力通常需要使用强化学习来进行训练。因此，一般深度学习算法会使用软性注意力的方式进行计算，

---

#### 3.3 Self Attention
> [!tip] 大白话理解（Plain-language Intuition）
> 自注意力像让句子中的每个词都向其他词提问：谁与我最相关？相关性变成权重，再用这些权重汇总信息。它能一步连接远距离词，但代价是标准实现对序列长度通常需要平方级注意力矩阵。

- Self Attention是Google在transformer模型中提出的，上面介绍的都是一般情况下Attention发生在Target元素Query和Source中所有元素之间。而Self Attention，指的是Source内部元素之间或者Target内部元素之间发生的Attention机制，也可以理解为Target=Source这种特殊情况下的注意力机制。当然，具体的计算过程仍然是一样的，只是计算对象发生了变化而已。
- 上面内容也有说到，一般情况下Attention本质上是Target和Source之间的一种单词对齐机制。那么如果是Self Attention机制，到底学的是哪些规律或者抽取了哪些特征呢？或者说引入Self Attention有什么增益或者好处呢？仍然以机器翻译为例来说明, 如下图所示：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000078.png]]

- Attention的发展主要经历了两个阶段：

> - 从上图中可以看到, self Attention可以远距离的捕捉到语义层面的特征(its的指代对象是Law).
> - 应用传统的RNN, LSTM, 在获取长距离语义特征和结构特征的时候, 需要按照序列顺序依次计算, 距离越远的联系信息的损耗越大, 有效提取和捕获的可能性越小.
> - 但是应用self-attention时, 计算过程中会直接将句子中任意两个token的联系通过一个计算步骤直接联系起来

---

## 注意力机制（Attention Mechanism）介绍2
### 1 注意力机制（Attention Mechanism）规则

- 它需要三个指定的输入Q(query), K(key), V(value), 然后通过计算公式得到注意力的结果, 这个结果代表query在key和value作用下的注意力表示. 当输入的Q=K=V时, 称作自注意力计算规则；当Q、K、V不相等时称为一般注意力计算规则

> 例子：seq2seq架构翻译应用中的Q、K、V解释

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000067.png]]

- seq2seq模型架构包括三部分，分别是encoder(编码器)、decoder(解码器)、中间语义张量c。
- 图中表示的是一个中文到英文的翻译：欢迎 来 北京 → welcome to BeiJing。编码器首先处理中文输入"欢迎 来 北京"，通过GRU模型获得每个时间步的输出张量，最后将它们拼接成一个中间语义张量c；接着解码器将使用这个中间语义张量c以及每一个时间步的隐层张量, 逐个生成对应的翻译语言.
- 在上述机器翻译架构中加入Attention的方式有两种：
- 第一种tensorflow版本(传统方式)，如下图所示：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000079.png]]

> 上图翻译应用中的Q、K、V解释
>
> - 查询张量Q: 解码器每一步输出或者是当前输入的x
> - 键张量K: 编码部分每个时间步的结果组合而成
> - 值张量V:编码部分每个时间步的结果组合而成

- 第二种Pytorch版本(改进版)，如下图所示：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000080.png]]

> 上图翻译应用中的Q、K、V解释
>
> - 查询张量Q: 解码器每一步的输出或者是当前输入的x
> - 键张量K: 解码器上一步的隐藏层输出
> - 值张量V:编码部分每个时间步输出结果组合而成

- 两个版本对比：
- pytorch版本的是乘型attention，tensorflow版本的是加型attention。pytorch这里直接将与上一个unit隐状态prev_hidden拼接起来✖W得到score，之后将score过softmax得到attenion_weights.
- 解码过程如下：
- （1）采用自回归机制，比如：输入“go”来预测“welcome”，输入“welcome”来预测"to",输入“to”来预测“Beijing”。在输入“welcome”来预测"to"解码中，可使用注意力机制
- （2）查询张量Q：一般可以是“welcome”词嵌入层以后的结果，查询张量Q为生成谁就是谁的查询张量（比如这里为了生成“to”，则查询张量就是“to”的查询张量，请仔细体会这一点）
- （3） 键向量K：一般可以是上一个时间步的隐藏层输出
- （4）值向量V：一般可以是编码部分每个时间步的结果组合而成
- （5）查询张量Q来生成“to”，去检索“to”单词和“欢迎”、“来”、“北京”三个单词的权重分布，注意力结果表示（用权重分布 乘以内容V）

#### 1.3 常见的注意力计算规则

- 将Q，K进行纵轴拼接, 做一次线性变化, 再使用softmax处理获得结果最后与V做张量乘法. $$ Attention(Q,K,V)=Softmax(Linear([Q,K]))\cdot V $$
- 将Q，K进行纵轴拼接, 做一次线性变化后再使用tanh函数激活, 然后再进行内部求和, 最后使用softmax处理获得结果再与V做张量乘法. $$ Attention(Q,K,V)=Softmax(sum(tanh(Linear([Q,K]))))\cdot V $$
- 将Q与K的转置做点积运算, 然后除以一个缩放系数, 再使用softmax处理获得结果最后与V做张量乘法. $$ Attention(Q,K,V)=Softmax(\frac{Q\cdot K^T}{\sqrt{d_{k}}})\cdot V $$
- 说明：当注意力权重矩阵和V都是三维张量且第一维代表为batch条数时, 则做bmm运算.bmm是一种特殊的张量乘法运算.
- bmm运算演示:

```text
# 如果参数1形状是(b × n × m), 参数2形状是(b × m × p), 则输出为(b × n × p)
>>> input = torch.randn(10, 3, 4)
>>> mat2 = torch.randn(10, 4, 5)
>>> res = torch.bmm(input, mat2)
>>> res.size()
torch.Size([10, 3, 5])
```

### 2 什么是深度神经网络注意力机制（Attention Mechanism）

- 注意力机制是注意力计算规则能够应用的深度学习网络的载体, 同时包括一些必要的全连接层以及相关张量处理, 使其与应用网络融为一体. 使用自注意力计算规则的注意力机制称为自注意力机制.
- 说明: NLP领域中, 当前的注意力机制大多数应用于seq2seq架构, 即编码器和解码器模型.
- 请思考：为什么要在深度神经网络中引入注意力机制？
  - 1、rnn等循环神经网络，随着时间步的增长，前面单词的特征会遗忘，造成对句子特征提取不充分
  - 2、rnn等循环神经网络是一个时间步一个时间步的提取序列特征，效率低下
  - 3、研究者开始思考，能不能对32个单词（序列）同时提取事物特征，而且还是并行的，所以引入注意力机制！

### 3 注意力机制（Attention Mechanism）的作用

- 在解码器端的注意力机制: 能够根据模型目标有效的聚焦编码器的输出结果, 当其作为解码器的输入时提升效果. 改善以往编码器输出是单一定长张量, 无法存储过多信息的情况.
- 在编码器端的注意力机制: 主要解决表征问题, 相当于特征提取过程, 得到输入的注意力表示. 一般使用自注意力(self-attention).

注意力机制在网络中实现的图形表示:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000061.png]]

### 4 注意力机制（Attention Mechanism）实现步骤
#### 4.1 步骤

- 第一步: 根据注意力计算规则, 对Q，K，V进行相应的计算.
- 第二步: 根据第一步采用的计算方法, 如果是拼接方法，则需要将Q与第二步的计算结果再进行拼接, 如果是转置点积, 一般是自注意力, Q与V相同, 则不需要进行与Q的拼接.
- 第三步: 最后为了使整个attention机制按照指定尺寸输出, 使用线性层作用在第二步的结果上做一个线性变换, 得到最终对Q的注意力表示.

#### 4.2 代码实现

- 常见注意力机制的代码分析:

```python
# 任务描述：
# 有QKV：v是内容比如32个单词，每个单词64个特征，k是32个单词的索引，q是查询张量
# 我们的任务：输入查询张量q，通过注意力机制来计算如下信息：
# 1、查询张量q的注意力权重分布：查询张量q和其他32个单词相关性（相识度）
# 2、查询张量q的结果表示：有一个普通的q升级成一个更强大q；用q和v做bmm运算
# 3 注意：查询张量q查询的目标是谁，就是谁的查询张量。
#   eg：比如查询张量q是来查询单词"我"，则q就是我的查询张量

import torch
import torch.nn as nn
import torch.nn.functional as F

# MyAtt类实现思路分析
# 1 init函数 (self, query_size, key_size, value_size1, value_size2, output_size)
# 准备2个线性层 注意力权重分布self.attn 注意力结果表示按照指定维度进行输出层 self.attn_combine
# 2 forward(self, Q, K, V):
# 求查询张量q的注意力权重分布, attn_weights[1,32]
# 求查询张量q的注意力结果表示 bmm运算, attn_applied[1,1,64]
# q 与 attn_applied 融合，再按照指定维度输出 output[1,1,32]
# 返回注意力结果表示output:[1,1,32], 注意力权重分布attn_weights:[1,32]

class MyAtt(nn.Module):
    #                   32          32          32              64      32
    def __init__(self, query_size, key_size, value_size1, value_size2, output_size):
        super(MyAtt, self).__init__()
        self.query_size = query_size
        self.key_size = key_size
        self.value_size1 = value_size1
        self.value_size2 = value_size2
        self.output_size = output_size

        # 线性层1 注意力权重分布
        self.attn = nn.Linear(self.query_size + self.key_size, self.value_size1)

        # 线性层2 注意力结果表示按照指定维度输出层 self.attn_combine
        self.attn_combine = nn.Linear(self.query_size+self.value_size2, output_size)

    def forward(self, Q, K, V):
        # 1 求查询张量q的注意力权重分布, attn_weights[1,32]
        # [1,1,32],[1,1,32]--> [1,32],[1,32]->[1,64]
        # [1,64] --> [1,32]
        # tmp1 = torch.cat( (Q[0], K[0]), dim=1)
        # tmp2 = self.attn(tmp1)
        # tmp3 = F.softmax(tmp2, dim=1)
        attn_weights = F.softmax( self.attn(torch.cat( (Q[0], K[0]), dim=-1)), dim=-1)

        # 2 求查询张量q的结果表示 bmm运算, attn_applied[1,1,64]
        # [1,1,32] * [1,32,64] ---> [1,1,64]
        attn_applied =  torch.bmm(attn_weights.unsqueeze(0), V)

        # 3 q 与 attn_applied 融合，再按照指定维度输出 output[1,1,64]
        # 3-1 q与结果表示拼接 [1,32],[1,64] ---> [1,96]
        output = torch.cat((Q[0], attn_applied[0]), dim=-1)
        # 3-2 shape [1,96] ---> [1,32]
        output = self.attn_combine(output).unsqueeze(0)

        # 4 返回注意力结果表示output:[1,1,32], 注意力权重分布attn_weights:[1,32]
        return output, attn_weights
```

> - 调用:

```text
if __name__ == '__main__':

    query_size = 32
    key_size = 32
    value_size1 = 32 # 32个单词
    value_size2 = 64 # 64个特征
    output_size = 32

    Q = torch.randn(1, 1, 32)
    K = torch.randn(1, 1, 32)
    V = torch.randn(1, 32, 64)
    # V = torch.randn(1, value_size1, value_size2)

    # 1 实例化注意力类 对象
    myattobj = MyAtt(query_size, key_size, value_size1, value_size2, output_size)

    # 2 把QKV数据扔给注意机制，求查询张量q的注意力结果表示、注意力权重分布
    output, attn_weights = myattobj(Q, K, V)
    print('查询张量q的注意力结果表示output--->', output.shape, output)
    print('查询张量q的注意力权重分布attn_weights--->', attn_weights.shape, attn_weights)
```

> - 输出效果:

```text
查询张量q的注意力结果表示output---> torch.Size([1, 1, 32]) tensor([[[ 0.3135, -0.0539,  0.0597, -0.0046, -0.3389, -0.1238,  1.0385,
           0.8896, -0.0268, -0.0705, -0.8409,  0.6547,  0.5909, -0.6048,
           0.6303, -0.2233,  0.7678, -0.3140,  0.3635, -0.3234, -0.1053,
           0.5845,  0.1163, -0.2203, -0.0812, -0.0868,  0.0218, -0.0597,
           0.6923, -0.1848, -0.8266, -0.0614]]], grad_fn=<UnsqueezeBackward0>)
查询张量q的注意力权重分布attn_weights---> torch.Size([1, 32]) tensor([[0.0843, 0.0174, 0.0138, 0.0431, 0.0110, 0.0308, 0.0608, 0.0216, 0.0101,
         0.0406, 0.0462, 0.0111, 0.0349, 0.0065, 0.0383, 0.0526, 0.0151, 0.0193,
         0.0294, 0.0632, 0.0322, 0.0072, 0.0294, 0.0388, 0.0135, 0.0443, 0.0594,
         0.0332, 0.0117, 0.0168, 0.0293, 0.0344]], grad_fn=<SoftmaxBackward0>)
```

- 更多有关注意力机制的应用我们将在案例中进行详尽的理解分析.

## 注意力机制（Attention Mechanism）拓展阅读
### 1 注意力机制（Attention Mechanism）原理
#### 1.1 注意力机制（Attention Mechanism）示意图

Attention机制的工作原理并不复杂，我们可以用下面这张图做一个总结

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000064.png]]

#### 1.2 Attention计算过程

- 阶段一: query 和 key 进行相似度计算，得到一个query 和 key 相关性的分值
- 阶段二: 将这个分值进行归一化(softmax)，得到一个注意力的分布
- 阶段三: 使用注意力分布和 value 进行计算，得到一个融合注意力的更好的 value 值

为了更好的说明上面的情况, 我们通过注意力来做一个机器翻译(NMT) 的任务，机器翻译中，我们会使用 seq2seq 的架构，每个时间步从词典里生成一个翻译的结果。就像下面这张图一样.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000065.png]]

在没有注意力之前，我们每次都是根据 Encoder 部分的输出结果来进行生成，提出注意力后，就是想在生成翻译结果时并不是看 Encoder 中所有的输出结果，而是先来看看想生成的这部分和哪些单词可能关系会比较大，关系大的我多借鉴些；关系小的，少借鉴些。就是这样一个想法，我们看看该如何操作。

- 这里为了生成单词，我们把 Decoder 部分输入后得到的向量作为 query；把 Encoder 部分每个单词的向量作为 key。首先我们先把 query 和 每一个单词进行点乘 $score=query\cdot key$ ，得到相关性的分值；
- 有了这些分值后，我们对这些分值做一个 $softmax$ ，得到一个注意力的分布
- 有了这个注意力，我们就可以用它和 Encoder 的输出值 (value) 进行相乘，得到一个加权求和后的值，这个值就包含注意力的表示，我们用它来预测要生成的词。

这个过程我们可以看看一个动图的事例理解一下:

#### 1.3 Attention计算逻辑

当然，Attention 并不是只有这一种计算方式，后来还有很多人找到了各种各样的计算注意力的方法, 比如我们上面介绍的三种计算规则, 但是从本质上，它们都遵循着这个三步走的逻辑:

- query 和 key 进行相似度计算，得到一个query 和 key 相关性的分值
- 将这个分值进行归一化(softmax)，得到一个注意力的分布
- 使用注意力分布和 value 进行计算，得到一个融合注意力的更好的 value 值

#### 1.4 有无attention模型对比
##### 1 无attention机制的模型

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000066.png]]

- 文本处理领域的Encoder-Decoder框架可以这么直观地去理解：可以把它看作适合处理由一个句子（或篇章）生成另外一个句子（或篇章）的通用处理模型。对于句子对 ，我们的目标是给定输入句子Source，期待通过Encoder-Decoder框架来生成目标句子Target。Source和Target可以是同一种语言，也可以是两种不同的语言。而Source和Target分别由各自的单词序列构成： $$ Source = \langle X_1,X_2 \cdots X_m \rangle \\ Target = \langle y_1,y_2 \cdots y_n \rangle $$
- encoder顾名思义就是对输入句子Source进行编码，将输入句子通过非线性变换转化为中间语义表示C： $$ C = F(X_1,X_2 \cdots X_m) $$
- 对于解码器Decoder来说，其任务是根据句子Source的中间语义表示C和之前已经生成的历史信息,y_1, y_2…y_i-1来生成i时刻要生成的单词y_i $$ y_i = G(C,y_1,y_2 \cdots y_{i-1}) $$
- 上述图中展示的Encoder-Decoder框架是没有体现出“注意力模型”的，所以可以把它看作是注意力不集中的分心模型。为什么说它注意力不集中呢？请观察下目标句子Target中每个单词的生成过程如下： $$ y_1 = f(C) \\ y_2 = f(C, y_1) \\ y_3 = f(C, y_1, y_2) $$
- 其中f是Decoder的非线性变换函数。从这里可以看出，在生成目标句子的单词时，不论生成哪个单词，它们使用的输入句子Source的语义编码C都是一样的，没有任何区别。
- 每个yi都依次这么产生，那么看起来就是整个系统根据输入句子Source生成了目标句子Target。如果Source是中文句子，Target是英文句子，那么这就是解决机器翻译问题的Encoder-Decoder框架；如果Source是一篇文章，Target是概括性的几句描述语句，那么这是文本摘要的Encoder-Decoder框架；如果Source是一句问句，Target是一句回答，那么这是问答系统或者对话机器人的Encoder-Decoder框架。由此可见，在文本处理领域，Encoder-Decoder的应用领域相当广泛。
- **问题点是** : 语义编码C是由句子Source的每个单词经过Encoder 编码产生的，这意味着不论是生成哪个单词，还是，其实句子Source中任意单词对生成某个目标单词yi来说影响力都是相同的，这是为何说这个模型没有体现出注意力的缘由。这类似于人类看到眼前的画面，但是眼中却没有注意焦点一样.

##### 2 有attention机制的模型

- 如果拿机器翻译来解释这个分心模型的Encoder-Decoder框架更好理解，比如输入的是英文句子：Tom chase Jerry，Encoder-Decoder框架逐步生成中文单词：“汤姆”，“追逐”，“杰瑞”。在翻译“杰瑞”这个中文单词的时候，分心模型里面的每个英文单词对于翻译目标单词“杰瑞”贡献是相同的，很明显这里不太合理，显然“Jerry”对于翻译成“杰瑞”更重要，但是分心模型是无法体现这一点的，这就是为何说它没有引入注意力的原因。
- 没有引入注意力的模型在输入句子比较短的时候问题不大，但是如果输入句子比较长，此时所有语义完全通过一个中间语义向量来表示，单词自身的信息已经消失，可想而知会丢失很多细节信息，这也是为何要引入注意力模型的重要原因。
- 上面的例子中，如果引入Attention模型的话，应该在翻译“杰瑞”的时候，体现出英文单词对于翻译当前中文单词不同的影响程度，比如给出类似下面一个概率分布值：（Tom,0.3）(Chase,0.2) (Jerry,0.5).每个英文单词的概率代表了翻译当前单词“杰瑞”时，注意力分配模型分配给不同英文单词的注意力大小。这对于正确翻译目标语单词肯定是有帮助的，因为引入了新的信息。
- 同理，目标句子中的每个单词都应该学会其对应的源语句子中单词的注意力分配概率信息。这意味着在生成每个单词的时候，原先都是相同的中间语义表示C会被替换成根据当前生成单词而不断变化的。理解Attention模型的关键就是这里，即由固定的中间语义表示C换成了根据当前输出单词来调整成加入注意力模型的变化的。增加了注意力模型的Encoder-Decoder框架理解起来如下图所示:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000065.png]]

- 即生成目标句子单词的过程成了下面的形式： $$ y_1 = f1(C_1) \\ y_2 = f1(C_2, y_1) \\ y_3 = f1(C_3, y_1, y_2) $$
- 而每个Ci可能对应着不同的源语句子单词的注意力分配概率分布，比如对于上面的英汉翻译来说，其对应的信息可能如下: $$ C_{Tom}=g(0.6*f2(Tom), 0.2*f2(Chase), 0.2*f2(Jerry)) \\ C_{Chase}=g(0.2*f2(Tom), 0.7*f2(Chase), 0.1*f2(Jerry)) \\ C_{Jerry}=g(0.3*f2(Tom), 0.2*f2(Chase), 0.5*f2(Jerry)) $$
- f2函数代表Encoder对输入英文单词的某种变换函数，比如如果Encoder是用的RNN模型的话，这个f2函数的结果往往是某个时刻输入后隐层节点的状态值；g代表Encoder根据单词的中间表示合成整个句子中间语义表示的变换函数，一般的做法中，g函数就是对构成元素加权求和，即下列公式 $$ C_i = \sum_{j=1}^{L_x}a_{ij}h_j $$
- Lx代表输入句子source的长度, a_ij代表在Target输出第i个单词时source输入句子中的第j个单词的注意力分配系数, 而hj则是source输入句子中第j个单词的语义编码, 假设Ci下标i就是上面例子所说的'汤姆', 那么Lx就是3, h1=f('Tom'), h2=f('Chase'),h3=f('jerry')分别输入句子每个单词的语义编码, 对应的注意力模型权值则分别是0.6, 0.2, 0.2, 所以g函数本质上就是加权求和函数, 如果形象表示的话, 翻译中文单词'汤姆'的时候, 数学公式对应的中间语义表示Ci的形成过程类似下图:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）/03-Seq2Seq 与注意力机制（Seq2Seq and Attention）-20260813120000063.png]]
