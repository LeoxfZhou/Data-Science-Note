---
title: "GPT、GPT-2 与 GPT-3 的预训练范式（GPT, GPT-2, and GPT-3 Pretraining Paradigms）"
tags:
  - data-science/nlp
status: published
created: 2026-08-13
published_at: 2026-08-13
---
# GPT、GPT-2 与 GPT-3 的预训练范式（GPT, GPT-2, and GPT-3 Pretraining Paradigms）

## GPT模型介绍
> [!tip] 大白话理解（Plain-language Intuition）
> GPT 按从左到右的顺序预测下一个 token。训练目标与实际生成过程一致，所以适合续写和生成；但当前位置不能直接看到未来 token。
### 1 GPT介绍

- GPT是OpenAI公司提出的一种语言预训练模型.
- OpenAI在论文 [<< Improving Language Understanding by Generative Pre-Training >>](https://s3-us-west-2.amazonaws.com/openai-assets/research-covers/language-unsupervised/language_understanding_paper.pdf) 中提出GPT模型.
- OpenAI后续又在论文 [<< Language Models are Unsupervised Multitask Learners >>](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) 中提出GPT2模型.
- GPT和GPT2模型结构差别不大, 但是GPT2采用了更大的数据集进行训练.
- OpenAI GPT模型是在Google BERT模型之前提出的, 与BERT最大的区别在于GPT采用了传统的语言模型方法进行预训练, 即使用单词的上文来预测单词, 而BERT是采用了双向上下文的信息共同来预测单词.
- 正是因为训练方法上的区别, 使得GPT更擅长处理自然语言生成任务(NLG), 而BERT更擅长处理自然语言理解任务(NLU).

### 2 GPT的架构

- 看三个语言模型的对比架构图, 中间的就是GPT:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000159.png]]

> - 从上图可以很清楚的看到GPT采用的是单向Transformer模型, 例如给定一个句子[u1, u2, ..., un], GPT在预测单词ui的时候只会利用[u1, u2, ..., u(i-1)]的信息, 而BERT会同时利用上下文的信息[u1, u2, ..., u(i-1), u(i+1), ..., un].
> - 作为两大模型的直接对比, BERT采用了Transformer的Encoder模块, 而GPT采用了Transformer的Decoder模块. 并且GPT的Decoder Block和经典Transformer Decoder Block还有所不同, 如下图所示:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000160.png]]

> - 如上图所示, 经典的Transformer Decoder Block包含3个子层, 分别是Masked Multi-Head Attention层, encoder-decoder attention层, 以及Feed Forward层. 但是在GPT中取消了第二个encoder-decoder attention子层, 只保留Masked Multi-Head Attention层, 和Feed Forward层.
> - 作为单向Transformer Decoder模型, GPT利用句子序列信息预测下一个单词的时候, 要使用Masked Multi-Head Attention对单词的下文进行遮掩(look ahead mask), 来防止未来信息的提前泄露. 例如给定一个句子包含4个单词[A, B, C, D], GPT需要用[A]预测B, 用[A, B]预测C, 用[A, B, C]预测D. 很显然的就是当要预测B时, 需要将[B, C, D]遮掩起来.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000161.png]]

> - 具体的遮掩操作是在slef-attention进行softmax之前进行的, 一般的实现是将MASK的位置用一个无穷小的数值-inf来替换, 替换后执行softmax计算得到新的结果矩阵. 这样-inf的位置就变成了0. 如上图所示, 最后的矩阵可以很方便的做到当利用A预测B的时候, 只能看到A的信息; 当利用[A, B]预测C的时候, 只能看到A, B的信息.
> - 注意: 对比于经典的Transformer架构, 解码器模块采用了6个Decoder Block; GPT的架构中采用了12个Decoder Block.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000162.png]]

### 3 GPT训练过程

GPT的训练也是典型的两阶段过程:

- 第一阶段: 无监督的预训练语言模型.
- 第二阶段: 有监督的下游任务fine-tunning.

#### 3.1 无监督的预训练语言模型

给定句子U = [u1, u2, ..., un], GPT训练语言模型时的目标是最大化下面的似然函数: $$ L_1(U)=\sum_i\log P(u_i|u_{i-k},\cdots,u_{i-1};\Theta) $$ 有上述公式可知, GPT是一个单向语言模型, 假设输入张量用h0表示, 则计算公式如下: $$ h_0 = UW_e + W_p $$ 其中Wp是单词的位置编码, We是单词本身的word embedding. Wp的形状是[max_seq_len, embedding_dim], We的形状是[vocab_size, embedding_dim].

