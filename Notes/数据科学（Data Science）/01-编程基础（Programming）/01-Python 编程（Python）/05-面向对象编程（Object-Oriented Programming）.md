---
title: 面向对象编程（Object-Oriented Programming）
aliases:
  - Python OOP
  - 面向对象编程
status: published
detail_level: comprehensive
merge_policy: union-zero-loss
reviewed_at: 2026-08-11
published_at: 2026-08-11
source:
  - Processing/02-Processed/2026-08-11-Python编程/originals/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/面向对象编程.md
---

# 面向对象编程（Object-Oriented Programming）
## 面向对象编程 (Object-Oriented Programming)
### 结构化补充（Structured Supplement）：什么时候使用类

类适合把**状态**和操作这些状态的**行为**组织在一起。只有几个无状态步骤时，普通函数 (Function)通常更简单。

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

### 结构化补充（Structured Supplement）：常见误区

- 不要在 `__init__` 中调用可能被子类重写、且依赖子类未初始化状态的方法。
- 不要把每段逻辑都包装成类；无状态转换使用函数 (Function)更直接。
- 不要为了“复用几行代码”建立很深的继承 (Inheritance)体系。
- 不要把双下划线当作安全边界。
- 属性已经足够时，不需要机械地编写 Java 风格的 getter/setter。

### 一、 模拟学生和老师的一天

|学生|老师|
|---|---|
|人物出场介绍(姓名、年龄、年级)|人物出场介绍(姓名、年龄、部门)|
|起床(睁开眼睛、起身、穿好衣服)|起床(睁开眼睛、起身、穿好衣服)|
|洗漱(刷牙、洗脸)|洗漱(刷牙、洗脸)|
|吃饭(吃菜、扒饭)|吃饭(吃菜、扒饭)|
|登录账号(输入账号密码、登录成功)|打卡(录入指纹、打卡成功)|
|学习(看视频、查资料、写代码)|工作(授课、答疑、写代码)|
|吃饭(吃菜、扒饭)|吃饭(吃菜、扒饭)|
|学习(看视频、查资料、写代码)|工作(授课、答疑、写代码)|
|吃饭(吃菜、扒饭)|吃饭(吃菜、扒饭)|
|洗漱(刷牙、洗脸)|洗漱(刷牙、洗脸)|
|睡觉(脱掉外套、躺下、闭眼)|睡觉(脱掉外套、躺下、闭眼)|
|人数统计(统计、公布)|人数统计(统计、公布)|

