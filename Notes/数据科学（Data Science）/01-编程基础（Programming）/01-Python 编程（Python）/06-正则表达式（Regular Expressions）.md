---
title: 正则表达式（Regular Expressions）
aliases:
  - Python re
  - 正则表达式(Regular Expression)
status: published
detail_level: comprehensive
merge_policy: union-zero-loss
reviewed_at: 2026-08-11
published_at: 2026-08-11
source:
  - Processing/02-Processed/2026-08-11-Python编程/originals/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/正则表达式(Regular Expression).md
---

# 正则表达式（Regular Expressions）
## 正则表达式 (Regular Expression)
### 一、 简介 (Introduction)
#### 结构化补充（Structured Supplement）：什么时候使用正则

正则表达式 (Regular Expression)适合描述**文本模式**，例如验证固定格式、提取日志字段和批量替换。

如果 `str.startswith()`、`split()`、`replace()` 已经能清晰解决问题，就不必使用正则。正则越复杂，维护和边界测试成本越高。

```python
import re

# 正则本身包含很多反斜杠，使用原始字符串可以避免 Python 再次转义。
pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
match = pattern.search("created_at=2026-08-10")

if match:
    print(match.group())  # 2026-08-10
```

#### 结构化补充（Structured Supplement）：边界与性能

- 用户输入如果只是普通文本，应先用 `re.escape()` 转义，再拼入模式。
- 避免含糊的嵌套量词 (Quantifier)，例如 `(a+)+`，长输入可能造成灾难性回溯 (Backtracking)。
- 复杂模式应先 `re.compile()`，并为合法、非法、空字符串 (String)和极长字符串 (String)建立测试。
- HTML、JSON、编程语言 (Programming Language)等结构化内容应使用专用解析器，不要用正则完整解析。

```python
import re


def contains_literal(text: str, keyword: str) -> bool:
    # 如果不转义，keyword 中的 . * ? 等字符会被当作正则语法。
    return re.search(re.escape(keyword), text) is not None
```

#### 结构化补充（Structured Supplement）：调试与测试正则

每个重要模式至少测试：

- 正常输入 (Valid Input)。
- 边界长度 (Boundary Length)。
- 空字符串 (Empty String)。
- 多行文本 (Multiline Text)。
- Unicode 字符 (Unicode Characters)。
- 极长输入 (Very Long Input)。
- 看起来相似但应拒绝的输入 (Near-miss Input)。

```python
import re

pattern = re.compile(r"[a-z][a-z0-9_]{2,19}", re.IGNORECASE)

cases = {
    "ada": True,
    "a_1": True,
    "1ada": False,
    "ab": False,
    "": False,
}

for text, expected in cases.items():
    actual = pattern.fullmatch(text) is not None
    assert actual is expected, (text, expected, actual)
```

对字符串 (String)进行操作的需求很多，只凭索引 (Index)切片 (Slicing)、对象方法等方式有时是不够用的（比如：判断一个字符串 (String)是否是有效的 email 地址），此时可以考虑使用正则表达式 (Regular Expression)。
假设 QQ 邮箱的规则如下：
- 结尾是 `@qq.com`
- `@` 前面只能是数字
- 且长度为 5-11 位
- 且不能以 0 开头

```Python
import re
pattern = r'^[1-9]\d{4,10}@qq\.com$'
p = re.compile(pattern)
def isvalid(email):
    if p.fullmatch(email):
        print("有效的QQ邮箱")
    else:
        print("无效的QQ邮箱")

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

**正则表达式 (Regular Expression)**，是对字符串 (String)操作的一种“逻辑公式”，它是由一些特定的字符组成的一个“匹配规则”，可以对要匹配的字符串 (String)指定该“规则”。
许多语言都支持利用正则表达式 (Regular Expression)进行字符串 (String)操作，Python 也不例外，通过内置的 `re` 模块 (Module)实现。
---
### 二、 字符匹配 (Character Matching)
#### 结构化补充（Structured Supplement）：Unicode (Unicode) 与边界

Python 3 的字符串 (String)模式默认按 Unicode (Unicode) 处理，因此 `\w` 不只匹配 ASCII 英文字母、数字和下划线，也可能匹配中文等 Unicode 单词字符。

```python
import re

print(re.findall(r"\w+", "Python 数据分析 2026"))
print(re.findall(r"[A-Za-z0-9_]+", "Python 数据分析 2026"))

