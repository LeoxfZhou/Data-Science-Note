---
title: 哈希表与排序算法（Hash Tables and Sorting Algorithms）
status: published
detail_level: comprehensive
published_at: 2026-08-17
updated_at: 2026-08-17
---
# 哈希表与排序算法（Hash Tables and Sorting Algorithms）
## 1. 哈希表（Hash Table）
哈希表通过哈希函数（Hash Function）把键映射到槽位。理想情况下查询、插入和删除的平均复杂度为 $O(1)$，最坏可退化为 $O(n)$。
- 哈希值相同或映射到同一槽位称为碰撞（Collision），不能把它误判为键相等。
- 键相等必须蕴含哈希值相等；Python 自定义对象若实现 `__eq__()`，通常也应实现一致的 `__hash__()`。
- 可变对象一般不能作为哈希键，因为插入后哈希值变化会使对象无法从原槽位找到。
- 负载因子（Load Factor）是元素数与槽位数之比；过高时碰撞增多，需要扩容并重新散列。

> [!tip] 大白话理解（Plain-language Intuition）
> 哈希表像按名字算出储物柜号码。不同名字可能算到同一个柜子，所以柜内还要核对真实姓名；柜子太挤时要换更大的柜区并重新分配。

### 1.1 碰撞处理（Collision Resolution）
- **链地址法（Separate Chaining）**：每个槽位保存桶，碰撞键进入同一桶。
- **开放寻址法（Open Addressing）**：发生碰撞后按探测序列寻找空槽，包括线性探测、二次探测和双重哈希。
- 开放寻址删除不能直接改成“从未使用”，否则会截断探测链；需要墓碑标记（Tombstone）或重新整理。
- 扩容必须对所有有效键重新计算槽位，不能只复制数组。

### 1.2 Python `dict` 与 `set`（Python Dictionaries and Sets）
- `dict` 保持插入顺序，但顺序不是按键排序。
- `set` 不承诺业务可依赖的稳定迭代顺序。
- `dict.get(key, default)` 不修改映射；`setdefault()` 可能插入默认值。
- 计数优先使用 `collections.Counter`，分组可用 `defaultdict(list)`。
```python
from collections import Counter, defaultdict

words = ["cat", "dog", "cat", "bird"]
counts = Counter(words)
groups: defaultdict[int, list[str]] = defaultdict(list)
for word in words:
    groups[len(word)].append(word)
print(counts["cat"], dict(groups))
# 期望输出:
# 2 {3: ['cat', 'dog', 'cat'], 4: ['bird']}
```

### 1.3 典型哈希题型（Common Hashing Problems）
- 两数之和：存已见值到索引的映射，查找目标补数。
- 最长无重复子串：滑动窗口记录字符最后位置。
- 字母异位词：排序后的字符串或字符频次元组作为规范键。
- 首个不重复字符：先计数，再按原顺序扫描。
- 前中序重建树：用值到中序索引的映射把重复线性查找降为 $O(1)$；前提是值唯一。

## 2. 排序的评价维度（Sorting Criteria）
- **时间复杂度（Time Complexity）**：最好、平均、最坏情形。
- **空间复杂度（Space Complexity）**：是否原地（In-place）。
- **稳定性（Stability）**：相等键排序后是否保持原相对顺序。
- **适应性（Adaptiveness）**：输入接近有序时能否更快。
- **比较排序下界**：仅通过比较区分顺序的一般排序最坏需要 $\Omega(n\log n)$ 次比较。

|算法（Algorithm）|最好|平均|最坏|额外空间|稳定|
|---|---:|---:|---:|---:|---|
|冒泡排序|$O(n)$|$O(n^2)$|$O(n^2)$|$O(1)$|是|
|选择排序|$O(n^2)$|$O(n^2)$|$O(n^2)$|$O(1)$|通常否|
|插入排序|$O(n)$|$O(n^2)$|$O(n^2)$|$O(1)$|是|
|希尔排序|依间隔序列|依间隔序列|常见上界 $O(n^2)$|$O(1)$|否|
|归并排序|$O(n\log n)$|$O(n\log n)$|$O(n\log n)$|$O(n)$|是|
|快速排序|$O(n\log n)$|$O(n\log n)$|$O(n^2)$|平均 $O(\log n)$ 栈|否|
|堆排序|$O(n\log n)$|$O(n\log n)$|$O(n\log n)$|$O(1)$|否|

