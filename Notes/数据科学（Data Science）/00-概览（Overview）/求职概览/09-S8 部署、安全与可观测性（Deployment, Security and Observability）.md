---
title: "S8 部署、安全与可观测性（Deployment, Security and Observability）"
aliases:
  - "S8 Deployment Security and Observability"
tags:
  - career/llm-application-engineer
  - interview/production
status: published
created: 2026-08-27
updated: 2026-08-27
---
# S8 部署、安全与可观测性（Deployment, Security and Observability）
> [!tip] 导航（Navigation）
> 上一阶段：[[08-S7 Agent 与工作流（Agents and Workflows）]]｜[[00-概览（Overview）]]｜下一阶段：[[10-S9 项目、面试与求职表达（Projects, Interviews and Job Search）]]
## 1. 镜像、容器、卷与端口（Images, Containers, Volumes, and Ports）
### 概念与原理（Concept and Mechanism）
- 镜像（Image）是只读构建产物，容器（Container）是镜像的运行实例；卷（Volume）保存独立于容器生命周期的数据；端口映射把宿主端口转发到容器监听端口。
- 容器可删除重建，因此数据库数据、上传文件和索引不能只保存在容器可写层。容器不是虚拟机，也不应承载人工修改后的不可复现状态。

### 最小代码示例（Minimal Example）
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 非 root 用户降低应用被利用后的系统权限。
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
构建镜像会下载基础镜像和依赖，结果受网络、平台和锁定版本影响。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：容器重启后数据为什么可能丢失？**

**参考答案：**容器可写层属于该容器实例，删除重建后不会自动保留。持久数据应放入具名卷、绑定挂载或外部数据库，并验证备份与恢复，而不是依赖容器文件系统。

## 2. Dockerfile、`.dockerignore` 与最小权限（Dockerfile, Build Context, and Least Privilege）
### 概念与原理（Concept and Mechanism）
- Dockerfile 应固定必要版本、利用构建缓存、减少不必要系统包，并使用非 root 用户运行。
- `.dockerignore` 缩小构建上下文，避免 `.git`、虚拟环境、缓存、数据集、密钥和本机配置进入镜像。
- 多阶段构建（Multi-stage Build）可把编译工具留在构建阶段，只复制运行产物到最终镜像。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么镜像里不能只依赖运行时环境变量覆盖已经复制进去的 `.env`？**

**参考答案：**镜像层可能仍包含 `.env`，即使最终容器使用其他值，拥有镜像的人仍能提取旧密钥。敏感配置从一开始就不能进入构建上下文或镜像层。

## 3. Docker Compose、网络、健康检查与持久化（Compose, Networking, Health Checks, and Persistence）
### 概念与原理（Concept and Mechanism）
- Docker Compose 描述 API、PostgreSQL、Redis 等多服务开发或单机部署拓扑。服务在 Compose 网络中通过服务名通信，不能把容器内的 `localhost` 当成其他容器。
- `depends_on` 的启动顺序不等于依赖已经可用；应用仍需就绪检查、连接重试和迁移协调。

### 最小代码示例（Minimal Example）
```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
  db:
    image: pgvector/pgvector:pg17
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 10
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```
启动会创建容器、网络与卷，属于外部副作用；镜像标签应在实际项目中进一步固定和验证。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：健康检查成功是否代表整个 RAG 系统正确？**

**参考答案：**不代表。健康检查只回答服务是否存活或关键依赖是否就绪，不替代端到端功能和质量评测。检查过重还可能自身造成负载或因外部模型短暂故障不断重启健康进程。

## 4. CI/CD、质量门禁与回滚（CI/CD, Quality Gates, and Rollback）
### 概念与原理（Concept and Mechanism）
- 持续集成（Continuous Integration, CI）在提交或合并请求上自动执行 lint、类型检查和测试；持续交付/部署（Continuous Delivery/Deployment, CD）把通过验证的同一构建产物推进到环境。
- 失败测试应阻止发布。密钥通过 CI Secret 注入，不能写入仓库或打印到日志。回滚应部署上一个不可变镜像或版本，而不是在线手改容器。

### 最小代码示例（Minimal Example）
```yaml
name: test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest
```
该工作流会在 GitHub Actions 环境安装依赖并运行测试，输出取决于代码与依赖状态。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：数据库迁移如何回滚？**

**参考答案：**优先采用向后兼容的扩展—迁移—收缩（Expand-Migrate-Contract）流程：先新增兼容结构，再迁移数据和应用，确认稳定后删除旧结构。破坏性迁移不应只依赖自动 `down` 脚本，必须有备份、恢复演练和发布协调。

## 5. 日志、指标与追踪（Logs, Metrics, and Traces）
### 概念与原理（Concept and Mechanism）
- 日志（Logs）记录离散事件，指标（Metrics）聚合可计算的时间序列，追踪（Traces）展示一次请求跨服务和阶段的因果路径。
- Request ID/Trace ID 应贯穿 API、检索、数据库、模型和后台任务。基础指标包括请求量、错误率、P50/P95/P99 延迟、检索耗时、候选数量、模型 Token、模型延迟与估算成本。

> [!tip] 大白话理解（Plain-language Intuition）
> 指标告诉你“系统整体哪里不对”，追踪告诉你“这一次请求卡在哪一步”，日志告诉你“那一步具体发生了什么”。三者相互补充。