得到输入张量h0后, 要将h0传入GPT的Decoder Block中, 依次得到ht: $$ h_t = transformer\_block(h_{l-1})\;\;\;\;l\in[1,t] $$ 最后通过得到的ht来预测下一个单词: $$ P(u)=softmax(h_tW_e^T) $$

#### 3.2 有监督的下游任务fine-tunning

GPT经过预训练后, 会针对具体的下游任务对模型进行微调. 微调采用的是有监督学习, 训练样本包括单词序列[x1, x2, ..., xn]和label y. GPT微调的目标任务是根据单词序列[x1, x2, ..., xn]预测标签y.

$$P(y|x^1,\cdots,x^m)=softmax(h_l^mW_y)$$

其中 $W_y$ 表示预测输出的矩阵参数, 微调任务的目标是最大化下面的函数:

$$L_2=\sum_{(x,y)}\log P(y|x^1,\cdots,x^m)$$

综合两个阶段的目标任务函数, 可知GPT的最终优化函数为:

$$L_3 = L_2 + \lambda L_1$$

## GPT2模型介绍
### 1 GPT2的架构

从模型架构上看, GPT2并没有特别新颖的架构, 它和只带有解码器模块的Transformer很像.

所谓语言模型, 作用就是根据已有句子的一部分, 来预测下一个单词会是什么. 现实应用中大家最熟悉的一个语言模型应用, 就是智能手机上的输入法, 它可以根据当前输入的内容智能推荐下一个要打的字.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000168.png]]

GPT2也是一个语言预测生成模型, 只不过比手机上应用的模型要大很多, 也更加复杂. 常见的手机端应用的输入法模型基本占用50MB空间, 而OpenAI的研究人员使用了40GB的超大数据集来训练GPT2, 训练后的GPT2模型最小的版本也要占用超过500MB空间来存储所有的参数, 至于最大版本的GPT2则需要超过6.5GB的存储空间.

自从Transformer问世以来, 很多预训练语言模型的工作都在尝试将编码器或解码器堆叠的尽可能高, 那类似的模型可以堆叠到多深呢? 事实上, 这个问题的答案也就是区别不同GPT2版本的主要因素之一. 比如最小版本的GPT2堆叠了12层, 中号的24层, 大号的36层, 超大号的堆叠了整整48层!

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000169.png]]

### 2 GPT2模型的细节

以机器人第一法则为例, 来具体看GPT2的工作细节. * 机器人第一法则: 机器人不得伤害人类, 或者目睹人类将遭受危险而袖手旁观.

#### 2.1 模型过程

首先明确一点: GPT2的工作流程很像传统语言模型, 一次只输出一个单词(token).

GPT2之所以在生成式任务中表现优秀, 是因为在每个新单词(token)产生后, 该单词就被添加在之前生成的单词序列后面, 添加后的新序列又会成为模型下一步的新输入. 这种机制就叫做自回归(auto-regression), 如下所示:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000170.png]]

其次明确一点: GPT2模型是一个只包含了Transformer Decoder模块的模型.

和BERT模型相比, GPT2的解码器在self-attention层上有一个关键的差异: 它将后面的单词(token)遮掩掉, 而BERT是按照一定规则将单词替换成[MASK].

举个例子, 如果我们重点关注4号位置的单词及其前序路径, 我们可以让模型只允许注意当前计算的单词和它之前的单词, 如下图所示:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000171.png]]

注意: 能够清楚的区分BERT使用的自注意力模块(self-attention)和GPT2使用的带掩码的自注意力模块(masked self-attention)很重要! 普通的self-attention允许模型的任意一个位置看到它右侧的信息(下图左侧), 而带掩码的self-attention则不允许这么做(下图右侧).

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000172.png]]

在Transformer原始论文发表后, 一篇名为<< Generating Wikipedia by Summarizing Long Sequences >>的论文提出用另一种Transformer模块的排列方式来进行语言建模-它直接扔掉了编码器, 只保留解码器. 这个早期的基于Transformer的模型由6个Decoder Block堆叠而成:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000173.png]]

上图中所有的解码器模块都是一样的, 因为只展开了第一个解码器的内部结构. 和GPT一样, 只保留了带掩码的self-attention子层, 和Feed Forward子层.

