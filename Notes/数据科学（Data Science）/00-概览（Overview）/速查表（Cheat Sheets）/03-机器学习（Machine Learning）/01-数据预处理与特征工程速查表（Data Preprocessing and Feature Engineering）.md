---
title: "数据预处理与特征工程速查表（Data Preprocessing and Feature Engineering Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - machine-learning
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "scikit-learn 1.5–1.9；以当前稳定版官方文档为准"
---
# 数据预处理与特征工程速查表（Data Preprocessing and Feature Engineering Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
安装：`python -m pip install scikit-learn`；常用导入：`import sklearn`。训练集拟合一切有状态变换，验证/测试集只调用 `transform`/`predict`。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
### scikit-learn 包信息（scikit-learn Package Metadata）
- **安装包（Distribution）**：`scikit-learn`。
- **导入模块（Import Module）**：`sklearn`。
- **安装命令（Installation）**：`python -m pip install -U scikit-learn`。
- **用途（Purpose）**：预处理、特征工程、经典机器学习模型、评估、模型选择与流水线。
- **正式笔记（Detailed Note）**：[[01-机器学习概览（Machine Learning Overview）]]。

```python
from sklearn.preprocessing import StandardScaler

scaled = StandardScaler().fit_transform([[1.0], [3.0]])
print(scaled.ravel().tolist())  # 输出: [-1.0, 1.0]
```
- **版本边界（Version Boundary）**：持久化的 sklearn 模型不保证跨版本兼容；训练与加载环境应固定相同依赖版本。
## 数据拆分与泄漏防护（Splitting and Leakage Prevention）
先拆分再拟合预处理器；时间数据不得随机打乱未来到过去。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|随机拆分|`train_test_split(X, y, test_size=.2, stratify=y, random_state=42)`|返回训练/测试数组|
|K 折|`KFold(n_splits=5, shuffle=True, random_state=42)`|返回索引划分器|
|分层 K 折|`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`|保持类别比例|
|分组 K 折|`GroupKFold(n_splits=5)`|同一组不跨训练验证|
|时间序列拆分|`TimeSeriesSplit(n_splits=5)`|返回时间有序划分|
|交叉验证预测|`cross_val_predict(estimator, X, y, cv=5)`|返回每样本折外预测|
|学习曲线|`learning_curve(estimator, X, y, cv=5)`|返回训练规模和分数矩阵|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.model_selection import train_test_split
X = [[i] for i in range(10)]; y = [0]*5 + [1]*5
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, stratify=y, random_state=42)
print(len(X_train), len(X_test), sum(y_test))
# 期望输出:
# 8 2 1
```
## 缺失值与缩放（Imputation and Scaling）
树模型通常不需要缩放；距离、梯度和正则化模型通常需要。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|简单填补|`SimpleImputer(strategy='median')`|返回填补器；fit 学习统计量|
|迭代填补|`IterativeImputer(...)`|实验性多变量填补器|
|缺失指示|`MissingIndicator(features='missing-only')`|返回缺失布尔特征|
|标准化|`StandardScaler()`|学习均值/标准差并输出缩放数组|
|区间缩放|`MinMaxScaler(feature_range=(0,1))`|缩放到训练集范围|
|稳健缩放|`RobustScaler()`|使用中位数与四分位距|
|单位范数|`Normalizer(norm='l2')`|逐样本缩放，无需学习统计量|
|幂变换|`PowerTransformer(method='yeo-johnson')`|减少偏态并可标准化|
|分位数变换|`QuantileTransformer(output_distribution='normal')`|映射经验分布|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
X = np.array([[1., np.nan], [3., 4.], [5., 8.]])
filled = SimpleImputer(strategy="median").fit_transform(X)
scaled = StandardScaler().fit_transform(filled)
print(filled.tolist())
print(np.round(scaled.mean(axis=0), 7).tolist())
# 期望输出:
# [[1.0, 6.0], [3.0, 4.0], [5.0, 8.0]]
# [0.0, 0.0]
```
## 类别、文本与组合特征（Categorical, Text, and Composition）
未知类别策略必须在训练时定义。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|独热编码|`OneHotEncoder(handle_unknown='ignore', sparse_output=True)`|返回稀疏矩阵|
|序数编码|`OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)`|返回数值数组|
|标签编码|`LabelEncoder()`|仅用于目标 y，返回整数标签|
|词袋|`CountVectorizer(ngram_range=(1,1), min_df=1)`|返回稀疏计数矩阵|
|TF-IDF|`TfidfVectorizer(ngram_range=(1,2), max_features=None)`|返回稀疏权重矩阵|
|列级变换|`ColumnTransformer(transformers, remainder='drop')`|拼接不同列变换结果|
|多项式特征|`PolynomialFeatures(degree=2, include_bias=False)`|返回交互项数组|
|自定义变换|`FunctionTransformer(func, validate=False)`|返回可放进 Pipeline 的变换器|
|特征联合|`FeatureUnion(transformer_list)`|横向拼接多个变换输出|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
X = pd.DataFrame({"age": [20, 40], "city": ["A", "B"]})
prep = ColumnTransformer([("num", StandardScaler(), ["age"]), ("cat", OneHotEncoder(sparse_output=False), ["city"])])
print(prep.fit_transform(X).tolist())
# 期望输出:
# [[-1.0, 1.0, 0.0], [1.0, 0.0, 1.0]]
```
## 特征选择与不平衡（Feature Selection and Imbalance）
特征选择必须在交叉验证内部拟合；重采样也只作用于训练折。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|低方差过滤|`VarianceThreshold(threshold=0)`|返回保留特征的变换器|
|单变量选择|`SelectKBest(score_func=f_classif, k=10)`|返回最高分特征|
|模型选择|`SelectFromModel(estimator, threshold='median')`|按模型重要性选特征|
|递归消除|`RFE(estimator, n_features_to_select=...)`|迭代删除较弱特征|
|类别权重|`class_weight='balanced'`|按频率反比调整损失权重|
|样本权重|`estimator.fit(X, y, sample_weight=w)`|影响训练目标，返回已拟合模型|
|随机过采样|`RandomOverSampler(random_state=42)`|imblearn 返回重采样数据|
|SMOTE|`SMOTE(random_state=42)`|合成少数类样本；不能在拆分前执行|
|随机欠采样|`RandomUnderSampler(random_state=42)`|删除多数类样本|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import numpy as np
from sklearn.feature_selection import VarianceThreshold
X = np.array([[1, 0, 3], [1, 2, 4], [1, 4, 5]])
sel = VarianceThreshold()
print(sel.fit_transform(X).tolist())
print(sel.get_support().tolist())
# 期望输出:
# [[0, 3], [2, 4], [4, 5]]
# [False, True, True]
```
## 高频工作模式（Common Workflows）
- **最小闭环（Minimum Loop）**：先用最小输入跑通读取、转换、验证与输出，再替换真实数据。
- **组合优先（Composition First）**：把解析、业务逻辑和 I/O 分层，便于单元测试和复用。
- **可观测性（Observability）**：在边界处记录输入规模、关键参数、耗时和异常，不记录凭据。
- **可复现性（Reproducibility）**：固定随机种子、依赖版本和配置，并保存数据与模型版本。
## 常见错误与排查（Common Errors and Troubleshooting）
- **类型或形状不匹配**：先打印 `type`、`dtype`、`shape`，再检查广播、索引和设备。
- **隐式修改**：链式操作前确认是否原地修改；必要时显式复制并写测试。
- **边界遗漏**：至少覆盖空输入、单元素、重复值、极端值和非法参数。
- **版本漂移**：遇到弃用警告时查询当前官方迁移说明，不长期屏蔽警告。
## 相关详细笔记（Detailed Notes）
- [[数据科学（Data Science）]]
- [[01-Python 环境配置（Environment Setup）]]
- [[02-Python 基础语法（Python Basics）]]
- [[03-错误与异常（Errors and Exceptions）]]
- [[04-文件、路径、模块与包（Files Paths Modules and Packages）]]
- [[05-面向对象编程（Object-Oriented Programming）]]
- [[06-正则表达式（Regular Expressions）]]
- [[07-Python 并发与网络编程（Python Concurrency and Networking）]]
- [[01-NumPy 数值计算（NumPy）]]
- [[02-Pandas 数据处理（Pandas）]]
- [[03-Matplotlib 数据可视化（Matplotlib Data Visualization）]]
- [[01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）]]
- [[02-二分查找与边界搜索（Binary Search and Boundary Queries）]]
- [[03-顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）]]
- [[04-链表结构与实现（Linked-list Structures and Implementations）]]
- [[05-链表典型算法（Classic Linked-list Algorithms）]]
- [[06-递归、栈、队列与双端队列（Recursion, Stacks, Queues, and Deques）]]
- [[07-优先队列、堆与并查集（Priority Queues, Heaps, and Disjoint Sets）]]
- [[08-树、二叉搜索树与平衡树（Trees, Binary Search Trees, and Balanced Trees）]]
- [[09-哈希表与排序算法（Hash Tables and Sorting Algorithms）]]
- [[10-图结构、遍历与最短路径（Graphs, Traversal, and Shortest Paths）]]
- [[11-贪心、动态规划与分治（Greedy, Dynamic Programming, and Divide and Conquer）]]
- [[12-双指针、字符串与数据结构设计题（Two Pointers, Strings, and Data-structure Design）]]
- [[13-算法图示索引（Algorithm Diagram Index）]]
- [[01-Python 爬虫前置基础（Python Prerequisites for Web Scraping）]]
- [[02-HTML 与 CSS 页面结构（HTML and CSS Page Structure）]]
- [[03-网页解析：正则、XPath 与 Beautiful Soup（Web Parsing）]]
- [[04-HTTP 请求与反爬处理（HTTP Requests and Anti-scraping）]]
- [[05-Selenium 浏览器自动化（Selenium Browser Automation）]]
- [[06-爬虫数据存储：MySQL 与 Redis（Crawler Data Storage）]]
- [[07-Scrapy 与 Scrapy-Redis 框架（Scrapy and Scrapy-Redis Frameworks）]]
- [[08-逆向分析与加密基础（Reverse Engineering and Cryptography Basics）]]
- [[01-C++ 环境与编译（Environment and Compilation）]]
- [[02-C++ 基础语法、预处理与控制流（Basics Preprocessing and Control Flow）]]
- [[03-C++ 自定义数据类型（Custom Data Types）]]
- [[04-C++ 指针、引用、数组与字符串（Pointers References Arrays and Strings）]]
- [[05-C++ 函数、回调与递归（Functions Callbacks and Recursion）]]
- [[06-C++ 存储期与内存管理（Storage Duration and Memory Management）]]
- [[07-ONNX 环境与模型图检查（Environment and Model Graph Inspection）]]
- [[08-C++ 类、对象、继承与多态（Classes, Inheritance, and Polymorphism）]]
- [[09-C++ 文件流与持久化（File Streams and Persistence）]]
- [[10-C++ 模板与泛型编程（Templates and Generic Programming）]]
- [[11-C++ STL 容器与迭代器（STL Containers and Iterators）]]
- [[12-C++ 函数对象与 STL 算法（Function Objects and STL Algorithms）]]
- [[01-通讯录管理系统（Address Book Management System）]]
- [[02-职工管理系统（Employee Management System）]]
- [[03-机房预约系统（Computer Room Reservation System）]]
- [[04-演讲比赛流程管理系统（Speech Contest Workflow System）]]
- [[01-机器学习概览（Machine Learning Overview）]]
- [[01-集成学习方法（Ensemble Learning Methods）]]
- [[01-深度学习概览（Deep Learning Overview）]]
- [[01-人工神经网络与前向传播（Artificial Neural Networks and Forward Propagation）]]
- [[02-神经网络损失函数与输出契约（Neural Network Loss Functions and Output Contracts）]]
- [[03-反向传播与链式法则（Backpropagation and the Chain Rule）]]
- [[04-梯度下降、优化器与学习率调度（Gradient Descent, Optimizers, and Learning-rate Scheduling）]]
- [[01-PyTorch 数据集、变换与加载器（PyTorch Datasets, Transforms, and DataLoaders）]]
- [[02-PyTorch 模型工程结构与环境（PyTorch Model Engineering Structure and Environment）]]
- [[03-神经网络激活函数（Neural Network Activation Functions）]]
- [[04-PyTorch 训练与评估循环（PyTorch Training and Evaluation Loops）]]
- [[05-PyTorch 模型持久化与推理（PyTorch Model Persistence and Inference）]]
- [[01-PyTorch 张量基础（PyTorch Tensor Fundamentals）]]
- [[02-PyTorch 自动微分与神经网络组件（PyTorch Autograd and Neural Network Components）]]
- [[03-PyTorch 线性回归实战（PyTorch Linear Regression）]]
- [[04-PyTorch 全连接网络与手机价格分类实践（PyTorch MLP and Phone-price Classification）]]
- [[05-远程 GPU 服务器与 Linux 基础（Remote GPU Server and Linux Basics）]]
- [[01-神经网络参数初始化与梯度流（Neural Network Initialization and Gradient Flow）]]
- [[02-模型欠拟合、过拟合与泛化（Model Underfitting, Overfitting, and Generalization）]]
- [[03-批归一化与常见归一化方法（Batch Normalization and Common Normalization Methods）]]
- [[01-图像表示、预处理与 CNN 概览（Image Representation, Preprocessing, and CNN Overview）]]
- [[02-二维卷积、感受野与 Conv2d（2D Convolution, Receptive Field, and Conv2d）]]
- [[03-池化、尺寸变换与 CNN 网络结构（Pooling, Spatial Transformation, and CNN Architecture）]]
- [[01-CIFAR-10 图像分类实践（CIFAR-10 Image Classification Practice）]]
- [[01-LeNet-5 手写数字识别与早期 CNN（LeNet-5 and Early CNNs）]]
- [[02-AlexNet 与大规模 GPU 视觉训练（AlexNet and Large-scale GPU Vision Training）]]
- [[03-VGG 与小卷积核深层堆叠（VGG and Deep Stacks of Small Kernels）]]
- [[04-GoogLeNet 与 Inception 多尺度融合（GoogLeNet and Inception Multi-scale Fusion）]]
- [[05-ResNet 残差学习与快捷连接（ResNet Residual Learning and Shortcut Connections）]]
- [[06-DenseNet 密集连接与特征复用（DenseNet Dense Connectivity and Feature Reuse）]]
- [[07-SENet 通道注意力与特征重标定（SENet Channel Attention and Feature Recalibration）]]
- [[08-MobileNet 深度可分离卷积与端侧网络（MobileNet Depthwise Separable Convolution and Edge Networks）]]
- [[09-ShuffleNet 组卷积与通道重组（ShuffleNet Group Convolution and Channel Shuffle）]]
- [[01-目标检测任务、范式与系统流程（Object Detection Tasks, Paradigms, and Pipeline）]]
- [[02-目标检测评估指标：IoU、Precision、Recall、AP 与 mAP（Object Detection Metrics）]]
- [[03-候选区域与选择性搜索（Region Proposals and Selective Search）]]
- [[04-锚框、样本匹配与边界框回归（Anchors, Label Assignment, and Box Regression）]]
- [[05-非极大值抑制与 Soft-NMS（Non-Maximum Suppression and Soft-NMS）]]
- [[06-R-CNN 系列两阶段检测器演化（Evolution of Two-stage R-CNN Detectors）]]
- [[07-YOLOv1、YOLOv2 与 YOLOv3 演化（YOLOv1-v3 Evolution）]]
- [[08-YOLOv4 架构、训练策略与检测头（YOLOv4 Architecture and Training）]]
- [[09-YOLOv5 架构、训练与部署边界（YOLOv5 Architecture, Training, and Deployment）]]
- [[10-YOLOv8 网络结构、标签分配与损失（YOLOv8 Architecture and Losses）]]
- [[01-目标检测关联视觉模块：FCN、实例分割、RoIAlign 与 FPN（Related Vision Modules）]]
- [[01-自然语言处理概览（NLP Overview）]]
- [[02-NLP 核心模型图解（NLP Core Model Visual Guide）]]
- [[01-循环神经网络、词嵌入与文本生成（RNN, Word Embedding, and Text Generation）]]
- [[02-文本向量表示与 Word2Vec（Text Vectorization and Word2Vec）]]
- [[03-Seq2Seq 与注意力机制（Seq2Seq and Attention）]]
- [[04-自注意力机制（Self-Attention）]]
- [[05-HMM 与 CRF 序列标注（HMM and CRF Sequence Labeling）]]
- [[01-Transformer 架构与注意力（Transformer Architecture and Attention）]]
- [[02-Transformer PyTorch 实现（Transformer PyTorch Implementation）]]
- [[03-FastText 文本分类与词向量（FastText Classification and Embeddings）]]
- [[04-NLP 迁移学习（NLP Transfer Learning）]]
- [[05-BERT 原理与模型族（BERT Principles and Family）]]
- [[06-ELMo 上下文词表示（ELMo Contextual Embeddings）]]
- [[07-GPT 模型演进（GPT Model Evolution）]]
- [[08-BERT、GPT 与 ELMo 对比（BERT, GPT, and ELMo Comparison）]]
- [[01-大语言模型术语、生命周期与工程生态（LLM Terminology and Lifecycle）]]
- [[01-LangChain 架构、环境与模型调用（Architecture, Setup, and Model I-O）]]
- [[02-输出解析、提示词与 LCEL 链（Output Parsing, Prompts, and LCEL Chains）]]
- [[03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）]]
- [[04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）]]
- [[05-LangChain Agent 与本地工具（Agents and Local Tools）]]
- [[06-MCP 工具集成（MCP Tool Integration）]]
- [[07-Agent 记忆与中间件（Agent Memory and Middleware）]]
- [[01-NLP 预处理与信息抽取（NLP Preprocessing and Information Extraction）]]
- [[02-Jieba 中文分词、词典、关键词与词性（Jieba Tokenization and Keywords）]]
- [[03-Gensim 词典、词袋与 TF-IDF（Gensim Dictionary, BoW, and TF-IDF）]]
- [[04-HanLP 本地推理与 RESTful 调用（HanLP Native and RESTful Usage）]]
- [[05-Hugging Face Transformers（Hugging Face Transformers）]]
- [[06-Hugging Face Tokenizer 与 Datasets 数据管线（Hugging Face Tokenizer and Datasets Pipeline）]]
- [[07-子词分词算法：BPE、WordPiece 与 Unigram（Subword Tokenization Algorithms）]]
- [[01-文本语料探索性分析（Exploratory Text Corpus Analysis）]]
- [[02-N-Gram、长度规范与文本数据增强（N-Gram and Text Augmentation）]]
- [[03-NLP 标准数据集与任务基准（NLP Datasets and Benchmarks）]]
- [[01-新闻主题分类实践（News Topic Classification Practice）]]
- [[02-RNN 人名语言分类器（RNN Name Language Classifier）]]
- [[03-注意力 Seq2Seq 机器翻译（Attention Seq2Seq Translation）]]
- [[04-Transformer 机器翻译（Transformer Machine Translation）]]
- [[05-Transformer 语言模型（Transformer Language Model）]]
- [[06-预训练模型迁移学习实践（Pretrained Model Transfer Learning Practice）]]
- [[07-电商评论情感分类演进（E-commerce Review Sentiment Classification Evolution）]]
- [[01-FastAPI 核心开发参考（FastAPI Core Development Reference）]]
- [[01-基于 NumPy 的三层 BP 神经网络（Three-layer BP Neural Network with NumPy）]]
- [[01-智能闸杆系统架构与项目模板（SmartGate Architecture and Project Template）]]
- [[01-YOLOv8 自定义目标检测项目模板（YOLOv8 Custom Detection Project Template）]]
- [[02-FastAPI 机器学习推理服务模板（FastAPI ML Inference Service Template）]]
- [[03-Flask 机器学习推理服务模板（Flask ML Inference Service Template）]]
- [[01-OpenCV Python 工具箱（OpenCV Python Toolbox）]]
- [[02-OpenCV 图像处理原理（OpenCV Image Processing Principles）]]
- [[01-Pillow 与 Torchvision 图像变换（Pillow and Torchvision Image Transforms）]]
## 官方参考（Official References）
- [scikit-learn 用户指南](https://scikit-learn.org/stable/user_guide)
