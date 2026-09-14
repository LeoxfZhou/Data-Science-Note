---
title: "电商评论情感分类演进（E-commerce Review Sentiment Classification Evolution）"
tags:
  - data-science/nlp
  - sentiment-analysis
status: published
created: 2026-08-20
published_at: 2026-08-20
---
# 电商评论情感分类演进（E-commerce Review Sentiment Classification Evolution）
> [!tip] 大白话理解（Plain-language Intuition）
> 四个版本解决的是同一个二分类问题：先把评论变成数字，再让模型输出“正面”的分数。RNN 是基线；LSTM 和 GRU 用门控机制缓解长期依赖；BERT 直接复用预训练语义表示。按版本对照，能清楚看到“换模型”时哪些模块保持不变、哪些接口必须调整。
## 0. 项目边界与运行顺序（Project Scope and Execution Order）
- 数据集（Dataset）：`online_shopping_10_cats.csv`，过滤空评论并只保留标签 `0/1`。
- 典型流程（Pipeline）：`process.py` → `train.py` → `evaluate.py` / `predict.py`。
- 外部副作用（Side Effect）：预处理会写入数据文件，训练会写模型权重与 TensorBoard 日志；因此相关代码不提供伪造的固定输出。
- 相关理论（Theory）：[[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）]]、[[05-BERT 原理与模型族（BERT Principles and Family）]]。
## 1. RNN 基线版本（RNN Baseline, V1.0）
### 需求说明
本案例的目标是基于 RNN构建一个文本情感分类模型，对评论内容进行二分类判断（正面或负面）。
### 需求分析
### 数据集处理
本案例的目标对用户评论文本进行情感分类，因此需使用带有情感标签（正面/负面）的评论数据集。
数据集来源为ChineseNLPCorpus，格式CSV，具体结构如下

|cat|label|review|
|---|---|---|
|书籍|1|感谢于歌先生为大家带来这么精彩的一本好书！|
|书籍|0|这本书纸质不怎样，内容也不怎样。|
|水果|1|苹果酸甜可口，大小适中，好吃。|
|水果|0|不是很大，比较甜，不会回购，感觉加运费后不划算。|
本案例只需选取数据集中的review和label字段，构造输入-输出对即可。
### 模型结构设计
模型整体由以下三个主要部分组成：
本任务采用基于循环神经网络（RNN）的语言模型结构（RNNLM）来实现文本的特征提取和分类。模型整体由以下三个主要部分组成：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114045.png]]
- 嵌入层（Embedding）
将输入的词或字索引映射为稠密向量表示，便于后续神经网络处理。
- 循环神经网络（RNN）
用于建模输入序列的上下文信息，输出最后一个时间步的隐藏状态作为上下文表示。
- 输出层（Linear）
将 RNN的隐藏状态输出映射为一个标量，表示该评论为正面情感的倾向得分（经sigmod函数后，大于0.5判定为正面情感，小于等于0.5判定为负面情感）。
### 训练方案
- 损失函数：
使用 BCEWithLogitsLoss，结合了sigmoid激活和二分类交叉熵计算，数值稳定且适合二分类任务。
- 优化器：
使用Adam优化器进行参数更新，提升训练效率。
### 评估方案
模型训练完毕后，使用测试集统计正确率。
### 需求实现
### 项目结构
项目结构如下：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114046.png]]
### 完整代码
完整代码如下：
#### 数据预处理

```python
### process.py
import pandas as pd
from sklearn.model_selection import train_test_split
from tokenizer import JiebaTokenizer
import config
def process():
    """
    数据预处理主函数。
    """
    print("开始处理数据")
    # 1. 读取原始数据文件
    df = pd.read_csv(
        config.RAW_DATA_DIR / 'online_shopping_10_cats.csv',
        usecols=['review', 'label'],
        encoding='utf-8'
    )
    # 2. 数据清洗：去除空值和空字符串
    df = df.dropna()
    df = df[df['review'].str.strip().ne('')]
    # 3. 划分训练集和测试集
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    # 4. 构建词表并保存
    JiebaTokenizer.build_vocab(
        train_df['review'].tolist(),
        config.PROCESSED_DATA_DIR / 'vocab.txt'
    )
    # 5. 加载词表
    tokenizer = JiebaTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'vocab.txt')
    # 6. 编码训练集并保存
    train_df['review'] = train_df['review'].apply(
        lambda x: tokenizer.encode(x, seq_len=config.SEQ_LEN)
    )
    train_df.to_json(
        config.PROCESSED_DATA_DIR / 'indexed_train.jsonl',
        orient='records',
        lines=True
    )
    # 7. 编码测试集并保存
    test_df['review'] = test_df['review'].apply(
        lambda x: tokenizer.encode(x, seq_len=config.SEQ_LEN)
    )
    test_df.to_json(
        config.PROCESSED_DATA_DIR / 'indexed_test.jsonl',
        orient='records',
        lines=True
    )
    print("数据处理完成")
if __name__ == '__main__':
    process()
```
#### 自定义分词器

```python
### tokenizer.py
import jieba
from tqdm import tqdm
jieba.setLogLevel(jieba.logging.WARNING)
class JiebaTokenizer:
    """
    基于 jieba 的分词器，用于分词、编码和词表管理。
    """
    unk_token = '<unk>'
    pad_token = '<pad>'
    @staticmethod
    def tokenize(sentence):
        """
        对句子进行分词。
        :param sentence: 输入句子。
        :return: 分词后的 token 列表。
        """
        return jieba.lcut(sentence)
    @classmethod
    def build_vocab(cls, sentences, vocab_file):
        """
        构建词表并保存到文件。
        :param sentences: 句子列表。
        :param vocab_file: 保存词表的文件路径。
        """
        unique_words = set()
        for sentence in tqdm(sentences, desc='分词'):
            # 收集所有唯一词
            for word in cls.tokenize(sentence):
                unique_words.add(word)
        # 将 pad 和 unk 放在词表开头
        vocab_list = [cls.pad_token, cls.unk_token] + list(unique_words)
        # 保存词表到文件
        with open(vocab_file, 'w', encoding='utf-8') as f:
            for word in vocab_list:
                f.write(word + '\n')
    @classmethod
    def from_vocab(cls, vocab_file):
        """
        从文件加载词表。
        :param vocab_file: 词表文件路径。
        :return: JiebaTokenizer 实例。
        """
        with open(vocab_file, 'r', encoding='utf-8') as f:
            vocab_list = [line.strip() for line in f.readlines()]
        return cls(vocab_list)
    def __init__(self, vocab_list):
        """
        初始化 tokenizer。
        :param vocab_list: 词表列表。
        """
        self.vocab_list = vocab_list
        self.vocab_size = len(vocab_list)
        self.word2index = {word: index for index, word in enumerate(vocab_list)}
        self.index2word = {index: word for index, word in enumerate(vocab_list)}
        self.unk_token_index = self.word2index[self.unk_token]
        self.pad_token_index = self.word2index[self.pad_token]
    def encode(self, sentence, seq_len):
        """
        将句子编码为索引列表。
        :param sentence: 输入句子。
        :param seq_len: 序列长度。
        :return: 索引列表。
        """
        tokens = self.tokenize(sentence)
        indexes = [self.word2index.get(token, self.unk_token_index) for token in tokens]
        # 填充或截断
        if len(indexes) >= seq_len:
            return indexes[:seq_len]
        else:
            return indexes + [self.pad_token_index] * (seq_len - len(indexes))
```
#### 自定义数据集

