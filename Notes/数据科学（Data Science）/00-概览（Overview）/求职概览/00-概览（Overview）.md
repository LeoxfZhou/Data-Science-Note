---
title: "大模型应用工程师面试知识导航（LLM Application Engineer Interview Index）"
aliases:
  - "LLM Application Engineer Interview Index"
tags:
  - career/llm-application-engineer
  - interview
status: published
created: 2026-08-27
updated: 2026-08-27
---
# 大模型应用工程师面试知识导航（LLM Application Engineer Interview Index）
> [!tip] 使用方法（How to Use）
> [[大模型应用工程师学习计划]]负责学习顺序、项目任务与验收；本组笔记负责面试前快速复习。每个知识点先给出可以直接表达的概括，再说明原理、场景、最小示例、常见追问与参考答案；需要深入学习时沿 Wiki Link 进入正式技术笔记。
## 1. 分阶段知识入口（Stage Index）

|阶段|面试知识笔记|核心目标|
|---|---|---|
|S0|[[01-S0 开发环境与基础复核（Environment and Foundation Review）]]|环境、依赖、复现、计时、SQL 与采集合规|
|S1|[[02-S1 Python 工程与基础算法（Python Engineering and Algorithms）]]|Python、HTTP、异步、测试、Git 与基础算法|
|S2|[[03-S2 PyTorch、深度学习与 NLP 基础（PyTorch, Deep Learning and NLP）]]|训练流程、NLP 数据流、指标与典型模型|
|S3|[[04-S3 大模型应用基础（LLM Application Fundamentals）]]|模型参数、提示、结构化输出、流式 API 与错误治理|
|S4|[[05-S4 RAG 基础（RAG Fundamentals）]]|解析、切块、向量检索、引用回答与框架边界|
|S5|[[06-S5 AI 后端工程化（AI Backend Engineering）]]|FastAPI、PostgreSQL、pgvector、Redis、权限与后台任务|
|S6|[[07-S6 RAG 优化与评测（RAG Optimization and Evaluation）]]|混合检索、重排、检索指标、生成评测与实验方法|
|S7|[[08-S7 Agent 与工作流（Agents and Workflows）]]|工具调用、状态、控制流、安全边界与低代码平台|
|S8|[[09-S8 部署、安全与可观测性（Deployment, Security and Observability）]]|Docker、CI/CD、日志指标追踪、安全、可靠性与成本|
|S9|[[10-S9 项目、面试与求职表达（Projects, Interviews and Job Search）]]|作品集、项目表达、现场追问、JD 分析与投递复盘|
|Optional|[[11-Optional 扩展技能（Optional Advanced Skills）]]|Java、推理优化、微调、低代码平台与扩展算法|

## 2. 面试回答结构（Interview Answer Structure）
回答技术问题时优先采用四步结构：
1. **定义（Definition）**：一句话说明它是什么。
2. **机制（Mechanism）**：说明数据如何流动、状态如何变化或约束如何生效。
3. **场景（Scenario）**：说明什么时候使用，以及什么时候不应该使用。
4. **权衡（Trade-off）**：补充性能、正确性、复杂度、安全或成本代价。

回答项目问题时采用“问题—方案—证据—反思”结构：
1. **问题（Problem）**：业务目标、输入输出和限制是什么。
2. **方案（Solution）**：架构、关键组件和选择理由是什么。
3. **证据（Evidence）**：测试、指标、延迟、成本和 Bad Case 如何证明结果。
4. **反思（Reflection）**：失败在哪里、如何定位、下一步如何改进。

## 3. 快速复习顺序（Rapid Review Order）
- **30 分钟复习**：S3 → S4 → S5 → S6 → S7 → S8。
- **后端岗位加试**：补 S1、S5、S8。
- **NLP/算法岗位加试**：补 S2、Optional 中的微调与数学。
- **项目终面准备**：重点复习 S9，并为每个项目准备可验证数据和失败案例。

## 参考资料（References）
- [[大模型应用工程师学习计划]]
