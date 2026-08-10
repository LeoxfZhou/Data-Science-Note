## 概念速查表

在看代码前，先用这张表快速对应 Gensim 的核心概念：

|**Gensim 核心方法**|**作用与解释**|**笔记核心提炼**|
|---|---|---|
|**`Dictionary`**|建立词汇与 ID 的双向映射表（词典）|去重，给每个词分配唯一索引。|
|**`token2id`**|通过词查询对应的数字 ID|例如 `dct.token2id['上班']` -> `22`。|
|**`dct[id]`**|通过数字 ID 反向查询原词|例如 `dct[22]` -> `'上班'`。|
|**`doc2idx`**|将一段文本转化为 ID 序列|未登录词（词典里没有的词）会标为 `-1`。|
|**`doc2bow`**|一键转换成 **稀疏词袋表示**|输出格式为 `[(词ID, 出现频次), ...]`，极省内存。|
|**`TfidfModel`**|计算词语在文档中的 TF-IDF 权重|过滤高频无用词，突出高区分度特征。|

## 一、 简易语料库的构建与词典操作 (CELL 1 ~ 4)

这一部分首先使用 `jieba` 对中文句子进行分词，然后利用 Gensim 的 `Dictionary` 类自动建立一个“词典”，并演示了词典的基本查询与保存。

Python

```
import numpy as np
import gensim
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
import jieba

# ==================== Step 1: 文本准备与中文分词 ====================

text1 = "我是来自湖南张家界的小明，我喜好大海\n我从事IT相关工作\n我讨厌夏天"
text2 = "计算机视觉和自然语言我比较喜好自然语言的内容"
text3 = "我不想上班，我想出去玩"

# 初始化文档列表，准备存放分词结果
docs = []

# 遍历每个文本，去除换行符，并使用 jieba 进行精准分词
for text in [text1, text2, text3]:
    # text.replace('\n', '') 去除文本中的换行，防止分词出现干扰
    # jieba.lcut 会直接返回一个分词后的 list
    docs.append(list(jieba.lcut(text.replace('\n', ''))))

# 输出分词后的文档列表：一个“二维列表”结构
# docs -> [['我', '是', '来自', ...], ['计算机', '视觉', ...], ...]
print("分词后的语料库 docs:\n", docs)


# ==================== Step 2: 构建词典 (Dictionary) ====================

# Dictionary 类会自动统计 docs 中所有不重复的词，并建立 {词 -> 唯一ID} 的映射
dct = Dictionary(docs)

# len(dct) 可以直接获取词典中不重复词的总数（即词汇量）
print(f"去重后单词数目/词典大小: {len(dct)}")
print(f"当前词典内部状态: {dct}")


# ==================== Step 3: 词典的常见 API 操作 ====================

# 将词典保存为可读的 txt 文本，方便本地查看映射关系（格式为：ID\t词\t频次）
dct.save_as_text('./datas/a.txt')

# 1. 正向查询：通过【词】找【ID】 (通过 .token2id 属性)
print("‘上班’对应的ID:", dct.token2id['上班']) 
print("‘我’对应的ID:", dct.token2id['我'])     

# 2. 反向查询：通过【ID】找【词】 (直接像列表一样索引 dct)
print("ID为22的词是:", dct[22]) 
print("ID为0的词是:", dct[0])   
```

> 📝 **我的笔记：**
> 
> - **分词：** 计算机看不懂一整句中文，必须先切分成一个个词语（用 `jieba.lcut` ）。
>     
> - **词典：** `Dictionary` 的作用就是做一张“花名册”。它把所有分出来的词排个序，并给每个词发一个唯一的数字编号（ID）。
>     

## 二、 底层原理剖析：手写 One-Hot 与词袋模型 (CELL 5)

**这一步是全代码的核心痛点！** 作者在这里故意绕了个弯，手动用最基础的矩阵操作还原了“词袋模型”的生成过程，目的是为了让我们理解底层数学逻辑。

$$\text{词袋向量 (Bag of Words)} = \sum (\text{该句子中每个词的 One-Hot 向量})$$

Python

