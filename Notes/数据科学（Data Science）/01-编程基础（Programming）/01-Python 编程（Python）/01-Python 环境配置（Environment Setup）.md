---
title: Python 环境配置（Environment Setup）
aliases:
  - Python 环境搭建
  - 环境配置
status: published
detail_level: comprehensive
merge_policy: union-zero-loss
reviewed_at: 2026-08-11
published_at: 2026-08-11
source:
  - Processing/02-Processed/2026-08-11-Python编程/originals/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/环境配置.md
---

# Python 环境配置（Environment Setup）
## Python 入门与环境搭建 (Mac版)
### 结构化补充（Structured Supplement）：常见问题排查
#### 安装成功但无法导入

```ipython
import sys

print(sys.executable)

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

然后在终端执行：

```bash
python -m pip show package-name
```

如果两边的 Python 环境不同，就是典型的“装到了 A 环境，却在 B 环境运行”。

#### 不要使用 `sudo pip install`

这可能覆盖系统管理的 Python 包。遇到权限错误 (Error)时，应创建虚拟环境 (Virtual Environment)，而不是提升权限。

#### 环境可以激活，但 IDE 仍然报错

终端环境和 IDE 解释器 (Interpreter)是两个设置。需要在 IDE 中重新选择 `.venv`，然后重启语言服务或 Notebook 内核 (Kernel)。

---
### 一、 初识编程语言 (Programming Language)
#### 结构化补充（Structured Supplement）：需要区分的三个概念

- **解释器（Interpreter）**：真正执行 Python 程序的程序，例如 CPython。
- **虚拟环境（Virtual Environment）**：为一个项目隔离解释器 (Interpreter)和第三方依赖。
- **编辑器/IDE**：编写和调试代码的工具，例如 VS Code、PyCharm、Jupyter。

Python 源码通常会先编译为字节码，再由 Python 虚拟机执行。因此把 Python 简化成“只逐行解释、不经过编译”并不准确。

#### 1. 什么是编程语言 (Programming Language)
用来和计算机交流、控制计算机，让计算机按照我们的要求做事情，这样的语言叫做编程语言 (Programming Language)。
#### 2. 发展历程
计算机语言经历了3个阶段：
1. **机器语言 (Machine Language)**: 用二进制编码 (Encoding)表示的机器指令，是 CPU 能直接识别并执行的唯一一种语言。
1. **汇编语言 (Assembly Language)**: 符号语言。用与机器指令含义相近的英文缩写、字母和数字等符号来取代机器指令。
1. **高级语言 (High-level Language)**: 面向用户的语言，更接近人类的自然语言，通用性强。
#### 3. 编译型 vs 解释型
计算机 CPU 只认识机器指令，高级语言 (High-level Language)需要“翻译”。
- **编译方式**: 源代码 (Source Code) -> 编译器 (Compiler) -> **目标程序文件** -> 计算机执行。执行速度快。
- **解释方式**: 源代码 (Source Code) -> 解释器 (Interpreter) -> **逐句翻译并执行** (不产生目标文件)。
- **Python 属于**: **解释型语言 (Interpreted Language)**。
---
### 二、 Python 简介
#### 1. 诞生背景
- **作者**: Guido van Rossum ("龟叔")。
- **时间**: 1989 年圣诞节期间，为了打发无聊时间而编写。
- **地位**: TIOBE 排行榜常年第一 (Jan 2025/2026 数据)。
#### 2. Python 之禅 (Zen of Python)
Python 设计的原则与哲学，可以通过代码 `import this` 查看。
```Python
import this
## 翻译摘要：
## Beautiful is better than ugly. (优美胜于丑陋)
## Explicit is better than implicit. (明了胜于晦涩)
## Simple is better than complex. (简洁胜于复杂)
## Readability counts. (可读性很重要)
```
---
### 三、 环境搭建 (Environment Setup)
#### 1. Python 安装
##### 结构化补充（Structured Supplement）：推荐选择

| 场景 | 推荐方案 | 原因 |
|---|---|---|
| 普通 Python 项目 | 官方 Python + `venv` + `pip` | 标准库自带，轻量且通用 |
| 数据科学 Notebook | `venv` 或 Conda | 两者都可以；团队保持一致更重要 |
| CUDA、复杂二进制依赖 | Conda/Mamba | 更适合管理非 Python 依赖 |
| 在线临时实验 | Google Colab 等托管环境 | 无需先处理本机驱动和环境 |

> [!tip]
> 初学阶段优先掌握 `venv`。只有项目确实需要 Conda 时再切换，避免同时学习多套环境工具。

##### 结构化补充（Structured Supplement）：Python 解释器 (Python Interpreter) 的查找顺序

激活虚拟环境 (Virtual Environment) 的本质之一，是把该环境的可执行目录放到 `PATH` 环境变量 (Environment Variable) 前面。

```bash
# macOS / Linux
which -a python python3