# 期望输出:
# ['Python', '数据分析', '2026']
# ['Python', '2026']
```

需要严格 ASCII (ASCII) 语义时可以明确字符集 (Character Set)，或使用 `re.ASCII` 标志 (Flag)。

词边界 `\b` 是 `\w` 与 `\W` 的交界，不等同于自然语言分词边界；中文分词不要依赖 `\b`。

- **匹配机制 (Matching Mechanism)**：对要匹配的字符串 (String)的元素挨个判断是否与“规则”匹配。
- **书写注意**：正则表达式 (Regular Expression)是字符串 (String)，所以书写时通常不要随意加空格。
- **反斜杠问题 (Backslash Issue)**：因为正则表达式 (Regular Expression)和 Python 字符串 (String)都使用反斜杠字符来转义，有时就需要使用双倍的反斜杠才能达到想要的效果，而这很麻烦，所以强烈建议大家在写正则表达式 (Regular Expression)时，用**原始字符串 (Raw String)**。
正则表达式 (Regular Expression)可以包含普通字符或者特殊字符（元字符 (Metacharacter)）。
#### 1. 普通字符 (Ordinary Characters)
大多数字符为普通字符，它们只会和自身匹配。

```Python
import re
p = re.compile(r"test123")
print(p.search("atest123b"))
## <re.Match object; span=(1, 8), match='test123'>
```

#### 2. 特殊字符 / 元字符 (Meta Characters)
##### 结构化补充（Structured Supplement）：常用元字符 (Metacharacter)

| 模式 | 含义 |
|---|---|
| `.` | 除换行外的任意字符（启用 `re.DOTALL` 后也包含换行） |
| `^` / `$` | 字符串 (String)或行的开头/结尾 |
| `\A` / `\Z` | 整个字符串 (String)的开头/结尾 |
| `\d` / `\D` | 数字 / 非数字 |
| `\w` / `\W` | 单词字符 / 非单词字符 |
| `\s` / `\S` | 空白 / 非空白 |
| `[abc]` | 集合 (Set)中的一个字符 |
| `[^abc]` | 不在集合 (Set)中的一个字符 |
| `a|b` | 匹配 `a` 或 `b` |
| `(...)` | 捕获分组 (Capturing Group) |
| `(?:...)` | 非捕获分组 (Non-capturing Group) |

量词 (Quantifier)：

| 量词 (Quantifier) | 次数 |
|---|---|
| `*` | 0 次或更多 |
| `+` | 1 次或更多 |
| `?` | 0 次或 1 次 |
| `{m}` | 恰好 m 次 |
| `{m,n}` | m 到 n 次 |

量词 (Quantifier)默认是贪婪的；在后面加 `?` 可以改为非贪婪，例如 `.*?`。

##### 结构化补充（Structured Supplement）：前后查找 (Lookarounds)

前后查找 (Lookaround)只检查上下文，不把上下文字符包含进最终匹配。

| 语法 | 名称 | 含义 |
|---|---|---|
| `(?=...)` | 正向先行断言 (Positive Lookahead) | 后面必须满足 |
| `(?!...)` | 负向先行断言 (Negative Lookahead) | 后面不能满足 |
| `(?<=...)` | 正向后行断言 (Positive Lookbehind) | 前面必须满足 |
| `(?<!...)` | 负向后行断言 (Negative Lookbehind) | 前面不能满足 |

```python
import re

prices = re.findall(r"\d+(?=元)", "苹果10元，香蕉6元")
units = re.findall(r"(?<=￥)\d+(?:\.\d+)?", "￥12.5 ￥8")

