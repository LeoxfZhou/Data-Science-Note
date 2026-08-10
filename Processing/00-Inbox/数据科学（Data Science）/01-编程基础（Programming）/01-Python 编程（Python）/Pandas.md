## 一、 pandas 简介
**Pandas** 是 Python 进行数据分析的一个扩展库，是基于 NumPy 的一种工具。能够快速得从不同格式的文件中加载数据（比如 CSV、Excel 文件等），然后将其转换为可处理的对象。
Pandas 在 `ndarray` 的基础上构建出了两种更适用于数据分析的存储结构，分别是 **Series**（一维数据结构）和 **DataFrame**（二维数据结构）。在操作 Series 和 DataFrame 时，基本上可以看成是 NumPy 中的一维和二维数组来操作，数组的绝大多数操作它们都可以适用。
---
## 二、 Pandas Series
Series 是一种一维数据结构，每一个元素都带有一个索引，与 NumPy 中的一维数组类似。Series 可以保存任何数据类型，比如整数、字符串、浮点数、Python 对象等，它的索引默认为整数，从 0 开始依次递增。
### 1. 创建 Series 对象
`pd.Series(data=None, index=None, dtype=None, name=None)`
- `data`: array-like, dict, or scalar value
- `index`: 索引必须是不可变数据类型，允许相同。不指定时，默认为从 0 开始依次递增的整数
- `dtype`: 数据类型，如果没有指定，则会自动推断得出
- `name`: 设置 Series 的名称

```Python
import numpy as np
import pandas as pd
""" 标量创建Series对象:
标量值按照 index 的数量进行重复，并与其一一对应
如果没有指定index, 就只有一个数据 """
d = 99
ser = pd.Series(data=d)
print(ser)                                      # 0    99
                                                # dtype: int64
ser = pd.Series(data=d, index=[1, 2, 3])
print(ser)                                      # 1    99
                                                # 2    99
                                                # 3    99
                                                # dtype: int64
""" str创建Series对象: 当作标量一样处理 """
d = 'abc'
ser = pd.Series(data=d, index=[1, 2, 3])
print(ser)                                      # 1    abc
                                                # 2    abc
                                                # 3    abc
                                                # dtype: object
""" list创建Series对象 """
d = ['a', 'b', 'c']
ser = pd.Series(data=d)
print(ser)                                      # 0    a
                                                # 1    b
                                                # 2    c
                                                # dtype: object
""" ndarray创建Series对象 """
d = np.array([1, 2, 3])
ser = pd.Series(data=d, dtype=np.float64, index=('one', 'two', 'three'), name='test-series')
print(ser)                                      # one      1.0
                                                # two      2.0
                                                # three    3.0
                                                # Name: test-series, dtype: float64
""" dict创建Series对象:
默认用字典的键作为index, 对应字典的值作为数据 """
d = {'a': 1, 'b': 2, 'c': 3}
ser = pd.Series(data=d)  # index=['a', 'b', 'c'] 可省略
print(ser)                                      # a    1
                                                # b    2
                                                # c    3
                                                # dtype: int64
""" dict创建Series对象:
如果指定索引不是字典的键, 那么会得到缺失值NaN """
d = {'a': 1, 'b': 2, 'c': 3}
ser = pd.Series(data=d, index=['a', 'y', 'z'])
print(ser)                                      # a    1.0
                                                # y    NaN
                                                # z    NaN
                                                # dtype: float64
```

### 2. 访问 Series 数据
两种方式: 位置索引访问、索引标签访问。
**位置索引访问：**

```Python
import numpy as np
import pandas as pd
d = np.array([1, 2, 3, 4, 5])
# 注意：索引中有重复标签 'e'
ser = pd.Series(data=d, index=('a', 'e', 'c', 'd', 'e'))
print(ser)                     # a    1
                               # e    2
                               # c    3
                               # d    4
                               # e    5
                               # dtype: int64
# ⚠️ 警告！未来版本中 ser[1] 将按标签 '1' 查找（但这里没有标签 '1'）
# 当前仍按位置返回第1个元素（值为2），但这是不安全的！
print(ser[1])                  # 2  ← 实际是位置索引（但会报 FutureWarning）
# 切片 [1:3] 在 Series 中始终是**位置切片**（即使有整数标签）
print(ser[1:3])                # e    2
                               # c    3
                               # dtype: int64
# 步进切片也按位置
print(ser[:-2:2])              # a    1
                               # c    3
                               # dtype: int64
# 整数列表索引：当前按位置，但未来会按标签 → 强烈不推荐！
print(ser[[2, 1, 3]])          # c    3
                               # e    2
                               # d    4
                               # dtype: int64
```

**索引标签访问：**

```Python
import numpy as np
import pandas as pd
d = np.array([1, 2, 3, 4, 5])
ser = pd.Series(data=d, index=('a', 'e', 'c', 'd', 'e'))  # 注意：'e' 重复
print(ser)                     # a    1
                               # e    2
                               # c    3
                               # d    4
                               # e    5
                               # dtype: int64
# 按唯一标签取值
print(ser['c'])                # 3
# 按重复标签取值 → 返回所有匹配项（Series）
print(ser['e'])                # e    2
                               # e    5
                               # dtype: int64
""" 索引标签切片时, 右边不是开区间哦 """
# 标签切片 ['a':'d'] 是**闭区间**（包含 'd'），且按**原始顺序**截取
print(ser['a':'d'])            # a    1
                               # e    2
                               # c    3
                               # d    4
                               # dtype: int64
# 步进切片 [: 'c' : 2] → 从开头到 'c'（含），步长2
print(ser[:'c':2])             # a    1
                               # c    3
                               # dtype: int64
# 按标签列表索引（顺序由列表决定，重复标签会全部返回）
print(ser[['c', 'e', 'd']])    # c    3
                               # e    2   ← 第一个 'e'
                               # e    5   ← 第二个 'e'
                               # d    4
                               # dtype: int64
```

### 3. 修改 Series 索引与数据
**修改 Series 索引：**  
可以通过给 `index` 属性重新赋值达到修改索引的目的。

```Python
import pandas as pd
ser = pd.Series([4, 7, -5, 3], index=['a', 'b', 'c','d'])
print(ser)                    # a    4
                              # b    7
                              # c   -5
                              # d    3
                              # dtype: int64
ser.index = ['aa', 'bb', 'cc', 'dd'] # 修改原数据
print(ser)                    # aa    4
                              # bb    7
                              # cc   -5
                              # dd    3
                              # dtype: int64
```

**修改 Series 数据：**  
可以通过索引和切片的方式修改数据。

```Python
import pandas as pd
ser = pd.Series([2, 3, 4, 5], index=['a', 'b', 'c','d'])
ser['a'] = 8
print(ser)                    # a    8
                              # b    3
                              # c    4
                              # d    5
                              # dtype: int64
ser['b':'d'] = [7, 8, 9]
print(ser)                    # a    8
                              # b    7
                              # c    8
                              # d    9
                              # dtype: int64
```

### 4. Series 常用属性
|属性|描述|
|---|---|
|`dtype`|返回 Series 对象数据类型|
|`name`|返回 Series 对象名称|
|`shape`|返回 Series 对象的形状|
|`size`|返回 Series 中的元素数量|
|`values`|以 ndarray 数组的形式返回 Series 中的数据|
|`index`|返回 index|

```Python
import pandas as pd
d = [1, 2, 3, 4]
ser = pd.Series(data=d, index=['a', 'b', 'c', 'd'], name="Test-Series")
print(ser.dtype)      # int64
print(ser.name)       # Test-Series
print(ser.size)       # 4
print(ser.values)     # [1 2 3 4]
print(ser.index)      # Index(['a', 'b', 'c', 'd'], dtype='object')
```

### 5. Series 运算
Series 保留了 NumPy 中的数组运算，且 Series 进行数组运算的时候，索引与值之间的映射关系不会发生改变。在进行 Series 和 Series 的运算时，把两个 Series 中索引一样的值进行运算，其他不一样的做并集，对应的值为 NaN。

