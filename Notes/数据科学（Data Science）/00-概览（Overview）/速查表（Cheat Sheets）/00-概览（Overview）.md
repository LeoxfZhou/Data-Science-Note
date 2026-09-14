---
title: "数据科学速查表导航（Data Science Cheat Sheet Index）"
tags:
  - data-science/cheat-sheet
status: published
updated_at: 2026-09-10
---
# 数据科学速查表导航（Data Science Cheat Sheet Index）
## 使用方法（How to Use）
- 先按领域进入对应速查表；需要完整推导、背景或项目细节时使用每篇末尾的 Wiki Link 跳转到正式 Notes。
- 速查表面向工作和学习中的实际查询，覆盖常用功能、参数、返回值、状态变化、异常、边界、组合模板和排查路径。
- API 会随版本变化；先看每篇 YAML 的验证日期与版本范围，再核对文末官方文档。
## 包名快速定位（Package Quick Lookup）

|安装包（Distribution）|导入模块（Import Module）|速查表位置|
|---|---|---|
|`numpy` / `pandas`|`numpy` / `pandas`|02-数据处理与采集：NumPy / Pandas|
|`matplotlib` / `seaborn`|`matplotlib` / `seaborn`|02-数据处理与采集：Matplotlib 与 Seaborn|
|`scikit-learn`|`sklearn`|03-机器学习：数据预处理与特征工程（入口），其余模型页按任务展开|
|`torch`|`torch`|04-深度学习：PyTorch 张量、自动微分与模块|
|`torchvision` / `albumentations`|`torchvision` / `albumentations`|05-计算机视觉：图像处理与增强|
|`torchtext` / `torchaudio` / `torchinfo` / `tensorboard` / `deepspeed`|同名模块；TensorBoard 训练端常从 `torch.utils.tensorboard` 导入|04-深度学习：PyTorch 数据、训练、推理与调试|
|`tensorflow` / `keras`|`tensorflow` / `keras`|04-深度学习：神经网络、前向传播与反向传播|
|`opencv-python` / `Pillow`|`cv2` / `PIL`|05-计算机视觉：图像处理、OpenCV、Pillow 与 Torchvision|
|`ultralytics`|`ultralytics`|05-计算机视觉：目标检测|
|`jieba` / `gensim` / `hanlp` / `hanlp-restful`|`jieba` / `gensim` / `hanlp` / `hanlp_restful`|06-NLP：预处理、传统特征与评估|
|`spacy` / `fasttext` / `wordcloud`|`spacy` / `fasttext` / `wordcloud`|06-NLP：预处理、传统特征与评估|
|`transformers` / `datasets` / `tokenizers` / `sentencepiece` / `peft`|同名模块|06-NLP：Hugging Face Tokenizer、Datasets 与 Models|
|`regex` / `sacremoses` / `boto3`|同名模块|06-NLP：Hugging Face Tokenizer、Datasets 与 Models 的可选依赖|
|`openai` / `vllm`|`openai` / `vllm`|06-NLP：大模型调用、提示词与结构化输出|
|`llama-index*` / `FlagEmbedding` / `pymilvus`|`llama_index` / `FlagEmbedding` / `pymilvus`|06-NLP：RAG、嵌入、检索与 Milvus|
|`unstructured` / `Markdown`|`unstructured` / `markdown`|06-NLP：RAG、嵌入、检索与 Milvus|
|`langchain*` / `langgraph` / `mcp`|按拆分包使用下划线导入模块|06-NLP：LangChain、LCEL、Agent、MCP 与记忆|
|`google-genai` / `langchain-google-genai`|`google.genai` / `langchain_google_genai`|06-NLP：LangChain、LCEL、Agent、MCP 与记忆|
|`sentence-transformers` / `langchain-huggingface`|`sentence_transformers` / `langchain_huggingface`|06-NLP：LangChain、LCEL、Agent、MCP 与记忆|
|`requests` / `httpx` / `beautifulsoup4` / `lxml`|`requests` / `httpx` / `bs4` / `lxml`|02-数据处理与采集：Web 数据采集|
|`selenium` / `Scrapy` / `scrapy-redis` / `itemadapter` / `ddddocr`|`selenium` / `scrapy` / `scrapy_redis` / `itemadapter` / `ddddocr`|02-数据处理与采集：Web 数据采集|
|`Twisted` / `cryptography` / `pyOpenSSL` / `pywin32`|`twisted` / `cryptography` / `OpenSSL` / `win32*`|02-数据处理与采集：Web 数据采集|
|`PyExecJS` / `pycryptodome`|`execjs` / `Crypto`|02-数据处理与采集：Web 数据采集|
|`PyMySQL` / `redis`|`pymysql` / `redis`|02-数据处理与采集：SQL、MySQL 与 Redis|
|`jupyterlab` / `ipykernel`|同名模块；主要使用 CLI|01-编程基础：Python 标准库与工程工具|
|`pytest` / `python-dotenv` / `tqdm` / `wheel`|`pytest` / `dotenv` / `tqdm` / `wheel`|07-工程与部署：Python 项目结构、配置、日志与 pytest|
|`fastapi` / `uvicorn` / `pydantic` / `python-multipart` / `Flask`|`fastapi` / `uvicorn` / `pydantic` / `multipart` / `flask`|07-工程与部署：FastAPI、Flask、ONNX 与模型部署|
|`onnx` / `onnxruntime`|`onnx` / `onnxruntime`|07-工程与部署：FastAPI、Flask、ONNX 与模型部署|
|`coremltools` / `texttable`|同名模块|07-工程与部署：FastAPI、Flask、ONNX 与模型部署|

