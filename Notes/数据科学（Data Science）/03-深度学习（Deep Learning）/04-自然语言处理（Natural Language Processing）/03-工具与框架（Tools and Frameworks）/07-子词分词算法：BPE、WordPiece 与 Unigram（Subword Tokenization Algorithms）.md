---
title: "子词分词算法：BPE、WordPiece 与 Unigram（Subword Tokenization Algorithms）"
tags:
  - data-science/nlp
  - tokenization
status: published
created: 2026-08-20
published_at: 2026-08-20
---
# 子词分词算法：BPE、WordPiece 与 Unigram（Subword Tokenization Algorithms）
## 1. 为什么使用子词（Why Subwords）
- **词级分词（Word-level Tokenization）**直观，但词表大，遇到新词、拼写变体和复合词时容易产生未登录词（Out-of-vocabulary, OOV）。
- **字符级分词（Character-level Tokenization）**几乎不产生 OOV，但序列更长，单个字符携带的语义较弱，模型需要更长上下文才能组合出词义。
- **子词分词（Subword Tokenization）**位于两者之间：高频词或片段保留为一个 Token，低频词拆成多个可复用片段，从而在词表大小、序列长度和 OOV 风险之间折中。
> [!tip] 大白话理解（Plain-language Intuition）
> 子词词表像一盒“常用积木”。常见词直接用一块积木，罕见词则用几块较小积木拼出来；盒子不需要收录世界上每个完整单词，也不必把所有内容拆到单个字符。
## 2. 分词粒度与语言差异（Granularity and Language Differences）
### 2.1 英文（English）
- 词级通常利用空格和标点作为初步边界，但新词、专有名词、复合词和形态变化仍会造成 OOV。
- 字符级词表小、覆盖率高，却会显著拉长序列。
- 子词可以复用词根、前缀、后缀或高频字符片段，通常更适合预训练语言模型（Pretrained Language Model）。
### 2.2 中文（Chinese）
- 汉字本身常带语义，因此字符级方案比英文字符级更可行。
- 词级分词需要词典、规则或模型判断没有空格标记的词边界。
- 子词算法可把汉字作为初始单位，从语料中学习“自然”“语言”“处理”等高频组合，不要求人工维护完整词典。
## 3. BPE（Byte Pair Encoding）
### 3.1 训练过程（Training）
1. 把语料中的词拆为字符或字节等初始符号，并统计频率。
2. 找出当前最常见的相邻 Token 对。
3. 合并该对，产生一个新 Token，并记录合并规则（Merge Rule）。
4. 重复统计与合并，直到达到目标词表大小或停止条件。
### 3.2 编码过程（Encoding）
- 对输入应用训练阶段学到的合并规则；规则顺序会影响最终切分。
- 罕见词只要能由基础符号组成，就可以拆成多个子词，减少整体退化为 `<unk>` 的概率。
### 3.3 特点与边界（Characteristics and Boundaries）
- 高频相邻片段更容易成为完整 Token，词表利用率高且实现直观。
- 纯字符 BPE 仍可能遇到未覆盖字符；字节级 BPE（Byte-level BPE）把输入退化到字节，覆盖能力更强，但可读性会下降。
- 训练语料的频率分布直接影响合并规则；领域迁移后，专业词可能被拆得过碎。
## 4. WordPiece
### 4.1 核心思想（Core Idea）
- WordPiece 与 BPE 都从较小单位逐步学习子词，但选择合并对时使用的评分会倾向于组合“共同出现强、各自又不算过度常见”的片段，而不是只看相邻对的绝对频率。
- 推理时通常不重放完整合并规则，而是在最终词表中执行最长匹配优先（Longest-match-first）：从词首寻找最长可用子词，再继续处理剩余部分。
- BERT 风格词表常用 `##` 表示“该子词继续前一个词”，例如 `hug` + `##s`。
> [!tip] 大白话理解（Plain-language Intuition）
> WordPiece 像从单词左侧开始用“最长能匹配的积木”铺过去；当前位置找不到任何积木时，整个词可能回退为 `[UNK]`，因此词表覆盖与规范化规则非常重要。
## 5. Unigram
### 5.1 训练过程（Training）
1. 从一个较大的候选子词词表开始。
2. 用一元语言模型（Unigram Language Model）为每个子词分配概率。
3. 估计删除每个候选子词会让整个语料损失增加多少。
4. 优先剪掉影响最小的候选，重新估计概率，直到达到目标词表大小。
### 5.2 编码过程（Encoding）
- 同一句文本往往存在多种合法切分；Unigram 在分词网格（Segmentation Lattice）中寻找概率最大的路径。
- 与按固定顺序重放合并规则的 BPE 不同，它可以比较整条切分路径的概率；某些实现还支持从多个高概率切分中采样，用于子词正则化（Subword Regularization）。
> [!tip] 大白话理解（Plain-language Intuition）
> Unigram 先准备一大盒积木，再不断淘汰“拿掉也不太影响拼句子”的积木；真正分词时，它会比较多种拼法，选整体最合理的一种。
## 6. 三种算法对比（Comparison）

|维度（Dimension）|BPE|WordPiece|Unigram|
|---|---|---|---|
|训练起点|小词表，逐步合并|小词表，按评分逐步合并|大候选词表，逐步剪枝|
|训练决策|最高频相邻对|偏向关联强的相邻对|删除后语料损失增量|
|推理方式|按已学习的合并规则切分|最长匹配优先|选择概率最大的完整切分|
|典型标记|依实现而定|常见 `##` 续接前缀|SentencePiece 常见 `▁` 空格标记|
|主要风险|领域变化导致切分过碎|无法完全覆盖时可能产生 `[UNK]`|训练与解码实现更复杂|
## 7. Tokenizer 流水线（Tokenizer Pipeline）
1. **规范化（Normalization）**：Unicode 规范化、大小写处理、去重音符号等；必须与模型预训练时的策略一致。
2. **预分词（Pre-tokenization）**：先按空格、标点、字节或其他边界拆分输入。
3. **模型（Model）**：由 BPE、WordPiece 或 Unigram 把预分词结果拆为子词并映射到 ID。
4. **后处理（Post-processing）**：加入 `[CLS]`、`[SEP]` 等特殊 Token，并生成句段标记。
5. **解码（Decoding）**：根据模型的续接符、空格标记或字节编码还原可读文本。
## 8. 工程注意事项（Engineering Notes）
- 模型与 Tokenizer 必须成对加载；即使模型结构相同，换词表也会让同一个 ID 表示完全不同的 Token。
- 修改规范化、预分词或特殊 Token 后，旧权重不一定仍兼容；新增 Token 时通常还要调用模型的嵌入矩阵扩容接口。
- 对命名实体识别（Named Entity Recognition, NER）等 Token 级任务，应使用快速分词器（Fast Tokenizer）的偏移映射（Offset Mapping）或词对齐接口，把子词结果映射回原字符/原词。
- 不应仅比较词表大小；还要观察平均序列长度、未知 Token 比例、领域词切分质量、训练吞吐与下游指标。
## 9. 官方参考（Official References）
- [Hugging Face Tokenizers Models API](https://huggingface.co/docs/tokenizers/en/api/models)
- [Hugging Face Tokenizer 组件（Components）](https://huggingface.co/docs/tokenizers/python/latest/components.html)
- [Hugging Face WordPiece 教程](https://huggingface.co/docs/course/chapter6/6)
- [Hugging Face Unigram 教程](https://huggingface.co/learn/llm-course/chapter6/7)