# 查看当前 shell 实际执行的命令位置。
command -v python
```

```powershell
# Windows
where.exe python
py --list
```

在程序内部检查：

```python
import site
import sys

print(sys.executable)
print(sys.prefix)
print(sys.base_prefix)
print(site.getsitepackages())

# 虚拟环境中 sys.prefix 通常与 sys.base_prefix 不同。
inside_virtual_environment = sys.prefix != sys.base_prefix
print(inside_virtual_environment)

# 输出说明: 解释器路径、环境前缀和 site-packages 路径由本机环境决定；
# 最后一行在虚拟环境中通常为 True，在系统解释器中通常为 False。
```

- **推荐方案**: 安装 **Anaconda**。

    - **理由**: 开源发行版 (Distribution)，包含 Python 解释器 (Interpreter)、Conda 包管理器 (Package Manager)以及 180+ 科学包，比单独安装省事。

    - **下载**: [Anaconda 官网](https://www.anaconda.com/download) 或 [清华镜像 (推荐)](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/?C=M&O=D)。

#### 2. IDE 安装 (集成开发环境 (Integrated Development Environment, IDE))
##### 结构化补充（Structured Supplement）：IDE 与 Notebook
###### VS Code / PyCharm

核心操作只有两个：

1. 打开项目根目录。
2. 把 Python Interpreter 指向项目内的 `.venv`。

验证 IDE 使用了正确解释器 (Interpreter)：

```python
import sys

# 该路径应该落在当前项目的 .venv 内；否则 IDE 可能选错了解释器。
print(sys.executable)
print(sys.version)

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```

###### Jupyter

```bash
python -m pip install jupyterlab ipykernel

# 注册独立内核后，Notebook 可以明确选择当前项目环境。
python -m ipykernel install --user \
  --name ds-project \
  --display-name "Python (ds-project)"
```

在 Notebook 中安装包时，优先使用 `%pip install package`，因为它会使用当前内核 (Kernel)对应的环境。

##### 结构化补充（Structured Supplement）：Notebook 内核 (Notebook Kernel) 常见陷阱

Notebook 页面显示的环境名称不一定等于启动 Jupyter 的终端环境。真正执行代码的是当前选中的内核 (Kernel)。

```ipython
import sys

print(sys.executable)