# 找不以 .tmp 结尾的文件名。负向先行断言从当前位置检查后续内容。
pattern = re.compile(r"^(?!.*\.tmp$).+\.[A-Za-z0-9]+$")
```

Python 的后行断言 (Lookbehind) 通常要求固定长度模式，因此 `(?<=a+)` 这类可变长度写法会报错。

有些字符它们和自身并不匹配，而是匹配一些与众不同的东西或者影响正则表达式 (Regular Expression)的其他部分（对其重复或改变含义）。
元字符 (Metacharacter)包括：`. ^ $ * + ? {} [] \ | ()`
#### `.`
- 匹配除了换行符以外的任意一个字符。
- `DOTALL` 模式下，它将匹配包括换行符的任意一个字符。

```Python
import re
p = re.compile(r".")
print(p.match("abc"))
print(p.match("9bc"))
print(p.match("@bc"))
print(p.match(".bc"))
print(p.match("\tbc"))
print(p.match("\nbc"))
p = re.compile(r".", flags=re.DOTALL)
print(p.match("\nbc"))
## <re.Match object; span=(0, 1), match='a'>
## <re.Match object; span=(0, 1), match='9'>
## <re.Match object; span=(0, 1), match='@'>
## <re.Match object; span=(0, 1), match='.'>
## <re.Match object; span=(0, 1), match='\t'>
## None
## <re.Match object; span=(0, 1), match='\n'>
```

#### `^`
- 匹配字符串 (String)的开头。
- `MULTILINE` 模式下，还会继续匹配换行后的开头。

```Python
import re
p = re.compile(r"^ab")
print(p.findall("abcd\nabfg"))
p = re.compile(r"ab", flags=re.MULTILINE)
print(p.findall("abcd\nabfg"))
## ['ab']
## ['ab', 'ab']
```

#### `$`
- 匹配字符串 (String)的末尾或者匹配在字符串 (String)结尾的换行符之前的末尾。
- `MULTILINE` 模式下，还会匹配换行符之前的末尾（换行符可以不在字符串 (String)末尾）。

```Python
import re
p = re.compile(r"cd$")
print(p.findall("abcd\n"))
p = re.compile(r"cd$", flags=re.MULTILINE)
print(p.findall("abcd\nefcd"))
"""会找到两个(空的)匹配:一个在换行符之前,一个在字符串的末尾"""
p = re.compile(r"$")
print(p.findall("abcd\n"))
## ['cd']
## ['cd', 'cd']
## ['', '']
```

#### `*`
- 对它前面的正则表达式 (Regular Expression)匹配 0 到任意次重复，尽量多的匹配（贪婪匹配 (Greedy Matching) Greedy Match）。

```Python
import re
p = re.compile(r"ab*")
print(p.search("a"))
print(p.search("ab"))
print(p.search("abb"))
print(p.search("abbbc"))
## <re.Match object; span=(0, 1), match='a'>
## <re.Match object; span=(0, 2), match='ab'>
## <re.Match object; span=(0, 3), match='abb'>
## <re.Match object; span=(0, 4), match='abbb'>
```

#### `+`
- 对它前面的正则表达式 (Regular Expression)匹配 1 到任意次重复，尽量多的匹配（贪婪）。

```Python
import re
p = re.compile(r"ab+")
print(p.search("a"))
print(p.search("ab"))
print(p.search("abb"))
print(p.search("abbbc"))
## None
## <re.Match object; span=(0, 2), match='ab'>
## <re.Match object; span=(0, 3), match='abb'>
## <re.Match object; span=(0, 4), match='abbb'>
```

#### `?`
- 对它前面的正则表达式 (Regular Expression)匹配 0 到 1 次，尽量多的匹配（贪婪）。

```Python
import re
p = re.compile(r"ab?")
print(p.search("a"))
print(p.search("ab"))
print(p.search("abb"))
print(p.search("abbbc"))

# 期望输出:
# <re.Match object; span=(0, 1), match='a'>
# <re.Match object; span=(0, 2), match='ab'>
# <re.Match object; span=(0, 2), match='ab'>
# <re.Match object; span=(0, 2), match='ab'>
```

#### `?`, `+?`, `??` (非贪婪匹配 (Non-greedy Matching) Non-greedy Match)
- , `+`, `?` 都是贪婪的，它们对字符串 (String)进行尽可能多的匹配，有时候并不需要这种行为，可以在之后添加 `?`，就可以以非贪婪的方式进行匹配，则尽可能少的字符将会被匹配。

```Python
import re
p = re.compile(r'<.*>')
print(p.search('<a> b <c>'))
p = re.compile(r'<.*?>')
print(p.search('<a> b <c>'))
p = re.compile(r"ab+?")
print(p.search("abbbc"))
p = re.compile(r"ab??")
print(p.search("abc"))

# 期望输出:
# <re.Match object; span=(0, 9), match='<a> b <c>'>
# <re.Match object; span=(0, 3), match='<a>'>
# <re.Match object; span=(0, 2), match='ab'>
# <re.Match object; span=(0, 1), match='a'>
```

#### `{m}`
- 对其之前的正则表达式 (Regular Expression)指定匹配 `m` 个重复。

```Python
import re
p = re.compile(r"ab{2}")
print(p.search("abc"))
print(p.search("abbc"))
print(p.search("abbbc"))

# 期望输出:
# None
# <re.Match object; span=(0, 3), match='abb'>
# <re.Match object; span=(0, 3), match='abb'>
```

#### `{m,n}`
- 对其之前的正则表达式 (Regular Expression)进行 `m` 到 `n` 次匹配，在 `m` 和 `n` 之间取尽量多（贪婪方式）。
- 忽略 `m` 则下限默认为 0，忽略 `n` 则上限默认为无限次（逗号不能省略）。

```Python
import re
p = re.compile(r"ab{2,4}")
print(p.search("abc"))
print(p.search("abbc"))
print(p.search("abbbc"))
print(p.search("abbbbc"))
print(p.search("abbbbbc"))
p = re.compile(r"ab{,4}")
print(p.search("ac"))
print(p.search("abc"))
p = re.compile(r"ab{2,}")
print(p.search("abbbbc"))
print(p.search("abbbbbc"))

