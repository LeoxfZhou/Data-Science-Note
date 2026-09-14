---
title: "S4 RAG 基础（RAG Fundamentals）"
aliases:
  - "S4 RAG Fundamentals"
tags:
  - career/llm-application-engineer
  - interview/rag
status: published
created: 2026-08-27
updated: 2026-08-27
---
# S4 RAG 基础（RAG Fundamentals）
> [!tip] 导航（Navigation）
> 上一阶段：[[04-S3 大模型应用基础（LLM Application Fundamentals）]]｜[[00-概览（Overview）]]｜下一阶段：[[06-S5 AI 后端工程化（AI Backend Engineering）]]
## 1. RAG 数据流与职责边界（RAG Data Flow and Boundaries）
### 概念与原理（Concept and Mechanism）
- 检索增强生成（Retrieval-Augmented Generation, RAG）在回答前从外部知识库检索证据，再把证据与问题交给生成模型。典型离线链路为采集 → 解析 → 清洗 → 切块 → Embedding → 建索引；在线链路为查询处理 → 检索 → 重排 → 上下文组装 → 生成 → 引用与校验。
- RAG 不会把知识写进模型参数。它提升可更新性和可追溯性，但答案质量仍受解析、切块、召回、排序和生成各阶段影响。

> [!tip] 大白话理解（Plain-language Intuition）
> RAG 像开卷考试：检索系统负责找资料，生成模型负责依据资料组织答案。找错页是检索问题，看到了正确页却答错是生成问题。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：RAG 与微调（Fine-tuning）如何选择？**

**参考答案：**需要频繁更新、引用来源或使用私有事实知识时优先 RAG；需要稳定改变模型行为、风格或特定任务能力时考虑微调。两者可以组合：微调改善行为，RAG 提供动态事实。不能用微调替代权限隔离和实时知识更新。

## 2. 文档解析、Metadata 与 OCR（Document Parsing, Metadata, and OCR）
### 概念与原理（Concept and Mechanism）
- 文档解析应同时产出正文与元数据（Metadata），例如来源 ID、文件名、页码、标题路径、时间、权限域和内容哈希。
- 页眉页脚、乱码、重复文本和空内容会污染检索。扫描 PDF 只有图像层，需要光学字符识别（Optical Character Recognition, OCR）；不能把解析得到的空字符串当成“没有内容”。
- 解析失败应记录状态与原因，不应向索引写入空 Chunk。

### 最小代码示例（Minimal Example）
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ParsedPage:
    source_id: str
    page_number: int
    title_path: tuple[str, ...]
    text: str

page = ParsedPage("manual-v1", 12, ("安装", "GPU"), "检查驱动版本")
print(page.page_number)  # 输出: 12
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么 Metadata 对 RAG 很重要？**

**参考答案：**它用于权限过滤、版本过滤、引用回溯、时间筛选和定位原文。只有向量和文本而没有稳定来源信息，系统很难证明答案依据、删除某份文档或隔离不同用户数据。

## 3. Chunking 策略（Chunking Strategies）
### 概念与原理（Concept and Mechanism）
- 固定长度切分实现简单但可能截断语义；递归切分按段落、句子等分隔符逐级拆分；标题切分保留文档结构；语义切分依据嵌入或模型判断主题边界，成本更高。
- Chunk Size 太小会丢失上下文并增加索引数量，太大会混入无关内容并占用上下文窗口；Overlap 减少边界信息损失，但会造成重复召回和存储增长。
- Chunk 必须保留与原文位置的稳定关联，并记录切分配置，以便重新索引和实验复现。

### 最小代码示例（Minimal Example）
```python
def sliding_chunks(text: str, size: int, overlap: int) -> list[str]:
    if not 0 <= overlap < size:
        raise ValueError("overlap 必须满足 0 <= overlap < size")
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        if end == len(text):  # 最后一个完整片段已经覆盖文本末尾，避免再产生重复尾片段。
            break
        start = end - overlap
    return chunks

print(sliding_chunks("ABCDEFGHIJ", size=4, overlap=1))  # 输出: ['ABCD', 'DEFG', 'GHIJ']
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：法规、财报和产品说明书应使用同一 Chunk Size 吗？**

**参考答案：**不应该机械统一。法规适合保留条款和层级，财报需要保留表格与章节语境，说明书需要保留步骤和警告的邻接关系。Chunk Size 应通过文档结构、典型问题和检索评测共同确定。

## 4. Embedding、余弦相似度与向量索引（Embeddings, Cosine Similarity, and Vector Indexes）
### 概念与原理（Concept and Mechanism）
- 嵌入向量（Embedding）把文本映射到连续空间，使语义相近内容在所选距离度量下更接近；向量保存的是数值表示，不是原文替代品。
- 余弦相似度比较方向：$\cos(\theta)=\frac{x\cdot y}{\|x\|\|y\|}$。归一化后，点积与余弦排序可等价，但必须确认索引和模型使用的度量契约。
- 精确检索遍历完整候选保证召回；近似最近邻（Approximate Nearest Neighbor, ANN）以部分召回换速度和规模。FAISS、Chroma 或 pgvector 都必须与原文存储和 Metadata 关联。

> [!tip] 大白话理解（Plain-language Intuition）
> Embedding 像把句子的含义放到一张多维地图上，检索是在地图中找近邻。地图坐标不能还原完整原文，所以原文和来源仍要单独保存。

### 最小代码示例（Minimal Example）
```python
from math import sqrt