## 3. 基础比较排序（Elementary Comparison Sorts）
### 3.1 冒泡排序（Bubble Sort）
相邻逆序元素交换；若一轮没有交换，可提前结束。每轮把一个最大元素“冒”到未排序区末尾。
### 3.2 选择排序（Selection Sort）
每轮寻找未排序区最小元素，与边界元素交换。交换次数少，但比较次数始终为 $\Theta(n^2)$，普通交换会破坏稳定性。
### 3.3 插入排序（Insertion Sort）
把当前元素插入左侧已排序区。接近有序、小数组或作为混合排序的基础算法时表现良好。
```python
def insertion_sort(values: list[int]) -> None:
    for index in range(1, len(values)):
        current = values[index]
        position = index
        while position > 0 and values[position - 1] > current:
            values[position] = values[position - 1]
            position -= 1
        values[position] = current

numbers = [5, 2, 4, 6, 1, 3]
insertion_sort(numbers)
print(numbers)  # [1, 2, 3, 4, 5, 6]
```

## 4. 高效比较排序（Efficient Comparison Sorts）
### 4.1 归并排序（Merge Sort）
递归拆成两半，分别排序，再线性合并。
- 时间始终为 $O(n\log n)$，稳定版本在相等时先取左侧。
- 数组版本需 $O(n)$ 辅助空间；链表可通过改链接合并。
- 外部排序可分块排序后进行多路归并，适合数据大于内存的场景。
```python
def merge_sort(values: list[int]) -> list[int]:
    if len(values) < 2:
        return values.copy()
    middle = len(values) // 2
    left, right = merge_sort(values[:middle]), merge_sort(values[middle:])
    merged: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    return merged + left[i:] + right[j:]

print(merge_sort([5, 1, 4, 2, 8]))  # [1, 2, 4, 5, 8]
```

### 4.2 快速排序（Quick Sort）
选择基准（Pivot），把元素划分到较小、相等、较大区域，再递归处理两侧。
- 随机基准或三数取中降低已排序输入持续产生极端分区的风险。
- 大量重复键时使用三路划分，避免重复值造成递归不平衡。
- 最坏 $O(n^2)$，随机化后期望 $O(n\log n)$。
- 原地快排通常不稳定；递归深度最坏为 $O(n)$。

### 4.3 希尔排序（Shell Sort）
按逐渐缩小的间隔对远距离元素执行插入排序，最后间隔必须为 1。复杂度依赖间隔序列，通常不稳定。

## 5. 非比较排序（Non-comparison Sorts）
### 5.1 计数排序（Counting Sort）
统计每个整数键出现次数，再按键顺序输出。
- 时间 $O(n+k)$，空间 $O(k)$，其中 $k$ 是键范围。
- 键范围远大于元素数时空间浪费严重。
- 使用前缀和并从右向左放置可构造稳定版本。

### 5.2 桶排序（Bucket Sort）
按值域分配到多个桶，桶内排序后连接。性能依赖数据分布和桶设计；分布均匀时接近线性，极端集中时退化。

### 5.3 基数排序（Radix Sort）
按个位、十位等逐位执行稳定排序。最低位优先（LSD）要求每一轮稳定；需额外处理负数、变长字符串和进制选择。

## 6. Python 排序接口（Python Sorting APIs）
- `sorted(iterable, key=None, reverse=False)` 返回新列表。
- `list.sort()` 原地排序并返回 `None`。
- 二者使用稳定的 Timsort，能利用已有有序片段。
- `key` 对每个元素通常只计算一次，优先于自定义二元比较器。
- 多关键字可返回元组；利用稳定性也可从次要键到主要键分多轮排序。
```python
records = [("Alice", 90), ("Bob", 90), ("Carol", 85)]
ordered = sorted(records, key=lambda item: (-item[1], item[0]))
print(ordered)
# 期望输出:
# [('Alice', 90), ('Bob', 90), ('Carol', 85)]
```

## 7. 快速选择与部分排序（Quickselect and Partial Sorting）
快速选择只递归进入包含第 $k$ 个元素的一侧，平均 $O(n)$、最坏 $O(n^2)$；随机基准可改善期望表现。
- 少量 Top-K 可用大小为 $k$ 的堆：$O(n\log k)$。
- 需要完整排序才使用 $O(n\log n)$ 排序。
- Python 可用 `heapq.nsmallest()`、`nlargest()`；性能取决于 $k$ 与 $n$ 比例。

## 8. 常见错误（Common Errors）
- 把哈希碰撞当成键相等，或使用可变键。
- 自定义 `__eq__()` 与 `__hash__()` 契约不一致。
- 排序时比较器不满足传递性，导致结果不确定。
- 快排分区边界不收缩，出现死循环或无限递归。
- 稳定归并在相等时错误地先取右侧。
- 对巨大稀疏值域使用计数排序。
- 误以为 Python `set` 按插入顺序稳定。

## 9. 相关笔记（Related Notes）
- [[07-优先队列、堆与并查集（Priority Queues, Heaps, and Disjoint Sets）]]
- [[11-贪心、动态规划与分治（Greedy, Dynamic Programming, and Divide and Conquer）]]
