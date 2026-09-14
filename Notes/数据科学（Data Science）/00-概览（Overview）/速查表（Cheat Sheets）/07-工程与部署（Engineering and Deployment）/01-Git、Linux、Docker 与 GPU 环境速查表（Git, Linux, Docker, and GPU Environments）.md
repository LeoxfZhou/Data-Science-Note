---
title: "Git、Linux、Docker 与 GPU 环境速查表（Git, Linux, Docker, and GPU Environments Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - engineering/environment
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "Git 2.x；Linux 常用 GNU/POSIX 工具；Docker Engine/Compose 当前稳定版"
---
# Git、Linux、Docker 与 GPU 环境速查表（Git, Linux, Docker, and GPU Environments Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
命令执行前确认目录、目标和副作用；凭据放本地安全存储或环境变量，不写入镜像、日志和仓库。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## Git 日常与恢复（Git Workflow and Recovery）
提交是快照；分支是可移动引用；远端操作前先查看状态和差异。

|功能（Operation）|实际写法（Command / Python Usage）|返回值与状态变化|
|---|---|---|
|状态|`git status --short`|返回工作树/暂存状态|
|差异|`git diff / git diff --staged`|返回未暂存/已暂存差异|
|选择暂存|`git add path`|更新索引|
|提交|`git commit -m 'message'`|创建提交并移动当前分支|
|历史|`git log --oneline --graph --decorate`|返回提交图|
|分支|`git switch -c codex/topic`|创建并切换分支|
|同步|`git fetch origin`|更新远端跟踪引用，不改工作树|
|变基|`git rebase origin/main`|重放提交，冲突时暂停|
|临时保存|`git stash push -u`|保存跟踪及未跟踪改动|
|恢复单文件|`git restore path / --staged path`|恢复工作树或取消暂存|
|找回引用|`git reflog`|返回本地引用移动历史|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```bash
git status --short
git log -1 --oneline
# 输出取决于当前仓库。
```
## Linux 文件、进程与文本（Linux Files, Processes, and Text）
优先只读检查，再执行移动、权限或进程操作。

|功能（Operation）|实际写法（Command / Python Usage）|返回值与状态变化|
|---|---|---|
|列文件|`ls -lah path`|输出含隐藏项的详细列表|
|查文件|`find path -type f -name '*.py'`|输出匹配路径|
|查文本|`rg -n 'pattern' path`|输出匹配行|
|查看文件|`sed -n '1,120p' file`|输出指定行|
|磁盘空间|`df -h / du -sh path`|输出文件系统/目录用量|
|进程|`ps aux / pgrep -af name`|输出进程信息|
|监控|`top / htop`|交互显示资源|
|终止|`kill -TERM pid`|请求优雅终止，有进程副作用|
|权限|`chmod u+x script.sh`|修改执行位|
|环境变量|`export APP_ENV=dev`|修改当前 shell 及子进程环境|
|管道失败|`set -o pipefail`|任一管道阶段失败时整体失败|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```bash
printf "b\na\n" | sort | uniq -c
# 期望输出：
#   1 a
#   1 b
```
## Docker、Compose 与 GPU（Containers and GPU）
镜像是只读模板，容器是运行实例，卷保存持久数据。

|功能（Operation）|实际写法（Command / Python Usage）|返回值与状态变化|
|---|---|---|
|构建|`docker build -t app:dev .`|创建镜像|
|运行|`docker run --rm -p 8000:8000 app:dev`|创建并运行容器|
|停止|`docker stop container`|向主进程发送停止信号；容器仍保留|
|重新启动|`docker start container`|启动已停止容器并保留其可写层|
|删除容器|`docker rm container`|删除停止的容器及其可写层，默认不删除命名卷|
|删除镜像|`docker image rm app:dev`|删除未被容器占用的镜像引用|
|环境文件|`docker run --env-file .env app`|注入变量；`.env` 不进 Git|
|绑定挂载|`docker run --mount type=bind,src="$PWD/data",dst=/app/data app`|直接映射主机目录，修改双方可见|
|命名卷|`docker run --mount type=volume,src=app-data,dst=/app/data app`|由 Docker 管理持久数据|
|端口映射|`docker run -p 127.0.0.1:8000:8000 app`|把宿主机 8000 转发到容器 8000，仅绑定本机|
|查看|`docker ps -a / docker images`|输出容器/镜像列表|
|检查对象|`docker inspect container`|返回完整 JSON 配置和运行状态|
|日志|`docker logs -f container`|流式输出日志|
|进入|`docker exec -it container sh`|启动容器内 shell|
|Compose 启动|`docker compose up -d --build`|构建并后台启动服务|
|Compose 状态|`docker compose ps`|输出当前项目服务状态|
|Compose 日志|`docker compose logs -f service`|持续输出指定服务日志|
|Compose 暂停服务|`docker compose stop`|停止服务但保留容器和网络|
|Compose 拆除|`docker compose down`|删除服务容器与网络，默认保留命名卷|
|Compose 连卷删除|`docker compose down -v`|同时删除声明的命名卷，数据不可从容器恢复|
|GPU|`docker run --gpus all image nvidia-smi`|向容器暴露 GPU|
|GPU 检查|`nvidia-smi / torch.cuda.is_available()`|输出驱动状态或布尔值|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。
### 镜像、容器与数据状态（Images, Containers, and Data State）
- **镜像（Image）**：只读文件系统模板；重新构建镜像不会自动替换正在运行的旧容器。
- **容器（Container）**：镜像的运行实例；`stop` 后可再次 `start`，`rm` 会删除容器可写层。
- **命名卷（Named Volume）**：由 Docker 管理，适合数据库等长期数据；`docker compose down` 默认保留，`down -v` 才会删除。
- **绑定挂载（Bind Mount）**：直接映射明确的主机路径，适合开发代码和用户可见文件；主机移动或权限变化会影响容器。
- **主进程（PID 1）**：容器在主进程退出后停止；服务必须以前台方式运行并正确处理终止信号。
### 网络与服务名（Networking and Service Names）
- **`HOST:CONTAINER`**：`-p 8000:8080` 表示访问宿主机 8000 会转发到容器 8080；应用仍需在容器内监听 `0.0.0.0:8080`。
- **服务间通信**：Compose 服务通过服务名和容器端口访问，例如 `http://api:8000`；容器中的 `localhost` 只代表该容器自身。
- **最小暴露**：数据库等内部服务通常只加入 Compose 网络，不映射到公网；确需本机访问时绑定 `127.0.0.1`。
### Docker Desktop 与命令行对照（Docker Desktop and CLI Mapping）