```python
### dataset.py
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import config
class ReviewAnalyzeDataset(Dataset):
    """
    评论情感分析数据集。
    """
    def __init__(self, file_path):
        """
        初始化数据集。
        :param file_path: 数据文件路径（JSONL 格式）。
        """
        # 加载 JSONL 数据到内存
        self.data = pd.read_json(file_path, lines=True).to_dict(orient='records')
    def __len__(self):
        """
        获取数据集样本数。
        :return: 样本数量。
        """
        return len(self.data)
    def __getitem__(self, index):
        """
        获取指定索引的样本。
        :param index: 样本索引。
        :return: (input_tensor, target_tensor)
        """
        # 构建输入和目标张量
        input_tensor = torch.tensor(self.data[index]['review'], dtype=torch.long)
        target_tensor = torch.tensor(self.data[index]['label'], dtype=torch.float)
        return input_tensor, target_tensor
def get_dataloader(train=True):
    """
    创建数据加载器。
    :param train: 是否加载训练集（True）或测试集（False）。
    :return: DataLoader 实例。
    """
    file_name = 'indexed_train.jsonl' if train else 'indexed_test.jsonl'
    # 创建数据集实例
    dataset = ReviewAnalyzeDataset(config.PROCESSED_DATA_DIR / file_name)
    # 返回 DataLoader
    return DataLoader(dataset, batch_size=config.BATCH_SIZE, shuffle=True)
if __name__ == '__main__':
    # 简单测试数据加载器
    dataloader = get_dataloader()
    for input_tensor, target_tensor in dataloader:
        print(input_tensor.shape, target_tensor.shape)
        break
```
#### 模型定义

```python
### model.py
import torch
from torch import nn
import config
from torchinfo import summary
class ReviewAnalyzeModel(nn.Module):
    """
    评论情感分析模型，基于 LSTM。
    """
    def __init__(self, vocab_size, padding_idx):
        """
        初始化模型。
        :param vocab_size: 词表大小。
        :param padding_idx: padding token 的索引。
        """
        super().__init__()
        # 嵌入层：将索引映射为词向量
        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=config.EMBEDDING_DIM,
            padding_idx=padding_idx
        )
        # RNN层：提取序列特征
        self.rnn= nn.RNN(
            input_size=config.EMBEDDING_DIM,
            hidden_size=config.HIDDEN_DIM,
            batch_first=True
        )
        # 线性层：映射到单输出，用于二分类
        self.linear = nn.Linear(in_features=config.HIDDEN_DIM, out_features=1)
    def forward(self, x):
        """
        前向传播。
        :param x: 输入张量，形状 (batch_size, seq_len)。
        :return: 模型输出张量，形状 (batch_size,)。
        """
        # 嵌入层处理
        embed = self.embedding(x)  # (batch_size, seq_len, embedding_dim)
        # RNN处理序列
        output, _ = self.rnn(embed)  # (batch_size, seq_len, hidden_dim)
        # 取最后时间步隐藏状态用于分类
        result = self.linear(output[:, -1, :]).squeeze(dim=1)  # (batch_size,)
        return result
if __name__ == '__main__':
    model = ReviewAnalyzeModel(vocab_size=1000, padding_idx=0)
    # 创建 dummy 输入张量用于结构展示
    dummy_input = torch.randint(
        low=0,
        high=1000,
        size=(config.BATCH_SIZE, config.SEQ_LEN),
        dtype=torch.long
    )
    # 打印模型结构信息
summary(model, input_data=dummy_input)
```
#### 模型训练

```python
### train.py
import time
import torch
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from dataset import get_dataloader
from tokenizer import JiebaTokenizer
import config
from model import ReviewAnalyzeModel
def train_one_epoch(model, dataloader, loss_function, optimizer, device):
    """
    训练一个 epoch。
    :param model: 模型。
    :param dataloader: 数据加载器。
    :param loss_function: 损失函数。
    :param optimizer: 优化器。
    :param device: 设备。
    :return: 平均损失。
    """
    total_loss = 0
    model.train()
    for inputs, targets in tqdm(dataloader, desc='训练'):
        # 移动数据到设备
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        # 前向传播
        outputs = model(inputs)
        # 计算损失
        loss = loss_function(outputs, targets)
        # 反向传播
        loss.backward()
        # 参数更新
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(dataloader)
def train():
    """
    模型训练主函数。
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    dataloader = get_dataloader()
    tokenizer = JiebaTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'vocab.txt')
    model = ReviewAnalyzeModel(
        vocab_size=tokenizer.vocab_size,
        padding_idx=tokenizer.pad_token_index
    ).to(device)
    loss_function = torch.nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.LEARNING_RATE)
    writer = SummaryWriter(log_dir=config.LOG_DIR / time.strftime('%Y-%m-%d_%H-%M-%S'))
    best_loss = float('inf')
    for epoch in range(1, config.EPOCHS + 1):
        print(f'========== Epoch: {epoch} ==========')
        avg_loss = train_one_epoch(model, dataloader, loss_function, optimizer, device)
        print(f'Loss: {avg_loss:.4f}')
        writer.add_scalar('Loss/Train', avg_loss, epoch)
        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save(model.state_dict(), config.MODELS_DIR / 'model.pt')
            print('模型保存成功')
if __name__ == '__main__':
    train()
```
#### 模型预测

```python
### predict.py
import torch
import config
from tokenizer import JiebaTokenizer
from model import ReviewAnalyzeModel
def predict_batch(input_tensor, model):
    """
    对一个 batch 的输入进行预测。
    :param input_tensor: 输入张量，形状 (batch_size, seq_len)。
    :param model: 模型。
    :return: 概率列表。
    """
    model.eval()
    with torch.no_grad():
        # 前向传播获取 logits
        output = model(input_tensor)
        # 使用 sigmoid 将 logits 转换为概率
        probs = torch.sigmoid(output)
    return probs.tolist()
def predict(user_input, model, tokenizer, device):
    """
    对单条用户输入进行预测。
    :param user_input: 用户输入文本。
    :param model: 模型。
    :param tokenizer: 分词器。
    :param device: 设备。
    :return: 概率值。
    """
    # 编码并填充输入文本
    input_ids = tokenizer.encode(user_input, config.SEQ_LEN)
    # 转换为张量并移动到设备
    input_tensor = torch.tensor([input_ids], dtype=torch.long).to(device)
    # 获取预测概率
    probs = predict_batch(input_tensor, model)
    prob = probs[0]
    return prob
def run_predict():
    """
    启动预测交互程序。
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # 加载 tokenizer
    tokenizer = JiebaTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'vocab.txt')
    # 创建并加载模型
    model = ReviewAnalyzeModel(
        vocab_size=tokenizer.vocab_size,
        padding_idx=tokenizer.pad_token_index
    ).to(device)
    model.load_state_dict(torch.load(config.MODELS_DIR / 'model.pt'))
    print('请输入要预测的评论：（输入 q 或 quit 退出）')
    while True:
        user_input = input('> ')
        if user_input in ['q', 'quit']:
            print('退出程序')
            break
        if not user_input:
            print('输入为空，请重新输入')
            continue
        # 预测结果
        prob = predict(user_input, model, tokenizer, device)
        if prob > 0.5:
            print(f'正面评价（置信度：{prob:.2f}）')
        else:
            print(f'负面评价（置信度：{1 - prob:.2f}）')
if __name__ == '__main__':
    run_predict()
```
#### 模型评估

