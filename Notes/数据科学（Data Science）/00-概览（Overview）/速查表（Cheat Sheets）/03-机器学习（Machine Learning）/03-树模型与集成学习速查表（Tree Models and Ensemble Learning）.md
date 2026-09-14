---
title: "树模型与集成学习速查表（Tree Models and Ensemble Learning Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - machine-learning
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "scikit-learn 1.5–1.9；以当前稳定版官方文档为准"
---
# 树模型与集成学习速查表（Tree Models and Ensemble Learning Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
安装：`python -m pip install scikit-learn`；常用导入：`import sklearn`。训练集拟合一切有状态变换，验证/测试集只调用 `transform`/`predict`。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 决策树（Decision Trees）
树递归选择切分降低不纯度；大白话：不断问“哪个条件最能把答案分开”。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|分类树|`DecisionTreeClassifier(criterion='gini', max_depth=None)`|返回分类树|
|回归树|`DecisionTreeRegressor(criterion='squared_error')`|返回回归树|
|限制深度|`max_depth=n`|降低复杂度和过拟合|
|叶节点下限|`min_samples_leaf=n_or_fraction`|限制每个叶子样本数|
|分裂下限|`min_samples_split=n_or_fraction`|限制内部节点分裂|
|特征子采样|`max_features=None`|控制每次候选特征|
|代价复杂度剪枝|`ccp_alpha=0.0`|增大可剪去弱分支|
|特征重要性|`model.feature_importances_`|返回不纯度下降重要性|
|树结构导出|`export_text(model, feature_names=...)`|返回文本规则|
|决策路径|`model.decision_path(X)`|返回稀疏节点指示矩阵|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.tree import DecisionTreeClassifier, export_text
X = [[0],[1],[2],[3]]; y=[0,0,1,1]
m=DecisionTreeClassifier(max_depth=1, random_state=0).fit(X,y)
print(m.predict([[.5],[2.5]]).tolist())
print(m.get_depth(), m.get_n_leaves())
# 期望输出:
# [0, 1]
# 1 2
```
## Bagging 与随机森林（Bagging and Random Forests）
Bootstrap 样本和随机特征让多棵树降低相关性，再平均降低方差。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|Bagging|`BaggingClassifier(estimator=None, n_estimators=10)`|返回并行基学习器集成|
|随机森林分类|`RandomForestClassifier(n_estimators=100)`|返回树集成|
|随机森林回归|`RandomForestRegressor(n_estimators=100)`|返回连续预测集成|
|极端随机树|`ExtraTreesClassifier(n_estimators=100)`|使用更随机切分|
|袋外评分|`oob_score=True`|训练后提供 oob_score_，需 bootstrap|
|并行|`n_jobs=-1`|使用全部可用 CPU|
|类别权重|`class_weight='balanced'`|按类别频率调整样本权重|
|投票分类|`VotingClassifier(estimators, voting='soft')`|组合多种模型概率|
|投票回归|`VotingRegressor(estimators)`|平均多个回归输出|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.ensemble import RandomForestClassifier
X=[[0],[1],[2],[3]]; y=[0,0,1,1]
m=RandomForestClassifier(n_estimators=20, random_state=0).fit(X,y)
print(m.predict([[.2],[2.8]]).tolist())
# 期望输出:
# [0, 1]
```
## Boosting（Boosting Models）
串行加入弱学习器修正当前残差；大白话：后面的模型专门补前面做错的题。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|AdaBoost|`AdaBoostClassifier(n_estimators=50, learning_rate=1.0)`|返回加权弱学习器|
|梯度提升分类|`GradientBoostingClassifier(n_estimators=100, learning_rate=.1)`|返回阶段加法模型|
|梯度提升回归|`GradientBoostingRegressor(loss='squared_error')`|返回回归集成|
|直方图提升|`HistGradientBoostingClassifier(max_iter=100)`|高效分箱并原生支持缺失值|
|学习率|`learning_rate=.1`|缩小每棵树贡献，通常需更多树|
|早停|`early_stopping='auto'`|根据验证分数停止（模型支持时）|
|阶段预测|`model.staged_predict(X)`|返回每阶段预测迭代器|
|训练分数|`model.train_score_`|返回各阶段训练损失（部分模型）|
|XGBoost|`xgboost.XGBClassifier(...)`|第三方高性能梯度提升|
|LightGBM|`lightgbm.LGBMClassifier(...)`|第三方叶优先生长提升|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.ensemble import HistGradientBoostingClassifier
X=[[0],[1],[2],[3],[4],[5]]; y=[0,0,0,1,1,1]
m=HistGradientBoostingClassifier(max_iter=20, random_state=0).fit(X,y)
print(m.predict([[0],[5]]).tolist())
# 期望输出:
# [0, 0]
```
## 解释、验证与持久化（Interpretation, Validation, and Persistence）
内建重要性偏向高基数连续特征，优先用独立验证集上的排列重要性。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|交叉验证|`cross_validate(model, X, y, cv=5, return_train_score=True)`|返回分数与耗时字典|
|排列重要性|`permutation_importance(model, X_val, y_val, n_repeats=10)`|返回均值/标准差|
|部分依赖|`PartialDependenceDisplay.from_estimator(model, X, features)`|返回显示对象|
|个体条件期望|`kind='individual'`|绘制样本级响应曲线|
|叶索引|`model.apply(X)`|返回每棵树的叶节点索引|
|概率|`model.predict_proba(X)`|返回类别概率矩阵|
|序列化|`joblib.dump(model, path)`|写模型文件；只加载可信文件|
|加载|`joblib.load(path)`|返回对象；不可信内容可执行代码|
|随机控制|`random_state=42`|固定随机采样与切分|
|温启动|`warm_start=True`|保留已训练估计器以追加树（参数约束需一致）|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
X=[[0,0],[0,1],[1,0],[1,1]]; y=[0,0,1,1]
m=RandomForestClassifier(n_estimators=30, random_state=0).fit(X,y)
r=permutation_importance(m,X,y,n_repeats=3,random_state=0)
print((r.importances_mean[0] >= r.importances_mean[1]))
# 期望输出:
# True
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