# 期望输出:
# None
# <re.Match object; span=(0, 3), match='abb'>
# <re.Match object; span=(0, 4), match='abbb'>
# <re.Match object; span=(0, 5), match='abbbb'>
# <re.Match object; span=(0, 5), match='abbbb'>
# <re.Match object; span=(0, 1), match='a'>
# <re.Match object; span=(0, 2), match='ab'>
# <re.Match object; span=(0, 5), match='abbbb'>
# <re.Match object; span=(0, 6), match='abbbbb'>
```

#### `{m,n}?`
- 上面 `{m,n}` 的非贪婪模式。

```Python
import re
p = re.compile(r"ab{2,4}?")
print(p.search("abc"))
print(p.search("abbc"))
print(p.search("abbbc"))
print(p.search("abbbbc"))
print(p.search("abbbbbc"))
p = re.compile(r"ab{,4}?")
print(p.search("ac"))
print(p.search("abc"))
p = re.compile(r"ab{2,}?")
print(p.search("abbbbc"))
print(p.search("abbbbbc"))

# 期望输出:
# None
# <re.Match object; span=(0, 3), match='abb'>
# <re.Match object; span=(0, 3), match='abb'>
# <re.Match object; span=(0, 3), match='abb'>
# <re.Match object; span=(0, 3), match='abb'>
# <re.Match object; span=(0, 1), match='a'>
# <re.Match object; span=(0, 1), match='a'>
# <re.Match object; span=(0, 3), match='abb'>
# <re.Match object; span=(0, 3), match='abb'>
```

#### `|`
- 任意个正则表达式 (Regular Expression)可以用 `|` 连接，比如 `A|B` 表示匹配正则表达式 (Regular Expression) `A` 或者 `B`，一旦有一个先匹配成功，另外的就不会再进行匹配。

```Python
import re
p = re.compile(r"d|e|b")
print(p.search("abc"))
print(p.search("aebcd"))

# 期望输出:
# <re.Match object; span=(1, 2), match='b'>
# <re.Match object; span=(1, 2), match='e'>
```

#### `\` (转义与特殊序列 (Sequence) Escape & Special Sequence)
- 转义特殊字符。
- 用来表示一个特殊序列（由 `\` 和一个字符组成的特殊序列 (Sequence)）。

```Python
import re
## 只匹配 * 号
p = re.compile(r"\*")
print(p.fullmatch("*"))
## 只匹配 + 号
p = re.compile(r"\+")
print(p.fullmatch("+"))
## 只匹配 ? 号
p = re.compile(r"\?")
print(p.fullmatch("?"))

# 期望输出:
# <re.Match object; span=(0, 1), match='*'>
# <re.Match object; span=(0, 1), match='+'>
# <re.Match object; span=(0, 1), match='?'>
```

#### `\number`
- 匹配数字代表的分组里面的内容（每个括号是一个子组，子组从 1 开始编号），在 `[` 和 `]` 字符集 (Character Set)内，任何数字转义都被看作是字符。

```Python
import re
""" \1匹配的内容和第1组一定一样 """
p = re.compile(r"(.+) \1")
print(p.search("ab abc"))
print(p.search("5 5"))
""" 两个组匹配的内容不一定一样 """
p = re.compile(r" (.+) (.+)")
print(p.search("ab abc"))
print(p.search("5 5"))

# 期望输出:
# <re.Match object; span=(0, 5), match='ab ab'>
# <re.Match object; span=(0, 3), match='5 5'>
# None
# None
```

#### `\A`
- 匹配字符串 (String)的开头，类似于 `^`，区别在于：`MULTILINE` 模式下，`\A` 不识别换行。

```Python
import re
p = re.compile(r"^ab")
print(p.findall("abcd\nabfg"))
p = re.compile(r"^ab", flags=re.MULTILINE)
print(p.findall("abcd\nabfg"))
p = re.compile(r"\Aab")
print(p.findall("abcd\nabfg"))
p = re.compile(r"\Aab", flags=re.MULTILINE)
print(p.findall("abcd\nabfg"))

# 期望输出:
# ['ab']
# ['ab', 'ab']
# ['ab']
# ['ab']
```

#### `\b` 与 `\B`
- `\b`：匹配空字符串 (String)，但只在单词开始或结尾的位置，即匹配一个**单词边界 (Word Boundary)**。
- `\B`：匹配空字符串 (String)，但不能在单词开始或结尾的位置，即匹配非单词边界。

```Python
import re
p = re.compile(r"er\b")
print(p.search("never"))
print(p.search("verb"))
p = re.compile(r"\ba\b")
print(p.search("I have a dog"))
p = re.compile(r"er\B")
print(p.search("never"))
print(p.search("verb"))
p = re.compile(r"\Ba\B")
print(p.search("I have a dog"))

# 期望输出:
# <re.Match object; span=(3, 5), match='er'>
# None
# <re.Match object; span=(7, 8), match='a'>
# None
# <re.Match object; span=(1, 3), match='er'>
# <re.Match object; span=(3, 4), match='a'>
```

#### `\d` 与 `\D`
- `\d`：匹配任意一个数字字符，等价于 `[0-9]`。
- `\D`：匹配任意一个非数字字符，等价于 `[^0-9]`。

```Python
import re
p = re.compile(r"\d")
print(p.search("a1234b"))
p = re.compile(r"\d+")
print(p.search("a1234b"))
p = re.compile(r"\D")
print(p.search("ab1234c"))
p = re.compile(r"\D+")
print(p.search("ab1234c"))

