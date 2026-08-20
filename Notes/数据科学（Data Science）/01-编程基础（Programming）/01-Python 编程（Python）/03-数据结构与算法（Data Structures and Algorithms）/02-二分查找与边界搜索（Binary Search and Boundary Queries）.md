---
title: Python 二分查找与边界搜索（Python Binary Search and Boundary Queries）
aliases:
  - Python Binary Search
  - Python Boundary Queries
status: published
detail_level: comprehensive
merge_policy: union-zero-loss
published_at: 2026-08-17
updated_at: 2026-08-17
---
# Python 二分查找与边界搜索（Python Binary Search and Boundary Queries）
## 1. 二分查找的前提与核心思想（Prerequisite and Core Idea）
二分查找（Binary Search）也称折半查找，用于在**已按同一规则有序排列**且支持高效随机访问的序列中查找目标。每轮比较中间元素后，可以排除约一半候选区间。
- 升序序列满足 $A_0\le A_1\le\cdots\le A_{n-1}$。
- 若序列未排序，比较中间值不能判断目标在哪一半，二分查找会返回错误结果。
- Python `list` 和 `tuple` 按索引读取为 $O(1)$，适合二分查找；链表按索引读取为 $O(n)$，套用二分流程通常不能得到整体 $O(\log n)$。
- 二分查找不仅能判断元素是否存在，还能求插入点、重复元素边界、排名、前驱和后继。

> [!tip] 大白话理解（Plain-language Intuition）
> 像查字典：先翻到中间，发现目标字母更靠前，就把后半本全部排除。每翻一次，剩余范围约减半，所以即使数据很多，比较次数也增长得很慢。

## 2. 区间不变量（Interval Invariants）
区间不变量（Interval Invariant）是在每轮循环开始和结束时都成立的约束。二分查找最容易出错的地方不是“取中点”，而是混用了不同区间定义。
### 2.1 闭区间 `[left, right]`（Closed Interval）
- 初始值：`left = 0`，`right = len(values) - 1`。
- 区间非空条件：`left <= right`；`left == right` 时仍有一个未检查元素，不能提前终止。
- 若 `values[mid] < target`，中点已经排除，更新 `left = mid + 1`。
- 若 `target < values[mid]`，更新 `right = mid - 1`。
### 2.2 左闭右开区间 `[left, right)`（Half-open Interval）
- 初始值：`left = 0`，`right = len(values)`。
- 区间非空条件：`left < right`；`right` 本身永远不属于候选区间。
- 若向右搜索，更新 `left = mid + 1`；若向左搜索，更新 `right = mid`。
- 若错误地写成 `right = mid - 1`，会漏掉候选；若在闭区间实现中写 `right = mid`，则可能无法缩小区间而死循环。

> [!tip] 大白话理解（Plain-language Intuition）
> 区间写法像约定门票是否包含终点。闭区间两端都“持票入场”，左闭右开区间的右端只是围栏、不算候选。更新边界时必须一直遵守同一份门票规则。

## 3. 查找任意一个匹配位置（Find Any Matching Index）
### 3.1 闭区间实现（Closed-interval Implementation）
```python
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")

def binary_search(values: Sequence[T], target: T) -> int:
    """返回任意一个等于 target 的索引；不存在时返回 -1。"""
    left = 0
    right = len(values) - 1

    while left <= right:
        # Python 整数不会溢出；写成 left + (right-left)//2 也便于迁移到定长整数语言。
        mid = left + (right - left) // 2
        if values[mid] < target:
            left = mid + 1
        elif target < values[mid]:
            right = mid - 1
        else:
            return mid
    return -1

numbers = [-1, 0, 3, 5, 9, 12]
print(binary_search(numbers, 9))  # 输出: 4
print(binary_search(numbers, 2))  # 输出: -1
print(binary_search([], 2))       # 输出: -1
```
- 对含重复值的序列，该函数只保证返回某个匹配索引，不保证最左或最右。
- 循环每轮严格缩小候选区间，因此一定终止。

### 3.2 左闭右开实现（Half-open Implementation）
```python
def binary_search_half_open(values: list[int], target: int) -> int:
    left = 0
    right = len(values)

    while left < right:
        mid = left + (right - left) // 2
        if values[mid] < target:
            left = mid + 1
        elif target < values[mid]:
            right = mid  # right 不属于候选，所以保留为新的排他边界。
        else:
            return mid
    return -1

print(binary_search_half_open([1, 3, 5, 7], 5))  # 输出: 2
print(binary_search_half_open([1, 3, 5, 7], 4))  # 输出: -1
```

