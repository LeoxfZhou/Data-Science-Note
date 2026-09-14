---
title: "聚类与降维速查表（Clustering and Dimensionality Reduction Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - machine-learning
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "scikit-learn 1.5–1.9；以当前稳定版官方文档为准"
---
# 聚类与降维速查表（Clustering and Dimensionality Reduction Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
安装：`python -m pip install scikit-learn`；常用导入：`import sklearn`。训练集拟合一切有状态变换，验证/测试集只调用 `transform`/`predict`。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 聚类前处理与 K-Means（Preprocessing and K-Means）
距离算法通常需要缩放；K-Means 假设近似球状、方差相近的簇。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|标准化|`StandardScaler()`|返回缩放特征|
|K-Means|`KMeans(n_clusters=8, init='k-means++', n_init='auto')`|返回质心聚类器|
|小批量 K-Means|`MiniBatchKMeans(n_clusters=8, batch_size=1024)`|适合大样本和 partial_fit|
|训练并标记|`model.fit_predict(X)`|返回每行簇标签|
|新样本标记|`model.predict(X_new)`|返回最近质心标签|
|质心|`model.cluster_centers_`|返回 (k, features) 数组|
|惯性|`model.inertia_`|返回样本到最近中心平方距离和|
|轮廓系数|`silhouette_score(X, labels)`|返回 [-1,1] 分数；至少两个有效簇|
|肘部法|`比较不同 k 的 inertia_`|返回候选曲线，不是自动真值|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.cluster import KMeans
X=[[0,0],[0,1],[9,9],[9,8]]
m=KMeans(n_clusters=2,n_init=10,random_state=0).fit(X)
print(sorted(m.labels_.tolist()))
print(m.cluster_centers_.shape)
# 期望输出:
# [0, 0, 1, 1]
# (2, 2)
```
## 密度与层次聚类（Density and Hierarchical Clustering）
密度方法可发现非球形簇并标记噪声；参数受尺度强烈影响。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|DBSCAN|`DBSCAN(eps=.5, min_samples=5)`|无需预设簇数，噪声标签为 -1|
|OPTICS|`OPTICS(min_samples=5, max_eps=inf)`|返回多密度排序聚类|
|HDBSCAN|`HDBSCAN(min_cluster_size=5)`|返回层次密度聚类（版本可用性需核对）|
|凝聚聚类|`AgglomerativeClustering(n_clusters=2, linkage='ward')`|自底向上合并|
|距离阈值|`AgglomerativeClustering(n_clusters=None, distance_threshold=d)`|按阈值停止|
|均值漂移|`MeanShift(bandwidth=None)`|通过密度峰值发现簇|
|谱聚类|`SpectralClustering(n_clusters=8, affinity='rbf')`|图切分，适合复杂边界|
|簇标签|`model.labels_`|返回训练样本标签|
|核心样本|`dbscan.core_sample_indices_`|返回核心点索引|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.cluster import DBSCAN
X=[[0,0],[0,.1],[5,5],[20,20]]
labels=DBSCAN(eps=.3,min_samples=2).fit_predict(X)
print(labels.tolist())
# 期望输出:
# [0, 0, -1, -1]
```
## PCA 与矩阵分解（PCA and Matrix Factorization）
PCA 寻找最大方差正交方向；大白话：旋转坐标轴，用更少方向保留主要变化。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|PCA|`PCA(n_components=None, whiten=False)`|返回线性降维器|
|保留方差|`PCA(n_components=.95)`|选择达到累计方差比例的维数|
|增量 PCA|`IncrementalPCA(n_components=k, batch_size=None)`|支持分批训练|
|截断 SVD|`TruncatedSVD(n_components=k)`|支持稀疏矩阵，不先中心化|
|非负分解|`NMF(n_components=k, init='nndsvda')`|输入必须非负|
|拟合变换|`model.fit_transform(X)`|学习并返回低维表示|
|逆变换|`model.inverse_transform(Z)`|返回近似重构|
|解释方差|`pca.explained_variance_ratio_`|返回各主成分方差比例|
|主轴|`pca.components_`|返回 (components, features) 数组|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import numpy as np
from sklearn.decomposition import PCA
X=np.array([[1,0],[2,0],[3,0]],dtype=float)
p=PCA(n_components=1).fit(X)
print(p.transform(X).shape)
print(np.round(p.explained_variance_ratio_,2).tolist())
# 期望输出:
# (3, 1)
# [1.0]
```
## 流形学习与可视化（Manifold Learning and Visualization）
t-SNE/UMAP 图中的全局距离和簇间空白不能直接当成真实结构。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|t-SNE|`TSNE(n_components=2, perplexity=30, init='pca')`|返回可视化嵌入，无稳定 transform|
|Isomap|`Isomap(n_neighbors=5, n_components=2)`|返回保持测地距离嵌入|
|LLE|`LocallyLinearEmbedding(n_neighbors=5, n_components=2)`|返回局部线性嵌入|
|MDS|`MDS(n_components=2, normalized_stress='auto')`|返回保持成对距离嵌入|
|谱嵌入|`SpectralEmbedding(n_components=2)`|返回图拉普拉斯嵌入|
|UMAP|`umap.UMAP(n_neighbors=15, min_dist=.1)`|第三方快速流形嵌入|
|固定随机性|`random_state=42`|提高重复运行一致性|
|标准化输入|`StandardScaler().fit_transform(X)`|避免尺度支配距离|
|验证稳定性|`更换 seed/参数并比较邻域保持`|返回稳定性证据而非单张图|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from sklearn.manifold import MDS
X=[[0,0],[1,0],[0,1],[1,1]]
Z=MDS(n_components=2,random_state=0,n_init=1,max_iter=20).fit_transform(X)
print(Z.shape)
# 期望输出:
# (4, 2)
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