```Python
import pandas as pd
ser1 = pd.Series([15, 20], index=["a", "b"])
print(ser1 + 1)        # a    16
                       # b    21
                       # dtype: int64
print(ser1 - 1)        # a    14
                       # b    19
                       # dtype: int64
print(ser1 * 2)        # a    30
                       # b    40
                       # dtype: int64
print(ser1 / 2)        # a     7.5
                       # b    10.0
                       # dtype: float64
ser2 = pd.Series([1, 2], index=["c", "a"])
print(ser1 + ser2)     # a    17.0
                       # b     NaN
                       # c     NaN
                       # dtype: float64
print(ser1 - ser2)     # a    13.0
                       # b     NaN
                       # c     NaN
                       # dtype: float64
print(ser1 * ser2)     # a    30.0
                       # b     NaN
                       # c     NaN
                       # dtype: float64
print(ser1 / ser2)     # a    7.5
                       # b    NaN
                       # c    NaN
                       # dtype: float64
```

---
## 三、 Pandas DataFrame
DataFrame 是一种表格型的二维数据结构，既有行索引 (`index`)，又有列索引 (`columns`)，且默认都是从0开始递增的整数。可以把每一列看作是共同用一个索引的 Series，且不同列的数据类型可以不同。
### 1. 创建 DataFrame 对象
`pd.DataFrame(data=None, index=None, columns=None, dtype=None)`
- `data`: array-like, dict
- `index`: 行索引。不指定时，默认为从 0 开始依次递增的整数
- `columns`: 列索引。不指定时，默认为从 0 开始依次递增的整数
- `dtype`: 数据类型，如果没有指定，则会自动推断得出

```Python
import numpy as np
import pandas as pd
""" ndarray创建DataFrame对象 """
d = np.array([[1, 2, 3], [4, 5, 6]])
df = pd.DataFrame(data=d, dtype=np.float64)
print(df)                     #      0    1    2
                              # 0  1.0  2.0  3.0
                              # 1  4.0  5.0  6.0
""" 单一列表创建DataFrame对象 """
d = ['Tom', 'Bob', 'Linda']
df = pd.DataFrame(data=d)
print(df)                     #        0
                              # 0    Tom
                              # 1    Bob
                              # 2  Linda
""" 嵌套列表创建DataFrame对象 """
d = [['Tom', 17], ['Bob', 18], ['Linda', 26]]
df = pd.DataFrame(data=d, index=['p1', 'p2', 'p3'], columns=['name', 'age'])
print(df)                     #      name  age
                              # p1    Tom   17
                              # p2    Bob   18
                              # p3  Linda   26
""" 字典嵌套列表创建DataFrame对象:
字典data中, 所有键对应的值的元素个数必须相同
默认情况下，字典的键被用作列索引 """
d = {'name': ['Tom', 'Bob', 'Linda'], 'age': [17, 18, 26]}
df = pd.DataFrame(data=d, index=['p1', 'p2', 'p3'])
print(df)                     #      name  age
                              # p1    Tom   17
                              # p2    Bob   18
                              # p3  Linda   26
""" Series创建DataFrame对象 """
d = {
    'name': pd.Series(['Tom', 'Bob', 'Linda'], index=['p1', 'p2', 'p3']),
    'age': pd.Series([17, 18, 26], index=['p1', 'p2', 'p8'])
}
df = pd.DataFrame(data=d)
print(df)                     #      name   age
                              # p1    Tom  17.0
                              # p2    Bob  18.0
                              # p3  Linda   NaN
                              # p8    NaN  26.0
d = [
    pd.Series(['Tom', 'Bob', 'Linda'], index=['p1', 'p2', 'p3'], name="name"),
    pd.Series([17, 18, 26], index=['p1', 'p2', 'p3'], name='age')
]
df = pd.DataFrame(data=d)
print(df)                     #        p1   p2     p3
                              # name  Tom  Bob  Linda
                              # age    17   18     26
```

### 2. 访问 DataFrame 数据
**索引获取列数据，切片获取行数据：**

```Python
import pandas as pd
d = {'name': ['Tom', 'Bob', 'Linda'], 'age': [17, 18, 26], 'height': [172, 176, 188]}
df = pd.DataFrame(data=d, index=['p1', 'p2', 'p3'])
print(df)                                 #      name  age  height
                                          # p1    Tom   17     172
                                          # p2    Bob   18     176
                                          # p3  Linda   26     188
# 索引获取列数据
print(df['age'])                          # p1    17
                                          # p2    18
                                          # p3    26
                                          # Name: age, dtype: int64
print(df[['age', 'name']])                #     age   name
                                          # p1   17    Tom
                                          # p2   18    Bob
                                          # p3   26  Linda
# 切片获取行数据
print(df[0: 1])# 下标切片左闭右开
                                          #    name  age  height
                                          # p1  Tom   17     172
print(df['p1': 'p2'])# 标签切片两边都是闭区间
                                          #    name  age  height
                                          # p1  Tom   17     172
                                          # p2  Bob   18     176
# 组合使用
print(df[['name', 'age']][0: : 2])        #      name  age
                                          # p1    Tom   17
                                          # p3  Linda   26
print(df[0: : 2][['name', 'age']])        #      name  age
                                          # p1    Tom   17
                                          # p3  Linda   26
```

`**loc**` **指定标签获取数据，**`**iloc**` **指定下标获取数据：**

```Python
import pandas as pd
d = {'name': ['Tom', 'Bob', 'Linda'], 'age': [17, 18, 26], 'height': [172, 176, 188]}
df = pd.DataFrame(data=d, index=['p1', 'p2', 'p3'])
print(df)
""" loc允许接两个参数分别是行和列, 且只能接收标签索引 """
# 选取行索引为'p1'的数据
print(df.loc['p1'])                     # name      Tom
                                        # age        17
                                        # height    172
                                        # Name: p1, dtype: object
# 选取行索引为'p2'且列索引为'age'的数据
print(df.loc['p2', 'age'])              # 18
# 选取行索引为'p2'且列索引分别为'age'和'name'的数据
print(df.loc['p2', ['age', 'name']])    # age      18
                                        # name    Bob
                                        # Name: p2, dtype: object
# 选取行索引分别为'p3'和'p2'且列索引分别为'age'和'name'的数据
print(df.loc[['p3', 'p2'], ['age', 'name']])  #     age   name
                                              # p3   26  Linda
                                              # p2   18    Bob
""" iloc允许接两个参数分别是行和列, 且只能接收整数索引 """
# 选取行索引为0的数据
print(df.iloc[0])                       # name      Tom
                                        # age        17
                                        # height    172
                                        # Name: p1, dtype: object
# 选取行索引为1且列索引为1的数据
print(df.iloc[1, 1])                    # 18
# 选取行索引为1且列索引分别为1和0的数据
print(df.iloc[1, [1, 0]])               # age      18
                                        # name    Bob
                                        # Name: p2, dtype: object
# 选取行索引分别为2和1且列索引分别为1和0的数据
print(df.iloc[[2, 1], [1, 0]])          #     age   name
                                        # p3   26  Linda
                                        # p2   18    Bob
```

### 3. 修改 DataFrame 索引与数据
**修改 DataFrame 索引：**  
修改对应的属性即可。

```Python
import pandas as pd
d = {'name': ['Tom', 'Bob', 'Linda'], 'age': [17, 18, 26], 'height': [172, 176, 188]}
df = pd.DataFrame(data=d, index=['p1', 'p2', 'p3'])
print(df)                               #      name  age  height
                                        # p1    Tom   17     172
                                        # p2    Bob   18     176
                                        # p3  Linda   26     188
""" 修改行索引 """
df.index = ['n1', 'n2', 'n3']
""" 修改列索引 """
df.columns = ['names', 'ages', 'heights']
print(df)                               #     names  ages  heights
                                        # n1    Tom    17      172
                                        # n2    Bob    18      176
                                        # n3  Linda    26      188
```

**修改 DataFrame 数据：**  
对访问的数据重新赋值，即可修改数据；如果访问数据不存在，则会添加数据。