def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = sqrt(sum(value * value for value in left))
    right_norm = sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        raise ValueError("零向量没有可定义的余弦方向")
    return dot / (left_norm * right_norm)

print(round(cosine_similarity([1, 0], [1, 1]), 3))  # 输出: 0.707
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么向量数据库不能作为唯一数据源？**

**参考答案：**向量索引用于相似度检索，可能近似、可重建且缺少完整事务语义；系统仍需保存原文、版本、权限和处理状态。删除或更新文档时，应以主数据记录协调向量索引，而不是只操作向量。

### 相关笔记（Related Notes）
- [[02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）]]

## 5. 查询、Top-K 与 Metadata Filter（Querying, Top-K, and Metadata Filtering）
### 概念与原理（Concept and Mechanism）
- 查询应使用与文档相同且版本一致的 Embedding 模型。Top-K 控制进入候选集的数量：太小可能漏证据，太大会增加噪声、重排成本和上下文占用。
- Metadata Filter 应在检索阶段强制执行租户、权限、文档版本和时间条件，不能先跨用户召回再依赖模型忽略越权内容。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：Top-K 越大，召回效果一定越好吗？**

**参考答案：**Recall 通常可能提高，但无关候选、延迟和后续成本也会增加，最终答案甚至可能变差。应在评测集上联合观察 Recall@K、重排效果、生成正确性、延迟和成本。

## 6. 上下文组装、引用与拒答（Context Assembly, Citations, and Abstention）
### 概念与原理（Concept and Mechanism）
- 上下文组装应去除重复片段、保留来源边界、控制 Token 预算，并明确区分指令与不可信文档内容。
- 引用必须指向真正支持结论的原文，不能只列“检索到的文档”。资料不足时应返回缺少的证据和可继续查询的方向，而不是编造答案。

### 最小代码示例（Minimal Example）
```python
def build_context(chunks: list[dict[str, str]]) -> str:
    return "\n\n".join(
        f"[来源: {chunk['source']}]\n{chunk['text']}" for chunk in chunks
    )

context = build_context([{"source": "manual.md#p12", "text": "支持 CUDA 设备。"}])
print(context)

# 期望输出:
# [来源: manual.md#p12]
# 支持 CUDA 设备。
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：如何区分“没有检索到”和“检索到了但模型答错”？**

**参考答案：**先独立检查正确证据是否出现在 Top-K 或重排候选中；没有则属于解析、切块、查询或召回问题。正确证据已进入最终上下文但答案错误，则检查上下文组装、Prompt、模型理解、引用绑定和生成校验。

## 7. 无框架实现与 RAG 框架（Framework-free and Framework-based RAG）
### 概念与原理（Concept and Mechanism）
- 无大型框架版本用于理解并测试每个接口：解析器、切块器、Embedder、Retriever、Reranker 和 Generator。
- LangChain 或 LlamaIndex 可提供连接器、索引封装、工作流和追踪集成，但抽象层可能随版本变化。业务代码应依赖自己的稳定接口，并保留替换核心组件的能力。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么先做无框架版本？**

**参考答案：**为了看清数据契约、失败位置和评测边界。理解核心链路后再使用框架可以提高开发效率；若直接依赖黑盒链，出现版本变化、空检索或 Metadata 丢失时很难定位。

## 8. 法规知识库项目的面试表达（Regulation RAG Interview Framing）
- **数据（Data）**：只使用允许公开访问的法规，保存文档版本、条款、页码和来源 URL。
- **基础版本（Baseline）**：解析、结构切块、Embedding、Top-K、带引用回答和无答案拒答，不依赖大型框架。
- **对照版本（Comparison）**：使用一个 RAG 框架复现相同数据契约和评测集，比较开发效率与可控性。
- **测试（Testing）**：至少包含直接事实、跨段、歧义和无答案问题；追踪每个答案到原文。
- **高频追问（Common Follow-up）**：更换 Embedding 为什么需要重建索引？因为新模型产生的向量空间不同，旧文档向量与新查询向量不可直接比较。

## 参考资料（References）
- [[大模型应用工程师学习计划]]
- [pgvector 官方文档](https://github.com/pgvector/pgvector)
