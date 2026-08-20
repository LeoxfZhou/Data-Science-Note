---
title: C++ 模板与泛型编程（Templates and Generic Programming）
status: published
detail_level: comprehensive
published_at: 2026-08-17
updated_at: 2026-08-17
---
# C++ 模板与泛型编程（Templates and Generic Programming）
## 1. 模板的目标（Purpose of Templates）
模板（Template）让算法和数据结构以类型或编译期值为参数，在实例化（Instantiation）时生成具体代码。
- 函数模板抽象操作。
- 类模板抽象类型结构。
- 非类型模板参数（Non-type Template Parameter）传递编译期常量。
- 模板通常定义在头文件中，因为实例化点必须看见完整定义。

## 2. 函数模板（Function Templates）
```cpp
#include <iostream>
#include <string>
#include <utility>

template <typename T>
void exchange_values(T& first, T& second) {
    T temporary = std::move(first);
    first = std::move(second);
    second = std::move(temporary);
}

int main() {
    std::string left = "A";
    std::string right = "B";
    exchange_values(left, right); // T 从实参推导为 std::string。
    std::cout << left << ' ' << right << '\n';
}
// 期望输出:
// B A
```
- 模板参数推导不进行任意隐式转换；实参类型冲突时可显式指定类型或调整接口。
- 返回类型无法从函数实参推导时需要显式模板参数或使用 `auto`/尾置返回类型。
- 普通非模板函数与模板同时可用时，重载决议通常优先最佳匹配，不应只背“普通函数永远优先”。

## 3. 类模板（Class Templates）
```cpp
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <vector>

template <typename T>
class Stack {
public:
    void push(const T& value) { values_.push_back(value); }

    T pop() {
        if (values_.empty()) {
            throw std::out_of_range("pop from empty stack");
        }
        T value = std::move(values_.back());
        values_.pop_back();
        return value;
    }

    [[nodiscard]] std::size_t size() const noexcept { return values_.size(); }

private:
    std::vector<T> values_;
};

int main() {
    Stack<int> values;
    values.push(10);
    values.push(20);
    std::cout << values.pop() << ' ' << values.size() << '\n';
}
// 期望输出:
// 20 1
```
- 类模板成员只有在被使用或显式实例化时才要求相关操作有效。
- 类模板对象参数推导（Class Template Argument Deduction, CTAD）自 C++17 可根据构造实参推导部分类型，但复杂接口仍建议明确类型。
- 类外定义成员时需同时写模板参数列表和 `Class<T>::member`。

## 4. 特化与约束（Specialization and Constraints）
- 全特化（Full Specialization）为特定模板参数提供完整实现。
- 偏特化（Partial Specialization）只适用于类模板和变量模板，函数模板通常通过重载表达。
- 传统 SFINAE 在替换失败时移除候选；C++20 概念（Concept）与 `requires` 能更清楚地声明约束并改善错误信息。
```cpp
#include <concepts>

template <std::totally_ordered T>
const T& maximum(const T& first, const T& second) {
    return first < second ? second : first;
}
```

> [!tip] 大白话理解（Plain-language Intuition）
> 模板不是“什么类型都能用”，而是“只要类型具备代码需要的能力就能用”。概念把这些能力要求写在接口门口，避免编译器到函数深处才报一大串难读错误。

## 5. 类型参数的传递与所有权（Parameter Passing and Ownership）
- 只读大对象通常使用 `const T&`。
- 需要取得所有权可按值接收再移动，或提供左值/右值重载。
- 转发引用（Forwarding Reference）配合 `std::forward<T>()` 保留值类别，用于通用包装器。
- 不要无条件使用 `std::move` 返回局部变量；它可能阻碍返回值优化（RVO）。

## 6. 模板编译模型（Template Compilation Model）
- 模板在语法分析和实例化阶段可能分两次查找名称，涉及依赖名（Dependent Name）时需要 `typename` 或 `template` 消歧义。
- 每个翻译单元可生成相同实例，链接器按单一定义规则（One Definition Rule, ODR）合并；定义必须一致。
- 显式实例化可控制代码生成位置，但会增加构建设计复杂度。

## 7. 常见错误（Common Errors）
- 只在 `.cpp` 定义通用模板，其他翻译单元实例化时找不到定义。
- 模板参数没有约束，错误信息出现在实现深处。
- 把函数模板偏特化当作合法语法。
- 混淆复制、移动和完美转发。
- 对不同模板实例误以为它们是继承关系，例如 `Container<Derived>` 不是 `Container<Base>` 的子类型。

## 8. 相关笔记（Related Notes）
- [[08-C++ 类、对象、继承与多态（Classes, Inheritance, and Polymorphism）]]
- [[11-C++ STL 容器与迭代器（STL Containers and Iterators）]]
