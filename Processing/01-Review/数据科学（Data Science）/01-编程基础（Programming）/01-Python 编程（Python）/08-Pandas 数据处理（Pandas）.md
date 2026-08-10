---
title: Pandas 数据处理（Pandas）
aliases:
  - Pandas
status: review
detail_level: comprehensive
source:
  - Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/Pandas.md
suggested_target: Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/08-Pandas 数据处理（Pandas）.md
operation: 新建
merge_target: null
---

# Pandas 数据处理（Pandas）

## 1. 核心对象

- `Series`：带索引的一维数据。
- `DataFrame`：由行索引和列标签组织的二维表格。

```python
import pandas as pd

frame = pd.DataFrame(
    {
        "name": ["Ada", "Lin", "Sam"],
        "age": [28, 31, 25],
        "score": [0.91, 0.87, 0.95],
    }
)

print(frame.shape)
print(frame.dtypes)
print(frame.head())
```

Pandas 会按照索引标签对齐数据。这非常强大，但也可能在索引不一致时产生意外的 `NaN`。

## 2. 读取数据后的第一轮检查

```python
import pandas as pd

frame = pd.read_csv(
    "samples.csv",
    usecols=["id", "label", "score", "created_at"],
    dtype={"id": "string", "label": "category"},
    parse_dates=["created_at"],
)

print(frame.head())
print(frame.shape)
frame.info()
print(frame.describe(include="all"))
```

第一轮应检查：

- 行数、列数和列名是否符合预期。
- `dtype` 是否正确，尤其是 ID、类别和日期。
- 缺失值与重复值。
- 数值范围和异常类别。
- 主键是否应该唯一。

```python
print(frame.isna().sum())
print(frame.duplicated().sum())
print(frame["label"].value_counts(dropna=False))
print(frame["id"].is_unique)
```

## 3. 选择行和列

```python
scores = frame["score"]
subset = frame[["id", "label", "score"]]

high_scores = frame.loc[frame["score"] >= 0.9, ["id", "label", "score"]]
first_rows = frame.iloc[:5, :3]
```

- `.loc` 按标签选择。
- `.iloc` 按整数位置选择。
- 布尔条件要使用 `&`、`|`、`~`，并为每个条件加括号。

```python
selected = frame.loc[
    (frame["score"] >= 0.8) & frame["label"].notna()
]
```

不要写 `condition_a and condition_b`，因为 Python 的 `and` 不能逐元素组合 Series。

## 4. 安全赋值

```python
# 使用 .loc 明确指定行和列，避免链式索引造成赋值不确定。
frame.loc[frame["score"] < 0, "score"] = pd.NA

# 如果需要独立子表，显式复制，后续修改不会依赖原表的视图行为。
working = frame.loc[:, ["id", "label", "score"]].copy()
working["score_percent"] = working["score"] * 100
```

避免：

```python
# frame[frame["score"] < 0]["score"] = 0  # 链式赋值，可能没有修改原表。
```

## 5. 缺失值与类型转换

```python
import pandas as pd

frame["age"] = pd.to_numeric(frame["age"], errors="coerce").astype("Int64")
frame["created_at"] = pd.to_datetime(frame["created_at"], errors="coerce")

frame["label"] = frame["label"].fillna("unknown")
frame["score"] = frame["score"].fillna(frame["score"].median())
```

填充前必须回答“缺失代表什么”。随意用均值或 0 填充可能改变数据含义，并造成数据泄漏。机器学习场景中，填充值只能根据训练集计算。

```python
required_columns = ["id", "label"]
cleaned = frame.dropna(subset=required_columns)
```

## 6. 文本、日期与去重

```python
frame["name"] = frame["name"].str.strip().str.lower()
frame["month"] = frame["created_at"].dt.to_period("M")

# 按业务主键去重，并明确保留哪一条记录。
frame = (
    frame.sort_values("created_at")
    .drop_duplicates(subset=["id"], keep="last")
)
```

去重前先确定重复的业务定义；整行相同、主键相同和部分字段相同不是同一个问题。

## 7. 分组：split-apply-combine

### 聚合（Aggregation）

```python
summary = (
    frame.groupby("label", dropna=False)
    .agg(
        sample_count=("id", "size"),
        mean_score=("score", "mean"),
        max_score=("score", "max"),
    )
    .reset_index()
)
```

### 变换（Transformation）

```python
# transform 返回与原行数相同的结果，因此可以直接写回原表。
group_mean = frame.groupby("label")["score"].transform("mean")
frame["score_centered"] = frame["score"] - group_mean
```

