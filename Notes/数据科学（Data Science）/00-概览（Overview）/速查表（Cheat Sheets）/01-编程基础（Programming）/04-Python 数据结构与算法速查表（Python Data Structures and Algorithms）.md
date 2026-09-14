---
title: Python 数据结构与算法速查表（Python Data Structures and Algorithms）
aliases:
  - Python Data Structure Cheat Sheet
  - Python 数据结构接口速查
  - 数据结构速查表
tags:
  - python
  - data-structures
  - cheat-sheet
status: published
detail_level: quick-reference
published_at: 2026-09-04
updated_at: 2026-09-07
---
# Python 数据结构与算法速查表（Python Data Structures and Algorithms）
## 1. 使用说明（How to Use This Cheat Sheet）
本笔记用于快速查询数据结构（Data Structure）的常见操作、Python 实际写法、返回值、状态变化与异常边界。原理、复杂度、完整实现和典型算法继续保存在对应专题笔记中。
- **Python 实际写法（Python API）**：可以直接用于 Python 内置容器或标准库对象的表达式，例如用 `list.append()` 完成压栈。
- **自定义接口（Custom Interface）**：Python 标准库没有相应结构时，沿用详细笔记中的教学接口，例如 `DisjointSet.find()`。
- **原地修改（In-place Mutation）**：会改变原对象；如果方法同时返回元素，表格会明确说明。仅查询操作不改变结构。

> [!warning] 实际写法边界（Python Usage Boundary）
> 表中“实际写法”优先列出 Python 内置容器或标准库 API；Python 没有内置实现时，列出对应详细笔记中的教学类接口。复制自定义结构示例前，需要先引入对应类定义。

## 2. 顺序表、动态数组与 Python `list`（Sequential List, Dynamic Array, and Python `list`）
顺序表（Sequential List）按位置保存一组有序元素；Python `list` 是动态数组（Dynamic Array），适合索引访问、尾部追加、切片和遍历。频繁在头部插入或删除时应考虑 `collections.deque`。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|元素数量|`len(values)`|返回 `int`，不修改列表|
|判断为空|`not values`|返回 `bool`，不修改列表|
|当前容量|无公开 `list` API|自定义动态数组可返回已分配槽位数|
|读取元素|`values[index]`|返回元素；越界抛出 `IndexError`|
|修改元素|`values[index] = item`|替换指定位置；越界抛出 `IndexError`|
|尾部追加|`values.append(item)`|原地添加元素，返回 `None`|
|指定位置插入|`values.insert(index, item)`|原地插入并移动后续元素，返回 `None`|
|删除并返回|`values.pop(index)`|默认删除并返回末尾元素；空列表或越界抛出 `IndexError`|
|按值删除|`values.remove(item)`|删除第一个匹配值，返回 `None`；不存在时抛出 `ValueError`|
|成员判断|`item in values`|返回 `bool`，不修改列表|
|查找位置|`values.index(item)`|返回第一个匹配索引；不存在时抛出 `ValueError`|
|统计次数|`values.count(item)`|返回匹配次数|
|清空|`values.clear()`|移除全部元素，返回 `None`|
|遍历|`for item in values`|按索引顺序访问元素|

```python
values = [10, 20]
values.append(30)
values.insert(1, 15)
removed = values.pop()

print(values, removed)  # [10, 15, 20] 30
print(values[1], 20 in values)  # 15 True
```

详细原理与实现：[[03-顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）]]

## 3. 链表（Linked List）
链表（Linked List）通过节点引用维护逻辑顺序，适合在已知节点附近执行插入和删除。按索引定位仍需从头或尾遍历，不能把链接修改的 $O(1)$ 误解为任意位置操作都是 $O(1)$。

### 3.1 公共操作（Common Operations）

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|元素数量|`len(linked)`|返回维护的节点数|
|判断为空|`linked.is_empty()`|返回 `bool`|
|头部插入|`linked.prepend(item)`|建立新头节点，返回 `None`|
|尾部插入|`linked.append(item)`|建立新尾节点；维护尾引用时为常数操作|
|指定位置插入|`linked.insert(index, item)`|定位后插入；越界抛出 `IndexError`|
|删除并返回|`linked.pop(index)`|移除并返回元素；空链表或越界抛出 `IndexError`|
|按值删除|`linked.remove(item)`|删除第一个匹配节点；不存在时抛出 `ValueError`|
|成员判断|`linked.contains(item)`|返回 `bool`|
|遍历|`iter(linked)`|按链接顺序产生元素|