|功能（Operation）|实际写法（Command Usage）|返回值与状态变化|
|---|---|---|
|查看 Containers 页面|`docker ps -a`|列出运行与停止的容器|
|点击 Start/Stop|`docker start / docker stop`|切换容器运行状态，不删除对象|
|点击 Delete|`docker rm`|删除容器；是否保留数据取决于卷|
|查看 Logs|`docker logs -f`|读取标准输出与错误日志|
|查看 Inspect|`docker inspect`|返回端口、挂载、网络和环境配置|
|查看 Images 页面|`docker image ls`|列出本地镜像|
|查看 Volumes 页面|`docker volume ls`|列出命名卷|

### 最小 Compose 生命周期（Minimal Compose Lifecycle）
```bash
docker compose config
docker compose up -d --build
docker compose ps
docker compose logs --tail=100 app
docker compose down
# 命令会创建或移除容器与网络；具体输出取决于 compose.yaml 和运行环境。
```
### 调试与安全边界（Debugging and Security Boundaries）
- **容器立即退出**：先看 `docker logs` 和 `docker inspect` 的退出码，再确认入口命令、配置文件、权限和依赖服务。
- **端口无法访问**：依次核对容器状态、应用监听地址、容器端口、宿主机映射端口和防火墙。
- **数据“消失”**：检查实际挂载点和卷名；不要在未备份数据库前运行 `down -v`、`volume rm` 或清理命令。
- **镜像更新不生效**：重新构建并重新创建容器；只重启旧容器仍使用旧镜像配置。
- **秘密管理**：不要把密钥写入 Dockerfile、镜像层、Compose 文件或日志；使用未提交的环境文件或秘密管理服务，并限制文件权限。
- **镜像安全**：固定可信基础镜像版本，以非 root 用户运行，减少安装包与开放端口，并在发布前扫描漏洞。
## 高频工作模式（Common Workflows）
- **基线（Baseline）**：先用最小可解释模型和极小数据过拟合测试，确认数据、损失和指标链路正确。
- **训练（Training）**：固定随机种子，记录数据版本、超参数、权重、指标与环境。
- **验证（Validation）**：验证集只用于选型与调参，最终测试集只评估一次。
- **推理（Inference）**：冻结随机行为、关闭梯度、统一预处理并验证输出 schema。
- **性能（Performance）**：先测量数据加载、计算、通信与后处理，再针对瓶颈优化。
- **上线（Production）**：增加输入校验、超时、批处理、监控、回滚和隐私保护。
## 常见错误与排查（Common Errors and Troubleshooting）
- **维度错误**：记录每个关键张量的 `shape/dtype/device`，按模块契约逐层核对。
- **训练不稳定**：检查输入归一化、标签范围、损失配对、学习率、梯度范数和 NaN/Inf。
- **指标虚高**：排查数据泄漏、重复样本、错误划分、阈值选择和只看单一平均指标。
- **推理漂移**：确保训练与服务使用同一 tokenizer、类别表、归一化统计和模型版本。
- **资源泄漏**：及时关闭文件、图像、客户端与进程；长任务持续观察 CPU/GPU/内存。
- **版本漂移**：固定主要依赖并以官方迁移说明处理弃用，不静默忽略警告。
## 相关详细笔记（Detailed Notes）
- [[01-Python 环境配置（Environment Setup）]]
- [[05-远程 GPU 服务器与 Linux 基础（Remote GPU Server and Linux Basics）]]
- [[01-Docker Desktop、容器、存储、网络与 Compose（Docker Desktop, Containers, Storage, Networks, and Compose）]]
## 官方参考（Official References）
- [Docker Compose 参考](https://docs.docker.com/compose/compose-file/)
