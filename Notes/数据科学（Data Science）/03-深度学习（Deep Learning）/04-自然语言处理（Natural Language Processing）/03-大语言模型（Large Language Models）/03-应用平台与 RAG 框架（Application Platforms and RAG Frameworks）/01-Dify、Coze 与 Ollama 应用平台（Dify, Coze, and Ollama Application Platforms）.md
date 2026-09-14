---
title: Dify、Coze 与 Ollama 应用平台（Dify, Coze, and Ollama Application Platforms）
tags:
  - data-science/nlp/llm-platforms
  - data-science/rag
status: published
created: 2026-09-10
published_at: 2026-09-10
verified_at: 2026-09-10
---
# Dify、Coze 与 Ollama 应用平台（Dify, Coze, and Ollama Application Platforms）
## 1. 三类工具的职责边界

|工具|核心角色|主要能力|不负责什么|
|---|---|---|---|
|Ollama|本地模型运行时（Local Model Runtime）|下载、管理并通过本地 API 运行生成模型或嵌入模型|不提供完整知识库、工作流和应用运营平台|
|Dify|大模型应用开发平台（LLM Application Platform）|模型接入、提示词、知识库、工作流、Agent、API 与应用界面|本身不是一个大语言模型|
|Coze|托管式智能体平台（Managed Agent Platform）|在线创建智能体、工作流、知识库和工具集成|通常不要求用户自行维护底层数据库与容器|

Dify 既可使用云服务，也可自托管（Self-hosted）；Coze 的产品入口和界面会演化，不能把二者永久简化成“Dify 只能本地、Coze 只能云端”。真正的区别应从部署控制权、数据边界、模型选择、维护成本和平台限制判断。
> [!tip] 大白话理解（Plain-language Intuition）
> Ollama 像发动机，负责让模型转起来；Dify 和 Coze 像应用装配台，把发动机、资料库、工具和流程拼成用户可用的产品。发动机能单独工作，但装配台仍需要连接一个模型提供者。
## 2. Dify 自托管架构
Dify 的 Docker Compose 部署由多个服务组成，而不是单个容器。当前官方快速开始中，核心服务包括 Web、API、Worker、定时 Worker、插件守护进程等，依赖组件包括 PostgreSQL、Redis、向量存储、Nginx、沙箱和 SSRF 代理；具体服务会随版本变化，应以目标版本的 Compose 文件为准。

|组件|职责|常见故障表现|
|---|---|---|
|Web / Nginx|前端资源与反向代理|页面打不开、静态资源失败|
|API|应用、模型、知识库和账户接口|保存、调用或初始化请求失败|
|Worker / Worker Beat|异步任务与周期任务|文档处理、索引或任务长期排队|
|PostgreSQL|账号、应用、配置与业务元数据|登录、迁移或状态读取失败|
|Redis|缓存、队列与临时状态|任务积压、状态不同步|
|向量数据库（Vector Database）|知识块向量及检索|索引失败或知识库召回为空|
|Plugin Daemon|模型提供者和插件运行支持|Provider 安装或调用失败|
|Sandbox / SSRF Proxy|代码执行隔离与请求保护|工具执行或外部访问异常|

