---
title: 顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）
aliases:
  - Python Dynamic Arrays
  - Python Lists and Sequential Storage
status: published
detail_level: comprehensive
merge_policy: union-zero-loss
published_at: 2026-08-17
updated_at: 2026-08-17
---
# 顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）
## 1. 线性表与存储模型（Linear Lists and Storage Models）
线性表（Linear List）是一组具有先后顺序的元素。除首尾元素外，每个元素通常有一个直接前驱和一个直接后继；元素个数可以固定，也可以随操作变化。
- **顺序表（Sequential List）**：把元素或元素引用存放在连续存储区中，逻辑顺序由物理排列自然表示。
- **链表（Linked List）**：节点可以分散存放，通过引用连接并表达逻辑顺序。
- 顺序表适合按索引随机访问；链表适合已知节点附近的链接修改。二者都是线性表的实现模型，不是两个互斥的抽象数据类型（Abstract Data Type, ADT）。

> [!tip] 大白话理解（Plain-language Intuition）
> 顺序表像一排连续编号的储物柜，知道号码就能直接走到目标柜；链表像寻宝提示，每个地点只告诉你下一个地点在哪里。前者查位置快，后者在已知连接点时改链条方便。

## 2. 连续存储与随机访问（Contiguous Storage and Random Access）
### 2.1 地址计算（Address Calculation）
若固定大小元素连续存储，首元素地址为 $BaseAddress$，每个元素占 $c$ 字节，则索引 $i$ 对应地址为：
$$
Address(i)=BaseAddress+i\times c
$$
- 索引是逻辑地址（Logical Address）；计算出的内存位置是物理地址（Physical Address）。
- 地址计算只需要固定次数的算术操作，因此随机访问为 $O(1)$。
- 前提是每个槽位宽度固定。如果元素本体大小不同，顺序表可以连续保存固定宽度的**引用**，再通过引用访问实际对象。
- Python `list` 采用后一种模型：内部连续保存 `PyObject*` 引用，而不是把不同大小的 Python 对象本体内嵌在同一数组中。

### 2.2 容量与逻辑长度（Capacity and Logical Size）
动态顺序表通常维护：
- **逻辑长度（Logical Size）**：当前实际包含的元素数。
- **容量（Capacity）**：当前存储区无需重新分配即可容纳的最大元素数。
- 必须始终满足不变量 $0\le size\le capacity$；只有 `[0, size)` 范围内的槽位属于有效元素。

### 2.3 一体式与分离式结构（Integrated and Separated Layouts）
- **一体式结构（Integrated Layout）**：表头元数据与固定元素区组成一个整体；扩大元素区通常需要搬迁整个对象。
- **分离式结构（Separated Layout）**：表对象保存长度、容量和指向独立元素区的引用；扩容时替换元素区引用，表对象本身可以保持不变。
- Python 层观察到的 `id(values)` 代表列表对象身份。CPython 内部元素引用数组重新分配时，列表对象身份通常不变；但 `values = values + [item]` 会创建并绑定新列表，不能据此推断 `id` 总是不变。

## 3. 动态扩容与摊还分析（Dynamic Growth and Amortized Analysis）
### 3.1 固定增量与几何增长（Fixed and Geometric Growth）
容量不足时需要申请更大存储区、复制现有引用，再释放旧存储区。
- **固定增量（Fixed Increment）**：每次增加固定槽位，空间浪费少，但连续追加 $n$ 个元素可能累计复制 $\Theta(n^2)$ 个引用。
- **几何增长（Geometric Growth）**：容量乘以大于 1 的比例，如 `1.5` 或 `2`；扩容次数约为 $O(\log n)$，连续追加的总复制量为 $O(n)$，因此单次追加的摊还复杂度为 $O(1)$。
- 几何比例越大，扩容更少但预留空间更多；比例越小，空间更紧凑但重新分配更频繁。

> [!tip] 大白话理解（Plain-language Intuition）
> 每来一个人就只加一把椅子，会不停搬桌子；一次多预留一些座位，偶尔搬一次但之后很多人都能直接坐下。某一次扩容仍然很贵，平均到一长串追加操作上却很便宜。

