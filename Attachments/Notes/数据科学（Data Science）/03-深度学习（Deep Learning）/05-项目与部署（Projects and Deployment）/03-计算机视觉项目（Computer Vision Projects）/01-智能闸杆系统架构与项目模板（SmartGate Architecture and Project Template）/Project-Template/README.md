# SmartGate AI 可复用项目模板（Reusable Project Template）

这套模板把车牌检测（Plate Detection）、光学字符识别（Optical Character Recognition, OCR）、业务编排（Orchestration）和可选硬件控制（Optional Hardware Control）拆成可独立测试的组件。默认使用模拟推理（Mock Inference），所以不下载权重也能先跑通管道。

## 快速启动（Quick Start）
1. 创建虚拟环境：`python -m venv .venv`。
2. 激活环境：macOS/Linux 使用 `source .venv/bin/activate`，Windows PowerShell 使用 `.venv\Scripts\Activate.ps1`。
3. 安装依赖：`python -m pip install -r requirements.txt`。
4. 运行无网络冒烟测试：`python -m pytest -q`。
5. 分别启动三个服务：
   - `uvicorn services.detector_service.app:app --port 9001`
   - `uvicorn services.recognizer_service.app:app --port 9002`
   - `uvicorn services.orchestrator.server:app --port 9993`

## 最先替换的三处（First Three Replacements）
- `configs/service_config.yaml`：端口、URL、超时、MQTT 和串口配置。
- `configs/model_hyper.yaml`：检测/OCR 权重、阈值、图像尺寸和训练参数。
- `services/*/predictor.py` 或 `ocr_engine.py`：把模拟推理替换成真实 YOLO 与 OCR 推理引擎。

## 运行模式（Run Modes）
- **模拟模式（Mock Mode）**：不需要 GPU、摄像头或模型权重，用于验证接口和业务状态机。
- **真实模式（Real Mode）**：加载检测与 OCR 权重；必须补充预处理、后处理、设备选择和并发策略。
- **硬件模式（Hardware Mode）**：在业务放行后通过 MQTT 或串口发出开闸命令；默认关闭，避免误动作。

## 安全边界（Safety Boundaries）
- Web 服务的成功响应不等于物理设备已执行；硬件确认需要单独的回执（Acknowledgement）。
- 模型置信度低、服务超时、车牌为空或授权失败时默认拒绝开闸（Fail Closed）。
- 密钥、MQTT 密码、串口设备名和真实车牌日志应通过环境变量或本地配置注入，不提交到 Git。
