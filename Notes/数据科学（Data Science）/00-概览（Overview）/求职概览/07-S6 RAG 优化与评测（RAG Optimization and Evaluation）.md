---
title: "S6 RAG 优化与评测（RAG Optimization and Evaluation）"
aliases:
  - "S6 RAG Optimization and Evaluation"
tags:
  - career/llm-application-engineer
  - interview/rag-evaluation
status: published
created: 2026-08-27
updated: 2026-08-27
---
# S6 RAG 优化与评测（RAG Optimization and Evaluation）
> [!tip] 导航（Navigation）
> 上一阶段：[[06-S5 AI 后端工程化（AI Backend Engineering）]]｜[[00-概览（Overview）]]｜下一阶段：[[08-S7 Agent 与工作流（Agents and Workflows）]]
## 1. 评测集、标注与数据隔离（Evaluation Sets, Labels, and Data Separation）
### 概念与原理（Concept and Mechanism）
- 每个评测问题应记录参考答案或关键要点、支持答案的文档与 Chunk、问题类型和是否应拒答。
- 题型至少覆盖直接事实、跨段综合、歧义、时效冲突和无答案问题。开发集（Development Set）用于调参数，测试集（Test Set）只在方案固定后使用。
- 评测答案、标准 Chunk 或测试问题不能进入被评系统的知识库或 Prompt，否则形成评测泄漏（Evaluation Leakage）。

### 最小代码示例（Minimal Example）
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class EvaluationCase:
    question: str
    expected_points: tuple[str, ...]
    relevant_chunk_ids: frozenset[str]
    should_abstain: bool = False

case = EvaluationCase("保修期多久？", ("两年",), frozenset({"manual#12"}))
print(case.should_abstain)  # 输出: False
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么不能一边看测试集结果一边调 Chunk Size？**

**参考答案：**反复依据测试集调参会让方案间接拟合测试样本，使最终指标过于乐观。应在开发集上选策略，保留独立测试集进行最终评估。

## 2. BM25、向量检索与混合检索（BM25, Dense Retrieval, and Hybrid Search）
### 概念与原理（Concept and Mechanism）
- BM25 是稀疏关键词检索（Sparse Retrieval），依据词频、逆文档频率和长度归一化评分，擅长精确术语、编号和专有名词。
- 向量检索（Dense Retrieval）依据语义表示匹配改写和近义表达，但可能忽略精确数字或罕见 Token。
- 混合检索（Hybrid Search）结合两类候选。分数尺度不一致时，可使用倒数排名融合（Reciprocal Rank Fusion, RRF）按名次融合，再交给重排器（Reranker）。

> [!tip] 大白话理解（Plain-language Intuition）
> BM25 像按原词查目录，向量检索像按意思找近义内容。一个擅长“字面完全命中”，一个擅长“换了说法也能找到”，混合检索同时保留两条线索。

### 最小代码示例（Minimal Example）
```python
from collections import defaultdict

def reciprocal_rank_fusion(rankings: list[list[str]], constant: int = 60) -> list[str]:
    scores: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for rank, document_id in enumerate(ranking, start=1):
            scores[document_id] += 1 / (constant + rank)
    return sorted(scores, key=scores.get, reverse=True)

print(reciprocal_rank_fusion([["A", "B"], ["B", "C"]]))  # 输出: ['B', 'A', 'C']
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么不能直接把 BM25 分数与余弦相似度相加？**

**参考答案：**两种分数的范围、分布和含义不同，直接相加会让某一检索器因尺度占优势。可以先归一化并校准权重，或使用 RRF 这类只依赖排名的方法。

## 3. Metadata Filter、Reranker 与 Query Rewrite（Metadata Filtering, Reranking, and Query Rewriting）
### 概念与原理（Concept and Mechanism）
- Metadata Filter 先约束租户、时间、文档类型和版本，再在合法候选中检索。
- Reranker 对第一阶段召回的较小候选集进行更精细的“查询—文档”相关性评分；它通常提高排序质量，但增加延迟和成本。
- Query Rewrite 可补全上下文、展开缩写或生成检索表达，但必须保留原始问题，避免改写偏离用户意图。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么不直接用 Reranker 扫描全部文档？**

**参考答案：**交叉编码式重排通常需要对每个查询—文档对执行较昂贵模型计算，不适合全库扫描。常用两阶段架构先快速召回几十到几百个候选，再重排较小集合。

## 4. Recall@K、MRR 与 NDCG（Retrieval Metrics）
### 概念与原理（Concept and Mechanism）
- Recall@K 衡量前 K 个结果覆盖了多少相关文档，适合关注“证据是否被找回”。
- 平均倒数排名（Mean Reciprocal Rank, MRR）关注第一个相关结果的位置，单题倒数排名为 $1/rank$。
- 归一化折损累计增益（Normalized Discounted Cumulative Gain, NDCG）支持多级相关性，并对高排名结果赋予更大权重。

### 最小代码示例（Minimal Example）
```python
def recall_at_k(ranked_ids: list[str], relevant_ids: set[str], k: int) -> float:
    if not relevant_ids:
        raise ValueError("相关文档集合不能为空")
    return len(set(ranked_ids[:k]) & relevant_ids) / len(relevant_ids)