```python
### evaluate.py
import torch
from tokenizer import JiebaTokenizer
import config
from model import ReviewAnalyzeModel
from dataset import get_dataloader
from predict import predict_batch
def evaluate(model, dataloader, device):
    """
    模型评估。
    :param model: 模型。
    :param dataloader: 数据加载器。
    :param device: 设备。
    :return: 准确率。
    """
    total_count = 0
    correct_count = 0
    model.eval()
    for inputs, targets in dataloader:
        # 数据转移到设备
        inputs = inputs.to(device)
        targets = targets.tolist()
        # 获取预测概率
        probs = predict_batch(inputs, model)
        # 统计准确率
        for prob, target in zip(probs, targets):
            pred_label = 1 if prob > 0.5 else 0
            if pred_label == target:
                correct_count += 1
            total_count += 1
    return correct_count / total_count
def run_evaluate():
    """
    运行评估流程。
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tokenizer = JiebaTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'vocab.txt')
    model = ReviewAnalyzeModel(
        vocab_size=tokenizer.vocab_size,
        padding_idx=tokenizer.pad_token_index
    ).to(device)
    model.load_state_dict(torch.load(config.MODELS_DIR / 'model.pt'))
    dataloader = get_dataloader(train=False)
    acc = evaluate(model, dataloader, device)
    print("========== 评估结果 ==========")
    print(f"准确率：{acc:.4f}")
    print("=============================")
if __name__ == '__main__':
    run_evaluate()
```
#### 配置文件

```python
### config.py
### 项目根目录
from pathlib import Path
### 项目根目录
ROOT_DIR = Path(__file__).parent.parent
### 数据路径
RAW_DATA_DIR = ROOT_DIR / 'data' / 'raw'
PROCESSED_DATA_DIR = ROOT_DIR / 'data' / 'processed'
### 模型与日志路径
MODELS_DIR = ROOT_DIR / 'models'
LOG_DIR = ROOT_DIR / 'logs'
### 训练参数
SEQ_LEN = 128  # 输入序列长度
BATCH_SIZE = 64  # 批大小
EMBEDDING_DIM = 64  # 嵌入层维度
HIDDEN_DIM = 128  # LSTM 隐藏层维度
LEARNING_RATE = 1e-3  # 学习率
EPOCHS = 30  # 总训练轮数
```
### 存在问题
### 概述
尽管循环神经网络（RNN）在处理序列数据方面具有天然优势，但它在实际应用中面临一个非常严重的问题：长期依赖建模困难。这指的是：在训练过程中，当输入序列很长时，模型难以有效学习早期输入对最终输出的影响。

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114047.png]]
### 问题分析
上述问题的根本原因在于训练过程中存在的梯度消失或梯度爆炸问题。
在训练RNN时，采用的是时间反向传播（Backpropagation Through Time, BPTT）方法，在反向传播过程中，梯度需要在每个时间步上不断链式传递，下图为RNN在训练过程中的计算图：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114048.png]]
高清大图：
根据上述计算图，可以得出
其中每一项表示每条路径对贡献。
展开早期时间步的某一条路径（例如）可以得到
展开其中一环（为简单起见，按照标量推导）
现有，令
则有
可得，
所以，早期路径的展开可以写为：
可以看到上述公式中有很多次的连乘，其中的范围是(0,1]，如下图所示

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114050.png]]
所以若也小于1，那么经过的多次连乘，早期路径（例如）的值就会指数级衰减，并迅速接近于0，这个现象称为梯度消失。
由于早期时间步的梯度值几乎为0，所以总梯度几乎只会受到最近时间步的输入影响，换句话说，在权重参数更新（）时，早期输入的信息几乎不会对的更新产生贡献。
这就导致模型只能学到短期依赖，而无法学到长期依赖。
另外，若大于1（大到大于1），那么经过的多次连乘，早期路径（例如）的值就会指数级增长，这个现象称为梯度爆炸，梯度爆炸又会使得参数更新极不稳定。
这两个问题是制约RNN 学习长期依赖的主要瓶颈。

## 2. LSTM 改进版本（LSTM Improvement, V2.0）
将上一节使用RNN实现的评论情感分析模型改为使用LSTM，并对比两者的效果。
### 项目结构
项目结构如下：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114073.png]]
### 完整代码
完整代码如下：
#### 数据预处理

```python
### process.py
import pandas as pd
from sklearn.model_selection import train_test_split
from tokenizer import JiebaTokenizer
import config
def process():
    """
    数据预处理主函数。
    """
    print("开始处理数据")
    # 1. 读取原始数据文件
    df = pd.read_csv(
        config.RAW_DATA_DIR / 'online_shopping_10_cats.csv',
        usecols=['review', 'label'],
        encoding='utf-8'
    )
    # 2. 数据清洗：去除空值和空字符串
    df = df.dropna()
    df = df[df['review'].str.strip().ne('')]
    # 3. 划分训练集和测试集
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    # 4. 构建词表并保存
    JiebaTokenizer.build_vocab(
        train_df['review'].tolist(),
        config.PROCESSED_DATA_DIR / 'vocab.txt'
    )
    # 5. 加载词表
    tokenizer = JiebaTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'vocab.txt')
    # 6. 编码训练集并保存
    train_df['review'] = train_df['review'].apply(
        lambda x: tokenizer.encode(x, seq_len=config.SEQ_LEN)
    )
    train_df.to_json(
        config.PROCESSED_DATA_DIR / 'indexed_train.jsonl',
        orient='records',
        lines=True
    )
    # 7. 编码测试集并保存
    test_df['review'] = test_df['review'].apply(
        lambda x: tokenizer.encode(x, seq_len=config.SEQ_LEN)
    )
    test_df.to_json(
        config.PROCESSED_DATA_DIR / 'indexed_test.jsonl',
        orient='records',
        lines=True
    )
    print("数据处理完成")
if __name__ == '__main__':
    process()
```
#### 自定义分词器

```python
### tokenizer.py
import jieba
from tqdm import tqdm
jieba.setLogLevel(jieba.logging.WARNING)
class JiebaTokenizer:
    """
    基于 jieba 的分词器，用于分词、编码和词表管理。
    """
    unk_token = '<unk>'
    pad_token = '<pad>'
    @staticmethod
    def tokenize(sentence):
        """
        对句子进行分词。
        :param sentence: 输入句子。
        :return: 分词后的 token 列表。
        """
        return jieba.lcut(sentence)
    @classmethod
    def build_vocab(cls, sentences, vocab_file):
        """
        构建词表并保存到文件。
        :param sentences: 句子列表。
        :param vocab_file: 保存词表的文件路径。
        """
        unique_words = set()
        for sentence in tqdm(sentences, desc='分词'):
            # 收集所有唯一词
            for word in cls.tokenize(sentence):
                unique_words.add(word)
        # 将 pad 和 unk 放在词表开头
        vocab_list = [cls.pad_token, cls.unk_token] + list(unique_words)
        # 保存词表到文件
        with open(vocab_file, 'w', encoding='utf-8') as f:
            for word in vocab_list:
                f.write(word + '\n')
    @classmethod
    def from_vocab(cls, vocab_file):
        """
        从文件加载词表。
        :param vocab_file: 词表文件路径。
        :return: JiebaTokenizer 实例。
        """
        with open(vocab_file, 'r', encoding='utf-8') as f:
            vocab_list = [line.strip() for line in f.readlines()]
        return cls(vocab_list)
    def __init__(self, vocab_list):
        """
        初始化 tokenizer。
        :param vocab_list: 词表列表。
        """
        self.vocab_list = vocab_list
        self.vocab_size = len(vocab_list)
        self.word2index = {word: index for index, word in enumerate(vocab_list)}
        self.index2word = {index: word for index, word in enumerate(vocab_list)}
        self.unk_token_index = self.word2index[self.unk_token]
        self.pad_token_index = self.word2index[self.pad_token]
    def encode(self, sentence, seq_len):
        """
        将句子编码为索引列表。
        :param sentence: 输入句子。
        :param seq_len: 序列长度。
        :return: 索引列表。
        """
        tokens = self.tokenize(sentence)
        indexes = [self.word2index.get(token, self.unk_token_index) for token in tokens]
        # 填充或截断
        if len(indexes) >= seq_len:
            return indexes[:seq_len]
        else:
            return indexes + [self.pad_token_index] * (seq_len - len(indexes))
```
#### 自定义数据集

