---
title: 文件、路径、模块与包（Files Paths Modules and Packages）
aliases:
  - 文件、路径操作、模块与包
status: published
detail_level: comprehensive
merge_policy: union-zero-loss
reviewed_at: 2026-08-11
published_at: 2026-08-11
source:
  - Processing/02-Processed/2026-08-11-Python编程/originals/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/文件、路径操作、模块与包.md
---

# 文件、路径 (Path)、模块 (Module)与包（Files Paths Modules and Packages）
## 模块 (Module) & 包 (Modules & Packages)
### 一、 模块 (Module)概念 (Module Concept)
#### 模块 (Module)、包和发行包 (Distribution Package)

- **模块（Module）**：一个可导入的 Python 文件，例如 `metrics.py`。
- **导入包（Import Package）**：组织模块 (Module)的目录结构。
- **发行包（Distribution Package）**：通过 `pip` 安装的项目，例如 `scikit-learn`；它的安装名不一定等于导入名。

传统包通常包含 `__init__.py`，但现代 Python 也支持没有该文件的命名空间 (Namespace)包，因此“包一定有 `__init__.py`”不是绝对规则。

- 模块 (Module)是一个包含 Python 定义和语句的文件，把相关的代码分配到一个模块 (Module)里，可以让代码更好用、更易懂。
### 二、 模块 (Module)导入 (Module Import)
#### 导入方式

```python
import math
import numpy as np
from pathlib import Path
from collections import Counter as FrequencyCounter
```

使用原则：

- 导入通常放在文件顶部：标准库、第三方库、本地模块 (Module)分组排列。
- 避免 `from module import *`，因为它会污染当前命名空间 (Namespace)并隐藏名称来源。
- 不要为了让导入成功就在程序中随意修改 `sys.path`；应修正项目结构或安装方式。
- 避免让本地文件与标准库或第三方库同名，例如 `json.py`、`numpy.py`。

- 模块 (Module)可以被别的程序引入，以使用该模块 (Module)中定义的变量 (Variable)，函数 (Function)等功能。
- 习惯上（但不强制要求）把所有导入语句放在模块 (Module)的开头。
- 一个模块 (Module)被另一个程序第一次导入时，会执行该模块 (Module)。
#### 1. 导入语法

```Python
import module
import module as alias  # 别名 (Alias)
from module import item
from module import item as alias
from module import *
```

**注意**：请慎用 `from module import *`，很容易出现名称重复的情况，导致出现一些意外的问题。
---
### 三、 包的概念 (Package Concept)
#### 推荐项目结构

```text
project/
├── pyproject.toml
├── README.md
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── data.py
│       └── model.py
└── tests/
    └── test_data.py
```

把可复用逻辑放在模块 (Module)中，把 Notebook 当作探索和展示入口，可以减少复制粘贴。

- Python 包本质上是一个文件夹，只是该文件夹会包含 `__init__.py` 模块 (Module)。
- 和文件夹一样，包里面还可以存在子包 (Sub-package)、模块 (Module)或者其它文件。
#### 1. 包的作用 (Role of Packages)
- **避免相同命名冲突**：如果在同一个包里，是不允许两个模块 (Module)命名相同的，但是如果不在同一个包里，是可以的。
- **模块 (Module)分区**：把不同功能的模块 (Module)归类到不同的包里，方便查询和修改。在比较大型的项目中常常需要编写大量的模块 (Module)，此时我们可以使用包来对这些模块 (Module)进行管理。
---
### 四、 包的导入 (Package Import)

```Python
import package
import package as alias
from package import module
from package import module as alias
from package.module import item
from package.module import item as alias
```

---
### 五、 搜索路径 (Search Path)
- `sys` 模块 (Module)的 `path` 变量 (Variable)以列表 (List) 的形式记录了 Python 解释器 (Interpreter) 自动查找所需模块 (Module)或包的路径 (Path)。
- 如果这些路径 (Path)都找不到，则会报错：`ModuleNotFoundError: No module named 'xxx'`。
**代码示例 (Code Example)：**

```Python
import sys
## 查看搜索路径列表
print(sys.path)
## 如果模块不在路径中，可以手动添加
## sys.path.append('你的路径')
```

