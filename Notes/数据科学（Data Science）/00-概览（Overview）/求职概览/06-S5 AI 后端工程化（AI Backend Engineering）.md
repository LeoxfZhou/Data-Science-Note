---
title: "S5 AI 后端工程化（AI Backend Engineering）"
aliases:
  - "S5 AI Backend Engineering"
tags:
  - career/llm-application-engineer
  - interview/backend
status: published
created: 2026-08-27
updated: 2026-08-27
---
# S5 AI 后端工程化（AI Backend Engineering）
> [!tip] 导航（Navigation）
> 上一阶段：[[05-S4 RAG 基础（RAG Fundamentals）]]｜[[00-概览（Overview）]]｜下一阶段：[[07-S6 RAG 优化与评测（RAG Optimization and Evaluation）]]
## 1. FastAPI Router、Dependency 与 Pydantic（FastAPI Routing, Dependencies, and Pydantic）
### 概念与原理（Concept and Mechanism）
- Router 按业务领域组织路径操作；依赖注入（Dependency Injection）集中处理认证、数据库会话和共享校验；Pydantic 在系统边界验证请求与响应 Schema。
- 统一错误格式应包含稳定错误码、可读消息和请求 ID；HTTP 状态码表达协议层结果，业务错误码表达领域原因。

### 最小代码示例（Minimal Example）
```python
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)

def current_user_id(x_user_id: str = Header()) -> str:
    if not x_user_id:
        raise HTTPException(status_code=401, detail="missing user")
    return x_user_id

@app.post("/queries")
def create_query(payload: QueryRequest, user_id: str = Depends(current_user_id)) -> dict[str, str]:
    return {"user_id": user_id, "question": payload.question}
```
启动服务属于持续进程；实际响应取决于请求 Header 和 Body。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么不在每个接口里手写认证逻辑？**

**参考答案：**重复代码容易出现某个接口漏校验或行为不一致。依赖注入把认证作为显式接口依赖，便于复用、测试和替换，但资源级权限仍需结合具体对象进行检查。

### 相关笔记（Related Notes）
- [[01-FastAPI 核心开发参考（FastAPI Core Development Reference）]]
- [[02-FastAPI 机器学习推理服务模板（FastAPI ML Inference Service Template）]]

## 2. REST 接口、SSE、OpenAPI 与健康检查（REST APIs, SSE, OpenAPI, and Health Checks）
### 概念与原理（Concept and Mechanism）
- 文档上传、查询、会话、引用和删除应使用可理解的资源模型。SSE 适合单向流式 Token 或事件；每个事件需有明确类型，客户端断开时服务端应取消上游任务。
- OpenAPI 描述请求、响应、认证和错误契约，可生成客户端并驱动接口测试。
- 存活检查（Liveness）回答“进程是否活着”，就绪检查（Readiness）回答“是否可以接收流量”；后者可检查必要依赖，但不应执行昂贵全链路请求。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：`200 OK` 中返回 `{"success": false}` 有什么问题？**

**参考答案：**它削弱了 HTTP 状态语义，使网关、监控和客户端无法按协议正确识别失败。应使用合适状态码表示认证、权限、冲突、校验或服务故障，并在 Body 中提供稳定业务错误信息。

## 3. 关系模型、约束、迁移与事务（Relational Modeling, Constraints, Migrations, and Transactions）
### 概念与原理（Concept and Mechanism）
- 用户、文档、Chunk、会话和消息应使用稳定 ID 与外键表达关系；唯一约束维护幂等性，索引服务真实查询路径。
- Schema 迁移（Schema Migration）把数据库结构变化版本化，使开发、测试和生产按同一顺序演进。
- 文档与 Chunk 的状态更新需要事务或可恢复工作流，避免主记录显示成功但索引只写入一部分。

### 最小代码示例（Minimal Example）
```sql
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    source_hash TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending', 'running', 'succeeded', 'failed')),
    UNIQUE (user_id, source_hash)
);
```
该 DDL 会修改数据库 Schema，属于数据库副作用。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：索引为什么会让写入变慢？**

**参考答案：**新增、更新或删除行时，数据库还要维护相关索引页，产生额外 CPU、I/O、锁与存储开销。索引应围绕高频过滤、排序和连接设计，并用查询计划验证实际效果。