```Python
import pandas as pd
d = {'name': ['Tom', 'Bob', 'Linda'], 'age': [17, 18, 26], 'height': [172, 176, 188]}
df = pd.DataFrame(data=d, index=['p1', 'p2', 'p3'])
print("初始 df:")
print(df)
# 初始 df:
#      name  age  height
# p1    Tom   17     172
# p2    Bob   18     176
# p3  Linda   26     188
# 修改单列数据（三种等价方式）
df['height'] = [1.72, 1.88, 1.76]
print("\n修改 height 后:")
print(df)
# 
# 修改 height 后:
#      name  age  height
# p1    Tom   17    1.72
# p2    Bob   18    1.88
# p3  Linda   26    1.76
# 修改多列数据
df[['name', 'age']] = [['Bob', 19], ['Tom', 22], ['Jack', 27]]
print("\n修改 name 和 age 后:")
print(df)
# 
# 修改 name 和 age 后:
#     name  age  height
# p1   Bob   19    1.72
# p2   Tom   22    1.88
# p3  Jack   27    1.76
# 追加单列
df['weight'] = [65, 75, 60]
print("\n追加 weight 后:")
print(df)
# 
# 追加 weight 后:
#     name  age  height  weight
# p1   Bob   19    1.72      65
# p2   Tom   22    1.88      75
# p3  Jack   27    1.76      60
# 追加多列
df[['grade', 'address']] = [['一', '威宁路'], ['二', '长宁路'], ['三', '大马路']]
print("\n追加 grade 和 address 后:")
print(df)
# 
# 追加 grade 和 address 后:
#     name  age  height  weight grade address
# p1   Bob   19    1.72      65     一     威宁路
# p2   Tom   22    1.88      75     二     长宁路
# p3  Jack   27    1.76      60     三     大马路
# ✅ 正确修改单行数据（关键：指定具体列或使用完整值）
# 方法1：用 .loc 指定行和所有列
df.loc['p2'] = ['Tony', 23, 1.72, 70, '二', '南京西路']  # 必须提供全部6个值！
# 方法2：只修改部分列（推荐！）
df.loc['p2', ['name', 'age', 'height']] = ['Tony', 23, 1.72]
# 方法3：用 .iloc（按位置）
df.iloc[1, :3] = ['Tony', 23, 1.72]  # 只改前3列
print("\n修改 p2 行后:")
print(df)
# 
# 修改 p2 行后:
#     name  age  height  weight grade   address
# p1   Bob   19    1.72      65     一       威宁路
# p2  Tony   23    1.72      70     二     南京西路
# p3  Jack   27    1.76      60     三       大马路
# 修改多行数据（确保值与列数匹配）
df.iloc[[0, 1], :3] = [['Jack', 27, 1.76], ['Tony', 19, 1.72]]
print("\n修改前两行后:")
print(df)
# 
# 修改前两行后:
#     name  age  height  weight grade   address
# p1  Jack   27    1.76      65     一       威宁路
# p2  Tony   19    1.72      70     二     南京西路
# p3  Jack   27    1.76      60     三       大马路
# 追加单行数据
df.loc['p4'] = ['Toby', 23, 178, 70, '四', '新地址']
print("\n追加 p4 行后:")
print(df)
# 
# 追加 p4 行后:
#     name  age  height  weight grade   address
# p1  Jack   27    1.76      65     一       威宁路
# p2  Tony   19    1.72      70     二     南京西路
# p3  Jack   27    1.76      60     三       大马路
# p4  Toby   23  178.00      70     四       新地址
```

### 4. DataFrame 常用属性
|属性|描述|
|---|---|
|`T`|转置|
|`dtypes`|返回每一列的数据类型|
|`shape`|返回 DataFrame 的形状|
|`size`|返回 DataFrame 中的元素数量|
|`index`|返回行索引|
|`columns`|返回列索引|
|`axes`|以列表形式返回行索引和列索引|
|`values`|以 ndarray 数组的形式返回 DataFrame 中的数据|

```Python
import pandas as pd
import numpy as np
d = [['Tom', 17], ['Bob', 18], ['Linda', 26]]
df = pd.DataFrame(data=d, index=['p1', 'p2', 'p3'], columns=['name', 'age'])
print(df)
#      name  age
# p1    Tom   17
# p2    Bob   18
# p3  Linda   26
print(df.T)  # 转置：行变列，列变行
#        p1   p2     p3
# name  Tom  Bob  Linda
# age    17   18     26
print(df.dtypes)  # 每列的数据类型
# name    object
# age      int64
# dtype: object
print(df.shape)  # (行数, 列数)
# (3, 2)
print(df.size)  # 总元素个数 = 行数 × 列数
# 6
print(df.index)  # 行索引（标签）
# Index(['p1', 'p2', 'p3'], dtype='object')
print(df.columns)  # 列名
# Index(['name', 'age'], dtype='object')
print(df.axes)  # [index, columns]，即所有轴的标签
# [Index(['p1', 'p2', 'p3'], dtype='object'), Index(['name', 'age'], dtype='object')]
print(df.values)  # 转换为 NumPy 数组（不含索引和列名）
# [['Tom' 17]
#  ['Bob' 18]
#  ['Linda' 26]]
```

---
## 四、 DataFrame 常用方法
### 1. 缺失值检测
`DataFrame.isnull()` / `DataFrame.notnull()`: 检测 DataFrame 中的缺失值。

```Python
import pandas as pd
import numpy as np
d = [[8, np.nan],
     [np.nan, 7],
     [0, 2],
     [np.nan, np.nan]]
df = pd.DataFrame(data=d)
print(df)
#      0    1
# 0  8.0  NaN
# 1  NaN  7.0
# 2  0.0  2.0
# 3  NaN  NaN
print(df.isnull())   # 检测缺失值：NaN → True，非 NaN → False
#        0      1
# 0  False   True
# 1   True  False
# 2  False  False
# 3   True   True
print(df.notnull())  # 检测非缺失值：NaN → False，非 NaN → True（与 isnull() 相反）
#        0      1
# 0   True  False
# 1  False   True
# 2   True   True
# 3  False  False
```

### 2. 插入列
`DataFrame.insert(loc, column, value)`
- `loc`: int，整数列索引，指定插入数据列的位置
- `column`: 新插入的数据列的名字
- `value`: int, Series, or array-like，插入的数据

```Python
import pandas as pd
d = {'name': ['Tom', 'Bob', 'Linda'], 'age': [17, 18, 26]}
df = pd.DataFrame(data=d, index=['p1', 'p2', 'p3'])
print(df)
#      name  age
# p1    Tom   17
# p2    Bob   18
# p3  Linda   26
# insert()方法插入新的列
# 参数：(loc, column_name, values)
df.insert(2, 'weight', [65, 75, 60])
print(df)
#      name  age  weight
# p1    Tom   17      65
# p2    Bob   18      75
# p3  Linda   26      60
```

### 3. 重新索引
`DataFrame.reindex(labels=None, axis=0, index=None, columns=None, fill_value=np.NaN)`
- `labels`: 要获取数据的列标签或者行标签，传入列表，与 `axis` 对应
- `axis`: 轴的方向，0 为行，1 为列
- `index`: 要获取数据的行索引，传入列表
- `columns`: 要获取数据的列索引，传入列表
- `fill_value`: 填充的缺失值（标量），默认为 `np.NaN`
- 返回重新索引组成的新的 DataFrame 对象