这些解码器和经典Transformer原始论文中的解码器模块相比, 除了删除了第二个Encoder-Decoder Attention子层外, 其他构造都一样.

#### 2.2 GPT2工作细节探究

- GPT2可以处理最长1024个单词的序列.
- 每个单词都会和它的前序路径一起"流经"所有的解码器模块.

> - 对于生成式模型来说, 基本工作方式都是提供一个预先定义好的起始token, 比如记做"s".
> - 此时模型的输入只有一个单词, 所以只有这个单词的路径是活跃的. 单词经过层层处理, 最终得到一个词向量. 该向量可以对于词汇表的每个单词计算出一个概率(GPT2的词汇表中有50000个单词). 在本例中, 我们选择概率最高的单词["The"]作为下一个单词.
> - 注意: 这种选择最高概率输出的策略有时会出现问题-如果我们持续点击输入法推荐单词的第一个, 它可能会陷入推荐同一个词的循环中, 只有你点击第二个或第三个推荐词, 才能跳出这种循环. 同理, GPT2有一个top-k参数, 模型会从概率最大的前k个单词中抽样选取下一个单词.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000174.png]]

> - 接下来, 我们将输出的单词["The"]添加在输入序列的尾部, 从而构建出新的输入序列["s", "The"], 让模型进行下一步的预测:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000175.png]]

> - 此时第二个单词的路径是当前唯一活跃的路径了. GPT2的每一层都保留了它们对第一个单词的解释, 并且将运用这些信息处理第二个单词, GPT2不会根据第二个单词重新来解释第一个单词.

- 关于输入编码: 当我们更加深入的了解模型的内部细节时, 最开始就要面对模型的输入, 和其他自然语言模型一样, GPT2同样从嵌入矩阵中查找单词对应的嵌入向量, 该矩阵(embedding matrix)也是整个模型训练结果的一部分.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000178.png]]

> - 如上图所示, 每一行都是一个词嵌入向量: 一个能够表征某个单词, 并捕获其语义的数字向量. 嵌入的维度大小和GPT2模型的大小相关, 最小的模型采用了768这个维度, 最大的采用了1600这个维度.
> - 所以在整个模型运作起来的最开始, 我们需要在嵌入矩阵中查找起始单词"s"对应的嵌入向量. 但在将其输入给模型之前, 还需要引入位置编码(positional encoding), 1024分输入序列位置中的每一个都对应了一个位置编码, 同理于词嵌入矩阵, 这些位置编码组成的矩阵也是整个模型训练结果的一部分.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000179.png]]

> - 经历前面的1, 2两步, 输入单词在进入模型第一个transformer模块前的所有处理步骤就结束了. 综上所述, GPT2模型包含两个权值矩阵: 词嵌入矩阵和位置编码矩阵. 而输入到transformer模块中的张量就是这两个矩阵对应的加和结果.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000176.png]]

- transformer模块的堆叠:
- 最底层的transformer模块处理单词的步骤:
- 首先通过自注意力层处理, 接着将其传递给前馈全连接层, 这其中包含残差连接和Layer Norm等子层操作.
- 最底层的transformer模块处理结束后, 会将结果张量传递给第二层的transformer模块, 继续进行计算.
- 每一个transformer模块的处理方式都是一样的, 不断的重复相同的模式, 但是每个模块都会维护自己的self-attention层和Feed Forward层的权重值.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000177.png]]

- GPT2的自注意力机制回顾
- 自然语言的含义是极度依赖上下文的, 比如下面所展示的"机器人第二法则":

> - 机器人必须遵守人类给它的命令, 除非该命令违背了第一法则.
> - 在上述语句中, 有三处单词具有指代含义, 除非我们知道这些词所精确指代的上下文, 否则根本不可能理解这句话的真实语义.
> - 当模型处理这句话的时候, 模型必须知道以下三点:
> - [它]指代机器人.
> - [命令]指代前半句话中人类给机器人下达的命令, 即[人类给它的命令].
> - [第一法则]指代机器人第一法则的完整内容.
> - 这就是自注意力机制所做的工作, 它在处理每个单词之前, 融入了模型对于用来解释某个单词的上下文的相关单词的理解. 具体的做法是: 给序列中的每一个单词都赋予一个相关度得分, 本质上就是注意力权重.
> - 看下图, 举个例子, 最上层的transformer模块在处理单词"it"的时候会关注"a robot", 所以"a", "robot", "it", 这三个单词与其得分相乘加权求和后的特征向量会被送入之后的Feed Forward层.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000180.png]]