### 六、`__name__` 属性 (`__name__` Attribute)
#### `__name__ == "__main__"`

模块 (Module)被直接运行时，`__name__` 是 `"__main__"`；被其他模块 (Module)导入时，`__name__` 是模块 (Module)名。

```python
def main() -> None:
    print("运行命令行入口")  # 输出: 运行命令行入口


if __name__ == "__main__":
    # 把入口放进判断中，导入这个模块时就不会意外执行任务。
    main()
```

每个模块 (Module)都有一个 `__name__` 属性：
- 当其值是 `'__main__'` 时，说明**该模块 (Module)自身在运行**。
- 否则，说明该模块 (Module)是**因为被导入才执行的**，此时其值为模块 (Module)名。
**应用场景 (Application Scenario)：**
在完成一个模块 (Module)的编写之前，我们一般会对模块 (Module)中的功能进行测试，看看各项功能是否正常运行。对于这些测试的代码，我们希望**只在直接运行这个模块 (Module)时执行**，而在其它程序导入这个模块 (Module)时不要执行，这个时候就可以借助 `__name__` 属性来实现。
**代码示例 (Code Example)：**

```Python
def add(x, y):
    print(x + y)
    print(x * 2)
## 只有当该文件被直接运行时，下面的测试代码才会被执行
## 如果该文件被作为模块导入到其他程序中，下面的代码不会被执行
if __name__ == '__main__':
    add(3, 4)
    add('3', '4')

# 期望输出（直接运行该文件时）:
# 7
# 6
# 34
# 33
```

## 文件和路径 (Path)操作 (File and Path Operations)
### 使用 `pathlib` 操作路径 (Path)

`pathlib.Path` 能跨 Windows、macOS 和 Linux 组合 (Composition)路径 (Path)，通常比手动拼接 (Concatenation)字符串 (String)更安全。

```python
from pathlib import Path

project_root = Path.cwd()
data_dir = project_root / "data" / "raw"
input_file = data_dir / "samples.csv"

# parents=True 会创建缺失的父目录；exist_ok=True 让重复运行保持幂等。
data_dir.mkdir(parents=True, exist_ok=True)

print(input_file.name)       # samples.csv
print(input_file.stem)       # samples
print(input_file.suffix)     # .csv
print(input_file.parent)
print(input_file.exists())
print(input_file.is_file())
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

遍历文件：

```python
from pathlib import Path

for csv_path in Path("data").glob("*.csv"):
    print(csv_path)

for image_path in Path("images").rglob("*.png"):
    # rglob 会递归搜索子目录，大目录中使用时要注意成本。
    print(image_path)

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

> [!warning]
> 相对路径 (Path)默认相对于“当前工作目录”，不一定相对于当前 `.py` 文件。调试路径 (Path)问题时先检查 `Path.cwd()`。

如果配置文件应相对于当前脚本定位：

```python
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = MODULE_DIR / "config.json"
```

### `os`、`shutil` 与 `tempfile`

`pathlib` 主要处理路径 (Path)；`shutil` 处理高级文件操作；`tempfile` 安全创建临时资源。

```python
import shutil
from pathlib import Path

source = Path("data/raw.csv")
backup = Path("backup/raw.csv")
backup.parent.mkdir(parents=True, exist_ok=True)

# copy2 尽量保留修改时间等元数据；目标存在时会覆盖，调用前应确认策略。
shutil.copy2(source, backup)
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory(prefix="data-processing-") as temp_directory:
    temp_path = Path(temp_directory)
    intermediate = temp_path / "intermediate.json"
    intermediate.write_text("{}", encoding="utf-8")

# 离开 with 后临时目录自动清理，不应继续使用 intermediate。
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

`shutil.move()`、`Path.replace()` 和删除操作会改变文件系统状态，执行前应解析明确目标并检查冲突。

### 一、 路径 (Path)操作 (Path Operations)
路径 (Path)决定了文件或目录在文件系统中的位置，可以是绝对路径 (Absolute Path) 或相对路径 (Relative Path)。
- **绝对路径 (Path)**：从根目录开始的完整路径 (Path)。比如：
    `D:\\PythonFiles\\p01.py`
- **相对路径 (Path)**：是相对于某个位置开始的路径 (Path)。
    - `.` 表示当前目录
    - `..` 表示当前目录的上一级目录

`os` 模块 (Module)中提供了很多对目录和文件操作的函数 (Function)：
#### `os.getcwd()`
- 返回表示当前工作目录的字符串 (String)。

```Python
import os
print(os.getcwd())

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

