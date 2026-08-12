---
title: "Jieba 中文分词、词典、关键词与词性（Jieba Tokenization and Keywords）"
tags:
  - data-science/nlp/jieba
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# Jieba 中文分词、词典、关键词与词性（Jieba Tokenization and Keywords）
> [!tip] 大白话理解（Plain-language Intuition）
> Jieba 会先用前缀词典（Prefix Dictionary）列出一句话可能怎样切词，形成有向无环图（Directed Acyclic Graph, DAG），再用动态规划（Dynamic Programming）选择整体概率较高的路径；词典里没有的片段可交给隐马尔可夫模型（Hidden Markov Model, HMM）尝试识别。自定义词频改变的正是候选路径的权重，因此可能连带影响相邻词的切分。
## Notebook 环境与转换说明（Notebook Environment and Conversion）
- **内核显示名（Kernel Display Name）**：`ShenLan`。
- **语言（Language）**：`python`。
- **内核名称（Kernel Name）**：`python3`。
- **单元数量（Cell Count）**：42。
- Markdown 单元、代码单元、执行序号与已保存文本输出全部按原顺序保留；外部文件路径仍需在运行环境中提供。
## 单元 1：代码（Code Cell）
- **原执行序号（Execution Count）**：`2`。
```python
#引入jieba模块, 默认安装pip install jieba
import jieba

# 基本使用
word_list = jieba.cut("欢迎来到NLP自然语言的世界!")
print(type(word_list))
print("【基本应用】: {}".format(" / ".join(word_list)))

# 期望输出（来自 Notebook 已保存输出）:
# Building prefix dict from the default dictionary ...
# <class 'generator'>
# Dumping model to file cache /var/folders/53/dnds1kp165781h18s6qmkpsm0000gn/T/jieba.cache
# Loading model cost 0.783 seconds.
# Prefix dict has been built successfully.
# 【基本应用】: 欢迎 / 来到 / NLP / 自然语言 / 的 / 世界 / !
```
## 单元 2：说明（Markdown Cell）
## 一、分词
## 单元 3：代码（Code Cell）
- **原执行序号（Execution Count）**：`6`。
```python
# 导入包
import jieba

word_list = jieba.cut('我来到湖南国防科技大学', cut_all=True)
print("【全模式】: {}".format(" /".join(word_list)))

word_list = jieba.cut('我来到湖南国防科技大学')
print("【精确模式】: {}".format(" /".join(word_list)))

word_list = jieba.cut_for_search('我来到湖南国防科技大学')
print("【搜索引擎模式】: {}".format(" /".join(word_list)))


word_list = jieba.cut("我在台电大厦上班", HMM=False)
print("【仅词典模式】: {}".format(" /".join(word_list)))

word_list = jieba.cut("我在台电大厦上班", HMM=True)
print("【HMM新词发现模式】: {}".format(" /".join(word_list)))

# 期望输出（来自 Notebook 已保存输出）:
# 【全模式】: 我 /来到 /湖南 /南国 /国防 /国防科 /国防科技 /国防科技大学 /科技 /大学
# 【精确模式】: 我 /来到 /湖南 /国防科技大学
# 【搜索引擎模式】: 我 /来到 /湖南 /国防 /科技 /大学 /国防科 /国防科技大学
# 【仅词典模式】: 我 /在 /台 /电 /大厦 /上班
# 【HMM新词发现模式】: 我 /在 /台电 /大厦 /上班
```
## 单元 4：说明（Markdown Cell）
### API区别说明
- jieba.cut：返回的是一个迭代器对象
- jieba.lcut：返回的是一个list集合
## 单元 5：代码（Code Cell）
- **原执行序号（Execution Count）**：`3`。
```python
cut_word_list = jieba.cut('我来到湖南国防科技大学')
print("【cut API返回的数据类型】: {}".format(type(cut_word_list)))
print("【cut API返回结果】: {}".format(' /'.join(cut_word_list)))
print("【cut API返回结果<再次获取>】: {}".format(' /'.join(cut_word_list)))

print("")

lcut_word_list = jieba.lcut('我来到湖南国防科技大学')
print("【lcut API返回的数据类型】: {}".format(type(lcut_word_list)))
print("【lcut API返回结果】: {}".format(' /'.join(lcut_word_list)))
print("【lcut API返回结果<再次获取>】: {}".format(' /'.join(lcut_word_list)))

# 期望输出（来自 Notebook 已保存输出）:
# 【cut API返回的数据类型】: <class 'generator'>
# 【cut API返回结果】: 我 /来到 /湖南 /国防科技大学
# 【cut API返回结果<再次获取>】:
#
# 【lcut API返回的数据类型】: <class 'list'>
# 【lcut API返回结果】: 我 /来到 /湖南 /国防科技大学
# 【lcut API返回结果<再次获取>】: 我 /来到 /湖南 /国防科技大学
```
## 单元 6：说明（Markdown Cell）
## 二、自定义词典
## 单元 7：说明（Markdown Cell）
### 载入词典
```
jieba.load_userdict(filename): 加载给定文件filename中定义的单词
```
- 每一行分三部分：词语、词频（可省略）、词性（可省略），用空格隔开，顺序不可颠倒；
- 词性详见：<a href="#ext1">jieba词性说明</a>
## 单元 8：代码（Code Cell）
- **原执行序号（Execution Count）**：`4`。
```python
# 仅词典匹配
word_list = jieba.cut('外卖送餐公司中饿了么是你值得信赖的选择', HMM=False)
print("【载入词典前<无HMM>】: {}".format('/'.join(word_list)))

# 对于连续单独成词的文本，使用HMM继续分词
word_list = jieba.cut('外卖送餐公司中饿了么是你值得信赖的选择', HMM=True)
print("【载入词典前<有HMM>】: {}".format('/'.join(word_list)))

# 期望输出（来自 Notebook 已保存输出）:
# 【载入词典前<无HMM>】: 外卖/送/餐/公司/中/饿/了/么/是/你/值得/信赖/的/选择
# 【载入词典前<有HMM>】: 外卖/送餐/公司/中饿/了/么/是/你/值得/信赖/的/选择
```
## 单元 9：代码（Code Cell）
- **原执行序号（Execution Count）**：`5`。
```python
# 加载词典
jieba.load_userdict('./datas/word_dict.txt')
```
## 单元 10：代码（Code Cell）
- **原执行序号（Execution Count）**：`6`。
```python
with open('./datas/word_dict.txt', 'r', encoding='utf-8') as reader:
    for line in reader:
        print(line.strip())

# 期望输出（来自 Notebook 已保存输出）:
# #自定义词典：一词占一行，每行分三个部分：词语，词频（可忽略），词性（可忽略）
# 饿了么 2 nt
# 徐良才 2 nr
# 驻军官兵 2
```
## 单元 11：代码（Code Cell）
- **原执行序号（Execution Count）**：`7`。
```python
word_list = jieba.cut('外卖送餐公司中饿了么是你值得信赖的选择', HMM=False)
print("【载入词典后<无HMM>】: {}".format('/'.join(word_list)))

word_list = jieba.cut('外卖送餐公司中饿了么是你值得信赖的选择', HMM=True)
print("【载入词典后<有HMM>】: {}".format('/'.join(word_list)))

# 期望输出（来自 Notebook 已保存输出）:
# 【载入词典后<无HMM>】: 外卖/送/餐/公司/中/饿了么/是/你/值得/信赖/的/选择
# 【载入词典后<有HMM>】: 外卖/送餐/公司/中/饿了么/是/你/值得/信赖/的/选择
```
## 单元 12：说明（Markdown Cell）
### 动态调整词典
- 使用```add_word(word, freq=None, tag=None)```和```del_word(word)```可以在程序中动态修改词典
- 使用```suggest_freq(segment, tune=True)```可以调节单个词语的词频，使其能或者不能被分出来
## 单元 13：代码（Code Cell）
- **原执行序号（Execution Count）**：`8`。
```python
word_list = jieba.cut('如果放到post中将出错。', HMM=False)
print("【不启动HMM+不添加分词】: {}".format('/'.join(word_list)))

# 期望输出（来自 Notebook 已保存输出）:
# 【不启动HMM+不添加分词】: 如果/放到/post/中将/出错/。
```
## 单元 14：代码（Code Cell）
- **原执行序号（Execution Count）**：`9`。
```python
jieba.suggest_freq('中', tune=False)

# 期望输出（来自 Notebook 已保存输出）:
# 243191
```
## 单元 15：代码（Code Cell）
- **原执行序号（Execution Count）**：`10`。
```python
jieba.suggest_freq(('中', '将'), tune=True)

# 期望输出（来自 Notebook 已保存输出）:
# 494
```
## 单元 16：代码（Code Cell）
- **原执行序号（Execution Count）**：`11`。
```python
jieba.suggest_freq('中', tune=False)

# 期望输出（来自 Notebook 已保存输出）:
# 243192
```
## 单元 17：代码（Code Cell）
- **原执行序号（Execution Count）**：`12`。
```python
word_list = jieba.cut('如果放到post中将出错。', HMM=False)
print("【不启动HMM+添加分词】: {}".format('/'.join(word_list)))

# 期望输出（来自 Notebook 已保存输出）:
# 【不启动HMM+添加分词】: 如果/放到/post/中/将/出错/。
```
## 单元 18：说明（Markdown Cell）
## 三、关键词抽取
## 单元 19：代码（Code Cell）
- **原执行序号（Execution Count）**：`13`。
```python
import jieba.analyse
```
## 单元 20：代码（Code Cell）
- **原执行序号（Execution Count）**：`14`。
```python
# https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_10141364001547692745%22%7D&n_type=0&p_from=1
sentence = """
新华社澳门8月1日电（方钊、郭鑫）1日上午，解放军驻澳门部队在新口岸军营隆重举行升国旗仪式和“八一”招待会，庆祝中国人民解放军建军92周年。
8时，驻澳部队威武的仪仗队护送国旗，步伐铿锵走向升旗台。军乐队奏响雄壮的《中华人民共和国国歌》，驻澳门部队官兵在司令员徐良才和政委孙文举带领下整齐列队，面向国旗庄严敬礼，目送鲜艳的五星红旗冉冉升起，献上深情祝福。
“八一”招待会于11时举行，主礼嘉宾与各界来宾一同观看了纪录片《濠江战旗别样红》，全面了解驻军进澳门20年来履行防务情况。驻澳门部队司令员徐良才和澳门特区行政长官崔世安致辞。
徐良才深情回顾了中国人民解放军的光辉历程。他表示，今年是中国人民解放军进驻澳门20周年，驻军自进驻之日起，就坚定不移地贯彻“一国两制”伟大方针，坚定不移地遵守澳门基本法和驻军法，坚定不移地维护澳门繁荣稳定，始终视国家和民族利益高于一切，始终遵守澳门现行社会制度，尊重和支持特区政府依法施政，积极参加社会公益事业，把澳门同胞当亲人。
徐良才说，近年来，驻军官兵时刻牢记习主席重要嘱托，深入贯彻习近平强军思想，坚持政治建军、服务大局，坚持任务牵引、练兵备战，坚持依法从严、锤炼作风，部队履行防务能力稳步提升。驻军部队的建设发展，离不开特区各界和澳门同胞的关心，离不开中联办、外交公署等中央驻澳机构的支持，特别是特区政府为驻军有效履行防务创造了良好环境和条件，对此致以衷心的感谢和崇高的敬意。
崔世安向驻澳门部队官兵致以节日的祝贺，对驻军一直以来对特区发展的有力支持表示感谢。他表示，20年来，驻澳部队与澳门特区同呼吸、共命运，视驻地为故乡，把居民当亲人，支持特区政府依法施政，积极开展多元化的、丰富多彩的爱民活动，主动参与献血、植树等社会公益活动；与特区政府合办“澳门青年学生军事夏令营”，培养青年“爱国爱澳”的核心价值；在防灾救灾工作上，以高度的责任感，大力支持特区政府。事实证明，驻澳部队是维护“一国两制”的重要力量，是维护澳门繁荣稳定的重要基石，为澳门特区各项事业的进步作出了不懈的努力和巨大的贡献。
全国政协副主席何厚铧、中央政府驻澳门联络办公室主任傅自应、外交部驻澳门特派员公署特派员沈蓓莉、驻澳部队政委孙文举、澳门特区立法会主席高开贤等，以及澳门特区政府、中央驻澳机构、澳区全国人大代表、政协委员、社团、高校、往届军事夏令营学生代表等300余人出席了招待会。
"""
```
## 单元 21：说明（Markdown Cell）
### 基于TF-IDF算法抽取关键词
- ```jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())```
    - 功能：关键词提取
    - 参数说明：
        - sentence：待提取的文本
        - topK：返回多少个TF/IDF权重最大的关键词，默认为20个
        - withWeight：是否返回关键词的权重值，默认为False，表示不返回
        - allowPOS: 仅提取制定词性的词，默认为空，表示不筛选