### 二、 面向过程编程 (Procedure-Oriented Programming)
```Python
def get_up(name):
    print(f'{name}睁开眼睛')
    print(f'{name}起身')
    print(f'{name}穿好衣服')
def wash(name):
    print(f'{name}刷牙')
    print(f'{name}洗脸')
def eat(name):
    print(f'{name}吃菜')
    print(f'{name}扒饭')
def login_id(name):
    print(f'{name}输入账号密码')
    print(f'{name}登陆账号成功')
def study(name):
    print(f'{name}看视频')
    print(f'{name}查资料')
    print(f'{name}写代码')
def sleep(name):
    print(f'{name}脫掉外套')
    print(f'{name}躺下')
    print(f'{name}闭上眼睛')
count_s = 0
stu1 = '张三'
age1 = 18
grade1 = '高三'
print(f'大家好!我是{stu1},今年{age1}岁,目前正在读{grade1}!')
count_s += 1
get_up(stu1)
wash(stu1)
eat(stu1)
login_id(stu1)
study(stu1)
eat(stu1)
study(stu1)
eat(stu1)
wash(stu1)
sleep(stu1)
print(f'当前统计的学生人数为:{count_s}')
def clock_in(name):
    print(f'{name}录入指纹')
    print(f'{name}打卡成功')
def work(name):
    print(f'{name}授课')
    print(f'{name}答疑')
    print(f'{name}写代码')
count_t = 0
t1 = '老赵'
age1 = 39
department = '教学部'
print(f'大家好!我是{t1},今年{age1}岁,在{department}任职!')
count_t += 1
get_up(t1)
wash(t1)
eat(t1)
clock_in(t1)
work(t1)
eat(t1)
work(t1)
eat(t1)
wash(t1)
sleep(t1)
print(f'当前统计的老师人数为:{count_t}')

# 期望输出:
# 大家好!我是张三,今年18岁,目前正在读高三!
# 张三睁开眼睛
# 张三起身
# 张三穿好衣服
# 张三刷牙
# 张三洗脸
# 张三吃菜
# 张三扒饭
# 张三输入账号密码
# 张三登陆账号成功
# 张三看视频
# 张三查资料
# 张三写代码
# 张三吃菜
# 张三扒饭
# 张三看视频
# 张三查资料
# 张三写代码
# 张三吃菜
# 张三扒饭
# 张三刷牙
# 张三洗脸
# 张三脫掉外套
# 张三躺下
# 张三闭上眼睛
# 当前统计的学生人数为:1
# 大家好!我是老赵,今年39岁,在教学部任职!
# 老赵睁开眼睛
# 老赵起身
# 老赵穿好衣服
# 老赵刷牙
# 老赵洗脸
# 老赵吃菜
# 老赵扒饭
# 老赵录入指纹
# 老赵打卡成功
# 老赵授课
# 老赵答疑
# 老赵写代码
# 老赵吃菜
# 老赵扒饭
# 老赵授课
# 老赵答疑
# 老赵写代码
# 老赵吃菜
# 老赵扒饭
# 老赵刷牙
# 老赵洗脸
# 老赵脫掉外套
# 老赵躺下
# 老赵闭上眼睛
# 当前统计的老师人数为:1
```
### 三、 面向对象编程 (Object-Oriented Programming)
```Python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.show_time()
    def get_up(self):
        print(f'{self.name}睁开眼睛')
        print(f'{self.name}起身')
        print(f'{self.name}穿好衣服')
    def wash(self):
        print(f'{self.name}刷牙')
        print(f'{self.name}洗脸')
    def eat(self):
        print(f'{self.name}吃菜')
        print(f'{self.name}扒饭')
    def sleep(self):
        print(f'{self.name}脫掉外套')
        print(f'{self.name}躺下')
        print(f'{self.name}闭上眼睛')
    def show_time(self):
        pass
class Student(Person):
    count_s = 0
    def __init__(self, name, age, grade):
        self.grade = grade
        super(Student, self).__init__(name, age)
        Student.count_s += 1
    def show_time(self):
        print(f'大家好!我是{self.name},今年{self.age}岁,目前正在读{self.grade}!')
    def login_id(self):
        print(f'{self.name}输入账号密码')
        print(f'{self.name}登陆账号成功')
    def study(self):
        print(f'{self.name}看视频')
        print(f'{self.name}查资料')
        print(f'{self.name}写代码')
    @classmethod
    def publish(cls):
        print(f'当前统计的学生人数为:{cls.count_s}')
class Teacher(Person):
    count_t = 0
    def __init__(self, name, age, department):
        self.department = department
        super(Teacher, self).__init__(name, age)
        Teacher.count_t += 1
    def show_time(self):
        print(f'大家好!我是{self.name},今年{self.age}岁,在{self.department}任职!')
    def clock_in(self):
        print(f'{self.name}录入指纹')
        print(f'{self.name}打卡成功')
    def work(self):
        print(f'{self.name}授课')
        print(f'{self.name}答疑')
        print(f'{self.name}写代码')
    @classmethod
    def publish(cls):
        print(f'当前统计的老师人数为:{cls.count_t}')
stu1 = Student('张三', 18, '高三')
stu2 = Student('李四', 16, '高一')
stu3 = Student('王五', 17, '高二')
Student.publish()
t1 = Teacher('老赵', 39, '教学部')
t2 = Teacher('老孙', 45, '后勤部')
Teacher.publish()

# 期望输出:
# 大家好!我是张三,今年18岁,目前正在读高三!
# 大家好!我是李四,今年16岁,目前正在读高一!
# 大家好!我是王五,今年17岁,目前正在读高二!
# 当前统计的学生人数为:3
# 大家好!我是老赵,今年39岁,在教学部任职!
# 大家好!我是老孙,今年45岁,在后勤部任职!
# 当前统计的老师人数为:2
```
### 四、 面向对象基本概念 (Basic Concepts of OOP)
#### 1. 类与对象 (Class and Object)
##### 结构化补充（Structured Supplement）：类对象 (Class Object)与实例对象 (Instance Object)