- `agg()` 用于生成每组的摘要表。
- `transform()` 用于把组级结果对齐回原始行。
- 自定义 `apply()` 更灵活，但通常更慢；能用内置聚合或向量化操作时优先不用它。

## 8. 合并与拼接

### `merge`

```python
users = pd.DataFrame({"user_id": [1, 2], "name": ["Ada", "Lin"]})
orders = pd.DataFrame({"user_id": [1, 1, 3], "amount": [10, 20, 30]})

result = users.merge(
    orders,
    on="user_id",
    how="left",
    validate="one_to_many",  # 关系不符合预期时立即报错，防止静默放大行数。
    indicator=True,
)
```

连接前后都检查：

- 键是否唯一。
- 预期是一对一、一对多还是多对多。
- 行数是否意外增加。
- 未匹配记录有多少。

### `concat`

```python
all_months = pd.concat([january, february], ignore_index=True)
```

`concat()` 沿某个轴堆叠表；`merge()` 根据键关联表，两者用途不同。

## 9. 排序、重塑与透视表

```python
ordered = frame.sort_values(
    ["label", "score"],
    ascending=[True, False],
    na_position="last",
)

pivot = frame.pivot_table(
    index="label",
    columns="month",
    values="score",
    aggfunc="mean",
)
```

宽表转长表：

```python
long_frame = wide_frame.melt(
    id_vars=["id"],
    var_name="metric",
    value_name="value",
)
```

## 10. 文件读写与大文件

```python
frame.to_csv("cleaned.csv", index=False, encoding="utf-8")
frame.to_excel("cleaned.xlsx", index=False)
```

读取大 CSV 时只选需要的列、指定类型，或分块处理：

```python
import pandas as pd

total_rows = 0
for chunk in pd.read_csv("large.csv", chunksize=100_000):
    valid_chunk = chunk.dropna(subset=["id"])
    total_rows += len(valid_chunk)
```

分块只降低单次内存占用；跨块去重、全局排序和全局统计需要额外设计状态。

## 11. 一个可复用的清洗管道

```python
import pandas as pd


def clean_samples(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"id", "label", "score", "created_at"}
    missing_columns = required - set(frame.columns)
    if missing_columns:
        raise ValueError(f"缺少列：{sorted(missing_columns)}")

    cleaned = frame.loc[:, sorted(required)].copy()
    cleaned["id"] = cleaned["id"].astype("string").str.strip()
    cleaned["label"] = cleaned["label"].astype("string").str.strip().str.lower()
    cleaned["score"] = pd.to_numeric(cleaned["score"], errors="coerce")
    cleaned["created_at"] = pd.to_datetime(cleaned["created_at"], errors="coerce")

    # 关键字段缺失时无法可靠恢复，因此直接移除并在上层记录数量。
    cleaned = cleaned.dropna(subset=["id", "label", "created_at"])
    cleaned = cleaned.loc[cleaned["score"].between(0, 1, inclusive="both")]

    # 同一 ID 保留时间最新的记录，规则明确才能保证重复运行结果一致。
    cleaned = (
        cleaned.sort_values("created_at")
        .drop_duplicates(subset=["id"], keep="last")
        .reset_index(drop=True)
    )
    return cleaned
```

## 12. Series (Series) 详细操作

`Series` 由值数组 (Values) 和索引 (Index) 组成。算术运算会按索引标签对齐，而不是单纯按位置对齐。

```python
import pandas as pd

left = pd.Series([10, 20], index=["a", "b"])
right = pd.Series([1, 2], index=["b", "c"])

print(left + right)
# a、c 缺少对应项，因此结果是 NaN；只有 b 能完成加法。

print(left.add(right, fill_value=0))
```

常用属性 (Attributes)：

| 属性 | 含义 |
|---|---|
| `.index` | 索引对象 (Index Object) |
| `.array` | 底层扩展数组 (Extension Array) |
| `.to_numpy()` | 转为 NumPy 数组 (NumPy Array) |
| `.dtype` | 数据类型 (Data Type) |
| `.name` | Series 名称 |
| `.size` | 元素数量 |

## 13. DataFrame (DataFrame) 创建方式

```python
import numpy as np
import pandas as pd

from_dict = pd.DataFrame(
    {
        "name": ["Ada", "Lin"],
        "score": [0.9, 0.8],
    },
    index=["sample-1", "sample-2"],
)

from_records = pd.DataFrame.from_records(
    [
        {"name": "Ada", "score": 0.9},
        {"name": "Lin", "score": 0.8},
    ]
)

from_array = pd.DataFrame(
    np.arange(6).reshape(2, 3),
    columns=["a", "b", "c"],
)
```

用标量创建列时会广播到所有行：

```python
from_dict["source"] = "manual"
```