```Python
import pandas as pd
import numpy as np
data = np.arange(12).reshape(3, 4)
df = pd.DataFrame(data, index=['n1', 'n2', 'n3'], columns=['a', 'b', 'c', 'd'])
print(df)
#     a  b   c   d
# n1  0  1   2   3
# n2  4  5   6   7
# n3  8  9  10  11
# 重新索引行标签为 'n2' 的数据行（两种等价写法）
df2 = df.reindex(labels=['n2'], axis=0)
print(df2)
#     a  b  c  d
# n2  4  5  6  7
df2 = df.reindex(index=['n2'])  # 更常用：直接指定 index
print(df2)
#     a  b  c  d
# n2  4  5  6  7
# 重新索引列标签为 'c' 的数据列（两种等价写法）
df2 = df.reindex(labels=['c'], axis=1)
print(df2)
#      c
# n1   2
# n2   6
# n3  10
df2 = df.reindex(columns=['c'])  # 更常用：直接指定 columns
print(df2)
#      c
# n1   2
# n2   6
# n3  10
# 重新索引行：包含不存在的标签 'n4'，用 fill_value=np.pi 填充
df2 = df.reindex(index=['n2', 'n1', 'n4'], fill_value=np.pi)
print(df2)
#            a         b         c         d
# n2  4.000000  5.000000  6.000000  7.000000
# n1  0.000000  1.000000  2.000000  3.000000
# n4  3.141593  3.141593  3.141593  3.141593
```

### 4. 拼接
`pd.concat(objs, axis=0, join='outer', ignore_index=False)`
- `objs`: DataFrame 对象的序列
- `axis`: 要拼接的轴
- `join`: 外连接（`'outer'`）保留两个表中的所有信息；内连接（`'inner'`）只保留共有信息
- `ignore_index`: 如果指定为 `True`，则索引将变为从 0 开始递增的整数
- 返回一个新的 DataFrame

```Python
import pandas as pd
df = pd.DataFrame([[1, 2], [3, 4]], index=['p1', 'p2'], columns=list('AB'))
print(df)                                 
#     A  B
# p1  1  2
# p2  3  4
df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AC'))
print(df2)                                
#    A  C
# 0  5  6
# 1  7  8
# 默认 concat：axis=0（按行拼接），join='outer'（并集列）
print(pd.concat([df, df2]))               
#     A    B    C
# p1  1  2.0  NaN
# p2  3  4.0  NaN
# 0   5  NaN  6.0
# 1   7  NaN  8.0
# join='inner'：只保留公共列（A）
print(pd.concat([df, df2], join='inner')) 
#     A
# p1  1
# p2  3
# 0   5
# 1   7
# axis=1：按列拼接（左右拼接），默认 join='outer'
print(pd.concat([df, df2], axis=1))       
#       A    B    A    C
# p1  1.0  2.0  NaN  NaN
# p2  3.0  4.0  NaN  NaN
# 0   NaN  NaN  5.0  6.0
# 1   NaN  NaN  7.0  8.0
# 修改 df2 的索引，使其与 df 有重叠（'p1'）
df2.index = [0, 'p1']  
print(df2)                                
#    A  C
# 0   5  6
# p1  7  8
# 按列拼接 + join='inner' → 只保留公共行索引（'p1'）
print(pd.concat([df, df2], axis=1, join='inner'))  
#    A  B  A  C
# p1  1  2  7  8
```

### 5. 合并 (Merge)
`pd.merge(left, right, how='inner', on=None)`
- `left`: 左侧 DataFrame 对象
- `right`: 右侧 DataFrame 对象
- `how`: 要执行的合并类型。
    - `'inner'` 为内连接，取左右两个 DataFrame 的键的交集进行合并；
    - `'left'` 为左连接，以左侧 DataFrame 的键为基准进行合并，如果左侧 DataFrame 中的键在右侧不存在，则用缺失值 NaN 填充；
    - `'right'` 为右连接，以右侧 DataFrame 的键为基准进行合并，如果右侧 DataFrame 中的键在左侧不存在，则用缺失值 NaN 填充；
    - `'outer'` 为外连接，取左右两个 DataFrame 的键的并集进行合并。
- `on`: 指定用于连接的键（即列标签的名字），该键必须同时存在于左右两个 DataFrame 中，如果没有指定，那么将会以两个 DataFrame 的列名交集做为连接键。

```Python
import pandas as pd
d1 = {'name': ['Tom', 'Bob', 'Jack'], 'age': [18, 17, 19], 'weight': [65, 66, 67]}
df1 = pd.DataFrame(data=d1)
d2 = {'name': ['Tom', 'Jack'], 'height': [168, 187], 'weight': [65, 68]}
df2 = pd.DataFrame(data=d2)
print(df1)                                      #    name  age  weight
                                                # 0   Tom   18      65
                                                # 1   Bob   17      66
                                                # 2  Jack   19      67
print(df2)                                      #    name  height  weight
                                                # 0   Tom     168      65
                                                # 1  Jack     187      68
print(pd.merge(df1, df2, how='inner', on='name'))  #    name  age  weight_x  height  weight_y
                                                   # 0   Tom   18        65     168        65
                                                   # 1  Jack   19        67     187        68
print(pd.merge(df1, df2, how='left', on='name'))   #    name  age  weight_x  height  weight_y
                                                   # 0   Tom   18        65   168.0      65.0
                                                   # 1   Bob   17        66     NaN       NaN
                                                   # 2  Jack   19        67   187.0      68.0
print(pd.merge(df1, df2, how='right', on='name'))  #    name  age  weight_x  height  weight_y
                                                   # 0   Tom   18        65     168        65
                                                   # 1  Jack   19        67     187        68
print(pd.merge(df1, df2, how='outer', on='name'))  #    name  age  weight_x  height  weight_y
                                                   # 0   Bob   17        66     NaN       NaN
                                                   # 1  Jack   19        67   187.0      68.0
                                                   # 2   Tom   18        65   168.0      65.0
```

### 6. 删除行或列
`DataFrame.drop(labels=None, axis=0, index=None, columns=None, inplace=False)`
- `labels`: 要删除的列标签或者行标签，如果要删除多个，传入列表，与 `axis` 对应
- `axis`: 轴的方向，0 为行，1 为列
- `index`: 要删除的行索引，如果要删除多个，传入列表
- `columns`: 要删除的列索引，如果要删除多个，传入列表
- `inplace`: `inplace=True` 时，对原数据操作，返回 `None`

```Python
import pandas as pd
df = pd.DataFrame([[1, 2], [3, 4], [5, 6]], index=['n1', 'n2', 'n3'], columns=['a','b'])
print(df)
#     a  b
# n1  1  2
# n2  3  4
# n3  5  6
# 删除行索引为 'n2' 的数据行（两种等价写法）
print(df.drop(labels='n2', axis=0))
#     a  b
# n1  1  2
# n3  5  6
print(df.drop(index='n2'))
#     a  b
# n1  1  2
# n3  5  6
# 删除列索引为 'b' 的数据列（两种等价写法）
print(df.drop(labels='b', axis=1))
#     a
# n1  1
# n2  3
# n3  5
print(df.drop(columns='b'))
#     a
# n1  1
# n2  3
# n3  5
# 批量删除多行
print(df.drop(labels=['n2', 'n1'], axis=0))
#     a  b
# n3  5  6
print(df.drop(index=['n2', 'n1']))
#     a  b
# n3  5  6
# 批量删除所有列 → 返回空 DataFrame（但保留行索引）
print(df.drop(labels=['a', 'b'], axis=1))
# Empty DataFrame
# Columns: []
# Index: [n1, n2, n3]
print(df.drop(columns=['a', 'b']))
# Empty DataFrame
# Columns: []
# Index: [n1, n2, n3]
# inplace=True：直接修改原 DataFrame，返回 None（所以 print 输出的是修改后的 df）
df.drop(index='n1', inplace=True)
print(df)
#     a  b
# n2  3  4
# n3  5  6
```

### 7. 删除缺失值
`DataFrame.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)`
- `axis`: 0 表示删除包含缺失值的行，1 表示删除包含缺失值的列
- `how`: `'any'` 表示如果存在任何缺失值，则删除该行或列；`'all'` 表示如果所有值都是缺失值，则删除该行或列
- `thresh`: 只保留至少 n 个非 NaN 值的行或列，n 由该参数指定
- `subset`: 定义要根据哪些列（行）中的缺失值来删除行（列），和 `axis` 成行列对应关系
- `inplace`: 如果为 `True` 表示对原数据操作，返回 `None` 删除缺失值所在的行或列

