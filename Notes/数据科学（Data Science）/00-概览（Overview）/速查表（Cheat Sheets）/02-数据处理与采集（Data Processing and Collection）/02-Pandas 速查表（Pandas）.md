---
title: "Pandas 速查表（Pandas Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - pandas
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "pandas 2.2–3.0；已按 3.0 用户指南核对"
---
# Pandas 速查表（Pandas Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
安装：`python -m pip install pandas`；导入：`import pandas as pd`。优先使用显式列名、可空 dtype 和链式无副作用转换。
- **安装包（Distribution）**：`pandas`。
- **导入模块（Import Module）**：`pandas`，惯例别名为 `pd`。
- **安装命令（Installation）**：`python -m pip install -U pandas`。
- **用途（Purpose）**：表格数据读取、清洗、连接、聚合、时间序列和导出。
- **正式笔记（Detailed Note）**：[[02-Pandas 数据处理（Pandas）]]。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 创建、读取与检查（Creation, I/O, and Inspection）
读入后立即检查 schema、行数、缺失值与重复键。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|构建表|`pd.DataFrame(data, columns=None)`|返回 DataFrame|
|CSV 读取|`pd.read_csv(path, usecols=None, dtype=None, parse_dates=None)`|返回 DataFrame；有文件 I/O|
|Parquet 读取|`pd.read_parquet(path, columns=None)`|返回 DataFrame；需 parquet 引擎|
|Excel 读取|`pd.read_excel(path, sheet_name=0)`|返回 DataFrame 或工作表字典|
|SQL 查询|`pd.read_sql(query, connection, params=None)`|返回 DataFrame；有数据库读取|
|查看头尾|`df.head(n=5) / df.tail(n=5)`|返回切片|
|结构摘要|`df.info()`|打印 dtype、非空计数与内存，返回 None|
|统计摘要|`df.describe(include=None)`|返回统计 DataFrame|
|类型查看|`df.dtypes`|返回 Series|
|维度|`df.shape`|返回 (行数, 列数) 元组|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import pandas as pd
df = pd.DataFrame({"x": [1, 2], "y": [3, None]})
print(df.shape)
print(df.isna().sum().to_dict())
# 期望输出:
# (2, 2)
# {'x': 0, 'y': 1}
```
## 选择、索引与赋值（Selection, Indexing, and Assignment）
优先 `.loc`/`.iloc`，避免链式赋值。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|选列|`df['col']`|返回 Series|
|选多列|`df[['a', 'b']]`|返回 DataFrame|
|标签选择|`df.loc[rows, columns]`|按标签返回标量、Series 或 DataFrame|
|位置选择|`df.iloc[rows, columns]`|按整数位置返回结果|
|条件筛选|`df.loc[df['score'].ge(60)]`|返回筛选后的 DataFrame|
|表达式查询|`df.query('score >= @threshold')`|返回 DataFrame|
|安全取列|`df.get('col', default)`|返回列或默认值|
|新增或覆盖列|`df.loc[:, 'new'] = values`|原地修改指定列|
|设置索引|`df.set_index(keys, drop=True)`|返回新 DataFrame|
|重置索引|`df.reset_index(drop=False)`|返回新 DataFrame|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import pandas as pd
df = pd.DataFrame({"name": ["A", "B"], "score": [80, 55]})
passed = df.loc[df["score"] >= 60, ["name", "score"]]
print(passed.to_dict("records"))
# 期望输出:
# [{'name': 'A', 'score': 80}]
```
## 清洗、类型与字符串（Cleaning, Types, and Strings）
缺失、空字符串、非法值与重复记录是不同问题。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|缺失判断|`df.isna()`|返回布尔 DataFrame|
|填充缺失|`df.fillna(value)`|返回新对象|
|删除缺失|`df.dropna(subset=None, how='any')`|返回删行/列后的对象|
|类型转换|`series.astype(dtype)`|返回新 Series；非法值抛出异常|
|宽容数值转换|`pd.to_numeric(series, errors='coerce')`|返回数值 Series，非法项为 NaN|
|日期转换|`pd.to_datetime(series, errors='coerce', utc=False)`|返回日期时间结果|
|字符串清理|`series.str.strip()`|返回字符串 Series|
|字符串匹配|`series.str.contains(pattern, na=False, regex=True)`|返回布尔 Series|
|替换值|`series.replace(mapping)`|返回新 Series|
|去重|`df.drop_duplicates(subset=None, keep='first')`|返回去重 DataFrame|
|重命名|`df.rename(columns=mapping)`|返回新 DataFrame|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import pandas as pd
s = pd.Series([" 1 ", "bad", None], dtype="string")
clean = pd.to_numeric(s.str.strip(), errors="coerce")
print(clean.isna().tolist())
# 期望输出:
# [False, True, True]
```
## 分组、聚合与窗口（GroupBy, Aggregation, and Windows）
聚合缩减行数，转换保持原索引，窗口基于相邻观察。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|分组|`df.groupby(keys, dropna=True, observed=False)`|返回 GroupBy|
|多聚合|`grouped.agg(total=('x','sum'), avg=('x','mean'))`|返回聚合 DataFrame|
|同形状转换|`grouped['x'].transform('mean')`|返回与原组行对齐的 Series|
|逐组筛选|`grouped.filter(fn)`|返回保留组的 DataFrame|
|透视表|`pd.pivot_table(df, values, index, columns, aggfunc='mean')`|返回透视 DataFrame|
|交叉表|`pd.crosstab(index, columns, normalize=False)`|返回频数表|
|滚动窗口|`series.rolling(window, min_periods=None).mean()`|返回滚动均值 Series|
|扩展窗口|`series.expanding(min_periods=1).sum()`|返回累计窗口结果|
|滞后|`series.shift(periods=1)`|返回移位 Series|
|差分|`series.diff(periods=1)`|返回差值 Series|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import pandas as pd
df = pd.DataFrame({"team": ["A","A","B"], "score": [1,3,5]})
print(df.groupby("team")["score"].agg(["sum","mean"]))
# 期望输出:
# sum  mean
# team           
# A       4   2.0
# B       5   5.0
```
## 合并、重塑与排序（Merge, Reshape, and Sort）
连接前验证键唯一性和预期基数，避免行数爆炸。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|数据库式连接|`left.merge(right, on=keys, how='inner', validate='one_to_one')`|返回新 DataFrame；基数不符抛 MergeError|
|索引连接|`left.join(right, how='left')`|返回按索引连接结果|
|纵向拼接|`pd.concat(frames, axis=0, ignore_index=False)`|返回拼接对象|
|长转宽|`df.pivot(index, columns, values)`|返回宽表；键重复抛 ValueError|
|聚合透视|`df.pivot_table(...)`|重复键可聚合|
|宽转长|`df.melt(id_vars, value_vars)`|返回长表|
|堆叠|`df.stack() / df.unstack()`|在列层与索引层间重塑|
|排序|`df.sort_values(by, ascending=True, na_position='last')`|返回排序结果|
|排名|`series.rank(method='average', ascending=True)`|返回浮点排名|
|采样|`df.sample(n=None, frac=None, random_state=None)`|返回抽样结果|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import pandas as pd
orders = pd.DataFrame({"id": [1,2], "uid": [10,20]})
users = pd.DataFrame({"uid": [10,20], "name": ["A","B"]})
out = orders.merge(users, on="uid", validate="many_to_one")
print(out[["id","name"]].to_dict("records"))
# 期望输出:
# [{'id': 1, 'name': 'A'}, {'id': 2, 'name': 'B'}
```
## 导出、性能与 Copy-on-Write（Export, Performance, and CoW）
列式格式适合分析；pandas 3 默认 Copy-on-Write，仍应避免依赖隐式视图修改。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|CSV 输出|`df.to_csv(path, index=False, encoding='utf-8')`|写文件，返回 None|
|Parquet 输出|`df.to_parquet(path, index=False)`|写列式文件|
|SQL 输出|`df.to_sql(name, connection, if_exists='fail', index=False)`|写数据库并返回行数或 None|
|字典输出|`df.to_dict(orient='records')`|返回字典列表|
|NumPy 视图/副本|`df.to_numpy(copy=False)`|返回 ndarray，不保证零复制|
|内存统计|`df.memory_usage(deep=True)`|返回各列字节数 Series|
|分类类型|`series.astype('category')`|返回分类 Series，低基数字符串常节省内存|
|批量映射|`series.map(mapping_or_callable)`|返回映射 Series|
|逐行应用|`df.apply(fn, axis=1)`|返回 Series/DataFrame；通常慢于向量化|
|空表判断|`df.empty`|返回布尔值|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import pandas as pd
df = pd.DataFrame({"group": ["x","x","y"]})
before = int(df.memory_usage(deep=True).sum())
df["group"] = df["group"].astype("category")
after = int(df.memory_usage(deep=True).sum())
print(after < before)
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
- [[02-Pandas 数据处理（Pandas）]]
## 官方参考（Official References）
- [pandas 用户指南](https://pandas.pydata.org/docs/user_guide/)
