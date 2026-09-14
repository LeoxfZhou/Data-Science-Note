---
title: "Python 项目结构、配置、日志与 pytest 速查表（Python Project Structure, Configuration, Logging, and pytest Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - engineering/python-project
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "Python 3.11–3.14；pytest 8.x"
---
# Python 项目结构、配置、日志与 pytest 速查表（Python Project Structure, Configuration, Logging, and pytest Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
推荐 `src/` 布局、`pyproject.toml` 单一配置入口、结构化日志和独立测试。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 2. 第三方工程包（Third-party Engineering Packages）
### 2.1 pytest（pytest）
- **安装包（Distribution）**：`pytest`。
- **导入模块（Import Module）**：`pytest`；常用入口为 `python -m pytest`。
- **安装命令（Installation）**：`python -m pip install -U pytest`。
- **用途（Purpose）**：测试发现、断言、参数化、fixture、临时目录与异常验证。
- **正式笔记（Detailed Note）**：[[01-Python 环境配置（Environment Setup）]] 中的测试环境约定。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|参数化|`@pytest.mark.parametrize(names, cases)`|把一个测试扩展为多组用例|
|异常断言|`with pytest.raises(Error, match=...)`|验证异常类型与消息|
|fixture|`@pytest.fixture`|注册可注入的测试资源|
|临时目录|`tmp_path`|为当前测试返回独立 Path|