```python
### dataset.py
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import config
class ReviewAnalyzeDataset(Dataset):
    """
    评论情感分析数据集。
    """
    def __init__(self, file_path):
        """
        初始化数据集。
        :param file_path: 数据文件路径（JSONL 格式）。
        """
        # 加载 JSONL 数据到内存
        self.data = pd.read_json(file_path, lines=True).to_dict(orient='records')
    def __len__(self):
        """
        获取数据集样本数。
        :return: 样本数量。
        """
        return len(self.data)
    def __getitem__(self, index):
        """
        获取指定索引的样本。
        :param index: 样本索引。
        :return: (input_tensor, target_tensor)
        """
        # 构建输入和目标张量
        input_tensor = torch.tensor(self.data[index]['review'], dtype=torch.long)
        target_tensor = torch.tensor(self.data[index]['label'], dtype=torch.float)
        return input_tensor, target_tensor
def get_dataloader(train=True):
    """
    创建数据加载器。
    :param train: 是否加载训练集（True）或测试集（False）。
    :return: DataLoader 实例。
    """
    file_name = 'indexed_train.jsonl' if train else 'indexed_test.jsonl'
    # 创建数据集实例
    dataset = ReviewAnalyzeDataset(config.PROCESSED_DATA_DIR / file_name)
    # 返回 DataLoader
    return DataLoader(dataset, batch_size=config.BATCH_SIZE, shuffle=True)
if __name__ == '__main__':
    # 简单测试数据加载器
    dataloader = get_dataloader()
    for input_tensor, target_tensor in dataloader:
        print(input_tensor.shape, target_tensor.shape)
        break
```
#### 模型定义

```python
### model.py
import torch
from torch import nn
import config
from torchinfo import summary
class ReviewAnalyzeModel(nn.Module):
    """
    评论情感分析模型，基于 LSTM。
    """
    def __init__(self, vocab_size, padding_idx):
        """
        初始化模型。
        :param vocab_size: 词表大小。
        :param padding_idx: padding token 的索引。
        """
        super().__init__()
        # 嵌入层：将索引映射为词向量
        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=config.EMBEDDING_DIM,
            padding_idx=padding_idx
        )
        # LSTM 层：提取序列特征
        self.lstm = nn.LSTM(
            input_size=config.EMBEDDING_DIM,
            hidden_size=config.HIDDEN_DIM,
            batch_first=True
        )
        # 线性层：映射到单输出，用于二分类
        self.linear = nn.Linear(in_features=config.HIDDEN_DIM, out_features=1)
    def forward(self, x):
        """
        前向传播。
        :param x: 输入张量，形状 (batch_size, seq_len)。
        :return: 模型输出张量，形状 (batch_size,)。
        """
        # 嵌入层处理
        embed = self.embedding(x)  # (batch_size, seq_len, embedding_dim)
        # LSTM 处理序列
        output, _ = self.lstm(embed)  # (batch_size, seq_len, hidden_dim)
        # 取最后时间步隐藏状态用于分类
        result = self.linear(output[:, -1, :]).squeeze(dim=1)  # (batch_size,)
        return result
if __name__ == '__main__':
    model = ReviewAnalyzeModel(vocab_size=1000, padding_idx=0)
    # 创建 dummy 输入张量用于结构展示
    dummy_input = torch.randint(
        low=0,
        high=1000,
        size=(config.BATCH_SIZE, config.SEQ_LEN),
        dtype=torch.long
    )
    # 打印模型结构信息
summary(model, input_data=dummy_input)
```
#### 模型训练

```python
### train.py
import time
import torch
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from dataset import get_dataloader
from tokenizer import JiebaTokenizer
import config
from model import ReviewAnalyzeModel
def train_one_epoch(model, dataloader, loss_function, optimizer, device):
    """
    训练一个 epoch。
    :param model: 模型。
    :param dataloader: 数据加载器。
    :param loss_function: 损失函数。
    :param optimizer: 优化器。
    :param device: 设备。
    :return: 平均损失。
    """
    total_loss = 0
    model.train()
    for inputs, targets in tqdm(dataloader, desc='训练'):
        # 移动数据到设备
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        # 前向传播
        outputs = model(inputs)
        # 计算损失
        loss = loss_function(outputs, targets)
        # 反向传播
        loss.backward()
        # 参数更新
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(dataloader)
def train():
    """
    模型训练主函数。
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    dataloader = get_dataloader()
    tokenizer = JiebaTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'vocab.txt')
    model = ReviewAnalyzeModel(
        vocab_size=tokenizer.vocab_size,
        padding_idx=tokenizer.pad_token_index
    ).to(device)
    loss_function = torch.nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.LEARNING_RATE)
    writer = SummaryWriter(log_dir=config.LOG_DIR / time.strftime('%Y-%m-%d_%H-%M-%S'))
    best_loss = float('inf')
    for epoch in range(1, config.EPOCHS + 1):
        print(f'========== Epoch: {epoch} ==========')
        avg_loss = train_one_epoch(model, dataloader, loss_function, optimizer, device)
        print(f'Loss: {avg_loss:.4f}')
        writer.add_scalar('Loss/Train', avg_loss, epoch)
        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save(model.state_dict(), config.MODELS_DIR / 'model.pt')
            print('模型保存成功')
if __name__ == '__main__':
    train()
```
#### 模型预测

```python
### predict.py
import torch
import config
from tokenizer import JiebaTokenizer
from model import ReviewAnalyzeModel
def predict_batch(input_tensor, model):
    """
    对一个 batch 的输入进行预测。
    :param input_tensor: 输入张量，形状 (batch_size, seq_len)。
    :param model: 模型。
    :return: 概率列表。
    """
    model.eval()
    with torch.no_grad():
        # 前向传播获取 logits
        output = model(input_tensor)
        # 使用 sigmoid 将 logits 转换为概率
        probs = torch.sigmoid(output)
    return probs.tolist()
def predict(user_input, model, tokenizer, device):
    """
    对单条用户输入进行预测。
    :param user_input: 用户输入文本。
    :param model: 模型。
    :param tokenizer: 分词器。
    :param device: 设备。
    :return: 概率值。
    """
    # 编码并填充输入文本
    input_ids = tokenizer.encode(user_input, config.SEQ_LEN)
    # 转换为张量并移动到设备
    input_tensor = torch.tensor([input_ids], dtype=torch.long).to(device)
    # 获取预测概率
    probs = predict_batch(input_tensor, model)
    prob = probs[0]
    return prob
def run_predict():
    """
    启动预测交互程序。
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # 加载 tokenizer
    tokenizer = JiebaTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'vocab.txt')
    # 创建并加载模型
    model = ReviewAnalyzeModel(
        vocab_size=tokenizer.vocab_size,
        padding_idx=tokenizer.pad_token_index
    ).to(device)
    model.load_state_dict(torch.load(config.MODELS_DIR / 'model.pt'))
    print('请输入要预测的评论：（输入 q 或 quit 退出）')
    while True:
        user_input = input('> ')
        if user_input in ['q', 'quit']:
            print('退出程序')
            break
        if not user_input:
            print('输入为空，请重新输入')
            continue
        # 预测结果
        prob = predict(user_input, model, tokenizer, device)
        if prob > 0.5:
            print(f'正面评价（置信度：{prob:.2f}）')
        else:
            print(f'负面评价（置信度：{1 - prob:.2f}）')
if __name__ == '__main__':
    run_predict()
```
#### 模型评估

