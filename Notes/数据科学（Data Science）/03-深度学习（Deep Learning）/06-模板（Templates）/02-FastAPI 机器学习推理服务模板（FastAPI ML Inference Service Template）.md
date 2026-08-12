---
title: "FastAPI 机器学习推理服务模板（FastAPI ML Inference Service Template）"
tags:
  - data-science/templates/fastapi-ml
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# FastAPI 机器学习推理服务模板（FastAPI ML Inference Service Template）
**FastAPI (基于 ASGI 协议)**：现代、高性能、天然支持异步。它最大的优势在于基于 Pydantic 的**自动类型检查与数据校验**，以及自动生成的 Swagger API 文档，是目前机器学习工程化（MLOps）的首选。

```python
import time
from typing import Optional
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
import uvicorn
from fastapi import FastAPI, HTTPException, status

# ==========================================
# 📊 Pydantic 数据契约与校验防护网
# ==========================================
class InferenceRequest(BaseModel):
    """
    是什么：请求体结构校验类
    为什么：FastAPI 核心优势之一。在进入核心算法前，自动拦截类型错误（如前端传了数字而非字符串），
           直接在网关层抛出 422 错误，保护底层算法免受脏数据污染。
    """
    image_name: str = Field(..., min_length=1, description="必须是有效的图片文件名或Base64编码")
    save_log: Optional[bool] = Field(default=False, description="[可选] 是否强制保留该次请求的日志")

class InferenceResponse(BaseModel):
    """
    是什么：响应体输出格式规范
    为什么：严格限制对外输出的 JSON 结构。即使算法内部输出了多余的敏感字段，
           FastAPI 也会根据此模型进行强行过滤，只返回定义的字段，保证对外接口的契约稳定性。
    """
    status: str
    result: str
    latency_ms: float

# ==========================================
# 📦 异步生命周期治理 (Lifespan Context)
# ==========================================
# 存储全局模型的字典，充当全局单例容器
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    是什么：现代 FastAPI 推荐的模型生命周期管理器（替代了过时的 @app.on_event("startup")）
    为什么：解耦了 Web 服务的启动与深度学习模型的加载。
           当服务器拉起时触发 yield 前的代码（加权引导）；当进程关闭（Ctrl+C）时触发 yield 后的代码，
           可以优雅地释放 GPU 显存或关闭数据库连接，防止僵尸进程驻留。
    """
    # [启动时执行]
    print("------- [Lifespan] 正在加载大模型权重至显存/内存 -------")
    # 模拟真实模型初始化
    ml_models["plate_model"] = lambda x: "沪ARZ007"
    yield
    # [关闭时执行]
    print("------- [Lifespan] 正在清空显存并优雅关闭服务 -------")
    ml_models.clear()

# 初始化 FastAPI 实例并注入生命周期管理
app = FastAPI(lifespan=lifespan)

# ==========================================
# 🛣️ 高性能 API 路由设计
# ==========================================
# ⚠️ 易错点/高危并发区（async def 与 def 的抉择）：
# 为什么这里不用 async def 而是用普通的 def？
# 是什么：这是一个高强度的 CPU 密集型/GPU 密集型矩阵运算（深度学习推理）。
# 为什么：如果在这里写 async def，而你底层的神经网络模型是同步阻塞计算（如传统的 PyTorch forward），
#        它将会死死霸占 Python 唯一的事件循环主线程，直接导致整个 FastAPI 沦为串行执行，并发数暴跌为 1！
#        使用普通的 def，FastAPI 内部的线程池（ThreadPoolExecutor）会自动接管这个路由，
#        从而在独立的线程中并发执行推理，保护主事件循环不被阻塞。
@app.post("/predict", response_model=InferenceResponse, status_code=status.HTTP_200_OK)
def predict_endpoint(payload: InferenceRequest):
    """
    是什么：高性能车牌识别推理端点
    输入：经过 Pydantic 强校验的请求对象 payload
    输出：符合 InferenceResponse 规范的响应数据
    """
    start_time = time.time()

    # 1. 动态从生命周期容器中提取全局单例模型
    model = ml_models.get("plate_model")
    if not model:
        # 为什么：防御性编程，防止网络未准备好时响应盲目请求
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is initializing or failed to load."
        )

    try:
        # 2. 执行推理管道
        raw_result = model(payload.image_name)

        # [可选功能] 根据请求中的参数决定是否启用数据增强的跟踪日志
        if payload.save_log:
            print(f"[Optional Log] File {payload.image_name} has been verified.")

        duration = (time.time() - start_time) * 1000

        # 3. 返回数据（FastAPI 会自动将 dict 转化为 Pydantic 模型并序列化为 JSON）
        return {
            "status": "success",
            "result": raw_result,
            "latency_ms": round(duration, 2)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference Engine Crash: {str(e)}"
        )

# ==========================================
# 🎛️ 控制面板：本地调试与一键切换
# ==========================================
if __name__ == "__main__":
    # 开关变量控制运行模式
    # "SERVER"       : 启动高性能 ASGI 容器 Uvicorn 运行 Web
    # "LOCAL_VERIFY" : 本地代码逻辑单元离线自检
    RUN_MODE = "SERVER"

    if RUN_MODE == "SERVER":
        print("[Mode] 正在由 Uvicorn ASGI 服务器拉起服务...")
        # ⚠️ 易错点/多进程配置说明：
        # 1. workers=1: 当部署深度学习模型时，如果设置多个 workers，每个子进程都会完整复制一份模型到显存中，
        #    极易导致显存爆炸（OOM）。在显存敏感的 GPU 环境下，建议多进程交给外部 K8s 调度，此处保持 1。
        # 2. app="fastapi_app:app": 这里的字符串必须对应 "当前文件名:FastAPI变量名"。
        uvicorn.run("fastapi_app:app", host="0.0.0.0", port=5000, workers=1, reload=False)

    elif RUN_MODE == "LOCAL_VERIFY":
        print("[Mode] 正在验证 Pydantic 数据契约的约束力...")
        # 前置条件：手动模拟前端构造的非法与合法数据，验证防御能力
        print("1. 测试空数据拦截机制：")
        try:
            # 故意传入非法空字符串，看是否能触发我们的 Field 最小长度过滤
            bad_data = InferenceRequest(image_name="")
        except Exception as ve:
            print(f"-> 拦截成功（预期内报错）: {ve}")

        print("\n2. 测试正常数据映射机制：")
        good_data = InferenceRequest(image_name="test_plate.jpg", save_log=True)
        print(f"-> 数据成功解析成对象，对象属性 image_name = {good_data.image_name}")
```