### 3.2 CPython `list` 的当前实现边界（Current CPython Implementation Boundary）
- Python 语言只规定 `list` 的行为，不承诺具体容量公式；PyPy 或未来 CPython 可以采用不同策略。
- 当前 CPython 主分支会进行温和的比例预分配并把容量调整到 4 的倍数，源码给出的典型容量序列为 `0, 4, 8, 16, 24, 32, 40, 52, 64, 76, ...`。
- 当前核心计算近似为 `newsize + newsize // 8 + 6` 后按 4 对齐；若一次增长很大，源码会减少不必要的预留。
- 因此原稿中的“空表先分配 8 个、满后扩 4 倍、大表再扩 2 倍”不能作为现代 CPython 的通用规则。

## 4. 教学型动态数组实现（Educational Dynamic-array Implementation）
下面使用 `ctypes.py_object` 创建固定容量的对象引用数组，以显式展示 `size`、`capacity`、扩容、移动和边界检查。生产代码通常应直接使用 Python `list`。
```python
import ctypes
from collections.abc import Iterator

class DynamicArray:
    def __init__(self, initial_capacity: int = 4) -> None:
        if initial_capacity <= 0:
            raise ValueError("initial_capacity must be positive")
        self._size = 0
        self._capacity = initial_capacity
        self._data = self._make_array(initial_capacity)

    @staticmethod
    def _make_array(capacity: int):
        return (ctypes.py_object * capacity)()

    def __len__(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return self._capacity

    def _normalize_index(self, index: int) -> int:
        # 与 Python 序列一致地支持负索引，但最终必须落在 [0, size)。
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("dynamic array index out of range")
        return index

    def _resize(self, new_capacity: int) -> None:
        new_data = self._make_array(new_capacity)
        for index in range(self._size):
            new_data[index] = self._data[index]
        self._data = new_data
        self._capacity = new_capacity

    def insert(self, index: int, value: object) -> None:
        if not 0 <= index <= self._size:
            raise IndexError("insert index out of range")
        if self._size == self._capacity:
            # 采用 2 倍增长便于展示；真实容器可选择其他几何比例。
            self._resize(self._capacity * 2)
        for position in range(self._size, index, -1):
            self._data[position] = self._data[position - 1]
        self._data[index] = value
        self._size += 1

    def append(self, value: object) -> None:
        self.insert(self._size, value)

    def remove_at(self, index: int) -> object:
        index = self._normalize_index(index)
        removed = self._data[index]
        for position in range(index, self._size - 1):
            self._data[position] = self._data[position + 1]
        self._size -= 1
        # 清除不再使用的引用，避免被删除对象因残留引用而无法回收。
        self._data[self._size] = None
        return removed

    def __getitem__(self, index: int) -> object:
        return self._data[self._normalize_index(index)]

    def __iter__(self) -> Iterator[object]:
        for index in range(self._size):
            yield self._data[index]

values = DynamicArray(initial_capacity=2)
values.append("A")
values.append("C")
values.insert(1, "B")
print(list(values))              # 输出: ['A', 'B', 'C']
print(len(values), values.capacity)  # 输出: 3 4
print(values[-1])                # 输出: C
print(values.remove_at(1))       # 输出: B
print(list(values))              # 输出: ['A', 'C']
```

### 4.1 操作复杂度（Operation Complexity）

|操作（Operation）|典型复杂度|最坏复杂度|原因|
|---|---:|---:|---|
|按索引读取/赋值|$O(1)$|$O(1)$|通过偏移直接定位槽位|
|尾部追加|摊还 $O(1)$|$O(n)$|扩容时复制全部有效引用|
|尾部删除|$O(1)$|$O(1)$|无需移动其他元素|
|头部或中间插入|$O(n)$|$O(n)$|后续引用整体右移|
|头部或中间保序删除|$O(n)$|$O(n)$|后续引用整体左移|
|按值查找|$O(n)$|$O(n)$|最坏需逐个比较|
|遍历|$O(n)$|$O(n)$|访问每个有效元素一次|

