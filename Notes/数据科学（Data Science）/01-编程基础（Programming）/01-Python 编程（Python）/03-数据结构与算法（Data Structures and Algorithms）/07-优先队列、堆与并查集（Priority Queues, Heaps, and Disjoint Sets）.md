---
title: 优先队列、堆与并查集（Priority Queues, Heaps, and Disjoint Sets）
status: published
detail_level: comprehensive
published_at: 2026-08-17
updated_at: 2026-08-17
---
# 优先队列、堆与并查集（Priority Queues, Heaps, and Disjoint Sets）
## 1. 优先队列（Priority Queue）
优先队列按优先级而非进入顺序取出元素。抽象操作通常包括 `push`、查看最高优先级元素 `peek` 和删除最高优先级元素 `pop`。

|实现（Implementation）|插入|查看最小值|删除最小值|
|---|---:|---:|---:|
|无序数组|$O(1)$|$O(n)$|$O(n)$|
|有序数组|$O(n)$|$O(1)$|$O(1)$|
|二叉堆（Binary Heap）|$O(\log n)$|$O(1)$|$O(\log n)$|

- Python `heapq` 提供最小堆（Min-heap）。最大堆可存负优先级，或在支持相应 API 的版本使用最大堆函数。
- 元组按字段依次比较；优先级相同时，若任务对象不可比较，应加入单调计数器作为稳定平局字段。
```python
from heapq import heappop, heappush
from itertools import count

counter = count()
tasks: list[tuple[int, int, str]] = []
heappush(tasks, (2, next(counter), "normal"))
heappush(tasks, (1, next(counter), "urgent"))
heappush(tasks, (1, next(counter), "another urgent"))
print([heappop(tasks)[2] for _ in range(len(tasks))])
# 期望输出:
# ['urgent', 'another urgent', 'normal']
```

## 2. 二叉堆（Binary Heap）
完全二叉树（Complete Binary Tree）可紧凑存入数组。最小堆要求任意父节点不大于子节点，最大堆反之。
### 2.1 数组索引关系（Array Index Relationships）
对从 0 开始的索引 $i$：
- 父节点：$(i-1)//2$，仅当 $i>0$。
- 左孩子：$2i+1$。
- 右孩子：$2i+2$。
- 若孩子索引不小于数组长度，则该孩子不存在。

> [!tip] 大白话理解（Plain-language Intuition）
> 堆只保证“家长不比孩子大”，不保证兄弟之间或整层已经排序。因此根节点一定最小，但寻找任意其他值仍可能要看很多节点。

### 2.2 上浮、下沉与建堆（Sift Up, Sift Down, and Heapify）
- **上浮（Sift Up）**：新元素先放数组末尾，与父节点比较并交换，直到堆序恢复。
- **下沉（Sift Down）**：删除根后把末尾元素移到根，与更合适的孩子交换，直到堆序恢复。
- 从最后一个非叶节点向前执行下沉可在线性时间 $O(n)$ 建堆；逐个插入为 $O(n\log n)$。
- `heapq.heapify(values)` 原地建堆，不返回新列表。

### 2.3 堆排序（Heap Sort）
堆排序先建最大堆，再反复把根与未排序区末尾交换并缩小堆。
- 时间复杂度始终为 $O(n\log n)$。
- 原地版本额外空间为 $O(1)$。
- 通常不稳定（Unstable），相等元素的相对次序可能改变。
- Python 业务代码通常直接使用稳定的 `sorted()`；手写堆排序主要用于学习或受限环境。

## 3. Top-K 与数据流问题（Top-K and Streaming Problems）
- 求第 $k$ 大元素时维护大小为 $k$ 的最小堆；堆顶是当前前 $k$ 大中的最小者。
- 求第 $k$ 小元素时维护大小为 $k$ 的最大堆。
- 数据流中位数使用最大堆保存较小一半、最小堆保存较大一半，并保持长度差不超过 1。
```python
def kth_largest(values: list[int], k: int) -> int:
    if not 1 <= k <= len(values):
        raise ValueError("k must be in [1, len(values)]")
    heap: list[int] = []
    for value in values:
        heappush(heap, value)
        if len(heap) > k:
            heappop(heap)
    return heap[0]

print(kth_largest([3, 2, 1, 5, 6, 4], 2))  # 5
```