### 3.2 类型差异（Variant Differences）
- **单向链表（Singly Linked List）**：节点保存 `next` 引用，结构简单；已知前驱时可直接修改链接。当前节点不能直接找到前驱，删除尾节点通常需要遍历。
- **双向链表（Doubly Linked List）**：节点同时保存 `prev` 和 `next` 引用；已知节点时可直接修改两侧链接。每个节点需要额外引用，修改时必须同步四周链接。
- **循环链表（Circular Linked List）**：尾节点指回头节点，适合轮询、约瑟夫问题和循环调度。遍历必须设置终止条件，否则可能无限循环。

```python
from dataclasses import dataclass

@dataclass
class Node:
    value: int
    next: "Node | None" = None

head = Node(20)
head = Node(10, head)  # prepend(10)
head.next.next = Node(30)  # append(30)，示例已知尾节点

values: list[int] = []
current = head
while current is not None:
    values.append(current.value)
    current = current.next

print(values)  # [10, 20, 30]
```

详细原理与完整实现：[[04-链表结构与实现（Linked-list Structures and Implementations）]]

## 4. 栈（Stack）
栈（Stack）遵循后进先出（Last In, First Out, LIFO），适合函数调用、括号匹配、撤销操作和深度优先搜索（Depth-first Search, DFS）。Python 通常使用 `list` 的尾部操作实现。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|元素数量|`len(stack)`|返回元素个数|
|判断为空|`not stack`|返回 `bool`|
|压栈|`stack.append(item)`|把元素加入栈顶，返回 `None`|
|弹栈|`stack.pop()`|移除并返回栈顶；空栈抛出 `IndexError`|
|查看栈顶|`stack[-1]`|返回栈顶但不移除；空栈抛出 `IndexError`|
|清空|`stack.clear()`|移除全部元素，返回 `None`|

```python
stack: list[str] = []
stack.append("A")
stack.append("B")

print(len(stack), stack[-1])  # 2 B
print(stack.pop(), stack)  # B ['A']
print(not stack)  # False
```

详细原理与应用：[[06-递归、栈、队列与双端队列（Recursion, Stacks, Queues, and Deques）]]

## 5. 队列、环形队列与双端队列（Queue, Circular Queue, and Deque）
队列（Queue）遵循先进先出（First In, First Out, FIFO）；双端队列（Double-ended Queue, Deque）允许在两端插入和删除。普通 Python 队列优先使用 `collections.deque`，不要用 `list.pop(0)`，因为它需要移动后续元素。

### 5.1 队列操作（Queue Operations）

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|元素数量|`len(queue)`|返回元素个数|
|判断为空|`not queue`|返回 `bool`|
|入队|`queue.append(item)`|从队尾加入元素，返回 `None`|
|出队|`queue.popleft()`|移除并返回队首；空队列抛出 `IndexError`|
|查看队首|`queue[0]`|返回队首但不移除；空队列抛出 `IndexError`|
|查看队尾|`queue[-1]`|返回队尾但不移除；空队列抛出 `IndexError`|
|清空|`queue.clear()`|移除全部元素，返回 `None`|

### 5.2 环形队列操作（Circular-queue Operations）

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|判断为空|`is_empty()`|通常通过维护的 `size == 0` 判断|
|判断已满|`is_full()`|通常判断 `size == capacity`|
|入队|`enqueue(item)`|写入尾索引并通过模运算回绕；已满时应拒绝或扩容|
|出队|`dequeue()`|读取头索引并通过模运算回绕；为空时应抛出异常|
|查看两端|`front()`、`rear()`|读取逻辑队首或队尾，不移除元素|

> [!warning] `deque(maxlen=...)` 不等于拒绝溢出的环形队列
> 定长 `deque` 已满后继续追加会自动丢弃另一端元素。需要“满时拒绝写入”或线程阻塞语义时，应显式检查容量或使用 `queue.Queue(maxsize=...)`。