# 在 Notebook 中使用当前内核安装包，避免装到另一个 Python。
%pip install pandas
```

修改包版本 (Version)后应重启内核 (Restart Kernel)，否则内存中可能仍保留旧模块 (Module)对象。

IDE 集成了编码 (Encoding)、分析、编译、调试等功能。
- **主流选择**: PyCharm, VSCode, Jupyter。
- **PyCharm**: 推荐使用，功能强大。
---
### 四、 PyCharm 常用快捷键 (Mac 适配版)

> 注意: 已将课程资料中的 Windows 键位转换为 Mac 常用键位。
#### 1. 编辑与操作

|功能|Windows (原资料)|**Mac (适配)**|
|---|---|---|
|**全选**|Ctrl + A|**Cmd + A**|
|**复制**|Ctrl + C|**Cmd + C**|
|**粘贴**|Ctrl + V|**Cmd + V**|
|**剪切**|Ctrl + X|**Cmd + X**|
|**撤销**|Ctrl + Z|**Cmd + Z**|
|**重做**|Ctrl + Y|**Cmd + Shift + Z**|
|**查找**|Ctrl + F|**Cmd + F**|
|**替换**|Ctrl + R|**Cmd + R**|
|**缩进**|Tab|**Tab**|
|**取消缩进**|Shift + Tab|**Shift + Tab**|

#### 2. 光标与行移动

|功能|Windows (原资料)|**Mac (适配)**|
|---|---|---|
|**移到行首**|Home|**Cmd + ←** or **Fn + ←**|
|**移到行尾**|End|**Cmd + →** or **Fn + →**|
|**整行上下移动**|Ctrl + Shift + ↑/↓|**Opt + Shift + ↑/↓**|
|**下方新建一行**|Shift + Enter|**Shift + Enter**|
|**上方新建一行**|Ctrl + Alt + Enter|**Cmd + Opt + Enter**|

#### 3. 运行与调试
- **运行**: Mac 上通常直接使用 **Ctrl + R** 或 **Ctrl + Shift + R** (取决于设置)，也可以在上下文菜单中选择 Run。
- **中断**: **Ctrl + C** (在 Terminal 中死循环时使用)。
#### 4. 代码调试示例 (Debug)
##### 结构化补充（Structured Supplement）：调试器 (Debugger) 基础

断点 (Breakpoint)调试 (Breakpoint Debugging) 应重点观察：

- 当前调用栈 (Call Stack)。
- 局部变量 (Local Variables) 和对象类型。
- 条件分支是否按预期进入。
- 循环变量 (Variable)和张量形状是否在某次迭代变化。
- 异常 (Exception)断点 (Exception Breakpoint) 是否停在异常 (Exception)第一次抛出的位置。

标准库也提供 `breakpoint()`：

```python
def calculate(value: int) -> int:
    result = value * 2
    breakpoint()  # 调试完成后应删除，避免生产程序意外暂停。
    return result
```

PyCharm 可以通过断点 (Breakpoint)查看代码执行流程。
```Python
## 示例代码
def add(left, right):
    print("执行第8行啦")
    print("执行第9行啦", left + right)
print("执行第1行啦")
print(2/1)
## 调用函数
add(3, 4)

# 期望输出:
# 执行第1行啦
# 2.0
# 执行第8行啦
# 执行第9行啦 7
```
### Python 之禅与基础语法
#### 一、 Python 之禅 (The Zen of Python)
在 Python 终端或编辑器中输入并运行 `import this`，会输出一段名为 **Python 之禅** 的文字。它是 Python 语言的设计哲学和准则，作者是 Tim Peters。
- **核心理念**：

    - **优美胜于丑陋** (Beautiful is better than ugly)：追求代码的简洁与美感。

    - **明了胜于晦涩** (Explicit is better than implicit)：代码逻辑应清晰可见，不应隐藏意图。

    - **简洁胜于复杂** (Simple is better than complex)：尽量用最简单的方式解决问题。

    - **可读性很重要** (Readability counts)：代码是写给人看的，要符合大众风格。

    - **扁平胜于嵌套** (Flat is better than nested)：避免过深的逻辑嵌套。

```Python
import this
## 执行后输出：The Zen of Python, by Tim Peters...
```
---
#### 二、 模块 (Module)、包 (Package) 与 库 (Library)
**1. 关键字 (Keyword)：**`import`
`import` 是 Python 官方预定义的具有特殊功能的单词（共 35 个），专门用于**导入**模块 (Module)或包。
**2. 概念辨析**
- **模块 (Module)**：本质上就是一个 `.py` 后缀的 **Python 文件**（例如 `this.py`）。
- **包 (Package)**：本质上是一个包含多个模块 (Module)的 **文件夹**，用于分区管理和避免命名冲突。
- **库 (Library)**：功能相对专一的包。

    - _常用的库_：`numpy` (科学计算), `pandas` (数据分析), `matplotlib` (数据可视化)。

**3. 导入语法**
```Python
import 模块名
## 注意：不需要加 .py 后缀，例如：import this
```

> **Mac 快捷键提示**：在 PyCharm 中，按住 `Command ⌘` 键并点击模块 (Module)名（如 `this`），可以跳转查看该模块 (Module)的源代码 (Source Code)。
---
#### 三、 变量 (Variable) 的定义与使用
**1. 定义变量 (Variable)的三要素**
```Python
## 变量名 = 数据内容
number = 789
```
- **变量 (Variable)名** (Variable Name)：等号左边。由字母、数字、下划线组成，**不能以数字开头**。
- **赋值符号** (`=`): 将右边的数据关联到左边的名称上。
- **值/数据** (Value/Data)：等号右边的内容。
**2. 重要原则**
- **先定义，后使用**：必须先给变量 (Variable)赋值，之后才能调用，否则会报 `NameError` (名字错误 (Error))。
---
#### 四、 基础数据类型 (Data Type)初步
**1. 字符串 (String)**
用于表示文本数据，也是数据的一种。
- **单行字符串 (String)**：用一对单引号 `' '` 或双引号 `" "` 包裹。
- **多行字符串 (String)**：用一对三单引号 `''' '''` 或三双引号 `""" """` 包裹。
```Python
## 单行定义
s1 = 'Hello Mac'
s2 = "Python"
## 多行定义 (保留换行格式)
s3 = """
这是
多行内容
"""
```
---
#### 五、 模块 (Module)导入的底层逻辑
- **首次导入即执行**：当一个模块（如 `this.py`）**第一次**被 `import` 时，解释器 (Interpreter)会从头到尾执行该模块 (Module)内的所有代码。

    - 这就是为什么执行 `import this` 会直接打印出文字的原因（因为 `this.py` 内部包含了 `print` 语句）。

    - 重复导入不会重复执行。

- **成员访问**：使用 `模块名.变量名` 的形式访问模块 (Module)内定义好的变量 (Variable)。
```Python
import this
## this.py 内部定义了变量 s (字符串) 和 d (字典)
print(this.s)  # 访问并打印 this 模块中的变量 s (即经过加密处理后的 Zen of Python 原文)
print(this.d)  # 访问 this 模块中的变量 d
```
---
#### 六、 注释 (Comment) & Mac 快捷键
注释是给开发者看的备注，解释器 (Interpreter)运行时会完全忽略它们。
- **单行注释**：使用 `#` 开头。
- **多行注释**：使用三引号包裹（如果没有赋值给变量 (Variable)，它就是注释）。
```Python
## 这是一个单行注释，程序不执行这里
'''
这是一个多行注释
可以写很多行
程序也不执行这里
'''
a = 10  # 注释也可以写在代码的后面
```
**Mac 专属效率工具箱**

