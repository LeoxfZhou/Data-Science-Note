## 项目目录结构

```text
SmartGate_AI/                   # 项目根目录
├── configs/                    # 1. 配置中心
│   ├── service_config.yaml     # 服务端口、超时时间、服务间路由配置
│   └── model_hyper.yaml        # 模型训练/推理超参数配置
│
├── data/                       # 2. 数据仓库
│   ├── raw/                    # 摄像头采集的原始全景图
│   ├── processed/              # 裁剪后的车牌/车辆特写数据集
│   └── annotations/            # 数据标签（YOLO格式的txt、OCR格式的文本）
│
├── training/                   # 3. 算法炼丹炉（微调与实验）
│   ├── detect_train/           # 目标检测（如YOLO）训练代码与loss日志
│   └── ocr_train/              # 字符识别（如CRNN/ConvNeXt）微调代码
│
├── services/                   # 4. 前线战场：微服务集群（核心部署区）
│   ├── detector_service/       # 服务A：检测节点 (建议端口 9001)
│   │   ├── models/             # 存放 best.onnx 或 TensorRT 引擎
│   │   ├── predictor.py        # 底层推理驱动（图像前处理、NMS后处理）
│   │   └── app.py              # Flask/FastAPI 接口服务
│   │
│   ├── recognizer_service/     # 服务B：识别节点 (建议端口 9002)
│   │   ├── models/             # 存放 OCR 微调后的模型权重
│   │   ├── ocr_engine.py       # 文字破译底层驱动
│   │   └── app.py              # Flask/FastAPI 接口服务
│   │
│   ├── orchestrator/           # 核心：中控网关调度器 (建议端口 9993)
│   │   ├── pipeline.py         # 流水线总指挥（串联服务A与服务B）
│   │   ├── business_logic.py   # 业务逻辑（白名单比对、扣费状态校验）
│   │   └── server.py           # 对外提供给摄像头的终极 API 入口
│   │
│   └── hardware_agent/         # 硬件控制代理服务
│       ├── mqtt_client.py      # 通过 MQTT 协议发布“抬杆”指令给物联网网关
│       └── serial_controller.py# 通过 RS485/串口 直接发送十六进制电平开闸
│
├── shared_utils/               # 5. 公共工具库
│   ├── __init__.py
│   ├── image_tool.py           # 图像编解码（Base64转换、内存裁剪Image.crop）
│   └── logger.py               # 工业级多进程安全日志组件（按天切分日志）
│
├── tests/                      # 6. 验收与仿真测试
│   ├── mock_camera.py          # 模拟路口摄像头高并发压测脚本
│   └── test_pipeline.py        # 端到端（E2E）功能完备性测试
│
├── requirements.txt            # 项目依赖清单
└── README.md                   # 部署与运维手册