> - 自注意力机制沿着序列的每一个单词的路径进行处理, 主要由3个向量组成:
> - Query(查询向量), 当前单词的查询向量被用来和其它单词的键向量相乘, 从而得到其它词相对于当前词的注意力得分.
> - Key(键向量), 键向量就像是序列中每个单词的标签, 它使我们搜索相关单词时用来匹配的对象.
> - Value(值向量), 值向量是单词真正的表征, 当我们算出注意力得分后, 使用值向量进行加权求和得到能代表当前位置上下文的向量.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000181.png]]

> - 如上图所示, 一个简单的比喻是在档案柜中找文件. 查询向量Query就像一张便利贴, 上面写着你正在研究的课题. 键向量Key像是档案柜中文件夹上贴的标签. 当你找到和便利贴上所写相匹配的文件夹时, 拿出对应的文件夹, 文件夹里的东西便是值向量Value.
> - 将单词的查询向量Query分别乘以每个文件夹的键向量Key，得到各个文件夹对应的注意力得分Score.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000182.png]]

> - 我们将每个文件夹的值向量Value乘以其对应的注意力得分Score, 然后求和, 得到最终自注意力层的输出, 如下图所示:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000183.png]]

> - 这样将值向量加权混合得到的结果也是一个向量, 它将其50%的注意力放在了单词"robot"上, 30%的注意力放在了"a"上, 还有19%的注意力放在了"it"上.

- 模型的输出:

> - 当最后一个transformer模块产生输出之后, 模型会将输出张量乘上词嵌入矩阵:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000184.png]]

> - 我们知道, 词嵌入矩阵的每一行都对应模型的词汇表中一个单词的嵌入向量. 所以这个乘法操作得到的结果就是词汇表中每个单词对应的注意力得分, 如下图所示:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000185.png]]

> - 一般来说, 我们都采用贪心算法, 选取得分最高的单词作为输出结果(top_k = 1).
> - 但是一个更好的策略是对于词汇表中得分较高的一部分单词, 将它们的得分作为概率从整个单词列表中进行抽样(得分越高的单词越容易被选中).
> - 通常会用一个折中的方法, 即选取top_k = 40, 这样模型会考虑注意力得分排名前40的单词.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000186.png]]

> - 如上图所示, 模型就完成了一个时间步的迭代, 输出了一个单词. 接下来模型会不断的迭代, 直至生成完整的序列(序列长度达到1024的上限, 或者序列的某一个时间步生成了结束符).

## GPT3模型介绍
### 1 GPT-3的介绍

GPT-3 (Generative Pre-training Transformer 3) 是由OpenAI开发的一种大型自然语言生成模型，具有非常强大的自然语言生成能力，可以生成高质量的自然语言文本。GPT-3能够执行许多自然语言处理任务，如翻译、问答、摘要生成、文本分类等。

GPT-3于2020年5月早些时候由Open AI推出，作为其先前语言模型 (LM) GPT-2 的继承者。 它被认为比GPT-2更好、更大。事实上，与他语言模型相比，OpenAI GPT-3 的完整版拥有大约 1750 亿个可训练参数，是迄今为止训练的最大模型，这份 72 页的 [研究论文](https://arxiv.org/pdf/2005.14165.pdf) 非常详细地描述了该模型的特性、功能、性能和局限性。

下图为不同模型之间训练参数的对比：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000163.png]]

### 2 GPT-3的模型细节
#### 2.1 GPT-3训练数据集

一般来说，模型的参数越多，训练模型所需的数据就越多。GPT-3共训练了5个不同的语料大约 45 TB 的文本数据，分别是低质量的Common Crawl，高质量的WebText2，Books1，Books2和Wikipedia，GPT-3根据数据集的不同的质量赋予了不同的权值，权值越高的在训练的时候越容易抽样到，如下表所示。

|**数据集**|**数量（tokens）**|**训练数据占比**|
|---|---|---|
|Common Crawl（filterd）|4100亿|60%|
|Web Text2|190亿|22%|
|BOOK1|120亿|8%|
|BOOK2|550亿|8%|
|Wikipedia|30亿|2%|

不同数据的介绍：