### 5.3 双端队列操作（Deque Operations）

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|右端加入|`deque.append(item)`|原地加入，返回 `None`|
|左端加入|`deque.appendleft(item)`|原地加入，返回 `None`|
|右端弹出|`deque.pop()`|移除并返回右端元素；为空抛出 `IndexError`|
|左端弹出|`deque.popleft()`|移除并返回左端元素；为空抛出 `IndexError`|
|查看两端|`deque[0]`、`deque[-1]`|读取但不移除；为空抛出 `IndexError`|
|旋转|`deque.rotate(steps)`|正数向右、负数向左原地旋转|
|清空|`deque.clear()`|移除全部元素|

```python
from collections import deque

queue: deque[str] = deque()
queue.append("task-A")
queue.append("task-B")

print(queue[0], queue[-1])  # task-A task-B
print(queue.popleft(), list(queue))  # task-A ['task-B']

queue.appendleft("urgent")
queue.rotate(1)
print(list(queue))  # ['task-B', 'urgent']
```

详细原理与应用：[[06-递归、栈、队列与双端队列（Recursion, Stacks, Queues, and Deques）]]

## 6. 优先队列与堆（Priority Queue and Heap）
优先队列（Priority Queue）按优先级而不是进入顺序取出元素；`heapq` 使用 `list` 表示最小堆（Min-heap），最小元素始终位于 `heap[0]`。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|原地建堆|`heapq.heapify(values)`|把现有列表改为堆，返回 `None`|
|插入元素|`heapq.heappush(heap, item)`|保持堆性质，返回 `None`|
|弹出最小值|`heapq.heappop(heap)`|移除并返回最小元素；空堆抛出 `IndexError`|
|查看最小值|`heap[0]`|返回最小元素但不移除；空堆抛出 `IndexError`|
|先插入再弹出|`heapq.heappushpop(heap, item)`|返回插入前后整体最小的元素；通常比两次调用更高效|
|替换堆顶|`heapq.heapreplace(heap, item)`|先弹出旧堆顶再插入新元素；空堆抛出 `IndexError`|
|取最小的 $k$ 个|`heapq.nsmallest(k, iterable)`|返回升序列表，不要求输入已建堆|
|取最大的 $k$ 个|`heapq.nlargest(k, iterable)`|返回降序列表，不要求输入已建堆|
|线程安全入队|`queue.PriorityQueue.put(item)`|加入带锁优先队列；可能阻塞或抛出 `Full`|
|线程安全出队|`queue.PriorityQueue.get()`|移除并返回最高优先级元素；可能阻塞或抛出 `Empty`|

```python
import heapq

tasks = [(2, "normal"), (0, "critical"), (1, "urgent")]
heapq.heapify(tasks)
heapq.heappush(tasks, (1, "review"))

print(heapq.heappop(tasks))  # (0, 'critical')
print(tasks[0])  # (1, 'review')
```

当优先级相同且任务对象不可比较时，应加入递增序号组成 `(priority, sequence, task)`，避免 Python 继续比较 `task` 并触发 `TypeError`。最大堆（Max-heap）可使用取负优先级的稳定写法，但取出后要恢复符号。

详细原理与应用：[[07-优先队列、堆与并查集（Priority Queues, Heaps, and Disjoint Sets）]]

## 7. 哈希表与集合（Hash Table and Set）
哈希表（Hash Table）通过键的哈希值定位存储位置。Python `dict` 保存键值映射，`set` 保存不重复元素；查找、插入和删除通常为平均 $O(1)$，但碰撞严重时最坏可退化为 $O(n)$。

### 7.1 字典（Dictionary）

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|元素数量|`len(mapping)`|返回键值对数量|
|判断为空|`not mapping`|返回 `bool`|
|成员判断|`key in mapping`|判断键是否存在，不检查值|
|严格读取|`mapping[key]`|返回值；键不存在时抛出 `KeyError`|
|带默认值读取|`mapping.get(key, default)`|不存在时返回 `default`，不插入键|
|插入或更新|`mapping[key] = value`|原地写入；已有键会覆盖旧值|
|缺失时插入|`mapping.setdefault(key, default)`|返回现有值，或插入并返回默认值|
|批量更新|`mapping.update(other)`|原地合并，重复键使用新值|
|删除并返回|`mapping.pop(key[, default])`|移除并返回值；无默认值且键不存在时抛出 `KeyError`|
|删除最后一项|`mapping.popitem()`|按后进先出顺序移除并返回键值对；空字典抛出 `KeyError`|
|查看键、值、条目|`keys()`、`values()`、`items()`|返回随字典变化的动态视图|
|清空|`mapping.clear()`|移除全部键值对|

