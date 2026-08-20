---
title: 递归、栈、队列与双端队列（Recursion, Stacks, Queues, and Deques）
status: published
detail_level: comprehensive
published_at: 2026-08-17
updated_at: 2026-08-17
---
# 递归、栈、队列与双端队列（Recursion, Stacks, Queues, and Deques）
## 1. 递归（Recursion）
递归函数把原问题缩小为结构相同的子问题，直到到达基本情况（Base Case）。每一层调用都保存参数、局部变量和返回位置，形成调用栈（Call Stack）。
- **基本情况**：不再递归，负责终止。
- **递归关系**：说明如何从更小问题得到当前答案。
- **规模收敛**：每次调用必须让问题更接近基本情况。
- **回溯阶段**：子调用返回后，当前层完成剩余计算。

> [!tip] 大白话理解（Plain-language Intuition）
> 递归像把任务交给“处理更小版本的自己”。每个人都要记住交付后的下一步，并且必须有一个人能直接完成任务；否则会无限转交，最终耗尽调用栈。

### 1.1 单路与多路递归（Single and Multiple Recursion）
- 单路递归每层最多调用一次自身，例如阶乘、链表反转和二分查找。
- 多路递归每层调用多次自身，例如朴素斐波那契、汉诺塔和树遍历。
- 多路递归的调用数可能指数增长；应检查子问题是否重复，并考虑记忆化（Memoization）或动态规划（Dynamic Programming）。
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print([fibonacci(i) for i in range(8)])  # [0, 1, 1, 2, 3, 5, 8, 13]
```

### 1.2 递归复杂度与优化（Complexity and Optimization）
- 递推式 $T(n)=T(n-1)+O(1)$ 通常得到 $O(n)$。
- 分治递推式可用主定理（Master Theorem）分析，例如归并排序 $T(n)=2T(n/2)+O(n)=O(n\log n)$。
- 记忆化缓存“参数相同的子问题”，用空间换时间。
- 尾递归（Tail Recursion）把递归调用作为最后一步，但 CPython 不做尾调用消除；深度仍受递归限制。
- 能自然改写为循环且输入可能很深时，Python 应优先迭代，避免 `RecursionError`。

## 2. 栈（Stack）
栈遵循后进先出（Last In, First Out, LIFO）。核心操作为压栈（Push）、弹栈（Pop）和查看栈顶（Peek）。
- Python `list.append()` 与 `list.pop()` 的尾部操作摊还为 $O(1)$，适合实现栈。
- 不要用 `list.pop(0)` 实现栈或队列头删，它需要移动后续元素，为 $O(n)$。
- 空栈弹出应明确抛出异常或返回约定哨兵，接口不能含糊。
```python
class Stack:
    def __init__(self) -> None:
        self._items: list[object] = []

    def push(self, item: object) -> None:
        self._items.append(item)

    def pop(self) -> object:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> object:
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