|功能|Mac 快捷键|说明|
|---|---|---|
|**批量注释/取消注释**|`Command ⌘` + `/`|选中多行代码后使用|
|**构建多个光标**|`Option ⌥` + 鼠标左键点击|在不同位置同时输入或删除|
|**光标跳至行首**|`Command ⌘` + `←`|相当于 Windows 的 Home 键|
|**光标跳至行尾**|`Command ⌘` + `→`|相当于 Windows 的 End 键|
|**查看源码**|`Command ⌘` + 鼠标左键点击|点击变量 (Variable)名或模块 (Module)名|

## Conda 虚拟环境 (Virtual Environment)管理 (Virtual Environment Management)
### 一、 为什么需要虚拟环境 (Virtual Environment)？
#### 结构化补充（Structured Supplement）：使用 `venv` 创建项目环境
##### macOS / Linux

```bash
# 在项目根目录创建 .venv。把环境放在项目内，IDE 更容易自动识别。
python3 -m venv .venv

# 激活后，python 和 pip 会指向当前项目的隔离环境。
source .venv/bin/activate

python --version
python -m pip --version
```

##### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1

python --version
python -m pip --version
```

退出环境：

```bash
deactivate
```

> [!warning]
> 不要把 `.venv/` 提交到 Git。虚拟环境 (Virtual Environment)包含平台相关文件，应通过依赖清单 (Dependency Manifest)重建。

`.gitignore`：

```gitignore
.venv/
__pycache__/
*.py[cod]
.ipynb_checkpoints/
```

- **Base 环境 (Base Environment)**：安装 Anaconda/Miniconda 后自带的默认环境。它预装了 Python 和许多常用的第三方库 (Third-party Libraries)，如 `numpy`, `pandas` 等。
- **隔离性 (Isolation)**：

    - 不同的项目可能需要不同版本 (Version)的 Python (如 3.7 vs 3.10) 或不同版本 (Version)的库。

    - 如果所有项目都混在 Base 环境中，容易导致**包冲突 (Package Conflict)**。

    - **虚拟环境 (Virtual Environment)**允许为每个项目创建一个独立的“房间”，互不干扰。

---
### 二、 基础查询命令
在使用 Conda 前，建议 Windows 用户以**管理员身份运行 (Run as Administrator)** 命令行，避免权限问题。

|功能|命令|说明|
|---|---|---|
|**列出包**|`conda list`|列出当前激活环境中已安装的所有包|
|**列出环境**|`conda env list`|列出本机所有 Conda 环境，带 `*` 号的为当前激活环境|
|**搜索包版本 (Version)**|`conda search <package_name>`|查看某个包有哪些版本 (Version)可供下载 (如 `conda search python`)|

---
### 三、 配置镜像源 (Mirror Configuration)
由于 Conda 默认源在国外，下载速度可能较慢或失败。建议配置国内镜像（如清华源）以加速下载。
#### 1. 添加镜像源 (Add Channels)
```Bash
## 添加清华大学 Anaconda 镜像源
conda config --add channels <https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/>
```

> **注意**：如果复制时出现换行，请务必在记事本中整理成一行后再执行，否则会添加错误 (Error)的链接。
#### 2. 查看与恢复
```Bash
## 查看当前配置的所有镜像源
conda config --show channels
## 移除指定的镜像源 (如果加错了可以用这个)
conda config --remove channels <channel_url>
## 恢复默认源 (删除所有自定义镜像)
conda config --remove-key channels
```
---
### 四、 虚拟环境 (Virtual Environment)的生命周期管理
#### 结构化补充（Structured Supplement）：Conda 的最小用法

```bash
# 不要长期把所有项目都装进 base；每个项目创建独立环境。
conda create --name ds-project python=3.12
conda activate ds-project