## 4. pgvector 与向量检索（pgvector and Vector Search）
### 概念与原理（Concept and Mechanism）
- pgvector 把向量与关系数据保存在 PostgreSQL 中，可利用事务、连接和 Metadata Filter。`<->` 表示 L2 距离，`<#>` 表示负内积，`<=>` 表示余弦距离；排序方向和索引操作符必须与度量一致。
- 默认精确检索提供完整召回；HNSW 与 IVFFlat 是近似索引。HNSW 通常有更好的速度—召回权衡，但构建更慢、内存更多；IVFFlat 需要已有数据训练列表，并通过 lists/probes 权衡速度与召回。

### 最小代码示例（Minimal Example）
```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE chunks (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(3) NOT NULL
);
CREATE INDEX chunks_embedding_hnsw
ON chunks USING hnsw (embedding vector_cosine_ops);

SELECT id, content, 1 - (embedding <=> '[0.1,0.2,0.3]') AS cosine_similarity
FROM chunks
WHERE user_id = 42
ORDER BY embedding <=> '[0.1,0.2,0.3]'
LIMIT 5;
```
该示例会修改并查询数据库；结果依赖表中数据。生产中维度必须与实际 Embedding 模型一致。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么加了近似向量索引后，结果可能少于预期？**

**参考答案：**近似索引先扫描有限候选，Metadata 条件可能在候选扫描后过滤掉部分结果。可调整搜索参数、启用适用版本的迭代扫描、优化过滤列索引、分区，或在规模允许时使用精确检索；最终应以 Recall 与延迟实测决定。

## 5. 查询计划与慢查询（Query Plans and Slow Queries）
### 概念与原理（Concept and Mechanism）
- `EXPLAIN` 展示优化器计划，`EXPLAIN ANALYZE` 会实际执行并显示真实耗时与行数，因此对写操作使用时必须谨慎。
- 重点比较估算行数与实际行数、顺序扫描、连接方式、排序、缓存命中以及过滤掉的行数。慢查询不一定缺索引，也可能是低选择性、统计信息过期、返回数据过多或 N+1 查询。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么数据库可能不使用已经存在的索引？**

**参考答案：**优化器估计顺序扫描更便宜，例如查询匹配大部分表、表很小、统计信息不准确、表达式与索引不匹配，或排序/类型转换破坏了可用条件。应检查计划和数据分布，不应强行认定“有索引就必须使用”。

## 6. Redis 数据结构、Key 与 TTL（Redis Data Structures, Keys, and TTL）
### 概念与原理（Concept and Mechanism）
- String 适合缓存值和计数器，Hash 适合对象字段，List 适合简单序列，Stream 是带 ID 的追加日志并支持消费组。选择数据结构应依据访问模式，而不是把所有内容序列化为一个大字符串。
- Key 应包含业务域、租户和版本，例如 `rag:session:{user_id}:{session_id}`；TTL 限制缓存陈旧和内存占用，但到期不等于主数据删除。

### 最小代码示例（Minimal Example）
```python
def session_key(user_id: int, session_id: str, version: int = 1) -> str:
    return f"rag:v{version}:session:{user_id}:{session_id}"

print(session_key(42, "abc"))  # 输出: rag:v1:session:42:abc
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：Redis 为什么不会自动让系统变快？**

**参考答案：**缓存只有在命中率足够、数据允许短暂陈旧且失效策略正确时才减少下游访问。低命中、序列化开销、网络往返、热 Key 和一致性维护都可能抵消收益。

### 相关笔记（Related Notes）
- [[06-爬虫数据存储：MySQL 与 Redis（Crawler Data Storage）]]

## 7. 缓存穿透、击穿与一致性（Cache Penetration, Breakdown, and Consistency）
### 概念与原理（Concept and Mechanism）
- 缓存穿透（Cache Penetration）是大量不存在的 Key 每次都访问数据库；可使用输入校验、短 TTL 空值或概率结构缓解。
- 缓存击穿（Cache Breakdown）是热点 Key 失效时大量请求同时回源；可使用互斥重建、逻辑过期或随机化 TTL 缓解。
- Cache-aside 常见流程是读缓存未命中后读数据库并回填；写入通常先更新数据库再删除缓存，并接受明确的一致性窗口。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么不能默认用 Redis 分布式锁解决所有并发问题？**

**参考答案：**锁会引入超时、租约、进程暂停、故障转移和正确释放等复杂性。数据库唯一约束、原子更新、幂等键、队列串行化或单机锁常更合适；只有跨进程互斥确实必要时才选择分布式锁并设计故障语义。

## 8. 认证、密码与多租户隔离（Authentication, Passwords, and Tenant Isolation）
### 概念与原理（Concept and Mechanism）
- 认证（Authentication）确认用户是谁，授权（Authorization）确认用户能做什么。密码应使用专用慢哈希算法并带盐，不可明文或使用普通快速哈希。
- 多租户查询必须在可信代码或数据库策略中同时限定资源 ID 和租户 ID。只验证“用户已登录”不足以阻止用户 A 访问用户 B 的对象。

### 最小代码示例（Minimal Example）
```python
def can_access(resource_owner_id: int, current_user_id: int) -> bool:
    return resource_owner_id == current_user_id

