---
title: 正则表达式（Regular Expressions）
aliases:
  - Python re
  - 正则表达式(Regular Expression)
status: review
detail_level: comprehensive
source:
  - Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/正则表达式(Regular Expression).md
suggested_target: Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/06-正则表达式（Regular Expressions）.md
operation: 新建
merge_target: null
---

# 正则表达式（Regular Expressions）

## 1. 什么时候使用正则

正则表达式适合描述**文本模式**，例如验证固定格式、提取日志字段和批量替换。

如果 `str.startswith()`、`split()`、`replace()` 已经能清晰解决问题，就不必使用正则。正则越复杂，维护和边界测试成本越高。

```python
import re

# 正则本身包含很多反斜杠，使用原始字符串可以避免 Python 再次转义。
pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
match = pattern.search("created_at=2026-08-10")

if match:
    print(match.group())  # 2026-08-10
```

## 2. 常用元字符

| 模式 | 含义 |
|---|---|
| `.` | 除换行外的任意字符（启用 `re.DOTALL` 后也包含换行） |
| `^` / `$` | 字符串或行的开头/结尾 |
| `\A` / `\Z` | 整个字符串的开头/结尾 |
| `\d` / `\D` | 数字 / 非数字 |
| `\w` / `\W` | 单词字符 / 非单词字符 |
| `\s` / `\S` | 空白 / 非空白 |
| `[abc]` | 集合中的一个字符 |
| `[^abc]` | 不在集合中的一个字符 |
| `a|b` | 匹配 `a` 或 `b` |
| `(...)` | 捕获分组 |
| `(?:...)` | 非捕获分组 |

量词：

| 量词 | 次数 |
|---|---|
| `*` | 0 次或更多 |
| `+` | 1 次或更多 |
| `?` | 0 次或 1 次 |
| `{m}` | 恰好 m 次 |
| `{m,n}` | m 到 n 次 |

量词默认是贪婪的；在后面加 `?` 可以改为非贪婪，例如 `.*?`。

## 3. `search`、`match` 与 `fullmatch`

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

## 4. 提取数据

### 命名分组

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
    print(match.groupdict())
```

### 多个匹配

```python
import re

text = "loss=0.52 accuracy=0.91"

values = re.findall(r"(\w+)=([0-9.]+)", text)
print(values)  # [('loss', '0.52'), ('accuracy', '0.91')]

for match in re.finditer(r"\w+=([0-9.]+)", text):
    # finditer 保留位置和分组信息，也避免一次性创建很大的结果列表。
    print(match.span(), match.group())
```

> [!note]
> `findall()` 的返回结构受捕获分组影响：无分组返回完整匹配，一个分组返回字符串列表，多个分组返回元组列表。

## 5. 替换与分割

```python
import re

text = "phone: 13812345678"
masked = re.sub(r"(?<=\d{3})\d{4}(?=\d{4})", "****", text)
print(masked)

parts = re.split(r"[,;\s]+", "red, green;blue")
print(parts)
```

替换逻辑需要代码时，可以传入函数：

```python
import re


def normalize_number(match: re.Match) -> str:
    value = float(match.group())
    return f"{value:.2f}"


result = re.sub(r"\d+(?:\.\d+)?", normalize_number, "loss=1 accuracy=0.9234")
```

## 6. 常用标志

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

## 7. 边界与性能

- 用户输入如果只是普通文本，应先用 `re.escape()` 转义，再拼入模式。
- 避免含糊的嵌套量词，例如 `(a+)+`，长输入可能造成灾难性回溯。
- 复杂模式应先 `re.compile()`，并为合法、非法、空字符串和极长字符串建立测试。
- HTML、JSON、编程语言等结构化内容应使用专用解析器，不要用正则完整解析。

```python
import re


def contains_literal(text: str, keyword: str) -> bool:
    # 如果不转义，keyword 中的 . * ? 等字符会被当作正则语法。
    return re.search(re.escape(keyword), text) is not None
```

## 8. 分组 (Groups) 与反向引用 (Backreferences)

### 捕获分组 (Capturing Group)

```python
import re

match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", "2026-08-10")
if match:
    print(match.group(0))   # 整个匹配。
    print(match.group(1))   # 第一个捕获组。
    print(match.groups())   # 所有捕获组构成的元组。
```

### 命名分组 (Named Group)

```python
pattern = re.compile(
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
)
match = pattern.fullmatch("2026-08-10")
if match:
    print(match.group("year"))
    print(match.groupdict())
```

### 反向引用 (Backreference)

```python
# \1 要求后面再次出现第一个捕获组的内容，可发现连续重复单词。
duplicate_word = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)
print(duplicate_word.search("This is is duplicated"))
```

命名反向引用使用 `(?P=name)`：

```python
quoted = re.compile(r"(?P<quote>['\"])(?P<content>.*?)(?P=quote)")
```

## 9. 前后查找 (Lookarounds)

前后查找只检查上下文，不把上下文字符包含进最终匹配。

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

## 10. Pattern 对象 (Pattern Object) 与 Match 对象 (Match Object)

### Pattern 常用方法

| 方法 | 用途 |
|---|---|
| `pattern.search()` | 任意位置找第一个匹配 |
| `pattern.match()` | 只从开头尝试 |
| `pattern.fullmatch()` | 整个字符串必须匹配 |
| `pattern.findall()` | 返回所有匹配的值 |
| `pattern.finditer()` | 惰性返回 Match 迭代器 |
| `pattern.split()` | 按模式拆分 |
| `pattern.sub()` | 替换匹配 |
| `pattern.subn()` | 替换并返回替换次数 |

### Match 常用属性和方法

```python
import re

match = re.search(r"(?P<key>\w+)=(?P<value>\d+)", "epochs=20")
if match:
    print(match.group())
    print(match.group("value"))
    print(match.start(), match.end(), match.span())
    print(match.string)
    print(match.lastgroup)
```

## 11. Unicode (Unicode) 与边界

Python 3 的字符串模式默认按 Unicode (Unicode) 处理，因此 `\w` 不只匹配 ASCII 英文字母、数字和下划线，也可能匹配中文等 Unicode 单词字符。

```python
import re

print(re.findall(r"\w+", "Python 数据分析 2026"))
print(re.findall(r"[A-Za-z0-9_]+", "Python 数据分析 2026"))
```

需要严格 ASCII (ASCII) 语义时可以明确字符集，或使用 `re.ASCII` 标志 (Flag)。

词边界 `\b` 是 `\w` 与 `\W` 的交界，不等同于自然语言分词边界；中文分词不要依赖 `\b`。

## 12. 调试与测试正则

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

## 13. 完成检查

- [ ] 能根据任务选择 `search`、`match` 或 `fullmatch`。
- [ ] 能解释捕获组、非捕获组和命名组。
- [ ] 能使用 `finditer`、`sub` 与 `split`。
- [ ] 知道原始字符串为什么适合编写正则。
- [ ] 能识别局部匹配、贪婪匹配和嵌套量词的风险。

## 参考资料

- [Python 标准库：re](https://docs.python.org/3/library/re.html)
- [Python HOWTO：Regular Expression](https://docs.python.org/3/howto/regex.html)