```python
### evaluate.py
import torch
from tokenizer import JiebaTokenizer
import config
from model import ReviewAnalyzeModel
from dataset import get_dataloader
from predict import predict_batch
def evaluate(model, dataloader, device):
    """
    模型评估。
    :param model: 模型。
    :param dataloader: 数据加载器。
    :param device: 设备。
    :return: 准确率。
    """
    total_count = 0
    correct_count = 0
    model.eval()
    for inputs, targets in dataloader:
        # 数据转移到设备
        inputs = inputs.to(device)
        targets = targets.tolist()
        # 获取预测概率
        probs = predict_batch(inputs, model)
        # 统计准确率
        for prob, target in zip(probs, targets):
            pred_label = 1 if prob > 0.5 else 0
            if pred_label == target:
                correct_count += 1
            total_count += 1
    return correct_count / total_count
def run_evaluate():
    """
    运行评估流程。
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tokenizer = JiebaTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'vocab.txt')
    model = ReviewAnalyzeModel(
        vocab_size=tokenizer.vocab_size,
        padding_idx=tokenizer.pad_token_index
    ).to(device)
    model.load_state_dict(torch.load(config.MODELS_DIR / 'model.pt'))
    dataloader = get_dataloader(train=False)
    acc = evaluate(model, dataloader, device)
    print("========== 评估结果 ==========")
    print(f"准确率：{acc:.4f}")
    print("=============================")
if __name__ == '__main__':
    run_evaluate()
```
#### 配置文件

```python
### config.py
### 项目根目录
from pathlib import Path
### 项目根目录
ROOT_DIR = Path(__file__).parent.parent
### 数据路径
RAW_DATA_DIR = ROOT_DIR / 'data' / 'raw'
PROCESSED_DATA_DIR = ROOT_DIR / 'data' / 'processed'
### 模型与日志路径
MODELS_DIR = ROOT_DIR / 'models'
LOG_DIR = ROOT_DIR / 'logs'
### 训练参数
SEQ_LEN = 128  # 输入序列长度
BATCH_SIZE = 64  # 批大小
EMBEDDING_DIM = 64  # 嵌入层维度
HIDDEN_DIM = 128  # LSTM 隐藏层维度
LEARNING_RATE = 1e-3  # 学习率
EPOCHS = 30  # 总训练轮数
```
### 存在问题
尽管 LSTM 相较传统 RNN 解决了长期依赖问题，性能大幅提升，但在实际应用中，仍存在一些明显的局限性和问题，主要包括：
- 难以并行计算
LSTM 的时间步之间具有强依赖性（后一个时间步的输入依赖前一个时间步的输出），导致无法进行大规模并行加速，训练和推理速度受限。
- 参数量大，计算开销高
每个 LSTM 单元内部包含多个门控机制（输入门、遗忘门、输出门），每个门都需要独立计算，导致参数数量和计算量远大于普通 RNN。
在资源受限的场景下（如移动端、嵌入式设备），部署 LSTM 会面临挑战。
- 长期依赖建模仍然有限
虽然 LSTM 延缓了梯度消失问题，但并不能完全消除。当序列极长时，模型依然难以有效捕捉非常远距离的依赖关系。

## 3. GRU 改进版本（GRU Improvement, V3.0）
将之前实现的评论情感分析模型改为使用GRU，并对比RNN、LSTM、GRU三者的效果。
### 项目结构
项目结构如下：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114091.png]]
### 完整代码
#### 数据预处理

```python
### process.py
import pandas as pd
from sklearn.model_selection import train_test_split
from tokenizer import JiebaTokenizer
import config
def process():
    print("开始处理数据")
    # 1.读取数据
    df = pd.read_csv(config.RAW_DATA_DIR / 'online_shopping_10_cats.csv', usecols=['review', 'label'], encoding='utf-8')
    # 2.过滤数据
    df = df.dropna()
    df = df[df['review'].str.strip().ne('')]
    # 3.划分数据集
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    # 4.构建词表
    JiebaTokenizer.build_vocab(train_df['review'].tolist(), config.PROCESSED_DATA_DIR / 'vocab.txt')
    # 5.构建Tokenizer对象
    tokenizer = JiebaTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'vocab.txt')
    # 6.构建训练集并保存
    train_df['review'] = train_df['review'].apply(lambda x: tokenizer.encode(x, seq_len=config.SEQ_LEN))
    train_df.to_json(config.PROCESSED_DATA_DIR / 'indexed_train.jsonl', orient='records', lines=True)
    # 7.构建测试集并保存
    test_df['review'] = test_df['review'].apply(lambda x: tokenizer.encode(x, seq_len=config.SEQ_LEN))
    test_df.to_json(config.PROCESSED_DATA_DIR / 'indexed_test.jsonl', orient='records', lines=True)
    print("数据处理完成")
if __name__ == '__main__':
    process()
```
#### 自定义分词器

```python
### tokenizer.py
import jieba
from tqdm import tqdm
jieba.setLogLevel(jieba.logging.WARNING)
class JiebaTokenizer:
    unk_token = '<unk>'
    pad_token = '<pad>'
    @staticmethod
    def tokenize(sentence):
        """
        分词
        :param sentence: 句子
        :return: token列表
        """
        return jieba.lcut(sentence)
    @classmethod
    def build_vocab(cls, sentences, vocab_file):
        """
        构建并保存词表
        :param sentences: 句子列表
        :param vocab_file: 词表文件路径
        """
        # 1.获取词表
        unique_words = set()
        for sentence in tqdm(sentences, desc='分词'):
            for word in cls.tokenize(sentence):
                unique_words.add(word)
        vocab_list = [cls.pad_token, cls.unk_token] + list(unique_words)
        # 2.保存词表
        with open(vocab_file, 'w', encoding='utf-8') as f:
            for word in vocab_list:
                f.write(word + '\n')
    def __init__(self, vocab_list):
        """
        初始化tokenizer
        :param vocab_list: 词表列表
        """
        self.vocab_list = vocab_list  # 此表列表(实例属性)
        self.vocab_size = len(vocab_list)  # 词表大小(实例属性)
        self.word2index = {word: index for index, word in enumerate(vocab_list)}  # 词到索引(实例属性)
        self.index2word = {index: word for index, word in enumerate(vocab_list)}  # 索引到词(实例属性)
        self.unk_token_index = self.word2index[self.unk_token]  # 未知词索引(实例属性)
        self.pad_token_index = self.word2index[self.pad_token]
    @classmethod
    def from_vocab(cls, vocab_file):
        """
        加载词表并创建Tokenizer对象
        :param vocab_file: 词表文件
        :return: tokenizer对象
        """
        with open(vocab_file, 'r', encoding='utf-8') as f:
            vocab_list = [line[:-1] for line in f.readlines()]
        return cls(vocab_list)
    def encode(self, sentence, seq_len):
        """
        编码
        :param sentence: 句子
        :param seq_len: 长度
        :return: 索引列表
        """
        tokens = self.tokenize(sentence)
        indexes = [self.word2index.get(token, self.unk_token_index) for token in tokens]
        if len(indexes) >= seq_len:
            return indexes[:seq_len]
        else:
            return indexes + [self.pad_token_index] * (seq_len - len(indexes))
```
#### 自定义数据集

