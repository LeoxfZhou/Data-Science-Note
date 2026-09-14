---
title: Docker Desktop、容器、存储、网络与 Compose（Docker Desktop, Containers, Storage, Networks, and Compose）
tags:
  - data-science/deployment/docker
  - engineering/containerization
status: published
created: 2026-09-10
published_at: 2026-09-10
verified_at: 2026-09-10
---
# Docker Desktop、容器、存储、网络与 Compose（Docker Desktop, Containers, Storage, Networks, and Compose）
## 1. Docker 的核心对象
- **Docker Desktop**：本机图形管理界面，展示容器、镜像、卷、网络、日志与资源使用情况。
- **Docker Engine**：真正创建并运行容器的后台服务（Daemon）。Desktop 显示正常不等于某个应用容器正常，应继续检查容器状态和日志。
- **镜像（Image）**：只读的软件包与文件系统模板，包含应用、依赖和默认启动配置。
- **容器（Container）**：由镜像创建的运行实例；同一镜像可以创建多个互相隔离的容器。
- **仓库（Registry）**：保存与分发镜像的服务，例如 Docker Hub。
> [!tip] 大白话理解（Plain-language Intuition）
> 镜像像“安装包加配置好的系统模板”，容器像“根据模板真正启动的一次程序”。删除容器不会自动删除镜像；重新运行镜像会得到新的容器实例。
## 2. 容器状态与主进程（Main Process）
容器通常围绕一个主进程运行：主进程持续运行，容器处于 `Running`；主进程正常结束或异常退出，容器进入 `Exited`。
- `Created`：容器已创建但尚未启动。
- `Running`：主进程正在运行。
- `Paused`：进程被暂停。
- `Exited`：主进程已经结束；一次性任务出现此状态不一定是错误。
- `Restarting`：重启策略正在反复拉起进程，通常应先查看第一条实际错误。
- `Healthy` / `Unhealthy`：健康检查（Health Check）的结果，不等于进程是否存在。
`hello-world` 打印信息后正常退出；Web、数据库等长期服务则应保持运行。不要把所有 `Exited` 都当作失败。
## 3. 端口映射（Port Mapping）
端口写法 `HOST_PORT:CONTAINER_PORT` 表示把宿主机端口转发到容器内服务端口。

|示例|宿主机访问地址|容器内监听地址|
|---|---|---|
|`8080:80`|`http://localhost:8080`|容器的 `80/tcp`|
|`3307:3306`|`localhost:3307`|容器的 `3306/tcp`|

- 宿主机端口必须未被其他进程占用；同一宿主机端口不能同时绑定给多个容器。
- 容器间通信通常使用服务名与容器端口，而不是宿主机端口。
- 端口映射通常在创建容器时确定；需要改变时，常见做法是根据新配置重建容器。
- 未发布端口的服务仍可被同一 Docker 网络中的其他容器访问，但不能直接从宿主机访问。
> [!tip] 大白话理解（Plain-language Intuition）
> `8080:80` 像把 Mac 的 8080 号前台窗口接到容器内部的 80 号柜台。外部访客找 8080，Docker 再把请求送进 80。
## 4. Stop、Start、Delete 与数据生命周期
- **停止（Stop）**：停止主进程，容器和其可写层仍然保留；之后可以 `Start` 同一个容器。
- **启动（Start）**：重新启动已有容器，不会重新创建镜像或卷。
- **删除容器（Delete Container）**：移除容器实例及其未持久化的可写层；镜像和独立卷通常仍保留。
- **删除镜像（Delete Image）**：删除本地镜像缓存；被容器使用时通常无法直接删除。
- **删除卷（Delete Volume）**：删除持久化数据，风险通常高于删除容器，应先确认备份和引用关系。
容器应被视为可重建运行单元，不应把数据库等重要状态只保存在容器可写层。
## 5. 卷与绑定挂载（Volume and Bind Mount）

|类型|来源由谁管理|典型场景|主要风险|
|---|---|---|---|
|命名卷（Named Volume）|Docker|数据库、缓存持久化、应用状态|误用 `down -v` 或手动删卷造成数据丢失|
|绑定挂载（Bind Mount）|宿主机明确路径|源代码热更新、配置、开发数据|容器可能修改宿主机文件；路径与权限依赖本机|
|临时文件系统（tmpfs）|内存|不应落盘的临时数据|容器停止后数据消失|