def reciprocal_rank(ranked_ids: list[str], relevant_ids: set[str]) -> float:
    return next((1 / rank for rank, item in enumerate(ranked_ids, 1) if item in relevant_ids), 0.0)

ranked = ["d3", "d1", "d2"]
relevant = {"d1", "d2"}
print(recall_at_k(ranked, relevant, 2))  # 输出: 0.5
print(reciprocal_rank(ranked, relevant)) # 输出: 0.5
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：Recall@K 提高后，最终回答为什么可能变差？**

**参考答案：**召回更多正确证据的同时也可能引入大量干扰项；排序、上下文去重或生成模型可能无法分辨冲突。应联合评估候选精度、重排、上下文质量、答案正确性、忠实度、延迟和成本。

## 5. 生成正确性、忠实度、引用与拒答（Correctness, Faithfulness, Citations, and Abstention）
### 概念与原理（Concept and Mechanism）
- 正确性（Correctness）比较答案与可信事实；忠实度（Faithfulness）检查答案陈述是否得到提供上下文支持；引用准确性检查引用片段是否真正支撑相邻结论。
- 无答案评测检查证据不足时是否拒答。模型可能正确地引用了材料，却回答了错误问题；也可能答案事实正确，但不受本次上下文支持，因此指标必须分开。

### 最小代码示例（Minimal Example）
```python
def citation_precision(claim_support: list[bool]) -> float:
    return sum(claim_support) / len(claim_support) if claim_support else 0.0

print(citation_precision([True, False, True]))  # 输出: 0.6666666666666666
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：答案正确是否意味着 RAG 系统正确？**

**参考答案：**不一定。模型可能依靠参数记忆碰巧答对，却没有使用检索证据；在私有或时效知识中这种答案不可追踪。应同时检查检索证据、忠实度和引用支持。

## 6. LLM-as-a-Judge 与人工抽查（LLM-as-a-Judge and Human Review）
### 概念与原理（Concept and Mechanism）
- LLM-as-a-Judge 使用模型按量表评价答案，适合大规模初筛复杂语言质量，但会受提示、模型偏好、答案长度、位置和自我偏好影响。
- 量表必须定义评分标准和示例；评审模型、版本和 Prompt 应固定并记录；关键样本和分歧样本需要人工抽查。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：如何验证 LLM Judge 是否可信？**

**参考答案：**建立人工标注子集，计算 Judge 与人工的一致性，检查不同题型和分数段偏差；对模型版本、提示顺序和答案位置做敏感性测试，并保存 Judge 理由供审计。

## 7. Bad Case 分类与受控实验（Bad-case Taxonomy and Controlled Experiments）
### 概念与原理（Concept and Mechanism）
- 失败应区分解析、切块、查询、召回、过滤、排序、上下文、生成、引用和权限问题。分类后才能选择对应改动。
- 每次实验只改变少量变量，记录数据版本、模型、Chunk 配置、Top-K、重排、Prompt、随机参数、指标、延迟和成本。
- 回归测试（Regression Test）确保修复一种错误后，没有破坏既有正确案例。

### 最小代码示例（Minimal Example）
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Experiment:
    name: str
    chunk_size: int
    top_k: int
    use_reranker: bool

baseline = Experiment("baseline", chunk_size=400, top_k=5, use_reranker=False)
candidate = Experiment("reranked", chunk_size=400, top_k=20, use_reranker=True)
print(baseline.chunk_size == candidate.chunk_size)  # 输出: True
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：如何证明 Reranker 真正带来提升？**

**参考答案：**固定数据、切块、Embedding 和生成设置，只改变候选数量与重排步骤，在同一评测集比较 Recall、MRR/NDCG、最终答案、延迟和成本，并对改善与退化案例分类分析。

## 8. 可评测企业级 RAG 的面试表达（Evaluated RAG Interview Framing）
- **评测集（Evaluation Set）**：至少覆盖事实、跨段、歧义和无答案问题，并标注相关 Chunk。
- **对照实验（Ablation）**：比较两种 Chunk 配置、稀疏与向量检索、混合检索以及加入 Reranker 前后。
- **指标（Metrics）**：Recall@K、MRR/NDCG、答案正确性、忠实度、引用准确性、拒答、P50/P95 延迟和成本。
- **证据（Evidence）**：保存配置、结果、图表和至少 20 个 Bad Case；不能只展示挑选出的成功示例。
- **高频追问（Common Follow-up）**：指标下降如何定位？先看检索命中和排名，再检查最终上下文，最后检查生成与引用，按阶段缩小范围。

## 参考资料（References）
- [[大模型应用工程师学习计划]]
- [pgvector 混合检索与重排说明](https://github.com/pgvector/pgvector#hybrid-search)