```
# ==================== Step 4: 序号化与手写 One-Hot、词袋 ====================

# 这里的 n 表示词典大小加 1。为什么要 +1？
# 因为多留了一维给“未登录词（OOV）”，防止在后面的矩阵索引中越界。
n = len(dct) + 1 

text4 = "我是来自北京的小明"
text4_words = list(jieba.lcut(text4.replace('\n', ''))) # 分词结果

# 1. 序号化：将词转化为对应的 ID
# dct.doc2idx 接收词列表，返回对应的 ID 列表。若词不在词典中（比如“北京”），默认返回 -1。
# 为了避免索引 -1 在 Python 中指向列表末尾，这里将所有 ID 整体 +1。
# 这样，未登录词的 ID (-1) + 1 就变成了 0（作为未知词的专属通道），其他有效 ID 也顺利后移。
result = list(np.asarray(dct.doc2idx(text4_words, unknown_word_index=-1)) + 1)
print("分词列表:", text4_words)
print("序号化结果 (整体+1，防止未知词 -1 越界):", result)

# 2. 构建 One-Hot 矩阵
# 初始化一个形状为 [当前文档单词数, 词典大小n] 的全零矩阵
result2 = [[0] * n for _ in range(len(result))]

# 遍历每个词的 ID，在对应的索引位置填入 1
for i, _id in enumerate(result):
    if _id != -1:  # 如果是有效词ID
        result2[i][_id] = 1
print("One-Hot结果 (每一行代表一个词的独热编码):")
print(result2)

# 3. 计算手写词袋法结果
# 词袋法（BOW）就是把文档中每个词的 One-Hot 向量进行相加（降维叠加），从而得到句子中每个词出现的频次。
# np.sum(..., axis=0) 将所有词的独热编码沿列相加，得到一条长度为 n 的频次向量
result3 = list(np.sum(np.asarray(result2), 0))
print("手写词袋法结果 (所有词的 One-Hot 叠加):")
print(result3)
```

> 📝 **我的笔记：**
> 
> - **One-Hot（独热编码）：** 给每个词造一个超长的向量，只有该词对应 ID 的那个格子里是 `1`，其他格子全是 `0`。
>     
> - **词袋模型（BOW）：** 词袋只关心“词频”。把句子里所有词的 One-Hot 像叠罗汉一样加起来，就得到了这个句子中每个词的出现次数。
>     

## 三、 工业级封装：Gensim 的 doc2bow 威力 (CELL 6)

手写 One-Hot 矩阵极其消耗内存（因为里面有海量的 `0`，属于**稀疏矩阵**）。在实际工程中，我们绝对不手写，而是直接用 Gensim 封装好的 `doc2bow`，它只保存非零的数据，极大节省内存。

Python

```
# ==================== Step 5: 手写逻辑 vs Gensim 自带 doc2bow ====================

text4 = "我是来自北京的小明，我喜好玩游戏" # 包含未登录词 "北京"、"玩游戏"
text4_words = list(jieba.lcut(text4.replace('\n', '')))

# 【原生手写路线】
result = dct.doc2idx(text4_words)  # 原生 ID 列表，未登录词仍为 -1
print("原生序号化结果 (未登录词为 -1):", result)

# 生成没有偏移（即维度就是实际词典大小 len(dct)）的 One-Hot 矩阵
result2 = [[0] * len(dct) for _ in range(len(result))]
for i, _id in enumerate(result):
    if _id != -1:                  # 自动过滤未登录词，不计入统计
        result2[i][_id] = 1

# 沿列求和得到词袋向量
result3 = list(np.sum(np.asarray(result2), 0))
print("原生手写词袋向量:\n", result3)


# 【Gensim 工业路线】
# 一行代码代替上述所有手动操作！
# doc2bow 返回的是稀疏格式：[(词ID, 词频), (词ID, 词频), ...]
result4 = dct.doc2bow(text4_words) 
print("Gensim 官方 doc2bow 稀疏表示:\n", result4)
```