- Common Crawl语料库包含在 8 年的网络爬行中收集的 PB 级数据。语料库包含原始网页数据、元数据提取和带有光过滤的文本提取。
- WebText2是来自具有 3+ upvotes 的帖子的所有出站 Reddit 链接的网页文本。
- Books1和Books2是两个基于互联网的图书语料库。
- 英文维基百科页面 也是训练语料库的一部分。

#### 2.2 GPT-3模型架构

GPT-3 不是一个单一的模型，而是一个模型系列。系列中的每个模型都有不同数量的可训练参数。下表显示了每个模型、体系结构及其对应的参数：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000164.png]]

事实上，OpenAI GPT-3 系列模型与 GPT-2 模型相架构完全一致。

最大版本 GPT-3 175B 或“GPT-3”具有175个B参数、96层的多头Transformer、Head size为96、词向量维度为12288、文本长度大小为2048。

#### 2.3 GPT-3三种评估方式

任何语言模型可以执行的各种任务取决于它是如何微调/更新的。使用 GPT-3，可以完成前面讨论的许多 NLP 任务，而无需任何微调、梯度或参数更新，这使得该模型**与任务无关**。因此，OpenAI GPT-3 可以在很少或没有示例的情况下执行任务。让我们了解与模型相关的Few-shot/One-shot/Zero-shot任务概念，并通过一些示例了解如何与模型进行交互。

Few-shot、One-shot、Zero-shot Learning策略主要是用于解决神经网络模型因为训练数据少，导致模型泛化能力差的问题。

以从英语到法语的翻译任务为例，分别对比传统的微调策略和GPT-3三种评估方式。

下图是传统的微调策略：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000167.png]]

传统的微调策略存在问题：

- 微调需要对每一个任务有一个任务相关的数据集以及和任务相关的微调。
- 需要一个相关任务大的数据集，而且需要对其进行标注
- 当一个样本没有出现在数据分布的时候，泛化性不见得比小模型要好

下图显示了 GPT-3 三种评估方式:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000166.png]]

在zero-shot的设置条件下：先给出任务的描述，之后给出一个测试数据对其进行测试，直接让预训练好的模型去进行任务测试。

在one-shot的设置条件下：在预训练和真正翻译的样本之间，插入一个样本做指导。好比说在预训练好的结果和所要执行的任务之间，给一个例子，告诉模型英语翻译为法语，应该这么翻译。

在few-shot的设置条件下：在预训练和真正翻译的样本之间，插入多个样本做指导。好比说在预训练好的结果和所要执行的任务之间，给多个例子，告诉模型应该如何工作。

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/02-Transformer 与预训练模型（Transformer and Pretrained Models）/07-GPT 模型演进（GPT Model Evolution）/07-GPT 模型演进（GPT Model Evolution）-20260813120000165.png]]

上述表格显示了 GPT-3 模型在执行零样本、单样本和少样本翻译任务时的Blue分数对比（用于度量同一源语句的自动翻译与人工创建的参考翻译之间的差异）。从表中可以看出， GPT-3 三种评估方式不用微调、梯度或参数更新，模型依然可以达到很好的效果，其中GPT-3的few-shot还在部分任务上超越了当前SOTA。

### 3 GPT-3和ChatGPT的区别和联系

ChatGPT是一种基于GPT-3的聊天机器人模型。它旨在使用 GPT-3 的语言生成能力来与用户进行自然语言对话。例如，用户可以向 ChatGPT 发送消息，然后 ChatGPT 会根据消息生成一条回复。

GPT-3 是一个更大的自然语言处理模型，而 ChatGPT 则是使用 GPT-3 来构建的聊天机器人。它们之间的关系是 ChatGPT 依赖于 GPT-3 的语言生成能力来进行对话。

### 4 python调用ChatGPT模型

要使用GPT-3或ChatGPT模型，您需要先访问OpenAI的API网站( [https://beta.openai.com/docs/quickstart](https://beta.openai.com/docs/quickstart) )，然后从API网站获取你的 API 密钥，然后则可以使用Python调用GPT-3或ChatGPT模型。

首先，您需要安装OpenAI的Python库，可以使用以下命令完成：

```bash
pip install openai
```

要使用 ChatGPT 模型，您需要使用以下代码：

```python
import openai

openai.api_key = "YOUR API KEY"

model_engine = "text-davinci-002"
# 使用GPT3: model_engine ="davinci"
prompt = "Hi, how are you doing today?"

completions = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.7,
)

message = completions.choices[0].text
print(message)
```

请注意，上述代码仅是示例，您可能需要根据自己的需要调整代码以获得所需的结果
