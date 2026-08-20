---
title: 链表结构与实现（Linked-list Structures and Implementations）
aliases:
  - Python Linked Lists
  - 单链表、双向链表与循环链表
status: published
detail_level: comprehensive
merge_policy: union-zero-loss
published_at: 2026-08-17
updated_at: 2026-08-17
---
# 链表结构与实现（Linked-list Structures and Implementations）
## 1. 链表的存储模型（Linked-list Storage Model）
链表（Linked List）是一种线性数据结构（Linear Data Structure）。节点（Node）不要求位于连续内存中，逻辑顺序由节点保存的引用（Reference）连接而成。
- 节点的数据域（Data Field）保存元素。
- 链接域（Link Field）保存后继节点、前驱节点或二者的引用。
- 头引用（Head Reference）指出第一个有效节点；尾引用（Tail Reference）可选，用于加速尾部操作。
- 普通链表的边界链接为 `None`；循环链表（Circular Linked List）的尾节点重新指向头节点或哨兵节点。

![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/04-链表结构与实现（Linked-list Structures and Implementations）/04-链表结构与实现（Linked-list Structures and Implementations）-20221110083407176.png]]

> [!tip] 大白话理解（Plain-language Intuition）
> 顺序表像连续编号的座位，按编号能直接定位，但中间插人时要让后面的人挪位；链表像每个人手里记着“下一位是谁”，座位可以分散。已找到连接点时，插入或删除只需改几条引用，但寻找第 $i$ 个节点仍要从头顺着链接走。

### 1.1 链表的主要类型（Main Linked-list Types）
- **单向链表（Singly Linked List）**：每个节点只保存 `next`。
- **双向链表（Doubly Linked List）**：每个节点同时保存 `prev` 与 `next`，可以双向遍历。
- **循环链表（Circular Linked List）**：尾部链接回到头部或哨兵，不存在普通意义上的 `None` 终点。
- **带哨兵链表（Sentinel-based Linked List）**：使用不代表业务元素的哨兵节点（Sentinel Node，也称 Dummy Node）统一空表、头部和尾部边界。

![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/04-链表结构与实现（Linked-list Structures and Implementations）/04-链表结构与实现（Linked-list Structures and Implementations）-20221110083427372.png]]

![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/04-链表结构与实现（Linked-list Structures and Implementations）/04-链表结构与实现（Linked-list Structures and Implementations）-20221110083538273.png]]

### 1.2 哨兵节点（Sentinel Node）
哨兵节点不保存有效业务数据，只承担结构边界职责。例如头哨兵的 `next` 始终代表首个有效节点；空表时它指向 `None` 或另一哨兵。
- 删除首节点时不再需要单独判断“前驱是否存在”。
- 插入空表和非空表可以复用同一套链接逻辑。
- 哨兵值不得参与查询、长度计算或业务输出。
- 哨兵不是 Python 的特殊语法，只是一种降低分支数量的设计技巧。

![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/04-链表结构与实现（Linked-list Structures and Implementations）/04-链表结构与实现（Linked-list Structures and Implementations）-20221110084611550.png]]

> [!tip] 大白话理解（Plain-language Intuition）
> 哨兵像队伍最前面的固定引导牌。即使队伍没人，引导牌也在；增加或删除第一个真人时，程序始终修改“引导牌后面是谁”，不用为队首另写一套代码。

## 2. 复杂度与顺序表对比（Complexity and Sequential-list Comparison）

|操作（Operation）|无尾引用的单链表|有尾引用的链表|动态数组（Dynamic Array）|
|---|---:|---:|---:|
|按索引访问|$O(n)$|$O(n)$|$O(1)$|
|头部插入或删除|$O(1)$|$O(1)$|$O(n)$|
|尾部插入|$O(n)$|$O(1)$|摊还 $O(1)$|
|尾部删除|$O(n)$；单链表仍需找前驱|单链表 $O(n)$，双向链表 $O(1)$|$O(1)$|
|已知前驱后的插入或删除|$O(1)$|$O(1)$|$O(n)$|
|按值查找|$O(n)$|$O(n)$|$O(n)$|

- 链表中间插入的“链接修改”本身是 $O(1)$，但若输入只有索引，先找目标或前驱仍需 $O(n)$。
- 链表每个节点额外保存引用，并且对象通常分散，空间开销和缓存局部性（Cache Locality）通常劣于连续数组。
- 动态数组插入、删除的主要成本是移动后续元素；链表的主要成本通常是寻找节点。
- Python 的对象和引用本身有额外开销，因此教学实现不应被理解为比内置 `list` 更节省内存或更快。

## 3. 单向链表（Singly Linked List）
### 3.1 结构不变量（Structural Invariants）
- `_sentinel.next` 指向首个有效节点；空表时为 `None`。
- `_tail` 指向最后一个有效节点；空表时指回 `_sentinel`。
- `_size` 等于从 `_sentinel.next` 到 `None` 可达的有效节点数。
- 尾节点的 `next` 必须为 `None`，否则遍历可能不终止。

