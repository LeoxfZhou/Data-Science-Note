---
title: "S9 项目、面试与求职表达（Projects, Interviews and Job Search）"
aliases:
  - "S9 Projects Interviews and Job Search"
tags:
  - career/llm-application-engineer
  - interview/portfolio
status: published
created: 2026-08-27
updated: 2026-08-27
---
# S9 项目、面试与求职表达（Projects, Interviews and Job Search）
> [!tip] 导航（Navigation）
> 上一阶段：[[09-S8 部署、安全与可观测性（Deployment, Security and Observability）]]｜[[00-概览（Overview）]]｜扩展：[[11-Optional 扩展技能（Optional Advanced Skills）]]
## 1. 可复现作品集（Reproducible Portfolio）
### 核心内容（Core Artifacts）
- README 说明问题、目标用户、架构、依赖、启动、配置、测试、演示和限制。
- 架构图展示服务与外部依赖，数据流图展示一次请求经过解析、检索、模型与返回的顺序。
- 评测集、指标、对照实验和 Bad Case 提供可验证证据；Docker、测试与部署说明证明别人可以复现。
- 公开仓库不得包含密钥、私人数据、付费资料、个人绝对路径和无法再获取的本机依赖。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：一个能运行的 Demo 和可用于求职的项目有什么区别？**

**参考答案：**求职项目除了正常路径，还要展示问题定义、架构选择、错误处理、测试、评测、部署、限制和失败复盘。面试官需要判断候选人是否理解系统，而不是只确认页面能返回答案。

## 2. 项目 30 秒、3 分钟与 15 分钟表达（Project Pitches）
### 30 秒版本（30-second Pitch）
按“用户问题—核心方案—量化结果”表达：
> 我实现了一个面向公开法规的多用户 RAG 服务，解决长文档检索和答案溯源问题。系统使用结构切块、混合检索、Reranker 和带引用生成，并通过独立评测集比较优化前后的 Recall、答案忠实度、P95 延迟和成本。

### 3 分钟版本（3-minute Explanation）
1. 业务问题、用户和约束。
2. 数据从上传到引用答案的完整流程。
3. 三个关键选择及替代方案。
4. 指标、失败案例和改进证据。
5. 当前限制与下一步。

### 10～15 分钟版本（Deep Dive）
按数据、检索、生成、后端、可靠性、安全、评测和部署展开；每一层都准备一项失败案例及修复过程。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么要准备不同时长版本？**

**参考答案：**不同面试环节可用时间和关注点不同。短版验证问题价值与结果，长版展示系统理解和工程深度；核心事实必须一致，不能在长版才暴露关键限制。

## 3. 技术选型与替代方案（Technology Choices and Alternatives）
### 回答结构（Answer Structure）
1. 明确约束：数据量、请求量、延迟、成本、隐私和团队经验。
2. 给出候选：例如 FAISS、pgvector 或独立向量数据库。
3. 说明选择：当前规模需要事务与 Metadata Filter，因此选择 pgvector。
4. 承认代价：大规模专用检索能力、扩缩容和运维方案仍需进一步评估。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么不应该只回答“因为它流行”？**

**参考答案：**流行度不说明它满足当前约束。好的选型回答必须把需求、可选方案、证据和代价连起来，并说明在什么条件变化后会重新选型。

## 4. 指标表达与证据边界（Metric Claims and Evidence Boundaries）
### 概念与原则（Concept and Principles）
- 所有简历数字必须能说明分母、数据集、基线、测量环境和统计方法。
- “提高 30%”必须说明是相对提升还是绝对百分点；“高并发”“工业级”“高精度”需要容量、部署和指标证据。
- 只展示最好一次结果属于选择偏差，应报告稳定运行或重复实验情况。