stack = Stack()
stack.push("A")
stack.push("B")
print(stack.peek(), stack.pop(), stack.pop())  # B B A
```

### 2.1 栈的典型用途（Typical Uses）
- 函数调用与递归。
- 括号匹配、语法分析和撤销操作。
- 深度优先搜索（Depth-first Search, DFS）。
- 中缀表达式转后缀表达式及后缀表达式求值。
```python
def is_valid_brackets(text: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    opened: list[str] = []
    for char in text:
        if char in "([{" :
            opened.append(char)
        elif char in pairs:
            if not opened or opened.pop() != pairs[char]:
                return False
    return not opened

print(is_valid_brackets("{[()]}") , is_valid_brackets("([)]"))  # True False
```

## 3. 队列（Queue）
队列遵循先进先出（First In, First Out, FIFO）。入队（Enqueue）发生在尾部，出队（Dequeue）发生在头部。
- `collections.deque.append()` 与 `popleft()` 两端均为 $O(1)$，是通用队列首选。
- 链表实现需要同时维护头尾引用，才能让入队和出队均为 $O(1)$。
- 环形数组实现用头索引、尾索引和容量复用空间，避免每次出队移动元素。
```python
from collections import deque

tasks: deque[str] = deque()
tasks.append("download")
tasks.append("parse")
print(tasks.popleft(), list(tasks))  # download ['parse']
```

### 3.1 环形队列（Circular Queue）
容量为 $capacity$ 的数组通过模运算回绕：`next_index = (index + 1) % capacity`。
- 若只维护头尾索引，`head == tail` 可能同时表示空和满；可额外维护 `size`、浪费一个槽位，或使用单独状态位。
- 入队前检查满，出队前检查空。
- 扩容时必须按逻辑顺序复制，而不是按物理数组顺序直接复制。

> [!tip] 大白话理解（Plain-language Intuition）
> 环形队列像转盘：前面空出的格子会被后续任务重新使用。索引走到数组末尾后回到 0，因此必须另外记录“现在到底有多少元素”，否则头尾重合时无法区分空转盘和满转盘。

## 4. 双端队列（Double-ended Queue, Deque）
双端队列允许在两端插入和删除，可同时模拟栈与队列。

|操作（Operation）|`collections.deque` 方法|复杂度|
|---|---|---:|
|右端加入|`append()`|$O(1)$|
|左端加入|`appendleft()`|$O(1)$|
|右端删除|`pop()`|$O(1)$|
|左端删除|`popleft()`|$O(1)$|
|两端查看|索引 `0`、`-1`|$O(1)$|
|中间索引|`deque[i]`|最坏 $O(n)$|

- `maxlen` 可创建定长双端队列；满后追加会自动丢弃另一端元素，适合滚动窗口，但可能造成静默数据丢失。
- 广度优先搜索（Breadth-first Search, BFS）使用普通队列；0-1 BFS 根据边权 0 或 1 分别从左端或右端入队。

## 5. 单调栈与单调队列（Monotonic Stack and Queue）
### 5.1 单调队列（Monotonic Queue）
滑动窗口最大值维护一个值或索引递减的双端队列：新元素进入时删除尾部所有不可能再成为最大值的元素，窗口移动时删除过期头索引。
```python
def sliding_window_max(values: list[int], width: int) -> list[int]:
    if width <= 0 or width > len(values):
        raise ValueError("width must be in [1, len(values)]")
    candidates: deque[int] = deque()
    result: list[int] = []
    for index, value in enumerate(values):
        while candidates and candidates[0] <= index - width:
            candidates.popleft()
        while candidates and values[candidates[-1]] <= value:
            candidates.pop()
        candidates.append(index)
        if index >= width - 1:
            result.append(values[candidates[0]])
    return result

print(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))
# 期望输出:
# [3, 3, 5, 5, 6, 7]
```

### 5.2 单调栈（Monotonic Stack）
单调栈保留仍可能影响后续答案的候选索引，常用于下一个更大元素、柱状图最大矩形和接雨水。
- 每个元素最多进栈、出栈一次，总时间通常为 $O(n)$。
- 存索引比只存值更通用，可同时计算距离、宽度和原值。

## 6. 常见错误（Common Errors）
- 递归缺少基本情况或问题规模不收敛。
- 在循环里反复对 `list` 使用 `pop(0)`，导致 $O(n^2)$。
- 环形队列没有区分空和满，或回绕时忘记取模。
- 单调队列只存值却需要判断元素是否过期。
- 把 `deque(maxlen=n)` 的自动丢弃行为当作普通队列使用。
- 依赖线程安全时误以为 `deque` 的所有复合操作都是原子的；生产者—消费者应使用 `queue.Queue`、锁或异步队列。

## 7. 相关笔记（Related Notes）
- [[04-链表结构与实现（Linked-list Structures and Implementations）]]
- [[07-优先队列、堆与并查集（Priority Queues, Heaps, and Disjoint Sets）]]