> 📝 **我的笔记：**
> 
> - 假设词典有 10 万个词，一句话只有 5 个词。手写词袋会产生一个 10 万维的巨型列表（里面有 99995 个零）；
>     
> - 而 `dct.doc2bow` 返回：`[(2, 1), (5, 1), (8, 2)]`（只记录有频次的词），这不仅精简，更是 NLP 处理海量文本时活命的技巧。
>     

## 四、 TF-IDF 模型的计算与实战 (CELL 7 ~ 13)

这一部分先在迷你语料库上计算 TF-IDF，随后加载著名的英文大文本数据集 **`text8`** 进行真实场景的实战：如何切分伪文档、建立百万词典并输出 TF-IDF 权重。

Python

```
# ==================== Step 6: 迷你语料库上的 TF-IDF ====================

# 1. 将迷你语料库（3个文档）全部转换为 Gensim 稀疏词袋列表
corpus = [dct.doc2bow(doc) for doc in docs]

# 2. 初始化并训练 TF-IDF 模型
# 模型通过统计整个语料库中词语的分布，计算出每个词的 IDF（逆文档频率）值
model = TfidfModel(corpus=corpus)

# 3. 使用模型预测：传入第一个文档的词袋，输出其所有词的 TF-IDF 权重
# 输出格式同样为稀疏表示：[(词ID, TF-IDF值), ...]
print("第一个文档的 TF-IDF 权重结果:\n", model[corpus[0]])


# ==================== Step 7: 实战——大语料加载与伪文档切分 ====================

# text8 是由维基百科清洗出来的超长英文单一文本（没有明确的文档边界）
with open('./datas/text8', 'r', encoding='utf-8') as reader:
    content = reader.read()

# 数据预处理：
# 1. content.split(" "): 按空格切割成单词
# 2. filter(lambda t: t.strip(), ...): 过滤掉多余的空格或空字符串
# 3. word.encode("utf-8"): 将英文单词转换为 byte 字节格式（更省内存空间）
words = list(map(lambda word: word.encode("utf-8"), filter(lambda t: t.strip(), content.split(" "))))
total_words = len(words)
print("text8 总单词数目:", total_words)
print("前10个单词:", words[:10])

# 伪文档切分：
# 因为 TF-IDF 的核心是基于“文档（Document）”计算的，如果只有一整篇文本就无法计算 IDF。
# 因此这里采用“每 10,000 个单词切分为一个模拟文档”的方式，强行构建一个多文档语料库。
word_per_doc = 10000
docs = []

for i in range(total_words // word_per_doc + 1):
    start_idx = i * word_per_doc
    end_idx = start_idx + word_per_doc
    tmp_words = words[start_idx:end_idx]
    if len(tmp_words) > 0:
        docs.append(tmp_words)
        
print("模拟分割出的总文档数目:", len(docs))


# ==================== Step 8: 大语料下的 TF-IDF 完整流水线 ====================

# 1. 针对 text8 构建庞大的大词典
dct_large = Dictionary(docs)
print(f"大语料词典大小: {len(dct_large)}")

# 2. 将所有分割后的伪文档转换为稀疏词袋表示
corpus_large = [dct_large.doc2bow(line) for line in docs]

# 3. 训练大语料的 TF-IDF 模型
model_large = TfidfModel(corpus=corpus_large)

# 4. 获取并计算第一个模拟文档的 TF-IDF
tfidf_large_result = model_large[corpus_large[0]]
print("第一个伪文档的 TF-IDF 稀疏表示长度:", len(tfidf_large_result))
print("前5个词的 TF-IDF 权重结果:", tfidf_large_result[:5])
```

> 📝 **我的笔记：**
> 
> - **TF-IDF 的终极奥义：**
>     
>     - **TF (Term Frequency, 词频)**：这个词在我这篇文档里出现了几次？（越多越重要）
>         
>     - **IDF (Inverse Document Frequency, 逆文档频率)**：这个词在所有文档中多常见？像 "the", "of", "的" 在所有文档都出现，IDF 就极低；而像 "anarchism" 只在特定文档出现，IDF 就极高。
>         
>     - **公式**：$\text{TF-IDF} = \text{TF} \times \text{IDF}$，即**频次高且有独特代表性**的词，权重才高。
>