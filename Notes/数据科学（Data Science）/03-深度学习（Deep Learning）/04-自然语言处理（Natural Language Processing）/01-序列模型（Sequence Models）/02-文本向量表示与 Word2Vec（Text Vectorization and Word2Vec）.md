---
title: "文本向量表示、One-Hot、Word2Vec 与词嵌入（Text Vectorization, One-Hot, Word2Vec, and Embeddings）"
tags:
  - data-science/nlp
status: published
created: 2026-08-13
published_at: 2026-08-13
---
# 文本向量表示、One-Hot、Word2Vec 与词嵌入（Text Vectorization, One-Hot, Word2Vec, and Embeddings）

> [!warning] joblib 导入边界（joblib Import Boundary）
> `from sklearn.externals import joblib` 已从 scikit-learn 移除；现代环境应安装 `joblib` 并直接使用 `import joblib`。该变更记录在 [scikit-learn 0.21 变更说明](https://scikit-learn.org/stable/whats_new/v0.21.html)。

### 1 文本张量表示

- 将一段文本使用张量进行表示，其中一般将词汇表示成向量，称作词向量，再由各个词向量按顺序组成矩阵形成文本表示.
- 举个例子:

```text
["人生", "该", "如何", "起头"]

==>

# 每个词对应矩阵中的一个向量
[[1.32, 4,32, 0,32, 5.2],
 [3.1, 5.43, 0.34, 3.2],
 [3.21, 5.32, 2, 4.32],
 [2.54, 7.32, 5.12, 9.54]]
```

- 文本张量表示的作用:
  - 将文本表示成张量（矩阵）形式，能够使语言文本可以作为计算机处理程序的输入，进行接下来一系列的解析工作.
- 文本张量表示的方法:
  - one-hot编码
  - Word2vec
  - Word Embedding

### 2 one-hot词向量表示
> [!tip] 大白话理解（Plain-language Intuition）
> 词向量不是给词贴一个编号，而是把词放到一个可计算的坐标空间里；经常出现在相似上下文中的词会被放得更近。这样模型才能用距离和方向表达语义关系。

- 又称独热编码，将每个词表示成具有n个元素的向量，这个词向量中只有一个元素是1，其他元素都是0，不同词汇元素为0的位置不同，其中n的大小是整个语料中不同词汇的总数.
- 举个例子:

```text
["改变", "要", "如何", "起手"]`
==>

[[1, 0, 0, 0],
 [0, 1, 0, 0],
 [0, 0, 1, 0],
 [0, 0, 0, 1]]
```

- onehot编码实现:

> - 进行onehot编码:

```python
import jieba
# 导入keras中的词汇映射器Tokenizer
from tensorflow.keras.preprocessing.text import Tokenizer
# 导入用于对象保存与加载的joblib
from sklearn.externals import joblib

# 思路分析 生成onehot
# 1 准备语料 vocabs
# 2 实例化词汇映射器Tokenizer, 使用映射器拟合现有文本数据 (内部生成 index_word word_index)
# 2-1 注意idx序号-1
# 3 查询单词idx 赋值 zero_list，生成onehot
# 4 使用joblib工具保存映射器 joblib.dump()
def dm_onehot_gen():

    # 1 准备语料 vocabs
    vocabs = {"周杰伦", "陈奕迅", "王力宏", "李宗盛", "吴亦凡", "鹿晗"}

    # 2 实例化词汇映射器Tokenizer, 使用映射器拟合现有文本数据 (内部生成 index_word word_index)
    # 2-1 注意idx序号-1
    mytokenizer = Tokenizer()
    mytokenizer.fit_on_texts(vocabs)

    # 3 查询单词idx 赋值 zero_list，生成onehot
    for vocab in vocabs:
        zero_list = [0] * len(vocabs)
        idx = mytokenizer.word_index[vocab] - 1
        zero_list[idx] = 1
        print(vocab, '的onehot编码是', zero_list)

    # 4 使用joblib工具保存映射器 joblib.dump()
    mypath = './mytokenizer'
    joblib.dump(mytokenizer, mypath)
    print('保存mytokenizer End')

    # 注意5-1 字典没有顺序 onehot编码没有顺序 []-有序 {}-无序 区别
    # 注意5-2 字典有的单词才有idx idx从1开始
    # 注意5-3 查询没有注册的词会有异常 eg: 狗蛋
    print(mytokenizer.word_index)
    print(mytokenizer.index_word)
```

> - 输出效果:

```text
陈奕迅 的onehot编码是 [1, 0, 0, 0, 0, 0]
王力宏 的onehot编码是 [0, 1, 0, 0, 0, 0]
鹿晗 的onehot编码是 [0, 0, 1, 0, 0, 0]
周杰伦 的onehot编码是 [0, 0, 0, 1, 0, 0]
李宗盛 的onehot编码是 [0, 0, 0, 0, 1, 0]
吴亦凡 的onehot编码是 [0, 0, 0, 0, 0, 1]

保存mytokenizer End

{'陈奕迅': 1, '王力宏': 2, '鹿晗': 3, '周杰伦': 4, '李宗盛': 5, '吴亦凡': 6}
{1: '陈奕迅', 2: '王力宏', 3: '鹿晗', 4: '周杰伦', 5: '李宗盛', 6: '吴亦凡'}
```

> - onehot编码器的使用:

```python
# 思路分析
# 1 加载已保存的词汇映射器Tokenizer joblib.load(mypath)
# 2 查询单词idx 赋值zero_list，生成onehot 以token为'李宗盛'
# 3 token = "狗蛋" 会出现异常
def dm_onehot_use():

    vocabs = {"周杰伦", "陈奕迅", "王力宏", "李宗盛", "吴亦凡", "鹿晗"}

    # 1 加载已保存的词汇映射器Tokenizer joblib.load(mypath)
    mypath = './mytokenizer'
    mytokenizer = joblib.load(mypath)

    # 2 编码token为"李宗盛"  查询单词idx 赋值 zero_list，生成onehot
    token = "李宗盛"
    zero_list = [0] * len(vocabs)
    idx = mytokenizer.word_index[token] - 1
    zero_list[idx] = 1
    print(token, '的onehot编码是', zero_list)
```

> - 输出效果:

```text
李宗盛 的onehot编码是 [0, 0, 0, 0, 1, 0]
```

- one-hot编码的优劣势：
  - 优势：操作简单，容易理解.
  - 劣势：完全割裂了词与词之间的联系，而且在大语料集下，每个向量的长度过大，占据大量内存.
  - 正因为one-hot编码明显的劣势，这种编码方式被应用的地方越来越少，取而代之的是接下来我们要学习的稠密向量的表示方法word2vec和word embedding.

### 3 word2vec模型
#### 3.1 模型介绍

- word2vec是一种流行的将词汇表示成向量的无监督训练方法, 该过程将构建神经网络模型, 将网络参数作为词汇的向量表示, 它包含CBOW和skipgram两种训练模式.
- CBOW(Continuous bag of words)模式:
  - 给定一段用于训练的文本语料, 再选定某段长度(窗口)作为研究对象, 使用上下文词汇预测目标词汇.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）-20260813120000009.png]]

> - 分析:
> - 图中窗口大小为9, 使用前后4个词汇对目标词汇进行预测.

- CBOW模式下的word2vec过程说明:

> - 假设我们给定的训练语料只有一句话: Hope can set you free (愿你自由成长)，窗口大小为3，因此模型的第一个训练样本来自Hope can set，因为是CBOW模式，所以将使用Hope和set作为输入，can作为输出，在模型训练时， Hope，can，set等词汇都使用它们的one-hot编码. 如图所示: 每个one-hot编码的单词与各自的变换矩阵(即参数矩阵3x5, 这里的3是指最后得到的词向量维度)相乘之后再相加, 得到上下文表示矩阵(3x1).

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）-20260813120000010.png]]

> - 接着, 将上下文表示矩阵与变换矩阵(参数矩阵5x3, 所有的变换矩阵共享参数)相乘, 得到5x1的结果矩阵, 它将与我们真正的目标矩阵即can的one-hot编码矩阵(5x1)进行损失的计算, 然后更新网络参数完成一次模型迭代.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）-20260813120000011.png]]

> - 最后窗口按序向后移动，重新更新参数，直到所有语料被遍历完成，得到最终的变换矩阵(3x5)，这个变换矩阵与每个词汇的one-hot编码(5x1)相乘，得到的3x1的矩阵就是该词汇的word2vec张量表示.

- skipgram模式:
  - 给定一段用于训练的文本语料, 再选定某段长度(窗口)作为研究对象, 使用目标词汇预测上下文词汇.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）-20260813120000013.png]]

> - 分析:
> - 图中窗口大小为9, 使用目标词汇对前后四个词汇进行预测.

- skipgram模式下的word2vec过程说明:

> - 假设我们给定的训练语料只有一句话: Hope can set you free (愿你自由成长)，窗口大小为3，因此模型的第一个训练样本来自Hope can set，因为是skipgram模式，所以将使用can作为输入 ，Hope和set作为输出，在模型训练时， Hope，can，set等词汇都使用它们的one-hot编码. 如图所示: 将can的one-hot编码与变换矩阵(即参数矩阵3x5, 这里的3是指最后得到的词向量维度)相乘, 得到目标词汇表示矩阵(3x1).
> - 接着, 将目标词汇表示矩阵与多个变换矩阵(参数矩阵5x3)相乘, 得到多个5x1的结果矩阵, 它将与我们Hope和set对应的one-hot编码矩阵(5x1)进行损失的计算, 然后更新网络参数完成一次模 型迭代.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）-20260813120000014.png]]

> - 最后窗口按序向后移动，重新更新参数，直到所有语料被遍历完成，得到最终的变换矩阵即参数矩阵(3x5)，这个变换矩阵与每个词汇的one-hot编码(5x1)相乘，得到的3x1的矩阵就是该词汇的word2vec张量表示.

- 词向量的检索获取

> - 神经网络训练完毕后，神经网络的参数矩阵w就我们的想要词向量。如何检索某1个单词的向量呢？以CBOW方式举例说明如何检索a单词的词向量。
> - 如下图所示：a的onehot编码[10000]，用参数矩阵[3,5] * a的onehot编码[10000]，可以把参数矩阵的第1列参数给取出来，这个[3,1]的值就是a的词向量。

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）-20260813120000012.png]]

#### 3.2 word2vec的训练和使用

- 第一步: 获取训练数据
- 第二步: 训练词向量
- 第三步: 模型超参数设定
- 第四步: 模型效果检验
- 第五步: 模型的保存与重加载

##### 1 获取训练数据

数据来源： [http://mattmahoney.net/dc/enwik9.zip](http://mattmahoney.net/dc/enwik9.zip)

在这里, 我们将研究英语维基百科的部分网页信息, 它的大小在300M左右。这些语料已经被准备好, 我们可以通过Matt Mahoney的网站下载。

**注意：原始数据集已经放在/root/data/enwik9.zip，解压后数据为/root/data/enwik9，预处理后的数据为/root/data/fil9**

> - 查看原始数据:

```text
$ head -10 data/enwik9

# 原始数据将输出很多包含XML/HTML格式的内容, 这些内容并不是我们需要的
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.3/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.3/ http://www.mediawiki.org/xml/export-0.3.xsd" version="0.3" xml:lang="en">
  <siteinfo>
    <sitename>Wikipedia</sitename>
    <base>http://en.wikipedia.org/wiki/Main_Page</base>
    <generator>MediaWiki 1.6alpha</generator>
    <case>first-letter</case>
      <namespaces>
      <namespace key="-2">Media</namespace>
      <namespace key="-1">Special</namespace>
      <namespace key="0" />
```

> - 原始数据处理:

```text
# 使用wikifil.pl文件处理脚本来清除XML/HTML格式的内容
# perl wikifil.pl data/enwik9 > data/fil9 #该命令已经执行
```

> - 查看预处理后的数据:

```text
# 查看前80个字符
head -c 80 data/fil9

# 输出结果为由空格分割的单词
 anarchism originated as a term of abuse first used against early working class
```

##### 2 词向量的训练保存加载

fasttext 是 facebook 开源的一个词向量与文本分类工具。下面是该工具包的安装方法

```bash
# 训练词向量工具库的安装
# 方法1 简洁版
pip install fasttext
# 方法2：源码安装(推荐)
# 以linux安装为例： 目录切换到虚拟开发环境目录下，再执行git clone 操作
git clone https://github.com/facebookresearch/fastText.git
cd fastText
# 使用pip安装python中的fasttext工具包
sudo pip install .
```

```text
# 导入fasttext
import fasttext

def dm_fasttext_train_save_load():
    # 1 使用train_unsupervised(无监督训练方法) 训练词向量
    mymodel = fasttext.train_unsupervised('./data/fil9')
    print('训练词向量 ok')

    # 2 save_model()保存已经训练好词向量
    # 注意，该行代码执行耗时很长
    mymodel.save_model("./data/fil9.bin")
    print('保存词向量 ok')

    # 3 模型加载
    mymodel = fasttext.load_model('./data/fil9.bin')
    print('加载词向量 ok')

# 步骤1运行效果如下：
有效训练词汇量为124M, 共218316个单词
Read 124M words
Number of words:  218316
Number of labels: 0
Progress: 100.0% words/sec/thread:   53996 lr:  0.000000 loss:  0.734999 ETA:   0h 0m
```

##### 3 查看单词对应的词向量

```python
# 通过get_word_vector方法来获得指定词汇的词向量, 默认词向量训练出来是1个单词100特征
def dm_fasttext_get_word_vector():
    mymodel = fasttext.load_model('./data/fil9.bin')

    myvector = mymodel.get_word_vector('the')
    print('myvector->', type(myvector), myvector.shape, myvector)

# 运行效果如下：
array([-0.03087516,  0.09221972,  0.17660329,  0.17308897,  0.12863874,
        0.13912526, -0.09851588,  0.00739991,  0.37038437, -0.00845221,
        ...
       -0.21184735, -0.05048715, -0.34571868,  0.23765688,  0.23726143],
      dtype=float32)
```

##### 4 模型效果检验

```text
# 检查单词向量质量的一种简单方法就是查看其邻近单词, 通过我们主观来判断这些邻近单词是否与目标单词相关来粗略评定模型效果好坏.
# 查找"运动"的邻近单词, 我们可以发现"体育网", "运动汽车", "运动服"等.
>>> model.get_nearest_neighbors('sports')

[(0.8414610624313354, 'sportsnet'), (0.8134572505950928, 'sport'), (0.8100415468215942, 'sportscars'), (0.8021156787872314, 'sportsground'), (0.7889881134033203, 'sportswomen'), (0.7863013744354248, 'sportsplex'), (0.7786710262298584, 'sporty'), (0.7696356177330017, 'sportscar'), (0.7619683146476746, 'sportswear'), (0.7600985765457153, 'sportin')]

# 查找"音乐"的邻近单词, 我们可以发现与音乐有关的词汇.
>>> model.get_nearest_neighbors('music')

[(0.8908010125160217, 'emusic'), (0.8464668393135071, 'musicmoz'), (0.8444250822067261, 'musics'), (0.8113634586334229, 'allmusic'), (0.8106718063354492, 'musices'), (0.8049437999725342, 'musicam'), (0.8004694581031799, 'musicom'), (0.7952923774719238, 'muchmusic'), (0.7852965593338013, 'musicweb'), (0.7767147421836853, 'musico')]

# 查找"小狗"的邻近单词, 我们可以发现与小狗有关的词汇.
>>> model.get_nearest_neighbors('dog')

[(0.8456876873970032, 'catdog'), (0.7480780482292175, 'dogcow'), (0.7289096117019653, 'sleddog'), (0.7269964218139648, 'hotdog'), (0.7114801406860352, 'sheepdog'), (0.6947550773620605, 'dogo'), (0.6897546648979187, 'bodog'), (0.6621081829071045, 'maddog'), (0.6605004072189331, 'dogs'), (0.6398137211799622, 'dogpile')]
```

##### 5 模型超参数设定

```text
# 在训练词向量过程中, 我们可以设定很多常用超参数来调节我们的模型效果, 如:
# 无监督训练模式: 'skipgram' 或者 'cbow', 默认为'skipgram', 在实践中，skipgram模式在利用子词方面比cbow更好.
# 词嵌入维度dim: 默认为100, 但随着语料库的增大, 词嵌入的维度往往也要更大.
# 数据循环次数epoch: 默认为5, 但当你的数据集足够大, 可能不需要那么多次.
# 学习率lr: 默认为0.05, 根据经验, 建议选择[0.01，1]范围内.
# 使用的线程数thread: 默认为12个线程, 一般建议和你的cpu核数相同.

>>> model = fasttext.train_unsupervised('data/fil9', "cbow", dim=300, epoch=1, lr=0.1, thread=8)

Read 124M words
Number of words:  218316
Number of labels: 0
Progress: 100.0% words/sec/thread:   49523 lr:  0.000000 avg.loss:  1.777205 ETA:   0h 0m 0s
```

### 4 词嵌入word embedding介绍

- 通过一定的方式将词汇映射到指定维度(一般是更高维度)的空间.
- 广义的word embedding包括所有密集词汇向量的表示方法，如之前学习的word2vec, 即可认为是word embedding的一种.
- 狭义的word embedding是指在神经网络中加入的embedding层, 对整个网络进行训练的同时产生的embedding矩阵(embedding层的参数), 这个embedding矩阵就是训练过程中所有输入词汇的向量表示组成的矩阵.
- word embedding的可视化分析:

> - 通过使用tensorboard可视化嵌入的词向量.

```python
import torch
from tensorflow.keras.preprocessing.text import Tokenizer
from torch.utils.tensorboard import SummaryWriter
import jieba
import torch.nn as nn

# 注意：
# fs = tf.io.gfile.get_filesystem(save_path)
# AttributeError: module 'tensorflow._api.v2.io.gfile' has no attribute 'get_filesystem'
# 错误原因分析：
#  1 from tensorboard.compat import tf 使用了tf 如果安装tensorflow，默认会调用它tf的api函数
import tensorflow as tf
import tensorboard as tb
tf.io.gfile = tb.compat.tensorflow_stub.io.gfile

# 实验：nn.Embedding层词向量可视化分析
# 1 对句子分词 word_list
# 2 对句子word2id求my_token_list，对句子文本数值化sentence2id
# 3 创建nn.Embedding层，查看每个token的词向量数据
# 4 创建SummaryWriter对象, 可视化词向量
#   词向量矩阵embd.weight.data 和 词向量单词列表my_token_list添加到SummaryWriter对象中
#   summarywriter.add_embedding(embd.weight.data, my_token_list)
# 5 通过tensorboard观察词向量相似性
# 6 也可通过程序，从nn.Embedding层中根据idx拿词向量

def dm02_nnembeding_show():

    # 1 对句子分词 word_list
    sentence1 = '传智教育是一家上市公司，旗下有黑马程序员品牌。我是在黑马这里学习人工智能'
    sentence2 = "我爱自然语言处理"
    sentences = [sentence1, sentence2]

    word_list = []
    for s in sentences:
        word_list.append(jieba.lcut(s))
    # print('word_list--->', word_list)

    # 2 对句子word2id求my_token_list，对句子文本数值化sentence2id
    mytokenizer = Tokenizer()
    mytokenizer.fit_on_texts(word_list)
    # print(mytokenizer.index_word, mytokenizer.word_index)

    # 打印my_token_list
    my_token_list = mytokenizer.index_word.values()
    print('my_token_list-->', my_token_list)

    # 打印文本数值化以后的句子
    sentence2id = mytokenizer.texts_to_sequences(word_list)
    print('sentence2id--->', sentence2id, len(sentence2id))

    # 3 创建nn.Embedding层
    embd = nn.Embedding(num_embeddings=len(my_token_list), embedding_dim=8)
    # print("embd--->", embd)
    # print('nn.Embedding层词向量矩阵-->', embd.weight.data, embd.weight.data.shape, type(embd.weight.data))

    # 4 创建SummaryWriter对象 词向量矩阵embd.weight.data 和 词向量单词列表my_token_list
    summarywriter = SummaryWriter()
    summarywriter.add_embedding(embd.weight.data, my_token_list)
    summarywriter.close()

    # 5 通过tensorboard观察词向量相似性
    # cd 程序的当前目录下执行下面的命令
    # 启动tensorboard服务 tensorboard --logdir=runs --host 0.0.0.0
    # 通过浏览器，查看词向量可视化效果 http://127.0.0.1:6006

    print('从nn.Embedding层中根据idx拿词向量')
    # # 6 从nn.Embedding层中根据idx拿词向量
    for idx in range(len(mytokenizer.index_word)):
        tmpvec = embd(torch.tensor(idx))
        print('%4s'%(mytokenizer.index_word[idx+1]), tmpvec.detach().numpy())
```

> - 程序运行效果

```text
 my_token_list--> dict_values(['是', '黑马', '我', '传智', '教育', '一家', '上市公司', '，', '旗下', '有', '程序员', '品牌', '。', '在', '这里', '学习', '人工智能', '爱', '自然语言', '处理'])

sentence2id---> [[4, 5, 1, 6, 7, 8, 9, 10, 2, 11, 12, 13, 3, 1, 14, 2, 15, 16, 17], [3, 18, 19, 20]] 2

从nn.Embedding层中根据idx拿词向量

  是      [ 0.46067393 -0.9049023  -0.03143226 -0.32443136  0.03115687 -1.3352231
 -0.08336695 -2.4732168 ]
 黑马      [ 0.66760564  0.08703537  0.23735243  1.5896837  -1.8869231   0.22520915
 -1.0676078  -0.7654686 ]
  我      [-0.9093167  -0.6114051  -0.6825029   0.9269122   0.5208822   2.294128
 -0.11160549 -0.34862307]
 传智      [-1.1552105 -0.4274638 -0.8121502 -1.4969801 -1.3328248 -1.0934378
  0.6707438 -1.1796173]
 教育      [ 0.01580311 -1.1884228   0.59364647  1.5387698  -1.0822943   0.36760855
 -0.4652998  -0.57378227]
 一家      [-1.1898873  -0.42482868 -1.9391155  -1.5678993  -1.6960118   0.22525501
 -1.0754168   0.41797593]
上市公司     [ 0.590556   2.4274144  1.6698223 -0.9776848 -0.6119061  0.4434897
 -2.3726876 -0.2607738]
  ，      [-0.17568143  1.0074369   0.2571488   1.8940887  -0.5383494   0.65416646
  0.63454026  0.6235991 ]
 旗下      [ 2.8400452  -1.0096515   2.247107    0.30006626 -1.2687006   0.05855403
  0.01199368 -0.6156502 ]
  有      [ 0.89320636 -0.43819678  1.0345292   1.3546743  -1.4238662  -1.6994532
  0.30445674  2.673923  ]
程序员      [ 1.2147354   0.24878891  0.36161897  0.37458655 -0.48264053 -0.0141514
  1.2033817   0.7899459 ]
 品牌      [ 0.59799325 -0.01371854  0.0628166  -1.4829391   0.39795023 -0.39259398
 -0.60923046  0.54170054]
  。      [ 0.59599686  1.6038656  -0.10832139  0.25223547  0.37193906  1.1944667
 -0.91253406  0.6869221 ]
  在      [-1.161504    2.6963246  -0.6087775   0.9399654   0.8480068   0.684357
  0.96156543 -0.3541162 ]
 这里      [ 0.1034054  -0.01949253  0.8989019   1.61057    -1.5983531   0.17945968
 -0.17572908 -0.9724814 ]
 学习      [-1.3899843  -1.0846052  -1.1301199  -0.4078141   0.40511298  0.6562911
  0.9231357  -0.34704337]
人工智能     [-1.4966388  -1.0905199   1.001238   -0.75254333 -1.4210068  -1.854177
  1.0471514  -0.27140012]
  爱      [-1.5254552   0.6189947   1.2703396  -0.4826037  -1.4928672   0.8320283
  1.7333516   0.16908517]
自然语言     [-0.3856235  -1.2193452   0.9991112  -1.5821775   0.45017946 -0.66064674
  0.08045111  0.62901515]
 处理      [ 1.5062869   1.3156213  -0.21295634  0.47610474  0.08946162  0.57107806
 -1.0727187   0.16396333]

 词向量和词显示标签 写入磁盘ok 在当前目录下查看 ./runs 目录
```

> - 在终端启动tensorboard服务:

```text
$ cd ~
$ tensorboard --logdir=runs --host 0.0.0.0

# 通过http://192.168.88.161:6006访问浏览器可视化页面
```

> - 浏览器展示并可以使用右侧近邻词汇功能检验效果:

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/01-序列模型（Sequence Models）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）/02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）-20260813120000015.png]]
## Gensim Word2Vec 词向量的加载、训练与迁移（Gensim Word2Vec Loading, Training, and Transfer）
> [!tip] 大白话理解（Plain-language Intuition）
> `KeyedVectors` 是“只负责查词向量的字典”，适合加载别人已经训练好的向量；`Word2Vec` 还包含训练状态，适合在自己的语料上继续学习。训练结束后只需查询向量时，保存 `model.wv` 更轻量。
### 1. Word2Vec 文本格式（Word2Vec Text Format）
- 第一行通常是 `<词汇总数> <向量维度>`。
- 后续每行是一个词及其向量分量：`word value_1 value_2 ... value_n`。
- 文本格式便于检查但体积大；二进制格式（Binary Format）加载更快，读取时必须让 `binary` 参数与文件实际格式一致。
### 2. 加载公开词向量（Loading Pretrained Vectors）
```python
from gensim.models import KeyedVectors

vectors = KeyedVectors.load_word2vec_format(
    "sgns.weibo.word.bz2",
    binary=False,
)

print(vectors.vector_size)  # 300，具体值取决于文件
print(vectors.similarity("地铁", "公交"))  # 浮点相似度，结果取决于所加载的向量
print(vectors.most_similar("地铁", topn=3))  # 三个最相近词及其余弦相似度
```
- `vectors[word]` 返回该词的稠密向量（Dense Vector）。词不在词表中时会抛出 `KeyError`，工程代码应先使用 `word in vectors.key_to_index` 检查。
- `similarity(a, b)` 计算两个词向量的余弦相似度（Cosine Similarity）；接近 `1` 表示方向相近，接近 `-1` 表示方向相反，但它不等同于严格的人类语义判断。
- `most_similar()` 支持正向词与负向词组合，可做类比查询；结果会继承训练语料中的偏差（Bias）。
### 3. 在自有语料上训练（Training on a Custom Corpus）
```python
import jieba
import pandas as pd
from gensim.models import Word2Vec

data = pd.read_csv("reviews.csv", encoding="utf-8", usecols=["review"])
sentences = [
    [token for token in jieba.lcut(review) if token.strip()]
    for review in data["review"].dropna()
]

model = Word2Vec(
    sentences=sentences,
    vector_size=100,  # 每个词向量的维度；越大表达容量越高，内存和样本需求也越大。
    window=5,         # 中心词左右最多观察多少个上下文位置。
    min_count=2,      # 低于该频次的词不进入词表，减少噪声和内存占用。
    sg=1,             # 1 表示 Skip-gram；0 表示 CBOW。
    workers=4,        # 并行训练线程数；多线程可能使逐次结果不完全可复现。
    seed=42,
)

# 保存为通用 Word2Vec 格式；磁盘写入属于外部副作用，不提供固定输出。
model.wv.save_word2vec_format("my_vectors.kv", binary=False)
```
- **Skip-gram**：用中心词预测上下文，通常更关注低频词，但训练较慢。
- **CBOW**：用上下文预测中心词，训练通常更快，对高频模式较稳定。
- `min_count` 过高会删除有价值的领域术语；过低会扩大词表并把拼写噪声引入模型。
### 4. 初始化 PyTorch 嵌入层（Initializing a PyTorch Embedding）
```python
import torch
from torch import nn

word_to_index = vectors.key_to_index
embedding_matrix = torch.tensor(vectors.vectors, dtype=torch.float32)

embedding = nn.Embedding.from_pretrained(
    embedding_matrix,
    freeze=False,  # False 允许下游任务继续微调；True 可保留原向量并减少可训练参数。
)

tokens = ["我", "喜欢", "地铁"]
missing = [token for token in tokens if token not in word_to_index]
if missing:
    raise KeyError(f"词表中缺少 Token：{missing}")

token_ids = torch.tensor([[word_to_index[token] for token in tokens]])
embedded = embedding(token_ids)
print(embedded.shape)  # torch.Size([1, 3, 300])，末维取决于 vectors.vector_size
```
- `freeze=True` 适合小数据或希望固定通用语义的场景；`freeze=False` 允许适配当前任务，但学习率过大会破坏已有语义结构。
- 预训练词表通常没有专用的填充 Token（Padding Token）和未知 Token（Unknown Token）；构建下游词表时应明确这些行的索引、初始化方式与 `padding_idx`。
- 如果重新排列词表，必须同步重排向量矩阵；只复制向量而沿用另一套 Token-ID 映射会造成静默语义错位。
