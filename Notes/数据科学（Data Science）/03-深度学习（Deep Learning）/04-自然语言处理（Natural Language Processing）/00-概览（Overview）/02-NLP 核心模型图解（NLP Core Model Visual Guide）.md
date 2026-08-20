---
title: "NLP 核心模型图解（NLP Core Model Visual Guide）"
tags:
  - data-science/nlp
  - diagrams
status: published
created: 2026-08-20
published_at: 2026-08-20
---
# NLP 核心模型图解（NLP Core Model Visual Guide）
> [!tip] 使用方法（How to Use）
> 本笔记只集中索引已经被正式知识笔记使用的图示；正文概念请沿 Wiki Link 进入对应专题。未进入知识正文的原稿图片已在用户批准后移入 macOS 废纸篓。
## 1. 主题导航（Topic Navigation）
- [[01-自然语言处理概览（NLP Overview）]]
- [[02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）]]
- [[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）]]
- [[03-Seq2Seq 与注意力机制（Seq2Seq and Attention）]]
- [[01-Transformer 架构与注意力（Transformer Architecture and Attention）]]
- [[05-BERT 原理与模型族（BERT Principles and Family）]]
- [[07-电商评论情感分类演进（E-commerce Review Sentiment Classification Evolution）]]
## 2. 已使用图示（Figures Used by Published Notes）
### 2.1 已并入正式笔记的图示（Figures Used by Published Notes）
- 以下图示均被 [[07-电商评论情感分类演进（E-commerce Review Sentiment Classification Evolution）]] 正文引用；这里只保留集中索引。
- **RNN 评论分类模型结构（RNN Review-classification Architecture）**
  ![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114045.png]]
- **RNN 评论分类项目结构（RNN Review-classification Project Structure）**
  ![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114046.png]]
- **RNN 长期依赖问题（RNN Long-term Dependency Problem）**
  ![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114047.png]]
- **随时间反向传播计算图（Backpropagation Through Time Graph）**
  ![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114048.png]]
- **RNN 梯度连乘与梯度消失（RNN Gradient Products and Vanishing Gradients）**
  ![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114050.png]]
- **LSTM 评论分类项目结构（LSTM Review-classification Project Structure）**
  ![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114073.png]]
- **GRU 评论分类项目结构（GRU Review-classification Project Structure）**
  ![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-20260820114091.png]]
- **BERT 评论分类项目结构（BERT Review-classification Project Structure）**
  ![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/00-概览（Overview）/02-NLP 核心模型图解（NLP Core Model Visual Guide）/02-NLP 核心模型图解（NLP Core Model Visual Guide）-202608201140188.png]]