```python
class Dataset:
    default_split = "train"  # 类属性：所有实例共享默认设置。

    def __init__(self, name: str, split: str | None = None) -> None:
        self.name = name  # 实例属性：每个对象有自己的值。
        self.split = split or self.default_split
```

- `Dataset` 是类对象 (Class Object)。
- `Dataset("cats")` 创建实例对象 (Instance Object)。
- 类属性 (Class Attribute)适合真正共享的常量；不要把可变列表 (List)当作类属性 (Class Attribute)保存每个实例的数据。

错误 (Error)示例：

```python
class BadDataset:
    samples = []  # 所有实例会共享同一个列表，容易产生隐蔽的数据串扰。
```

##### 结构化补充（Structured Supplement）：实例方法 (Instance Method)、类方法 (Class Method)与静态方法 (Static Method)

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

##### 结构化补充（Structured Supplement）：数据类（Dataclass）

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

- **类对象 (Class Object)**、**实例对象 (Instance Object)**、**类属性 (Class Attribute)**、**实例属性 (Instance Attribute)**
- `object` 是所有类的父类 (Superclass)，通常省略不写。
```Python
class Student(object):
    school = '深兰教育' # 类属性(类变量)
    def __init__(self, name, age):
        self.name = name # 实例属性(实例变量)
        self.age = age
```
#### 2. 魔术方法 (Magic Methods)
##### 结构化补充（Structured Supplement）：`__new__`、`__init__` 与常用魔术方法 (Magic Method)

- `__new__` 负责创建并返回实例，很少需要自己重写。
- `__init__` 在实例创建后初始化属性，不应返回值 (Return Value)。
- `__repr__` 提供适合调试的字符串 (String)表示。
- `__len__`、`__iter__`、`__enter__` 等让对象参与 Python 协议 (Protocol)。

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

官方定义好的，以两个下划线开头并且以两个下划线结尾来命名的方法。
- **特点**：一般不需要主动调用，在满足特定条件时，会被自动调用。
- `**__new__**`：称为构造方法 (Constructor)，用来创建实例对象 (Instance Object)，并返回该实例对象 (Instance Object)。
- `**__init__**`：称为初始化方法 (Initializer)，可以对实例对象 (Instance Object)进行属性定制，没有返回值 (Return Value)。
**实例化过程：**
1. 每当实例化时，先自动调用魔术方法 (Magic Method) `__new__(cls, *args, **kwargs)`，把要实例化的类对象 (即：`Student`) 作为实参 (Actual Argument)传递给形参 (Formal Parameter) `cls`，并把实例化时传入的其他实参 (即：`'张三', 28`) 传递给形参 (Formal Parameter) `args`, `*kwargs`，然后 `__new__` 方法根据 `cls` 创建出一个对应的实例对象 (Instance Object)，并返回该实例对象 (Instance Object)。
1. 再自动调用魔术方法 (Magic Method) `__init__(self, name, age)`，把 `__new__` 方法创建的实例对象 (Instance Object)作为实参 (Actual Argument)传递给形参 (Formal Parameter) `self`，实例化时传入的其他实参 (Actual Argument)分别传给形参 (Formal Parameter) `name`, `age`，然后 `__init__` 方法再对 `self` 进行属性定制 (inplace 操作)。
#### 3. 属性调用与操作 (Attribute Operations)
##### 结构化补充（Structured Supplement）：对象属性字典 (Attribute Dictionary) 与 `__slots__`

普通实例通常把属性保存在 `__dict__` 中，因此可以动态增加属性。

```python
class Sample:
    def __init__(self, value: float) -> None:
        self.value = value


sample = Sample(1.0)
print(sample.__dict__)  # 输出: {'value': 1.0}
```