官方快速开始要求先准备 `.env`，再运行 `docker compose up -d`，最后用 `docker compose ps` 检查主要容器处于 `Up` 或 `healthy`；一次性权限初始化任务正常退出不应误判为系统失败。
## 3. Dify 连接宿主机 Ollama
当 Dify 位于 Docker Desktop 容器中，而 Ollama 运行在 Mac 或 Windows 宿主机时：
- 容器内的 `localhost:11434` 指向 Dify 容器本身，不是宿主机。
- 常用地址为 `http://host.docker.internal:11434`。
- Dify 需要分别登记生成模型（Generation Model）与嵌入模型（Embedding Model）；两者承担不同任务，不能因为都由 Ollama 提供就混用。
- 生成模型读取提示词与检索上下文并生成答案；嵌入模型把文档块和查询映射为向量。
- 不应为了排错直接把 Ollama 监听地址改为 `0.0.0.0` 并暴露公网；先验证宿主机 API、容器到宿主机的路由和防火墙。
```text
浏览器
  ↓
Dify Web / API / Worker ── PostgreSQL / Redis / 向量数据库
  │
  └── http://host.docker.internal:11434
                         ↓
                      Ollama
```
## 4. 最小 RAG 工作流
检索增强生成（Retrieval-Augmented Generation, RAG）把外部资料在查询时交给模型，不等同于微调（Fine-tuning）。
```text
文档 → 解析与切块 → 嵌入 → 向量索引
用户问题 → 查询嵌入 → 相似度检索 → 相关文本块 + 问题 → 生成模型 → 答案与引用
```
> [!tip] 大白话理解（Plain-language Intuition）
> 普通聊天像闭卷答题；RAG 先从资料柜里找出最相关的几页，再让模型带着这些页回答。资料没有写的内容，系统应明确说证据不足，而不是靠语言流畅度补一个答案。
### 4.1 最小验收用例
1. 准备一小段含唯一事实的测试文档。
2. 使用嵌入模型完成索引。
3. 把知识检索节点连接到对话或工作流。
4. 提问一个资料内问题，检查答案和引用是否命中。
5. 提问一个资料外问题，检查系统是否拒绝无依据补全。
仅验证“回答看起来合理”不够，还应检查实际召回文本、相似度、切块边界和来源元数据。
## 5. Dify 与 Coze 的选型

|考虑项|自托管 Dify|托管式 Coze|
|---|---|---|
|运维|用户维护容器、数据库、升级与备份|平台维护基础设施|
|数据边界|可把主要业务数据留在受控环境，但外接云模型仍会发送请求|上传资料和交互通常进入平台托管环境|
|模型与组件自由度|较高，可接本地或云端提供者|受平台可用模型、插件、区域和配额约束|
|上手速度|部署和排错成本较高|通常更快完成原型|
|可移植性|Compose、数据和配置由用户管理，迁移空间较大|可能依赖平台专有节点和发布机制|

选择平台前确认：数据是否允许上传、模型是否可用、知识库如何导出、调用费用、插件权限、地区隔离、审计日志和停服后的恢复方式。
## 6. Dify 启动与排错顺序
```bash
docker compose version
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose ps
docker compose logs --tail=100
```
这些命令会访问网络或改变容器状态，不提供固定输出。
1. 配置解析失败：先检查 Compose YAML 和 `.env`，不要先反复启动。
2. 拉取出现 `TLS handshake timeout`、`EOF`：检查 Docker Daemon 的代理与网络；后续 `No such image` 常是镜像未拉取的连锁结果。
3. 页面打不开：检查 Nginx/Web/API 状态、发布端口和浏览器请求。
4. 页面一直加载：检查 API 响应、WebSocket、Redis、数据库迁移和浏览器控制台，不只看容器是否 `healthy`。
5. 知识库卡住：检查 Worker、向量数据库、嵌入模型和文档解析日志。
6. Ollama 连接失败：分别从宿主机和容器测试地址，确认没有误用容器 `localhost`。
HTTP `401 Unauthorized` 表示请求通常已经到达服务但鉴权失败；它与超时、连接拒绝或 DNS 失败不是同一类问题。
## 7. 生命周期、资源与备份
- `docker compose stop` 停止计算进程但保留容器和卷；停止后 CPU/GPU 使用通常下降，磁盘占用仍存在。
- `docker compose down` 移除应用容器与网络，命名卷默认保留。
- `docker compose down -v` 会删除卷，可能同时删除数据库、知识库索引与应用配置，不应作为普通收尾操作。
- 升级前备份持久化卷和 `.env`，阅读目标版本迁移说明，并比较新版 `.env.example` 与现有配置。
- `.env`、管理密码、模型 API Key 和私有资料不得进入公开 Git、日志或截图。
## 8. 参考资料
- [Dify Docker Compose 快速部署](https://docs.dify.ai/en/self-host/deploy/quick-start/docker-compose)
- [[01-Docker Desktop、容器、存储、网络与 Compose（Docker Desktop, Containers, Storage, Networks, and Compose）]]
- [[02-LlamaIndex 本地 RAG、检索与索引持久化（LlamaIndex Local RAG, Retrieval, and Index Persistence）]]