## 4. 阻塞队列（Blocking Queue）
阻塞队列在空队列读取时等待数据，在有界队列已满时等待空间，常用于生产者—消费者模型（Producer–Consumer Model）。
- Python 线程使用 `queue.Queue(maxsize=n)`；`put()` 与 `get()` 可阻塞并支持超时。
- 每次成功 `get()` 后应在 `finally` 中调用 `task_done()`，确保异常不会让 `join()` 永久等待。
- 结束工作线程可发送唯一哨兵对象；哨兵数量通常至少等于消费者数量。
- `asyncio.Queue` 面向协程，不应跨线程当作 `queue.Queue` 使用。

> [!tip] 大白话理解（Plain-language Intuition）
> 普通队列只负责存取，阻塞队列还负责“没货就等、仓库满了也等”，避免生产者和消费者不停轮询浪费 CPU。

## 5. 并查集（Disjoint-set Union, DSU）
并查集维护若干互不相交集合，支持：
- `find(x)`：找到元素所属集合的代表元（Representative）。
- `union(a, b)`：合并两个集合。
- `connected(a, b)`：判断两个元素是否属于同一集合。

### 5.1 路径压缩与按规模合并（Path Compression and Union by Size）
- 路径压缩让查找沿途节点直接指向根。
- 按规模或按秩合并让较小树接到较大树下，避免形成长链。
- 两种优化同时使用时，单次操作的摊还复杂度为 $O(\alpha(n))$，其中反阿克曼函数（Inverse Ackermann Function）增长极慢，工程上近似常数。
```python
class DisjointSet:
    def __init__(self, size: int) -> None:
        if size < 0:
            raise ValueError("size must be non-negative")
        self.parent = list(range(size))
        self.component_size = [1] * size

    def find(self, item: int) -> int:
        root = item
        while root != self.parent[root]:
            root = self.parent[root]
        while item != root:
            parent = self.parent[item]
            self.parent[item] = root
            item = parent
        return root

    def union(self, first: int, second: int) -> bool:
        root_a, root_b = self.find(first), self.find(second)
        if root_a == root_b:
            return False
        if self.component_size[root_a] < self.component_size[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        self.component_size[root_a] += self.component_size[root_b]
        return True

    def connected(self, first: int, second: int) -> bool:
        return self.find(first) == self.find(second)

dsu = DisjointSet(5)
dsu.union(0, 1)
dsu.union(1, 2)
print(dsu.connected(0, 2), dsu.connected(0, 4))  # True False
```

### 5.2 典型用途（Typical Uses）
- Kruskal 最小生成树。
- 动态连通性、朋友圈或网络分组。
- 检测无向图加入边后是否形成环。
- 网格岛屿合并和等价关系维护。
- 普通并查集不支持高效删除或拆分集合；需要回滚并查集或动态连通结构时必须改用专门设计。

## 6. 常见错误（Common Errors）
- 误以为堆数组整体有序。
- 只按优先级压入不可比较对象，平局时触发 `TypeError`。
- Top-K 堆方向用反，或未检查非法 `k`。
- `Queue.get()` 后忘记 `task_done()`，导致 `join()` 不返回。
- 并查集合并时直接连接原元素而不是根，破坏集合结构。
- 递归 `find()` 在退化树上可能超过 Python 递归深度；迭代实现更稳健。

## 7. 相关笔记（Related Notes）
- [[06-递归、栈、队列与双端队列（Recursion, Stacks, Queues, and Deques）]]
- [[08-树、二叉搜索树与平衡树（Trees, Binary Search Trees, and Balanced Trees）]]
- [[10-图结构、遍历与最短路径（Graphs, Traversal, and Shortest Paths）]]