### 最小代码示例（Minimal Example）
```python
import json

event = {
    "event": "llm_call_completed",
    "request_id": "req-123",
    "model": "provider/model",
    "latency_ms": 820,
    "input_tokens": 300,
    "output_tokens": 80,
}
print(json.dumps(event, ensure_ascii=False, sort_keys=True))

# 期望输出:
# {"event": "llm_call_completed", "input_tokens": 300, "latency_ms": 820, "model": "provider/model", "output_tokens": 80, "request_id": "req-123"}
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：为什么不能把完整 Prompt 和检索文档默认写入日志？**

**参考答案：**其中可能包含个人信息、商业资料、提示注入内容和密钥，日志又常有更广访问范围和更长保留期。应默认记录长度、哈希、类别和脱敏摘要，只有受控调试场景按授权采样原文。

## 6. Prompt Injection 与不可信检索内容（Prompt Injection and Untrusted Retrieved Content）
### 概念与原理（Concept and Mechanism）
- 提示注入（Prompt Injection）是攻击者通过用户输入或外部文档诱导模型忽略开发者目标、泄露数据或调用不当工具；普通 Prompt 错误则是任务描述不清或格式不稳定。
- 检索文档、网页和工具结果都是不可信数据，不能因为它们位于“知识库”就拥有指令权限。
- 防护依赖最小权限、工具白名单、参数验证、数据隔离、输出校验和人工审批，不能只靠 System Prompt。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：把“忽略文档中的指令”写进 System Prompt 是否足够？**

**参考答案：**不够。模型仍可能受攻击内容影响。应用必须在架构上限制模型能看到和能执行的资源，工具层独立校验权限，高风险动作需要确认，并监控异常调用。

## 7. 文件上传、认证、限流与脱敏（Uploads, Authentication, Rate Limiting, and Redaction）
### 概念与原理（Concept and Mechanism）
- 上传接口限制大小、扩展名、实际内容类型、文件数量、解压规模和存储路径，随机化服务端文件名，防止路径穿越和压缩炸弹。
- 对外接口需要认证、资源级授权和速率限制；日志和错误响应应移除密钥、密码、Token、个人数据和内部堆栈。

### 最小代码示例（Minimal Example）
```python
from pathlib import Path

ALLOWED_SUFFIXES = {".txt", ".md", ".pdf"}

def validate_upload_name(filename: str) -> str:
    safe_name = Path(filename).name
    if Path(safe_name).suffix.lower() not in ALLOWED_SUFFIXES:
        raise ValueError("不支持的文件类型")
    return safe_name

print(validate_upload_name("../manual.pdf"))  # 输出: manual.pdf
```

### 面试问题与参考答案（Interview Questions and Answers）
**问题：只检查文件扩展名有什么风险？**

**参考答案：**扩展名由客户端提供，可把恶意内容改名为 `.pdf`。还要检查文件签名或实际解析结果、限制大小和资源使用，并在隔离环境中处理不可信文件。

## 8. 超时、重试、并发、缓存与降级（Timeouts, Retries, Concurrency, Caching, and Degradation）
### 概念与原理（Concept and Mechanism）
- 每个下游调用需要连接、读取和总时间预算；重试必须有限且只处理适合的短暂故障；并发上限保护数据库、模型与自身资源。
- 缓存适合重复且允许陈旧的结果，Key 必须包含模型、参数、权限域和知识版本。降级策略可以是返回检索结果、切换明确标记的模型或稍后重试，不能静默伪造完整成功。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：熔断（Circuit Breaker）和重试有什么区别？**

**参考答案：**重试针对单个请求的短暂故障；熔断器在下游持续失败时临时阻止更多调用，快速失败并给下游恢复时间。错误的重试会放大故障，熔断也需要半开探测和恢复策略。

## 9. Token 成本、延迟分位数与压力测试（Token Cost, Latency Percentiles, and Load Testing）
### 概念与原理（Concept and Mechanism）
- 单次成本通常由输入 Token、输出 Token、Embedding、重排和基础设施共同构成；缓存命中率和上下文长度会显著影响成本。
- P50 是中位延迟，P95 表示 95% 请求不超过该值。平均值会掩盖尾延迟（Tail Latency），用户体验和容量规划更关注分位数与错误率。

### 最小代码示例（Minimal Example）
```python
def estimated_cost(input_tokens: int, output_tokens: int, input_price: float, output_price: float) -> float:
    return input_tokens / 1_000_000 * input_price + output_tokens / 1_000_000 * output_price

print(round(estimated_cost(2_000, 500, 1.0, 4.0), 4))  # 输出: 0.004
```
示例价格仅用于演示计算，真实价格必须读取当前供应商报价。

### 面试问题与参考答案（Interview Questions and Answers）
**问题：压测为什么要同时记录错误率？**

**参考答案：**系统可以通过快速拒绝或失败获得看似很低的延迟。只有把吞吐、分位延迟、错误率、资源利用率和下游限流共同分析，才能判断真实容量。

## 10. 生产化部署的面试表达（Production Deployment Interview Framing）
- **交付（Delivery）**：固定依赖的镜像、Compose、数据库迁移、健康检查、环境变量样例和可复现 README。
- **质量门禁（Quality Gate）**：lint、类型检查、单元/集成测试通过后构建同一镜像；失败阻止部署。
- **安全（Security）**：非 root、密钥不入镜像、上传限制、身份与权限、限流、最小工具权限和日志脱敏。
- **观测（Observability）**：Request ID 串联 API、检索、数据库与模型；记录错误、P50/P95、Token 和成本。
- **可靠性（Reliability）**：超时、有限重试、并发限制、幂等、明确降级、持久化和回滚。

## 参考资料（References）
- [[大模型应用工程师学习计划]]
- [Docker 官方文档](https://docs.docker.com/)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/reference/security/secrets)
- [OWASP GenAI Security Project](https://genai.owasp.org/)
