---
title: C++ 类、对象、继承与多态（Classes, Inheritance, and Polymorphism）
status: published
detail_level: comprehensive
published_at: 2026-08-17
updated_at: 2026-08-17
---
# C++ 类、对象、继承与多态（Classes, Inheritance, and Polymorphism）
## 1. 封装（Encapsulation）
类（Class）把状态和操作绑定为一个类型。访问控制符：
- `public`：类外可访问，构成公开接口。
- `protected`：类自身、友元和派生类可访问。
- `private`：仅类自身和友元可访问。
- `class` 成员默认 `private`，`struct` 默认 `public`；除此之外二者都能有构造、方法、继承和模板。
```cpp
#include <iostream>
#include <stdexcept>

class BankAccount {
public:
    explicit BankAccount(double balance = 0.0) : balance_(balance) {
        if (balance < 0.0) {
            throw std::invalid_argument("balance cannot be negative");
        }
    }

    void deposit(double amount) {
        if (amount <= 0.0) {
            throw std::invalid_argument("amount must be positive");
        }
        balance_ += amount;
    }

    [[nodiscard]] double balance() const noexcept { return balance_; }

private:
    double balance_;
};

int main() {
    BankAccount account(100.0);
    account.deposit(25.0);
    std::cout << account.balance() << '\n';
}
// 期望输出:
// 125
```

## 2. 构造、析构与对象生命周期（Construction, Destruction, and Lifetime）
- 默认构造函数（Default Constructor）无需实参。
- 参数化构造函数建立带初始状态的对象；`explicit` 防止单参数构造产生意外隐式转换。
- 拷贝构造函数从同类型对象创建新对象；移动构造函数转移资源。
- 析构函数在对象生命周期结束时释放所拥有资源，不应抛出异常。
- 成员按**声明顺序**初始化，不按初始化列表书写顺序；基类先于派生类，析构顺序相反。
- `const` 成员和引用成员必须在成员初始化列表中初始化。

### 2.1 规则三、规则五与规则零（Rule of Three, Five, and Zero）
- 手动管理资源并自定义析构、拷贝构造或拷贝赋值之一时，通常要检查三者。
- C++11 加入移动构造和移动赋值，形成规则五。
- 优先让 `std::vector`、`std::string`、`std::unique_ptr` 等 RAII 类型管理资源，使类无需自定义五个特殊成员，即规则零。

> [!tip] 大白话理解（Plain-language Intuition）
> 对象像一份资源合同。构造时签约拿到资源，析构时负责归还；如果直接复印合同却让两份对象都以为自己拥有同一资源，就会重复释放。规则零的做法是把合同交给已经会正确复制或转移的标准库类型。

## 3. `this` 指针与 `const` 成员函数（The `this` Pointer and Const Methods）
- 非静态成员函数隐式接收 `this`，指向当前对象。
- `return *this;` 可返回当前对象引用以支持链式调用。
- `const` 成员函数中的 `this` 指向常量对象，不能修改普通成员；常量对象只能调用 `const` 成员函数。
- 静态成员函数没有 `this`，只能直接访问静态成员。
- 空指针调用成员函数属于未定义行为，即使函数体看似没有访问成员。

## 4. 友元（Friend）
友元函数或友元类可访问目标类的非公开成员。
- 友元不是成员，不受成员访问控制调用方式约束。
- 友元关系不继承、不传递，也不自动对称。
- 常用于对称二元运算符或需要紧密协作的辅助类型；过度使用会削弱封装。

## 5. 运算符重载（Operator Overloading）
- 至少一个操作数必须是用户自定义类型；不能改变优先级、结合性或操作数个数。
- `operator=`, `operator[]`, `operator()`, `operator->` 必须是成员函数。
- `<<` 常写为非成员并声明为友元，以便左操作数是流对象。
- 前置 `++x` 返回更新后的引用；后置 `x++` 用无意义 `int` 参数区分并返回旧值副本。
- `operator=` 要处理自赋值，并维持异常安全；现代资源类优先使用成员类型的默认赋值。

## 6. 继承（Inheritance）
派生类复用和扩展基类接口。公开继承表达“是一个”（is-a）关系；组合（Composition）表达“有一个”（has-a）关系。

|继承方式|基类 `public` 在派生类中|基类 `protected` 在派生类中|
|---|---|---|
|`public`|`public`|`protected`|
|`protected`|`protected`|`protected`|
|`private`|`private`|`private`|

- 基类 `private` 成员仍存在于派生对象中，但派生类不能直接访问。
- 派生构造函数先构造基类，再构造成员，最后执行派生构造函数体。
- 同名派生成员会隐藏基类同名集合；可用 `Base::name` 或 `using Base::name` 引入。
- 多继承可能产生菱形继承的重复基类子对象；虚继承可共享虚基类，但增加复杂度。

## 7. 多态（Polymorphism）
运行时多态需要：基类虚函数、派生类覆盖（Override），以及通过基类指针或引用调用。
```cpp
#include <iostream>
#include <memory>
#include <vector>

class Worker {
public:
    virtual ~Worker() = default; // 通过基类指针删除派生对象必须有虚析构。
    virtual void describe() const = 0;
};

class Engineer final : public Worker {
public:
    void describe() const override { std::cout << "Engineer\n"; }
};

int main() {
    std::vector<std::unique_ptr<Worker>> workers;
    workers.push_back(std::make_unique<Engineer>());
    for (const auto& worker : workers) {
        worker->describe();
    }
}
// 期望输出:
// Engineer
```
- `override` 让编译器检查签名确实覆盖虚函数；`final` 阻止继续覆盖或继承。
- 纯虚函数（Pure Virtual Function）使类成为抽象类，不能直接实例化。
- 对象切片（Object Slicing）发生在把派生对象按值复制为基类对象时，派生部分丢失；多态容器应保存指针或引用包装器。
- 基类若可能被多态删除，析构函数必须是 `virtual` 或受保护且禁止外部删除。

> [!tip] 大白话理解（Plain-language Intuition）
> 多态像统一的“播放”按钮：调用方只知道设备都能播放，实际按下后由具体设备决定如何工作。若把设备按值塞进一个只有“基础外壳”的盒子，专属部分会被切掉，这就是对象切片。

## 8. 对象模型边界（Object-model Boundaries）
- 非静态数据成员通常存入每个对象；静态成员属于类级别存储。
- 含虚函数的对象通常带虚表指针，但具体布局属于实现细节，标准不保证字节结构。
- 空类对象大小至少为 1，以保证不同对象具有不同地址；空基类优化可能消除作为基类时的空间。
- `sizeof` 不包含动态分配资源，只反映对象本体。

## 9. 常见错误（Common Errors）
- 用赋值代替成员初始化，导致成员先默认构造再赋值。
- 基类析构非虚却通过基类指针 `delete` 派生对象。
- 忘记 `override`，因签名差异意外隐藏而非覆盖。
- 返回局部对象引用或指针。
- 手写裸 `new[]`/`delete[]`，拷贝后发生双重释放。
- 用继承表达仅仅“复用代码”，破坏 is-a 语义；此时组合通常更合适。

## 10. 相关笔记（Related Notes）
- [[06-C++ 存储期与内存管理（Storage Duration and Memory Management）]]
- [[10-C++ 模板与泛型编程（Templates and Generic Programming）]]
- [[系统案例（System Examples）/02-职工管理系统（Employee Management System）]]