- 若允许破坏顺序，可用“目标槽位替换为尾元素，再弹出尾部”的方式在已知索引时做到 $O(1)$ 删除。
- `list.insert(len(values), item)` 与 `list.append(item)` 都表示尾部插入，但 `append()` 意图更清楚，通常也更直接。

## 5. Python `list` 与 `tuple`（Python Lists and Tuples）
### 5.1 `list`（Mutable Dynamic Sequence）
- `list` 是可变（Mutable）、保序（Ordered）的动态顺序表，槽位保存任意 Python 对象的引用。
- 索引访问通常为 $O(1)$；头部和中间插入、删除需要移动引用，为 $O(n)$。
- `append()` 是摊还 $O(1)$，不能误写成每次严格 $O(1)$。
- 列表保存引用，因此 `outer = [inner, inner]` 的两个槽位指向同一对象；通过任一槽位修改 `inner`，另一槽位会观察到相同变化。
### 5.2 `tuple`（Immutable Sequence）
- `tuple` 是不可变（Immutable）的顺序序列，创建后不能替换、插入或删除槽位。
- 不可变指元组保存的引用不变；若槽位引用可变对象，该对象内部仍可能变化。
- 元组无需为后续追加维护动态容量，适合表达固定记录和可哈希组合；只有所有元素均可哈希时，元组本身才可哈希。

## 6. 二维数组与嵌套序列（Two-dimensional Arrays and Nested Sequences）
Python 的嵌套列表是“外层引用数组 + 多个内层列表”，各行可以长度不同，并不保证所有数值本体形成一个连续二维内存块。

> [!example]- 引用式二维数组布局（Reference-based Two-dimensional Layout）
> ![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/03-顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）/03-顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）-20221104114132056.png]]

```python
rows = 3
columns = 4
matrix = [[0 for _ in range(columns)] for _ in range(rows)]
matrix[0][0] = 9
print(matrix)
# 期望输出:
# [[9, 0, 0, 0],
#  [0, 0, 0, 0],
#  [0, 0, 0, 0]]

aliased = [[0] * columns] * rows
aliased[0][0] = 9
print(aliased)
# 期望输出:
# [[9, 0, 0, 0],
#  [9, 0, 0, 0],
#  [9, 0, 0, 0]]
```
- `[[0] * columns] * rows` 复制的是同一个内层列表引用，修改一行会影响所有行。
- 规则矩阵应使用列表推导式为每一行创建独立对象。
- 需要紧凑同类型数值存储、向量化运算或明确行主序（Row-major Order）时，优先考虑 NumPy `ndarray`。

## 7. 空间局部性与遍历顺序（Spatial Locality and Traversal Order）
CPU 从内存读取数据时通常以缓存行（Cache Line）为单位带入相邻数据，常见缓存行大小为 64 字节。随后若立即访问邻近位置，更可能命中高速缓存；跨大步长访问则可能反复加载新缓存行。

> [!tip] 大白话理解（Plain-language Intuition）
> 去仓库拿一本书时，系统顺便把同一箱的书搬到手边。接下来按箱内顺序读就很省事；若每次都跳到另一个箱子，刚搬来的书还没用就被换走了。

> [!example]- 跨行访问导致缓存利用不足（Poor Cache Utilization）
> ![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/03-顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）/03-顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）-20221104164329026.png]]
> ![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/03-顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）/03-顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）-20221104164716282.png]]
> ![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/03-顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）/03-顺序表、动态数组与 Python 列表（Sequential Lists, Dynamic Arrays, and Python Lists）-20221104164947154.png]]

- Python `list` 的引用槽位连续，但被引用对象可能分散，因此局部性弱于紧凑的 C 数组或 NumPy 数组。
- 对 C 连续（C-contiguous）的 NumPy 二维数组，逐行访问通常比逐列跨步访问更符合空间局部性。
- I/O 也有类似现象：批量顺序读写通常比大量零散小请求更高效。
- 链表节点通常分散分配，遍历时缓存局部性通常较差，即使两种结构的渐近遍历复杂度都是 $O(n)$，实际常数仍可能相差很大。