# 期望输出:
# <re.Match object; span=(1, 2), match='1'>
# <re.Match object; span=(1, 5), match='1234'>
# <re.Match object; span=(0, 1), match='a'>
# <re.Match object; span=(0, 2), match='ab'>
```

#### `\s` 与 `\S`
- `\s`：匹配任何一个空白符。
- `\S`：匹配任何一个非空白符。

```Python
import re
p = re.compile(r"a\sb")
print(p.search("adb a bc"))
p = re.compile(r"a\Sb")
print(p.search("adb a bc"))

# 期望输出:
# <re.Match object; span=(4, 7), match='a b'>
# <re.Match object; span=(0, 3), match='adb'>
```

#### `\w` 与 `\W`
- `\w`：匹配一个字母或一个数字或一个下划线，等价于 `[a-zA-Z0-9_]`。
- `\W`：匹配一个非字母非数字非下划线的字符，等价于 `[^a-zA-Z0-9_]`。

```Python
import re
p = re.compile(r"a\wb")
print(p.findall("adba9ba_ba b"))
p = re.compile(r"a\Wb")
print(p.findall("adba9ba_ba b"))

# 期望输出:
# ['adb', 'a9b', 'a_b']
# ['a b']
```

#### `\Z`
- 只匹配字符串 (String)的末尾，且 `MULTILINE` 模式下，`\Z` 不识别换行。

```Python
import re
p = re.compile(r"cd\Z")
print(p.findall("abcd"))
# 结尾是 `\n`，因此字符串不以 `cd` 结束。
print(p.findall("abcd\n"))
# 即使启用 MULTILINE，\Z 仍只匹配整个字符串末尾，不匹配行末。
p2 = re.compile(r"cd\Z", flags=re.MULTILINE)
print(p2.findall("abcd\nef"))
# 整个字符串只有一个末尾位置，因此只得到一个空匹配。
p = re.compile(r"\Z")
print(p.findall("abcd\n"))

# 期望输出:
# ['cd']
# []
# []
# ['']
```

#### `\n \t \\ \' \"`
绝大部分 Python 的标准转义字符也被正则表达式 (Regular Expression)分析器支持。

```Python
import re
p = re.compile(r"\n")
print(p.findall("\n"))
p = re.compile(r"\t")
print(p.findall("\t"))
p = re.compile(r"\\")
print(p.findall("\\"))
p = re.compile(r"\'")
print(p.findall("'"))
p = re.compile(r"\"")
print(p.findall('"'))

# 期望输出:
# ['\n']
# ['\t']
# ['\\']
# ["'"]
# ['"']
```

#### 3. `[]` 字符集 (Character Set)
- 用于表示一个字符集 (Character Set)：
    - 字符可以单独列出，比如 `[amk]` 匹配 `a`， `m`， 或者 `k`。
    - 可以表示字符范围，通过用 将两个字符连起来。
    - 特殊字符在字符集 (Character Set)中，失去它的特殊含义。
    - 特殊序列 (Sequence)，如 `\d \s \w` 在字符集 (Character Set)中可以被接受。
- 不在字符集 (Character Set)范围内的字符可以通过取反来进行匹配，如果字符集 (Character Set)首字符是 `^` ，所有不在字符集 (Character Set)内的字符将会被匹配，`^` 如果不在字符集 (Character Set)首位，就没有特殊含义。
- 如果要匹配 `[` 或者 `]`，可以在它之前加上反斜杠。

```Python
import re
p = re.compile(r"[amk]")
print(p.findall("I have a monkey"))
p = re.compile(r"[a-y]")
print(p.findall("ahzyqAHZYQ"))
p = re.compile(r"[0-5][A-Y]")
print(p.findall("a0hzyq125A6HZYQ"))
p = re.compile(r"[.+]")
print(p.findall("abc"))
p = re.compile(r"[.+]")
print(p.findall("a.b+c.d+"))
p = re.compile(r"[\d]")
print(p.search("a1234b"))
p = re.compile(r"[\d+]")
print(p.findall("a1234b+"))
p = re.compile(r"[a\sb]")
print(p.findall("adb a bc"))
p = re.compile(r"[\w]")
print(p.findall("adb_a b!c"))
p = re.compile(r"[^5]")
print(p.findall("5a b512!5"))
p = re.compile(r"[^^]")
print(p.findall("5a^b512!5"))
p = re.compile(r"[\[\]]")
print(p.findall("[]"))

# 期望输出:
# ['a', 'a', 'm', 'k']
# ['a', 'h', 'y', 'q']
# ['5A']
# []
# ['.', '+', '.', '+']
# <re.Match object; span=(1, 2), match='1'>
# ['1', '2', '3', '4', '+']
# ['a', 'b', ' ', 'a', ' ', 'b']
# ['a', 'd', 'b', '_', 'a', 'b', 'c']
# ['a', ' ', 'b', '1', '2', '!']
# ['5', 'a', 'b', '5', '1', '2', '!', '5']
# ['[', ']']
```