conda install numpy pandas
conda list

conda deactivate
conda env remove --name ds-project
```

> [!warning]
> 不要随意固定教程中的旧版本 (Version)号，例如 Python 3.7 或很旧的 NumPy。只有项目兼容性明确要求时才锁定旧版本 (Version)。

#### 1. 创建环境 (Create Environment)
- **语法**：`conda create -n <环境名> python=<版本号>`
- **参数 (Parameter)**：`n` 代表 name (名字)。
```Bash
## 示例：创建一个名为 PY01 的环境，指定 Python 版本为 3.7
conda create -n PY01 python=3.7
```

> **提示**：执行后会提示即将下载的包，输入 `y` (Yes) 并回车确认安装。
#### 2. 激活与退出 (Activate & Deactivate)
```Bash
## 激活指定环境 (进入虚拟环境)
conda activate PY01
## 激活后，命令行前缀会变为 (PY01)
## 退出当前环境 (回到 Base 或上一级)
conda deactivate
```
#### 3. 删除环境 (Remove Environment)
- **注意**：**不能**在当前激活的环境中删除自己，必须先 `deactivate` 退回到 base 或其他环境。
```Bash
## 删除名为 PY01 的环境及其所有内容
conda remove -n PY01 --all
```
---
### 五、 包管理 (Package Management)
#### 结构化补充（Structured Supplement）：安装和记录依赖

```bash
# 使用 python -m pip 可以确保 pip 属于当前这个 Python 解释器。
python -m pip install --upgrade pip
python -m pip install numpy pandas matplotlib

# 查看当前环境实际安装的包。
python -m pip list

# 简单项目可以导出完整环境快照。
python -m pip freeze > requirements.txt

# 在另一台机器中重建环境。
python -m pip install -r requirements.txt
```

`requirements.txt` 适合简单项目；需要构建、发布或精细区分依赖时，再学习 `pyproject.toml`。

#### 结构化补充（Structured Supplement）：依赖清单 (Dependency Manifest) 的层次

| 文件 | 适用场景 | 说明 |
|---|---|---|
| `requirements.txt` | 简单应用、环境快照 | `pip install -r` 可直接重建 |
| `pyproject.toml` | 可安装项目、库、现代工具配置 | 声明项目元数据和直接依赖 |
| 锁文件 (Lock File) | 需要完全固定依赖解析 (Dependency Resolution)结果 | 由 uv、Poetry、PDM 等工具生成 |
| `environment.yml` | Conda 环境 | 可同时描述 Conda 与 pip 依赖 |

Conda 环境导出：

```bash
# --from-history 主要记录主动安装的顶层依赖，文件更适合跨平台共享。
conda env export --from-history > environment.yml

