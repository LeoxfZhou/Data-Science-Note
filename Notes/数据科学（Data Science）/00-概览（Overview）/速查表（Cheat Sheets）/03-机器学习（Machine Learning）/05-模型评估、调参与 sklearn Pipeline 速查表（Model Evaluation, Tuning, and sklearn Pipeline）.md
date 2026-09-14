---
title: "模型评估、调参与 sklearn Pipeline 速查表（Model Evaluation, Tuning, and sklearn Pipeline Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - machine-learning
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "scikit-learn 1.5–1.9；以当前稳定版官方文档为准"
---
# 模型评估、调参与 sklearn Pipeline 速查表（Model Evaluation, Tuning, and sklearn Pipeline Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
安装：`python -m pip install scikit-learn`；常用导入：`import sklearn`。训练集拟合一切有状态变换，验证/测试集只调用 `transform`/`predict`。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 分类评估（Classification Evaluation）
指标必须匹配类别不平衡、错误成本、阈值和是否需要概率。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|准确率|`accuracy_score(y, pred)`|返回正确比例|
|精确率|`precision_score(y, pred, average=...)`|返回预测正例中正确比例|
|召回率|`recall_score(y, pred, average=...)`|返回真实正例中找回比例|
|F1|`f1_score(y, pred, average=...)`|返回精确率与召回率调和均值|
|混淆矩阵|`confusion_matrix(y, pred, labels=None)`|返回计数矩阵|
|分类报告|`classification_report(y, pred, output_dict=False)`|返回文本或字典|
|ROC-AUC|`roc_auc_score(y, score)`|返回阈值无关排序分数|
|PR-AUC|`average_precision_score(y, score)`|返回平均精确率|
|对数损失|`log_loss(y, prob)`|返回概率交叉熵，越小越好|
|平衡准确率|`balanced_accuracy_score(y, pred)`|返回各类召回率平均|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.metrics import confusion_matrix, f1_score
y=[0,0,1,1]; p=[0,1,1,1]
print(confusion_matrix(y,p).tolist())
print(round(f1_score(y,p),3))
# 期望输出:
# [[1, 1], [0, 2]]
# 0.8
```
## 回归评估与残差（Regression Evaluation）
同时观察绝对误差、平方误差、相对误差和残差分布。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|MAE|`mean_absolute_error(y, pred)`|返回平均绝对误差|
|MSE|`mean_squared_error(y, pred)`|返回平均平方误差|
|RMSE|`root_mean_squared_error(y, pred)`|返回均方根误差|
|R²|`r2_score(y, pred)`|返回相对均值基线解释度，可为负|
|中位绝对误差|`median_absolute_error(y, pred)`|返回鲁棒误差|
|MAPE|`mean_absolute_percentage_error(y, pred)`|返回比例；真实值近零会失控|
|最大误差|`max_error(y, pred)`|返回最大绝对残差|
|残差|`residual = y - pred`|返回逐样本误差|
|评分器|`make_scorer(metric, greater_is_better=False)`|返回 sklearn scorer|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
y=[1,2,3]; p=[1,2,4]
print(round(mean_absolute_error(y,p),3))
print(round(root_mean_squared_error(y,p),3))
print(round(r2_score(y,p),3))
# 期望输出:
# 0.333
# 0.577
# 0.5
```
## Pipeline 与列变换（Pipeline and ColumnTransformer）
Pipeline 把预处理和模型绑定，防止交叉验证泄漏。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|顺序流水线|`Pipeline([('prep', prep), ('model', model)])`|返回复合估计器|
|简写|`make_pipeline(step1, step2)`|自动命名步骤|
|列变换|`ColumnTransformer([...], remainder='drop')`|并行变换列并拼接|
|拟合|`pipeline.fit(X, y)`|依次 fit/transform，末步 fit|
|预测|`pipeline.predict(X)`|依次 transform，末步 predict|
|访问步骤|`pipeline.named_steps['model']`|返回命名估计器|
|嵌套参数|`pipeline.set_params(model__C=1.0)`|修改子步骤参数|
|缓存|`Pipeline(..., memory=cache_dir)`|缓存可复用变换|
|特征名|`pipeline[:-1].get_feature_names_out()`|返回转换后列名（步骤支持时）|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
X=[[1],[None],[3],[4]]; y=[0,0,1,1]
p=make_pipeline(SimpleImputer(strategy="median"), LogisticRegression()).fit(X,y)
print(p.predict([[None],[5]]).tolist())
# 期望输出:
# [1, 1]
```
## 交叉验证与搜索（Cross-validation and Search）
调参结果必须报告搜索空间、CV 策略和独立测试集表现。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|交叉验证分数|`cross_val_score(model, X, y, cv=5, scoring=None)`|返回每折分数数组|
|多指标验证|`cross_validate(..., scoring={'f1':'f1','auc':'roc_auc'})`|返回分数/时间字典|
|网格搜索|`GridSearchCV(model, param_grid, cv=5, scoring=...)`|穷举参数组合并拟合|
|随机搜索|`RandomizedSearchCV(model, distributions, n_iter=20)`|随机采样组合|
|连续减半|`HalvingGridSearchCV(...)`|实验性逐轮淘汰配置|
|最佳模型|`search.best_estimator_`|返回重新拟合后的最佳估计器|
|最佳参数|`search.best_params_`|返回参数字典|
|搜索结果|`pd.DataFrame(search.cv_results_)`|返回每配置完整结果表|
|嵌套 CV|`外层评估 + 内层搜索`|返回更少偏差的泛化估计|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
X,y=load_iris(return_X_y=True)
s=GridSearchCV(LogisticRegression(max_iter=300), {"C":[.1,1.]}, cv=3).fit(X,y)
print(s.best_params_["C"] in [.1,1.], len(s.cv_results_["params"]))
# 期望输出:
# True 2
```
## 阈值、校准与可复现（Thresholds, Calibration, and Reproducibility）
模型排序、概率校准和最终决策是三个不同层次。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|ROC 曲线|`roc_curve(y, score)`|返回 FPR、TPR、阈值|
|PR 曲线|`precision_recall_curve(y, score)`|返回精确率、召回率、阈值|
|固定阈值|`pred = (prob >= threshold)`|返回布尔预测|
|阈值调优|`TunedThresholdClassifierCV(estimator, scoring=...)`|用 CV 选择决策阈值|
|概率校准|`CalibratedClassifierCV(estimator, method='sigmoid')`|返回校准分类器|
|校准曲线|`calibration_curve(y, prob, n_bins=10)`|返回各箱真实率和均值概率|
|随机种子|`random_state=42`|控制估计器和拆分随机性|
|配置快照|`model.get_params(deep=True)`|返回完整参数字典|
|版本记录|`sklearn.show_versions()`|打印依赖与系统版本|
|数据指纹|`对 schema、行数、哈希做记录`|返回可复现追踪信息|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import numpy as np
from sklearn.metrics import precision_score, recall_score
y=np.array([0,0,1,1]); prob=np.array([.1,.6,.7,.9])
for t in [.5,.8]:
    p=prob>=t
    print(t, round(precision_score(y,p),2), round(recall_score(y,p),2))
# 期望输出:
# 0.5 0.67 1.0
# 0.8 1.0 0.5
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
- [[02-FastAPI 机器学习推理服务模板（FastAPI ML Inference Service Template）]]
- [[03-Flask 机器学习推理服务模板（Flask ML Inference Service Template）]]
## 官方参考（Official References）
- [scikit-learn 用户指南](https://scikit-learn.org/stable/user_guide)