Compose 中同时出现服务级 `volumes` 和顶层 `volumes` 时：服务级配置说明“挂到容器哪里”，顶层配置声明“这个命名卷如何创建或复用”。
```yaml
services:
  db:
    image: postgres:16
    volumes:
      - db_data:/var/lib/postgresql/data
volumes:
  db_data:
```
该配置具有创建容器和持久化存储的外部副作用，不提供固定输出。
## 6. Docker 网络（Docker Network）
Compose 默认会为项目创建桥接网络（Bridge Network），同一网络中的服务可通过服务名进行域名解析（DNS）。
```yaml
services:
  api:
    image: example/api
    environment:
      DATABASE_URL: postgresql://app:secret@db:5432/app
  db:
    image: postgres:16
```
- `api` 访问数据库时使用 `db:5432`；`db` 是稳定的服务名。
- 不要写死容器 IP。容器重建后 IP 可能改变，服务名保持稳定。
- 容器中的 `localhost` 只表示当前容器本身，不表示宿主机或另一个容器。
- Docker Desktop 中，容器访问宿主机服务通常使用 `host.docker.internal`；生产 Linux 环境必须根据实际网络配置处理，不能机械照搬。
## 7. Docker Compose 应用模型
Docker Compose 使用 `compose.yaml` 声明多容器应用。常见顶层对象包括 `services`、`networks`、`volumes`、`configs` 和 `secrets`。
> [!tip] 大白话理解（Plain-language Intuition）
> 单个容器像一名员工，Compose 文件像整个项目的组织表：谁负责网页、谁负责 API、谁负责数据库、彼此怎么通信、数据放在哪里，都写在一份 YAML 中。
### 7.1 最小 Compose 示例
```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
  cache:
    image: redis:7-alpine
```
配置本身没有控制台输出；启动后会创建两个服务对应的容器和一个默认网络。
### 7.2 生命周期命令

|功能（Operation）|实际写法（CLI Usage）|返回值与状态变化|
|---|---|---|
|解析并检查配置|`docker compose config --quiet`|配置有效时退出码为 `0`；不启动服务|
|创建并启动服务|`docker compose up -d`|创建或重建容器、网络及所需卷，并在后台运行|
|查看状态|`docker compose ps`|只读显示服务、容器、状态与端口|
|查看日志|`docker compose logs --tail=100`|只读输出最近日志|
|停止服务|`docker compose stop`|停止容器但保留容器、网络和卷|
|重新启动已有服务|`docker compose start`|启动已存在且停止的容器|
|移除应用容器与默认网络|`docker compose down`|移除容器与网络；命名卷默认保留|
|连同卷一起移除|`docker compose down -v`|额外删除声明的命名卷，可能造成永久数据丢失|

`up` 会按当前配置协调资源；配置变化时可能重建容器。`start` 只启动现有容器，不重新解释配置来创建缺少的服务。
## 8. Docker Desktop 图形界面与命令行对应

|Docker Desktop 页面|主要用途|近似命令|
|---|---|---|
|Containers|启停、删除、展开 Compose 项目|`docker ps`、`docker compose ps`|
|Images|搜索、拉取、运行和删除镜像|`docker pull`、`docker image ls`|
|Volumes|查看卷及使用关系|`docker volume ls`、`docker volume inspect`|
|Logs|查看标准输出和标准错误|`docker logs`、`docker compose logs`|
|Inspect|查看容器配置、挂载和网络|`docker inspect`|
|Exec|在运行容器内执行诊断命令|`docker exec`|
|Files|查看容器文件系统|无完全等价的单一常用命令|
|Stats|查看 CPU、内存与网络使用|`docker stats`|

Docker Desktop 适合观察和管理已运行资源；Compose 文件的创建、差异审查、自动化与复杂配置仍以文本和命令行更可靠。
## 9. 排错顺序（Troubleshooting Order）
1. `docker info`：确认 Engine 可用，而不是只看应用窗口是否打开。
2. `docker compose config --quiet`：先验证 YAML 和变量解析。
3. `docker compose ps`：定位未启动、退出或反复重启的服务。
4. `docker compose logs <service>`：找到第一条具体错误，不被后续连锁报错干扰。
5. 检查端口占用、挂载路径权限、环境变量、卷空间和网络。
6. 拉取镜像失败时区分宿主机网络与 Docker Daemon 网络；Registry 返回 `401 Unauthorized` 可能只是未鉴权，反而说明端点可达。
7. `No such image` 若紧随拉取超时出现，通常是上游镜像未下载成功造成的连锁结果。
## 10. 安全边界（Security Boundaries）
- 运行不可信 Compose 文件前检查 `privileged`、宿主机绑定挂载、`network_mode: host`、设备映射、外部文件和 Secret 引用。
- 不把密码、令牌或真实 `.env` 提交到 Git；使用秘密管理、环境变量或受控的 Compose Secret。
- 数据库卷在删除或迁移前先备份；不要把 `down -v` 当成普通停止命令。
- 不把无需公网访问的数据库、缓存或本地模型端口发布到所有网络接口。
## 11. 参考资料
- [Docker Compose 应用模型](https://docs.docker.com/compose/intro/compose-application-model/)
- [Compose 网络与服务发现](https://docs.docker.com/compose/how-tos/networking/)
- [Compose 服务与挂载配置](https://docs.docker.com/reference/compose-file/services/)
- [Compose 文件信任模型](https://docs.docker.com/compose/trust-model/)

