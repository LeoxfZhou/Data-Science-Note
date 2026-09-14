---
title: "C++ 与 STL 速查表（C++ and STL Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - cpp/stl
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-07
version_scope: "C++17–C++23；编译器支持情况以 cppreference 与实现文档为准"
---
# C++ 与 STL 速查表（C++ and STL Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
典型编译：`c++ -std=c++20 -Wall -Wextra -Wpedantic main.cpp -o app`。启用调试符号和 Sanitizer 可更早发现未定义行为。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 值、引用、指针与生命周期（Values, References, Pointers, and Lifetime）
C++ 资源安全依赖作用域与 RAII（Resource Acquisition Is Initialization）。

|功能（Operation）|实际写法（C++ Usage）|返回值与状态变化|
|---|---|---|
|常量引用|`const T& ref = value;`|不复制且不可经 ref 修改；被引用对象必须存活|
|移动构造|`T moved = std`|move(value);::把 value 转为右值；源对象仍有效但值未指定|
|独占所有权|`std`|make_unique<T>(args...)::返回 unique_ptr<T>|
|共享所有权|`std`|make_shared<T>(args...)::返回 shared_ptr<T> 并增加引用计数|
|弱引用|`std`|weak_ptr<T>(shared)::不增加强引用计数|
|判空|`ptr == nullptr`|返回 bool|
|安全转换|`dynamic_cast<Derived*>(base)`|成功返回指针，失败返回 nullptr|
|作用域清理|`对象离开作用域`|自动调用析构函数并释放资源|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```cpp
#include <iostream>
#include <memory>
int main() {
  auto p = std::make_unique<int>(7);
  std::cout << *p << "\n";  // 7
}
```
## 顺序容器（Sequence Containers）
根据随机访问、两端操作、迭代器稳定性和内存连续性选择容器。

|功能（Operation）|实际写法（C++ Usage）|返回值与状态变化|
|---|---|---|
|动态数组|`std`|vector<T> v;::创建连续存储容器|
|尾部追加|`v.push_back(value)`|原地追加；扩容可能使迭代器和引用失效|
|原位构造|`v.emplace_back(args...)`|原地构造元素，返回引用（C++17+）|
|边界检查|`v.at(i)`|返回引用；越界抛 std::out_of_range|
|无检查索引|`v[i]`|返回引用；越界为未定义行为|
|预留容量|`v.reserve(n)`|容量至少 n，大小不变|
|双端队列|`std`|deque<T> d;::支持两端常数时间插入删除|
|双向链表|`std`|list<T> l;::节点式存储；不支持随机访问|
|固定数组|`std`|array<T, N> a;::栈语义固定长度容器|
|字符串|`std`|string s;::拥有字符序列，可修改|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```cpp
#include <iostream>
#include <vector>
int main() {
  std::vector<int> v{3, 1};
  v.push_back(2);
  for (int x : v) std::cout << x << " ";  // 3 1 2
}
```
## 关联容器与哈希容器（Associative Containers）
有序容器通常是平衡树；无序容器基于哈希并依赖良好哈希函数。

|功能（Operation）|实际写法（C++ Usage）|返回值与状态变化|
|---|---|---|
|有序映射|`std`|map<K, V> m;::键有序且唯一|
|哈希映射|`std`|unordered_map<K, V> m;::键唯一，平均常数时间查找|
|有序集合|`std`|set<T> s;::值有序且唯一|
|哈希集合|`std`|unordered_set<T> s;::值唯一，无稳定顺序|
|安全查找|`m.find(key)`|返回迭代器；未找到为 m.end()|
|存在判断|`m.contains(key)`|返回 bool（C++20）|
|插入|`m.emplace(key, value)`|返回迭代器与是否插入|
|索引访问|`m[key]`|返回值引用；缺键时插入默认值|
|不插入访问|`m.at(key)`|返回引用；缺键抛 out_of_range|
|删除键|`m.erase(key)`|返回删除数量|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```cpp
#include <iostream>
#include <unordered_map>
int main() {
  std::unordered_map<std::string, int> counts;
  ++counts["a"]; ++counts["a"];
  std::cout << counts.at("a") << "\n";  // 2
}
```
## 算法、迭代器与范围（Algorithms, Iterators, and Ranges）
STL 算法通过迭代器或范围操作容器，注意半开区间 `[first, last)`。

|功能（Operation）|实际写法（C++ Usage）|返回值与状态变化|
|---|---|---|
|排序|`std`|sort(v.begin(), v.end())::原地排序，返回 void|
|稳定排序|`std`|stable_sort(...)::相等键保持原顺序|
|查找|`std`|find(first, last, value)::返回迭代器或 last|
|二分下界|`std::lower_bound(first, last, value)`|返回首个不小于 `value` 的迭代器；输入必须有序|
|计数|`std::count_if(first, last, pred)`|返回满足条件的元素数量|
|转换|`std::transform(first, last, out, fn)`|写入输出范围并返回输出末端迭代器|
|归约|`std::accumulate(first, last, init)`|返回累计值|
|删除惯用法|`v.erase(std::remove(v.begin(), v.end(), value), v.end())`|真正移除并缩短 `vector`|
|范围视图|`v \| std::views::filter(pred)`|返回惰性视图（C++20）|
|最值|`std::minmax_element(first, last)`|返回最小和最大元素迭代器组成的 pair|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```cpp
#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>
int main() {
  std::vector<int> v{3, 1, 2};
  std::sort(v.begin(), v.end());
  std::cout << std::accumulate(v.begin(), v.end(), 0) << "\n";  // 6
}
```
## 泛型、可调用对象与现代语法（Templates and Modern C++）
模板在编译期实例化；Concept 可让约束和错误信息更清晰。