### 3.3 单比较平衡版（Single-comparison Balanced Variant）
平衡版在循环内只判断一次 `target < values[mid]`，把相等值暂时保留在左边界候选中，直到候选区间剩一个元素再统一检查。它减少循环内的分支，但可读性与边界处理更复杂。
```python
def binary_search_balanced(values: list[int], target: int) -> int:
    if not values:
        return -1

    left = 0
    right = len(values)  # 候选区间为 [left, right)。
    while right - left > 1:
        mid = left + (right - left) // 2
        if target < values[mid]:
            right = mid
        else:
            # 相等时不能 mid + 1，否则会把可能的答案排除。
            left = mid
    return left if values[left] == target else -1

print(binary_search_balanced([1, 3, 5, 7], 5))  # 输出: 2
print(binary_search_balanced([1, 3, 5, 7], 4))  # 输出: -1
```
- 空序列必须提前返回，否则最后访问 `values[left]` 会触发 `IndexError`。
- 该版本的比较次数更均衡，但 Python 实际性能仍需基准测试，不能只根据源码行数断言更快。

## 4. 左边界、右边界与插入点（Left Boundary, Right Boundary, and Insertion Point）
### 4.1 `lower_bound`：第一个不小于目标的位置（First Position Not Less Than Target）
`lower_bound(values, target)` 返回最小索引 `i`，使 `values[i] >= target`；若所有元素都小于目标，则返回 `len(values)`。返回值也等于序列中严格小于目标的元素个数。
```python
def lower_bound(values: list[int], target: int) -> int:
    left = 0
    right = len(values)
    while left < right:
        mid = left + (right - left) // 2
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left

values = [1, 2, 4, 4, 4, 7]
print(lower_bound(values, 4))  # 输出: 2
print(lower_bound(values, 5))  # 输出: 5
print(lower_bound(values, 0))  # 输出: 0
print(lower_bound(values, 9))  # 输出: 6
```

### 4.2 `upper_bound`：第一个大于目标的位置（First Position Greater Than Target）
`upper_bound(values, target)` 返回最小索引 `i`，使 `values[i] > target`；它也等于小于或等于目标的元素个数。最后一个小于或等于目标的位置是 `upper_bound(...) - 1`。
```python
def upper_bound(values: list[int], target: int) -> int:
    left = 0
    right = len(values)
    while left < right:
        mid = left + (right - left) // 2
        if values[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left

values = [1, 2, 4, 4, 4, 7]
print(upper_bound(values, 4))      # 输出: 5
print(upper_bound(values, 5))      # 输出: 5
print(upper_bound(values, 0) - 1)  # 输出: -1
```

> [!example]- 边界查询名词与区间（Boundary-query Terminology）
> ![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/02-二分查找与边界搜索（Binary Search and Boundary Queries）/02-二分查找与边界搜索（Binary Search and Boundary Queries）-20221125174155058.png]]

### 4.3 Python 标准库 `bisect`（Python Standard Library `bisect`）
`bisect_left(values, target)` 等价于 `lower_bound`，`bisect_right(values, target)` 等价于 `upper_bound`。二者查找插入点为 $O(\log n)$；真正执行 `insort_left()` 或 `list.insert()` 时，移动元素仍需 $O(n)$。
```python
from bisect import bisect_left, bisect_right

values = [1, 2, 4, 4, 4, 7]
print(bisect_left(values, 4))   # 输出: 2
print(bisect_right(values, 4))  # 输出: 5
```

## 5. 范围查询与顺序统计（Range Queries and Order Statistics）
令 `left = lower_bound(values, target)`，`right = upper_bound(values, target)`。

|需求（Query）|Python 半开切片/索引范围|说明|
|---|---|---|
|$x<target$|`values[:left]`|严格小于目标|
|$x\le target$|`values[:right]`|小于或等于目标|
|$target<x$|`values[right:]`|严格大于目标|
|$target\le x$|`values[left:]`|大于或等于目标|
|$low\le x\le high$|`values[lower_bound(low):upper_bound(high)]`|闭区间查询|
|$low<x<high$|`values[upper_bound(low):lower_bound(high)]`|开区间查询|

- **插入位置（Insertion Point）**：`lower_bound(values, target)`；将目标插入这里可保持非递减顺序，并放在已有相等元素之前。
- **零基排名（Zero-based Rank）**：严格小于目标的元素个数是 `lower_bound(...)`；若需要一基排名（One-based Rank），再加 `1`。
- **前驱（Predecessor）**：严格小于目标的最大元素位于 `lower_bound(...) - 1`；索引为 `-1` 表示不存在。
- **后继（Successor）**：严格大于目标的最小元素位于 `upper_bound(...)`；索引等于 `len(values)` 表示不存在。
- **最近邻（Nearest Neighbor）**：比较前驱和后继与目标的距离；距离相同时必须由业务规则决定优先较小值还是较大值。