#### 4. `(...)` 捕获分组 (Capturing Group)
##### 结构化补充（Structured Supplement）：提取数据
###### 命名分组 (Named Group)

```python
import re

log_pattern = re.compile(
    r"(?P<level>INFO|WARNING|ERROR)\s+"
    r"(?P<date>\d{4}-\d{2}-\d{2})\s+"
    r"(?P<message>.+)"
)

match = log_pattern.fullmatch("ERROR 2026-08-10 model failed")
if match:
    # groupdict 让字段名进入结果，比分组编号更容易维护。
    print(match.groupdict())  # 输出: {'level': 'ERROR', 'date': '2026-08-10', 'message': 'model failed'}
```

###### 多个匹配

```python
import re

text = "loss=0.52 accuracy=0.91"

values = re.findall(r"(\w+)=([0-9.]+)", text)
print(values)

for match in re.finditer(r"\w+=([0-9.]+)", text):
    # finditer 保留位置和分组信息，也避免一次性创建很大的结果列表。
    print(match.span(), match.group())

# 期望输出:
# [('loss', '0.52'), ('accuracy', '0.91')]
# (0, 9) loss=0.52
# (10, 23) accuracy=0.91
```

> [!note]
> `findall()` 的返回结构受捕获分组 (Capturing Group)影响：无分组返回完整匹配，一个分组返回字符串 (String)列表 (List)，多个分组返回元组 (Tuple)列表 (List)。

##### 结构化补充（Structured Supplement）：分组 (Groups) 与反向引用 (Backreferences)
###### 捕获分组 (Capturing Group)

```python
import re

match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", "2026-08-10")
if match:
    print(match.group(0))   # 整个匹配。
    print(match.group(1))   # 第一个捕获组。
    print(match.groups())   # 所有捕获组构成的元组。
```

###### 命名分组 (Named Group)

```python
pattern = re.compile(
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
)
match = pattern.fullmatch("2026-08-10")
if match:
    print(match.group("year"))
    print(match.groupdict())

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

###### 反向引用 (Backreference)

```python
# \1 要求后面再次出现第一个捕获组的内容，可发现连续重复单词。
duplicate_word = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)
print(duplicate_word.search("This is is duplicated"))

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

命名反向引用 (Backreference)使用 `(?P=name)`：

```python
quoted = re.compile(r"(?P<quote>['\"])(?P<content>.*?)(?P=quote)")
```

- 捕获分组 (Capturing Group)，匹配括号内的任意正则表达式 (Regular Expression)，并标识出该分组的开始和结尾。
- 组从 0 开始编号，组 0 始终存在，它表示整个正则，所以 `Match` 的对象方法都将组 0 作为默认参数 (Default Parameter)；子组从左到右编号，从 1 向上编号。
- 分组匹配的内容可以在之后其他分组用 `\number` 进行再次引用 (Reference)。
- 要匹配字符 `(` 或者 `)`，用 `\(` 或 `\)`，或者把它们包含在字符集 (Character Set)里：`[(]`，`[)]`。

```Python
import re
p = re.compile(r"b(.+)a(.+)e")
m = p.match("babacdefg")
print(m)
## Match 的对象方法 (返回组、起始结束位置信息)
print(m.group())
print(m.group(0))
print(m.group(1))
print(m.group(2))
print(m.group(2, 1, 0))
print(m.start(), m.end())
print(m.start(1), m.end(1))
print(m.start(2), m.end(2))
## 返回一个元组，包含 (Match.start([group]), Match.end([group]))，group默认为 0
print(m.span())
print(m.span(0))
print(m.span(1))
print(m.span(2))

# 期望输出:
# <re.Match object; span=(0, 7), match='babacde'>
# babacde
# babacde
# ab
# cd
# ('cd', 'ab', 'babacde')
# 0 7
# 1 3
# 4 6
# (0, 7)
# (0, 7)
# (1, 3)
# (4, 6)
```

---
### 三、 Pattern 对象方法 (Pattern Object Methods)
#### 结构化补充（Structured Supplement）：`search`、`match` 与 `fullmatch`

```python
import re

text = "user-123"

re.search(r"\d+", text)          # 在任意位置查找。
re.match(r"user", text)           # 只从字符串开头尝试。
re.fullmatch(r"user-\d+", text)   # 要求整个字符串都符合模式。
```