#### `os.listdir(path)`
- 返回 `path` 指定的文件夹中包含的文件或文件夹的名字构成的列表 (List)。

```Python
import os
cwd = os.getcwd()
print(os.listdir(cwd))

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

#### `os.makedirs(name, exist_ok=False)`
- 创建目录，并且还会自动创建到达最后一级目录所需要的中间目录。
- `exist_ok` 为 `False` (默认值)，表示如果目标目录已存在将引发 `FileExistsError`。

```Python
import os
os.makedirs('./dir1/dir2/dir3')
```

#### `os.path.basename(path)`
- 返回路径 (Path) `path` 最后一级的名称，通常用来返回文件名。

```Python
import os
print(os.path.basename('./dir3/dir2/dir1/a.txt'))

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

#### `os.path.dirname(path)`
- 返回路径 (Path) `path` 的目录名称。

```Python
import os
print(os.path.dirname('./dir3/dir2/dir1/a.txt'))

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

#### `os.path.split(path)`
- 把路径 (Path)分割成 `dirname` 和 `basename`，返回一个元组 (Tuple)。

```Python
import os
print(os.path.split('./dir3/dir2/dir1/a.txt'))

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

#### `os.path.splitext(path)`
- 把路径 (Path)中的扩展名分割出来，返回一个元组 (Tuple)。

```Python
import os
print(os.path.splitext('./dir3/dir2/dirl/a.txt'))

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

#### `os.path.exists(path)`
- `path` 路径 (Path)存在则返回 `True`，不存在则返回 `False`。

```Python
import os
p = r'D:\\PythonFiles\\p01.py'
print(os.path.exists(p))

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

#### `os.path.isfile(path)`
- 判断路径 (Path)是否为文件。

```Python
import os
print(os.path.isfile("./dir3/dir2/dir1/a.txt"))

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

#### `os.path.isdir(path)`
- 判断路径 (Path)是否为目录。

```Python
import os
print(os.path.isdir("./dir3/dir2/dir1"))

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

#### `os.path.join(path, *paths)`
- 智能地拼接 (Concatenation)一个或多个路径 (Path)部分。

```Python
import os
p1 = 'D:\\\\PythonFiles\\\\'
p2 = r'dir1\\dir2\\dir3'
p3 = 'p01.py'
print(os.path.join(p1, p2, p3))

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

---
### 二、 文件读写 (File Read & Write)
#### 文本文件 (Text File)读写

```python
from pathlib import Path

path = Path("notes.txt")

# 明确 encoding，避免代码换到另一台机器后出现乱码。
path.write_text("第一行\n第二行\n", encoding="utf-8")
content = path.read_text(encoding="utf-8")
print(content)
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

处理大文件时逐行读取，避免一次把整个文件加载进内存：

```python
from pathlib import Path

with Path("large.log").open("r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        if "ERROR" in line:
            print(line_number, line.rstrip())
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

常用模式：

| 模式 | 含义 | 风险 |
|---|---|---|
| `r` | 读取 | 文件不存在会报错 |
| `w` | 覆盖写入 | 原内容会被清空 |
| `a` | 追加写入 | 新内容写到末尾 |
| `x` | 仅新建 | 文件已存在会报错，可防止误覆盖 |
| `b` | 二进制模式 | 图片、模型权重等需要使用 |

#### JSON 与二进制文件 (Binary File)

```python
import json
from pathlib import Path

config = {"batch_size": 32, "learning_rate": 0.001}
path = Path("config.json")

with path.open("w", encoding="utf-8") as file:
    # ensure_ascii=False 让中文保持可读；indent 便于版本控制查看差异。
    json.dump(config, file, ensure_ascii=False, indent=2)

