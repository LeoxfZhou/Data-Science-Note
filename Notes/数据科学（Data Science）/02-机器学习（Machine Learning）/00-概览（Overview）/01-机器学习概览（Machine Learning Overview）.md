---
title: 机器学习概览（Machine Learning Overview）
status: published
published_at: 2026-08-11
---

# 机器学习概览（Machine Learning Overview）
## 1. 定义与定位（Definition and Positioning）
- 机器学习（Machine Learning, ML）研究如何让算法从数据中识别规律，并利用学到的规律完成预测、分类、排序、聚类或决策，而不是由开发者为每种输入手写全部规则。
- 深度学习（Deep Learning, DL）是机器学习的重要分支，通常使用多层人工神经网络（Artificial Neural Network）自动学习分层特征。
- 数据科学（Data Science）范围更广，除机器学习外还包括数据采集、清洗、探索、统计推断、可视化、实验设计、部署和业务解释。建议结合 [[数据科学（Data Science）]] 中的完整学习路径理解本笔记的位置。

## 2. 人工智能三要素（Three Elements of Artificial Intelligence）
原稿将人工智能（Artificial Intelligence, AI）的关键条件概括为：
1. **数据（Data）**：为模型提供可学习的样本、标签或交互反馈。数据的代表性、覆盖范围、标注质量和泄漏风险会直接影响模型上限。
2. **算力（Computing Power）**：支持特征处理、参数优化、超参数搜索和大规模推理。算力增加不能弥补错误标签、错误目标或不合理评估。
3. **算法（Algorithm）**：规定模型表示能力、学习目标和优化方式。算法必须与任务类型、数据规模、延迟、内存和可解释性要求匹配。

## 3. 学习前置基础（Prerequisites）
### 3.1 数学基础（Mathematical Foundations）
- **高等数学（Calculus）**：函数、极限、导数、偏导数、梯度和积分；其中梯度是理解损失函数优化的核心。
- **线性代数（Linear Algebra）**：向量、矩阵、张量、线性变换、特征值和矩阵分解；模型输入、参数和批量计算通常以这些结构表达。
- **概率论与数理统计（Probability and Mathematical Statistics）**：随机变量、分布、期望、方差、条件概率、最大似然估计、置信区间和假设检验；用于表达不确定性、定义模型和评估结论可靠性。

### 3.2 Python 与数据工具（Python and Data Tools）
- 掌握 Python 基础语法、函数、类、异常和模块管理。
- 使用 NumPy 完成数组与向量化计算，可参考 [[07-NumPy 数值计算（NumPy）]]。
- 使用 Pandas 完成表格数据的读取、清洗、转换和聚合，可参考 [[08-Pandas 数据处理（Pandas）]]。
- 能够区分训练集（Training Set）、验证集（Validation Set）和测试集（Test Set），并避免在预处理、特征选择或调参中发生数据泄漏（Data Leakage）。

## 4. 典型任务类型（Common Task Types）
- **监督学习（Supervised Learning）**：从带标签样本中学习输入到目标的映射。
  - 分类（Classification）：目标是离散类别，例如垃圾邮件识别。
  - 回归（Regression）：目标是连续数值，例如房价预测。
- **无监督学习（Unsupervised Learning）**：数据没有明确标签，常用于聚类（Clustering）、降维（Dimensionality Reduction）和异常检测（Anomaly Detection）。
- **半监督学习（Semi-supervised Learning）**：同时利用少量有标签数据和大量无标签数据。
- **强化学习（Reinforcement Learning）**：智能体（Agent）通过与环境交互，根据奖励（Reward）学习策略（Policy）。

## 5. 基本实验流程（Basic Experimental Workflow）
1. 明确业务问题、预测目标、约束和成功指标。
2. 获取并检查数据，确认样本单位、标签来源、时间范围和潜在偏差。
3. 划分训练集、验证集和测试集；任何根据数据学习得到的预处理参数都只能在训练集上拟合。
4. 建立简单基线（Baseline），再逐步增加特征或模型复杂度。
5. 训练模型并使用验证集选择超参数（Hyperparameter）。
6. 在测试集上进行一次最终评估，并同时报告适合任务的指标、误差分布和失败案例。
7. 部署后监控数据漂移（Data Drift）、概念漂移（Concept Drift）、延迟、资源消耗和业务影响。

## 6. 学习与数据资源（Learning and Dataset Resources）
- 吴恩达机器学习笔记：[在线笔记](http://www.ai-start.com/ml2014)。
- UCI 机器学习数据集仓库（UCI Machine Learning Repository）：[http://archive.ics.uci.edu/](http://archive.ics.uci.edu/)。
- Kaggle 竞赛与数据集：[https://www.kaggle.com/competitions](https://www.kaggle.com/competitions)。
- 阿里云天池（Tianchi）实验室：[https://tianchi.aliyun.com/datalab/index.htm](https://tianchi.aliyun.com/datalab/index.htm)。

> [!warning] 数据使用边界（Data Usage Boundary）
> 使用公开数据集前仍需检查许可证（License）、隐私要求、用途限制、数据更新时间和评价协议。竞赛测试集的榜单成绩不能替代面向真实业务分布的独立验证。

## 7. 与后续笔记的关系（Relationship to Subsequent Notes）
- 多模型组合方法见 [[01-集成学习方法（Ensemble Learning Methods）]]。
- 多层神经网络、自动特征学习和典型深度模型见 [[01-深度学习概览（Deep Learning Overview）]]。
- 本笔记只建立机器学习总览；具体模型的数学推导、API、调参和工程实现应放入对应专题笔记。
