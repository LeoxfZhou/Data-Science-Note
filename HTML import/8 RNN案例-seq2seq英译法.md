    

 

[[#_1|跳转至]]

[![logo](../img/logo.png)](.. "自然语言处理基础V4.0")

自然语言处理基础V4.0

8 RNN案例 seq2seq英译法

正在初始化搜索引擎

![logo](../assets/images/logo.svg)

 [![logo](../img/logo.png)](.. "自然语言处理基础V4.0")自然语言处理基础V4.0

- [ ]  第一章 自然语言处理入门
    
	第一章 自然语言处理入门
    
	- [1 自然语言处理入门](../01_mkdocs_NLP/1_%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86%E5%85%A5%E9%97%A8.html)
    
- [ ]  第二章 文本预处理
    
	第二章 文本预处理
    
	- [1 认识文本预处理](../02_mkdocs_preprocess/1%20%E8%AE%A4%E8%AF%86%E6%96%87%E6%9C%AC%E9%A2%84%E5%A4%84%E7%90%86.html)
	- [2 文本处理的基本方法](../02_mkdocs_preprocess/2%20%E6%96%87%E6%9C%AC%E5%A4%84%E7%90%86%E7%9A%84%E5%9F%BA%E6%9C%AC%E6%96%B9%E6%B3%95.html)
	- [3 文本张量表示方法](../02_mkdocs_preprocess/3%20%E6%96%87%E6%9C%AC%E5%BC%A0%E9%87%8F%E8%A1%A8%E7%A4%BA%E6%96%B9%E6%B3%95.html)
	- [4 文本数据分析](../02_mkdocs_preprocess/4%20%E6%96%87%E6%9C%AC%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90.html)
	- [5 文本特征处理](../02_mkdocs_preprocess/5%20%E6%96%87%E6%9C%AC%E7%89%B9%E5%BE%81%E5%A4%84%E7%90%86.html)
	- [6 文本数据增强](../02_mkdocs_preprocess/6%20%E6%96%87%E6%9C%AC%E6%95%B0%E6%8D%AE%E5%A2%9E%E5%BC%BA.html)
	- [7 jieba词性对照表](../02_mkdocs_preprocess/7%20jieba%E8%AF%8D%E6%80%A7%E5%AF%B9%E7%85%A7%E8%A1%A8.html)
    
- [x]  第三章 RNN及其变体
    
	第三章 RNN及其变体
    
	- [1 认识RNN模型](1%20%E8%AE%A4%E8%AF%86RNN%E6%A8%A1%E5%9E%8B.html)
	- [2 传统RNN模型](2%20%E4%BC%A0%E7%BB%9FRNN%E6%A8%A1%E5%9E%8B.html)
	- [3 LSTM模型](3%20LSTM%E6%A8%A1%E5%9E%8B.html)
	- [4 GRU模型](4%20GRU%E6%A8%A1%E5%9E%8B.html)
	- [5 RNN案例 人名分类器](5%20RNN%E6%A1%88%E4%BE%8B-%E4%BA%BA%E5%90%8D%E5%88%86%E7%B1%BB%E5%99%A8.html)
	- [6 注意力机制介绍1](6%20%E6%B3%A8%E6%84%8F%E5%8A%9B%E6%9C%BA%E5%88%B6%E4%BB%8B%E7%BB%8D1.html)
	- [7 注意力机制介绍2](7%20%E6%B3%A8%E6%84%8F%E5%8A%9B%E6%9C%BA%E5%88%B6%E4%BB%8B%E7%BB%8D2.html)
	- [ ]  8 RNN案例 seq2seq英译法 [8 RNN案例 seq2seq英译法](8%20RNN%E6%A1%88%E4%BE%8B-seq2seq%E8%8B%B1%E8%AF%91%E6%B3%95.html)
        
		目录
        
		- [[#_1|学习目标]]
		- [[#1-seq2seq|1 seq2seq介绍]]
            
			- [[#11-seq2seq|1.1 seq2seq模型架构]]
            
		- [[#2|2 数据集介绍]]
		- [[#3|3 案例步骤]]
            
			- [[#1|1 导入工具包和工具函数]]
			- [[#2_1|2 数据预处理]]
                
				- [[#1_1|1 清洗文本和构建文本字典]]
				- [[#2_2|2 构建数据源对象]]
				- [[#3_1|3 构建数据迭代器]]
                
			- [[#3-gru|3 构建基于GRU的编码器和解码器]]
                
				- [[#1-gru|1 构建基于GRU的编码器]]
				- [[#2-gru|2 构建基于GRU的解码器]]
				- [[#3-gruattention|3 构建基于GRU和Attention的解码器]]
                
			- [[#4|4 构建模型训练函数, 并进行训练]]
                
				- [[#1-teacher_forcing|1 teacher_forcing介绍]]
				- [[#2-teacher_forcing|2 teacher_forcing的作用]]
				- [[#3_2|3 构建内部迭代训练函数]]
				- [[#4_1|4 构建模型训练函数]]
				- [[#5|5 损失曲线分析]]
                
			- [[#5_1|5 构建模型评估函数并测试]]
                
				- [[#1_2|1 构建模型评估函数]]
				- [[#2_3|2 模型评估函数调用]]
				- [[#3-attention|3 Attention张量制图]]
                
            
		- [[#4_2|4 小结]]
        
    
- [ ]  第四章 Transformer
    
	第四章 Transformer
    
	- [1 Transformer背景介绍](../04_mkdocs_transformer/1%20Transformer%E8%83%8C%E6%99%AF%E4%BB%8B%E7%BB%8D.html)
	- [2 认识Transformer架构](../04_mkdocs_transformer/2%20%E8%AE%A4%E8%AF%86Transformer%E6%9E%B6%E6%9E%84.html)
	- [3 输入部分实现](../04_mkdocs_transformer/3%20%E8%BE%93%E5%85%A5%E9%83%A8%E5%88%86%E5%AE%9E%E7%8E%B0.html)
	- [4 编码器部分实现](../04_mkdocs_transformer/4%20%E7%BC%96%E7%A0%81%E5%99%A8%E9%83%A8%E5%88%86%E5%AE%9E%E7%8E%B0.html)
	- [5 解码器部分实现](../04_mkdocs_transformer/5%20%E8%A7%A3%E7%A0%81%E5%99%A8%E9%83%A8%E5%88%86%E5%AE%9E%E7%8E%B0.html)
	- [6 输出部分实现](../04_mkdocs_transformer/6%20%E8%BE%93%E5%87%BA%E9%83%A8%E5%88%86%E5%AE%9E%E7%8E%B0.html)
	- [7 模型构建](../04_mkdocs_transformer/7%20%E6%A8%A1%E5%9E%8B%E6%9E%84%E5%BB%BA.html)
    
- [ ]  第五章 迁移学习
    
	第五章 迁移学习
    
	- [1 fasttext工具介绍](../05_mkdocs_translearning/1%20fasttext%E5%B7%A5%E5%85%B7%E4%BB%8B%E7%BB%8D.html)
	- [2 fasttext模型架构](../05_mkdocs_translearning/2%20fasttext%E6%A8%A1%E5%9E%8B%E6%9E%B6%E6%9E%84.html)
	- [3 fasttext文本分类](../05_mkdocs_translearning/3%20fasttext%E6%96%87%E6%9C%AC%E5%88%86%E7%B1%BB.html)
	- [4 训练词向量](../05_mkdocs_translearning/4%20%E8%AE%AD%E7%BB%83%E8%AF%8D%E5%90%91%E9%87%8F.html)
	- [5 词向量迁移](../05_mkdocs_translearning/5%20%E8%AF%8D%E5%90%91%E9%87%8F%E8%BF%81%E7%A7%BB.html)
	- [6 迁移学习概念](../05_mkdocs_translearning/6%20%E8%BF%81%E7%A7%BB%E5%AD%A6%E4%B9%A0%E6%A6%82%E5%BF%B5.html)
	- [7 NLP中的常用预训练模型](../05_mkdocs_translearning/7%20NLP%E4%B8%AD%E7%9A%84%E5%B8%B8%E7%94%A8%E9%A2%84%E8%AE%AD%E7%BB%83%E6%A8%A1%E5%9E%8B.html)
	- [8 Transformers库使用](../05_mkdocs_translearning/8%20Transformers%E5%BA%93%E4%BD%BF%E7%94%A8.html)
	- [9 迁移学习实践](../05_mkdocs_translearning/9%20%E8%BF%81%E7%A7%BB%E5%AD%A6%E4%B9%A0%E5%AE%9E%E8%B7%B5.html)
	- [10 NLP中的标准数据集(拓展资料)](../05_mkdocs_translearning/10%20NLP%E4%B8%AD%E7%9A%84%E6%A0%87%E5%87%86%E6%95%B0%E6%8D%AE%E9%9B%86%28%E6%8B%93%E5%B1%95%E8%B5%84%E6%96%99%29.html)
    
- [ ]  第六章 Bert系列模型
    
	第六章 Bert系列模型
    
	- [1 BERT模型介绍](../06_mkdocs_bert_pretrained_model/1%20BERT%E6%A8%A1%E5%9E%8B%E4%BB%8B%E7%BB%8D.html)
	- [2 BERT模型特点](../06_mkdocs_bert_pretrained_model/2%20BERT%E6%A8%A1%E5%9E%8B%E7%89%B9%E7%82%B9.html)
	- [3 BERT系列模型介绍](../06_mkdocs_bert_pretrained_model/3%20BERT%E7%B3%BB%E5%88%97%E6%A8%A1%E5%9E%8B%E4%BB%8B%E7%BB%8D.html)
	- [4 ELMo模型介绍](../06_mkdocs_bert_pretrained_model/4%20ELMo%E6%A8%A1%E5%9E%8B%E4%BB%8B%E7%BB%8D.html)
	- [5 GPT模型介绍](../06_mkdocs_bert_pretrained_model/5%20GPT%E6%A8%A1%E5%9E%8B%E4%BB%8B%E7%BB%8D.html)
	- [6 BERT GPT ELMo模型的对比](../06_mkdocs_bert_pretrained_model/6%20BERT%20GPT%20ELMo%E6%A8%A1%E5%9E%8B%E7%9A%84%E5%AF%B9%E6%AF%94.html)
    
- [ ]  第七章 Transformer精选问答(拓展资料)
    
	第七章 Transformer精选问答(拓展资料)
    
	- [1 Transformer 各子模块作用](../07_mkdocs_review_model/1%20Transformer%20%E5%90%84%E5%AD%90%E6%A8%A1%E5%9D%97%E4%BD%9C%E7%94%A8.html)
	- [2 Transformer Decoder模块](../07_mkdocs_review_model/2%20Transformer%20Decoder%E6%A8%A1%E5%9D%97.html)
	- [3 Self attention机制详解](../07_mkdocs_review_model/3%20Self-attention%E6%9C%BA%E5%88%B6%E8%AF%A6%E8%A7%A3.html)
	- [4 Multi head Attention详解](../07_mkdocs_review_model/4%20Multi-head%20Attention%E8%AF%A6%E8%A7%A3.html)
	- [5 Transformer优势](../07_mkdocs_review_model/5%20Transformer%E4%BC%98%E5%8A%BF.html)
    

目录

- [[#_1|学习目标]]
- [[#1-seq2seq|1 seq2seq介绍]]
    
	- [[#11-seq2seq|1.1 seq2seq模型架构]]
    
- [[#2|2 数据集介绍]]
- [[#3|3 案例步骤]]
    
	- [[#1|1 导入工具包和工具函数]]
	- [[#2_1|2 数据预处理]]
        
		- [[#1_1|1 清洗文本和构建文本字典]]
		- [[#2_2|2 构建数据源对象]]
		- [[#3_1|3 构建数据迭代器]]
        
	- [[#3-gru|3 构建基于GRU的编码器和解码器]]
        
		- [[#1-gru|1 构建基于GRU的编码器]]
		- [[#2-gru|2 构建基于GRU的解码器]]
		- [[#3-gruattention|3 构建基于GRU和Attention的解码器]]
        
	- [[#4|4 构建模型训练函数, 并进行训练]]
        
		- [[#1-teacher_forcing|1 teacher_forcing介绍]]
		- [[#2-teacher_forcing|2 teacher_forcing的作用]]
		- [[#3_2|3 构建内部迭代训练函数]]
		- [[#4_1|4 构建模型训练函数]]
		- [[#5|5 损失曲线分析]]
        
	- [[#5_1|5 构建模型评估函数并测试]]
        
		- [[#1_2|1 构建模型评估函数]]
		- [[#2_3|2 模型评估函数调用]]
		- [[#3-attention|3 Attention张量制图]]
        
    
- [[#4_2|4 小结]]

# 8 RNN案例 seq2seq英译法

### 学习目标[[#_1|¶]]

- 更深一步了解seq2seq模型架构和翻译数据集
- 掌握使用基于GRU的seq2seq模型架构实现翻译的过程
- 掌握Attention机制在解码器端的实现过程

## 1 seq2seq介绍[[#1-seq2seq|¶]]

### 1.1 seq2seq模型架构[[#11-seq2seq|¶]]

![[s2s.png]]

- seq2seq模型架构分析:
    
- seq2seq模型架构包括三部分，分别是encoder(编码器)、decoder(解码器)、中间语义张量c。其中编码器和解码器的内部实现都使用了GRU模型
    
- 图中表示的是一个中文到英文的翻译：欢迎 来 北京 → welcome to BeiJing。编码器首先处理中文输入"欢迎 来 北京"，通过GRU模型获得每个时间步的输出张量，最后将它们拼接成一个中间语义张量c；接着解码器将使用这个中间语义张量c以及每一个时间步的隐层张量, 逐个生成对应的翻译语言
- 我们的案例通过英译法来讲解seq2seq设计与实现。

## 2 数据集介绍[[#2|¶]]

`# 数据集在虚拟机/root/data/下 - data/         - eng-fra-v2.txt`  

`i am from brazil .  je viens du bresil . i am from france .  je viens de france . i am from russia .  je viens de russie . i am frying fish .  je fais frire du poisson . i am not kidding .  je ne blague pas . i am on duty now .  maintenant je suis en service . i am on duty now .  je suis actuellement en service . i am only joking .  je ne fais que blaguer . i am out of time .  je suis a court de temps . i am out of work .  je suis au chomage . i am out of work .  je suis sans travail . i am paid weekly .  je suis payee a la semaine . i am pretty sure .  je suis relativement sur . i am truly sorry .  je suis vraiment desole . i am truly sorry .  je suis vraiment desolee .`

## 3 案例步骤[[#3|¶]]

基于GRU的seq2seq模型架构实现翻译的过程:

- 第一步: 导入工具包和工具函数
- 第二步: 对持久化文件中数据进行处理, 以满足模型训练要求
- 第三步: 构建基于GRU的编码器和解码器
- 第四步: 构建模型训练函数, 并进行训练
- 第五步: 构建模型评估函数, 并进行测试以及Attention效果分析

### 1 导入工具包和工具函数[[#1|¶]]

`# 用于正则表达式 import re # 用于构建网络结构和函数的torch工具包 import torch import torch.nn as nn import torch.nn.functional as F from torch.utils.data import Dataset, DataLoader # torch中预定义的优化方法工具包 import torch.optim as optim import time # 用于随机生成数据 import random import matplotlib.pyplot as plt  # 设备选择, 我们可以选择在cuda或者cpu上运行你的代码 device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # 起始标志 SOS_token = 0 # 结束标志 EOS_token = 1 # 最大句子长度不能超过10个 (包含标点) MAX_LENGTH = 10 # 数据文件路径 data_path = './data/eng-fra-v2.txt'  # 文本清洗工具函数 def normalizeString(s):     """字符串规范化函数, 参数s代表传入的字符串"""     s = s.lower().strip()     # 在.!?前加一个空格  这里的\1表示第一个分组   正则中的\num     s = re.sub(r"([.!?])", r" \1", s)     # s = re.sub(r"([.!?])", r" ", s)     # 使用正则表达式将字符串中 不是 大小写字母和正常标点的都替换成空格     s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)     return s`

### 2 数据预处理[[#2_1|¶]]

对持久化文件中数据进行处理, 以满足模型训练要求

#### 1 清洗文本和构建文本字典[[#1_1|¶]]

> - 清洗文本和构建文本字典思路分析

`# my_getdata() 清洗文本构建字典思路分析 # 1 按行读文件 open().read().strip().split(\n) my_lines # 2 按行清洗文本 构建语言对 my_pairs[] tmppair[] # 2-1格式 [['英文', '法文'], ['英文', '法文'], ['英文', '法文'], ['英文', '法文']....] # 2-2调用清洗文本工具函数normalizeString(s) # 3 遍历语言对 构建英语单词字典 法语单词字典 my_pairs->pair->pair[0].split(' ') pair[1].split(' ')->word # 3-1 english_word2index english_word_n french_word2index french_word_n # 其中 english_word2index = {0: "SOS", 1: "EOS"}  english_word_n=2 # 3-2 english_index2word french_index2word # 4 返回数据的7个结果 # english_word2index, english_index2word, english_word_n, # french_word2index, french_index2word, french_word_n, my_pairs`

> - 代码实现

`def my_getdata():      # 1 按行读文件 open().read().strip().split(\n)     my_lines = open(data_path, encoding='utf-8').read().strip().split('\n')     print('my_lines--->', len(my_lines))      # 2 按行清洗文本 构建语言对 my_pairs     # 格式 [['英文句子', '法文句子'], ['英文句子', '法文句子'], ['英文句子', '法文句子'], ... ]     # tmp_pair, my_pairs = [], []     # for l in my_lines:     #     for s in l.split('\t'):     #         tmp_pair.append(normalizeString(s))     #     my_pairs.append(tmp_pair)     #     tmp_pair = []     my_pairs = [[normalizeString(s) for s in l.split('\t')] for l in my_lines]     print('len(pairs)--->', len(my_pairs))      # 打印前4条数据     print(my_pairs[:4])      # 打印第8000条的英文 法文数据     print('my_pairs[8000][0]--->', my_pairs[8000][0])     print('my_pairs[8000][1]--->', my_pairs[8000][1])      # 3 遍历语言对 构建英语单词字典 法语单词字典     # 3-1 english_word2index english_word_n french_word2index french_word_n     english_word2index = {"SOS": 0, "EOS": 1}     english_word_n = 2      french_word2index = {"SOS": 0, "EOS": 1}     french_word_n = 2      # 遍历语言对 获取英语单词字典 法语单词字典     for pair in my_pairs:        for word in pair[0].split(' '):            if word not in english_word2index:                english_word2index[word] = english_word_n                english_word_n += 1         for word in pair[1].split(' '):            if word not in french_word2index:                french_word2index[word] = french_word_n                french_word_n += 1      # 3-2 english_index2word french_index2word     english_index2word = {v:k for k, v in english_word2index.items()}     french_index2word = {v:k for k, v in french_word2index.items()}      print('len(english_word2index)-->', len(english_word2index))     print('len(french_word2index)-->', len(french_word2index))     print('english_word_n--->', english_word_n, 'french_word_n-->', french_word_n)      return english_word2index, english_index2word, english_word_n, french_word2index, french_index2word, french_word_n, my_pairs`

> - 调用

`# 全局函数 获取英语单词字典 法语单词字典 语言对列表my_pairs english_word2index, english_index2word, english_word_n, \     french_word2index, french_index2word, french_word_n, \     my_pairs = my_getdata()`

> - 输出效果:

`my_lines---> 10599 len(pairs)---> 10599 [['i m .', 'j ai ans .'], ['i m ok .', 'je vais bien .'], ['i m ok .', 'ca va .'], ['i m fat .', 'je suis gras .']] my_pairs[8000][0]---> they re in the science lab . my_pairs[8000][1]---> elles sont dans le laboratoire de sciences . len(english_word2index)--> 2803 len(french_word2index)--> 4345 english_word_n---> 2803 french_word_n--> 4345 x.shape torch.Size([1, 9]) tensor([[ 75,  40, 102, 103, 677,  42,  21,   4,   1]]) y.shape torch.Size([1, 7]) tensor([[ 119,   25,  164,  165, 3222,    5,    1]]) x.shape torch.Size([1, 5]) tensor([[14, 15, 44,  4,  1]]) y.shape torch.Size([1, 5]) tensor([[24, 25, 62,  5,  1]]) x.shape torch.Size([1, 8]) tensor([[   2,    3,  147,   61,  532, 1143,    4,    1]]) y.shape torch.Size([1, 7]) tensor([[  6, 297,   7, 246, 102,   5,   1]])`

#### 2 构建数据源对象[[#2_2|¶]]

`# 原始数据 -> 数据源MyPairsDataset --> 数据迭代器DataLoader # 构造数据源 MyPairsDataset，把语料xy 文本数值化 再转成tensor_x tensor_y # 1 __init__(self, my_pairs)函数 设置self.my_pairs 条目数self.sample_len # 2 __len__(self)函数  获取样本条数 # 3 __getitem__(self, index)函数 获取第几条样本数据 #       按索引 获取数据样本 x y #       样本x 文本数值化   word2id  x.append(EOS_token) #       样本y 文本数值化   word2id  y.append(EOS_token) #       返回tensor_x, tensor_y  class MyPairsDataset(Dataset):     def __init__(self, my_pairs):         # 样本x         self.my_pairs = my_pairs          # 样本条目数         self.sample_len = len(my_pairs)      # 获取样本条数     def __len__(self):         return self.sample_len      # 获取第几条 样本数据     def __getitem__(self, index):          # 对index异常值进行修正 [0, self.sample_len-1]         index = min(max(index, 0), self.sample_len-1)          # 按索引获取 数据样本 x y         x = self.my_pairs[index][0]         y = self.my_pairs[index][1]          # 样本x 文本数值化         x = [english_word2index[word] for word in x.split(' ')]         x.append(EOS_token)         tensor_x = torch.tensor(x, dtype=torch.long, device=device)          # 样本y 文本数值化         y = [french_word2index[word] for word in y.split(' ')]         y.append(EOS_token)         tensor_y = torch.tensor(y, dtype=torch.long, device=device)         # 注意 tensor_x tensor_y都是一维数组，通过DataLoader拿出数据是二维数据         # print('tensor_y.shape===>', tensor_y.shape, tensor_y)          # 返回结果         return tensor_x, tensor_y`

#### 3 构建数据迭代器[[#3_1|¶]]

`def dm_test_MyPairsDataset():      # 1 实例化dataset对象     mypairsdataset = MyPairsDataset(my_pairs)      # 2 实例化dataloader     mydataloader = DataLoader(dataset=mypairsdataset, batch_size=1, shuffle=True)     for  i, (x, y) in enumerate (mydataloader):         print('x.shape', x.shape, x)         print('y.shape', y.shape, y)         if i == 1:             break`

> - 输出效果:

`x.shape torch.Size([1, 8]) tensor([[   2,   16,   33,  518,  589, 1460,    4,    1]]) y.shape torch.Size([1, 8]) tensor([[   6,   11,   52,  101, 1358,  964,    5,    1]]) x.shape torch.Size([1, 6]) tensor([[129,  78, 677, 429,   4,   1]]) y.shape torch.Size([1, 7]) tensor([[ 118,  214, 1073,  194,  778,    5,    1]])`

### 3 构建基于GRU的编码器和解码器[[#3-gru|¶]]

#### 1 构建基于GRU的编码器[[#1-gru|¶]]

- 编码器结构图:

![[encoder-network.png]]

> - 实现思路分析

`# EncoderRNN类 实现思路分析： # 1 init函数 定义2个层 self.embedding self.gru (batch_first=True) #    def __init__(self, input_size, hidden_size): # 2803 256  # 2 forward(input, hidden)函数，返回output, hidden #   数据经过词嵌入层 数据形状 [1,6] --> [1,6,256] #   数据经过gru层 形状变化 gru([1,6,256],[1,1,256]) --> [1,6,256] [1,1,256]  # 3 初始化隐藏层输入数据 inithidden() #   形状 torch.zeros(1, 1, self.hidden_size, device=device)`

> - 构建基于GRU的编码器

`class EncoderRNN(nn.Module):     def __init__(self, input_size, hidden_size):          # input_size 编码器 词嵌入层单词数 eg：2803         # hidden_size 编码器 词嵌入层每个单词的特征数 eg 256         super(EncoderRNN, self).__init__()         self.input_size = input_size         self.hidden_size = hidden_size          # 实例化nn.Embedding层         self.embedding = nn.Embedding(input_size, hidden_size)          # 实例化nn.GRU层 注意参数batch_first=True         self.gru = nn.GRU(hidden_size, hidden_size, batch_first=True)      def forward(self, input, hidden):          # 数据经过词嵌入层 数据形状 [1,6] --> [1,6,256]         output = self.embedding(input)          # 数据经过gru层 数据形状 gru([1,6,256],[1,1,256]) --> [1,6,256] [1,1,256]         output, hidden = self.gru(output, hidden)         return output, hidden      def inithidden(self):         # 将隐层张量初始化成为1x1xself.hidden_size大小的张量         return torch.zeros(1, 1, self.hidden_size, device=device)`

> - 调用

`def dm_test_EncoderRNN():      # 实例化dataset对象     mypairsdataset = MyPairsDataset(my_pairs)      # 实例化dataloader     mydataloader = DataLoader(dataset=mypairsdataset, batch_size=1, shuffle=True)      # 实例化模型     input_size = english_word_n     hidden_size = 256 #     my_encoderrnn = EncoderRNN(input_size, hidden_size)     print('my_encoderrnn模型结构--->', my_encoderrnn)      # 给encode模型喂数据     for  i, (x, y) in enumerate (mydataloader):          print('x.shape', x.shape, x)         print('y.shape', y.shape, y)          # 一次性的送数据         hidden = my_encoderrnn.inithidden()         encode_output_c, hidden = my_encoderrnn(x, hidden)         print('encode_output_c.shape--->', encode_output_c.shape, encode_output_c)          # 一个字符一个字符给为模型喂数据         hidden = my_encoderrnn.inithidden()         for i in range(x.shape[1]):             tmp = x[0][i].view(1,-1)             output, hidden = my_encoderrnn(tmp, hidden)          print('观察：最后一个时间步output输出是否相等') # hidden_size = 8 效果比较好         print('encode_output_c[0][-1]===>', encode_output_c[0][-1])         print('output===>', output)          break`

> - 输出效果:

`# 本输出效果为hidden_size = 8 x.shape torch.Size([1, 6]) tensor([[129, 124, 270, 558,   4,   1]]) y.shape torch.Size([1, 7]) tensor([[ 118,  214,  101, 1253, 1028,    5,    1]]) encode_output_c.shape---> torch.Size([1, 6, 8])  tensor([[[-0.0984,  0.4267, -0.2120,  0.0923,  0.1525, -0.0378,  0.2493,-0.2665],          [-0.1388,  0.5363, -0.4522, -0.2819, -0.2070,  0.0795,  0.6262, -0.2359],          [-0.4593,  0.2499,  0.1159,  0.3519, -0.0852, -0.3621,  0.1980, -0.1853],          [-0.4407,  0.1974,  0.6873, -0.0483, -0.2730, -0.2190,  0.0587, 0.2320],          [-0.6544,  0.1990,  0.7534, -0.2347, -0.0686, -0.5532,  0.0624, 0.4083],          [-0.2941, -0.0427,  0.1017, -0.1057,  0.1983, -0.1066,  0.0881, -0.3936]]], grad_fn=<TransposeBackward1>) 观察：最后一个时间步output输出是否相等 encode_output_c[0][-1]===> tensor([-0.2941, -0.0427,  0.1017, -0.1057,  0.1983, -0.1066,  0.0881, -0.3936],        grad_fn=<SelectBackward0>) output===> tensor([[[-0.2941, -0.0427,  0.1017, -0.1057,  0.1983, -0.1066,  0.0881,           -0.3936]]], grad_fn=<TransposeBackward1>)`

#### 2 构建基于GRU的解码器[[#2-gru|¶]]

- 解码器结构图:

![[decoder-network.png]]

> - 构建基于GRU的解码器实现思路分析

`# DecoderRNN 类 实现思路分析： # 解码器的作用：提取事物特征 进行分类（所以比 编码器 多了 线性层 和 softmax层） # 1 init函数 定义四个层 self.embedding self.gru self.out self.softmax=nn.LogSoftmax(dim=-1) #    def __init__(self, output_size, hidden_size): # 4345 256  # 2 forward(input, hidden)函数，返回output, hidden #   数据经过词嵌入层 数据形状 [1,1] --> [1,1,256] #   数据经过relu()层 output = F.relu(output) #   数据经过gru层 形状变化 gru([1,1,256],[1,1,256]) --> [1,1,256] [1,1,256] #   数据结果out层 形状变化 [1,1,256]->[1,256]-->[1,4345] #   返回 解码器分类output[1,4345]，最后隐层张量hidden[1,1,256]  # 3 初始化隐藏层输入数据 inithidden() #   形状 torch.zeros(1, 1, self.hidden_size, device=device)`

> - 编码实现

`class DecoderRNN(nn.Module):      def __init__(self, output_size, hidden_size):          # output_size 编码器 词嵌入层单词数 eg：4345         # hidden_size 编码器 词嵌入层每个单词的特征数 eg 256         super(DecoderRNN, self).__init__()         self.output_size = output_size         self.hidden_size = hidden_size          # 实例化词嵌入层         self.embedding = nn.Embedding(output_size, hidden_size)          # 实例化gru层，输入尺寸256 输出尺寸256         # 因解码器一个字符一个字符的解码 batch_first=True 意义不大         self.gru = nn.GRU(hidden_size, hidden_size, batch_first=True)          # 实例化线性输出层out 输入尺寸256 输出尺寸4345         self.out = nn.Linear(hidden_size, output_size)          # 实例化softomax层 数值归一化 以便分类         self.softmax = nn.LogSoftmax(dim=-1)      def forward(self, input, hidden):          # 数据经过词嵌入层         # 数据形状 [1,1] --> [1,1,256] or [1,6]--->[1,6,256]         output = self.embedding(input)          # 数据结果relu层使Embedding矩阵更稀疏，以防止过拟合         output = F.relu(output)          # 数据经过gru层         # 数据形状 gru([1,1,256],[1,1,256]) --> [1,1,256] [1,1,256]         output, hidden = self.gru(output, hidden)          # 数据经过softmax层 归一化         # 数据形状变化 [1,1,256]->[1,256] ---> [1,4345]         output = self.softmax(self.out(output[0]))         return output, hidden      def inithidden(self):          # 将隐层张量初始化成为1x1xself.hidden_size大小的张量         return torch.zeros(1, 1, self.hidden_size, device=device)`

> - 调用

`def dm03_test_DecoderRNN():      # 实例化dataset对象     mypairsdataset = MyPairsDataset(my_pairs)      # 实例化dataloader     mydataloader = DataLoader(dataset=mypairsdataset, batch_size=1, shuffle=True)      # 实例化模型     input_size = english_word_n     hidden_size = 256 # 观察结果数据 可使用8     my_encoderrnn = EncoderRNN(input_size, hidden_size)     print('my_encoderrnn模型结构--->', my_encoderrnn)      # 实例化模型     input_size = french_word_n     hidden_size = 256  # 观察结果数据 可使用8     my_decoderrnn = DecoderRNN(input_size, hidden_size)     print('my_decoderrnn模型结构--->', my_decoderrnn)      # 给模型喂数据 完整演示编码 解码流程     for i, (x, y) in enumerate (mydataloader):          print('x.shape', x.shape, x)         print('y.shape', y.shape, y)          # 1 编码：一次性的送数据         hidden = my_encoderrnn.inithidden()         encode_output_c, hidden = my_encoderrnn(x, hidden)         print('encode_output_c.shape--->', encode_output_c.shape, encode_output_c)          print('观察：最后一个时间步output输出') # hidden_size = 8 效果比较好         print('encode_output_c[0][-1]===>', encode_output_c[0][-1])          # 2 解码: 一个字符一个字符的解码         # 最后1个隐藏层的输出 作为 解码器的第1个时间步隐藏层输入         for i in range(y.shape[1]):             tmp = y[0][i].view(1, -1)             output, hidden = my_decoderrnn(tmp, hidden)             print('每个时间步解码出来4345种可能 output===>', output.shape)          break`

> - 输出效果

`my_encoderrnn模型结构---> EncoderRNN(   (embedding): Embedding(2803, 256)   (gru): GRU(256, 256, batch_first=True) ) my_decoderrnn模型结构---> DecoderRNN(   (embedding): Embedding(4345, 256)   (gru): GRU(256, 256, batch_first=True)   (out): Linear(in_features=256, out_features=4345, bias=True)   (softmax): LogSoftmax(dim=-1) ) x.shape torch.Size([1, 8]) tensor([[ 14,  40, 883, 677, 589, 609,   4,   1]]) y.shape torch.Size([1, 6]) tensor([[1358, 1125,  247, 2863,    5,    1]]) 每个时间步解码出来4345种可能 output===> torch.Size([1, 4345]) 每个时间步解码出来4345种可能 output===> torch.Size([1, 4345]) 每个时间步解码出来4345种可能 output===> torch.Size([1, 4345]) 每个时间步解码出来4345种可能 output===> torch.Size([1, 4345]) 每个时间步解码出来4345种可能 output===> torch.Size([1, 4345]) 每个时间步解码出来4345种可能 output===> torch.Size([1, 4345])`

#### 3 构建基于GRU和Attention的解码器[[#3-gruattention|¶]]

- 解码器结构图:

![[attention-decoder-network.png]]

> - 实现思路分析

`# 构建基于GRU和Attention的解码器 # AttnDecoderRNN 类 实现思路分析： # 1 init函数 定义六个层 #   self.embedding self.attn  self.attn_combine #   self.gru self.out self.softmax=nn.LogSoftmax(dim=-1) #   def __init__(self, output_size, hidden_size, dropout_p=0.1, max_length=MAX_LENGTH):: # 4345 256  # 2 forward(input, hidden, encoder_outputs)函数，返回output, hidden #   数据经过词嵌入层 数据形状 [1,1] --> [1,1,256] #   1 求查询张量q的注意力权重分布, attn_weights[1,10] #   2 求查询张量q的注意力结果表示 bmm运算, attn_applied[1,1,256] #   3 q 与 attn_applied 融合，经过层attn_combine 按照指定维度输出 output[1,1,256] #   数据经过relu()层 output = F.relu(output) #   数据经过gru层 形状变化 gru([1,1,256],[1,1,256]) --> [1,1,256] [1,1,256] #   返回 # 返回解码器分类output[1,4345]，最后隐层张量hidden[1,1,256] 注意力权重张量attn_weights[1,10]  # 3 初始化隐藏层输入数据 inithidden() #   形状 torch.zeros(1, 1, self.hidden_size, device=device)  # 相对传统RNN解码 AttnDecoderRNN类多了注意力机制,需要构建QKV # 1 在init函数中 (self, output_size, hidden_size, dropout_p=0.1, max_length=MAX_LENGTH)     # 增加层 self.attn  self.attn_combine  self.dropout # 2 增加函数 attentionQKV(self, Q, K, V) # 3 函数forward(self, input, hidden, encoder_outputs)     # encoder_outputs 每个时间步解码准备qkv 调用attentionQKV     # 函数返回值 output, hidden, attn_weights # 4 调用需要准备中间语义张量C encode_output_c`

> - 编码实现

`class AttnDecoderRNN(nn.Module):     def __init__(self, output_size, hidden_size, dropout_p=0.1, max_length=MAX_LENGTH):          # output_size   编码器 词嵌入层单词数 eg：4345         # hidden_size   编码器 词嵌入层每个单词的特征数 eg 256         # dropout_p     置零比率，默认0.1,         # max_length    最大长度10         super(AttnDecoderRNN, self).__init__()         self.output_size = output_size         self.hidden_size = hidden_size         self.dropout_p = dropout_p         self.max_length = max_length          # 定义nn.Embedding层 nn.Embedding(4345,256)         self.embedding = nn.Embedding(self.output_size, self.hidden_size)          # 定义线性层1：求q的注意力权重分布         self.attn = nn.Linear(self.hidden_size * 2, self.max_length)          # 定义线性层2：q+注意力结果表示融合后，在按照指定维度输出         self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)          # 定义dropout层         self.dropout = nn.Dropout(self.dropout_p)          # 定义gru层         self.gru = nn.GRU(self.hidden_size, self.hidden_size, batch_first=True)          # 定义out层 解码器按照类别进行输出(256,4345)         self.out = nn.Linear(self.hidden_size, self.output_size)          # 实例化softomax层 数值归一化 以便分类         self.softmax = nn.LogSoftmax(dim=-1)      def forward(self, input, hidden, encoder_outputs):         # input代表q [1,1] 二维数据 hidden代表k [1,1,256] encoder_outputs代表v [10,256]          # 数据经过词嵌入层         # 数据形状 [1,1] --> [1,1,256]         embedded = self.embedding(input)          # 使用dropout进行随机丢弃，防止过拟合         embedded = self.dropout(embedded)          # 1 求查询张量q的注意力权重分布, attn_weights[1,10]         attn_weights = F.softmax(             self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)          # 2 求查询张量q的注意力结果表示 bmm运算, attn_applied[1,1,256]         # [1,1,10],[1,10,256] ---> [1,1,256]         attn_applied = torch.bmm(attn_weights.unsqueeze(0), encoder_outputs.unsqueeze(0))          # 3 q 与 attn_applied 融合，再按照指定维度输出 output[1,1,256]         output = torch.cat((embedded[0], attn_applied[0]), 1)         output = self.attn_combine(output).unsqueeze(0)          # 查询张量q的注意力结果表示 使用relu激活         output = F.relu(output)          # 查询张量经过gru、softmax进行分类结果输出         # 数据形状[1,1,256],[1,1,256] --> [1,1,256], [1,1,256]         output, hidden = self.gru(output, hidden)         # 数据形状[1,1,256]->[1,256]->[1,4345]         output = self.softmax(self.out(output[0]))          # 返回解码器分类output[1,4345]，最后隐层张量hidden[1,1,256] 注意力权重张量attn_weights[1,10]         return output, hidden, attn_weights      def inithidden(self):         # 将隐层张量初始化成为1x1xself.hidden_size大小的张量         return torch.zeros(1, 1, self.hidden_size, device=device)`

> - 调用

`def dm_test_AttnDecoderRNN():     # 1 实例化 数据集对象     mypairsdataset = MyPairsDataset(my_pairs)      # 2 实例化 数据加载器对象     mydataloader = DataLoader(dataset=mypairsdataset, batch_size=1, shuffle=True)      #  实例化 编码器my_encoderrnn     my_encoderrnn = EncoderRNN(english_word_n, 256)      # 实例化 解码器DecoderRNN     my_attndecoderrnn = AttnDecoderRNN(french_word_n, 256)      # 3 遍历数据迭代器     for i, (x, y) in enumerate(mydataloader):          # 编码-方法1 一次性给模型送数据         hidden = my_encoderrnn.inithidden()         print('x--->', x.shape, x)         print('y--->', y.shape, y)          # [1, 6, 256], [1, 1, 256]) --> [1, 6, 256][1, 1, 256]         output, hidden = my_encoderrnn(x, hidden)         # print('output-->', output.shape, output)         # print('最后一个时间步取出output[0,-1]-->', output[0, -1].shape, output[0, -1])          # 中间语义张量C         encode_output_c = torch.zeros(MAX_LENGTH, my_encoderrnn.hidden_size,device=device)         for idx in range(output.shape[1]):             encode_output_c[idx] = output[0, idx]          # # 编码-方法2 一个字符一个字符给模型送数据         # hidden = my_encoderrnn.inithidden()         # for i in range(x.shape[1]):         #     tmp = x[0][i].view(1, -1)         #     # [1, 1, 256], [1, 1, 256]) --> [1, 1, 256][1, 1, 256]         #     output, hidden = my_encoderrnn(tmp, hidden)         # print('一个字符一个字符output', output.shape, output)          # 解码-必须一个字符一个字符的解码          for i in range(y.shape[1]):             tmp = y[0][i].view(1, -1)             output, hidden, attn_weights = my_attndecoderrnn(tmp, hidden, encode_output_c)             print('解码output.shape', output.shape )             print('解码hidden.shape', hidden.shape)             print('解码attn_weights.shape', attn_weights.shape)          break`

> - 输出效果:

`x---> torch.Size([1, 7]) tensor([[ 129,   78, 1873,  294, 1215,    4,    1]]) y---> torch.Size([1, 6]) tensor([[ 210, 3097,  248, 3095,    5,    1]]) 解码output.shape torch.Size([1, 4345]) 解码hidden.shape torch.Size([1, 1, 256]) 解码attn_weights.shape torch.Size([1, 10]) 解码output.shape torch.Size([1, 4345]) 解码hidden.shape torch.Size([1, 1, 256]) 解码attn_weights.shape torch.Size([1, 10]) 解码output.shape torch.Size([1, 4345]) 解码hidden.shape torch.Size([1, 1, 256]) 解码attn_weights.shape torch.Size([1, 10]) 解码output.shape torch.Size([1, 4345]) 解码hidden.shape torch.Size([1, 1, 256]) 解码attn_weights.shape torch.Size([1, 10]) 解码output.shape torch.Size([1, 4345]) 解码hidden.shape torch.Size([1, 1, 256]) 解码attn_weights.shape torch.Size([1, 10]) 解码output.shape torch.Size([1, 4345]) 解码hidden.shape torch.Size([1, 1, 256]) 解码attn_weights.shape torch.Size([1, 10])`

### 4 构建模型训练函数, 并进行训练[[#4|¶]]

#### 1 teacher_forcing介绍[[#1-teacher_forcing|¶]]

它是一种用于序列生成任务的训练技巧, 在seq2seq架构中, 根据循环神经网络理论，解码器每次应该使用上一步的结果作为输入的一部分, 但是训练过程中，一旦上一步的结果是错误的，就会导致这种错误被累积，无法达到训练效果, 因此，我们需要一种机制改变上一步出错的情况，因为训练时我们是已知正确的输出应该是什么，因此可以强制将上一步结果设置成正确的输出, 这种方式就叫做teacher_forcing.

#### 2 teacher_forcing的作用[[#2-teacher_forcing|¶]]

- 能够在训练的时候矫正模型的预测，避免在序列生成的过程中误差进一步放大.
    
- teacher_forcing能够极大的加快模型的收敛速度，令模型训练过程更快更平稳.
    

#### 3 构建内部迭代训练函数[[#3_2|¶]]

> - 模型训练参数

`# 模型训练参数 mylr = 1e-4 epochs = 2 # 设置teacher_forcing比率为0.5 teacher_forcing_ratio = 0.5 print_interval_num = 1000 plot_interval_num = 100`

> - 实现思路分析

`# 内部迭代训练函数Train_Iters # 1 编码 encode_output, encode_hidden = my_encoderrnn(x, encode_hidden) # 数据形状 eg [1,6],[1,1,256] --> [1,6,256],[1,1,256]  # 2 解码参数准备和解码 # 解码参数1 固定长度C encoder_outputs_c = torch.zeros(MAX_LENGTH, my_encoderrnn.hidden_size, device=device) # 解码参数2 decode_hidden # 解码参数3 input_y = torch.tensor([[SOS_token]], device=device) # 数据形状数据形状 [1,1],[1,1,256],[10,256] ---> [1,4345],[1,1,256],[1,10] # output_y, decode_hidden, attn_weight = my_attndecoderrnn(input_y, decode_hidden, encode_output_c) # 计算损失 target_y = y[0][idx].view(1) # 每个时间步处理 for idx in range(y_len): 处理三者之间关系input_y output_y target_y  # 3 训练策略 use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False # teacher_forcing  把样本真实值y作为下一次输入 input_y = y[0][idx].view(1, -1) # not teacher_forcing 把预测值y作为下一次输入 # topv,topi = output_y.topk(1) # if topi.squeeze().item() == EOS_token: break input_y = topi.detach()  # 4 其他 # 计算损失  # 梯度清零 # 反向传播  # 梯度更新 # 返回 损失列表myloss.item()/y_len`

> - 编码实现

`def Train_Iters(x, y, my_encoderrnn, my_attndecoderrnn, myadam_encode, myadam_decode, mycrossentropyloss):      # 1 编码 encode_output, encode_hidden = my_encoderrnn(x, encode_hidden)     encode_hidden = my_encoderrnn.inithidden()     encode_output, encode_hidden = my_encoderrnn(x, encode_hidden) # 一次性送数据     # [1,6],[1,1,256] --> [1,6,256],[1,1,256]      # 2 解码参数准备和解码     # 解码参数1 encode_output_c [10,256]     encode_output_c = torch.zeros(MAX_LENGTH, my_encoderrnn.hidden_size, device=device)     for idx in range(x.shape[1]):         encode_output_c[idx] = encode_output[0, idx]      # 解码参数2     decode_hidden = encode_hidden      # 解码参数3     input_y = torch.tensor([[SOS_token]], device=device)      myloss = 0.0     y_len = y.shape[1]      use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False     if use_teacher_forcing:         for idx in range(y_len):             # 数据形状数据形状 [1,1],[1,1,256],[10,256] ---> [1,4345],[1,1,256],[1,10]             output_y, decode_hidden, attn_weight = my_attndecoderrnn(input_y, decode_hidden, encode_output_c)             target_y = y[0][idx].view(1)             myloss = myloss + mycrossentropyloss(output_y, target_y)             input_y = y[0][idx].view(1, -1)     else:         for idx in range(y_len):             # 数据形状数据形状 [1,1],[1,1,256],[10,256] ---> [1,4345],[1,1,256],[1,10]             output_y, decode_hidden, attn_weight = my_attndecoderrnn(input_y, decode_hidden, encode_output_c)             target_y = y[0][idx].view(1)             myloss = myloss + mycrossentropyloss(output_y, target_y)              topv, topi = output_y.topk(1)             if topi.squeeze().item() == EOS_token:                 break             input_y = topi.detach()      # 梯度清零     myadam_encode.zero_grad()     myadam_decode.zero_grad()      # 反向传播     myloss.backward()      # 梯度更新     myadam_encode.step()     myadam_decode.step()      # 返回 损失列表myloss.item()/y_len     return myloss.item() / y_len`

#### 4 构建模型训练函数[[#4_1|¶]]

> - 实现思路分析

`# Train_seq2seq() 思路分析 # 实例化 mypairsdataset对象  实例化 mydataloader # 实例化编码器 my_encoderrnn 实例化解码器 my_attndecoderrnn # 实例化编码器优化器 myadam_encode 实例化解码器优化器 myadam_decode # 实例化损失函数 mycrossentropyloss = nn.NLLLoss() # 定义模型训练的参数 # epoches mylr=1e4 teacher_forcing_ratio print_interval_num  plot_interval_num (全局) # plot_loss_list = [] (返回) print_loss_total plot_loss_total starttime (每轮内部)  # 外层for循环 控制轮数 for epoch_idx in range(1, 1+epochs): # 内层for循环 控制迭代次数 # for item, (x, y) in enumerate(mydataloader, start=1): #   调用内部训练函数 Train_Iters(x, y, my_encoderrnn, my_attndecoderrnn, myadam_encode, myadam_decode, mycrossentropyloss) # 计算辅助信息 #   计算打印屏幕间隔损失-每隔1000次 # 计算画图间隔损失-每隔100次 #   每个轮次保存模型 torch.save(my_encoderrnn.state_dict(), PATH1) #   所有轮次训练完毕 画损失图 plt.figure() .plot(plot_loss_list) .save('x.png') .show()`

> - 编码实现

`def Train_seq2seq():      # 实例化 mypairsdataset对象  实例化 mydataloader     mypairsdataset = MyPairsDataset(my_pairs)     mydataloader = DataLoader(dataset=mypairsdataset, batch_size=1, shuffle=True)      # 实例化编码器 my_encoderrnn 实例化解码器 my_attndecoderrnn     my_encoderrnn = EncoderRNN(2803, 256)     my_attndecoderrnn = AttnDecoderRNN(output_size=4345, hidden_size=256, dropout_p=0.1, max_length=10)      # 实例化编码器优化器 myadam_encode 实例化解码器优化器 myadam_decode     myadam_encode = optim.Adam(my_encoderrnn.parameters(), lr=mylr)     myadam_decode = optim.Adam(my_attndecoderrnn.parameters(), lr=mylr)      # 实例化损失函数 mycrossentropyloss = nn.NLLLoss()     mycrossentropyloss = nn.NLLLoss()      # 定义模型训练的参数     plot_loss_list = []      # 外层for循环 控制轮数 for epoch_idx in range(1, 1+epochs):     for epoch_idx in range(1, 1+epochs):          print_loss_total, plot_loss_total = 0.0, 0.0         starttime = time.time()          # 内层for循环 控制迭代次数         for item, (x, y) in enumerate(mydataloader, start=1):             # 调用内部训练函数             myloss = Train_Iters(x, y, my_encoderrnn, my_attndecoderrnn, myadam_encode, myadam_decode, mycrossentropyloss)             print_loss_total += myloss             plot_loss_total += myloss              # 计算打印屏幕间隔损失-每隔1000次             if item % print_interval_num ==0 :                 print_loss_avg = print_loss_total / print_interval_num                 # 将总损失归0                 print_loss_total = 0                 # 打印日志，日志内容分别是：训练耗时，当前迭代步，当前进度百分比，当前平均损失                 print('轮次%d  损失%.6f 时间:%d' % (epoch_idx, print_loss_avg, time.time() - starttime))              # 计算画图间隔损失-每隔100次             if item % plot_interval_num == 0:                 # 通过总损失除以间隔得到平均损失                 plot_loss_avg = plot_loss_total / plot_interval_num                 # 将平均损失添加plot_loss_list列表中                 plot_loss_list.append(plot_loss_avg)                 # 总损失归0                 plot_loss_total = 0          # 每个轮次保存模型         torch.save(my_encoderrnn.state_dict(), './my_encoderrnn_%d.pth' % epoch_idx)         torch.save(my_attndecoderrnn.state_dict(), './my_attndecoderrnn_%d.pth' % epoch_idx)      # 所有轮次训练完毕 画损失图     plt.figure()     plt.plot(plot_loss_list)     plt.savefig('./s2sq_loss.png')     plt.show()      return plot_loss_list`

> - 输出效果

`轮次1  损失8.123402 时间:4 轮次1  损失6.658305 时间:8 轮次1  损失5.252497 时间:12 轮次1  损失4.906939 时间:16 轮次1  损失4.813769 时间:19 轮次1  损失4.780460 时间:23 轮次1  损失4.621599 时间:27 轮次1  损失4.487508 时间:31 轮次1  损失4.478538 时间:35 轮次1  损失4.245148 时间:39 轮次1  损失4.602579 时间:44 轮次1  损失4.256789 时间:48 轮次1  损失4.218111 时间:52 轮次1  损失4.393134 时间:56 轮次1  损失4.134959 时间:60 轮次1  损失4.164878 时间:63`

#### 5 损失曲线分析[[#5|¶]]

损失下降曲线

![[s2s_loss.png]]

> 一直下降的损失曲线, 说明模型正在收敛, 能够从数据中找到一些规律应用于数据.

### 5 构建模型评估函数并测试[[#5_1|¶]]

#### 1 构建模型评估函数[[#1_2|¶]]

`# 模型评估代码与模型预测代码类似，需要注意使用with torch.no_grad() # 模型预测时，第一个时间步使用SOS_token作为输入 后续时间步采用预测值作为输入，也就是自回归机制 def Seq2Seq_Evaluate(x, my_encoderrnn, my_attndecoderrnn):     with torch.no_grad():         # 1 编码：一次性的送数据         encode_hidden = my_encoderrnn.inithidden()         encode_output, encode_hidden = my_encoderrnn(x, encode_hidden)          # 2 解码参数准备         # 解码参数1 固定长度中间语义张量c         encoder_outputs_c = torch.zeros(MAX_LENGTH, my_encoderrnn.hidden_size, device=device)         x_len = x.shape[1]         for idx in range(x_len):             encoder_outputs_c[idx] = encode_output[0, idx]          # 解码参数2 最后1个隐藏层的输出 作为 解码器的第1个时间步隐藏层输入         decode_hidden = encode_hidden          # 解码参数3 解码器第一个时间步起始符         input_y = torch.tensor([[SOS_token]], device=device)          # 3 自回归方式解码         # 初始化预测的词汇列表         decoded_words = []         # 初始化attention张量         decoder_attentions = torch.zeros(MAX_LENGTH, MAX_LENGTH)         for idx in range(MAX_LENGTH): # note:MAX_LENGTH=10             output_y, decode_hidden, attn_weights = my_attndecoderrnn(input_y, decode_hidden, encoder_outputs_c)             # 预测值作为为下一次时间步的输入值             topv, topi = output_y.topk(1)             decoder_attentions[idx] = attn_weights              # 如果输出值是终止符，则循环停止             if topi.squeeze().item() == EOS_token:                 decoded_words.append('<EOS>')                 break             else:                 decoded_words.append(french_index2word[topi.item()])              # 将本次预测的索引赋值给 input_y，进行下一个时间步预测             input_y = topi.detach()          # 返回结果decoded_words， 注意力张量权重分布表(把没有用到的部分切掉)         return decoded_words, decoder_attentions[:idx + 1]`

#### 2 模型评估函数调用[[#2_3|¶]]

`# 加载模型 PATH1 = './gpumodel/my_encoderrnn.pth' PATH2 = './gpumodel/my_attndecoderrnn.pth' def dm_test_Seq2Seq_Evaluate():     # 实例化dataset对象     mypairsdataset = MyPairsDataset(my_pairs)     # 实例化dataloader     mydataloader = DataLoader(dataset=mypairsdataset, batch_size=1, shuffle=True)      # 实例化模型     input_size = english_word_n     hidden_size = 256  # 观察结果数据 可使用8     my_encoderrnn = EncoderRNN(input_size, hidden_size)     # my_encoderrnn.load_state_dict(torch.load(PATH1))     my_encoderrnn.load_state_dict(torch.load(PATH1, map_location=lambda storage, loc: storage), False)     print('my_encoderrnn模型结构--->', my_encoderrnn)      # 实例化模型     input_size = french_word_n     hidden_size = 256  # 观察结果数据 可使用8     my_attndecoderrnn = AttnDecoderRNN(input_size, hidden_size)     # my_attndecoderrnn.load_state_dict(torch.load(PATH2))     my_attndecoderrnn.load_state_dict(torch.load(PATH2, map_location=lambda storage, loc: storage), False)     print('my_decoderrnn模型结构--->', my_attndecoderrnn)      my_samplepairs =      [       ['i m impressed with your french .', 'je suis impressionne par votre francais .'],       ['i m more than a friend .', 'je suis plus qu une amie .'],       ['she is beautiful like her mother .', 'elle est belle comme sa mere .']     ]     print('my_samplepairs--->', len(my_samplepairs))      for index, pair in enumerate(my_samplepairs):         x = pair[0]         y = pair[1]          # 样本x 文本数值化         tmpx = [english_word2index[word] for word in x.split(' ')]         tmpx.append(EOS_token)         tensor_x = torch.tensor(tmpx, dtype=torch.long, device=device).view(1, -1)          # 模型预测         decoded_words, attentions = Seq2Seq_Evaluate(tensor_x, my_encoderrnn, my_attndecoderrnn)         # print('decoded_words->', decoded_words)         output_sentence = ' '.join(decoded_words)          print('\n')         print('>', x)         print('=', y)         print('<', output_sentence)`

> - 输出效果:

`> i m impressed with your french . = je suis impressionne par votre francais . < je suis impressionnee par votre francais . <EOS>  > i m more than a friend . = je suis plus qu une amie . < je suis plus qu une amie . <EOS>  > she is beautiful like her mother . = elle est belle comme sa mere . < elle est sa sa mere . <EOS>  > you re winning aren t you ? = vous gagnez n est ce pas ? < tu restez n est ce pas ? <EOS>  > he is angry with you . = il est en colere apres toi . < il est en colere apres toi . <EOS>  > you re very timid . = vous etes tres craintifs . < tu es tres craintive . <EOS>`

#### 3 Attention张量制图[[#3-attention|¶]]

`def dm_test_Attention():      # 实例化dataset对象     mypairsdataset = MyPairsDataset(my_pairs)     # 实例化dataloader     mydataloader = DataLoader(dataset=mypairsdataset, batch_size=1, shuffle=True)      # 实例化模型     input_size = english_word_n     hidden_size = 256  # 观察结果数据 可使用8     my_encoderrnn = EncoderRNN(input_size, hidden_size)     # my_encoderrnn.load_state_dict(torch.load(PATH1))     my_encoderrnn.load_state_dict(torch.load(PATH1, map_location=lambda storage, loc: storage), False)      # 实例化模型     input_size = french_word_n     hidden_size = 256  # 观察结果数据 可使用8     my_attndecoderrnn = AttnDecoderRNN(input_size, hidden_size)     # my_attndecoderrnn.load_state_dict(torch.load(PATH2))     my_attndecoderrnn.load_state_dict(torch.load(PATH2, map_location=lambda storage, loc: storage), False)      sentence = "we re both teachers ."     # 样本x 文本数值化     tmpx = [english_word2index[word] for word in sentence.split(' ')]     tmpx.append(EOS_token)     tensor_x = torch.tensor(tmpx, dtype=torch.long, device=device).view(1, -1)      # 模型预测     decoded_words, attentions = Seq2Seq_Evaluate(tensor_x, my_encoderrnn, my_attndecoderrnn)     print('decoded_words->', decoded_words)      # print('\n')     # print('英文', sentence)     # print('法文', output_sentence)      plt.matshow(attentions.numpy()) # 以矩阵列表的形式 显示     # 保存图像     plt.savefig("./s2s_attn.png")     plt.show()      print('attentions.numpy()--->\n', attentions.numpy())     print('attentions.size--->', attentions.size())`

> - 输出效果:

`decoded_words-> ['nous', 'sommes', 'toutes', 'deux', 'enseignantes', '.', '<EOS>']`

> - Attention可视化:

![[s2s_attn.png]]

- Attention图像的纵坐标代表输入的源语言各个词汇对应的索引, 0-6分别对应["we", "re", "both", "teachers", ".", ""], 纵坐标代表生成的目标语言各个词汇对应的索引, 0-7代表['nous', 'sommes', 'toutes', 'deux', 'enseignantes', '.', ''], 图中浅色小方块(颜色越浅说明影响越大)代表词汇之间的影响关系, 比如源语言的第1个词汇对生成目标语言的第1个词汇影响最大, 源语言的第4，5个词对生成目标语言的第5个词会影响最大, 通过这样的可视化图像, 我们可以知道Attention的效果好坏, 与我们人为去判定到底还有多大的差距. 进而衡量我们训练模型的可用性.

## 4 小结[[#4_2|¶]]

- seq2seq模型架构分析
	- seq2seq模型架构包括三部分，分别是encoder(编码器)、decoder(解码器)、中间语义张量c。其中编码器和解码器的内部实现都使用了GRU模型
- 基于GRU的seq2seq模型架构实现翻译的过程
	- 第一步: 导入必备的工具包和工具函数
	- 第二步: 对持久化文件中数据进行处理, 以满足模型训练要求
	- 第三步: 构建基于GRU的编码器和解码器
	- 第四步: 构建模型训练函数, 并进行训练
	- 第五步: 构建模型评估函数, 并进行测试以及Attention效果分析
- 第一步: 导入必备的工具包
	- python版本使用3.6.x, pytorch版本使用1.3.1
- 第二步: 对持久化文件中数据进行处理, 以满足模型训练要求
	- 清洗文本和构建文本字典、构建数据源、构建数据迭代器。文本处理的本质就是根据任务构建标签x、标签y
- 第三步: 构建基于GRU的编码器和解码器
	- 构建基于GRU的编码器
	- 构建基于GRU的解码器
	- 构建基于GRU和Attention的解码器
- 第四步: 构建模型训练函数, 并进行训练
	- 什么是teacher_forcing: 它是一种用于序列生成任务的训练技巧, 在seq2seq架构中, 根据循环神经网络理论，解码器每次应该使用上一步的结果作为输入的一部分, 但是训练过程中，一旦上一步的结果是错误的，就会导致这种错误被累积，无法达到训练效果, 因此，我们需要一种机制改变上一步出错的情况，因为训练时我们是已知正确的输出应该是什么，因此可以强制将上一步结果设置成正确的输出, 这种方式就叫做teacher_forcing
	- teacher_forcing的作用: 能够在训练的时候矫正模型的预测，避免在序列生成的过程中误差进一步放大. 另外, teacher_forcing能够极大的加快模型的收敛速度，令模型训练过程更快更平稳
	- 构建训练函数train
	- 调用训练函数并打印日志和制图
	- 损失曲线分析: 一直下降的损失曲线, 说明模型正在收敛, 能够从数据中找到一些规律应用于数据
- 第五步: 构建模型评估函数, 并进行测试以及Attention效果分析
	- 构建模型评估函数evaluate
	- 随机选择指定数量的数据进行评估
	- 进行了Attention可视化分析

[

上一页 7 注意力机制介绍2



](7%20%E6%B3%A8%E6%84%8F%E5%8A%9B%E6%9C%BA%E5%88%B6%E4%BB%8B%E7%BB%8D2.html)[

下一页 1 Transformer背景介绍

](../04_mkdocs_transformer/1%20Transformer%E8%83%8C%E6%99%AF%E4%BB%8B%E7%BB%8D.html)

Made with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)