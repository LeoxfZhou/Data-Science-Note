---
title: 链表典型算法（Classic Linked-list Algorithms）
aliases:
  - Linked-list Algorithms in Python
  - 链表双指针与递归
status: published
detail_level: comprehensive
merge_policy: union-zero-loss
published_at: 2026-08-17
updated_at: 2026-08-17
---
# 链表典型算法（Classic Linked-list Algorithms）
## 1. 公共节点与辅助函数（Shared Node and Helpers）
本篇使用同一个单向节点定义。算法接收或返回首个有效节点，不把容器对象和哨兵暴露为题目接口。
```python
from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count


@dataclass(eq=False)
class ListNode:
    value: int
    next: ListNode | None = None


def from_list(values: list[int]) -> ListNode | None:
    sentinel = ListNode(0)
    tail = sentinel
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return sentinel.next


def to_list(head: ListNode | None, *, limit: int = 100) -> list[int]:
    """limit 防止误把环形链表传入后无限遍历。"""
    result: list[int] = []
    while head is not None and len(result) < limit:
        result.append(head.value)
        head = head.next
    return result
```
- `eq=False` 保留节点按身份（Identity）比较的语义；相交与判环问题必须比较“是否为同一个节点”，不能只比较值。
- `from_list()` 使用哨兵统一空输入和首节点创建。
- `to_list()` 只用于无环结果；对环形结构应使用限定步数或专门的环检测函数。

## 2. 反转单向链表（Reverse a Singly Linked List）
迭代反转维护三个状态：已反转部分的新头 `previous`、当前节点 `current`、尚未处理部分的头 `following`。
1. 先保存 `current.next`，避免改变链接后丢失未处理部分。
2. 让 `current.next` 指向 `previous`。
3. 同时推进 `previous` 与 `current`。
```python
def reverse_list(head: ListNode | None) -> ListNode | None:
    previous = None
    current = head
    while current is not None:
        following = current.next
        current.next = previous
        previous = current
        current = following
    return previous


print(to_list(reverse_list(from_list([1, 2, 3, 4]))))  # [4, 3, 2, 1]
```
- 时间复杂度为 $O(n)$，额外空间为 $O(1)$。
- 递归也可把后继子链反转后令 `head.next.next = head`，但递归深度为 $O(n)$，长链表可能触发 Python 的递归深度限制。

> [!tip] 大白话理解（Plain-language Intuition）
> 像沿着一串单向路标往前走：每到一个路标，先记下原来下一站在哪里，再把箭头改向来路，最后走到刚才记住的下一站。若先改箭头再记下一站，后半条路就找不到了。

## 3. 按值删除全部节点（Remove All Matching Nodes）
哨兵使“删除首节点”和“删除中间节点”共享逻辑。若当前节点应删除，前驱不动；否则前驱前进。
```python
def remove_elements(head: ListNode | None, target: int) -> ListNode | None:
    sentinel = ListNode(0, head)
    previous = sentinel
    while previous.next is not None:
        if previous.next.value == target:
            previous.next = previous.next.next
        else:
            previous = previous.next
    return sentinel.next


print(to_list(remove_elements(from_list([1, 2, 6, 3, 6]), 6)))  # [1, 2, 3]
print(to_list(remove_elements(from_list([7, 7, 7]), 7)))  # []
```
- 时间复杂度为 $O(n)$，额外空间为 $O(1)$。
- 连续命中时不能无条件推进 `previous`，否则会跳过新的 `previous.next`。