赋值 Series 时按照索引对齐；如果只想按位置赋值，应先确认长度，再使用 `.to_numpy()`，但要清楚这样会放弃标签安全性。

## 14. 索引 (Index) 设计

默认的 `RangeIndex` 对大多数清洗流程已经足够。只有索引具有明确业务意义，并且确实需要标签对齐时才设置业务索引。

```python
indexed = frame.set_index("id", verify_integrity=True)
restored = indexed.reset_index()
```

`verify_integrity=True` 会在索引重复时抛错，适合本应唯一的主键 (Primary Key)。

多级索引 (MultiIndex) 可以表达多维标签：

```python
grouped = frame.set_index(["label", "created_at"]).sort_index()
cat_rows = grouped.loc["cat"]
```

多级索引能简化部分分组和重塑操作，但也会增加理解成本；普通列能清晰完成任务时不必强行使用。

## 15. 缺失值 (Missing Values) 详细规则

Pandas 中常见缺失标记：

- `np.nan`：传统浮点缺失值 (Floating Missing Value)。
- `pd.NA`：可空数据类型 (Nullable Data Type) 的通用缺失值。
- `NaT`：日期时间缺失值 (Not a Time)。
- `None`：对象列中可能出现，但通常会被转换。

```python
import pandas as pd

nullable = pd.Series([1, None, 3], dtype="Int64")
flags = pd.Series([True, None, False], dtype="boolean")
names = pd.Series(["Ada", None], dtype="string")
```

检测与统计：

```python
missing_by_column = frame.isna().sum()
missing_rate = frame.isna().mean().sort_values(ascending=False)

complete_rows = frame.notna().all(axis=1)
```

删除参数 (Parameters)：

```python
frame.dropna(
    axis=0,                 # 删除行；axis=1 表示删除列。
    how="any",             # 任一缺失即删除；how="all" 表示全部缺失才删除。
    subset=["id", "label"],
    thresh=None,            # 若设置，至少保留指定数量的非缺失值。
)
```

填充方法 (Filling Methods)：

```python
frame["category"] = frame["category"].fillna("unknown")
frame["sensor"] = frame["sensor"].ffill(limit=2)
frame["target"] = frame["target"].bfill()
```

时间序列 (Time Series) 中前向填充 (Forward Fill) 隐含“最近观测仍有效”的假设，必须根据业务判断，不能因为 API 方便就使用。

## 16. 类型系统 (Type System) 与内存

```python
frame = frame.convert_dtypes()
frame["label"] = frame["label"].astype("category")
frame["id"] = frame["id"].astype("string")
```

常见类型选择：

| 数据 | 推荐类型 | 原因 |
|---|---|---|
| ID、邮编、电话号码 | `string` | 不能参与数值计算，可能有前导零 |
| 少量重复类别 | `category` | 节省内存，并明确类别语义 |
| 可缺失整数 | `Int64` | 普通 NumPy 整数不能表示缺失 |
| 可缺失布尔 | `boolean` | 支持 `pd.NA` |
| 时间点 | `datetime64[ns]` 或含时区类型 | 支持 `.dt` 操作 |

检查内存：

```python
frame.info(memory_usage="deep")
print(frame.memory_usage(deep=True).sort_values(ascending=False))
```

## 17. `merge()` 连接类型 (Join Types) 详解

| `how` | 保留的键 |
|---|---|
| `inner` | 两边都有的键 |
| `left` | 左表全部键 |
| `right` | 右表全部键 |
| `outer` | 两边键的并集 |
| `cross` | 笛卡尔积 (Cartesian Product) |

`validate` 的常用值：

- `one_to_one` / `1:1`
- `one_to_many` / `1:m`
- `many_to_one` / `m:1`
- `many_to_many` / `m:m`

```python
merged = left.merge(
    right,
    left_on="user_id",
    right_on="owner_id",
    how="left",
    suffixes=("_user", "_order"),
    validate="one_to_many",
    indicator="merge_status",
)

print(merged["merge_status"].value_counts())
```

多对多连接 (Many-to-many Join) 会把相同键两边的组合全部展开，行数可能成倍增长。使用前应明确这是业务需要，而不是数据重复造成的意外。

## 18. GroupBy (GroupBy) 详细接口

### 单个聚合与多个聚合

```python
grouped = frame.groupby("label", dropna=False, observed=True)

means = grouped["score"].mean()
statistics = grouped["score"].agg(["count", "mean", "std", "min", "max"])
```

`observed=True` 对分类列 (Categorical Column) 只返回实际出现的类别，避免生成没有观测的组合。

### 过滤 (Filter)

```python
large_groups = frame.groupby("label").filter(lambda group: len(group) >= 10)
```