`__slots__` 可以限制预声明属性，并可能降低大量小对象的内存占用：

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
```

`__slots__` 会影响继承 (Inheritance)、弱引用 (Weak Reference)、序列化 (Serialization) 和动态属性 (Dynamic Attribute)，不应在没有性能测量 (Performance Measurement) 时随意使用。

**调用属性：**
- **调用实例属性 (Instance Attribute)**：只能用实例对象 (Instance Object)调用，不能用类对象 (Class Object)调用。
- **调用类属性 (Class Attribute)**：既可以用类对象 (Class Object)调用 (推荐)，也可以用实例对象 (Instance Object)调用。
- **注意**：当实例属性 (Instance Attribute)和类属性 (Class Attribute)同名时，实例对象 (Instance Object)优先调用实例属性 (Instance Attribute)。
```Python
stu1 = Student('张三', 28)
stu2 = Student('李四', age=32)
## 调用实例属性
print(stu1.name)
print(stu2.name)
## 调用类属性
print(Student.school)
print(stu1.school)

# 期望输出:
# 张三
# 李四
# 深兰教育
# 深兰教育
```
**修改、新增与删除属性：**
```Python
""" 修改实例属性: 只能用实例对象修改 """
stu1.age = 29
setattr(stu1, 'age', 27)
""" 修改类属性: 只能用类对象修改 """
Student.school = '深兰大学'
setattr(Student, 'school', '深兰教育')
""" 动态定义实例属性: 当实例对象修改的属性不存在时, 则新增该实例属性 """
stu1.school = 'ShenLanEdu' # 给 stu1 新增一个实例属性, 类属性不变
print(stu1.school)
setattr(stu2, 'adres', '威宁路')
""" 动态定义类属性: 当类对象修改的属性不存在时, 则新增该类属性 """
Student.subject = 'AI'
setattr(Student, 'course', '人工智能')
""" 删除属性: 可以用 del 语句 """
del stu1.age
delattr(stu1, 'name')
del Student.school
delattr(Student, 'subject')

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```
**与属性操作相关的内置函数 (Built-in Functions)：**
- `**getattr(object, name[, default])**`：获取对象的属性值。
- `**setattr(object, name, value)**`：设置对象的属性值。
- `**delattr(object, name)**`：删除对象的属性。
- `**hasattr(object, name)**`：判定对象是否包含对应的属性。
```Python
print(getattr(stu1, 'age'))
print(getattr(stu1, 'adres', '该实例属性不存在'))
print(hasattr(Student, 'school'))
print(hasattr(stu1, 'name'))

# 输出说明: 按 `print()` 的出现顺序输出上方已构造对象的当前值；若输出包含内存地址 (Memory Address)、随机数 (Random Number)、平台路径 (Path)或版本 (Version)信息，具体字符可能随运行环境变化。
```
### 五、 封装 (Encapsulation)
#### 结构化补充（Structured Supplement）：封装 (Encapsulation)与属性

Python 主要依赖约定，不提供严格的私有访问权限：

- `_name` 表示“内部使用”，调用方通常不应直接访问。
- `__name` 会触发名称改写（name mangling），主要用于避免子类意外覆盖，并不是真正安全的私有变量 (Variable)。
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

在属性名或方法名前面加两个下划线开头，声明为**私有属性 (Private Attribute)** 或 **私有方法 (Private Method)**。
私有属性或私有方法只能在该类的内部调用，不能在该类的外部直接调用。
```Python
class Person:
    school = '深兰教育'
    __eat = 'rice' # 私有类属性
    def __init__(self, name, age):
        self.name = name
        self.__age = age # 私有实例属性
    def get_up(self):
        print(f'{self.name}起床了!')
    def __sleep(self): # 私有方法
        print(f'{self.name}睡觉了!')
    @classmethod
    def get_eat(cls):
        return cls.__eat
    def get_age(self):
        return self.__age
    def call_sleep(self):
        self.__sleep()
## print(Person.__eat) # Error，外部不可直接访问
print(Person.get_eat())
p1 = Person('张三', 19)
print(p1.get_age())
p1.call_sleep()

# 期望输出:
# rice
# 19
# 张三睡觉了!
```
### 六、 继承 (Inheritance)
#### 结构化补充（Structured Supplement）：继承 (Inheritance)与组合 (Composition)

继承 (Inheritance)表达“是一个（is-a）”：

```python
class Predictor:
    def predict(self, features):
        raise NotImplementedError