## 4. 删除倒数第 n 个节点（Remove the N-th Node from the End）
快慢指针（Fast and Slow Pointers）保持固定间距：`fast` 从哨兵先走 `n + 1` 步，再与 `slow` 同步前进；`fast` 到 `None` 时，`slow` 恰好是待删节点的前驱。
```python
def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    if n <= 0:
        raise ValueError("n must be positive")
    sentinel = ListNode(0, head)
    slow = fast = sentinel
    for _ in range(n + 1):
        if fast is None:
            raise IndexError("n is larger than the linked-list length")
        fast = fast.next
    while fast is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next
    assert slow.next is not None
    slow.next = slow.next.next
    return sentinel.next


print(to_list(remove_nth_from_end(from_list([1, 2, 3, 4, 5]), 2)))  # [1, 2, 3, 5]
print(to_list(remove_nth_from_end(from_list([1]), 1)))  # []
```
- 时间复杂度为 $O(n)$，额外空间为 $O(1)$，只遍历一轮。
- 递归可以在回溯时累计倒数序号，但使用 $O(n)$ 调用栈；快慢指针更适合长链表。
- 若接口保证 `1 <= n <= length`，边界检查理论上不会触发；通用函数仍应拒绝非法输入。

## 5. 有序链表去重（Deduplicate a Sorted Linked List）
### 5.1 重复值保留一个（Keep One Copy）
输入必须按值有序，因此重复值必然相邻。相邻值相等时跳过后继；否则当前指针前进。
```python
def deduplicate_keep_one(head: ListNode | None) -> ListNode | None:
    current = head
    while current is not None and current.next is not None:
        if current.value == current.next.value:
            current.next = current.next.next
        else:
            current = current.next
    return head


print(to_list(deduplicate_keep_one(from_list([1, 1, 2, 3, 3]))))  # [1, 2, 3]
```

### 5.2 出现重复的值全部删除（Remove Every Duplicated Value）
`current` 与后继值相等时，先记住该重复值，再跳过整段；否则把 `previous` 前移。
```python
def deduplicate_remove_all(head: ListNode | None) -> ListNode | None:
    sentinel = ListNode(0, head)
    previous = sentinel
    while previous.next is not None:
        current = previous.next
        if current.next is not None and current.value == current.next.value:
            duplicated_value = current.value
            while previous.next is not None and previous.next.value == duplicated_value:
                previous.next = previous.next.next
        else:
            previous = current
    return sentinel.next


print(to_list(deduplicate_remove_all(from_list([1, 2, 3, 3, 4, 4, 5]))))  # [1, 2, 5]
print(to_list(deduplicate_remove_all(from_list([1, 1, 1, 2, 3]))))  # [2, 3]
```
- 两种算法的时间复杂度均为 $O(n)$，额外空间为 $O(1)$。
- “保留一个”和“全部删除”是不同契约，不能因为函数名都叫去重而混用。
- 未排序链表中的相同值不一定相邻，需要哈希集合或其他策略，不能直接使用以上实现。

## 6. 合并有序链表（Merge Sorted Linked Lists）
### 6.1 合并两个链表（Merge Two Lists）
每次把较小头节点接到结果尾部；一个输入耗尽后，剩余链本身已有序，可整体接入。
```python
def merge_two_sorted(
    first: ListNode | None,
    second: ListNode | None,
) -> ListNode | None:
    sentinel = ListNode(0)
    tail = sentinel
    while first is not None and second is not None:
        if first.value <= second.value:
            tail.next = first
            first = first.next
        else:
            tail.next = second
            second = second.next
        tail = tail.next
    tail.next = first if first is not None else second
    return sentinel.next


a = from_list([1, 2, 4])
b = from_list([1, 3, 4])
print(to_list(merge_two_sorted(a, b)))  # [1, 1, 2, 3, 4, 4]
```
- 时间复杂度为 $O(m+n)$，额外节点空间为 $O(1)$；函数会重用并重新连接输入节点。
- 若调用方还需要保留原链表结构，必须先复制节点，不能把此实现当成纯函数（Pure Function）。

