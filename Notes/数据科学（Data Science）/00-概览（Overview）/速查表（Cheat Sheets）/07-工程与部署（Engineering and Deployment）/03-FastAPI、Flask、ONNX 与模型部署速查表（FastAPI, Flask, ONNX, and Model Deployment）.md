---
title: "FastAPI、Flask、ONNX 与模型部署速查表（FastAPI, Flask, ONNX, and Model Deployment Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - engineering/deployment
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "FastAPI 0.115+；Flask 3.x；ONNX/ONNX Runtime 当前稳定版"
---
# FastAPI、Flask、ONNX 与模型部署速查表（FastAPI, Flask, ONNX, and Model Deployment Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
服务启动时一次加载模型，单请求只做验证、预处理、批处理调度、推理和后处理。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 2. 包级安装与导入索引（Package Installation and Import Index）
### 2.1 FastAPI、Uvicorn 与 Pydantic（FastAPI, Uvicorn, and Pydantic）
- **安装包（Distribution）**：`fastapi`、`uvicorn`、`pydantic`；表单和文件上传另需 `python-multipart`。
- **导入模块（Import Module）**：`fastapi`、`uvicorn`、`pydantic`；`python-multipart` 由 Starlette/FastAPI 间接使用，一般不直接导入。
- **安装命令（Installation）**：`python -m pip install -U fastapi 'uvicorn[standard]' pydantic python-multipart`。
- **用途（Purpose）**：FastAPI 提供 ASGI 路由与 OpenAPI，Uvicorn 运行 ASGI 应用，Pydantic 验证输入输出模型。
- **正式笔记（Detailed Note）**：[[01-FastAPI 核心开发参考（FastAPI Core Development Reference）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|应用|`FastAPI(lifespan=...)`|返回 ASGI 应用|
|数据模型|`class Input(BaseModel): ...`|定义验证与序列化 schema|
|文件上传|`UploadFile` / `File(...)`|解析 multipart 流；需要 `python-multipart`|
|启动服务|`uvicorn module:app --host ... --port ...`|启动常驻 ASGI 服务|

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

class Item(BaseModel):
    value: int

app = FastAPI()

@app.post("/double")
def double(item: Item) -> dict[str, int]:
    return {"result": item.value * 2}

response = TestClient(app).post("/double", json={"value": 3})
print(response.status_code, response.json())  # 输出: 200 {'result': 6}
```
```bash
uvicorn module_name:app --host 0.0.0.0 --port 8000
# 启动常驻网络服务；生产环境需配置进程管理、超时、访问日志和反向代理。
```
```python
import multipart

print(isinstance(multipart.__version__, str))  # 输出: True
# FastAPI 接收 Form 或 UploadFile 时会检查该依赖；不需要在路由代码中直接导入。
```
### 2.2 Flask（Flask）
- **安装包（Distribution）**：`Flask`。
- **导入模块（Import Module）**：`flask`。
- **安装命令（Installation）**：`python -m pip install -U Flask`。
- **用途（Purpose）**：轻量 WSGI Web 应用、路由、请求与响应处理。
- **正式笔记（Detailed Note）**：[[03-Flask 机器学习推理服务模板（Flask ML Inference Service Template）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|应用|`Flask(__name__)`|返回 WSGI 应用|
|注册路由|`@app.get(path)` / `@app.post(path)`|原地更新路由表|
|JSON 请求|`request.get_json()`|返回 Python 对象或错误响应|
|JSON 响应|`jsonify(data)`|返回带 JSON MIME 类型的 Response|

```python
from flask import Flask

app = Flask(__name__)

@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}

with app.test_client() as client:
    response = client.get("/health")
    print(response.status_code, response.get_json())  # 输出: 200 {'ok': True}
```
### 2.3 ONNX 与 ONNX Runtime（ONNX and ONNX Runtime）
- **安装包（Distribution）**：`onnx`；CPU 推理为 `onnxruntime`，GPU 推理通常为 `onnxruntime-gpu`，同一环境避免同时安装 CPU/GPU 变体。
- **导入模块（Import Module）**：`onnx`、`onnxruntime`（惯例别名 `ort`）。
- **安装命令（Installation）**：`python -m pip install -U onnx onnxruntime`；GPU 版本按官方兼容矩阵安装。
- **用途（Purpose）**：ONNX 定义和校验模型图，ONNX Runtime 负责跨平台推理。
- **正式笔记（Detailed Note）**：[[07-ONNX 环境与模型图检查（Environment and Model Graph Inspection）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|读取模型|`onnx.load(path)`|读取文件并返回 ModelProto|
|校验模型|`onnx.checker.check_model(model)`|成功返回 `None`，无效模型抛异常|
|创建会话|`ort.InferenceSession(path, providers=[...])`|加载模型并返回推理会话|
|输入信息|`session.get_inputs()`|返回输入 NodeArg 列表|
|执行推理|`session.run(output_names, feeds)`|返回 NumPy 数组列表|
|可用执行器|`ort.get_available_providers()`|返回当前环境 Provider 名称列表|

```python
import onnx
import onnxruntime as ort

print(isinstance(onnx.__version__, str))  # 输出: True
print(isinstance(ort.get_available_providers(), list))  # 输出: True
# InferenceSession 会读取模型文件；Provider 可用性取决于安装包、系统和硬件。
```
### 2.4 Core ML Tools（Core ML Tools）
- **安装包（Distribution）**：`coremltools`。
- **导入模块（Import Module）**：`coremltools`，惯例别名为 `ct`。
- **安装命令（Installation）**：`python -m pip install -U coremltools`；受支持的 Python、macOS 与模型前端版本必须按官方矩阵核对。
- **用途（Purpose）**：把 PyTorch/TensorFlow 模型转换为 Apple Core ML 格式并检查模型规格。
- **正式笔记（Detailed Note）**：[[09-YOLOv5 架构、训练与部署边界（YOLOv5 Architecture, Training, and Deployment）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|转换|`ct.convert(model, inputs=..., convert_to='mlprogram')`|返回 MLModel；执行模型转换|
|加载|`ct.models.MLModel(path)`|读取 Core ML 模型并返回对象|
|保存|`model.save(path)`|写 `.mlpackage` 或 `.mlmodel`|
|预测|`model.predict(inputs)`|在支持的平台返回输出字典|

```python
import coremltools as ct

print(isinstance(ct.__version__, str))  # 输出: True
# ct.convert(...) 会加载并转换模型，可能占用大量内存并写出 .mlpackage/.mlmodel。
```
### 2.5 texttable 命令行表格（texttable Console Tables）
- **安装包（Distribution）**：`texttable`。正式来源中的 `text-table` 写法不是当前常用安装名，速查表使用可核验的 PyPI 名称。
- **导入模块（Import Module）**：`texttable`。
- **安装命令（Installation）**：`python -m pip install -U texttable`。
- **用途（Purpose）**：在终端输出纯文本表格，某些模型导出/检查脚本将其作为辅助依赖。
- **正式笔记（Detailed Note）**：[[09-YOLOv5 架构、训练与部署边界（YOLOv5 Architecture, Training, and Deployment）]]。

```python
from texttable import Texttable

table = Texttable()
table.add_rows([["name", "value"], ["loss", 0.2]])
print("loss" in table.draw())  # 输出: True
```
## FastAPI 接口（FastAPI APIs）
类型注解和 Pydantic 模型同时生成验证与 OpenAPI schema。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|应用|`app=FastAPI(lifespan=lifespan)`|返回 ASGI 应用|
|GET|`@app.get('/health')`|注册路由|
|POST|`@app.post('/predict',response_model=Output)`|注册并验证响应|
|请求体|`payload: InputModel`|解析并验证 JSON|
|路径参数|`item_id:int`|验证 URL 路径值|
|查询参数|`limit:int=Query(10,ge=1,le=100)`|验证查询值|
|依赖|`Depends(get_service)`|注入请求依赖|
|错误|`raise HTTPException(status_code=400,detail=...)`|返回结构化 HTTP 错误|
|上传|`UploadFile`|返回流式临时文件接口|
|测试|`TestClient(app)`|返回同步测试客户端|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
app=FastAPI()
@app.get("/health")
def health(): return {"ok":True}
r=TestClient(app).get("/health")
print(r.status_code,r.json())
# 期望输出:
# 200 {'ok': True}
```
## Flask 与服务生命周期（Flask and Lifecycle）
Flask 核心轻量，验证、schema 和依赖管理需自行组合。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|应用|`app=Flask(__name__)`|返回 WSGI 应用|
|路由|`@app.get('/health')`|注册视图|
|JSON 请求|`request.get_json()`|返回 Python 对象或错误|
|JSON 响应|`jsonify(result)`|返回 Response|
|错误处理|`@app.errorhandler(ExceptionType)`|注册错误转换|
|应用配置|`app.config.from_prefixed_env()`|从前缀环境变量加载|
|请求上下文|`g.model`|保存单请求状态|
|测试客户端|`app.test_client()`|返回测试客户端|
|Gunicorn|`gunicorn 'package:create_app()' -w 4`|启动多 worker 服务|
|健康检查|`区分 liveness/readiness`|返回进程/依赖可用性|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
from flask import Flask
app=Flask(__name__)
@app.get("/health")
def health(): return {"ok":True}
with app.test_client() as c:
    r=c.get("/health"); print(r.status_code,r.json)
# 期望输出:
# 200 {'ok': True}
```
## ONNX、推理优化与生产（ONNX and Production Inference）
导出只是第一步，必须用代表性输入比较数值和动态形状。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|导出|`torch.onnx.export(model,args,path,input_names=...,dynamic_axes=...)`|写 ONNX 文件|
|检查|`onnx.checker.check_model(model)`|无效图抛 ValidationError|
|会话|`ort.InferenceSession(path,providers=[...])`|返回推理会话|
|输入元数据|`session.get_inputs()`|返回输入节点列表|
|运行|`session.run(output_names,input_feed)`|返回 NumPy 输出列表|
|执行提供器|`session.get_providers()`|返回可用 provider 顺序|
|动态量化|`quantize_dynamic(input,output,weight_type=QInt8)`|写量化模型|
|批处理|`按最大批量或等待时间聚合请求`|提高吞吐并增加延迟|
|预热|`启动时执行若干代表性推理`|初始化内核与缓存|
|并发限制|`Semaphore / worker 数 / GPU 队列`|防止显存和延迟失控|
|监控|`延迟分位数、吞吐、错误率、队列、漂移`|返回服务健康指标|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import numpy as np
x=np.array([[1.,2.]],dtype=np.float32)
print(x.dtype,x.shape)
# 期望输出:
# float32 (1, 2)
```
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
- [[07-ONNX 环境与模型图检查（Environment and Model Graph Inspection）]]
- [[09-YOLOv5 架构、训练与部署边界（YOLOv5 Architecture, Training, and Deployment）]]
- [[01-FastAPI 核心开发参考（FastAPI Core Development Reference）]]
- [[01-基于 NumPy 的三层 BP 神经网络（Three-layer BP Neural Network with NumPy）]]
- [[01-智能闸杆系统架构与项目模板（SmartGate Architecture and Project Template）]]
- [[02-FastAPI 机器学习推理服务模板（FastAPI ML Inference Service Template）]]
- [[03-Flask 机器学习推理服务模板（Flask ML Inference Service Template）]]
## 官方参考（Official References）
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Uvicorn 文档](https://www.uvicorn.org/)
- [Flask 文档](https://flask.palletsprojects.com/)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [ONNX Runtime 文档](https://onnxruntime.ai/docs/)
- [FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