```Python
import pandas as pd
import numpy as np
d = {'name': ['Tom', np.nan, 'Bob'], 'age': [np.nan, np.nan, 19], 'height': [177, 182, 179]}
df = pd.DataFrame(data=d)
print(df)
#   name   age  height
# 0  Tom   NaN     177
# 1  NaN   NaN     182
# 2  Bob  19.0     179
# 删除缺失值所在的行（默认：只要行中有任一 NaN 就删）
print(df.dropna())
#   name   age  height
# 2  Bob  19.0     179
# 删除缺失值所在的列（默认：只要列中有任一 NaN 就删）
print(df.dropna(axis=1))
#    height
# 0     177
# 1     182
# 2     179
# 修改数据：将 df[2, 'age'] 也设为 NaN
df.loc[2, 'age'] = np.nan
print(df)
#   name  age  height
# 0  Tom  NaN     177
# 1  NaN  NaN     182
# 2  Bob  NaN     179
# 删除所有值都是缺失值的列（how='all'）
print(df.dropna(axis=1, how='all'))
#   name  height
# 0  Tom     177
# 1  NaN     182
# 2  Bob     179
# → 'age' 列全为 NaN，被删除
# 只保留至少2个非NaN值的列（thresh=2）
print(df.dropna(axis=1, thresh=2))
#   name  height
# 0  Tom     177
# 1  NaN     182
# 2  Bob     179
# → 'name' 有2个非NaN，'height' 有3个，'age' 有0个 → 删 'age'
# 根据 'name'、'height' 列中的缺失值来删除行（subset 指定关注的列）
print(df.dropna(subset=['name', 'height']))
#   name  age  height
# 0  Tom  NaN     177
# 2  Bob  NaN     179
# → 第1行 'name' 缺失，被删；'age' 是否缺失不影响
# 根据第1、2行（索引1,2）中的缺失值来删除列（axis=1 + subset=[1,2]）
print(df.dropna(axis=1, subset=[1, 2]))
#    height
# 0     177
# 1     182
# 2     179
# → 在行1和行2中：
#    'name': [NaN, Bob] → 有 NaN
#    'age':  [NaN, NaN] → 全 NaN
#    'height': [182, 179] → 无 NaN
# → 所以只保留 'height'
# 对原数据操作（inplace=True）
df.dropna(axis=1, inplace=True)
print(df)
#    height
# 0     177
# 1     182
# 2     179
```

### 8. 填充缺失值
`DataFrame.fillna(value=None, method=None, axis=None, inplace=False, limit=None)`
- `value`: 需要填充的数据
- `method`: 填充方式。`'pad'`/`'ffill'` 表示用前一个非缺失值去填充该缺失值；`'backfill'`/`'bfill'` 表示用后一个非缺失值填充该缺失值
- `axis`: 指定填充方向
- `inplace`: 如果为 `True` 表示对原数据操作，返回 `None`
- `limit`: 限制填充个数

```Python
import pandas as pd
import numpy as np
df = pd.DataFrame([[np.nan, 2, np.nan, 0],
                   [3, 4, np.nan, 1],
                   [np.nan, np.nan, np.nan, np.nan],
                   [np.nan, 3, np.nan, 4]],
                  columns=list("ABCD"))
print(df)
#      A    B   C    D
# 0  NaN  2.0 NaN  0.0
# 1  3.0  4.0 NaN  1.0
# 2  NaN  NaN NaN  NaN
# 3  NaN  3.0 NaN  4.0
# 用标量填充: 将所有 NaN 填充为 0
print(df.fillna(0))
#      A    B    C    D
# 0  0.0  2.0  0.0  0.0
# 1  3.0  4.0  0.0  1.0
# 2  0.0  0.0  0.0  0.0
# 3  0.0  3.0  0.0  4.0
# 用字典填充: 指定不同列的填充值
dic = {'A': 6, 'B': 7}
print(df.fillna(dic))
#      A    B   C    D
# 0  6.0  2.0 NaN  0.0
# 1  3.0  4.0 NaN  1.0
# 2  6.0  7.0 NaN  NaN
# 3  6.0  3.0 NaN  4.0
# 用另一个 DataFrame 填充（按行列标签对齐）
np.random.seed(3)
arr = np.random.randint(1, 10, size=(3, 5))
df2 = pd.DataFrame(arr, columns=list("CFAHB"))
print(df2)
#    C  F  A  H  B
# 0  9  4  9  9  1
# 1  6  4  6  8  7
# 2  1  5  8  9  2
print(df.fillna(df2))
#      A    B    C    D
# 0  9.0  2.0  9.0  0.0  # A←9, C←9（来自 df2）
# 1  3.0  4.0  6.0  1.0  # C←6
# 2  8.0  2.0  1.0  NaN  # A←8, B←2, C←1（df2 第2行）
# 3  NaN  3.0  NaN  4.0  # df2 无 index=3，无法填充
# ⚠️ FutureWarning！推荐改用 .ffill() / .bfill()
# 用前一个非缺失值填充（向下填充，axis=0）
print(df.ffill())  # 替代 fillna(method='ffill')
#      A    B   C    D
# 0  NaN  2.0 NaN  0.0
# 1  3.0  4.0 NaN  1.0
# 2  3.0  4.0 NaN  1.0
# 3  3.0  3.0 NaN  4.0
# 用后一个非缺失值填充（向上填充，axis=0）
print(df.bfill())  # 替代 fillna(method='bfill')
#      A    B   C    D
# 0  3.0  2.0 NaN  0.0
# 1  3.0  4.0 NaN  1.0
# 2  NaN  3.0 NaN  4.0
# 3  NaN  3.0 NaN  4.0
# 沿列方向前向填充（从左到右）
print(df.ffill(axis=1))  # 替代 fillna(method='ffill', axis=1)
#      A    B    C    D
# 0  NaN  2.0  2.0  0.0
# 1  3.0  4.0  4.0  1.0
# 2  NaN  NaN  NaN  NaN
# 3  NaN  3.0  3.0  4.0
# 沿列方向后向填充（从右到左）
print(df.bfill(axis=1))  # 替代 fillna(method='bfill', axis=1)
#      A    B    C    D
# 0  2.0  2.0  0.0  0.0
# 1  3.0  4.0  1.0  1.0
# 2  NaN  NaN  NaN  NaN
# 3  3.0  3.0  4.0  4.0
# 指定列填充 + 限制每列最多填充 2 个
print(df.fillna({'A': 6, 'C': 7}, limit=2))
#      A    B    C    D
# 0  6.0  2.0  7.0  0.0  # A 和 C 被填充
# 1  3.0  4.0  7.0  1.0  # C 继续填充（第2个）
# 2  6.0  NaN  NaN  NaN  # A 填充（第2个），C 已达 limit=2，不再填
# 3  NaN  3.0  NaN  4.0  # A 已达 limit=2，不再填
```

### 9. 描述与统计
- `DataFrame.info(verbose=None, show_counts=None)`: 打印 DataFrame 的简明摘要。
    - `verbose`: 是否打印完整的摘要，为 `None` 时表示打印完整摘要，为 `False` 则打印简短摘要
    - `show_counts`: 是否显示 Non-Null Count，为 `None` 时表示显示，为 `False` 则不显示

```Python
import pandas as pd
import numpy as np
df = pd.DataFrame(data={'name': ['Tom', 'Bob', np.nan], 'age': [18, 19, 17], 'height': [167, 177, 178]}, index=['n1', 'n2', 'n3'])
print(df)
#    name  age  height
# n1  Tom   18     167
# n2  Bob   19     177
# n3  NaN   17     178
# 默认 info()：显示详细列信息，包括非空计数
df.info()
# <class 'pandas.core.frame.DataFrame'>
# Index: 3 entries, n1 to n3
# Data columns (total 3 columns):
#  #   Column  Non-Null Count  Dtype 
# ---  ------  --------------  ----- 
#  0   name    2 non-null      object
#  1   age     3 non-null      int64 
#  2   height  3 non-null      int64 
# dtypes: int64(2), object(1)
# memory usage: 96.0+ bytes
# verbose=False：不显示每列详情，只显示总列数
df.info(verbose=False)
# <class 'pandas.core.frame.DataFrame'>
# Index: 3 entries, n1 to n3
# Columns: 3 entries, name to height
# dtypes: int64(2), object(1)
# memory usage: 96.0+ bytes
# show_counts=False：显示列信息但隐藏“Non-Null Count”
df.info(show_counts=False)
# <class 'pandas.core.frame.DataFrame'>
# Index: 3 entries, n1 to n3
# Data columns (total 3 columns):
#  #   Column  Dtype 
# ---  ------  ----- 
#  0   name    object
#  1   age     int64 
#  2   height  int64 
# dtypes: int64(2), object(1)
# memory usage: 96.0+ bytes
```