print(can_access(resource_owner_id=42, current_user_id=42))  # 输出: True
print(can_access(resource_owner_id=7, current_user_id=42))   # 输出: False
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么只在前端隐藏“删除”按钮不算权限控制？**

**参考答案：**客户端由用户控制，可以直接构造 HTTP 请求。服务端必须对每次读取、更新和删除验证身份、动作权限和资源归属，前端隐藏只能改善体验。

## 9. 后台任务、状态机、幂等与删除一致性（Background Jobs, State Machines, Idempotency, and Deletion Consistency）
### 概念与原理（Concept and Mechanism）
- 文档解析和 Embedding 耗时较长，应提交后台任务并立即返回任务 ID。状态机至少区分 `pending`、`running`、`succeeded` 和 `failed`，同时记录重试次数与错误原因。
- 幂等键或唯一约束避免重复上传产生重复索引。删除文档需协调主记录、Chunk 和向量；跨系统操作无法使用单一事务时，可采用可重试步骤、补偿和最终一致性。

### 最小代码示例（Minimal Example）
```python
ALLOWED_TRANSITIONS = {
    "pending": {"running"},
    "running": {"succeeded", "failed"},
    "failed": {"pending"},
    "succeeded": set(),
}

def can_transition(current: str, target: str) -> bool:
    return target in ALLOWED_TRANSITIONS[current]

print(can_transition("pending", "running"))  # 输出: True
print(can_transition("succeeded", "running"))  # 输出: False
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：任务失败后为什么不能直接无条件重跑？**

**参考答案：**前一次可能已完成部分副作用，无条件重跑会生成重复 Chunk 或重复计费。任务步骤应幂等、记录检查点，并区分可重试临时错误与不可重试数据错误。

## 10. 单元、集成与故障测试（Unit, Integration, and Failure Testing）
### 概念与原理（Concept and Mechanism）
- 单元测试验证切块、权限和状态转换等纯逻辑；集成测试验证 API、数据库迁移、约束与事务；外部 LLM/Embedding 使用契约一致的 Mock，另保留少量受控真实联调。
- 必须覆盖权限越界、重复上传、解析失败、超时、模型不可用和删除后不可检索。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：Mock 外部模型后，如何避免测试与真实 API 脱节？**

**参考答案：**把供应商适配层限制为小而明确的契约，对内部业务使用 Mock；同时通过 Schema 校验、录制的脱敏响应或少量沙箱契约测试验证适配层。Mock 不能随意返回业务希望的格式。

## 11. 多用户 RAG 后端的面试表达（Multi-user RAG Backend Interview Framing）
- **架构（Architecture）**：FastAPI 接口层 → 认证与权限 → PostgreSQL 主数据 → 后台解析/Embedding → pgvector 检索 → LLM 流式生成；Redis 只承担明确的缓存、会话、限流或任务状态场景。
- **一致性（Consistency）**：唯一约束防重复；状态机记录处理进度；删除采用可重试协调流程；模型不可用不影响已上传数据。
- **安全（Security）**：每次查询带租户过滤，密码安全哈希，上传限制，密钥不入库不入日志。
- **证据（Evidence）**：两名测试用户隔离、故障重试、删除后不可召回、Mock 模型失败、端到端数据流图。

## 参考资料（References）
- [[大模型应用工程师学习计划]]
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [pgvector 官方文档](https://github.com/pgvector/pgvector)
- [Redis 数据类型](https://redis.io/docs/latest/develop/data-types/)
- [Redis 使用场景](https://redis.io/docs/latest/develop/use-cases/)