### 6.2 合并 k 个链表（Merge k Lists）
最小堆（Min-heap）始终选出当前最小头节点。计数器用于在值相等时打破平局，避免 Python 尝试比较 `ListNode`。
```python
def merge_k_sorted(lists: list[ListNode | None]) -> ListNode | None:
    heap: list[tuple[int, int, ListNode]] = []
    order = count()
    for node in lists:
        if node is not None:
            heappush(heap, (node.value, next(order), node))
    sentinel = ListNode(0)
    tail = sentinel
    while heap:
        _, _, node = heappop(heap)
        if node.next is not None:
            heappush(heap, (node.next.value, next(order), node.next))
        tail.next = node
        tail = node
    if tail is not sentinel:
        tail.next = None
    return sentinel.next


inputs = [from_list([1, 4, 5]), from_list([1, 3, 4]), from_list([2, 6])]
print(to_list(merge_k_sorted(inputs)))  # [1, 1, 2, 3, 4, 4, 5, 6]
```
- 总节点数为 $N$ 时，时间复杂度为 $O(N\log k)$，堆空间为 $O(k)$。
- 分治法（Divide and Conquer）反复调用两链合并也可达到 $O(N\log k)$；逐个从左到右合并在链表规模接近时可能退化到 $O(Nk)$。

## 7. 中间节点与回文判断（Middle Node and Palindrome Check）
### 7.1 查找中间节点（Find the Middle Node）
慢指针一次走一步，快指针一次走两步；偶数长度时返回两个中点中靠右者。
```python
def middle_node(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
    return slow


middle = middle_node(from_list([1, 2, 3, 4, 5, 6]))
print(to_list(middle))  # [4, 5, 6]
```

### 7.2 判断回文链表（Check Whether a List Is a Palindrome）
先找前半段末尾，再反转后半段并逐项比较。比较结束后恢复后半段，避免查询函数意外改变输入。
```python
def is_palindrome(head: ListNode | None) -> bool:
    if head is None or head.next is None:
        return True
    slow = fast = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
    second_half = reverse_list(slow.next)
    slow.next = second_half
    left, right = head, second_half
    matched = True
    while right is not None:
        if left.value != right.value:
            matched = False
            break
        left = left.next  # type: ignore[assignment]
        right = right.next
    slow.next = reverse_list(second_half)
    return matched


values = from_list([1, 2, 3, 2, 1])
print(is_palindrome(values), to_list(values))  # True [1, 2, 3, 2, 1]
```
- 时间复杂度为 $O(n)$，额外空间为 $O(1)$。
- 若省略恢复步骤，结果仍可判断正确，但输入链表会被截断或重排，这是一项重要副作用（Side Effect）。

## 8. 环检测与环入口（Cycle Detection and Entry）
Floyd 龟兔赛跑算法（Floyd's Tortoise and Hare Algorithm）分两阶段：
1. 慢指针走一步、快指针走两步；若相遇则有环，若快指针到 `None` 则无环。
2. 相遇后把一个指针移回头部，二者都改为每次一步；再次相遇的位置就是环入口。

![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/05-链表典型算法（Classic Linked-list Algorithms）/05-链表典型算法（Classic Linked-list Algorithms）-20221229190646563.png]]

设头到环入口距离为 $a$，环长为 $b$。首次相遇时快指针路程是慢指针两倍，两者路程差必为若干个完整环，即 $nb$。由此可推出从相遇点再走 $a$ 步会到达入口。

> [!tip] 大白话理解（Plain-language Intuition）
> 两个人在环形跑道上一个走得快、一个走得慢，只要跑道确实有环，快的人迟早会从后面追上慢的人。相遇后让一个人回起点，两人同速走，他们下一次碰头的位置恰好是进入环形跑道的入口。

```python
def detect_cycle_entry(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next
        if slow is fast:
            slow = head
            while slow is not fast:
                slow = slow.next  # type: ignore[assignment]
                fast = fast.next  # type: ignore[assignment]
            return slow
    return None


nodes = [ListNode(value) for value in [1, 2, 3, 4, 5]]
for current, following in zip(nodes, nodes[1:]):
    current.next = following
nodes[-1].next = nodes[2]
entry = detect_cycle_entry(nodes[0])
print(entry.value if entry else None)  # 3
print(detect_cycle_entry(from_list([1, 2, 3])))  # None
```
- 判断是否有环只需返回 `detect_cycle_entry(head) is not None`，也可以在第一阶段相遇时直接返回 `True`。
- 时间复杂度为 $O(n)$，额外空间为 $O(1)$；使用集合记录访问过的节点则是 $O(n)$ 额外空间。