# 完整导出包含所有传递依赖，更接近当前机器的精确快照。
conda env export > environment-lock.yml

conda env create --file environment.yml
```

`pip freeze` 同样记录当前环境中的所有包，不区分直接依赖 (Direct Dependency) 和传递依赖 (Transitive Dependency)。

#### 结构化补充（Structured Supplement）：包安装 (Package Installation) 的排错顺序

1. 确认解释器 (Interpreter)：`python -c "import sys; print(sys.executable)"`。
2. 确认 pip (Package Installer)：`python -m pip --version`。
3. 查看包信息：`python -m pip show package-name`。
4. 查看依赖冲突 (Dependency Conflict)：`python -m pip check`。
5. 再检查网络、代理 (Proxy)、镜像源 (Mirror) 和编译工具链 (Build Toolchain)。

```bash
python -m pip check
python -m pip list --outdated
python -m pip install --verbose package-name
```

遇到二进制扩展 (Binary Extension) 构建失败时，错误 (Error)原因可能不是 Python 代码，而是缺少编译器 (Compiler)、系统头文件或兼容的 Wheel (Wheel Package)。

可以在当前环境安装，也可以指定安装到某个环境。
#### 1. 安装包 (Install Packages)
- **依赖关系 (Dependency)**：Conda 会自动处理依赖。例如安装 `pandas` 时，如果环境里没有 `numpy`，它会自动一并安装。
```Bash
## 方式 A：在当前激活的环境中安装 numpy，指定版本 1.20.1
conda install numpy=1.20.1
## 方式 B：指定安装到某个环境 (无需激活该环境)
## 将 pandas 1.3.4 安装到 PY01 环境中
conda install -n PY01 pandas=1.3.4
```
#### 2. 卸载包 (Remove/Uninstall Packages)
- **级联卸载**：如果你卸载基础包 (如 `numpy`)，依赖它的包 (如 `pandas`) 也会失效或被一并卸载。
```Bash
## 方式 A：从当前环境中移除 pandas
conda remove pandas
## 方式 B：从指定环境 (PY01) 中移除 numpy
conda remove -n PY01 numpy
```
---
### 六、 PyCharm 集成 (IDE Integration)
创建好虚拟环境 (Virtual Environment)后，需要在 PyCharm 中进行关联才能使用。
1. **打开设置**：`PyCharm` -> `Settings` (Windows) / `Preferences` (Mac) -> `Project` -> `Python Interpreter` (Python 解释器 (Interpreter))。
1. **添加解释器 (Interpreter)**：

    - 点击右侧齿轮图标或 `Add Interpreter` -> 选择 `Local` (本地)。

    - 选择 **Existing environment** (现有环境)。

1. **定位路径 (Path)**：

    - 点击浏览 (`...`)，找到你的 Conda 环境目录。

    - **路径 (Path)示例**：`Anaconda安装目录/envs/PY01/python.exe` (Windows) 或 `python` (Mac)。

    - 点击 `OK` 完成添加。

1. **切换环境**：在 PyCharm 右下角点击当前解释器 (Interpreter)名称，可以快速在 Base 和其他虚拟环境 (Virtual Environment)间切换。

## 进阶补充与核对（Advanced Supplements and Verification）
### 结构化补充（Structured Supplement）：完成检查

- [ ] 能创建、激活、退出和删除虚拟环境 (Virtual Environment)。
- [ ] 能解释为什么使用 `python -m pip`。
- [ ] 能确认终端、IDE 和 Notebook 使用的是同一个解释器 (Interpreter)。
- [ ] 能用依赖文件在新目录中重建环境。
- [ ] 知道什么时候使用 `venv`，什么时候考虑 Conda。

### 结构化补充（Structured Supplement）：参考资料

- [Python Packaging User Guide：使用 pip 和 venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
- [Python 官方教程：虚拟环境 (Virtual Environment)与包](https://docs.python.org/3/tutorial/venv.html)
