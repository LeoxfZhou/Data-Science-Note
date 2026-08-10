---
title: 面向对象编程（Object-Oriented Programming）
aliases:
  - Python OOP
  - 面向对象编程
status: review
detail_level: comprehensive
source:
  - Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/面向对象编程.md
suggested_target: Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/05-面向对象编程（Object-Oriented Programming）.md
operation: 新建
merge_target: null
---

# 面向对象编程（Object-Oriented Programming）

## 1. 什么时候使用类

类适合把**状态**和操作这些状态的**行为**组织在一起。只有几个无状态步骤时，普通函数通常更简单。

```python
class TrainingRun:
    """记录一次训练任务的配置和当前状态。"""

    def __init__(self, model_name: str, epochs: int) -> None:
        if epochs <= 0:
            raise ValueError("epochs 必须大于 0")

        self.model_name = model_name
        self.epochs = epochs
        self.current_epoch = 0

    def advance(self) -> None:
        if self.current_epoch >= self.epochs:
            raise RuntimeError("训练已经结束")
        self.current_epoch += 1

    @property
    def progress(self) -> float:
        # 对外暴露计算结果，而不是让调用方重复实现进度逻辑。
        return self.current_epoch / self.epochs
```

```python
run = TrainingRun("resnet18", epochs=10)
run.advance()
print(run.progress)  # 0.1
```

## 2. 类对象与实例对象

```python
class Dataset:
    default_split = "train"  # 类属性：所有实例共享默认设置。

    def __init__(self, name: str, split: str | None = None) -> None:
        self.name = name  # 实例属性：每个对象有自己的值。
        self.split = split or self.default_split
```

- `Dataset` 是类对象。
- `Dataset("cats")` 创建实例对象。
- 类属性适合真正共享的常量；不要把可变列表当作类属性保存每个实例的数据。

错误示例：

```python
class BadDataset:
    samples = []  # 所有实例会共享同一个列表，容易产生隐蔽的数据串扰。
```

## 3. 实例方法、类方法与静态方法

```python
class ModelConfig:
    def __init__(self, name: str, learning_rate: float) -> None:
        self.name = name
        self.learning_rate = learning_rate

    def describe(self) -> str:
        return f"{self.name}: lr={self.learning_rate}"

    @classmethod
    def from_dict(cls, data: dict) -> "ModelConfig":
        # 类方法常用作备用构造器；使用 cls 可以兼容子类。
        return cls(data["name"], float(data["learning_rate"]))

    @staticmethod
    def is_valid_rate(value: float) -> bool:
        # 静态方法不依赖实例或类状态；只是与这个概念密切相关。
        return 0.0 < value < 1.0
```

## 4. `__new__`、`__init__` 与常用魔术方法

- `__new__` 负责创建并返回实例，很少需要自己重写。
- `__init__` 在实例创建后初始化属性，不应返回值。
- `__repr__` 提供适合调试的字符串表示。
- `__len__`、`__iter__`、`__enter__` 等让对象参与 Python 协议。

```python
class Batch:
    def __init__(self, samples: list) -> None:
        self.samples = samples

    def __len__(self) -> int:
        return len(self.samples)

    def __repr__(self) -> str:
        return f"Batch(size={len(self)})"
```

只有在确实需要改变对象创建过程时才重写 `__new__`。

## 5. 封装与属性

Python 主要依赖约定，不提供严格的私有访问权限：

- `_name` 表示“内部使用”，调用方通常不应直接访问。
- `__name` 会触发名称改写（name mangling），主要用于避免子类意外覆盖，并不是真正安全的私有变量。
- `property` 可以在保持属性式访问的同时加入验证逻辑。

```python
class OptimizerConfig:
    def __init__(self, learning_rate: float) -> None:
        self.learning_rate = learning_rate

    @property
    def learning_rate(self) -> float:
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, value: float) -> None:
        if value <= 0:
            raise ValueError("learning_rate 必须大于 0")
        self._learning_rate = float(value)
```

## 6. 继承与组合

继承表达“是一个（is-a）”：

```python
class Predictor:
    def predict(self, features):
        raise NotImplementedError


class LinearPredictor(Predictor):
    def predict(self, features):
        return sum(features)
```

组合表达“拥有一个（has-a）”，通常耦合更低：