## 9. 只给定待删节点（Delete a Node Without the Head）
若题目保证待删节点不是尾节点，可以复制后继值，再跳过后继。它实际删除的是“后继节点对象”，并让当前对象表现得像后继。
```python
def delete_given_node(node: ListNode) -> None:
    if node.next is None:
        raise ValueError("the tail node cannot be deleted without its predecessor")
    node.value = node.next.value
    node.next = node.next.next


head = from_list([4, 5, 1, 9])
assert head is not None and head.next is not None
delete_given_node(head.next)
print(to_list(head))  # [4, 1, 9]
```
- 不能用于尾节点，因为没有后继内容可复制，也无法访问尾节点的前驱。
- 若外部持有后继节点的引用，该技巧会改变对象身份与逻辑元素的对应关系；一般容器 API 不应随意采用。

## 10. 相交链表（Intersection of Two Linked Lists）
相交指两个链表共享同一节点对象及其后缀，不是恰好出现相同值。双指针走完自己的链后改走另一条链，二者最终走过相同总长度；若相交，会在首个共享节点相遇，否则会同时到 `None`。

![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/05-链表典型算法（Classic Linked-list Algorithms）/05-链表典型算法（Classic Linked-list Algorithms）-20221228081715799.png]]

![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/05-链表典型算法（Classic Linked-list Algorithms）/05-链表典型算法（Classic Linked-list Algorithms）-20221228082002730.png]]

```python
def intersection_node(
    first: ListNode | None,
    second: ListNode | None,
) -> ListNode | None:
    left, right = first, second
    while left is not right:
        left = second if left is None else left.next
        right = first if right is None else right.next
    return left


shared = from_list([4, 5])
first = ListNode(1, ListNode(2, shared))
second = ListNode(3, shared)
intersection = intersection_node(first, second)
print(intersection.value if intersection else None)  # 4
print(intersection_node(from_list([1, 2]), from_list([1, 2])))  # None
```
- 时间复杂度为 $O(m+n)$，额外空间为 $O(1)$。
- `left is right` 比较对象身份；用 `left.value == right.value` 会把值相同但互不共享的节点误判为相交。
- 该算法假设两个链表都无环。含环链表需要先分析各自环入口，再分类讨论。

## 11. 模式总结与常见错误（Pattern Summary and Common Errors）

|模式（Pattern）|核心状态|典型用途|
|---|---|---|
|哨兵节点|固定虚拟前驱|删除首节点、合并结果链|
|前驱与当前指针|`previous`、`current`|按值删除、区间重连|
|快慢指针|不同速度或固定间距|中点、倒数节点、判环|
|原地反转|`previous`、`current`、`following`|整链反转、回文判断|
|双链切换|走完 A 后走 B|相交节点|
|最小堆或分治|多个当前最小头|合并 k 个有序链表|

- 改链接前没有保存后继，会丢失未处理链。
- 连续删除时错误推进前驱，会漏删相邻目标。
- 把节点值相等当成节点身份相同，会破坏相交与判环判断。
- 对环形链表调用普通 `to_list()` 或 `while node is not None` 会无限循环。
- 递归实现虽短，但 Python 没有通用尾调用优化（Tail-call Optimization）；长链表应优先迭代。
- 原地算法通常重用节点并改变输入结构，API 文档必须说明副作用；只读查询如回文判断最好在结束前恢复结构。

## 12. 相关笔记（Related Notes）
- [[04-链表结构与实现（Linked-list Structures and Implementations）]]
- [[02-二分查找与边界搜索（Binary Search and Boundary Queries）]]
