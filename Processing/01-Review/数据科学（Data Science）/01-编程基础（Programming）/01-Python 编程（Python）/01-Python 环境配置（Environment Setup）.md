---
title: Python 环境配置（Environment Setup）
aliases:
  - Python 环境搭建
  - 环境配置
status: review
detail_level: comprehensive
source:
  - Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/环境配置.md
suggested_target: Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/01-Python 环境配置（Environment Setup）.md
operation: 新建
merge_target: null
---

# Python 环境配置（Environment Setup）

## 1. 需要区分的三个概念

- **解释器（Interpreter）**：真正执行 Python 程序的程序，例如 CPython。
- **虚拟环境（Virtual Environment）**：为一个项目隔离解释器和第三方依赖。
- **编辑器/IDE**：编写和调试代码的工具，例如 VS Code、PyCharm、Jupyter。

Python 源码通常会先编译为字节码，再由 Python 虚拟机执行。因此把 Python 简化成“只逐行解释、不经过编译”并不准确。

## 2. 推荐选择

| 场景 | 推荐方案 | 原因 |
|---|---|---|
| 普通 Python 项目 | 官方 Python + `venv` + `pip` | 标准库自带，轻量且通用 |
| 数据科学 Notebook | `venv` 或 Conda | 两者都可以；团队保持一致更重要 |
| CUDA、复杂二进制依赖 | Conda/Mamba | 更适合管理非 Python 依赖 |
| 在线临时实验 | Google Colab 等托管环境 | 无需先处理本机驱动和环境 |

> [!tip]
> 初学阶段优先掌握 `venv`。只有项目确实需要 Conda 时再切换，避免同时学习多套环境工具。

## 3. 使用 `venv` 创建项目环境

### macOS / Linux

```bash
# 在项目根目录创建 .venv。把环境放在项目内，IDE 更容易自动识别。
python3 -m venv .venv

# 激活后，python 和 pip 会指向当前项目的隔离环境。
source .venv/bin/activate

python --version
python -m pip --version
```

### Windows PowerShell

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
> 不要把 `.venv/` 提交到 Git。虚拟环境包含平台相关文件，应通过依赖清单重建。

`.gitignore`：

```gitignore
.venv/
__pycache__/
*.py[cod]
.ipynb_checkpoints/
```

## 4. 安装和记录依赖

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

## 5. Conda 的最小用法

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
> 不要随意固定教程中的旧版本号，例如 Python 3.7 或很旧的 NumPy。只有项目兼容性明确要求时才锁定旧版本。

## 6. IDE 与 Notebook

### VS Code / PyCharm

核心操作只有两个：

1. 打开项目根目录。
2. 把 Python Interpreter 指向项目内的 `.venv`。

验证 IDE 使用了正确解释器：

```python
import sys

# 该路径应该落在当前项目的 .venv 内；否则 IDE 可能选错了解释器。
print(sys.executable)
print(sys.version)
```

### Jupyter

```bash
python -m pip install jupyterlab ipykernel

# 注册独立内核后，Notebook 可以明确选择当前项目环境。
python -m ipykernel install --user \
  --name ds-project \
  --display-name "Python (ds-project)"
```

在 Notebook 中安装包时，优先使用 `%pip install package`，因为它会使用当前内核对应的环境。

## 7. 常见问题排查

### 安装成功但无法导入

```ipython
import sys

print(sys.executable)
```

然后在终端执行：

```bash
python -m pip show package-name
```

如果两边的 Python 环境不同，就是典型的“装到了 A 环境，却在 B 环境运行”。

### 不要使用 `sudo pip install`

这可能覆盖系统管理的 Python 包。遇到权限错误时，应创建虚拟环境，而不是提升权限。

### 环境可以激活，但 IDE 仍然报错

终端环境和 IDE 解释器是两个设置。需要在 IDE 中重新选择 `.venv`，然后重启语言服务或 Notebook 内核。

## 8. Python 解释器 (Python Interpreter) 的查找顺序

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
```

## 9. 依赖清单 (Dependency Manifest) 的层次

| 文件 | 适用场景 | 说明 |
|---|---|---|
| `requirements.txt` | 简单应用、环境快照 | `pip install -r` 可直接重建 |
| `pyproject.toml` | 可安装项目、库、现代工具配置 | 声明项目元数据和直接依赖 |
| 锁文件 (Lock File) | 需要完全固定依赖解析结果 | 由 uv、Poetry、PDM 等工具生成 |
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

## 10. 包安装 (Package Installation) 的排错顺序

1. 确认解释器 (Interpreter)：`python -c "import sys; print(sys.executable)"`。
2. 确认 pip (Package Installer)：`python -m pip --version`。
3. 查看包信息：`python -m pip show package-name`。
4. 查看依赖冲突：`python -m pip check`。
5. 再检查网络、代理 (Proxy)、镜像源 (Mirror) 和编译工具链 (Build Toolchain)。

```bash
python -m pip check
python -m pip list --outdated
python -m pip install --verbose package-name
```

遇到二进制扩展 (Binary Extension) 构建失败时，错误原因可能不是 Python 代码，而是缺少编译器、系统头文件或兼容的 Wheel (Wheel Package)。

## 11. Notebook 内核 (Notebook Kernel) 常见陷阱

Notebook 页面显示的环境名称不一定等于启动 Jupyter 的终端环境。真正执行代码的是当前选中的内核 (Kernel)。

```ipython
import sys

print(sys.executable)

# 在 Notebook 中使用当前内核安装包，避免装到另一个 Python。
%pip install pandas
```

修改包版本后应重启内核 (Restart Kernel)，否则内存中可能仍保留旧模块对象。

## 12. 调试器 (Debugger) 基础

断点调试 (Breakpoint Debugging) 应重点观察：

- 当前调用栈 (Call Stack)。
- 局部变量 (Local Variables) 和对象类型。
- 条件分支是否按预期进入。
- 循环变量和张量形状是否在某次迭代变化。
- 异常断点 (Exception Breakpoint) 是否停在异常第一次抛出的位置。

标准库也提供 `breakpoint()`：

```python
def calculate(value: int) -> int:
    result = value * 2
    breakpoint()  # 调试完成后应删除，避免生产程序意外暂停。
    return result
```

## 13. 完成检查

- [ ] 能创建、激活、退出和删除虚拟环境。
- [ ] 能解释为什么使用 `python -m pip`。
- [ ] 能确认终端、IDE 和 Notebook 使用的是同一个解释器。
- [ ] 能用依赖文件在新目录中重建环境。
- [ ] 知道什么时候使用 `venv`，什么时候考虑 Conda。

## 参考资料

- [Python Packaging User Guide：使用 pip 和 venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
- [Python 官方教程：虚拟环境与包](https://docs.python.org/3/tutorial/venv.html)
