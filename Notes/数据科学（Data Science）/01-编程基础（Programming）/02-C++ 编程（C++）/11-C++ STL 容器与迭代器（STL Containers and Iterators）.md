---
title: C++ STL 容器与迭代器（STL Containers and Iterators）
status: published
detail_level: comprehensive
published_at: 2026-08-17
updated_at: 2026-08-17
---
# C++ STL 容器与迭代器（STL Containers and Iterators）
## 1. STL 组件（Standard Template Library Components）
标准模板库（Standard Template Library, STL）的核心包括容器、算法、迭代器、函数对象、适配器和分配器。
- 容器负责存储。
- 迭代器提供统一遍历接口。
- 算法操作迭代器区间，通常采用半开区间 `[first, last)`。
- 容器适配器通过底层容器提供受限接口，例如 `stack`、`queue`、`priority_queue`。

## 2. 顺序容器（Sequence Containers）
### 2.1 `std::string`
- 管理连续字符序列，支持 `size()`、`append()`、`find()`、`substr()`、`insert()`、`erase()` 和比较。
- `c_str()` 返回以空字符结尾的只读指针；对象修改后旧指针可能失效。
- `operator[]` 不检查边界，`at()` 越界抛出 `std::out_of_range`。
### 2.2 `std::vector`
- 连续存储、随机访问 $O(1)$、尾部追加摊还 $O(1)$，中间插删 $O(n)$。
- `size()` 是元素数，`capacity()` 是无需重新分配可容纳数；`reserve()` 不改变大小，`resize()` 会改变元素数。
- 重新分配使所有指针、引用和迭代器失效；未重新分配的插入也可能使插入点及其后位置失效。
### 2.3 `std::deque`
- 分段连续存储，两端插删 $O(1)$，支持随机访问；中间插删仍为 $O(n)$。
- 不是一个连续数组，不能把全部元素当作单块内存传给 C API。
### 2.4 `std::list`
- 双向链表，已知迭代器位置插删 $O(1)$，不支持随机访问。
- `splice()` 可在链表之间转移节点而不复制元素。
- 缓存局部性和每节点开销通常差于 `vector`；不能仅因“中间插删多”就机械选择。

## 3. 容器适配器（Container Adapters）
- `std::stack`：LIFO，常以 `deque` 为底层。
- `std::queue`：FIFO，常以 `deque` 为底层。
- `std::priority_queue`：默认最大堆；自定义比较器定义“低优先级”关系，方向容易写反。
- 适配器不暴露迭代器，因为它们刻意限制访问模式。

## 4. 有序关联容器（Ordered Associative Containers）
- `set`/`multiset` 保存键；`map`/`multimap` 保存键值对。
- 通常以平衡搜索树实现，查找、插入、删除为 $O(\log n)$。
- `set`、`map` 键唯一；`multi*` 允许重复键。
- 比较器必须满足严格弱序（Strict Weak Ordering）。
- `map::operator[]` 在键不存在时插入默认值；只读查询用 `find()`、`contains()` 或 `at()`。

## 5. 无序关联容器（Unordered Associative Containers）
`unordered_set`、`unordered_map` 基于哈希表，平均 $O(1)$、最坏 $O(n)$。
- 自定义键需提供一致的哈希与相等关系。
- `reserve()`、`rehash()` 和最大负载因子影响桶数量与迭代器失效。
- 迭代顺序不代表插入或排序顺序。

## 6. 迭代器（Iterators）
迭代器类别从弱到强包括输入、输出、前向、双向、随机访问和连续迭代器。
- 不是所有迭代器都支持 `+ n`；通用代码用 `std::advance()`、`std::next()` 和 `std::distance()`。
- 修改容器前必须了解迭代器失效规则。
- 删除循环应使用容器 `erase()` 返回的下一个有效迭代器。
```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> values{1, 2, 3, 4, 5};
    for (auto it = values.begin(); it != values.end();) {
        if (*it % 2 == 0) {
            it = values.erase(it); // erase 后不能继续使用旧 it。
        } else {
            ++it;
        }
    }
    for (int value : values) std::cout << value << ' ';
}
// 期望输出:
// 1 3 5
```

## 7. 容器选择（Choosing a Container）

|需求|优先容器|
|---|---|
|连续内存、随机访问、通用默认|`vector`|
|两端频繁操作|`deque`|
|稳定节点地址、按迭代器拼接|`list`|
|有序唯一键|`set`/`map`|
|平均常数查找、不需要顺序|`unordered_set`/`unordered_map`|
|LIFO/FIFO/最高优先级|相应适配器|

## 8. 常见错误（Common Errors）
- `reserve()` 与 `resize()` 混淆。
- 在 `vector` 扩容后继续使用旧指针或迭代器。
- 用 `map[key]` 做只读查询却意外插入。
- 对 `list` 使用不存在的随机访问或通用 `std::sort`；链表使用成员 `sort()`。
- 自定义比较器不满足严格弱序。
- 把 `deque` 当作连续内存。

## 9. 相关笔记（Related Notes）
- [[10-C++ 模板与泛型编程（Templates and Generic Programming）]]
- [[12-C++ 函数对象与 STL 算法（Function Objects and STL Algorithms）]]
