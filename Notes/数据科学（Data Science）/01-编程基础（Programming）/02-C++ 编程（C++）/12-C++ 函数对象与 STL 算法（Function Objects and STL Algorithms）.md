---
title: C++ 函数对象与 STL 算法（Function Objects and STL Algorithms）
status: published
detail_level: comprehensive
published_at: 2026-08-17
updated_at: 2026-08-17
---
# C++ 函数对象与 STL 算法（Function Objects and STL Algorithms）
## 1. 可调用对象（Callable Objects）
可调用对象包括普通函数、函数指针、重载 `operator()` 的函数对象（Function Object/Functor）、Lambda 表达式和 `std::function`。
- 函数对象可保存状态并被内联优化。
- Lambda 默认生成匿名闭包类型；捕获决定外部变量如何进入闭包。
- `std::function<R(Args...)>` 提供类型擦除（Type Erasure），接口统一但可能有间接调用和分配开销。

## 2. 谓词与比较器（Predicates and Comparators）
- 一元谓词接收一个元素并返回可转为 `bool` 的结果。
- 二元谓词接收两个元素，常用于比较或关系判断。
- 排序比较器必须表达严格弱序：`comp(x, x)` 为假，关系具备非对称性和传递性。
```cpp
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Student {
    std::string name;
    int score;
};

int main() {
    std::vector<Student> students{{"Bob", 90}, {"Alice", 90}, {"Carol", 85}};
    std::sort(students.begin(), students.end(), [](const Student& left, const Student& right) {
        if (left.score != right.score) return left.score > right.score;
        return left.name < right.name;
    });
    for (const auto& student : students) std::cout << student.name << ' ';
}
// 期望输出:
// Alice Bob Carol
```

## 3. 常用遍历与变换算法（Traversal and Transformation Algorithms）
- `for_each`：对区间每个元素执行操作。
- `transform`：把输入区间映射到输出区间；输出容器必须已有空间或使用插入迭代器。
- `copy`、`copy_if`：复制全部或满足条件元素。
- `replace`、`replace_if`：原地替换；`replace_copy*` 输出到新范围。
- C++20 范围（Ranges）版本可直接接收范围并组合视图，但必须注意视图的惰性和底层对象生命周期。

## 4. 查找与计数（Search and Counting）
- `find`、`find_if` 返回首个匹配迭代器或 `end()`。
- `count`、`count_if` 返回匹配数量。
- `adjacent_find` 查找相邻重复或满足关系的元素。
- `binary_search` 只返回是否存在；`lower_bound`、`upper_bound` 返回边界位置。
- 二分算法要求范围已经按同一比较规则排序，否则结果未定义或无意义。

## 5. 排序与分区（Sorting and Partitioning）
- `sort`：平均 $O(n\log n)$，不稳定，需要随机访问迭代器。
- `stable_sort`：保持等价元素相对顺序，通常需要额外内存。
- `partial_sort`：只保证前一部分为最小且有序。
- `nth_element`：把第 $n$ 小元素放到正确位置，两侧仅保证分区，平均线性时间。
- `partition`/`stable_partition`：按谓词分成两组。
- `shuffle`：使用用户提供的随机数引擎做均匀洗牌；不要使用已移除的 `random_shuffle`。

## 6. 数值算法（Numeric Algorithms）
头文件 `<numeric>`：
- `accumulate`：左折叠求和或组合。
- `inner_product`：内积或自定义双序列归约。
- `iota`：填充递增序列。
- `partial_sum`、`adjacent_difference`：前缀累计与相邻差。
- 初始值类型决定 `accumulate` 的累加类型；对浮点或大整数不要误传窄类型 `0`。

## 7. 集合算法（Set Algorithms）
`set_union`、`set_intersection`、`set_difference`、`set_symmetric_difference` 操作**已排序区间**并输出到目标迭代器。
- 输入比较规则必须一致。
- 多重元素按出现次数语义处理，并不等同于数学集合自动去重。
- 输出容器需预留空间或使用 `std::back_inserter`。

## 8. 删除—擦除惯用法（Erase–Remove Idiom）
`std::remove` 不改变容器大小，只把保留元素移动到前部并返回新的逻辑结尾；随后调用容器 `erase` 真正删除尾部。
```cpp
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> values{1, 2, 3, 2, 4};
    values.erase(std::remove(values.begin(), values.end(), 2), values.end());
    for (int value : values) std::cout << value << ' ';
}
// 期望输出:
// 1 3 4
```
- C++20 对标准容器可使用 `std::erase`、`std::erase_if`。
- 关联容器键不可被算法随意重排，应使用成员 `erase`。

> [!tip] 大白话理解（Plain-language Intuition）
> `remove` 像把要保留的物品都推到货架前面，然后告诉你“有效区域到这里”。货架长度没有变化；`erase` 才真正拆掉后面的空位。

## 9. 算法与迭代器契约（Algorithm and Iterator Contracts）
- 输出范围必须足够大，或使用 `back_inserter`、`inserter` 等插入迭代器。
- 算法要求的迭代器类别必须满足，例如 `sort` 需要随机访问。
- 同一容器中输入输出区间重叠时，只有 API 明确允许才安全；移动重叠区域使用合适方向的 `copy` 或 `copy_backward`。
- 算法不会自动检查业务前置条件，如已排序、无别名或谓词纯度。

## 10. 常见错误（Common Errors）
- `transform` 输出到空 `vector.begin()`，造成越界写入。
- 对未排序范围使用 `binary_search` 或集合算法。
- 比较器使用 `<=` 而非 `<`，违反严格弱序。
- 认为 `remove` 已改变容器长度。
- Lambda 按引用捕获局部变量后逃逸，形成悬空引用。
- `accumulate` 初始值类型过窄导致截断或溢出。

## 11. 相关笔记（Related Notes）
- [[11-C++ STL 容器与迭代器（STL Containers and Iterators）]]
- [[系统案例（System Examples）/04-演讲比赛流程管理系统（Speech Contest Workflow System）]]