```python
### dataset.py
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import config
class ReviewAnalyzeDataset(Dataset):
    """
    评论情感分析数据集。
    """
    def __init__(self, file_path):
        """
        初始化数据集。
        :param file_path: 数据文件路径（jsonl 格式）
        """
        self.data = pd.read_json(file_path, lines=True).to_dict(orient='records')
    def __len__(self):
        """
        返回数据集大小。
        :return: 数据集长度
        """
        return len(self.data)
    def __getitem__(self, index):
        """
        获取单条样本。
        :param index: 索引
        :return: (input_tensor, target_tensor)
        """
        input_tensor = torch.tensor(self.data[index]['review'], dtype=torch.long)
        target_tensor = torch.tensor(self.data[index]['label'], dtype=torch.float)
        return input_tensor, target_tensor
def get_dataloader(train: bool = True):
    """
    获取数据加载器。
    :param train: 是否加载训练集
    :return: DataLoader
    """
    file_name = 'indexed_train.jsonl' if train else 'indexed_test.jsonl'
    dataset = ReviewAnalyzeDataset(config.PROCESSED_DATA_DIR / file_name)
    return DataLoader(dataset, batch_size=config.BATCH_SIZE, shuffle=True)
if __name__ == '__main__':
    dataloader = get_dataloader()
    for input_tensor, target_tensor in dataloader:
        print(f"输入形状: {input_tensor.shape}, 标签形状: {target_tensor.shape}")
        break
```
#### 模型定义

```python
### model.py
import torch
from torch import nn
import config
from torchinfo import summary
class ReviewAnalyzeModel(nn.Module):
    """
    评论情感分析模型：Embedding -> GRU -> Linear
    """
    def __init__(self, vocab_size, padding_idx):
        """
        初始化模型。
        :param vocab_size: 词表大小
        :param padding_idx: padding token 的索引
        """
        super().__init__()
        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=config.EMBEDDING_DIM,
            padding_idx=padding_idx
        )
        self.gru = nn.GRU(
            input_size=config.EMBEDDING_DIM,
            hidden_size=config.HIDDEN_DIM,
            batch_first=True
        )
        self.linear = nn.Linear(
            in_features=config.HIDDEN_DIM,
            out_features=1
        )
    def forward(self, x):
        """
        前向传播。
        :param x: 输入索引张量，形状 (batch_size, seq_len)
        :return: 输出 logits，形状 (batch_size,)
        """
        embed = self.embedding(x)  # 嵌入层输出: (batch_size, seq_len, embedding_dim)
        gru_output, _ = self.gru(embed)  # GRU输出: (batch_size, seq_len, hidden_dim)
        final_output = gru_output[:, -1, :]  # 取最后时间步输出
        logits = self.linear(final_output).squeeze(dim=1)  # 线性层 + squeeze: (batch_size,)
        return logits
if __name__ == '__main__':
    model = ReviewAnalyzeModel(vocab_size=1000, padding_idx=0)
    dummy_input = torch.randint(low=0, high=1000, size=(config.BATCH_SIZE, config.SEQ_LEN), dtype=torch.long)
    summary(model, input_data=dummy_input)
```
#### 模型训练

```python
### train.py
import time
import torch
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from dataset import get_dataloader
from tokenizer import JiebaTokenizer
from model import ReviewAnalyzeModel
import config
def train_one_epoch(model, dataloader, loss_function, optimizer, device):
    """
    单轮训练。
    :param model: 模型
    :param dataloader: 数据加载器
    :param loss_function: 损失函数
    :param optimizer: 优化器
    :param device: 设备
    :return: 平均损失
    """
    model.train()
    total_loss = 0
    for input_tensor, target_tensor in tqdm(dataloader, desc='训练'):
        input_tensor = input_tensor.to(device)
        target_tensor = target_tensor.to(device)
        optimizer.zero_grad()
        outputs = model(input_tensor)
        loss = loss_function(outputs, target_tensor)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(dataloader)
def train():
    """
    模型训练主逻辑。
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    dataloader = get_dataloader(train=True)
    tokenizer = JiebaTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'vocab.txt')
    model = ReviewAnalyzeModel(vocab_size=tokenizer.vocab_size,
                               padding_idx=tokenizer.pad_token_index).to(device)
    loss_function = torch.nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.LEARNING_RATE)
    writer = SummaryWriter(log_dir=config.LOG_DIR / time.strftime('%Y-%m-%d_%H-%M-%S'))
    best_loss = float('inf')
    for epoch in range(1, config.EPOCHS + 1):
        print(f'========== Epoch: {epoch} ==========')
        avg_loss = train_one_epoch(model, dataloader, loss_function, optimizer, device)
        print(f'Loss: {avg_loss:.4f}')
        writer.add_scalar('Loss/Train', avg_loss, epoch)
        # 保存最佳模型
        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save(model.state_dict(), config.MODELS_DIR / 'model.pt')
            print('模型保存成功')
if __name__ == '__main__':
    train()
```
#### 模型预测

```python
### predict.py
import torch
from tokenizer import JiebaTokenizer
from model import ReviewAnalyzeModel
import config
def predict_batch(input_tensor, model):
    """
    对一个批次输入进行预测。
    :param input_tensor: 输入张量 (batch_size, seq_len)
    :param model: 模型
    :return: 概率列表
    """
    model.eval()
    with torch.no_grad():
        logits = model(input_tensor)
    probs = torch.sigmoid(logits)
    return probs.tolist()
def predict(user_input: str, model, tokenizer, device):
    """
    对单条用户输入进行预测。
    :param user_input: 用户输入字符串
    :param model: 模型
    :param tokenizer: 分词器
    :param device: 设备
    :return: 概率值
    """
    input_indexes = tokenizer.encode(user_input, config.SEQ_LEN)
    input_tensor = torch.tensor([input_indexes], dtype=torch.long).to(device)
    probs = predict_batch(input_tensor, model)
    return probs[0]
def run_predict():
    """
    预测交互主逻辑。
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tokenizer = JiebaTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'vocab.txt')
    model = ReviewAnalyzeModel(vocab_size=tokenizer.vocab_size,
                               padding_idx=tokenizer.pad_token_index).to(device)
    model.load_state_dict(torch.load(config.MODELS_DIR / 'model.pt'))
    print('请输入要预测的评论：（输入 q 或 quit 退出）')
    while True:
        user_input = input('> ').strip()
        if user_input in ['q', 'quit']:
            print('退出程序')
            break
        if not user_input:
            print('输入为空，请重新输入')
            continue
        prob = predict(user_input, model, tokenizer, device)
        if prob > 0.5:
            print(f'正面评价（置信度：{prob:.2f}）')
        else:
            print(f'负面评价（置信度：{1 - prob:.2f}）')
if __name__ == '__main__':
    run_predict()
```
#### 模型评估

