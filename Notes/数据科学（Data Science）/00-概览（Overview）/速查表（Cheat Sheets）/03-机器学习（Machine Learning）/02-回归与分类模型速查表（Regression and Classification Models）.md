---
title: "回归与分类模型速查表（Regression and Classification Models Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - machine-learning
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "scikit-learn 1.5–1.9；以当前稳定版官方文档为准"
---
# 回归与分类模型速查表（Regression and Classification Models Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
安装：`python -m pip install scikit-learn`；常用导入：`import sklearn`。训练集拟合一切有状态变换，验证/测试集只调用 `transform`/`predict`。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 线性回归与正则化（Linear Regression and Regularization）
线性模型可解释、训练快；正则化控制方差和共线性。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|普通最小二乘|`LinearRegression(fit_intercept=True)`|拟合后提供 coef_、intercept_|
|岭回归|`Ridge(alpha=1.0)`|L2 正则，返回回归器|
|套索|`Lasso(alpha=1.0)`|L1 正则可产生稀疏系数|
|弹性网|`ElasticNet(alpha=1.0, l1_ratio=.5)`|混合 L1/L2|
|鲁棒回归|`HuberRegressor(epsilon=1.35)`|降低离群点影响|
|随机梯度回归|`SGDRegressor(loss='squared_error')`|支持大规模与 partial_fit|
|拟合|`model.fit(X, y)`|返回 self 并写入参数|
|预测|`model.predict(X)`|返回连续预测数组|
|评分|`model.score(X, y)`|回归默认返回 R²|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import numpy as np
from sklearn.linear_model import Ridge
X = np.array([[0.],[1.],[2.]]); y = np.array([1.,3.,5.])
m = Ridge(alpha=0).fit(X,y)
print(np.round(m.coef_,2).tolist(), round(float(m.predict([[3]])[0]),2))
# 期望输出:
# [2.0] 7.0
```
## 线性分类与概率（Linear Classification and Probabilities）
分类阈值应由业务成本和验证集选择，不默认固定 0.5。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|逻辑回归|`LogisticRegression(C=1.0, max_iter=100)`|返回概率线性分类器|
|线性 SVM|`LinearSVC(C=1.0)`|返回最大间隔分类器，默认无 predict_proba|
|核 SVM|`SVC(C=1.0, kernel='rbf', probability=False)`|返回核分类器|
|SGD 分类|`SGDClassifier(loss='log_loss')`|支持在线学习|
|朴素贝叶斯|`GaussianNB() / MultinomialNB()`|返回生成式分类器|
|最近邻|`KNeighborsClassifier(n_neighbors=5)`|基于邻居投票|
|类别预测|`model.predict(X)`|返回标签数组|
|概率预测|`model.predict_proba(X)`|返回每类概率矩阵（模型支持时）|
|决策分数|`model.decision_function(X)`|返回未校准分数|
|概率校准|`CalibratedClassifierCV(estimator, method='sigmoid')`|返回校准模型|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.linear_model import LogisticRegression
X = [[0],[1],[2],[3]]; y = [0,0,1,1]
m = LogisticRegression().fit(X,y)
print(m.predict([[0],[3]]).tolist())
print(m.predict_proba([[3]]).shape)
# 期望输出:
# [0, 1]
# (1, 2)
```
## 模型假设与选型（Assumptions and Selection）
先用可解释基线，再按非线性、样本规模和稀疏性升级。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|线性关系|`LinearRegression / LogisticRegression`|系数描述控制其他特征后的线性贡献|
|高维稀疏文本|`LogisticRegression / LinearSVC`|可直接处理稀疏矩阵|
|非线性边界|`SVC(kernel='rbf')`|样本大时训练和预测成本较高|
|局部结构|`KNeighborsClassifier`|需缩放，对高维和大样本较慢|
|计数特征|`MultinomialNB`|要求非负特征|
|连续近高斯|`GaussianNB`|按类独立高斯假设|
|离群回归|`HuberRegressor`|对大残差转为线性惩罚|
|多分类|`multi-class 自动策略`|返回每个输入一个类别|
|多标签|`OneVsRestClassifier(base)`|每个标签独立二分类|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
X,y = load_iris(return_X_y=True)
m = LogisticRegression(max_iter=300).fit(X,y)
print(m.classes_.tolist(), round(m.score(X,y),2))
# 期望输出:
# [0, 1, 2] 0.97
```
## 诊断与解释（Diagnostics and Interpretation）
系数受量纲、共线性和编码方式影响；不要直接解释为因果。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|模型参数|`model.get_params(deep=True)`|返回参数字典|
|更新参数|`model.set_params(C=0.1)`|修改配置并返回 self，需重新 fit|
|线性系数|`model.coef_`|返回 (目标/类别, 特征) 数组|
|截距|`model.intercept_`|返回截距数组|
|支持向量|`svc.support_vectors_`|返回支持向量矩阵|
|训练迭代|`model.n_iter_`|返回迭代次数信息|
|收敛警告|`ConvergenceWarning`|提示增加迭代、缩放或调整优化|
|排列重要性|`permutation_importance(model, X, y)`|返回打乱特征后的分数下降|
|部分依赖|`PartialDependenceDisplay.from_estimator(...)`|返回可视化对象|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.linear_model import LogisticRegression
m = LogisticRegression(C=.5, max_iter=200)
params = m.get_params()
print(params["C"], params["max_iter"])
# 期望输出:
# 0.5 200
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
- [[01-机器学习概览（Machine Learning Overview）]]
- [[01-集成学习方法（Ensemble Learning Methods）]]
- [[03-PyTorch 线性回归实战（PyTorch Linear Regression）]]
- [[04-PyTorch 全连接网络与手机价格分类实践（PyTorch MLP and Phone-price Classification）]]
- [[01-CIFAR-10 图像分类实践（CIFAR-10 Image Classification Practice）]]
- [[04-锚框、样本匹配与边界框回归（Anchors, Label Assignment, and Box Regression）]]
- [[03-FastText 文本分类与词向量（FastText Classification and Embeddings）]]
- [[01-新闻主题分类实践（News Topic Classification Practice）]]
- [[02-RNN 人名语言分类器（RNN Name Language Classifier）]]
- [[07-电商评论情感分类演进（E-commerce Review Sentiment Classification Evolution）]]
- [[02-FastAPI 机器学习推理服务模板（FastAPI ML Inference Service Template）]]
- [[03-Flask 机器学习推理服务模板（Flask ML Inference Service Template）]]
## 官方参考（Official References）
- [scikit-learn 用户指南](https://scikit-learn.org/stable/user_guide)
