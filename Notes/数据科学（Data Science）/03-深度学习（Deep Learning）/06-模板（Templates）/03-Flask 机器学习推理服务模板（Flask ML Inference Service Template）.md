---
title: "Flask 机器学习推理服务模板（Flask ML Inference Service Template）"
tags:
  - data-science/templates/flask-ml
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# Flask 机器学习推理服务模板（Flask ML Inference Service Template）
**Flask (基于 WSGI 协议)**：老牌、轻量、纯同步。它的开发心智负担低，周边生态极度成熟，非常适合中小型项目或使用 ONNXRuntime、TensorRT 等本身已释放 GIL（全局解释器锁）的多线程推理场景。

```python
import os
import time
from flask import Flask, request, jsonify

# ==========================================
# 🎛️ 全局配置与安全防线
# ==========================================
app = Flask(__name__)

# [配置项] 限制上传文件的最大体积（此处限制为 16MB）
# 是什么：Flask 内置的数据流截断配置。
# 为什么：生产环境下必须配置！防止恶意客户端上传数 GB 的超大文件导致服务器内存耗尽（OOM），直接挂掉。
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# [可选配置] 是否保存推理的中间结果图或特征图
# 开启后果：会在本地磁盘产生 IO 读写，降低吞吐量，适用于 Debug 调试或审计阶段。
# 关闭后果：纯内存计算，速度最快，适用于高并发生产环境。
SAVE_INTERMEDIATE_RESULTS = False

# ==========================================
# 📦 模型生命周期管理 (模拟你的车牌识别模型)
# ==========================================
class MockModel:
    """
    是什么：模拟深度学习推理引擎（如 YOLO 或 CRNN）
    为什么：在 Web 框架中，必须将模型实例在全局初始化一次，严禁在路由函数内部重复加载模型，
           因为加载权重是极度耗时的重型 IO 操作。
    """
    def __init__(self):
        # [可选功能] 可选择是否模拟加载大规模权重
        # 适用场景：测试生产环境部署时开启，日常跑纯单元测试（Unit Test）时可关闭以加速脚本拉起。
        self.use_heavy_weights = True
        if self.use_heavy_weights:
            time.sleep(0.5) # 模拟加载 best.onnx 的耗时
        self.model_name = "Plate_Recognition_v1.0"

    def preprocess(self, data):
        # 是什么：前处理阶段（如图像等比例缩放 Letterbox、归一化）
        return f"Preprocessed[{data}]"

    def predict_core(self, tensor):
        # 是什么：核心矩阵前向传播推理
        return "沪A8C871"

# ⚠️ 高危易错点（多线程环境下的单例模型）：
# 在全局作用域实例化模型。注意：Flask 在默认情况下开启了多线程（threaded=True）。
# 如果你的底层网络权重（如原生 PyTorch 未释放 GIL 的模型）不是线程安全的，并发请求时会导致 CUDA 报错或内存越界。
# 解决方案：使用线程安全引擎（如 ONNX Runtime）或在推理阶段加线程锁（Lock），或者使用多进程 Gunicorn 部署。
GLOBAL_MODEL = MockModel()

# ==========================================
# 🛣️ API 路由与业务逻辑编排
# ==========================================
@app.route('/predict', methods=['POST'])
def predict_endpoint():
    """
    是什么：标准的 Web 推理网关入口
    为什么：接收用户图像流，串联“前处理 -> 推理 -> 后处理”，并提供完善的异常捕获。
    """
    start_time = time.time()

    # 1. 健壮性校验：判断请求合法性
    if 'image_name' not in request.json:
        # 为什么：必须显式返回 HTTP 400 状态码，告诉前端请求参数缺失，而不是让代码报 KeyError 抛出 500
        return jsonify({"error": "Missing 'image_name' key in JSON payload"}), 400

    try:
        input_data = request.json['image_name']

        # 2. 调用单步流程 1：前处理
        features = GLOBAL_MODEL.preprocess(input_data)

        # 3. 调用单步流程 2：核心推理
        raw_result = GLOBAL_MODEL.predict_core(features)

        # [可选功能分支] 保存中间结果
        if SAVE_INTERMEDIATE_RESULTS:
            # 为什么：抽象出独立的分支，避免污染核心计算图的内存
            with open("debug_infer_log.txt", "a") as f:
                f.write(f"{input_data} -> {raw_result}\n")

        # 4. 构建标准响应体
        duration = (time.time() - start_time) * 1000 # 毫秒化
        return jsonify({
            "status": "success",
            "result": raw_result,
            "latency_ms": round(duration, 2)
        }), 200

    except Exception as e:
        # ⚠️ 易错点：切忌直接把原始的 Python Exception 字符串完全抛给公网用户（可能泄露代码路径或凭证）
        # 为什么：在后台日志打印真实错误便于排查，对外屏蔽敏感信息。
        app.logger.error(f"Prediction failed: {str(e)}")
        return jsonify({"error": "Internal server processing error"}), 500

# ==========================================
# 🎛️ 控制面板：本地调试与一键切换
# ==========================================
if __name__ == "__main__":
    # 开关变量控制运行模式
    # "SERVER"       : 真正拉起 Flask Web 服务器，挂起进程监听网关
    # "LOCAL_STEP"   : 本地单步单元测试（不需要拉起网络服务，不占端口）
    # "LOCAL_FLOW"   : 本地组合流管道验证（模拟完整的业务流水线）
    RUN_MODE = "SERVER"

    if RUN_MODE == "SERVER":
        print("[Mode] 正在启动线上生产级 Web 服务...")
        # ⚠️ 易错点/环境变量警示：
        # 1. 严禁在生产环境下将 debug 设置为 True！Debug 模式会开启 Werkzeug 重载器，允许远程执行任意代码，引发安全漏洞。
        # 2. host='0.0.0.0' 代表监听容器/宿主机的所有网络接口，这样外部网络（如你的 API 测试客户端）才能正常连接。
        app.run(host="0.0.0.0", port=9001, debug=False)

    elif RUN_MODE == "LOCAL_STEP":
        print("[Mode] 正在执行本地单步功能验证...")
        # 前置条件：GLOBAL_MODEL 必须成功初始化完毕
        test_img = "mock_car.jpg"
        step1 = GLOBAL_MODEL.preprocess(test_img)
        print(f"步骤 1 (前处理转换) 结果: {step1}")
        step2 = GLOBAL_MODEL.predict_core(step1)
        print(f"步骤 2 (字符识别推理) 结果: {step2}")

    elif RUN_MODE == "LOCAL_FLOW":
        print("[Mode] 正在执行全管道组合流验证...")
        # 前置条件：必须以 Mock 方式调用，模拟整个 Web 接收到解析的闭环
        # 这里直接模拟路由内部执行的组合逻辑
        test_payload = "mock_pipeline_car.png"
        pipeline_res = GLOBAL_MODEL.predict_core(GLOBAL_MODEL.preprocess(test_payload))
        print(f"组合流端到端输出车牌: {pipeline_res} -> [验证通过]")
```
