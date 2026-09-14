---
title: "N-Gram、长度规范与文本数据增强（N-Gram, Length Normalization, and Text Augmentation）"
tags:
  - data-science/nlp
status: published
created: 2026-08-13
published_at: 2026-08-13
---
# N-Gram、长度规范与文本数据增强（N-Gram, Length Normalization, and Text Augmentation）

## 文本特征处理
### 1 什么是n-gram特征

- 给定一段文本序列, 其中n个词或字的相邻共现特征即n-gram特征, 常用的n-gram特征是bi-gram和tri-gram特征, 分别对应n为2和3.
- 举个例子:

```text
假设给定分词列表: ["是谁", "敲动", "我心"]

对应的数值映射列表为: [1, 34, 21]

我们可以认为数值映射列表中的每个数字是词汇特征.

除此之外, 我们还可以把"是谁"和"敲动"两个词共同出现且相邻也作为一种特征加入到序列列表中,

假设1000就代表"是谁"和"敲动"共同出现且相邻

此时数值映射列表就变成了包含2-gram特征的特征列表: [1, 34, 21, 1000]

这里的"是谁"和"敲动"共同出现且相邻就是bi-gram特征中的一个.

"敲动"和"我心"也是共现且相邻的两个词汇, 因此它们也是bi-gram特征.

假设1001代表"敲动"和"我心"共同出现且相邻

那么, 最后原始的数值映射列表 [1, 34, 21] 添加了bi-gram特征之后就变成了 [1, 34, 21, 1000, 1001]
```

- 提取n-gram特征:

```python
# 一般n-gram中的n取2或者3, 这里取2为例
ngram_range = 2

def create_ngram_set(input_list):
    """
    description: 从数值列表中提取所有的n-gram特征
    :param input_list: 输入的数值列表, 可以看作是词汇映射后的列表,
                       里面每个数字的取值范围为[1, 25000]
    :return: n-gram特征组成的集合

    eg:
    >>> create_ngram_set([1, 3, 2, 1, 5, 3])
    {(3, 2), (1, 3), (2, 1), (1, 5), (5, 3)}
    """
    return set(zip(*[input_list[i:] for i in range(ngram_range)]))
```

- 调用:

```text
input_list = [1, 3, 2, 1, 5, 3]
res = create_ngram_set(input_list)
print(res)
```

> - 输出效果:

```text
# 该输入列表的所有bi-gram特征
{(3, 2), (1, 3), (2, 1), (1, 5), (5, 3)}
```

### 2 文本长度规范及其作用

- 一般模型的输入需要等尺寸大小的矩阵, 因此在进入模型前需要对每条文本数值映射后的长度进行规范, 此时将根据句子长度分布分析出覆盖绝大多数文本的合理长度, 对超长文本进行截断, 对不足文本进行补齐(一般使用数字0), 这个过程就是文本长度规范.
- 文本长度规范的实现:

```python
from tensorflow.keras.preprocessing import sequence

# cutlen根据数据分析中句子长度分布，覆盖90%左右语料的最短长度.
# 这里假定cutlen为10
cutlen = 10

def padding(x_train):
    """
    description: 对输入文本张量进行长度规范
    :param x_train: 文本的张量表示, 形如: [[1, 32, 32, 61], [2, 54, 21, 7, 19]]
    :return: 进行截断补齐后的文本张量表示
    """
    # 使用sequence.pad_sequences即可完成
    return sequence.pad_sequences(x_train, cutlen)
```

> - 调用:

```text
# 假定x_train里面有两条文本, 一条长度大于10, 一天小于10
x_train = [[1, 23, 5, 32, 55, 63, 2, 21, 78, 32, 23, 1],
           [2, 32, 1, 23, 1]]

res = padding(x_train)
print(res)
```

> - 输出效果:

```text
[[ 5 32 55 63  2 21 78 32 23  1]
 [ 0  0  0  0  0  2 32  1 23  1]]
```

## 文本数据增强（Text Data Augmentation）
### 1 回译数据增强法

- 回译数据增强目前是文本数据增强方面效果较好的增强方法, 一般基于google、有道等翻译接口, 将文本数据翻译成另外一种语言(一般选择小语种),之后再翻译回原语言, 即可认为得到与与原语料同标签的新语料, 新语料加入到原数据集中即可认为是对原数据集数据增强.
- 回译数据增强优势:
  - 操作简便, 获得新语料质量高.
- 回译数据增强存在的问题:
  - 在短文本回译过程中, 新语料与原语料可能存在很高的重复率, 并不能有效增大样本的特征空间.
- 高重复率解决办法:
  - 进行连续的多语言翻译, 如: 中文→韩文→日语→英文→中文, 根据经验, 最多只采用3次连续翻译, 更多的翻译次数将产生效率低下, 语义失真等问题.
- 回译数据增强实现（基于有道翻译接口）:

```python
# 导入必备的工具包
import requests

# 思路分析
# 1 定义需要访问的有道翻译API接口--url
# 2 定义需要翻译的文本：text
# 3 定义data数据：from代表原始语言, to代表目标语言, i代表需要翻译的文本, doctype:文本的类型
# 4 requests.post(url=url, params=data)即代表访问api接口的方法

def dm_translate():
    url = 'http://fanyi.youdao.com/translate'
    # 第一次翻译，目标语言英文
    text1 = '这个价格非常便宜'
    data1 = {'from': 'zh-CHS', 'to': 'en', 'i': text1, 'doctype': 'json'}
    response1 = requests.post(url=url, params=data1)
    res1 = response1.json()
    # 打印第一次翻译结果
    print(res1)

    # 第二次翻译， 目标语言中文
    text2 = 'The price is very cheap'
    data2 = {'from': 'en', 'to': 'zh-CHS', 'i': text2, 'doctype': 'json'}
    response2 = requests.post(url=url, params=data2)
    res2 = response2.json()
    # 打印第二次翻译结果
    print(res2)
```

输出结果展示:

```text
第一次翻译结果：{'type': 'ZH_CN2EN', 'errorCode': 0, 'elapsedTime': 1, 'translateResult': [[{'src': '这个价格非常便宜', 'tgt': 'The price is very cheap'}]]}

第二次翻译结果：{'type': 'EN2ZH_CN', 'errorCode': 0, 'elapsedTime': 1, 'translateResult': [[{'src': 'The price is very cheap', 'tgt': '价格非常便宜'}]]}
```

语言及其对应编码：

```text
'AUTO': '自动检测语言'
'zh-CHS': '中文',
'en': '英文'
'ja': '日语'
'ko': '韩语'
'fr': '法语'
'de': '德语'
```