- ```jieba.analyse.set_idf_path(file_name)```
    - 功能：自定义单词逆文件频率的值
    - 参数说明：
        - file_name: 本地磁盘文件路径，文件内容为各个单词的逆向文件频率，每行一个单词，两部分构成，第一部分为单词，第二部分为逆向文件频率，中间用空格隔开
    - 参考：[idf.txt.big](https://github.com/fxsjy/jieba/blob/master/extra_dict/idf.txt.big)
- ```jieba.analyse.set_stop_words(file_name)```
    - 功能：自定义停止词
    - 参数说明：
        - file_name: 本地磁盘文件路径, 每行一个停止词
    - 参考：[stop_words.txt](https://github.com/fxsjy/jieba/blob/master/extra_dict/stop_words.txt)
## 单元 22：代码（Code Cell）
- **原执行序号（Execution Count）**：`15`。
```python
jieba.analyse.extract_tags(sentence,topK=10)

# 期望输出（来自 Notebook 已保存输出）:
# ['澳门', '驻澳', '驻澳门部队', '特区政府', '驻军', '徐良才', '澳门特区', '20', '部队', '招待会']
```
## 单元 23：代码（Code Cell）
- **原执行序号（Execution Count）**：`16`。
```python
# 简单去看，内部就是计算一个TF-IDF = TF * IDF的值，然后排序
jieba.analyse.extract_tags(sentence,topK=10,withWeight=True)

# 期望输出（来自 Notebook 已保存输出）:
# [('澳门', 0.2831030211112844),
#  ('驻澳', 0.21935353216330275),
#  ('驻澳门部队', 0.17003887036085627),
#  ('特区政府', 0.1639544926850153),
#  ('驻军', 0.15160225656220183),
#  ('徐良才', 0.1462356881088685),
#  ('澳门特区', 0.1462356881088685),
#  ('20', 0.10967676608165138),
#  ('部队', 0.10377648176256882),
#  ('招待会', 0.0924040023440367)]
```
## 单元 24：代码（Code Cell）
- **原执行序号（Execution Count）**：`17`。
```python
jieba.analyse.extract_tags(sentence,topK=10,withWeight=True,
                           allowPOS=('n', 'ns','vn', 'a'))

# 期望输出（来自 Notebook 已保存输出）:
# [('澳门', 0.5714486907616666),
#  ('驻军', 0.30601196232000005),
#  ('澳门特区', 0.2951794445160494),
#  ('部队', 0.20947475022444442),
#  ('招待会', 0.1865191899166667),
#  ('防务', 0.1522948861057407),
#  ('文举', 0.14200965900246912),
#  ('依法', 0.13147027069444445),
#  ('公署', 0.11798607691506173),
#  ('建军', 0.11488342965234567)]
```
## 单元 25：代码（Code Cell）
- **原执行序号（Execution Count）**：`18`。
```python
# 设置自定义IDF文件
jieba.analyse.set_idf_path('./datas/idf.txt.big')
# 设置自定义停止词
jieba.analyse.set_stop_words('./datas/stop_words.txt')
# 再进行关键词提取
jieba.analyse.extract_tags(sentence,topK=10,withWeight=True,
                           allowPOS=('n', 'ns','vn', 'a'))

# 期望输出（来自 Notebook 已保存输出）:
# [('澳门', 0.5714486907616666),
#  ('部队', 0.4427691667740741),
#  ('驻军', 0.30601196232000005),
#  ('澳门特区', 0.2951794445160494),
#  ('防务', 0.22138458338703704),
#  ('依法', 0.22138458338703704),
#  ('主席', 0.22138458338703704),
#  ('招待会', 0.1865191899166667),
#  ('政委', 0.1475897222580247),
#  ('文举', 0.1475897222580247)]
```
## 单元 26：说明（Markdown Cell）
### 基于TextRank算法的关键词抽取
- ```jieba.analyse.textrank(sentence, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'), withFlag=False) ```
    - 功能：关键词提取
    - 参数说明：
        - sentence：待提取的文本
        - topK：返回多少个TF/IDF权重最大的关键词，默认为20个
        - withWeight：是否返回关键词的权重值，默认为False，表示不返回
        - allowPOS: 仅提取制定词性的词，默认不为空，表示进行筛选
        - withFlag：是否返回单词的词性值，默认为False，表示不返回(仅返回单词)
- NOTE: 参考[TextRank: Bringing Order into Texts](http://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf)论文
## 单元 27：代码（Code Cell）
- **原执行序号（Execution Count）**：`19`。
```python
jieba.analyse.textrank(sentence=sentence, topK=10)

# 期望输出（来自 Notebook 已保存输出）:
# ['澳门', '驻军', '部队', '澳门特区', '坚持', '支持', '防务', '履行', '国旗', '依法']
```
## 单元 28：代码（Code Cell）
- **原执行序号（Execution Count）**：`20`。
```python
jieba.analyse.textrank(sentence=sentence, topK=10, withWeight=True,
                       allowPOS=('n', 'ns','vn', 'v', 'a'), withFlag=True)

# 期望输出（来自 Notebook 已保存输出）:
# [(pair('澳门', 'ns'), 1.0),
#  (pair('驻军', 'n'), 0.5150728335629853),
#  (pair('部队', 'n'), 0.41732897719914397),
#  (pair('澳门特区', 'ns'), 0.3970962141957338),
#  (pair('重要', 'a'), 0.37778159391924593),
#  (pair('支持', 'v'), 0.3662188216433373),
#  (pair('坚持', 'v'), 0.3621765539284169),
#  (pair('防务', 'vn'), 0.3544464068364389),
#  (pair('履行', 'v'), 0.34640762164150035),
#  (pair('依法', 'n'), 0.3208985874730372)]
```
## 单元 29：代码（Code Cell）
- **原执行序号（Execution Count）**：`21`。
```python
jieba.analyse.textrank(sentence=sentence, topK=5, withWeight=True,
                       allowPOS=('n','nr'), withFlag=True)

# 期望输出（来自 Notebook 已保存输出）:
# [(pair('徐良才', 'nr'), 1.0),
#  (pair('部队', 'n'), 0.709163467727722),
#  (pair('主席', 'n'), 0.7033906297467337),
#  (pair('驻军', 'n'), 0.6108291079355574),
#  (pair('依法', 'n'), 0.5922974601476129)]
```
## 单元 30：说明（Markdown Cell）
## 单元 31：说明（Markdown Cell）
## 四、词性标注
- jieba中的分词词性说明详见: <a href="#ext1">jieba词性列表</a>
## 单元 32：代码（Code Cell）
- **原执行序号（Execution Count）**：`22`。
```python
import jieba.posseg as pseg
sentence = "我觉得人工智能未来的发展非常不错"
sentence = "姚明的身高"
sentence = "姚明的职业是什么"
# sentence = "成龙的身高是多少"
# 分词+词性标注
words = pseg.cut(sentence)

# 输出
print("%8s\t%8s" % ("【单词】", "【词性】"))
for word, flag in words:
    print("%8s\t%8s" % (word, flag))

# 期望输出（来自 Notebook 已保存输出）:
#     【单词】	    【词性】
#       姚明	      nr
#        的	      uj
#       职业	       n
#        是	       v
#       什么	       r
```
## 单元 33：代码（Code Cell）
- **原执行序号（Execution Count）**：`23`。
```python
import jieba.posseg as pseg
sentence = "徐良才说，近年来，驻军官兵时刻牢记习主席重要嘱托。"
# 分词+词性标注
words = pseg.cut(sentence)

# 输出
print("%8s\t%8s" % ("【单词】", "【词性】"))
for word, flag in words:
    print("%8s\t%8s" % (word, flag))

# 期望输出（来自 Notebook 已保存输出）:
#     【单词】	    【词性】
#      徐良才	      nr
#        说	       v
#        ，	       x
#      近年来	       t
#        ，	       x
#     驻军官兵	       x
#       时刻	       n
#       牢记	       n
#        习	       v
#       主席	       n
#       重要	       a
#       嘱托	       v
#        。	       x
```
## 单元 34：代码（Code Cell）
- **原执行序号（Execution Count）**：`24`。
```python
import jieba.posseg as pseg
sentence = "徐良才说，近年来，驻军官兵时刻牢记习主席重要嘱托。"

# 添加词典
jieba.add_word('习主席', 2, 'nr')

# 分词+词性标注
words = pseg.cut(sentence)

# 输出
print("%8s\t%8s" % ("【单词】", "【词性】"))
for word, flag in words:
    print("%8s\t%8s" % (word, flag))

# 期望输出（来自 Notebook 已保存输出）:
#     【单词】	    【词性】
#      徐良才	      nr
#        说	       v
#        ，	       x
#      近年来	       t
#        ，	       x
#     驻军官兵	       x
#       时刻	       n
#       牢记	       n
#      习主席	      nr
#       重要	       a
#       嘱托	       v
#        。	       x
```
## 单元 35：说明（Markdown Cell）
## 五、并行分词
- 原理：将目标文本按行分割后，把各行文本分配到多个Python进程中进行并行分词，然后归并结果。速度比单线程的快3~5倍。
- 基于Python自带的multiprocessing模块，暂时不支持windows
- 基本用法：
    - jieba.enable_parallel(4)
        - 开启并行分词模式，参数为并行进程数，可选
    - jieba.disable_parallel()
        - 关闭并行分词模式
- NOTE: **当同时使用并行分词和自定义词典的时候，要求将自定义词典放到并行分词之前做。**
## 单元 36：代码（Code Cell）
- **原执行序号（Execution Count）**：`25`。
```python
import jieba

# NotImplementedError: jieba: parallel mode only supports posix system
# jieba.enable_parallel()

content = '我是小明\n我是小明'
words = jieba.cut(content)
print(' / '.join(content))

# 期望输出（来自 Notebook 已保存输出）:
# 我 / 是 / 小 / 明 /
#  / 我 / 是 / 小 / 明
```
## 单元 37：说明（Markdown Cell）
### 扩展一：<a name='ext1'>jieba词性说明</a>
详见: <a href='http://ictclas.nlpir.org/nlpir/html/readme.htm'>ICTCLAS汉语词性标注集</a>
## 单元 38：说明（Markdown Cell）

|词性符号|词性名称|描述说明|
|:-|:-|:-|
|n|名词||
|nr|人名||
|ns|地名||
|nt|机构团体名||
|nz|其它专名||
|t|时间词||
|s|处方词||
|f|方位词||
|v|动词||
|vd|副动词|直接做状语的动词，动词和副词放到一起|
|vn|名动词|具有名词功能的动词，动词和名词放到一起|
|a|形容词||
|ad|副形词|直接作状语的形容词。形容词和副词放到一起。|
|an|名形词|具有名词功能的形容词。形容词和名词放到一起|
|b|区别词||
|z|状态词||
|r|代词||
|rr|人称代词||
|rz|指示代词||
|ry|疑问代词||
|m|数词||
|q|量词||
|d|副词||
|p|介词||
|c|连词||
|u|助词||
|e|叹词||
|eng|英语||
|y|语气词||
|o|拟声词||
|h|前缀||
|k|后缀||
|i|成语||
|l|习用语|临时的词语|
|q|量词||
|w|标点符号||
|x|字符串|符号、未知词性等描述|
## 单元 39：说明（Markdown Cell）
## 文本分类批量分词与词表构建

在实际的文本分类或 NLP 深度学习任务中，我们通常需要将原始数据集进行**批量分词**，并生成一份**全局词典（Vocabulary）**，为后续的词嵌入（Embedding）和序号化做准备。

### 1. 业务流程与设计思想

- **流式读写（Memory-Friendly）**：采用边读边写、逐行处理的方式，避免大文件一次性加载导致内存溢出。
- **动态去重**：利用 Python 的 `set` 集合收集所有分词结果，天然去重，高效构建词表。
- **特殊标记（Special Tokens）**：
    - `PAD`（Padding）：填充占位符。在模型批处理训练时，用于将不同长度的句子对齐到相同长度。
    - `UNK`（Unknown）：未知词占位符。用于在预测阶段替代未在词典中出现过的生僻词。
- **数据落盘**：
    - **分词语料**：词与词之间以 **空格** 隔开，文本与标签以 `\t`（Tab键）隔开。
    - **全局词典**：保存为标准的 `json` 数组，保持中文字符直观显示（不转码）。
## 单元 40：代码（Code Cell）
- **原执行序号（Execution Count）**：`None`。
```python
# 2.批量处理与词典生成代码
# -*- coding: utf-8 -*-
"""
Desc : 针对文本数据做批量分词，并将分词结果与去重词表保存到本地
"""
import json
import os
from typing import List
import jieba

# 1. 载入自定义词典（确保特定行业专业术语不被切碎）
jieba.load_userdict("./text_classify.word")


def split_text(text: str) -> List[str]:
    """文本分词函数"""
    return jieba.lcut(text)       # 方案 A：默认中文词级分词
    # return list(text.upper())   # 方案 B：字级分词（把每个字、英文字母当成一个词）


def t0(in_file, out_file):
    # 自动创建输出文件夹，防止路径不存在报错
    os.makedirs(os.path.dirname(out_file), exist_ok=True)

    # 初始化去重集合，用于收集词典
    vocabs = set()

    # 采用双 with 结构，边读入原始文件，边写入分词后的文件
    with open(in_file, "r", encoding="utf-8") as reader:
        with open(out_file, "w", encoding="utf-8") as writer:
            for line in reader:
                # 假设输入格式为：文本\t标签\n
                text, label = line.strip().split("\t")

                # 对文本进行分词
                tokens = split_text(text)

                # 将分词结果动态加入到词典集合中（自动去重）
                for token in tokens:
                    vocabs.add(token)

                # 写入新文件：分词用空格拼接，与标签用\t隔开
                writer.writelines(f"{' '.join(tokens)}\t{label}\n")

    # 2. 构建标准词表：在首部强行插入特殊占位符 ['PAD', 'UNK']
    vocabs = ['PAD', 'UNK'] + list(vocabs)

    # 3. 将单词映射表输出为漂亮的 JSON 文件
    vocab_path = os.path.join(str(os.path.dirname(out_file)), "vocabs.json")
    with open(vocab_path, 'w', encoding='utf-8') as w:
        # ensure_ascii=False 确保中文正常显示，indent=2 格式化缩进
        json.dump(vocabs, w, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # 执行批处理
    t0(
        in_file="../datas/text_classify/train.csv",
        out_file="../datas/text_classify/train_tokens.csv"
    )
```
## 单元 41：说明（Markdown Cell）
### 3. 关键技术点解析

- **`os.makedirs(..., exist_ok=True)`**
    - **作用**：级联创建目录。
    - **优势**：当 `exist_ok=True` 时，如果文件夹已经存在，不会抛出异常，省去了手动判断文件夹是否存在的步骤。
- **`json.dump(..., ensure_ascii=False)`**
    - **作用**：将 Python 对象序列化为 JSON 并写入文件。
    - **优势**：必须设置 `ensure_ascii=False`，否则写入 JSON 的中文会被强制转换为 Unicode 编码（如 `\u6211`），无法直观阅读。
- **`' '.join(tokens)`**
    - **作用**：深度学习框架（如 PyTorch、TensorFlow）在读取文本时，通常默认通过**空格**来识别词的边界。分词后用空格拼接，可以完美对接后续的 `Dataset` 读取流程。
## 单元 42：说明（Markdown Cell）