- `DataFrame.describe(percentiles=None, include=None, exclude=None)`: 返回描述性统计。
    - `percentiles`: 默认值为 `[.25, .5, .75]`，它返回第 25、第 50 和第 75 个百分位数
    - `include`: 包含在结果中的数据类型；默认 `None` 表示结果将包括所有数字列；`'all'` 表示包括所有列；`'number'` 表示包括所有数字列；`'object'` 表示包括所有字符列
    - `exclude`: 不包含在结果中的数据类型；默认 `None` 表示结果不会排除任何列；`'number'` 表示不包括所有数字列；`'object'` 表示不包括所有字符列

```Python
import pandas as pd
df = pd.DataFrame(data={'name': ['Tom', 'Bob', 'Bob'],'age': [18, 19, 17], 'height': [167, 177, 178]}, index=['n1', 'n2', 'n3'])
print(df)
#    name  age  height
# n1  Tom   18     167
# n2  Bob   19     177
# n3  Bob   17     178
# 默认 describe()：仅对数值列（int/float）进行统计
print(df.describe())
#         age      height
# count   3.0    3.000000
# mean   18.0  174.000000
# std     1.0    6.082763
# min    17.0  167.000000
# 25%    17.5  172.000000
# 50%    18.0  177.000000
# 75%    18.5  177.500000
# max    19.0  178.000000
# include='all'：同时包含数值列和非数值列（如 object）
print(df.describe(include='all'))
#        name   age      height
# count     3   3.0    3.000000
# unique    2   NaN         NaN   ← 分类统计（name 列）
# top     Bob   NaN         NaN   ← 出现最频繁的值
# freq      2   NaN         NaN   ← 最频繁值的出现次数
# mean    NaN  18.0  174.000000   ← 数值统计（age, height）
# std     NaN   1.0    6.082763
# min     NaN  17.0  167.000000
# 25%     NaN  17.5  172.000000
# 50%     NaN  18.0  177.000000
# 75%     NaN  18.5  177.500000
# max     NaN  19.0  178.000000
# include='object'：只对 object 类型列进行描述
print(df.describe(include='object'))
#        name
# count     3    ← 非空值数量
# unique    2    ← 唯一值个数（'Tom', 'Bob'）
# top     Bob    ← 最常见值
# freq      2    ← 最常见值出现次数
# include=['number', 'object']：显式指定要包含的数据类型
print(df.describe(include=['number', 'object']))
#        name   age      height
# count     3   3.0    3.000000
# unique    2   NaN         NaN
# top     Bob   NaN         NaN
# freq      2   NaN         NaN
# mean    NaN  18.0  174.000000
# std     NaN   1.0    6.082763
# min     NaN  17.0  167.000000
# 25%     NaN  17.5  172.000000
# 50%     NaN  18.0  177.000000
# 75%     NaN  18.5  177.500000
# max     NaN  19.0  178.000000
```

- `DataFrame.count(axis=0)`: 返回指定轴的非缺失值的数量
- `DataFrame.max(axis=0)`: 返回指定轴的最大值
- `DataFrame.min(axis=0)`: 返回指定轴的最小值
- `DataFrame.mean(axis=0)`: 返回指定轴的平均值
- `DataFrame.var(axis=0)`: 返回指定轴的方差
- `DataFrame.std(axis=0)`: 返回指定轴的标准差

```Python
import pandas as pd
import numpy as np
df = pd.DataFrame(data={'name': ['Tom', np.nan, 'Linda'], 'age': [18, 19, 17]}, index=['n1', 'n2', 'n3'])
print(df)
print(df.count())
print(df.count(axis=1))
d = np.random.normal(size=(7, 2))
df = pd.DataFrame(data=d)
print(df)
print(df.max(axis=0)) # 返回每列最大值
print(df.max(axis=1)) # 返回每行最大值
print(df.min(axis=0)) # 返回每列最小值
print(df.min(axis=1)) # 返回每行最小值
print(df.mean(axis=0)) # 返回每列平均值
print(df.mean(axis=1)) # 返回每行平均值
print(df.var(axis=0)) # 返回每列方差
print(df.var(axis=1)) # 返回每行方差
print(df.std(axis=0)) # 返回每列标准差
print(df.std(axis=1)) # 返回每行标准差
```

### 10. 采样
`DataFrame.sample(n=None, frac=None, replace=False, random_state=None, axis=None)`  
从指定的轴返回随机样本。
- `n`: 默认为 1，表示要采样的行数或列数，不能和 `frac` 参数一起使用
- `frac`: 表示要采用的比例，不能和 `n` 参数一起使用
- `replace`: 表示是否有放回采样
- `random_state`: 随机数种子
- `axis`: 表示采样的方向，默认为 0，行采样

```Python
import pandas as pd
df = pd.DataFrame(data={'name': ['Tom', 'Bob', 'Jack', 'Linda'], 'age': [18, 19, 17, 21], 'height': [167, 177, 178, 188]}, index=['n1', 'n2', 'n3', 'n4'])
print(df)
#      name  age  height
# n1    Tom   18     167
# n2    Bob   19     177
# n3   Jack   17     178
# n4  Linda   21     188
# 默认 n=1，随机采样一行数据
print(df.sample())
#    name  age  height
# n2  Bob   19     177
# 随机采样 75% 的数据（4 × 0.75 = 3 行）
print(df.sample(frac=0.75))
#      name  age  height
# n3   Jack   17     178
# n2    Bob   19     177
# n4  Linda   21     188
# 随机采样 2 行数据
print(df.sample(n=2))
#    name  age  height
# n3  Jack   17     178
# n1   Tom   18     167
# 有放回采样（replace=True）：可能重复
print(df.sample(n=2, replace=True))
#    name  age  height
# n1  Tom   18     167
# n1  Tom   18     167  ← 同一行被抽中两次！
# 随机采样 2 列数据（axis=1）
print(df.sample(n=2, axis=1))
#      name  height
# n1    Tom     167
# n2    Bob     177
# n3   Jack     178
# n4  Linda     188
# 设置随机种子（random_state=3），确保结果可复现
print(df.sample(n=2, random_state=3))
#      name  age  height
# n4  Linda   21     188
# n2    Bob   19     177
```

### 11. 去重
`DataFrame.drop_duplicates(subset=None, keep='first', inplace=False)`  
返回去重（删除重复行）之后的 DataFrame。
- `subset`: 表示要进行去重的列名，默认为 `None`，表示所有列
- `keep`: 保留哪些副本。`'first'` 表示只保留第一次出现的重复项，删除其余重复项；`'last'` 表示只保留最后一次出现的重复项；`False` 则表示删除所有重复项
- `inplace`: `False` 表示删除重复项后返回一个副本；`True` 表示直接在原数据上删除重复项