### 7.2 集合（Set）

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|元素数量|`len(items)`|返回元素数|
|成员判断|`item in items`|返回 `bool`|
|添加元素|`items.add(item)`|原地添加；重复元素不产生新副本|
|安全删除|`items.discard(item)`|元素不存在时不报错|
|严格删除|`items.remove(item)`|元素不存在时抛出 `KeyError`|
|弹出任意元素|`items.pop()`|移除并返回任意元素；空集合抛出 `KeyError`|
|交集|`left & right`|返回两者共有元素的新集合|
|并集|`left \| right`|返回包含两者全部元素的新集合|
|差集|`left - right`|返回只在 `left` 中的元素|
|对称差集|`left ^ right`|返回只存在于其中一个集合的元素|
|子集判断|`left <= right`|判断 `left` 是否为 `right` 的子集|
|原地批量添加|`items.update(other)`|把 `other` 的元素加入原集合|

```python
scores = {"Alice": 90}
scores.setdefault("Bob", 85)
scores["Alice"] = 95

train_ids = {1, 2, 3}
test_ids = {3, 4}

print(scores.get("Alice"), "Bob" in scores)  # 95 True
print(sorted(train_ids & test_ids))  # [3]
print(sorted(train_ids | test_ids))  # [1, 2, 3, 4]
print(sorted(train_ids - test_ids))  # [1, 2]
```

集合是无序结构，不能依赖其直接打印顺序；示例用 `sorted()` 只为获得稳定输出。

详细原理与应用：[[09-哈希表与排序算法（Hash Tables and Sorting Algorithms）]]、[[02-Python 基础语法（Python Basics）]]

## 8. 并查集（Disjoint-set Union, DSU）
并查集（Disjoint-set Union, DSU）维护元素所属的互不相交集合，常用于连通性判断、Kruskal 最小生成树和动态合并。路径压缩（Path Compression）与按规模合并（Union by Size）同时使用时，单次操作的摊还复杂度接近 $O(1)$，严格写作 $O(\alpha(n))$。

> [!tip] 大白话理解（Plain-language Intuition）
> 每个集合像一个社团，`find()` 查询成员最终属于哪个社团，`union()` 合并两个社团。路径压缩会让成员下次直接找到社团负责人，按规模合并会让小社团挂到大社团下面，避免关系链越来越长。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|创建结构|`DisjointSet(size)`|建立 `size` 个独立集合；负数或非法规模应抛出 `ValueError`|
|查找代表元|`find(item)`|返回根代表元并执行路径压缩；索引越界应抛出 `IndexError`|
|合并集合|`union(first, second)`|若成功合并返回 `True`；原本连通时返回 `False`|
|判断连通|`connected(first, second)`|返回两个元素是否属于同一集合|
|集合规模|`component_size(item)`|返回 `item` 所属集合的元素数；常通过根节点的 `size` 维护|

```python
# DisjointSet 的完整类定义见对应详细笔记。
groups = DisjointSet(5)
print(groups.union(0, 1))  # True
print(groups.union(1, 2))  # True
print(groups.connected(0, 2))  # True
print(groups.connected(0, 4))  # False
```

此代码块展示自定义接口的调用方式；运行前需要复制详细笔记中的 `DisjointSet` 类定义。当前详细实现提供 `find()`、`union()` 和 `connected()`；`component_size()` 是常见扩展接口，不应在未实现时直接调用。

详细原理与完整实现：[[07-优先队列、堆与并查集（Priority Queues, Heaps, and Disjoint Sets）]]

## 9. 树与二叉搜索树（Tree and Binary Search Tree）
树（Tree）表达层级关系；二叉搜索树（Binary Search Tree, BST）要求左子树键小于当前节点、右子树键大于当前节点。未平衡 BST 的操作平均为 $O(\log n)$、最坏退化为 $O(n)$；AVL 树或红黑树等平衡搜索树可把查找、插入和删除维持在 $O(\log n)$。