### 3.2 Python 完整实现（Complete Python Implementation）
```python
from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class _SNode(Generic[T]):
    value: T | None = None
    next: _SNode[T] | None = None


class SinglyLinkedList(Generic[T]):
    def __init__(self, values: Iterable[T] = ()) -> None:
        self._sentinel: _SNode[T] = _SNode()
        self._tail: _SNode[T] = self._sentinel
        self._size = 0
        for value in values:
            self.append(value)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        current = self._sentinel.next
        while current is not None:
            # current 是有效节点，所以 value 具有 T 的语义；哨兵不会进入循环。
            yield current.value  # type: ignore[misc]
            current = current.next

    def is_empty(self) -> bool:
        return self._size == 0

    def prepend(self, value: T) -> None:
        node = _SNode(value, self._sentinel.next)
        self._sentinel.next = node
        if self._size == 0:
            # 空表新增的节点既是首节点也是尾节点，必须同步维护 tail。
            self._tail = node
        self._size += 1

    def append(self, value: T) -> None:
        node = _SNode(value)
        self._tail.next = node
        self._tail = node
        self._size += 1

    def _node_before(self, index: int) -> _SNode[T]:
        """返回 index 位置的前驱；允许 index == size，以支持尾部插入。"""
        if index < 0:
            index += self._size
        if not 0 <= index <= self._size:
            raise IndexError("linked-list index out of range")
        previous = self._sentinel
        for _ in range(index):
            # index 已校验，循环期间 previous.next 必然存在。
            previous = previous.next  # type: ignore[assignment]
        return previous

    def insert(self, index: int, value: T) -> None:
        # 与 list.insert() 一致地先换算负索引，再把越界位置夹到首尾。
        if index < 0:
            index = max(0, self._size + index)
        else:
            index = min(index, self._size)
        previous = self._node_before(index)
        node = _SNode(value, previous.next)
        previous.next = node
        if index == self._size:
            self._tail = node
        self._size += 1

    def pop(self, index: int = -1) -> T:
        if self._size == 0:
            raise IndexError("pop from empty linked list")
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("linked-list index out of range")
        previous = self._node_before(index)
        target = previous.next
        assert target is not None
        previous.next = target.next
        self._size -= 1
        if target is self._tail:
            self._tail = previous
        # 断开已移除节点，便于调试时发现错误复用。
        target.next = None
        return target.value  # type: ignore[return-value]

    def remove(self, value: T) -> None:
        """删除第一个等于 value 的节点；不存在时与 list.remove() 一样抛错。"""
        previous = self._sentinel
        while previous.next is not None:
            if previous.next.value == value:
                target = previous.next
                previous.next = target.next
                self._size -= 1
                if target is self._tail:
                    self._tail = previous
                target.next = None
                return
            previous = previous.next
        raise ValueError(f"{value!r} is not in linked list")

    def contains(self, value: object) -> bool:
        return any(item == value for item in self)


numbers = SinglyLinkedList([1, 2, 3])
numbers.prepend(0)
numbers.append(4)
numbers.insert(2, 99)
removed = numbers.pop(2)
numbers.remove(3)
print(list(numbers), removed, len(numbers), numbers.contains(4))
# 期望输出:
# [0, 1, 2, 4] 99 4 True
```

### 3.3 边界条件（Edge Cases）
- 空表 `pop()` 应抛出 `IndexError`，不能静默返回模糊的 `None`，因为 `None` 也可能是合法元素。
- 删除唯一节点后，`_sentinel.next` 为 `None`，`_tail` 必须重新指向哨兵。
- 删除尾节点后必须更新 `_tail`；只修改前驱的 `next` 会留下失效尾引用。
- 插入时必须先让新节点指向原后继，再改前驱链接，否则可能丢失后半段链表。
- 单链表若只有目标节点而没有其前驱，通常不能在 $O(1)$ 内完成普通删除；“已知节点即可删除”的技巧会改写后继节点内容，并且不适用于尾节点。

## 4. 双向链表（Doubly Linked List）
双向节点同时保存前驱 `prev` 与后继 `next`。使用头尾两个哨兵后，空表满足 `head.next is tail` 且 `tail.prev is head`。

### 4.1 链接修改顺序（Link-update Order）
在节点 `left` 与 `right` 之间插入 `node` 时，需要建立四条关系：
```text
left.next = node
node.prev = left
node.next = right
right.prev = node
```
删除 `node` 时令 `node.prev.next = node.next` 且 `node.next.prev = node.prev`，然后断开 `node` 自身的两个链接。

> [!tip] 大白话理解（Plain-language Intuition）
> 双向链表像每个人同时牵着前后两个人。插入新人时，两边的手都要重新牵好；若只改一边，正向看似正常，反向遍历却会回到错误节点。