### 最小计算示例（Minimal Example）
```python
baseline, improved = 0.60, 0.72
absolute_points = (improved - baseline) * 100
relative_improvement = (improved - baseline) / baseline * 100
print(round(absolute_points, 1))       # 输出: 12.0
print(round(relative_improvement, 1)) # 输出: 20.0
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：Recall 从 0.60 到 0.72，应该如何描述？**

**参考答案：**提高了 0.12，即 12 个百分点；相对基线提高 20%。简历中应明确使用哪一种，并说明评测集与 K 值。

## 5. 失败案例与调试复盘（Failure Cases and Debugging Retrospective）
### 回答结构（Answer Structure）
- **现象（Symptom）**：用户看到什么、哪个指标变化。
- **定位（Diagnosis）**：如何通过日志、追踪、候选结果和最小复现缩小范围。
- **根因（Root Cause）**：具体的数据、状态、配置或契约问题。
- **修复（Fix）**：改了什么，为什么有效。
- **验证（Verification）**：哪些测试与指标证明修复没有引入回归。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：讲失败案例时为什么不能只说“调了参数就好了”？**

**参考答案：**这无法证明理解根因，也不能复现。应说明排除了哪些可能性、哪个证据定位到哪一层、改变了什么变量，以及修复前后指标和回归测试。

## 6. 核心项目 A：可评测企业级 RAG（Evaluated Enterprise RAG）
### 必讲内容（Required Talking Points）
- 数据解析、Metadata、切块和版本管理。
- 稀疏、向量、混合检索与 Reranker 的对照。
- 多用户隔离、后台索引、删除一致性和流式回答。
- Recall@K、MRR/NDCG、正确性、忠实度、引用、拒答、延迟和成本。
- Docker、CI、日志、指标、压力测试和安全边界。

### 高频追问与参考答案（Common Follow-ups and Answers）
**问题：你最大的优化是什么？**

**参考答案模板：**不要直接声称某组件最好。说明基线、唯一改变的变量、评测集、检索与生成指标、延迟/成本代价和退化案例。例如“混合检索加重排提高了专有名词问题的 MRR，但 P95 增加，因此只重排前 20 个候选并缓存稳定查询”。

## 7. 核心项目 B：受控工具调用研究助手（Controlled Tool-using Research Assistant）
### 必讲内容（Required Talking Points）
- 为什么任务需要动态选择知识库或只读数据库，而不是固定单链路。
- Tool Schema、参数与权限验证、错误结果、最大步骤/时间/成本和人工确认。
- 完整执行轨迹、端到端场景、提示注入与越权测试。

### 高频追问与参考答案（Common Follow-ups and Answers）
**问题：哪些步骤其实不是 Agent？**

**参考答案：**身份认证、权限检查、参数校验、SQL 白名单、工具执行、审批和结果持久化都是确定性代码；模型只负责在允许的工具和状态中提出下一步选择。

## 8. Python 与后端高频入口（Python and Backend Interview Entry Points）
- Python 对象、生成器、异常、异步、测试与复杂度：[[02-S1 Python 工程与基础算法（Python Engineering and Algorithms）]]。
- FastAPI、PostgreSQL、pgvector、Redis、权限与后台任务：[[06-S5 AI 后端工程化（AI Backend Engineering）]]。
- Docker、CI/CD、日志、追踪、安全与成本：[[09-S8 部署、安全与可观测性（Deployment, Security and Observability）]]。

## 9. LLM、RAG 与 Agent 高频入口（LLM, RAG, and Agent Interview Entry Points）
- Token、上下文、采样、结构化输出与模型 API：[[04-S3 大模型应用基础（LLM Application Fundamentals）]]。
- 解析、Chunking、Embedding、向量检索和引用回答：[[05-S4 RAG 基础（RAG Fundamentals）]]。
- 混合检索、Reranker、Recall@K、MRR 和生成评测：[[07-S6 RAG 优化与评测（RAG Optimization and Evaluation）]]。
- Tool Calling、状态、控制流、人工确认与低代码平台：[[08-S7 Agent 与工作流（Agents and Workflows）]]。

## 10. 现场算法与测试（Live Algorithms and Testing）
### 回答步骤（Answer Steps）
1. 复述输入、输出、约束和边界。
2. 给出暴力解法及复杂度，再说明优化依据。
3. 写代码时维护循环或递归不变量。
4. 用空输入、单元素、重复值、最大规模和错误输入验证。
5. 主动说明时间和空间复杂度。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：代码写完后应该先优化还是先测试？**

**参考答案：**先用代表性与边界用例验证正确性，再根据约束和瓶颈优化；每次优化后运行回归测试。未经验证的复杂优化比清晰正确的基线风险更高。

### 相关笔记（Related Notes）
- [[01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）]]
- [[12-双指针、字符串与数据结构设计题（Two Pointers, Strings, and Data-structure Design）]]

## 11. JD 分析、简历定制与投递复盘（JD Analysis, Resume Tailoring, and Application Review）
### 方法（Method）
- 收集足够数量的真实 JD，按大模型应用、AI 后端、RAG、Agent 和算法岗位分类。
- 统计重复出现的必备技能、加分项、业务领域和年限要求，不被单个 JD 的偶然措辞带偏。
- 针对岗位调整项目排序和关键词，但不写无法证明的技能。
- 投递记录包含公司、岗位、来源、日期、简历版本、进度、反馈和知识缺口；每 10～15 次投递复盘一次转化率。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么同一份简历不适合所有 AI 岗位？**

**参考答案：**不同岗位的核心产出不同：AI 后端看服务、数据库与可靠性，RAG 岗看检索与评测，Agent 岗看工具与控制流，算法岗看模型和实验。应在事实不变的前提下调整项目顺序和证据重点。

## 参考资料（References）
- [[大模型应用工程师学习计划]]
- [[00-概览（Overview）]]