```python
class PredictionService:
    def __init__(self, predictor: Predictor) -> None:
        # 通过注入依赖，可以在测试中换成假模型，而不必修改服务代码。
        self.predictor = predictor

    def handle(self, features):
        return {"prediction": self.predictor.predict(features)}
```

优先组合的常见原因：

- 可以在运行时替换组件。
- 更容易单元测试。
- 不会形成很深的继承层次。

`isinstance(object, Class)` 会考虑继承关系；`type(object) is Class` 只匹配精确类型。

## 7. 数据类（Dataclass）

对象主要用于保存数据时，`dataclass` 能减少样板代码：

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class ImageSize:
    width: int
    height: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("图像尺寸必须为正数")
```

`frozen=True` 阻止普通属性重新赋值，适合不应在创建后变化的配置值。

## 8. 抽象基类 (Abstract Base Class, ABC)

抽象基类 (Abstract Base Class, ABC) 可以规定子类必须实现的接口 (Interface)。

```python
from abc import ABC, abstractmethod


class Predictor(ABC):
    @abstractmethod
    def predict(self, features: list[float]) -> float:
        """根据输入特征返回预测结果。"""


class SumPredictor(Predictor):
    def predict(self, features: list[float]) -> float:
        return sum(features)
```

没有实现全部抽象方法 (Abstract Methods) 的子类不能被实例化。这适合框架边界，但小项目不应为了形式而创建大量抽象层。

## 9. 协议 (Protocol) 与鸭子类型 (Duck Typing)

Python 更常见的是鸭子类型 (Duck Typing)：对象只要提供所需行为即可，不强制继承某个父类。

类型检查需要表达这种结构时可以使用协议 (Protocol)：

```python
from typing import Protocol


class SupportsPredict(Protocol):
    def predict(self, features: list[float]) -> float:
        ...


def evaluate(model: SupportsPredict, features: list[float]) -> float:
    return model.predict(features)
```

协议 (Protocol) 主要服务静态类型检查 (Static Type Checking)，运行时不会自动验证每个对象。

## 10. 多重继承 (Multiple Inheritance) 与方法解析顺序 (Method Resolution Order, MRO)

Python 根据方法解析顺序 (Method Resolution Order, MRO) 查找属性和方法：

```python
class A:
    def describe(self) -> str:
        return "A"


class B(A):
    pass


class C(A):
    def describe(self) -> str:
        return "C"


class D(B, C):
    pass


print(D.mro())
print(D().describe())
```

协作式多重继承 (Cooperative Multiple Inheritance) 中，每层都应使用 `super()`，并保持兼容的方法签名；否则继承链可能被中断。

```python
class Named:
    def __init__(self, *, name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
```

业务代码通常优先组合 (Composition)，多重继承更多用于无状态混入类 (Mixin) 等明确模式。

## 11. 对象属性字典 (Attribute Dictionary) 与 `__slots__`

普通实例通常把属性保存在 `__dict__` 中，因此可以动态增加属性。

```python
class Sample:
    def __init__(self, value: float) -> None:
        self.value = value


sample = Sample(1.0)
print(sample.__dict__)
```

`__slots__` 可以限制预声明属性，并可能降低大量小对象的内存占用：

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
```

`__slots__` 会影响继承、弱引用 (Weak Reference)、序列化 (Serialization) 和动态属性，不应在没有性能测量时随意使用。

## 12. 常见误区

- 不要在 `__init__` 中调用可能被子类重写、且依赖子类未初始化状态的方法。
- 不要把每段逻辑都包装成类；无状态转换使用函数更直接。
- 不要为了“复用几行代码”建立很深的继承体系。
- 不要把双下划线当作安全边界。
- 属性已经足够时，不需要机械地编写 Java 风格的 getter/setter。

## 13. 完成检查

- [ ] 能区分类属性与实例属性。
- [ ] 能说明实例方法、类方法和静态方法的适用场景。
- [ ] 能解释单下划线、双下划线和 `property` 的区别。
- [ ] 能根据关系选择继承或组合。
- [ ] 知道什么时候使用 `dataclass`，什么时候普通函数更合适。

## 参考资料

- [Python 官方教程：Classes](https://docs.python.org/3/tutorial/classes.html)
- [Python 标准库：dataclasses](https://docs.python.org/3/library/dataclasses.html)