```Python
import pandas as pd
d = {'A': [1, 3, 3, 1], 'B':[0, 2, 5, 0], 'C': [4, 0, 4, 4], 'D':[1, 0, 0, 1]}
df = pd.DataFrame(data=d)
print(df)
#    A  B  C  D
# 0  1  0  4  1   ← 第0行
# 1  3  2  0  0
# 2  3  5  4  0
# 3  1  0  4  1   ← 第3行（与第0行完全相同）
# 默认 keep='first'：保留第一次出现的重复项，删除后续重复 → 删除第3行
print(df.drop_duplicates())
#    A  B  C  D
# 0  1  0  4  1
# 1  3  2  0  0
# 2  3  5  4  0
# keep='last'：保留最后一次出现的重复项 → 删除第0行
print(df.drop_duplicates(keep='last'))
#    A  B  C  D
# 1  3  2  0  0
# 2  3  5  4  0
# 3  1  0  4  1
# keep=False：所有重复项都删除（只要某行有重复，全部删掉）
print(df.drop_duplicates(keep=False))
#    A  B  C  D
# 1  3  2  0  0
# 2  3  5  4  0
# → 第0行和第3行互为重复，全部被删
# 按指定列 ['A', 'D'] 去重（只看这两列是否重复）
# 行1: (3,0), 行2: (3,0) → 重复
# 行0: (1,1), 行3: (1,1) → 重复
# keep='last' → 保留每组最后出现的行（行2 和 行3）
print(df.drop_duplicates(subset=['A', 'D'], keep='last'))
#    A  B  C  D
# 2  3  5  4  0   ← 保留 (3,0) 的最后一行（原索引2）
# 3  1  0  4  1   ← 保留 (1,1) 的最后一行（原索引3）
# inplace=True：直接修改原 DataFrame
df.drop_duplicates(subset=['A', 'D'], keep='last', inplace=True)
print(df)
#    A  B  C  D
# 2  3  5  4  0
# 3  1  0  4  1
```

### 12. 排序
`DataFrame.sort_values(by, axis=0, ascending=True, inplace=False, na_position='last')`
- `by`: 要排序的名称或名称列表。如果 `axis=0` 或 `'index'`，`by` 可指定列标签；如果 `axis=1` 或 `'columns'`，`by` 可指定行标签
- `axis`: 要排序的轴，可选择 0 或 `'index'`, 1 或 `'columns'`
- `ascending`: `False` 则为降序；如果这是一个 bool 列表，则必须匹配 `by` 的长度
- `inplace`: 是否原地操作
- `na_position`: 设置缺失值的排序位置，`'first'` 表示开头，`'last'` 表示结尾

```Python
import pandas as pd
import numpy as np
df = pd.DataFrame({'col1': [4, 1, 2, np.nan, 5, 2],
                   'col2': [2, 1, 9, 8, 7, 6],
                   'col3': [0, 1, 9, 4, 2, 3],
                   'col4': ['a', 'B', 'c', 'D', 'e', 1]})
print(df)
#    col1  col2  col3 col4
# 0   4.0     2     0    a
# 1   1.0     1     1    B
# 2   2.0     9     9    c
# 3   NaN     8     4    D
# 4   5.0     7     2    e
# 5   2.0     6     3    1
# 按 'col1' 升序排序（默认），NaN 在最后
print(df.sort_values(by=['col1']))
#    col1  col2  col3 col4
# 1   1.0     1     1    B
# 2   2.0     9     9    c
# 5   2.0     6     3    1
# 0   4.0     2     0    a
# 4   5.0     7     2    e
# 3   NaN     8     4    D
# 单列排序：by='col1' 等价于 by=['col1']
print(df.sort_values(by='col1'))
# （同上）
# 多列排序：先按 col1，再按 col2（默认升序）
print(df.sort_values(by=['col1', 'col2']))
#    col1  col2  col3 col4
# 1   1.0     1     1    B
# 5   2.0     6     3    1   ← col1=2 时，col2=6 < 9
# 2   2.0     9     9    c
# 0   4.0     2     0    a
# 4   5.0     7     2    e
# 3   NaN     8     4    D
# 按第5行（索引5）的值对**列**进行排序（axis=1）
print(df.sort_values(by=5, axis=1))
#   col4  col1  col3  col2
# 0    a   4.0     0     2
# 1    B   1.0     1     1
# 2    c   2.0     9     9
# 3    D   NaN     4     8
# 4    e   5.0     2     7
# 5    1   2.0     3     6
# → 第5行值：col4=1, col1=2, col3=3, col2=6 → 升序排列列
# 按第5行降序排列列
print(df.sort_values(by=5, axis=1, ascending=False))
#   col2  col3  col1 col4
# 0     2     0   4.0    a
# 1     1     1   1.0    B
# 2     9     9   2.0    c
# 3     8     4   NaN    D
# 4     7     2   5.0    e
# 5     6     3   2.0    1
# 多列不同排序方向：col1 升序，col2 降序
print(df.sort_values(['col1', 'col2'], ascending=[True, False]))
#    col1  col2  col3 col4
# 1   1.0     1     1    B
# 2   2.0     9     9    c   ← col1=2 时，col2=9 > 6
# 5   2.0     6     3    1
# 0   4.0     2     0    a
# 4   5.0     7     2    e
# 3   NaN     8     4    D
# 将 NaN 放在最前面
print(df.sort_values(by='col1', na_position='first'))
#    col1  col2  col3 col4
# 3   NaN     8     4    D   ← NaN 在最前
# 1   1.0     1     1    B
# 2   2.0     9     9    c
# 5   2.0     6     3    1
# 0   4.0     2     0    a
# 4   5.0     7     2    e
# 原地排序（修改原 DataFrame）
df.sort_values(by='col1', inplace=True)
print(df)
#    col1  col2  col3 col4
# 1   1.0     1     1    B
# 2   2.0     9     9    c
# 5   2.0     6     3    1
# 0   4.0     2     0    a
# 4   5.0     7     2    e
# 3   NaN     8     4    D
```

### 13. 应用函数
`DataFrame.apply(func, axis=0)`  
沿着给定的 DataFrame 轴应用 `func` 的结果。
- `func`: 应用于每一个列或行的函数
- `axis`: 0 or `'index'` 表示函数处理的是每一列；1 or `'columns'` 表示函数处理的是每一行

```Python
import pandas as pd
import numpy as np
d = [[1, 2, 0], [4, 1, 9], [2, 5, 7], [4, 3, 6]]
df = pd.DataFrame(d, columns=['A', 'B', 'C'])
print(df)
#    A  B  C
# 0  1  2  0
# 1  4  1  9
# 2  2  5  7
# 3  4  3  6
# 默认 axis=0：对每一列应用 np.sum → 计算每列的总和
print(df.apply(np.sum))
# A    11   ← 1+4+2+4
# B    11   ← 2+1+5+3
# C    22   ← 0+9+7+6
# dtype: int64
# axis=1：对每一行应用 np.sum → 计算每行的总和
print(df.apply(np.sum, axis=1))
# 0     3   ← 1+2+0
# 1    14   ← 4+1+9
# 2    14   ← 2+5+7
# 3    13   ← 4+3+6
# dtype: int64
```

### 14. 分组 (Groupby)
`DataFrame.groupby(by=None, as_index=True, sort=True, dropna=True)`  
返回一个包含分组信息的 DataFrameGroupBy 对象。
- `by`: 指定根据哪个或者哪些标签分组
- `as_index`: 对于聚合操作的输出结果，默认将分组列的值作为索引，如果将 `as_index` 设置为 `False`，可以重置索引 (0, 1, 2...)
- `sort`: 结果按分组标签的值升序排列，设置为 `False` 则不排序
- `dropna`: 默认为 `True` 时，分组标签那列的 NaN 在分组结果中不保留，设置为 `False`，可以保留 NaN 分组