```python
import pytest

@pytest.mark.parametrize(("value", "expected"), [(2, 4), (3, 9)])
def test_square(value: int, expected: int) -> None:
    assert value * value == expected

# 执行 python -m pytest -q；期望两个参数化用例均通过。
```
### 2.2 python-dotenv（python-dotenv）
- **安装包（Distribution）**：`python-dotenv`。
- **导入模块（Import Module）**：`dotenv`。
- **安装命令（Installation）**：`python -m pip install -U python-dotenv`。
- **用途（Purpose）**：开发环境从 `.env` 加载环境变量；生产环境优先使用平台密钥管理。
- **正式笔记（Detailed Note）**：[[01-Python 环境配置（Environment Setup）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|查找文件|`find_dotenv(usecwd=True)`|返回 `.env` 路径或空字符串|
|加载|`load_dotenv(path, override=False)`|把变量写入进程环境并返回是否加载成功|
|只读取|`dotenv_values(path)`|返回字典，不修改进程环境|

```python
from dotenv import dotenv_values

values = dotenv_values(stream=__import__("io").StringIO("MODE=dev\n"))
print(values["MODE"])  # 输出: dev
```
- **安全边界（Security Boundary）**：`.env` 必须进入 `.gitignore`，不得把真实密钥写入示例、日志或版本库。
### 2.3 tqdm 进度条（tqdm Progress Bars）
- **安装包（Distribution）**：`tqdm`。
- **导入模块（Import Module）**：`tqdm`。
- **安装命令（Installation）**：`python -m pip install -U tqdm`。
- **用途（Purpose）**：为可迭代对象、手动循环和 Pandas 操作增加低开销进度显示。
- **正式笔记（Detailed Note）**：[[04-PyTorch 训练与评估循环（PyTorch Training and Evaluation Loops）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|包装迭代器|`tqdm(iterable, total=None, desc=None)`|返回迭代器并向终端写进度|
|手动更新|`bar.update(n)`|原地增加完成量|
|更新描述|`bar.set_postfix(loss=value)`|原地修改显示字段|
|关闭|`bar.close()`|完成并释放显示资源|

```python
from tqdm import tqdm

values = [value * 2 for value in tqdm(range(3), disable=True)]
print(values)  # 输出: [0, 2, 4]
```
### 2.4 wheel 构建格式（Python Wheel Format）
- **安装包（Distribution）**：`wheel`。
- **导入模块（Import Module）**：`wheel`；通常由构建前端间接调用。
- **安装命令（Installation）**：`python -m pip install -U wheel`。
- **用途（Purpose）**：支持构建和安装 `.whl` 二进制分发格式；不能把其他平台或 Python ABI 的 wheel 强行装入当前环境。
- **正式笔记（Detailed Note）**：[[01-Python 环境配置（Environment Setup）]]。

```python
import wheel

print(isinstance(wheel.__version__, str))  # 输出: True
```
## 3. 标准库与本地模块边界（Standard-library and Local-module Boundary）
- `os`、`sys`、`pathlib`、`logging`、`json`、`dataclasses`、`typing`、`concurrent.futures`、`asyncio` 等属于 Python 标准库（Standard Library），随 Python 提供，无需执行 `pip install`。
- `config.py`、`dataset.py`、`model.py`、`tokenizer.py`、`train.py`、`predict.py` 等是项目本地模块（Local Module）；它们应通过项目包结构导入，不存在通用的同名安装命令。
## 项目、依赖与配置（Project and Configuration）
业务代码、配置、数据、测试和入口职责分离。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建虚拟环境|`python -m venv .venv`|创建本地环境目录|
|安装项目|`python -m pip install -e '.[dev]'`|以可编辑模式安装|
|模块入口|`python -m package.cli`|按包语义运行模块|
|项目配置|`pyproject.toml`|声明构建、依赖和工具设置|
|环境变量|`os.environ['API_KEY']`|返回变量；缺失抛 KeyError|
|宽容读取|`os.getenv('LOG_LEVEL','INFO')`|返回字符串或默认值|
|数据类配置|`@dataclass(frozen=True)`|返回不可变配置对象|
|Pydantic Settings|`BaseSettings`|验证并返回类型化配置|
|资源文件|`importlib.resources.files(package)`|返回包资源 Traversable|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
from dataclasses import dataclass
@dataclass(frozen=True)
class Config:
    batch_size:int=32
    device:str="cpu"
print(Config())
# 期望输出:
# Config(batch_size=32, device='cpu')
```
## 日志与错误边界（Logging and Errors）
日志回答何时、何处、什么输入规模和什么错误；不记录秘密和大块原始数据。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|记录器|`logging.getLogger(__name__)`|返回 Logger|
|配置|`logging.config.dictConfig(config)`|原地设置日志系统|
|参数日志|`logger.info('rows=%d',n)`|延迟格式化并输出|
|异常堆栈|`logger.exception('failed')`|在异常处理器内记录堆栈|
|结构化字段|`LoggerAdapter(logger,extra)`|返回携带上下文的记录器|
|轮转文件|`RotatingFileHandler(path,maxBytes,backupCount)`|返回轮转处理器|
|自定义异常|`class DataError(Exception): ...`|创建领域异常类型|
|异常链|`raise DataError(msg) from exc`|保留根因|
|入口退出码|`raise SystemExit(code)`|终止进程并返回状态码|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import logging
logging.basicConfig(level=logging.INFO,format="%(levelname)s:%(message)s")
logger=logging.getLogger("demo")
logger.info("rows=%d",3)
print(logger.name)
# 期望输出:
# demo
```
## pytest、Mock 与覆盖率（Testing and Coverage）
测试行为和契约，不绑定不必要实现细节。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|运行|`python -m pytest -q`|收集并运行测试|
|单测试|`pytest path/test_file.py`|test_name::运行指定节点|
|断言|`assert actual == expected`|失败显示表达式差异|
|异常断言|`with pytest.raises(ValueError,match='...')`|验证异常类型和消息|
|参数化|`@pytest.mark.parametrize('x,expected',cases)`|为每组参数生成测试|
|fixture|`@pytest.fixture`|声明可注入测试资源|
|临时路径|`tmp_path`|返回每测试独立 Path|
|环境修改|`monkeypatch.setenv(name,value)`|测试后自动恢复|
|替换属性|`monkeypatch.setattr(obj,name,value)`|测试后恢复|
|Mock|`unittest.mock.patch(target)`|临时替换依赖|
|覆盖率|`python -m pytest --cov=package --cov-report=term-missing`|输出缺失覆盖行|

### 参数与边界（Parameters and Boundaries）
- **形状与类型（Shape and Type）**：在模块边界写明批次轴、特征轴、数据类型和返回结构。
- **训练与推理（Train and Inference）**：区分训练态、评估态、梯度记录和随机层行为。
- **资源与副作用（Resources and Side Effects）**：显式管理设备、显存、文件、网络和外部服务。
- **失败边界（Failure Boundary）**：对空输入、长度不齐、越界标签、数值溢出和版本差异给出检查。

### 组合示例（Combined Example）
```python
import pytest
def reciprocal(x):
    if x==0: raise ValueError("zero")
    return 1/x
assert reciprocal(2)==.5
try: reciprocal(0)
except ValueError as exc: print(str(exc))
# 期望输出:
# zero
```
## 高频工作模式（Common Workflows）
- **基线（Baseline）**：先用最小可解释模型和极小数据过拟合测试，确认数据、损失和指标链路正确。
- **训练（Training）**：固定随机种子，记录数据版本、超参数、权重、指标与环境。
- **验证（Validation）**：验证集只用于选型与调参，最终测试集只评估一次。
- **推理（Inference）**：冻结随机行为、关闭梯度、统一预处理并验证输出 schema。
- **性能（Performance）**：先测量数据加载、计算、通信与后处理，再针对瓶颈优化。
- **上线（Production）**：增加输入校验、超时、批处理、监控、回滚和隐私保护。
## 常见错误与排查（Common Errors and Troubleshooting）
- **维度错误**：记录每个关键张量的 `shape/dtype/device`，按模块契约逐层核对。
- **训练不稳定**：检查输入归一化、标签范围、损失配对、学习率、梯度范数和 NaN/Inf。
- **指标虚高**：排查数据泄漏、重复样本、错误划分、阈值选择和只看单一平均指标。
- **推理漂移**：确保训练与服务使用同一 tokenizer、类别表、归一化统计和模型版本。
- **资源泄漏**：及时关闭文件、图像、客户端与进程；长任务持续观察 CPU/GPU/内存。
- **版本漂移**：固定主要依赖并以官方迁移说明处理弃用，不静默忽略警告。
## 相关详细笔记（Detailed Notes）
## 官方参考（Official References）
- [pytest 使用指南](https://docs.pytest.org/en/stable/how-to/usage.html)