### 4.2 Python 完整实现（Complete Python Implementation）
```python
@dataclass
class _DNode(Generic[T]):
    value: T | None = None
    prev: _DNode[T] | None = None
    next: _DNode[T] | None = None


class DoublyLinkedList(Generic[T]):
    def __init__(self, values: Iterable[T] = ()) -> None:
        self._head: _DNode[T] = _DNode()
        self._tail: _DNode[T] = _DNode()
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0
        for value in values:
            self.append(value)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        current = self._head.next
        while current is not self._tail:
            assert current is not None
            yield current.value  # type: ignore[misc]
            current = current.next

    @staticmethod
    def _insert_between(value: T, left: _DNode[T], right: _DNode[T]) -> _DNode[T]:
        node = _DNode(value=value, prev=left, next=right)
        left.next = node
        right.prev = node
        return node

    def prepend(self, value: T) -> None:
        first = self._head.next
        assert first is not None
        self._insert_between(value, self._head, first)
        self._size += 1

    def append(self, value: T) -> None:
        last = self._tail.prev
        assert last is not None
        self._insert_between(value, last, self._tail)
        self._size += 1

    def pop(self, index: int = -1) -> T:
        if self._size == 0:
            raise IndexError("pop from empty linked list")
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("linked-list index out of range")
        if index < self._size // 2:
            node = self._head.next
            for _ in range(index):
                node = node.next  # type: ignore[union-attr]
        else:
            node = self._tail.prev
            for _ in range(self._size - 1 - index):
                node = node.prev  # type: ignore[union-attr]
        assert node not in (None, self._head, self._tail)
        left, right = node.prev, node.next
        assert left is not None and right is not None
        left.next = right
        right.prev = left
        node.prev = node.next = None
        self._size -= 1
        return node.value  # type: ignore[return-value]


queue = DoublyLinkedList([2, 3])
queue.prepend(1)
queue.append(4)
print(list(queue), queue.pop(), queue.pop(0), list(queue))
# 期望输出:
# [1, 2, 3, 4] 4 1 [2, 3]
```

## 5. 循环链表（Circular Linked List）
循环单链表的尾节点 `next` 指回头节点；带哨兵的实现也可令尾节点指回哨兵。其典型用途包括轮询调度（Round-robin Scheduling）、循环播放和约瑟夫问题（Josephus Problem）。
- 空表和单节点表必须分别处理：单节点表中该节点的 `next` 指向自身或哨兵。
- 遍历终止条件不能写成 `current is not None`，而应检测是否回到起点或哨兵。
- 修改头节点时必须同步修改尾节点的回环引用。
- 若维护尾引用，头部和尾部插入都可为 $O(1)$；仅维护头引用时，寻找尾节点仍为 $O(n)$。
```python
class CircularLinkedList(Generic[T]):
    def __init__(self) -> None:
        self._tail: _SNode[T] | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def append(self, value: T) -> None:
        node = _SNode(value)
        if self._tail is None:
            node.next = node
            self._tail = node
        else:
            node.next = self._tail.next  # 新尾仍指向原头。
            self._tail.next = node
            self._tail = node
        self._size += 1

    def prepend(self, value: T) -> None:
        self.append(value)
        assert self._tail is not None
        # append 创建的新节点当前是尾；只移动 tail，环中的新节点便成为头。
        self._tail = self._tail.next

    def __iter__(self) -> Iterator[T]:
        if self._tail is None:
            return
        head = self._tail.next
        current = head
        while True:
            assert current is not None
            yield current.value  # type: ignore[misc]
            current = current.next
            if current is head:
                break


ring = CircularLinkedList[int]()
ring.append(2)
ring.prepend(1)
ring.append(3)
print(list(ring), len(ring))  # [1, 2, 3] 3
```

## 6. 选择与排错（Selection and Troubleshooting）
### 6.1 何时选择哪种结构（When to Choose Each Structure）
- 需要高频索引访问、切片或缓存友好遍历：优先 Python `list`。
- 需要频繁操作两端：优先标准库 `collections.deque`，而不是手写链表。
- 需要教学、理解引用重连或实现特定节点算法：使用显式链表。
- 需要从已知节点双向移动或 $O(1)$ 删除：使用双向链表并确保调用方持有有效节点引用。
- 需要循环调度：使用循环链表，但必须设计明确的停止条件。

### 6.2 常见错误（Common Errors）
- **丢链（Lost Chain）**：覆盖 `previous.next` 前没有保存原后继。
- **断链（Broken Back-link）**：双向链表只更新 `next`，忘记更新 `prev`。
- **无限循环（Infinite Loop）**：循环链表仍以 `None` 为结束条件。
- **尾引用悬空（Stale Tail Reference）**：删除末节点或唯一节点后没有更新 `tail`。
- **哨兵泄漏（Sentinel Leakage）**：把哨兵的占位值计入长度、查询结果或输出。
- **重复遍历（Repeated Traversal）**：每次循环都调用 $O(n)$ 的 `length()` 或按索引取节点，导致整体退化为 $O(n^2)$。

## 7. 相关笔记（Related Notes）
- [[03-顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）]]
- [[05-链表典型算法（Classic Linked-list Algorithms）]]