|功能（Operation）|实际写法（C++ Usage）|返回值与状态变化|
|---|---|---|
|函数模板|`template<class T> T max_value(T a, T b)`|为具体类型实例化函数|
|Concept 约束|`template<std`|integral T>::只接受满足概念的类型|
|类型推导|`auto value = expression;`|由初始化表达式推导类型|
|结构化绑定|`auto [key, value] = pair;`|创建元素绑定|
|Lambda|`[capture](auto x) { return x; }`|返回闭包对象|
|可选值|`std`|optional<T>::包含 T 或空状态|
|多类型值|`std`|variant<A, B>::同一时刻保存一种候选类型|
|只读字符串视图|`std`|string_view::非拥有字符视图；底层必须存活|
|编译期常量|`constexpr`|允许在常量表达式上下文求值|
|格式化|`std`|format("{}", value)::返回字符串（C++20，实现支持有差异）|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```cpp
#include <iostream>
#include <optional>
std::optional<int> parse(bool ok) { return ok ? std::optional{3} : std::nullopt; }
int main() {
  std::cout << parse(true).value_or(-1) << " " << parse(false).value_or(-1);  // 3 -1
}
```
## I/O、错误与并发（I/O, Errors, and Concurrency）
区分可恢复错误、程序错误和系统错误；避免裸 `new/delete`。

|功能（Operation）|实际写法（C++ Usage）|返回值与状态变化|
|---|---|---|
|控制台输出|`std`|cout << value::写入标准输出，返回 ostream 引用|
|文件输入|`std`|ifstream in(path)::构造输入流；失败状态可检查|
|整行读取|`std`|getline(in, line)::成功返回流真值，失败置状态|
|抛异常|`throw std`|runtime_error(msg)::栈展开并传播异常|
|捕获异常|`catch (const std`|exception& e)::按引用捕获多态异常|
|错误码|`std`|error_code ec::保存非异常式系统错误|
|创建线程|`std`|jthread worker(fn)::启动线程并在析构时请求停止、连接（C++20）|
|互斥锁|`std`|mutex::保护共享状态|
|作用域加锁|`std`|lock_guard lock(mutex)::构造时锁定，析构时释放|
|异步任务|`std`|async(std::launch::async, fn)::返回 future|
|取得结果|`future.get()`|返回结果或重新抛出任务异常；只能取一次|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```cpp
#include <future>
#include <iostream>
int main() {
  auto f = std::async(std::launch::async, [] { return 6 * 7; });
  std::cout << f.get() << "\n";  // 42
}
```
## 高频工作模式（Common Workflows）
- **最小闭环（Minimum Loop）**：先用最小输入跑通读取、转换、验证与输出，再替换真实数据。
- **组合优先（Composition First）**：把解析、业务逻辑和 I/O 分层，便于单元测试和复用。
- **可观测性（Observability）**：在边界处记录输入规模、关键参数、耗时和异常，不记录凭据。
- **可复现性（Reproducibility）**：固定随机种子、依赖版本和配置，并保存数据与模型版本。
## 常见错误与排查（Common Errors and Troubleshooting）
- **类型或形状不匹配**：先打印 `type`、`dtype`、`shape`，再检查广播、索引和设备。
- **隐式修改**：链式操作前确认是否原地修改；必要时显式复制并写测试。
- **边界遗漏**：至少覆盖空输入、单元素、重复值、极端值和非法参数。
- **版本漂移**：遇到弃用警告时查询当前官方迁移说明，不长期屏蔽警告。
## 相关详细笔记（Detailed Notes）
- [[01-C++ 环境与编译（Environment and Compilation）]]
- [[02-C++ 基础语法、预处理与控制流（Basics Preprocessing and Control Flow）]]
- [[03-C++ 自定义数据类型（Custom Data Types）]]
- [[04-C++ 指针、引用、数组与字符串（Pointers References Arrays and Strings）]]
- [[05-C++ 函数、回调与递归（Functions Callbacks and Recursion）]]
- [[06-C++ 存储期与内存管理（Storage Duration and Memory Management）]]
- [[07-ONNX 环境与模型图检查（Environment and Model Graph Inspection）]]
- [[08-C++ 类、对象、继承与多态（Classes, Inheritance, and Polymorphism）]]
- [[09-C++ 文件流与持久化（File Streams and Persistence）]]
- [[10-C++ 模板与泛型编程（Templates and Generic Programming）]]
- [[11-C++ STL 容器与迭代器（STL Containers and Iterators）]]
- [[12-C++ 函数对象与 STL 算法（Function Objects and STL Algorithms）]]
- [[01-通讯录管理系统（Address Book Management System）]]
- [[02-职工管理系统（Employee Management System）]]
- [[03-机房预约系统（Computer Room Reservation System）]]
- [[04-演讲比赛流程管理系统（Speech Contest Workflow System）]]
## 官方参考（Official References）
- [cppreference](https://en.cppreference.com/w/)
