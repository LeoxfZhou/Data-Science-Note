---
title: "NLP 预处理、传统特征与评估速查表（NLP Preprocessing, Traditional Features, and Evaluation Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - nlp/fundamentals
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "Python 3.11+；Jieba 0.42.x；Gensim 4.x；HanLP 2.x；spaCy 3.x；fastText 0.9.x；WordCloud 1.9.x"
---
# NLP 预处理、传统特征与评估速查表（NLP Preprocessing, Traditional Features, and Evaluation Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
文本流水线必须保存分词器、词表、特殊 token、最大长度、标签映射和评估脚本；训练与推理完全复用。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 2. 包级安装与导入索引（Package Installation and Import Index）
### 2.1 Jieba 中文分词（Jieba Chinese Segmentation）
- **安装包（Distribution）**：`jieba`。
- **导入模块（Import Module）**：`jieba`、`jieba.analyse`、`jieba.posseg`。
- **安装命令（Installation）**：`python -m pip install jieba`。
- **用途（Purpose）**：中文分词、关键词提取与词性标注。
- **正式笔记（Detailed Note）**：[[02-Jieba 中文分词、词典、关键词与词性（Jieba Tokenization and Keywords）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|精确模式|`jieba.lcut(text, cut_all=False)`|返回词列表，适合正文分析|
|全模式|`jieba.lcut(text, cut_all=True)`|返回所有可能词，结果可能重叠|
|搜索模式|`jieba.lcut_for_search(text)`|返回更细粒度词列表，适合搜索索引|
|加载词典|`jieba.load_userdict(path)`|原地更新当前分词器词典；文件 I/O|
|动态加词|`jieba.add_word(word, freq=None, tag=None)`|原地加入词及可选词频、词性|
|动态删词|`jieba.del_word(word)`|原地移除用户词条|
|调整切分|`jieba.suggest_freq(segment, tune=True)`|返回建议频率；`tune=True` 时修改词典|
|TF-IDF 关键词|`jieba.analyse.extract_tags(text, topK=20, withWeight=False)`|返回关键词列表或 `(词, 权重)` 列表|
|TextRank 关键词|`jieba.analyse.textrank(text, topK=20, withWeight=False)`|返回关键词列表或带权重列表|
|词性标注|`jieba.posseg.lcut(text)`|返回含 `word`、`flag` 的词对列表|
|启用并行|`jieba.enable_parallel(processnum)`|创建多进程加速默认分词器；Windows 不支持|
|关闭并行|`jieba.disable_parallel()`|终止 Jieba 并行进程|

```python
import jieba
import jieba.analyse
import jieba.posseg as pseg

text = "自然语言处理可以帮助机器理解文本"
print(jieba.lcut(text))
print(jieba.lcut_for_search("自然语言处理"))
jieba.add_word("大语言模型", freq=10000, tag="n")
print(jieba.lcut("大语言模型正在发展"))
print(jieba.analyse.extract_tags(text, topK=2))
print([(item.word, item.flag) for item in pseg.lcut("机器学习")])

# 期望输出（不同词典版本的切分与权重可能略有差异）:
# ['自然语言', '处理', '可以', '帮助', '机器', '理解', '文本']
# ['自然', '语言', '自然语言', '处理', '自然语言处理']
# ['大语言模型', '正在', '发展']
# ['自然语言', '文本']
# [('机器', 'n'), ('学习', 'v')]
```
- **停用词边界（Stop-word Boundary）**：`jieba.lcut()` 不会自动删除停用词；应在分词后用集合过滤。`extract_tags()` 与 `textrank()` 可分别通过对应分析器设置停用词文件。
- **状态边界（State Boundary）**：`load_userdict()`、`add_word()`、`del_word()` 和 `suggest_freq(..., tune=True)` 会修改进程内分词器状态，测试之间应重建独立 `jieba.Tokenizer()` 以避免相互污染。
- **并行边界（Parallel Boundary）**：并行模式依赖 `fork`，只支持 POSIX 系统，短文本可能因进程通信反而更慢。
### 2.2 Gensim 主题与向量工具（Gensim Topic and Vector Tools）
- **安装包（Distribution）**：`gensim`。
- **导入模块（Import Module）**：`gensim`。
- **安装命令（Installation）**：`python -m pip install --upgrade gensim`。
- **用途（Purpose）**：词典、词袋（Bag of Words, BoW）、TF-IDF、Word2Vec 与相似度检索。
- **正式笔记（Detailed Note）**：[[03-Gensim 词典、词袋与 TF-IDF（Gensim Dictionary, BoW, and TF-IDF）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|建立词典|`corpora.Dictionary(tokenized_docs)`|返回词典并分配 token ID|
|转词袋|`dictionary.doc2bow(tokens)`|返回稀疏 `(token_id, count)` 列表|
|过滤词表|`dictionary.filter_extremes(no_below=5, no_above=0.5)`|原地删除低频或过高频 token 并重排 ID|
|训练 TF-IDF|`models.TfidfModel(corpus)`|返回已拟合转换模型|
|转换语料|`tfidf[corpus]`|惰性返回稀疏 TF-IDF 向量|
|训练 Word2Vec|`models.Word2Vec(sentences, vector_size=100, window=5, min_count=5)`|返回模型；训练耗时且结果受随机性影响|
|近邻查询|`model.wv.most_similar(word, topn=10)`|返回 `(词, 余弦相似度)` 列表|

```python
from gensim import corpora, models

docs = [["机器", "学习"], ["机器", "翻译"]]
dictionary = corpora.Dictionary(docs)
corpus = [dictionary.doc2bow(doc) for doc in docs]
tfidf = models.TfidfModel(corpus)
print(len(dictionary), corpus[0])  # 输出: 3 [(0, 1), (1, 1)]
print(len(list(tfidf[corpus])))  # 输出: 2
```
- **边界（Boundary）**：`filter_extremes()` 会修改词典并改变 ID；持久化模型时必须同时保存匹配的词典和预处理规则。
### 2.3 HanLP 本地与 RESTful（HanLP Native and RESTful）
- **安装包（Distribution）**：本地推理使用 `hanlp`，云端客户端使用 `hanlp-restful`。
- **导入模块（Import Module）**：两者均使用 `hanlp` 命名空间，REST 客户端为 `hanlp_restful`。
- **安装命令（Installation）**：`python -m pip install hanlp`；REST 客户端为 `python -m pip install hanlp-restful`。
- **用途（Purpose）**：分词、词性、命名实体识别、依存句法与多任务 NLP。
- **正式笔记（Detailed Note）**：[[04-HanLP 本地推理与 RESTful 调用（HanLP Native and RESTful Usage）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|加载本地模型|`hanlp.load(model_id_or_path)`|首次可能下载模型；返回可调用组件|
|本地推理|`component(text_or_texts)`|返回任务相关字典、列表或文档对象|
|创建 REST 客户端|`HanLPClient(url, auth=token, language='zh')`|返回远程客户端，不立即请求|
|REST 解析|`client.parse(text, tasks=[...])`|发起网络请求并返回文档结果|

```python
import hanlp
import os
from hanlp_restful import HanLPClient

print(isinstance(hanlp.__version__, str))  # 输出: True
client = HanLPClient("https://www.hanlp.com/api", auth=os.environ["HANLP_AUTH"], language="zh")
# result = client.parse("自然语言处理", tasks=["tok/fine", "pos"])
# 网络请求依赖有效 HANLP_AUTH、额度和服务可用性，不提供固定输出。
```
- **安全边界（Security Boundary）**：真实令牌必须来自环境变量；本地 `hanlp.load()` 可能下载大型模型，生产环境应固定模型版本与缓存目录。
### 2.4 spaCy 工业 NLP 流水线（spaCy Industrial NLP Pipeline）
- **安装包（Distribution）**：`spacy`；语言模型是单独分发包。
- **导入模块（Import Module）**：`spacy`。
- **安装命令（Installation）**：`python -m pip install spacy`，随后按任务安装官方语言模型。
- **用途（Purpose）**：高性能分词、词性、实体、依存分析与可组合流水线。
- **正式笔记（Detailed Note）**：[[04-Transformer 机器翻译（Transformer Machine Translation）]] 中的工具对照。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|空白语言对象|`spacy.blank('en')`|返回无统计组件的 `Language`|
|处理文本|`nlp(text)`|返回 `Doc`|
|批处理|`nlp.pipe(texts, batch_size=128)`|惰性返回 `Doc` 迭代器|
|查看组件|`nlp.pipe_names`|返回流水线组件名列表|
|禁用组件|`nlp.select_pipes(disable=[...])`|返回上下文管理器，临时改变启用状态|

```python
import spacy

nlp = spacy.blank("en")
doc = nlp("Data science works.")
print([token.text for token in doc])  # 输出: ['Data', 'science', 'works', '.']
```
- **边界（Boundary）**：`spacy.blank()` 只有规则分词能力；词性、实体和依存结果需要安装并加载带权重的语言模型。
### 2.5 fastText 词向量与文本分类（fastText Embeddings and Classification）
- **安装包（Distribution）**：`fasttext`。
- **导入模块（Import Module）**：`fasttext`。
- **安装命令（Installation）**：`python -m pip install fasttext`。
- **用途（Purpose）**：子词词向量、监督文本分类和模型量化。
- **正式笔记（Detailed Note）**：[[03-FastText 文本分类与词向量（FastText Classification and Embeddings）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|监督训练|`fasttext.train_supervised(input=path, epoch=5, lr=0.1)`|读取训练文件并返回模型|
|无监督训练|`fasttext.train_unsupervised(input=path, model='skipgram')`|返回词向量模型|
|预测|`model.predict(text, k=1, threshold=0.0)`|返回标签元组与概率数组|
|词向量|`model.get_word_vector(word)`|返回固定维度 NumPy 数组|
|保存|`model.save_model(path)`|写入二进制模型文件|

```python
import fasttext

# model = fasttext.train_supervised(input="train.txt", epoch=5)
# labels, probabilities = model.predict("这部电影很好", k=1)
# 训练会读取文件并生成模型；预测结果取决于训练数据，不提供固定输出。
```
- **输入格式（Input Format）**：监督训练每行必须包含形如 `__label__positive 文本内容` 的标签；换行代表样本边界。
### 2.6 WordCloud 词云（WordCloud）
- **安装包（Distribution）**：`wordcloud`。
- **导入模块（Import Module）**：`wordcloud`。
- **安装命令（Installation）**：`python -m pip install wordcloud`。
- **用途（Purpose）**：按词频生成可视化词云；中文通常需要显式字体路径。
- **正式笔记（Detailed Note）**：[[01-文本语料探索性分析（Exploratory Text Corpus Analysis）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|由文本生成|`WordCloud(...).generate(text)`|拟合词频并返回自身|
|由频率生成|`WordCloud(...).generate_from_frequencies(freq)`|按给定频率更新布局并返回自身|
|转数组|`cloud.to_array()`|返回 RGB NumPy 数组|
|保存图片|`cloud.to_file(path)`|写文件并返回自身|

```python
from wordcloud import WordCloud

cloud = WordCloud(width=200, height=100, background_color="white").generate("data science data")
print(cloud.width, cloud.height)  # 输出: 200 100
```
- **边界（Boundary）**：中文文本应先分词并用空格连接；缺少可显示中文的 `font_path` 时可能出现方框或空白。
## 清洗、切分与规范化（Cleaning and Tokenization）
清洗只移除与任务确认无关的噪声；不要盲目删除大小写、标点、数字或否定词。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|Unicode 规范化|`unicodedata.normalize('NFKC',text)`|返回规范化字符串|
|正则替换|`re.sub(pattern,repl,text)`|返回新字符串|
|空白折叠|`' '.join(text.split())`|返回单空格文本|
|句子切分|`nltk.sent_tokenize(text)`|返回句子列表|
|英文词元|`nltk.word_tokenize(text)`|返回 token 列表|
|中文分词|`jieba.lcut(text)`|返回词列表|
|spaCy 流水线|`nlp(text)`|返回 Doc|
|词形还原|`token.lemma_`|返回词元字符串|
|停用词|`token.is_stop`|返回布尔值|
|批量处理|`nlp.pipe(texts,batch_size=...)`|返回 Doc 迭代器|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import re, unicodedata
text="Ａ  data\n science! "
clean=" ".join(unicodedata.normalize("NFKC",text).split())
print(clean)
print(re.findall(r"\w+",clean))
# 期望输出:
# A data science!
# ['A', 'data', 'science']
```
## 传统特征与相似度（Traditional Features and Similarity）
稀疏特征是强基线，尤其适合中小规模分类与检索。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|词袋|`CountVectorizer(min_df=1,ngram_range=(1,1))`|返回稀疏计数矩阵|
|TF-IDF|`TfidfVectorizer(ngram_range=(1,2),sublinear_tf=False)`|返回稀疏权重矩阵|
|哈希特征|`HashingVectorizer(n_features=2**20)`|无状态固定维稀疏矩阵|
|字符 n-gram|`TfidfVectorizer(analyzer='char_wb',ngram_range=(3,5))`|返回字符特征|
|余弦相似|`cosine_similarity(A,B)`|返回两两相似矩阵|
|欧氏距离|`pairwise_distances(A,B,metric='euclidean')`|返回距离矩阵|
|BM25|`BM25Okapi(corpus_tokens)`|返回词法相关性对象|
|倒排索引|`term -> sorted document ids`|返回按词查文档的数据结构|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
X=TfidfVectorizer().fit_transform(["deep learning","deep model","database"] )
print(X.shape)
print(round(cosine_similarity(X[:1],X[1:2])[0,0],3))
# 期望输出:
# (3, 4)
# 0.366
```
## 评估与错误分析（Evaluation and Error Analysis）
切分单位应与真实泛化边界一致，例如按用户、文档、时间或来源分组。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|分类 F1|`f1_score(y,p,average='macro')`|返回宏平均 F1|
|序列准确率|`逐 token 正确数/有效 token 数`|返回比例并忽略 padding|
|NER span F1|`seqeval.metrics.f1_score(y,p)`|按实体边界与类型返回 F1|
|BLEU|`sacrebleu.corpus_bleu(hypotheses,references)`|返回机器翻译分数|
|ROUGE|`evaluate.load('rouge').compute(...)`|返回重叠召回指标|
|困惑度|`exp(mean token NLL)`|返回正数，越低通常越好|
|编辑距离|`rapidfuzz.distance.Levenshtein.distance(a,b)`|返回编辑次数|
|分层报告|`按长度、类别、来源和置信度分桶`|返回每桶指标|
|混淆样本|`筛选 y!=pred 并保留概率`|返回错误分析表|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
from sklearn.metrics import f1_score
y=[0,0,1,2]; p=[0,1,1,2]
print(round(f1_score(y,p,average="macro"),3))
# 期望输出:
# 0.778
```
## 高频工作模式（Common Workflows）
- **基线（Baseline）**：先用最小可解释模型和极小数据过拟合测试，确认数据、损失和指标链路正确。
- **训练（Training）**：固定随机种子，记录数据版本、超参数、权重、指标与环境。
- **验证（Validation）**：验证集只用于选型与调参，最终测试集只评估一次。
- **推理（Inference）**：冻结随机行为、关闭梯度、统一预处理并验证输出 schema。
- **性能（Performance）**：先测量数据加载、计算、通信与后处理，再针对瓶颈优化。
- **上线（Production）**：增加输入校验、超时、批处理、监控、回滚和隐私保护。
## 常见错误与排查（Common Errors and Troubleshooting）
- **维度错误**：记录每个关键张量的 `shape/dtype/device`，按模块契约逐层核对。
- **训练不稳定**：检查输入归一化、标签范围、损失配对、学习率、梯度范数和 NaN/Inf。
- **指标虚高**：排查数据泄漏、重复样本、错误划分、阈值选择和只看单一平均指标。
- **推理漂移**：确保训练与服务使用同一 tokenizer、类别表、归一化统计和模型版本。
- **资源泄漏**：及时关闭文件、图像、客户端与进程；长任务持续观察 CPU/GPU/内存。
- **版本漂移**：固定主要依赖并以官方迁移说明处理弃用，不静默忽略警告。
## 相关详细笔记（Detailed Notes）
- [[06-正则表达式（Regular Expressions）]]
- [[01-自然语言处理概览（NLP Overview）]]
- [[02-NLP 核心模型图解（NLP Core Model Visual Guide）]]
- [[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）]]
- [[02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）]]
- [[03-Seq2Seq 与注意力机制（Seq2Seq and Attention）]]
- [[04-自注意力机制（Self-Attention）]]
- [[05-HMM 与 CRF 序列标注（HMM and CRF Sequence Labeling）]]
- [[01-Transformer 架构与注意力（Transformer Architecture and Attention）]]
- [[02-Transformer PyTorch 实现（Transformer PyTorch Implementation）]]
- [[03-FastText 文本分类与词向量（FastText Classification and Embeddings）]]
- [[04-NLP 迁移学习（NLP Transfer Learning）]]
- [[05-BERT 原理与模型族（BERT Principles and Family）]]
- [[06-ELMo 上下文词表示（ELMo Contextual Embeddings）]]
- [[07-GPT 模型演进（GPT Model Evolution）]]
- [[08-BERT、GPT 与 ELMo 对比（BERT, GPT, and ELMo Comparison）]]
- [[01-大语言模型术语、生命周期与工程生态（LLM Terminology and Lifecycle）]]
- [[01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）]]
- [[02-输出解析、提示词与 LCEL 链（Output Parsing, Prompts, and LCEL Chains）]]
- [[03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）]]
- [[04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）]]
- [[05-LangChain Agent 与本地工具（Agents and Local Tools）]]
- [[06-MCP 工具集成（MCP Tool Integration）]]
- [[07-Agent 记忆与中间件（Agent Memory and Middleware）]]
- [[01-NLP 预处理与信息抽取（NLP Preprocessing and Information Extraction）]]
- [[02-Jieba 中文分词、词典、关键词与词性（Jieba Tokenization and Keywords）]]
- [[03-Gensim 词典、词袋与 TF-IDF（Gensim Dictionary, BoW, and TF-IDF）]]
- [[04-HanLP 本地推理与 RESTful 调用（HanLP Native and RESTful Usage）]]
- [[05-Hugging Face Transformers（Hugging Face Transformers）]]
- [[06-Hugging Face Tokenizer 与 Datasets 数据管线（Hugging Face Tokenizer and Datasets Pipeline）]]
- [[07-子词分词算法：BPE、WordPiece 与 Unigram（Subword Tokenization Algorithms）]]
- [[01-文本语料探索性分析（Exploratory Text Corpus Analysis）]]
- [[02-N-Gram、长度规范与文本数据增强（N-Gram and Text Augmentation）]]
- [[03-NLP 标准数据集与任务基准（NLP Datasets and Benchmarks）]]
- [[01-新闻主题分类实践（News Topic Classification Practice）]]
- [[02-RNN 人名语言分类器（RNN Name Language Classifier）]]
- [[03-注意力 Seq2Seq 机器翻译（Attention Seq2Seq Translation）]]
- [[04-Transformer 机器翻译（Transformer Machine Translation）]]
- [[05-Transformer 语言模型（Transformer Language Model）]]
- [[06-预训练模型迁移学习实践（Pretrained Model Transfer Learning Practice）]]
- [[07-电商评论情感分类演进（E-commerce Review Sentiment Classification Evolution）]]
## 官方参考（Official References）
- [Hugging Face Tokenizer 文档](https://huggingface.co/docs/transformers/main_classes/tokenizer)
- [Jieba 官方仓库](https://github.com/fxsjy/jieba)
- [Gensim 官方文档](https://radimrehurek.com/gensim/)
- [HanLP 安装文档](https://hanlp.hankcs.com/docs/install.html)
- [spaCy 使用文档](https://spacy.io/usage)
- [fastText Python 模块文档](https://fasttext.cc/docs/en/python-module.html)
- [WordCloud 官方仓库](https://github.com/amueller/word_cloud)