with path.open("r", encoding="utf-8") as file:
    loaded_config = json.load(file)
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

复制二进制文件 (Binary File)不要先解码 (Decoding)为文本：

```python
from pathlib import Path

source = Path("model.bin")
target = Path("model-copy.bin")
target.write_bytes(source.read_bytes())
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

大文件复制应使用 `shutil.copy2()`，避免一次性读入内存。

#### CSV (Comma-Separated Values) 标准库读写

简单 CSV 可使用标准库 `csv`；数据分析和复杂缺失值 (Missing Value)处理参见 [[08-Pandas 数据处理（Pandas）]]。

```python
import csv
from pathlib import Path

rows = [
    {"name": "Ada", "score": 0.9},
    {"name": "Lin", "score": 0.8},
]

with Path("scores.csv").open("w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "score"])
    writer.writeheader()
    writer.writerows(rows)
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

`newline=""` 让 `csv` 模块 (Module)统一处理换行，尤其能避免 Windows 出现额外空行。

#### 安全与边界条件

- 覆盖或删除前，先解析并验证目标路径 (Path)。
- 不要把未经检查的用户输入直接拼进文件路径 (Path)，防止 `../` 路径 (Path)穿越。
- 写关键文件时可以先写临时文件，成功后再替换目标，减少中途崩溃造成的损坏。
- 需要处理 CSV/Excel 时优先使用 [[08-Pandas 数据处理（Pandas）]]，不要手工拆分字符串 (String)。
- 资源管理优先使用 `with`，参见 [[03-错误与异常（Errors and Exceptions）]]。

从文件的编码 (Encoding)方式来看，文件可以分为文本文件 (Text File) 和二进制文件 (Binary File)。
- **文本文件 (Text File)**：`txt`、`html`、`json` 等；
- **二进制文件 (Binary File)**：图片、音频、视频等。
#### `open(file, mode='r', encoding=None)`
- `file`: 文件路径 (Path)
- `mode`: 文件打开的模式，默认为 `'r'` 模式
- `encoding`: 指定文本文件 (Text File)的编码 (Encoding)方式 (Encoding)，默认依赖系统，处理非 ASCII 文本时，`"UTF-8"` 通常是首选编码 (Encoding)。
- 打开指定的文件，返回一个文件对象 (File Object)，该对象为迭代器 (Iterator)对象 (Iterator Object)。
当前 `open` 以默认模式打开指定的文件，返回一个文件对象 (File Object)，该对象为迭代器 (Iterator)对象，每次迭代会返回该文件中的一行数据。

```Python
file = open('./exam.txt')
print(next(file))
for i in file:
    print(i)
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

#### `mode` 常用模式：

|模式|描述|
|---|---|
|`r`|以只读方式打开文件。文件的指针将会放在文件的开头。|
|`w`|打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新的文件再写入。|
|`a`|打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。|
|`+`|如果要以读写模式打开，加上 `+` 即可，比如：`r+`、`w+`、`a+`|

---
### 三、 `file` 常用对象方法
#### 文件对象 (File Object) 详细方法

| 方法 | 用途 | 重要边界 |
|---|---|---|
| `read(size=-1)` | 读取指定数量字符/字节 | 大文件不要无条件全部读取 |
| `readline()` | 读取一行 | 返回值 (Return Value)通常保留换行符 |
| `readlines()` | 读取所有行到列表 (List) | 大文件占用大量内存 |
| `write(data)` | 写入并返回字符/字节数 | 文本/二进制模式类型必须匹配 |
| `writelines(lines)` | 写入可迭代行 | 不会自动添加换行符 |
| `flush()` | 把 Python 缓冲写入操作系统 | 不等于保证磁盘物理落盘 |
| `seek(offset, whence)` | 移动文件位置 | 文本模式只保证有限形式的定位 |
| `tell()` | 返回当前位置 | 文本模式值不一定是简单字符数 |
| `close()` | 刷新并关闭 | `with` 会自动调用 |

```python
from pathlib import Path

lines = ["first\n", "second\n"]
with Path("output.txt").open("w", encoding="utf-8", newline="") as file:
    file.writelines(lines)
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

#### `file.read(size=-1)`
- 从 `file` 中读取至多 `size` 个字符并返回。
- 如果 `size` 为负值或 `None`，则读取至 EOF (End Of File)。

```Python
with open(r"./t01.txt") as file:
    print(file.read(5))
    print(file.read(2))
    print(file.read())
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

#### `file.write(s)`
- 将字符串 (String) `s` 写入并返回写入的字符数。

```Python
with open(r"./t01.txt", mode='a') as file:
    num = file.write('\\nhello baby')
    print(num)
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

#### `file.flush()`
- 刷新缓冲区 (Buffer)，即将缓冲区中的数据立刻写入文件，同时清空缓冲区，不需要被动的等待缓冲区写入。一般情况下，文件关闭后会自动刷新缓冲区，但有时你需要在关闭前刷新它，这时就可以使用 `flush()` 方法。

```Python
import time
file = open(r"./t01.txt", mode='a')
file.write('\\n123456789')
time.sleep(5) # 文件需要等到关闭文件时才会把数据从缓冲区写入文件
file.close() # 关闭文件,自动刷新缓冲区,数据才写入文件
file = open(r"./t01.txt", mode='a')
file.write('\\n123456789')
file.flush() # 刷新缓冲区,数据立刻写入文件
time.sleep(5)
file.close()
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

#### `file.close()`
- 刷新缓冲区并关闭该文件。如果文件已经关闭，则此方法无效。
- 文件关闭后，对文件的任何操作（如：读取或写入）都会引发异常 (Exception) `ValueError`。

```Python
file = open(r'./t01.txt')
print(file.read())
file.close()
file.read() # 引发ValueError
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

#### `file.seek(offset)`
- 移动文件指针到指定位置。

```Python
with open('./exam.txt', mode='w+') as file:
    file.write('hello\\nworld')
    file.seek(7)
    print(file.read()) # 'world'
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

---
### 四、 `with` 语句 (With Statement)
#### 原子写入 (Atomic Write) 思路

关键配置不应直接覆盖：如果写入中途崩溃，目标可能只剩半个文件。更安全的流程是同目录写临时文件，刷新成功后再替换。

```python
import json
from pathlib import Path


def save_json_atomically(path: Path, data: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")

    with temporary.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.flush()

    # 同一文件系统内 replace 通常是原子替换；目标存在时会被覆盖。
    temporary.replace(path)
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

严格持久化还涉及 `os.fsync()`、目录同步和跨文件系统行为，普通学习项目先掌握“临时文件 + 替换”的故障模型。

这种常规写法如果在 `open` 之后 `close` 之前发生未知的异常 (Exception)，就不能确保打开的文件一定被正常关闭，这显然不是一个好的做法：

```Python
file = open(r'./t01.txt', mode='w')
file.write('hello world')
## ...
file.close()
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

所以可以使用下面这种写法，确保 `close` 一定会被执行：

```Python
file = open(r'./t01.txt', mode='w')
try:
    file.write('hello world')
finally:
    file.close()
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

用 `with` 语句将会是一种更加简洁、优雅的方式：

```Python
with open(r'./t01.txt', mode='w') as file:
    file.write('hello world')
```

> **外部副作用（External Side Effect）**：该示例会读取、创建或修改外部资源，其结果取决于文件系统或运行环境，因此不规定固定控制台输出（Console Output）。

## 进阶补充与核对（Advanced Supplements and Verification）
### 完成检查

- [ ] 能解释模块 (Module)、导入包和发行包 (Distribution Package)的区别。
- [ ] 能解释 `__name__ == "__main__"` 的用途。
- [ ] 能用 `Path` 创建、组合 (Composition)、检查和遍历路径 (Path)。
- [ ] 能正确选择文本/二进制模式和文件打开模式。
- [ ] 知道相对路径 (Path)为什么会随工作目录变化。

### 参考资料

- [Python 官方教程：Modules](https://docs.python.org/3/tutorial/modules.html)
- [Python 标准库：pathlib](https://docs.python.org/3/library/pathlib.html)
- [Python 官方教程：Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