```Python
import pandas as pd
import numpy as np
d={
    'company': ['A', 'B', 'A', 'C', 'C', 'B', 'C', 'A'],
    'salary': [8, 15, 10, 15, np.nan, 28, 30, 15],
    'age': [26, 29, 26, 30, 50, 30, 30, 35]
}
df = pd.DataFrame(data=d)
print(df)
# 根据'company'列的数据对行分组, 返回DataFrameGroupBy的实例对象
df_gb = df.groupby(by='company', as_index=False)
# 该实例对象是iterable, 迭代操作可以得到各个分组
for g, data in df_gb:
    print(g)
    print(data)
""" DataFrameGroupBy相关属性 """
print(df_gb.ngroups) # 分成了几组
print(df_gb.groups) # 各个分组的index
print(df_gb.indices) # 各个分组的index
""" DataFrameGroupBy相关方法 """
# 获取指定组的数据
print(df_gb.get_group('A'))
print(df_gb.get_group('B'))
print(df_gb.get_group('C'))
# 聚合操作(对各个组的数据分别操作)
print(df_gb.agg('mean'))
print(df_gb.agg(np.mean))
print(df_gb.agg('max'))
print(df_gb.agg('min'))
print(df_gb.agg('sum'))
print(df_gb.agg('median'))
print(df_gb.agg('std'))
print(df_gb.agg('var'))
print(df_gb.agg('count'))
# 变换操作(在聚合操作的结果之上, 还将值变换到分组前的对应位置上)
print(df_gb.transform('mean'))
print(df_gb.transform(np.mean))
# 新增两列数据
df[['avg_salary', 'avg_age']] = df_gb.transform('mean')
print(df)
# 可以包含NaN分组, 例如:
# df_gb = df.groupby(by='salary', dropna=False)
# 也可以根据多列数据对行分组, 例如:
# df_gb = df.groupby(by=['age', 'company'])
```

---
## 五、 DataFrame 的运算
DataFrame 保留了 NumPy 中的数组运算，且 DataFrame 进行数组运算的时候，索引与值之间的映射关系不会发生改变。在进行 DataFrame 和 DataFrame 的运算时，把两个 DataFrame 中行索引名和列索引名一样的值进行运算，其他不一样的做并集且对应的值为 NaN。

```Python
import pandas as pd
import numpy as np
d = np.arange(9).reshape((3, 3))
df1 = pd.DataFrame(data=d, columns=list('abc'), index=['n1', 'n2', 'n3'])
print(df1)
print(df1 + 1)
print(df1 - 1)
print(df1 * 2)
print(df1 / 2)
d = np.arange(16).reshape((4, 4))
df2 = pd.DataFrame(data=d, columns=list('dacf'), index=['n1', 'n2', 'n3', 'n4'])
print(df2)
print(df1 + df2)
print(df1 - df2)
print(df1 * df2)
print(df1 / df2)
```

---
## 六、 Pandas 文件读写
### 1. CSV 文件读写

```Python
import pandas as pd
import numpy as np
df = pd.read_csv('./test01.csv')
print(df)
# sep参数默认为逗号(test02.csv文件是用分号分隔)
df = pd.read_csv('./test02.csv', sep=';')
print(df)
# header参数默认自行推断, 会把第一行数据作为列索引(表头)
# 如果不想使用数据为列索引, 可设置为None, 那么列索引就会是(0, 1...)
df = pd.read_csv('./test03.csv', sep=';', header=None)
print(df)
# header=2, 指定第3行数据作为列索引(表头), 之后的行才为数据
df = pd.read_csv('./test03.csv', sep=';', header=2)
print(df)
# names参数可以指定列索引, 如果指定names, 则header推断为None
df = pd.read_csv('./test02.csv', sep=';', names=['name', 'age', 'height'])
print(df)
# 读取大文件片段
# nrows参数用来读取指定行数的数据:这里读取前两行数据(header先推断再读取)
df = pd.read_csv('./test01.csv', nrows=2)
print(df)
# skiprows参数用来指定需要跳过的行(先跳过, header再推断)
# 当skiprows为整数时, 表示跳过对应的前几行:这里跳过前两行
df = pd.read_csv('./test01.csv', skiprows=2)
print(df)
# 当skiprows为索引时, 表示跳过对应的索引行:这里跳过第1行和第3行
df = pd.read_csv('./test01.csv', skiprows=[0, 2])
print(df)
# usecols参数用来读取指定列的数据:这里读取第1列和第3列
df = pd.read_csv('./test01.csv', usecols=[0, 2])
print(df)
# chunksize参数指定时, read_csv会返回TextFileReader对象
# TextFileReader对象是个迭代器, 可以按照chunksize迭代
obj = pd.read_csv('./test01.csv', chunksize=2)
for i in obj:
    print(i)
```

**写入 CSV 文件：**

```Python
import pandas as pd
d = {
    '名字': ['张三', '李四', '王五', '赵六', '孙七'],
    '年龄': [18, 19, 20, 22, 17],
    '身高': [188, 178, 189, 175, 177]
}
df = pd.DataFrame(data=d)
print(df)
# 把DataFrame写入csv文件
# sep参数默认为逗号, 所以文件中分隔符为逗号
# index参数默认为True, 所以行索引也被写入了文件
# header参数默认为True, 所以列索引也被写入了文件
df.to_csv('./test04.csv')
# 可以给sep参数指定其他的分隔符(分隔符必须是一个字符)
df.to_csv('./test05.csv', sep=';')
# 如果不想把行索引写入文件可以把index参数指定为False
df.to_csv('./test06.csv', index=False)
# 如果不想把列索引写入文件可以把header参数指定为False
df.to_csv('./test07.csv', header=False)
```

### 2. EXCEL 文件读写
**写入 EXCEL 文件：**

```Python
import pandas as pd
d = {
    '名字': ['张三', '李四', '王五', '赵六', '孙七'],
    '年龄': [18, 19, 20, 22, 17],
    '身高': [188, 178, 189, 175, 177]
}
df = pd.DataFrame(data=d)
print(df)
# 把DataFrame写入excel文件
# index参数默认为True, 所以行索引也被写入了文件
# header参数默认为True, 所以列索引也被写入了文件
df.to_excel('./test08.xlsx')
# 如果不想把行索引写入文件可以把index参数指定为False
df.to_excel('./test09.xlsx', index=False)
# 如果不想把列索引写入文件可以把header参数指定为False
df.to_excel('./test10.xlsx', header=False)
# 把DataFrame写入excel文件，多工作表
writer = pd.ExcelWriter('./test11.xlsx')
# 写入工作表1
df.to_excel(writer, sheet_name='工作表1', index=False)
# 写入工作表2
df.iloc[:, :2].to_excel(writer, sheet_name='工作表2', index=False)
writer.close()
# with语句更优雅
with pd.ExcelWriter('./test11.xlsx') as writer:
    df.to_excel(writer, sheet_name='工作表1', index=False)
    df.iloc[:, :2].to_excel(writer, sheet_name='工作表2', index=False)
```

**读取 EXCEL 文件：**

```Python
import pandas as pd
# header参数默认为0, 会把第一行作为列索引(表头)
df = pd.read_excel('./test11.xlsx')
print(df)
# 如果不想使用数据为列索引, 可设置为None, 那么列索引就会是(0, 1...)
df = pd.read_excel('./test11.xlsx', header=None)
print(df)
# header=2, 指定第3行数据作为列索引(表头), 之后的行才为数据
df = pd.read_excel('./test11.xlsx', header=2)
print(df)
# names参数可以指定列索引(表头)
# 因为header为默认值0, 第一行会被names参数指定的值覆盖掉
df = pd.read_excel('./test11.xlsx', names=['name', 'age', 'height'])
print(df)
# 因为header为None, 第一行仍会当作数据
df = pd.read_excel('./test11.xlsx', header=None, names=['name', 'age', 'height'])
print(df)
# sheet_name指定要读取的工作表
# 如果为整数, 则为工作表的索引;默认为0, 表示读取第一个工作表
df = pd.read_excel('./test11.xlsx', sheet_name=1)
print(df)
# 如果为字符串, 则为工作表的名称
df = pd.read_excel('./test11.xlsx', sheet_name='工作表2')
print(df)
# 如果想要读取多个工作表, 可以指定为列表
df = pd.read_excel('./test11.xlsx', sheet_name=[0, '工作表2'])
print(df)
# 读取大文件片段
df = pd.read_excel('./test11.xlsx', nrows=2)
print(df)
df = pd.read_excel('./test11.xlsx', skiprows=2)
print(df)
df = pd.read_excel('./test11.xlsx', skiprows=[0, 2])
print(df)
df = pd.read_excel('./test11.xlsx', usecols=[0, 2])
print(df)
```