验证输入格式时优先 `fullmatch()`，否则可能只匹配到合法的局部。

```python
import re

USERNAME_PATTERN = re.compile(r"[a-z][a-z0-9_]{2,19}", re.IGNORECASE)


def is_valid_username(username: str) -> bool:
    return USERNAME_PATTERN.fullmatch(username) is not None
```

#### 结构化补充（Structured Supplement）：替换与分割

```python
import re

text = "phone: 13812345678"
masked = re.sub(r"(?<=\d{3})\d{4}(?=\d{4})", "****", text)
print(masked)

parts = re.split(r"[,;\s]+", "red, green;blue")
print(parts)

# 期望输出:
# phone: 138****5678
# ['red', 'green', 'blue']
```

替换逻辑需要代码时，可以传入函数 (Function)：

```python
import re


def normalize_number(match: re.Match) -> str:
    value = float(match.group())
    return f"{value:.2f}"


result = re.sub(r"\d+(?:\.\d+)?", normalize_number, "loss=1 accuracy=0.9234")
```

#### 结构化补充（Structured Supplement）：Pattern 对象 (Pattern Object) 与 Match 对象 (Match Object)
##### Pattern 常用方法

| 方法 | 用途 |
|---|---|
| `pattern.search()` | 任意位置找第一个匹配 |
| `pattern.match()` | 只从开头尝试 |
| `pattern.fullmatch()` | 整个字符串 (String)必须匹配 |
| `pattern.findall()` | 返回所有匹配的值 |
| `pattern.finditer()` | 惰性返回 Match 迭代器 (Iterator) |
| `pattern.split()` | 按模式拆分 |
| `pattern.sub()` | 替换匹配 |
| `pattern.subn()` | 替换并返回替换次数 |

##### Match 常用属性和方法

```python
import re

match = re.search(r"(?P<key>\w+)=(?P<value>\d+)", "epochs=20")
if match:
    print(match.group())
    print(match.group("value"))
    print(match.start(), match.end(), match.span())
    print(match.string)
    print(match.lastgroup)

# 期望输出:
# epochs=20
# 20
# 0 9 (0, 9)
# epochs=20
# value
```

#### `Pattern.match(string[, pos[, endpos]])`
- `string`：要匹配的字符串 (String)。
- `pos`：匹配的起始位置，默认为 0。
- `endpos`：匹配的结束位置，默认为字符串 (String)长度。
- 当字符串 (String)的起始位置匹配成功，返回 `Match` 类的实例对象（该实例对象 (Instance Object)包含匹配相关的信息：起始和结束位置、匹配的子串等等）；如果起始位置没有匹配，则返回 `None`。

```Python
import re
p = re.compile('og')
print(p.match("dog"))
print(p.search("dog", 1))

# 期望输出:
# None
# <re.Match object; span=(1, 3), match='og'>
```

#### `Pattern.fullmatch(string[, pos[, endpos]])`
- `string`：要匹配的字符串 (String)。
- `pos`：匹配的起始位置，默认为 0。
- `endpos`：匹配的结束位置，默认为字符串 (String)长度。
- 当整个字符串 (String)都匹配成功，返回 `Match` 类的实例对象（该实例对象 (Instance Object)包含匹配相关的信息：起始和结束位置、匹配的子串等等），否则返回 `None`。

```Python
import re
p = re.compile('o[gh]')
print(p.fullmatch("ogh"))
print(p.fullmatch("og"))
print(p.fullmatch("oh"))
print(p.fullmatch("dog"))
print(p.fullmatch("dog", 1))

# 期望输出:
# None
# <re.Match object; span=(0, 2), match='og'>
# <re.Match object; span=(0, 2), match='oh'>
# None
# <re.Match object; span=(1, 3), match='og'>
```

#### `Pattern.findall(string[, pos[, endpos]])`
- `string`：要匹配的字符串 (String)。
- `pos`：匹配的起始位置，默认为 0。
- `endpos`：匹配的结束位置，默认为字符串 (String)长度。
- 对字符串 (String)从左往右扫描，找到所有不重复匹配，以列表 (List)的形式返回，如果有子组，那么只保留子组的捕获内容，如果子组多个（至少两个子组），则以元组 (Tuple)形式构建列表 (List)，如果没有找到匹配的，则返回空列表 (List)。

```Python
import re
p = re.compile(r'\d')
print(p.findall("Ten years ago, Three dogs"))
print(p.findall("10 years ago, 3 dogs"))
## 多个分组，返回元组列表
p = re.compile(r'(\d+)-(\D)')
print(p.findall("Ten-years ago, Three-dogs"))
print(p.findall("101-years ago, 3-dogs"))

# 期望输出:
# []
# ['1', '0', '3']
# []
# [('101', 'y')]
```