```python
from typing import Optional

def predecessor_successor(
    values: list[int], target: int
) -> tuple[Optional[int], Optional[int]]:
    predecessor_index = lower_bound(values, target) - 1
    successor_index = upper_bound(values, target)
    predecessor = values[predecessor_index] if predecessor_index >= 0 else None
    successor = values[successor_index] if successor_index < len(values) else None
    return predecessor, successor

print(predecessor_successor([1, 2, 4, 4, 7], 4))  # 输出: (2, 7)
print(predecessor_successor([1, 2, 4], 0))         # 输出: (None, 1)
```

## 6. 典型任务（Typical Tasks）
### 6.1 搜索插入位置（Search Insert Position）
搜索插入位置就是 `lower_bound`。即使目标不存在，也返回能保持有序性的插入索引；该定义自然支持重复元素。
```python
def search_insert(values: list[int], target: int) -> int:
    return lower_bound(values, target)

print(search_insert([1, 3, 5, 6], 5))  # 输出: 2
print(search_insert([1, 3, 5, 6], 2))  # 输出: 1
print(search_insert([1, 3, 5, 6], 7))  # 输出: 4
```

### 6.2 查找重复值的开始与结束位置（Find First and Last Positions）
开始位置是 `lower_bound`，结束位置是 `upper_bound - 1`。若 `lower_bound` 已越界或对应元素不等于目标，则目标不存在。
```python
def search_range(values: list[int], target: int) -> tuple[int, int]:
    start = lower_bound(values, target)
    if start == len(values) or values[start] != target:
        return -1, -1
    return start, upper_bound(values, target) - 1

print(search_range([5, 7, 7, 8, 8, 10], 8))  # 输出: (3, 4)
print(search_range([5, 7, 7, 8, 8, 10], 6))  # 输出: (-1, -1)
print(search_range([], 0))                    # 输出: (-1, -1)
```

## 7. 正确性与复杂度（Correctness and Complexity）
### 7.1 正确性要点（Correctness Essentials）
- **初始化（Initialization）**：初始候选区间包含所有可能答案。
- **保持（Maintenance）**：每次比较后只排除已经证明不可能含答案的一半，区间不变量继续成立。
- **终止（Termination）**：每轮至少让 `left` 增大或 `right` 减小，候选区间严格缩短。
- **后置条件（Postcondition）**：普通查找终止时已找到目标或区间为空；边界查找终止时 `left == right`，该位置满足指定分界性质。

> [!tip] 大白话理解（Plain-language Intuition）
> 写对二分查找的关键不是背代码，而是每次都能回答：“答案现在一定还在哪个区间里？”只要这个承诺从初始化到循环结束都没被破坏，边界更新就不会凭感觉乱写。

### 7.2 复杂度（Complexity）
- 普通二分查找最好情况是 $O(1)$，即第一次中点比较就命中。
- 最坏与平均比较次数为 $O(\log n)$；更严格地说，最坏次数与 $\lfloor\log_2 n\rfloor+1$ 同阶。
- 迭代实现只保存有限个索引，额外空间为 $O(1)$。
- 递归实现的时间仍为 $O(\log n)$，但调用栈额外空间为 $O(\log n)$；Python 中迭代版通常更直接，也没有递归深度问题。
- 线性查找最坏为 $O(n)$，但无需预先排序且可用于只支持顺序访问的容器。

## 8. 常见错误与边界条件（Common Errors and Edge Cases）
- 忘记排序前提，或排序键（Key）与比较目标使用了不同规则。
- 闭区间写 `while left < right`，导致最后一个候选没有比较。
- 左闭右开区间向左缩小时写 `right = mid - 1`，从而漏掉候选。
- 更新成 `left = mid` 或 `right = mid` 却没有证明区间一定缩小，可能在两个元素时死循环。
- 找到相等值就立即返回，却又期待最左或最右位置；边界查询必须继续向相应方向收缩。
- 用 `-1` 同时表示“未找到”和有效的 Python 负索引。函数可以返回 `-1`，但调用者在访问 `values[index]` 前必须先判断。
- 直接套用其他语言的中点溢出技巧。在 Python 中整数不会溢出；`left + (right-left)//2` 主要用于明确区间长度并便于跨语言迁移。
- 在已排序列表中查找插入点是 $O(\log n)$，但插入仍是 $O(n)$；不能把整个插入操作误报为 $O(\log n)$。

## 9. 完成检查（Checklist）
- [ ] 能说明二分查找的排序与随机访问前提。
- [ ] 能分别维护闭区间与左闭右开区间不变量。
- [ ] 能实现任意匹配、`lower_bound`、`upper_bound` 和插入点。
- [ ] 能用边界函数完成范围、排名、前驱、后继和重复值区间查询。
- [ ] 能证明循环严格缩小并解释空序列、重复值和目标越界的行为。
- [ ] 能区分查找的 $O(\log n)$ 与 Python 列表插入的 $O(n)$。