### 9.1 通用树与二叉树操作（General Tree and Binary-tree Operations）

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|判断为空|`root is None`|返回 `bool`|
|读取根节点|`root`|返回根节点引用，不修改树|
|读取子节点|`node.left`、`node.right` 或 `node.children`|返回子节点引用或集合|
|树的大小|`size(root)`|返回节点总数|
|树的高度|`height(root)`|返回最长根到叶路径高度|
|前序遍历|`preorder(root)`|根 → 左 → 右地产生节点|
|中序遍历|`inorder(root)`|左 → 根 → 右地产生节点；BST 中得到有序键|
|后序遍历|`postorder(root)`|左 → 右 → 根地产生节点|
|层序遍历|`level_order(root)`|使用队列逐层产生节点|

### 9.2 二叉搜索树操作（BST Operations）

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|插入|`tree.insert(value)`|插入新键；重复键策略必须预先约定|
|查找|`tree.contains(value)` 或 `search(value)`|返回 `bool` 或节点引用|
|最小值|`minimum()`|沿左引用找到最小键；空树应抛出异常或返回约定哨兵|
|最大值|`maximum()`|沿右引用找到最大键|
|删除|`delete(value)`|删除键并重新连接子树；可能返回是否删除成功|
|有序遍历|`inorder(root)`|返回或产生升序键|

```python
from __future__ import annotations

from dataclasses import dataclass

@dataclass
class TreeNode:
    value: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None

root = TreeNode(8, left=TreeNode(3), right=TreeNode(10))

def contains(root: TreeNode | None, target: int) -> bool:
    current = root
    while current is not None:
        if target == current.value:
            return True
        current = current.left if target < current.value else current.right
    return False

print(contains(root, 10), contains(root, 7))  # True False
```

删除具有两个子节点的节点时，通常用中序后继或中序前驱替换当前键，再删除替代节点；不能只断开当前节点，否则会丢失整棵子树。

详细原理与完整实现：[[08-树、二叉搜索树与平衡树（Trees, Binary Search Trees, and Balanced Trees）]]

## 10. 图（Graph）
图（Graph）由顶点（Vertex）和边（Edge）组成。Python 标准库没有通用图容器；稀疏图通常用“顶点到邻居集合”的字典表示，带权图则把邻居映射为权重。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|顶点数量|`len(graph)`|返回顶点数|
|判断顶点存在|`vertex in graph`|返回 `bool`|
|添加顶点|`graph.setdefault(vertex, set())`|缺失时建立空邻接集合|
|添加有向边|`graph[source].add(target)`|原地加入边；需要先确保两端顶点存在|
|添加无向边|两端邻接集合分别 `add()`|原地加入两条对称邻接记录|
|获取邻居|`graph[vertex]`|返回邻居集合；缺失顶点时抛出 `KeyError`|
|判断边存在|`target in graph[source]`|返回 `bool`|
|计算度数|`len(graph[vertex])`|返回邻居数量；有向图需区分入度和出度|
|删除边|`graph[source].discard(target)`|边不存在时不报错；无向图需同步删除反向记录|
|删除顶点|删除顶点键并清理其他邻接集合|移除顶点及关联边|
|清空|`graph.clear()`|移除全部顶点和边|

```python
Graph = dict[str, set[str]]
graph: Graph = {}

def add_undirected_edge(graph: Graph, left: str, right: str) -> None:
    graph.setdefault(left, set()).add(right)
    graph.setdefault(right, set()).add(left)

add_undirected_edge(graph, "A", "B")
add_undirected_edge(graph, "A", "C")

print(sorted(graph["A"]))  # ['B', 'C']
print("A" in graph["B"], len(graph["A"]))  # True 2
```

遍历、拓扑排序、最短路径和最小生成树属于图算法，不在本速查表重复实现。

详细原理与算法：[[10-图结构、遍历与最短路径（Graphs, Traversal, and Shortest Paths）]]

## 11. 设计型数据结构（Designed Data Structures）
### 11.1 LRU 缓存（Least Recently Used Cache）
LRU 缓存淘汰最长时间未被访问的条目。典型实现用哈希表配合双向链表，或使用 `collections.OrderedDict`，使读取、写入和移动最近使用位置均为平均 $O(1)$。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|读取|`get(key)`|命中时返回值并把条目标记为最近使用；未命中返回约定哨兵|
|写入|`put(key, value)`|插入或更新并标记为最近使用；超容量时淘汰最久未使用项|
|成员判断|`key in cache`|只判断存在性；是否刷新使用顺序必须由接口约定|
|元素数量|`len(cache)`|返回当前条目数|
|清空|`clear()`|移除全部条目|