```python
### evaluate.py
import torch
from tokenizer import JiebaTokenizer
from model import ReviewAnalyzeModel
from dataset import get_dataloader
from predict import predict_batch
import config
def evaluate(model, dataloader, device):
    """
    模型评估。
    :param model: 模型
    :param dataloader: 数据加载器
    :param device: 设备
    :return: 准确率
    """
    model.eval()
    total_count = 0
    correct_count = 0
    for input_tensor, target_tensor in dataloader:
        input_tensor = input_tensor.to(device)
        target_tensor = target_tensor.tolist()
        probs = predict_batch(input_tensor, model)
        for prob, target in zip(probs, target_tensor):
            pred_label = 1 if prob > 0.5 else 0
            if pred_label == target:
                correct_count += 1
            total_count += 1
    return correct_count / total_count
def run_evaluate():
    """
    评估主流程。
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tokenizer = JiebaTokenizer.from_vocab(config.PROCESSED_DATA_DIR / 'vocab.txt')
    model = ReviewAnalyzeModel(vocab_size=tokenizer.vocab_size,
                               padding_idx=tokenizer.pad_token_index).to(device)
    model.load_state_dict(torch.load(config.MODELS_DIR / 'model.pt'))
    dataloader = get_dataloader(train=False)
    acc = evaluate(model, dataloader, device)
    print("========== 评估结果 ==========")
    print(f"准确率：{acc:.4f}")
    print("=============================")
if __name__ == '__main__':
    run_evaluate()
```
#### 配置文件

```python
### config.py
### 配置文件，定义项目路径和超参数
from pathlib import Path
### 项目根目录
ROOT_DIR = Path(__file__).parent.parent
### 数据路径
RAW_DATA_DIR = ROOT_DIR / 'data' / 'raw'
PROCESSED_DATA_DIR = ROOT_DIR / 'data' / 'processed'
### 模型与日志路径
MODELS_DIR = ROOT_DIR / 'models'
LOG_DIR = ROOT_DIR / 'logs'
### 超参数
SEQ_LEN = 128  # 序列长度
BATCH_SIZE = 64  # 批次大小
EMBEDDING_DIM = 64  # 嵌入维度
HIDDEN_DIM = 128  # GRU 隐藏层维度
LEARNING_RATE = 1e-3  # 学习率
EPOCHS = 30  # 训练轮数
```
### 存在问题
GRU 在简化结构、提高训练效率方面表现优秀，但在超长依赖建模、灵活性和并行计算方面仍存在天然限制。

## 4. BERT 迁移学习版本（BERT Transfer Learning, V4.0）
### 需求说明
本案例任务是基于预训练 BERT 模型实现评论的情感分析任务。
### 需求实现
#### 项目结构

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-202608201140188.png]]
#### 完整代码
##### 数据预处理

```python
### process.py
from datasets import load_dataset, ClassLabel
from transformers import AutoTokenizer
import config
def process_data():
    # 加载原始 CSV 数据
    dataset = load_dataset('csv', data_files=str(config.RAW_DATA_DIR / 'online_shopping_10_cats.csv'))['train']
    # 过滤空评论和非二分类标签
    dataset = dataset.filter(lambda x: x['review'] is not None and x['review'].strip() != '' and x['label'] in [0, 1])
    # 划分训练集和测试集
    dataset = dataset.cast_column("label", ClassLabel(names=["neg", "pos"]))
    dataset_dict = dataset.train_test_split(test_size=0.2, seed=42, stratify_by_column='label')
    print("数据划分完成")
    # 加载分词器
    tokenizer = AutoTokenizer.from_pretrained(config.PRE_TRAINED_DIR / 'bert-base-chinese')
    # 编码函数
    def tokenize(example):
        encoded = tokenizer(
            example['review'],
            max_length=config.SEQ_LEN,
            truncation=True,
            padding='max_length'
        )
        return {
            'input_ids': encoded['input_ids'],
            'attention_mask': encoded['attention_mask']
        }
    # 对训练和测试集分别编码
    dataset_dict = dataset_dict.map(tokenize, batched=True)
    print("分词完成")
    # 删除字段
    dataset_dict = dataset_dict.remove_columns(['review', 'cat'])
    # 保存处理结果
    dataset_dict['train'].save_to_disk(str(config.PROCESSED_DATA_DIR / 'train'))
    dataset_dict['test'].save_to_disk(str(config.PROCESSED_DATA_DIR / 'test'))
    print("保存完成")
if __name__ == '__main__':
    process_data()
```
##### 自定义数据集

```python
### dataset.py
from datasets import load_from_disk
from torch.utils.data import DataLoader
import config
def get_dataset(train=True):
    path = config.PROCESSED_DATA_DIR / ('train' if train else 'test')
    dataset = load_from_disk(str(path))
    # 设置为 PyTorch 格式，列自动转换为 tensor
    dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])
    return dataset
def get_dataloader(train=True):
    dataset = get_dataset(train)
    return DataLoader(dataset, batch_size=config.BATCH_SIZE, shuffle=True)
### 数据加载测试入口
if __name__ == '__main__':
    dataloader = get_dataloader(train=True)
    for batch in dataloader:
        print({k: v.shape for k, v in batch.items()})
        break
```
##### 模型定义

```python
### model.py
import torch.nn as nn
from transformers import AutoModel
import config
class ReviewAnalyzeModel(nn.Module):
    def __init__(self, freeze_bert=True):
        super().__init__()
        # 加载本地预训练的 BERT 模型
        self.bert = AutoModel.from_pretrained(config.PRE_TRAINED_DIR / 'bert-base-chinese')
        # 分类器：接收 [CLS] 向量 → 输出二分类的得分
        self.classifier = nn.Linear(self.bert.config.hidden_size, 1)
        # self.classifier 输入: (batch_size, hidden_size)
        # self.classifier 输出: (batch_size, 1)
        # 是否冻结 BERT 参数（只训练分类器部分）
        if freeze_bert:
            for param in self.bert.parameters():
                param.requires_grad = False
    # 前向传播过程
    def forward(self, input_ids, attention_mask):
        # input_ids.shape: (batch_size, seq_len)
        # attention_mask.shape: (batch_size, seq_len)
        # BERT 输出是命名元组，包含多个字段,其中last_hidden_state最后一层所有 token 的输出
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        # outputs.last_hidden_state.shape: (batch_size, seq_len, hidden_size)
        # 提取 [CLS] token（第一个位置）的输出向量
        cls_output = outputs.last_hidden_state[:, 0, :]  # cls_output.shape: (batch_size, hidden_size)
        # 通过线性层生成 logits
        logits = self.classifier(cls_output)  # logits.shape: (batch_size, 1)
        return logits.squeeze(-1)  # 返回形状: (batch_size,)
```
##### 模型训练

```python
### train.py
import time
import torch
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
import config
from dataset import get_dataloader
from model import ReviewAnalyzeModel
def train_one_epoch(model, dataloader, optimizer, loss_fn, device):
    model.train()
    total_loss = 0
    for batch_index, batch in enumerate(tqdm(dataloader, desc="训练")):
        input_ids = batch['input_ids'].to(device)  # input_ids.shape: (batch_size, seq_len)
        attention_mask = batch['attention_mask'].to(device)  # attention_mask.shape: (batch_size, seq_len)
        labels = batch['label'].float().to(device)  # labels.shape: (batch_size,)
        # 清除历史梯度
        optimizer.zero_grad()
        # 模型前向传播
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        # outputs.shape: (batch_size,)
        # 计算损失
        loss = loss_fn(outputs, labels)
        # 反向传播并更新参数
        loss.backward()
        optimizer.step()
        # 统计与显示损失
        total_loss += loss.item()
    avg_loss = total_loss / len(dataloader)
    return avg_loss
### 模型训练主函数
def train():
    # 选择运行设备
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}")
    # 加载训练数据集
    dataloader = get_dataloader(train=True)
    print("数据集加载完成")
    # 初始化模型并移动到设备
    model = ReviewAnalyzeModel(freeze_bert=False).to(device)
    # 使用 Adam 优化器
    optimizer = torch.optim.Adam(model.parameters(), lr=config.LEARNING_RATE)
    # 使用带 sigmoid 的二分类交叉熵损失函数
    loss_function = torch.nn.BCEWithLogitsLoss()
    # 初始化 TensorBoard 写入器
    log_dir = config.LOGS_DIR / time.strftime("%Y%m%d-%H%M%S")
    writer = SummaryWriter(log_dir=str(log_dir))
    # 多轮训练
    best_loss = float("inf")
    for epoch in range(1, config.EPOCHS + 1):
        print(f"========== Epoch {epoch} ==========")
        avg_loss = train_one_epoch(model, dataloader, optimizer, loss_function, device)
        print(f"训练集loss: {avg_loss:.4f}")
        # 写入 TensorBoard 日志
        writer.add_scalar("Loss/train", avg_loss, epoch)
        # 保存训练好的模型
        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save(model.state_dict(), config.MODELS_DIR / 'model.pt')
    writer.close()
if __name__ == '__main__':
    train()
```
##### 模型预测