#### `Pattern.split(string, maxsplit=0)`
- `string`：要匹配的字符串 (String)。
- `maxsplit`：最大分割次数，默认为 0，表示不限制次数。
- 按照匹配的子串将字符串 (String)分割，以列表 (List)形式返回。
- 如果有捕获分组 (Capturing Group)，那么分组里匹配的内容也会包含在结果中。
#### `Pattern.sub(repl, string, count=0)`
- `repl`：替换的字符串 (String) 或者 函数 (Function)。
- `string`：要被匹配后替换的字符串 (String)。
- `count`：最大替换次数；`0` 表示替换全部匹配。
- 返回一个新的字符串 (String)，不会原地修改原字符串 (String)。

```Python
import re

# 第二个捕获分组 (Capturing Group) 被 {2} 量化；它仍然只有一个组号，
# Match.groups() 只保留该分组最后一次迭代捕获到的字符。
p = re.compile(r"(\d)(\d){2}")
match = p.fullmatch("123")
print(match.groups())                # 输出: ('1', '3')
print(p.sub(r"\1XX", "123 456"))  # 输出: 1XX 4XX

# 注意: 不能把 `(\d)(\d){2}` 的捕获结果误解为三个独立分组；若需要分别保留三个数字，应写成 `(\d)(\d)(\d)`。
```

---
### 四、 模块 (Module)级别函数 (Module Level Functions)
如果你不想创建 `Pattern` 实例对象 (Instance Object)并调用其方法，也可以直接使用 `re` 模块 (Module)提供的函数 (Function)：
- `re.search(pattern, string, flags=0)`
- `re.match(pattern, string, flags=0)`
- `re.fullmatch(pattern, string, flags=0)`
- `re.findall(pattern, string, flags=0)`
- `re.split(pattern, string, maxsplit=0, flags=0)`
- `re.sub(pattern, repl, string, count=0, flags=0)`
### 编译模式
#### 结构化补充（Structured Supplement）：常用标志

| 标志 | 作用 |
|---|---|
| `re.IGNORECASE` / `re.I` | 忽略大小写 |
| `re.MULTILINE` / `re.M` | 让 `^`、`$` 匹配每一行边界 |
| `re.DOTALL` / `re.S` | 让 `.` 也匹配换行 |
| `re.VERBOSE` / `re.X` | 允许分行并添加注释，适合复杂模式 |

```python
import re

DATE_PATTERN = re.compile(
    r"""
    (?P<year>\d{4})
    [-/]
    (?P<month>0[1-9]|1[0-2])
    [-/]
    (?P<day>0[1-9]|[12]\d|3[01])
    """,
    re.VERBOSE,
)
```

这个模式只验证形式，不能确认 `2026-02-31` 是真实日期；日期语义应交给 `datetime` 校验。

编译标志可以修改正则表达式 (Regular Expression)的一些匹配方式，它在 re 模块 (Module)中有两个名
称:全名 和 缩写。其中需要掌握的有:
#### `re.I / re.IGNORECASE`
- 进行忽略大小写匹配
#### `import re`

```Plain
p=re.compile(r"[a-z]+",flags=re.IGNORECASE)
print(p.match("aAbBcC"))
```

#### `re.M / re.MULTILINE`
- 多行匹配，影响 ^ 和 $
- 设置以后， ^ 匹配字符串 (String)的开始，和每一行的开始;$ 匹配字符
    串尾，和每一行的结尾

```Python
import re
p = re.compile(r"^ab", flags=re.MULTILINE)
print(p.findall("abcd\nabfg"))
p = re.compile(r"cd$", flags=re.MULTILINE)
print(p.findall("abcd\nefcd"))

# 期望输出:
# ['ab', 'ab']
# ['cd', 'cd']
```

#### `re.S / re.DOTALL`
- 使 . 匹配包括换行在内的所有字符，没有设置时 . 是不能匹配换
    行符的

```Python
import re
p1 = re.compile(r".")
p2 = re.compile(r".", flags=re.DOTALL)
print(p1.search("\nbc"))
print(p2.search("\nbc"))

# 期望输出:
# <re.Match object; span=(1, 2), match='b'>
# <re.Match object; span=(0, 1), match='\n'>
```

## 进阶补充与核对（Advanced Supplements and Verification）
### 结构化补充（Structured Supplement）：完成检查

- [ ] 能根据任务选择 `search`、`match` 或 `fullmatch`。
- [ ] 能解释捕获组、非捕获组和命名组。
- [ ] 能使用 `finditer`、`sub` 与 `split`。
- [ ] 知道原始字符串 (Raw String)为什么适合编写正则。
- [ ] 能识别局部匹配、贪婪匹配 (Greedy Matching)和嵌套量词 (Quantifier)的风险。

### 结构化补充（Structured Supplement）：参考资料

- [Python 标准库：re](https://docs.python.org/3/library/re.html)
- [Python HOWTO：Regular Expression](https://docs.python.org/3/howto/regex.html)