```python
from collections import OrderedDict

cache: OrderedDict[str, int] = OrderedDict()
capacity = 2

cache["A"] = 1
cache["B"] = 2
cache.move_to_end("A")  # 访问 A，A 变为最近使用
cache["C"] = 3
cache.popitem(last=False)  # 淘汰最久未使用的 B

print(list(cache.items()))  # [('A', 1), ('C', 3)]
```

### 11.2 LFU 缓存（Least Frequently Used Cache）
LFU 缓存优先淘汰访问次数最少的条目；访问次数相同时通常再按 LRU 顺序打破平局。高效实现需要“键到节点”的哈希表和“频率到有序桶”的映射。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|读取|`get(key)`|命中时返回值并把访问频率加一；未命中返回约定哨兵|
|写入|`put(key, value)`|更新或插入；容量满时淘汰最低频率桶中的最旧项|
|当前最小频率|`min_frequency`|记录可被下一次淘汰的频率|
|元素数量|`len(cache)`|返回当前条目数|

```python
# LFUCache 是自定义类型；以下展示约定的调用语义。
cache = LFUCache(capacity=2)
cache.put("A", 1)
cache.put("B", 2)
print(cache.get("A"))  # 1，A 的访问频率增加
cache.put("C", 3)  # B 频率最低，因此被淘汰
print(cache.get("B"), cache.get("C"))  # None 3
```

### 11.3 跳表（Skip List）
跳表（Skip List）在有序链表之上建立多级随机索引。查找、插入和删除的期望复杂度为 $O(\log n)$，最坏为 $O(n)$；Python 标准库没有内置跳表，需要自定义实现或使用第三方有序容器。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|查找|`search(key)`|返回匹配值、节点或 `None`|
|插入|`insert(key, value)`|按随机层级建立索引；重复键策略需预先约定|
|删除|`delete(key)`|删除各层引用；通常返回是否删除成功|
|最小键|`first()`|返回底层链表第一个数据节点|
|有序遍历|`items()`|沿第 0 层按键顺序产生元素|

```python
# SkipList 是自定义类型；以下展示约定的调用语义。
index = SkipList()
index.insert(10, "A")
index.insert(30, "C")
index.insert(20, "B")

print(index.search(20))  # B
print(index.delete(20), index.search(20))  # True None
```

LRU、LFU 与跳表的设计原理：[[12-双指针、字符串与数据结构设计题（Two Pointers, Strings, and Data-structure Design）]]

## 12. 选择速查（Selection Guide）
- **按索引快速读取、尾部追加**：优先选择 `list`，索引读取和尾部追加都很高效。
- **频繁从两端加入或删除**：优先选择 `collections.deque`，两端操作不需要移动中间元素。
- **后进先出**：使用 `list` 作为栈，核心操作是 `append()` 和 `pop()`。
- **先进先出**：使用 `collections.deque` 作为队列，核心操作是 `append()` 和 `popleft()`。
- **持续取得最小或最高优先级元素**：优先选择 `heapq`，它能持续维护堆顶并高效插入、弹出。
- **按键快速查询**：优先选择 `dict`，适合键值映射和快速成员判断。
- **去重与集合运算**：优先选择 `set`，直接支持成员判断、交集、并集和差集。
- **动态合并并判断连通性**：优先选择并查集（Disjoint-set Union, DSU），路径压缩与按规模合并能避免树链过深。
- **表达层级或有序搜索**：选择树或平衡搜索树；树自然表达父子关系，平衡结构可避免搜索路径严重退化。
- **表达网络、依赖或路线**：选择图的邻接表；稀疏图只记录实际存在的邻接关系。
- **固定容量并按最近使用淘汰**：选择 LRU 缓存，使用哈希表配合顺序结构同时维护查询和访问次序。
- **需要有序键且频繁插入删除**：选择平衡树、跳表或第三方有序容器，避免每次修改都移动连续数组元素。

## 13. 常用算法模板（Common Algorithm Patterns）
### 13.1 二分查找（Binary Search）
二分查找要求搜索空间具有单调性。维护半开区间 `[left, right)` 时，循环条件为 `left < right`，最终 `left` 表示第一个满足条件的位置。
```python
from bisect import bisect_left

values = [1, 3, 3, 7]
index = bisect_left(values, 3)
print(index, values[index])  # 1 3
```
### 13.2 排序（Sorting）

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|生成排序副本|`sorted(values, key=..., reverse=False)`|返回新列表，不修改原序列|
|列表原地排序|`values.sort(key=..., reverse=False)`|修改原列表，返回 `None`|
|稳定多字段排序|`sorted(records, key=lambda item: (item.group, item.score))`|相等键保持原相对顺序|
|取得最小的若干项|`heapq.nsmallest(k, values, key=...)`|返回升序列表，不修改输入|