```python
### predict.py
import torch
from transformers import AutoTokenizer
import config
from model import ReviewAnalyzeModel
### 对一个 batch 的输入进行预测，返回 sigmoid 概率
def predict_batch(input_ids, attention_mask, model):
    model.eval()
    # input_ids.shape: (batch_size, seq_len)
    # attention_mask.shape: (batch_size, seq_len)
    with torch.no_grad():
        logits = model(input_ids=input_ids, attention_mask=attention_mask)
        # logits.shape: (batch_size,)
        probs = torch.sigmoid(logits)  # 概率值 ∈ [0, 1]，表示为正面情感的置信度
        return probs.tolist()  # 返回 Python 列表
def predict_text(user_input, model, tokenizer, device):
    # 文本编码为张量形式（长度固定）
    encoded = tokenizer(
        user_input,
        max_length=config.SEQ_LEN,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    input_ids = encoded['input_ids'].to(device)  # input_ids.shape: (1, seq_len)
    attention_mask = encoded['attention_mask'].to(device)  # attention_mask.shape: (1, seq_len)
    # 模型预测
    prob = predict_batch(input_ids, attention_mask, model)[0]
    return prob
### 交互式预测主程序
def run_predict():
    # 设置运行设备
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # 加载分词器和模型
    tokenizer = AutoTokenizer.from_pretrained(config.PRE_TRAINED_DIR / 'bert-base-chinese')
    model = ReviewAnalyzeModel().to(device)
    model.load_state_dict(torch.load(config.MODELS_DIR / 'model.pt', map_location=device))
    # 命令行交互循环
    print('请输入评价（输入q 或者 quit 退出）：')
    while True:
        user_input = input('> ').strip()
        # 输入为空或退出
        if user_input.lower() in {'q', 'quit'}:
            print('感谢使用，再见！')
            break
        if not user_input:
            print('输入不能为空，请重新输入')
            continue
        result = predict_text(user_input, model, tokenizer, device)
        # 显示结果
        if result > 0.5:
            print(f"正面评价（置信度：{result:.2f}）")
        else:
            print(f"负面评价（置信度：{1 - result:.2f}）")
if __name__ == '__main__':
    run_predict()
```
##### 模型评估

```python
### evaluate.py
import torch
from tqdm import tqdm
import config
from dataset import get_dataloader
from model import ReviewAnalyzeModel
from predict import predict_batch
def evaluate_model(dataloader, model, device):
    correct = 0
    total = 0
    for batch in tqdm(dataloader, desc="评估"):
        input_ids = batch['input_ids'].to(device)  # input_ids.shape: (batch_size, seq_len)
        attention_mask = batch['attention_mask'].to(device)  # attention_mask.shape: (batch_size, seq_len)
        labels = batch['label'].to(device)  # labels.shape: (batch_size,)
        # 预测每个样本的正面情感概率
        probs = predict_batch(input_ids, attention_mask, model)  # probs 是 float 列表
        # 将概率转换为预测标签（>= 0.5 为正面）
        preds = [1 if p >= 0.5 else 0 for p in probs]
        # 计算准确数量
        for pred, label in zip(preds, labels):
            if pred == int(label.item()):
                correct += 1
            total += 1
    # 输出准确率
    acc = correct / total if total > 0 else 0
    print("======= 评估结果 =======")
    print(f"准确率: {acc:.4f}")
    print("========================")
def run_evaluate():
    # 设置运行设备
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # 加载模型
    model = ReviewAnalyzeModel().to(device)
    model.load_state_dict(torch.load(config.MODELS_DIR / 'model.pt', map_location=device))
    # 加载测试数据集
    dataloader = get_dataloader(train=False)
    # 执行评估
    evaluate_model(dataloader, model, device)
if __name__ == '__main__':
    run_evaluate()
```
##### 配置文件

```python
### config.py
from pathlib import Path
### 项目根目录
BASE_DIR = Path(__file__).parent.parent
### 路径设置
MODELS_DIR = BASE_DIR / 'models'  # 模型参数保存路径
PROCESSED_DATA_DIR = BASE_DIR / 'data' / 'processed'  # 已处理数据存放路径（如 token 序列）
RAW_DATA_DIR = BASE_DIR / 'data' / 'raw'  # 原始 CSV 或文本数据路径
LOGS_DIR = BASE_DIR / 'logs'  # TensorBoard 日志保存路径
PRE_TRAINED_DIR = BASE_DIR / 'pretrained'  # 本地预训练模型存放路径
### 训练超参数
SEQ_LEN = 128  # 最大序列长度
BATCH_SIZE = 128  # 批处理大小
LEARNING_RATE = 1e-5  # 学习率
EPOCHS = 30  # 训练轮数
```

## 5. 版本选择（Version Selection）

|版本（Version）|优势（Strength）|主要限制（Limitation）|适用场景（Use Case）|
|---|---|---|---|
|RNN|结构最简单，便于理解序列分类主流程|长序列梯度传播困难|教学基线、小数据快速验证|
|LSTM|记忆单元与门控更适合长期依赖|参数量与计算量较大|需要较长上下文的传统序列任务|
|GRU|门控更精简，通常比 LSTM 更轻|表达上限仍受传统循环结构限制|训练资源较紧的序列分类|
|BERT|预训练上下文表示强，迁移效果通常更好|显存、推理延迟与版本依赖更高|效果优先、数据量有限的文本分类|
## 6. 失败模式与排错（Failure Modes and Troubleshooting）
- **标签类型（Label Type）**：`BCEWithLogitsLoss` 要求目标为浮点数且形状与 logits 一致；标签若为 `LongTensor` 会报类型错误。
- **长度与掩码（Length and Mask）**：RNN/LSTM/GRU 使用填充序列时必须确保长度排序、`enforce_sorted` 与真实数据一致；BERT 必须同时传入 `attention_mask`，否则填充位置会参与注意力计算。
- **加载位置（Load Location）**：使用 `map_location=device` 加载权重，避免在 CPU 机器上直接加载 CUDA 权重失败。
- **训练/评估模式（Train/Eval Mode）**：训练前调用 `model.train()`，预测与评估前调用 `model.eval()` 并进入 `torch.no_grad()`。
- **类别不平衡（Class Imbalance）**：仅报告准确率（Accuracy）可能掩盖少数类失败；工程中应追加精确率（Precision）、召回率（Recall）、F1 和混淆矩阵（Confusion Matrix）。
