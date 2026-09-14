---
title: "Matplotlib 与 Seaborn 速查表（Matplotlib and Seaborn Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - visualization
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "Matplotlib 3.8+；Seaborn 0.13+"
---
# Matplotlib 与 Seaborn 速查表（Matplotlib and Seaborn Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
安装：`python -m pip install matplotlib seaborn`。优先面向对象接口 `fig, ax = plt.subplots()`；Seaborn 用语义映射快速建立统计图。
### Matplotlib（Matplotlib）
- **安装包（Distribution）**：`matplotlib`。
- **导入模块（Import Module）**：`matplotlib`，常用 `matplotlib.pyplot as plt`。
- **安装命令（Installation）**：`python -m pip install -U matplotlib`。
- **用途（Purpose）**：底层绘图、坐标轴精细控制、导出静态图。
- **正式笔记（Detailed Note）**：[[03-Matplotlib 数据可视化（Matplotlib Data Visualization）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建画布|`plt.subplots()`|返回 Figure 与 Axes|
|折线图|`ax.plot(x, y, label=...)`|向 Axes 添加 Line2D 并返回列表|
|保存|`fig.savefig(path, dpi=300)`|写图像文件|
|关闭|`plt.close(fig)`|释放图形资源|

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
lines = ax.plot([0, 1], [1, 2])
print(len(lines))  # 输出: 1
plt.close(fig)
```
### Seaborn（Seaborn）
- **安装包（Distribution）**：`seaborn`。
- **导入模块（Import Module）**：`seaborn`，惯例别名为 `sns`。
- **安装命令（Installation）**：`python -m pip install -U seaborn`。
- **用途（Purpose）**：基于 DataFrame 的统计可视化与语义映射。
- **正式笔记（Detailed Note）**：[[03-Matplotlib 数据可视化（Matplotlib Data Visualization）]] 中的统计绘图对照。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|折线图|`sns.lineplot(data=df, x=..., y=..., hue=...)`|向当前/指定 Axes 添加统计折线|
|散点图|`sns.scatterplot(data=df, x=..., y=..., hue=...)`|返回 Axes|
|分布图|`sns.histplot(data=df, x=..., bins='auto')`|返回 Axes|
|主题|`sns.set_theme(context='notebook', style='whitegrid')`|修改进程级绘图默认样式|

```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots()
sns.lineplot(x=[0, 1], y=[0, 1], ax=ax)
print(len(ax.lines))  # 输出: 1
plt.close(fig)
```
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 画布、坐标轴与布局（Figure, Axes, and Layout）
Figure 是整张图，Axes 是一个绘图区。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建单图|`fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')`|返回 Figure 与 Axes|
|创建网格|`fig, axes = plt.subplots(r, c, sharex=False, sharey=False)`|返回 Figure 与 Axes 数组|
|添加标题|`ax.set_title(title)`|返回 Text|
|轴标签|`ax.set(xlabel='x', ylabel='y')`|返回属性对象列表|
|坐标范围|`ax.set_xlim(left, right) / ax.set_ylim(bottom, top)`|返回边界元组|
|网格|`ax.grid(True, alpha=.3)`|原地修改 Axes|
|图例|`ax.legend(loc='best')`|返回 Legend|
|紧凑布局|`fig.tight_layout()`|调整子图位置，返回 None|
|保存|`fig.savefig(path, dpi=300, bbox_inches='tight')`|写图像文件|
|关闭|`plt.close(fig)`|释放图形资源，返回 None|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
line, = ax.plot([0, 1, 2], [0, 1, 4], label="y=x²")
ax.set(xlabel="x", ylabel="y", title="Curve")
ax.legend()
print(type(line).__name__, len(ax.lines))
plt.close(fig)
# 期望输出:
# Line2D 1
```
## 基础图形（Core Plots）
选择图形应匹配任务：趋势、关系、分布或组成。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|折线图|`ax.plot(x, y, marker=None, label=None)`|返回 Line2D 列表|
|散点图|`ax.scatter(x, y, c=None, s=None, alpha=None)`|返回 PathCollection|
|柱状图|`ax.bar(x, height, width=.8)`|返回 BarContainer|
|水平柱图|`ax.barh(y, width)`|返回 BarContainer|
|直方图|`ax.hist(x, bins=10, density=False)`|返回计数、边界、Patch|
|箱线图|`ax.boxplot(data, showfliers=True)`|返回艺术家字典|
|面积填充|`ax.fill_between(x, y1, y2=0, alpha=None)`|返回 PolyCollection|
|误差棒|`ax.errorbar(x, y, yerr=None, xerr=None)`|返回 ErrorbarContainer|
|热图底层|`ax.imshow(matrix, cmap=None, aspect=None)`|返回 AxesImage|
|等高线|`ax.contour(X, Y, Z, levels=None)`|返回 ContourSet|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
bars = ax.bar(["A", "B"], [3, 5])
print(len(bars), bars[1].get_height())
plt.close(fig)
# 期望输出:
# 2 5
```
## 刻度、注释与颜色（Ticks, Annotation, and Color）
可读性来自单位、尺度、颜色含义和重点标注。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|刻度位置|`ax.set_xticks(positions, labels=None)`|返回 Tick 列表|
|刻度格式|`ax.xaxis.set_major_formatter(formatter)`|原地设置格式器|
|旋转标签|`ax.tick_params(axis='x', labelrotation=45)`|原地设置|
|文本|`ax.text(x, y, text, transform=None)`|返回 Text|
|箭头注释|`ax.annotate(text, xy, xytext=None, arrowprops=None)`|返回 Annotation|
|参考线|`ax.axhline(y, color='k', linestyle='--')`|返回 Line2D|
|色图|`plt.get_cmap(name)`|返回 Colormap|
|颜色归一|`matplotlib.colors.Normalize(vmin, vmax)`|返回归一化器|
|颜色条|`fig.colorbar(mappable, ax=ax)`|返回 Colorbar|
|对数坐标|`ax.set_yscale('log')`|修改坐标变换|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1,2,3], [10,100,1000])
ax.set_yscale("log")
ax.annotate("peak", xy=(3,1000))
print(ax.get_yscale())
plt.close(fig)
# 期望输出:
# log
```
## Seaborn 统计图（Seaborn Statistical Plots）
Seaborn 接受长表并通过 `hue/style/size` 映射语义。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|关系图|`sns.scatterplot(data=df, x='x', y='y', hue='group')`|返回 Axes|
|折线统计|`sns.lineplot(data=df, x='time', y='value', estimator='mean')`|返回 Axes|
|分布直方|`sns.histplot(data=df, x='x', bins='auto', kde=False)`|返回 Axes|
|核密度|`sns.kdeplot(data=df, x='x', hue='group')`|返回 Axes|
|箱线图|`sns.boxplot(data=df, x='group', y='value')`|返回 Axes|
|小提琴图|`sns.violinplot(...)`|返回 Axes|
|分类点图|`sns.pointplot(...)`|返回 Axes|
|热图|`sns.heatmap(matrix, annot=False, cmap=None)`|返回 Axes|
|成对关系|`sns.pairplot(data=df, hue=None)`|返回 PairGrid|
|分面关系|`sns.relplot(data=df, col='group', kind='scatter')`|返回 FacetGrid|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
df = pd.DataFrame({"x": [1,2,1,2], "y": [2,4,3,5], "g": ["A","A","B","B"]})
ax = sns.scatterplot(data=df, x="x", y="y", hue="g")
print(len(ax.collections) >= 1)
plt.close(ax.figure)
# 期望输出:
# True
```
## 时间序列、图像与输出质量（Specialized Plots and Export）
输出前检查尺寸、字体、颜色无障碍和矢量/位图格式。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|日期定位器|`matplotlib.dates.AutoDateLocator()`|返回自动日期刻度定位器|
|日期格式器|`matplotlib.dates.ConciseDateFormatter(locator)`|返回紧凑格式器|
|双轴|`ax2 = ax.twinx()`|返回共享 x 轴的新 Axes|
|次坐标轴|`ax.secondary_xaxis(location, functions=(f, inv))`|返回 SecondaryAxis|
|图像插值|`ax.imshow(image, interpolation='nearest')`|返回 AxesImage|
|遮罩无效值|`np.ma.masked_invalid(data)`|返回 MaskedArray|
|统一风格|`sns.set_theme(style='whitegrid', context='notebook')`|修改全局主题|
|调色板|`sns.color_palette(name, n_colors)`|返回颜色列表|
|SVG 输出|`fig.savefig('plot.svg')`|写矢量文件|
|透明背景|`fig.savefig(path, transparent=True)`|写透明背景图|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
print(tuple(round(x, 1) for x in fig.get_size_inches()))
plt.close(fig)
# 期望输出:
# (4.0, 3.0)
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
- [[03-Matplotlib 数据可视化（Matplotlib Data Visualization）]]
## 官方参考（Official References）
- [Matplotlib Axes 指南](https://matplotlib.org/stable/users/explain/axes/index.html)