### 13.3 遍历（Traversal）
- 深度优先搜索（Depth-first Search, DFS）使用递归或显式栈，适合路径探索、连通分量和回溯。
- 广度优先搜索（Breadth-first Search, BFS）使用 `collections.deque`，适合无权图最短步数和逐层遍历。
- 图可能有环，必须维护 `visited`；树遍历只有在节点不会重复引用时才可省略。
### 13.4 贪心、动态规划与分治（Greedy, Dynamic Programming, and Divide and Conquer）
- **贪心（Greedy）**：每一步选择当前最优方案；使用前必须证明局部最优能导向全局最优。
- **动态规划（Dynamic Programming, DP）**：定义状态、转移、初始条件和计算顺序；适合重叠子问题与最优子结构。
- **分治（Divide and Conquer）**：拆成相互独立的子问题，递归求解后合并；归并排序是典型示例。
```python
def fibonacci(count: int) -> int:
    if count < 0:
        raise ValueError("count must be non-negative")
    previous, current = 0, 1
    for _ in range(count):
        previous, current = current, previous + current
    return previous

print(fibonacci(7))  # 13
```
### 13.5 常见模式选择（Pattern Selection）
- 连续区间或子串问题先考虑滑动窗口、前缀和与双指针。
- 求最短步数且每条边代价相同，优先考虑 BFS。
- 需要尝试所有组合并撤销选择，考虑回溯。
- 需要维护动态最值或 Top-k，考虑堆。
- 需要动态合并连通分量，考虑并查集。
## 14. 常见错误（Common Errors）
- 用 `list.pop(0)` 实现高频队列出队，导致每次操作为 $O(n)$。
- 把自定义教学接口 `push()`、`enqueue()` 或 `size()` 当成 Python `list` 的真实方法。
- 在读取 `stack[-1]`、`queue[0]`、`heap[0]` 前没有检查空结构，触发 `IndexError`。
- 认为链表任意位置插入都是 $O(1)$，忽略定位目标或前驱节点所需的 $O(n)$。
- 修改双向链表时只更新一个方向的引用，破坏前后链接不变量。
- 把 `deque(maxlen=n)` 当成“满时拒绝写入”的队列，忽略其自动淘汰行为。
- 直接比较优先级相同但任务对象不可比较的堆元素，触发 `TypeError`。
- 在遍历 `dict` 或 `set` 的同时改变其大小，触发 `RuntimeError` 或造成逻辑错误。
- 依赖 `set` 的打印或遍历顺序；集合不提供稳定排序语义。
- 在无向图中只添加或删除一个方向的邻接记录，导致图结构不对称。
- 在有环图或循环链表中遍历时没有维护已访问集合或终止条件，造成无限循环。
- 在递归遍历深树或深图时忽略 Python 递归深度限制，应根据输入规模改用显式栈。

## 15. 相关笔记（Related Notes）
- [[01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）]]
- [[02-二分查找与边界搜索（Binary Search and Boundary Queries）]]
- [[03-顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）]]
- [[04-链表结构与实现（Linked-list Structures and Implementations）]]
- [[05-链表典型算法（Classic Linked-list Algorithms）]]
- [[06-递归、栈、队列与双端队列（Recursion, Stacks, Queues, and Deques）]]
- [[07-优先队列、堆与并查集（Priority Queues, Heaps, and Disjoint Sets）]]
- [[08-树、二叉搜索树与平衡树（Trees, Binary Search Trees, and Balanced Trees）]]
- [[09-哈希表与排序算法（Hash Tables and Sorting Algorithms）]]
- [[10-图结构、遍历与最短路径（Graphs, Traversal, and Shortest Paths）]]
- [[11-贪心、动态规划与分治（Greedy, Dynamic Programming, and Divide and Conquer）]]
- [[12-双指针、字符串与数据结构设计题（Two Pointers, Strings, and Data-structure Design）]]
- [[13-算法图示索引（Algorithm Diagram Index）]]