class LinearPredictor(Predictor):
    def predict(self, features):
        return sum(features)
```

组合 (Composition)表达“拥有一个（has-a）”，通常耦合更低：

```python
class PredictionService:
    def __init__(self, predictor: Predictor) -> None:
        # 通过注入依赖，可以在测试中换成假模型，而不必修改服务代码。
        self.predictor = predictor

    def handle(self, features):
        return {"prediction": self.predictor.predict(features)}
```

优先组合 (Composition)的常见原因：

- 可以在运行时替换组件。
- 更容易单元测试。
- 不会形成很深的继承 (Inheritance)层次。

`isinstance(object, Class)` 会考虑继承 (Inheritance)关系；`type(object) is Class` 只匹配精确类型。

#### 结构化补充（Structured Supplement）：抽象基类 (Abstract Base Class, ABC)

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

#### 结构化补充（Structured Supplement）：协议 (Protocol) 与鸭子类型 (Duck Typing)

Python 更常见的是鸭子类型 (Duck Typing)：对象只要提供所需行为即可，不强制继承 (Inheritance)某个父类。

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

#### 结构化补充（Structured Supplement）：多重继承 (Multiple Inheritance) 与方法解析顺序 (Method Resolution Order, MRO)

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

# 期望输出:
# [<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]
# C
```

协作式多重继承 (Cooperative Multiple Inheritance) 中，每层都应使用 `super()`，并保持兼容的方法签名；否则继承 (Inheritance)链可能被中断。

```python
class Named:
    def __init__(self, *, name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
```

业务代码通常优先组合 (Composition)，多重继承 (Multiple Inheritance)更多用于无状态混入类 (Mixin) 等明确模式。

- 所有的类都默认继承 (Inheritance)内置的 `object` 类，通常不用显式的写出来。
- 子类 (Subclass) 继承 (Inheritance)父类 (Superclass) 后，就可以调用父类中的属性和方法。
#### 与继承 (Inheritance)相关的两个内置函数 (Function)
- `**isinstance(object, classinfo)**`

    - `object`：实例对象 (Instance Object)

    - `classinfo`：类对象 (Class Object)或者由多个类对象 (Class Object)构成的元组 (Tuple)

    - 判定 `object` 是否为 `classinfo` 的实例对象 (Instance Object)或者其子类的实例对象 (Instance Object)。

- `**issubclass(class, classinfo)**`

    - `class`：类对象 (Class Object)

    - `classinfo`：类对象 (Class Object)或者由多个类对象 (Class Object)构成的元组 (Tuple)

    - 判定 `class` 是否为 `classinfo` 的子类。该函数 (Function)会把自己视作为自己的子类。

```Python
class A:
    pass
class B(A):
    pass
class C(A):
    pass
a = A()
b = B()
c = C()
## isinstance 判断 (考虑继承)
print(isinstance(a, A)) # True
print(type(a) is A)     # True
print(isinstance(b, A)) # True，考虑继承
print(type(b) is A)     # False，type不考虑继承
print(isinstance(c, (B, A))) # True，c是A子类的实例
## issubclass 判断
print(issubclass(B, A)) # True
print(issubclass(C, A)) # True
print(issubclass(A, A)) # True (把自己视作自己的子类)
```

## 进阶补充与核对（Advanced Supplements and Verification）
### 结构化补充（Structured Supplement）：完成检查

- [ ] 能区分类属性 (Class Attribute)与实例属性 (Instance Attribute)。
- [ ] 能说明实例方法 (Instance Method)、类方法 (Class Method)和静态方法 (Static Method)的适用场景。
- [ ] 能解释单下划线、双下划线和 `property` 的区别。
- [ ] 能根据关系选择继承 (Inheritance)或组合 (Composition)。
- [ ] 知道什么时候使用 `dataclass`，什么时候普通函数 (Function)更合适。

### 结构化补充（Structured Supplement）：参考资料

- [Python 官方教程：Classes](https://docs.python.org/3/tutorial/classes.html)
- [Python 标准库：dataclasses](https://docs.python.org/3/library/dataclasses.html)
