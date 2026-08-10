---
title: 文件、路径、模块与包（Files Paths Modules and Packages）
aliases:
  - 文件、路径操作、模块与包
status: review
detail_level: comprehensive
source:
  - Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/文件、路径操作、模块与包.md
suggested_target: Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/04-文件、路径、模块与包（Files Paths Modules and Packages）.md
operation: 新建
merge_target: null
---

# 文件、路径、模块与包（Files Paths Modules and Packages）

## 1. 模块、包和发行包

- **模块（Module）**：一个可导入的 Python 文件，例如 `metrics.py`。
- **导入包（Import Package）**：组织模块的目录结构。
- **发行包（Distribution Package）**：通过 `pip` 安装的项目，例如 `scikit-learn`；它的安装名不一定等于导入名。

传统包通常包含 `__init__.py`，但现代 Python 也支持没有该文件的命名空间包，因此“包一定有 `__init__.py`”不是绝对规则。

## 2. 导入方式

```python
import math
import numpy as np
from pathlib import Path
from collections import Counter as FrequencyCounter
```

使用原则：

- 导入通常放在文件顶部：标准库、第三方库、本地模块分组排列。
- 避免 `from module import *`，因为它会污染当前命名空间并隐藏名称来源。
- 不要为了让导入成功就在程序中随意修改 `sys.path`；应修正项目结构或安装方式。
- 避免让本地文件与标准库或第三方库同名，例如 `json.py`、`numpy.py`。

## 3. `__name__ == "__main__"`

模块被直接运行时，`__name__` 是 `"__main__"`；被其他模块导入时，`__name__` 是模块名。

```python
def main() -> None:
    print("运行命令行入口")


if __name__ == "__main__":
    # 把入口放进判断中，导入这个模块时就不会意外执行任务。
    main()
```

## 4. 推荐项目结构

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

把可复用逻辑放在模块中，把 Notebook 当作探索和展示入口，可以减少复制粘贴。

## 5. 使用 `pathlib` 操作路径

`pathlib.Path` 能跨 Windows、macOS 和 Linux 组合路径，通常比手动拼接字符串更安全。

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

遍历文件：

```python
from pathlib import Path

for csv_path in Path("data").glob("*.csv"):
    print(csv_path)

for image_path in Path("images").rglob("*.png"):
    # rglob 会递归搜索子目录，大目录中使用时要注意成本。
    print(image_path)
```

> [!warning]
> 相对路径默认相对于“当前工作目录”，不一定相对于当前 `.py` 文件。调试路径问题时先检查 `Path.cwd()`。

如果配置文件应相对于当前脚本定位：

```python
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = MODULE_DIR / "config.json"
```

## 6. 文本文件读写

```python
from pathlib import Path

path = Path("notes.txt")

# 明确 encoding，避免代码换到另一台机器后出现乱码。
path.write_text("第一行\n第二行\n", encoding="utf-8")
content = path.read_text(encoding="utf-8")
print(content)
```

处理大文件时逐行读取，避免一次把整个文件加载进内存：

```python
from pathlib import Path

with Path("large.log").open("r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        if "ERROR" in line:
            print(line_number, line.rstrip())
```

常用模式：

| 模式 | 含义 | 风险 |
|---|---|---|
| `r` | 读取 | 文件不存在会报错 |
| `w` | 覆盖写入 | 原内容会被清空 |
| `a` | 追加写入 | 新内容写到末尾 |
| `x` | 仅新建 | 文件已存在会报错，可防止误覆盖 |
| `b` | 二进制模式 | 图片、模型权重等需要使用 |

## 7. JSON 与二进制文件

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

复制二进制文件不要先解码为文本：

```python
from pathlib import Path

source = Path("model.bin")
target = Path("model-copy.bin")
target.write_bytes(source.read_bytes())
```

大文件复制应使用 `shutil.copy2()`，避免一次性读入内存。

## 8. 文件对象 (File Object) 详细方法

| 方法 | 用途 | 重要边界 |
|---|---|---|
| `read(size=-1)` | 读取指定数量字符/字节 | 大文件不要无条件全部读取 |
| `readline()` | 读取一行 | 返回值通常保留换行符 |
| `readlines()` | 读取所有行到列表 | 大文件占用大量内存 |
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

## 9. `os`、`shutil` 与 `tempfile`

`pathlib` 主要处理路径；`shutil` 处理高级文件操作；`tempfile` 安全创建临时资源。

```python
import shutil
from pathlib import Path

source = Path("data/raw.csv")
backup = Path("backup/raw.csv")
backup.parent.mkdir(parents=True, exist_ok=True)

# copy2 尽量保留修改时间等元数据；目标存在时会覆盖，调用前应确认策略。
shutil.copy2(source, backup)
```

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory(prefix="data-processing-") as temp_directory:
    temp_path = Path(temp_directory)
    intermediate = temp_path / "intermediate.json"
    intermediate.write_text("{}", encoding="utf-8")

# 离开 with 后临时目录自动清理，不应继续使用 intermediate。
```

`shutil.move()`、`Path.replace()` 和删除操作会改变文件系统状态，执行前应解析明确目标并检查冲突。

## 10. CSV (Comma-Separated Values) 标准库读写

简单 CSV 可使用标准库 `csv`；数据分析和复杂缺失值处理参见 [[08-Pandas 数据处理（Pandas）]]。

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

`newline=""` 让 `csv` 模块统一处理换行，尤其能避免 Windows 出现额外空行。

## 11. 原子写入 (Atomic Write) 思路

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

严格持久化还涉及 `os.fsync()`、目录同步和跨文件系统行为，普通学习项目先掌握“临时文件 + 替换”的故障模型。

## 12. 安全与边界条件

- 覆盖或删除前，先解析并验证目标路径。
- 不要把未经检查的用户输入直接拼进文件路径，防止 `../` 路径穿越。
- 写关键文件时可以先写临时文件，成功后再替换目标，减少中途崩溃造成的损坏。
- 需要处理 CSV/Excel 时优先使用 [[08-Pandas 数据处理（Pandas）]]，不要手工拆分字符串。
- 资源管理优先使用 `with`，参见 [[03-错误与异常（Errors and Exceptions）]]。

## 13. 完成检查

- [ ] 能解释模块、导入包和发行包的区别。
- [ ] 能解释 `__name__ == "__main__"` 的用途。
- [ ] 能用 `Path` 创建、组合、检查和遍历路径。
- [ ] 能正确选择文本/二进制模式和文件打开模式。
- [ ] 知道相对路径为什么会随工作目录变化。

## 参考资料

- [Python 官方教程：Modules](https://docs.python.org/3/tutorial/modules.html)
- [Python 标准库：pathlib](https://docs.python.org/3/library/pathlib.html)
- [Python 官方教程：Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