## 01-编程基础（Programming）
Python 语法、标准库、并发、数据结构与算法，以及 C/写 C++ 时最常查的接口。
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/01-编程基础（Programming）/01-Python 语法、函数与面向对象速查表（Python Syntax, Functions, and OOP）|Python 语法、函数与面向对象速查表（Python Syntax, Functions, and OOP Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/01-编程基础（Programming）/02-Python 标准库与工程工具速查表（Python Standard Library and Engineering Tools）|Python 标准库与工程工具速查表（Python Standard Library and Engineering Tools Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/01-编程基础（Programming）/03-Python 并发与网络编程速查表（Python Concurrency and Network Programming）|Python 并发与网络编程速查表（Python Concurrency and Network Programming Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/01-编程基础（Programming）/04-Python 数据结构与算法速查表（Python Data Structures and Algorithms）|Python 数据结构与算法速查表（Python Data Structures and Algorithms）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/01-编程基础（Programming）/05-C++ 与 STL 速查表（C++ and STL）|C++ 与 STL 速查表（C++ and STL Cheat Sheet）]]
## 02-数据处理与采集（Data Processing and Collection）
数组、表格、可视化、数据库和 Web 数据获取的完整工作流。
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/02-数据处理与采集（Data Processing and Collection）/01-NumPy 速查表（NumPy）|NumPy 速查表（NumPy Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/02-数据处理与采集（Data Processing and Collection）/02-Pandas 速查表（Pandas）|Pandas 速查表（Pandas Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/02-数据处理与采集（Data Processing and Collection）/03-Matplotlib 与 Seaborn 速查表（Matplotlib and Seaborn）|Matplotlib 与 Seaborn 速查表（Matplotlib and Seaborn Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/02-数据处理与采集（Data Processing and Collection）/04-SQL、MySQL 与 Redis 速查表（SQL, MySQL, and Redis）|SQL、MySQL 与 Redis 速查表（SQL, MySQL, and Redis Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/02-数据处理与采集（Data Processing and Collection）/05-Web 数据采集速查表（Web Data Collection）|Web 数据采集速查表（Web Data Collection Cheat Sheet）]]
## 03-机器学习（Machine Learning）
预处理、经典模型、无监督学习、评估、调参与 Pipeline。
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/03-机器学习（Machine Learning）/01-数据预处理与特征工程速查表（Data Preprocessing and Feature Engineering）|数据预处理与特征工程速查表（Data Preprocessing and Feature Engineering Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/03-机器学习（Machine Learning）/02-回归与分类模型速查表（Regression and Classification Models）|回归与分类模型速查表（Regression and Classification Models Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/03-机器学习（Machine Learning）/03-树模型与集成学习速查表（Tree Models and Ensemble Learning）|树模型与集成学习速查表（Tree Models and Ensemble Learning Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/03-机器学习（Machine Learning）/04-聚类与降维速查表（Clustering and Dimensionality Reduction）|聚类与降维速查表（Clustering and Dimensionality Reduction Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/03-机器学习（Machine Learning）/05-模型评估、调参与 sklearn Pipeline 速查表（Model Evaluation, Tuning, and sklearn Pipeline）|模型评估、调参与 sklearn Pipeline 速查表（Model Evaluation, Tuning, and sklearn Pipeline Cheat Sheet）]]
## 04-深度学习（Deep Learning）
反向传播、损失、优化器和 PyTorch 训练/推理闭环。
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/04-深度学习（Deep Learning）/01-神经网络、前向传播与反向传播速查表（Neural Networks, Forward Propagation, and Backpropagation）|神经网络、前向传播与反向传播速查表（Neural Networks, Forward Propagation, and Backpropagation Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/04-深度学习（Deep Learning）/02-激活函数、输出层与损失函数速查表（Activations, Output Layers, and Loss Functions）|激活函数、输出层与损失函数速查表（Activations, Output Layers, and Loss Functions Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/04-深度学习（Deep Learning）/03-优化器、学习率与泛化速查表（Optimizers, Learning Rates, and Generalization）|优化器、学习率与泛化速查表（Optimizers, Learning Rates, and Generalization Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/04-深度学习（Deep Learning）/04-PyTorch 张量、自动微分与模块速查表（PyTorch Tensors, Autograd, and Modules）|PyTorch 张量、自动微分与模块速查表（PyTorch Tensors, Autograd, and Modules Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/04-深度学习（Deep Learning）/05-PyTorch 数据、训练、推理与调试速查表（PyTorch Data, Training, Inference, and Debugging）|PyTorch 数据、训练、推理与调试速查表（PyTorch Data, Training, Inference, and Debugging Cheat Sheet）]]
## 05-计算机视觉（Computer Vision）
图像处理、分类、检测、分割和视觉部署。
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/05-计算机视觉（Computer Vision）/01-图像处理、OpenCV、Pillow 与 Torchvision 速查表（Image Processing, OpenCV, Pillow, and Torchvision）|图像处理、OpenCV、Pillow 与 Torchvision 速查表（Image Processing, OpenCV, Pillow, and Torchvision Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/05-计算机视觉（Computer Vision）/02-CNN、经典骨干与图像分类速查表（CNN, Classic Backbones, and Image Classification）|CNN、经典骨干与图像分类速查表（CNN, Classic Backbones, and Image Classification Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/05-计算机视觉（Computer Vision）/03-目标检测速查表（Object Detection）|目标检测速查表（Object Detection Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/05-计算机视觉（Computer Vision）/04-图像分割、多尺度模块与视觉部署速查表（Image Segmentation, Multi-scale Modules, and Vision Deployment）|图像分割、多尺度模块与视觉部署速查表（Image Segmentation, Multi-scale Modules, and Vision Deployment Cheat Sheet）]]
## 06-自然语言处理与大模型（NLP and LLM）
传统 NLP、序列模型、Transformer、预训练、RAG 与 Agent。
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/06-自然语言处理与大模型（NLP and LLM）/01-NLP 预处理、传统特征与评估速查表（NLP Preprocessing, Traditional Features, and Evaluation）|NLP 预处理、传统特征与评估速查表（NLP Preprocessing, Traditional Features, and Evaluation Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/06-自然语言处理与大模型（NLP and LLM）/02-词向量、RNN、LSTM、GRU 与 Seq2Seq 速查表（Embeddings, RNN, LSTM, GRU, and Seq2Seq）|词向量、RNN、LSTM、GRU 与 Seq2Seq 速查表（Embeddings, RNN, LSTM, GRU, and Seq2Seq Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/06-自然语言处理与大模型（NLP and LLM）/03-注意力与 Transformer 速查表（Attention and Transformers）|注意力与 Transformer 速查表（Attention and Transformers Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/06-自然语言处理与大模型（NLP and LLM）/04-BERT、GPT、ELMo 与预训练速查表（BERT, GPT, ELMo, and Pretraining）|BERT、GPT、ELMo 与预训练速查表（BERT, GPT, ELMo, and Pretraining Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/06-自然语言处理与大模型（NLP and LLM）/05-Hugging Face Tokenizer、Datasets 与 Models 速查表（Hugging Face Tokenizers, Datasets, and Models）|Hugging Face Tokenizer、Datasets 与 Models 速查表（Hugging Face Tokenizers, Datasets, and Models Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/06-自然语言处理与大模型（NLP and LLM）/06-大模型调用、提示词与结构化输出速查表（LLM Calls, Prompting, and Structured Outputs）|大模型调用、提示词与结构化输出速查表（LLM Calls, Prompting, and Structured Outputs Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/06-自然语言处理与大模型（NLP and LLM）/07-RAG、嵌入、检索与 Milvus 速查表（RAG, Embeddings, Retrieval, and Milvus）|RAG、嵌入、检索与 Milvus 速查表（RAG, Embeddings, Retrieval, and Milvus Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/06-自然语言处理与大模型（NLP and LLM）/08-LangChain、LCEL、Agent、MCP 与记忆速查表（LangChain, LCEL, Agents, MCP, and Memory）|LangChain、LCEL、Agent、MCP 与记忆速查表（LangChain, LCEL, Agents, MCP, and Memory Cheat Sheet）]]
## 07-工程与部署（Engineering and Deployment）
Git/Linux/Docker、项目测试和模型服务部署。
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/07-工程与部署（Engineering and Deployment）/01-Git、Linux、Docker 与 GPU 环境速查表（Git, Linux, Docker, and GPU Environments）|Git、Linux、Docker 与 GPU 环境速查表（Git, Linux, Docker, and GPU Environments Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/07-工程与部署（Engineering and Deployment）/02-Python 项目结构、配置、日志与 pytest 速查表（Python Project Structure, Configuration, Logging, and pytest）|Python 项目结构、配置、日志与 pytest 速查表（Python Project Structure, Configuration, Logging, and pytest Cheat Sheet）]]
- [[Notes/数据科学（Data Science）/00-概览（Overview）/速查表（Cheat Sheets）/07-工程与部署（Engineering and Deployment）/03-FastAPI、Flask、ONNX 与模型部署速查表（FastAPI, Flask, ONNX, and Model Deployment）|FastAPI、Flask、ONNX 与模型部署速查表（FastAPI, Flask, ONNX, and Model Deployment Cheat Sheet）]]