## 8. 索引边界与负索引（Index Bounds and Negative Indices）
- 对长度为 `n` 的 Python 序列，非负有效索引为 `[0, n)`。
- Python 允许负索引，`-1` 表示最后一个元素；完整有效范围是 `[-n, n)`。
- 超出范围会抛出 `IndexError`；与某些底层语言不同，Python 不允许越界读写任意内存。
- 切片会把越界端点裁剪到合法范围，通常不抛 `IndexError`，因此 `values[100:200]` 可能返回空列表。
```python
values = [10, 20, 30]
print(values[-1])      # 输出: 30
print(values[100:])    # 输出: []

try:
    print(values[3])
except IndexError as error:
    print(type(error).__name__)  # 输出: IndexError
```

## 9. 合并相邻有序区间（Merge Adjacent Sorted Runs）
给定一个列表，其中 `[0, split)` 与 `[split, len(values))` 分别有序，可以用双指针在线性时间内合并。递归版每次复制较小元素也能得到 $O(n)$ 时间，但 Python 递归会额外使用 $O(n)$ 调用栈；迭代版更稳妥。
```python
def merge_sorted_runs(values: list[int], split: int) -> None:
    if not 0 <= split <= len(values):
        raise ValueError("split must be within the list")

    left = 0
    right = split
    merged: list[int] = []
    while left < split and right < len(values):
        if values[left] <= values[right]:
            merged.append(values[left])
            left += 1
        else:
            merged.append(values[right])
            right += 1

    merged.extend(values[left:split])
    merged.extend(values[right:])
    values[:] = merged  # 保留原列表对象身份，只替换其全部元素。

numbers = [1, 5, 6, 2, 4, 10, 11]
merge_sorted_runs(numbers, split=3)
print(numbers)  # 输出: [1, 2, 4, 5, 6, 10, 11]
```
- 时间复杂度为 $O(n)$，辅助空间为 $O(n)$。
- 若输入两个区间并非各自有序，算法仍会执行，但不能保证输出全局有序。
- 对稳定合并（Stable Merge），相等时优先取左区间元素，因此条件使用 `<=`。

## 10. 常见错误（Common Errors）
- 把“元素引用连续”误写成“所有 Python 对象本体连续”。
- 把尾部追加写成严格 $O(1)$，忽略偶发扩容与摊还分析。
- 中间插入后忘记移动后续元素，或移动方向错误导致覆盖尚未复制的值。
- 删除元素后保留不再使用的对象引用，造成对象生命周期意外延长。
- 用 `[[value] * columns] * rows` 创建矩阵，导致各行别名（Aliasing）。
- 依赖某个 CPython 版本的精确扩容公式，却把它当作 Python 语言保证。
- 只比较渐近复杂度，不考虑缓存局部性、对象开销和数据规模。

## 11. 完成检查（Checklist）
- [ ] 能区分线性表、顺序表、链表和动态数组。
- [ ] 能解释随机访问公式、逻辑长度、容量与分离式结构。
- [ ] 能用摊还分析说明几何扩容为何使连续追加达到摊还 $O(1)$。
- [ ] 能区分 Python `list` 的语言行为与 CPython 的实现细节。
- [ ] 能实现带边界检查、插入、删除、遍历和扩容的教学型动态数组。
- [ ] 能解释嵌套列表别名、空间局部性与 Python 负索引边界。
- [ ] 能用双指针稳定合并两个相邻有序区间并分析复杂度。

## 参考资料（References）
- [Python Design and History FAQ：How are lists implemented in CPython?](https://docs.python.org/3/faq/design.html#how-are-lists-implemented-in-cpython)
- [CPython `Objects/listobject.c`](https://github.com/python/cpython/blob/main/Objects/listobject.c)
- [Python Built-in Types：Sequence Types](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range)