### 组内排名 (Within-group Ranking)

```python
frame["rank_in_label"] = (
    frame.groupby("label")["score"]
    .rank(method="dense", ascending=False)
)
```

### 分组滚动窗口 (Grouped Rolling Window)

```python
ordered = frame.sort_values(["device_id", "created_at"])
ordered["rolling_mean"] = (
    ordered.groupby("device_id")["value"]
    .transform(lambda series: series.rolling(3, min_periods=1).mean())
)
```

## 19. 日期时间 (Datetime) 与时间序列 (Time Series)

```python
import pandas as pd

frame["created_at"] = pd.to_datetime(
    frame["created_at"],
    errors="coerce",
    utc=True,
)

frame["year"] = frame["created_at"].dt.year
frame["weekday"] = frame["created_at"].dt.day_name()
frame["hour"] = frame["created_at"].dt.hour
```

时区 (Time Zone) 规则：

- 跨系统存储时间通常使用 UTC (Coordinated Universal Time)。
- 展示给用户时再转换到本地时区。
- 不要把带时区和不带时区的时间混在同一逻辑中。

```python
local_time = frame["created_at"].dt.tz_convert("Asia/Shanghai")
```

重采样 (Resampling)：

```python
hourly = (
    frame.set_index("created_at")
    .resample("1h")["value"]
    .mean()
)
```

## 20. 窗口操作 (Window Operations)

```python
series = frame["value"]

frame["rolling_mean_7"] = series.rolling(window=7, min_periods=1).mean()
frame["expanding_mean"] = series.expanding(min_periods=1).mean()
frame["ewm_mean"] = series.ewm(span=7, adjust=False).mean()
```

- 滚动窗口 (Rolling Window)：只使用最近固定范围。
- 扩展窗口 (Expanding Window)：从起点累积到当前行。
- 指数加权窗口 (Exponentially Weighted Window)：越近的数据权重越大。

## 21. 采样、排序和重复值

```python
sample = frame.sample(n=100, random_state=42, replace=False)

duplicate_mask = frame.duplicated(subset=["id"], keep=False)
duplicate_rows = frame.loc[duplicate_mask].sort_values("id")

deduplicated = frame.drop_duplicates(subset=["id"], keep="last")
```

`random_state` 让同一环境中的采样可复现。抽样前确认是否需要分层抽样 (Stratified Sampling)，尤其是类别不平衡数据。

## 22. `map()`、`apply()` 与向量化 (Vectorization)

```python
label_names = {0: "negative", 1: "positive"}
frame["label_name"] = frame["label"].map(label_names)

frame["name_length"] = frame["name"].str.len()  # 向量化字符串接口。
```

选择顺序：

1. 优先 Pandas/NumPy 内置向量化方法。
2. 单列元素映射可用 `Series.map()`。
3. 按行聚合先尝试向量化表达式。
4. 无法表达时才使用 `DataFrame.apply(axis=1)`。
5. `iterrows()` 通常最慢，并可能改变行内类型；确需迭代时考虑 `itertuples()`。

## 23. 方法链 (Method Chaining) 与 `pipe()`

```python
def keep_valid_scores(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.loc[frame["score"].between(0, 1)].copy()


result = (
    pd.read_csv("samples.csv")
    .rename(columns=str.lower)
    .drop_duplicates(subset=["id"], keep="last")
    .pipe(keep_valid_scores)
    .sort_values("score", ascending=False)
    .reset_index(drop=True)
)
```

方法链 (Method Chaining) 能让数据流顺序清晰，但链过长时应拆成有名称的函数，并在关键阶段断言数据契约 (Data Contract)。

```python
assert result["id"].is_unique
assert result["score"].between(0, 1).all()
```

## 24. 常见错误

- 忽略索引对齐，导致计算后出现意外 `NaN`。
- 使用链式索引赋值。
- 把 ID 当成数字，丢失前导零。
- 在划分训练/验证集之前用全量数据计算填充值。
- `merge` 后不检查关系和行数。
- 滥用逐行 `iterrows()` 或 `apply(axis=1)`，忽略向量化方案。
- 用 `inplace=True` 让处理链难以测试和复用。

## 25. 完成检查

- [ ] 能在读取后检查形状、类型、缺失、重复和主键。
- [ ] 能正确使用 `.loc`、`.iloc` 和布尔筛选。
- [ ] 能区分 `agg`、`transform`、`merge` 与 `concat`。
- [ ] 能解释索引对齐和链式赋值风险。
- [ ] 能把数据清洗写成输入明确、返回新表的函数。

## 参考资料

- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/)
- [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Group by: split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html)
