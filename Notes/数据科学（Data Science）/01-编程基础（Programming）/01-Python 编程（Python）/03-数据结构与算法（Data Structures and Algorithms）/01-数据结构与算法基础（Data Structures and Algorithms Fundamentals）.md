---
title: Python 数据结构与算法基础（Python Data Structures and Algorithms Fundamentals）
aliases:
  - Python Data Structures and Algorithms Fundamentals
  - Python 链表与复杂度
status: published
detail_level: comprehensive
merge_policy: union-zero-loss
published_at: 2026-08-17
updated_at: 2026-08-17
---
# Python 数据结构与算法基础（Python Data Structures and Algorithms Fundamentals）
## 1. 算法（Algorithm）
### 1.1 定义与作用（Definition and Purpose）
算法（Algorithm）是为解决一类问题或完成计算而设计的有限、严谨且可执行的步骤序列。算法通常接收零个或多个输入（Input），在有限时间内产生一个或多个输出（Output）。
- 算法描述解决问题的方法与思想，不依赖具体编程语言；Python 只是本系列的实现语言。
- 程序（Program）把算法编码为计算机可执行的指令，并通过数据结构（Data Structure）保存和组织算法处理的数据。
- “程序 = 数据结构 + 算法”：数据结构决定数据如何放置与访问，算法决定如何逐步处理数据。

> [!tip] 大白话理解（Plain-language Intuition）
> 数据结构像厨房里摆放食材的方式，算法像菜谱。食材堆得乱，即使菜谱正确也会不断花时间找东西；只有摆放方式和操作步骤互相匹配，程序才会高效。

### 1.2 算法的基本特性（Algorithm Properties）
1. **输入（Input）**：可以有零个或多个输入。
2. **输出（Output）**：至少产生一个结果；结果可以是返回值、状态变化或外部输出。
3. **有穷性（Finiteness）**：在有限步骤后终止，每一步也能在有限时间内完成。
4. **确定性（Definiteness）**：每一步含义明确，在给定状态下没有二义性。
5. **可行性（Effectiveness）**：每一步都能由计算模型实际执行。

### 1.3 从枚举到剪枝（From Enumeration to Pruning）
求自然数 $a,b,c$，使 $a+b+c=1000$ 且 $a^2+b^2=c^2$。三重枚举把三个变量都当作未知量，约执行 $O(n^3)$ 次组合；由第一个约束可直接得到 $c=1000-a-b$，因此只需枚举 $a,b$，降为 $O(n^2)$。
```python
def find_pythagorean_triples(total: int) -> list[tuple[int, int, int]]:
    results: list[tuple[int, int, int]] = []
    for a in range(total + 1):
        for b in range(total - a + 1):
            # c 已由和约束唯一确定；省去第三层循环与无效组合。
            c = total - a - b
            if a * a + b * b == c * c:
                results.append((a, b, c))
    return results

print(find_pythagorean_triples(1000))
# 期望输出:
# [(0, 500, 500), (200, 375, 425), (375, 200, 425), (500, 0, 500)]
```
- 两种算法得到同一结果，但工作量的增长阶不同。
- 原始运行秒数会受 CPU、操作系统、Python 版本与后台负载影响，不能把某次测得的 `1102` 秒或 `7` 秒当作算法固有属性。
- 若题目要求 $a,b,c$ 为正整数而不是含零的自然数，应把枚举起点改为 `1`，排除含零的两组结果。

## 2. 数据结构与抽象数据类型（Data Structures and Abstract Data Types）
### 2.1 数据结构（Data Structure）
数据结构（Data Structure）是组织、管理和存储数据的格式，目标是让特定访问与修改操作更高效。数据元素之间的逻辑关系、存储表示和允许的操作共同决定结构的行为。
- Python 内置数据结构（Built-in Data Structure）包括 `list`、`tuple`、`dict`、`set` 等。
- Python 标准库还提供 `collections.deque`、`heapq`、`queue.Queue` 等专用工具。
- 链表、图和自定义树等结构可以由类与对象实现；“Python 没有专用语法”不等于无法实现该结构。
- 数据结构是数据关系的静态表示；算法是在该结构上完成插入、删除、修改、查找、排序和遍历等操作的动态过程。

### 2.2 抽象数据类型（Abstract Data Type, ADT）
抽象数据类型（Abstract Data Type, ADT）由数据模型和一组操作契约组成，强调“能做什么”，不规定“内部怎样存”。例如栈（Stack）规定后进先出（Last In, First Out, LIFO），底层既可以使用动态数组，也可以使用链表。
- 常见操作包括插入（Insert）、删除（Delete）、修改（Update）、查找（Search）和排序（Sort）。
- 接口（Interface）把使用者与具体表示隔开，使实现可以在不改变调用方式的前提下替换。
- 同一个 ADT 的不同实现可能具有不同复杂度。例如队列若用 Python `list.pop(0)` 出队是 $O(n)$，用 `collections.deque.popleft()` 通常是 $O(1)$。

> [!tip] 大白话理解（Plain-language Intuition）
> ADT 像自动售货机的按钮和出货规则：使用者只关心按什么按钮会得到什么，不需要知道内部是传送带还是机械臂。实现可以更换，但对外承诺不能随意改变。

### 2.3 结构分类（Structure Categories）
#### 2.3.1 线性结构（Linear Structure）
- **顺序存储（Sequential Storage）**：元素或元素引用存放在连续区域，适合随机访问。Python `list` 是动态数组，连续保存对象引用，对象本身可以位于其他内存位置。
- **链式存储（Linked Storage）**：节点分散存放，通过引用连接；已知节点后的插入删除方便，但按位置查找需要逐节点遍历。
- 栈（Stack）、队列（Queue）和双端队列（Deque）是访问规则明确的 ADT，底层可用顺序存储或链式存储。
#### 2.3.2 非线性结构（Non-linear Structure）
- **树（Tree）**：表达层级关系，除根节点外每个节点通常只有一个父节点，可以有多个子节点。
- **图（Graph）**：由顶点（Vertex）和边（Edge）表达任意关系，一个顶点可以连接多个其他顶点。

## 3. 算法效率与渐近分析（Algorithm Efficiency and Asymptotic Analysis）
### 3.1 为什么不能只比较运行秒数（Why Wall-clock Time Is Insufficient）
实测时间（Wall-clock Time）会受到硬件、解释器、编译优化、缓存、输入分布和系统负载影响，因此只适合比较相同环境中的具体实现。复杂度分析则统计输入规模 $n$ 增长时基本操作数量或额外空间的增长趋势，用于跨环境比较算法的可扩展性。

> [!tip] 大白话理解（Plain-language Intuition）
> 秒表告诉你“这次跑了多久”，复杂度告诉你“数据扩大十倍以后会恶化到什么程度”。前者适合调优当前程序，后者适合在实现前排除扩展性很差的方案。

> [!example]- 线性查找与二分查找的成本曲线（Cost Curves）
> ![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）/01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）-20221108095747933.png]]
> ![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）/01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）-20221108100014451.png]]

### 3.2 大 O、大 Ω 与大 Θ（Big O, Big Omega, and Big Theta）
设 $f(n)$ 表示实际成本函数，$g(n)$ 表示用于描述增长量级的简化函数。
- **渐近上界（Asymptotic Upper Bound）**：若存在常数 $c>0$ 和 $n_0$，使所有 $n\ge n_0$ 都满足 $f(n)\le c g(n)$，则 $f(n)=O(g(n))$。
- **渐近下界（Asymptotic Lower Bound）**：若存在常数 $c>0$ 和 $n_0$，使所有 $n\ge n_0$ 都满足 $f(n)\ge c g(n)$，则 $f(n)=\Omega(g(n))$。
- **渐近紧界（Asymptotic Tight Bound）**：若存在正常数 $c_1,c_2,n_0$，使所有 $n\ge n_0$ 都满足 $c_1g(n)\le f(n)\le c_2g(n)$，则 $f(n)=\Theta(g(n))$。

> [!example]- 渐近界示意（Asymptotic Bounds）
> ![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）/01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）-20221108103846566.png]]

> [!tip] 大白话理解（Plain-language Intuition）
> $O$ 像成本的天花板，$\Omega$ 像地板，$\Theta$ 表示上下都被同一量级夹住。日常口语常把 $O$ 当作“复杂度等于”，严谨分析时应分清它只是上界还是紧确量级。

### 3.3 化简规则（Simplification Rules）
- 忽略常数因子：$100n^2=O(n^2)$。
- 多项式保留最高阶项：$n^3+n^2+n=O(n^3)$。
- 顺序执行的独立部分相加并保留主导项：$O(n)+O(n^2)=O(n^2)$。
- 嵌套循环在每层次数独立时相乘：两层各遍历 $n$ 次得到 $O(n^2)$。
- 分支在最坏情况分析中取代价最大的路径。
- 不同常数底的对数只差常数倍，因此通常统一写作 $O(\log n)$；$\log(n^c)=c\log n$，常数 $c$ 可忽略。
- 不能机械地把所有嵌套循环都相乘；若内层次数依赖外层索引，应先求和。例如 $1+2+\cdots+n=\Theta(n^2)$。

### 3.4 最好、平均、最坏与摊还成本（Best, Average, Worst, and Amortized Costs）
- **最好情况（Best Case）**：某些输入上所需的最少操作数。
- **平均情况（Average Case）**：在明确输入分布假设下的期望操作数；没有概率模型就不能随意声称“平均”。
- **最坏情况（Worst Case）**：规模为 $n$ 的所有合法输入中的最大操作数，能提供稳定上界。
- **摊还复杂度（Amortized Complexity）**：分析一串操作的平均成本，不依赖随机输入。例如 Python `list.append()` 偶尔需要扩容，但连续多次追加的摊还成本为 $O(1)$。

### 3.5 时间复杂度与空间复杂度（Time and Space Complexity）
- 时间复杂度（Time Complexity）衡量基本操作次数随 $n$ 的增长趋势。
- 空间复杂度（Space Complexity）通常衡量算法除输入本身之外所需的额外空间（Auxiliary Space）。
- 递归调用栈必须计入额外空间；尾递归在 CPython 中不会自动消除，因此深递归仍可能触发 `RecursionError`。

常见增长速度从低到高：
$$
O(1)<O(\log n)<O(n)<O(n\log n)<O(n^2)<O(n^3)<O(2^n)<O(n!)
$$

> [!example]- 常见复杂度增长曲线（Common Growth Rates）
> ![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）/01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）-20221108114915524.png]]

### 3.6 规模与耗时估算（Scale and Runtime Estimation）
假设一次基本操作耗时 $1$ 微秒，则 1 秒能执行约 $10^6$ 次操作，1 天约执行 $8.64\times10^{10}$ 次操作。
- 若 $f(n)=n^2$，1 秒可处理的最大规模约为 $1000$；1 天约为 $293938$。
- 若 $f(n)=\log_2 n$，理论规模可达到 $2^{10^6}$；现实中输入存储会先成为限制。
- 若 $f(n)=n!$，1 秒内最大约为 $9!$，1 天内最大约为 $13!$，说明阶乘增长很快失去可行性。
- 若冒泡排序处理 200 个元素耗时 200 秒，在同一环境下给 800 秒，时间扩大 4 倍；因成本近似与 $n^2$ 成正比，规模只能扩大 $\sqrt{4}=2$ 倍，约处理 400 个元素。

## 4. Python 性能测量（Python Performance Measurement）
### 4.1 `timeit` 的职责与 API（Purpose and API of `timeit`）
`timeit` 用于重复执行一小段代码，以降低定时器分辨率和偶发系统噪声的影响。复杂度解释增长趋势，基准测试（Benchmark）比较具体实现。
- `timeit.Timer(stmt='pass', setup='pass', timer=default_timer, globals=None)` 创建计时器。
- **`stmt`**：待测语句字符串或无参数可调用对象（Callable）。
- **`setup`**：每轮计时前所需的设置代码。
- **`timer`**：底层计时函数，通常保持默认值。
- **`globals`**：执行字符串语句时使用的全局命名空间。
- `Timer.timeit(number=1_000_000)` 返回 `stmt` 执行 `number` 次的**总秒数**，不是平均值；单次平均耗时需再除以 `number`。
- `Timer.repeat(repeat=5, number=...)` 返回多组总耗时；常取最小值观察较少受其他进程干扰的一次。
```python
from timeit import repeat

def build_with_append(size: int = 10_000) -> list[int]:
    result: list[int] = []
    for value in range(size):
        result.append(value)
    return result

def build_with_comprehension(size: int = 10_000) -> list[int]:
    return [value for value in range(size)]

append_runs = repeat(build_with_append, repeat=5, number=100)
comprehension_runs = repeat(build_with_comprehension, repeat=5, number=100)
print(min(append_runs) > 0)         # 输出: True
print(min(comprehension_runs) > 0)  # 输出: True
# 具体秒数依赖机器、Python 版本和当前负载，不应写成固定输出。
```

### 4.2 基准测试常见陷阱（Benchmark Pitfalls）
- 不要把输入构造、文件 I/O 或网络请求意外计入只想测量的核心操作。
- 比较方案必须使用等价输入与结果，避免一个函数完成了更多工作。
- 重复多组，避免首次导入、缓存状态和后台进程造成误判。
- 微基准测试的微小差异不一定代表真实应用；数据规模、内存占用和可读性同样重要。

## 5. Python 常用容器复杂度（Common Python Container Complexities）
以下复杂度描述主流 CPython 实现的典型行为；哈希冲突、内存分配与解释器实现可能改变常数或最坏情况。

|`list` 操作（Operation）|平均/摊还成本|最坏成本|原因|
|---|---:|---:|---|
|`items[index]`、赋值|$O(1)$|$O(1)$|按偏移访问对象引用|
|`append(value)`|摊还 $O(1)$|$O(n)$|偶尔扩容并复制引用|
|`pop()`|$O(1)$|$O(1)$|删除尾部元素|
|`insert(0, value)`、`pop(0)`|$O(n)$|$O(n)$|需要移动后续引用|
|`value in items`、`index(value)`|$O(n)$|$O(n)$|最坏需顺序比较|
|切片 `items[a:b]`|$O(k)$|$O(k)$|创建含 $k$ 个引用的新列表|
|`sort()`|$O(n\log n)$|$O(n\log n)$|CPython 使用 Timsort|

|`dict` / `set` 操作（Operation）|平均成本|最坏成本|说明|
|---|---:|---:|---|
|按键查询、插入、删除|$O(1)$|$O(n)$|依赖哈希分布与扩容|
|`key in mapping`|$O(1)$|$O(n)$|直接使用哈希表索引|
|遍历|$O(n)$|$O(n)$|访问全部有效条目|
|复制|$O(n)$|$O(n)$|需要复制全部条目|

## 6. 单向链表（Singly Linked List）
### 6.1 节点与头引用（Node and Head Reference）
单向链表节点包含数值域（Data Field）与链接域（Link Field）。`next` 保存下一个节点的引用，尾节点的 `next` 为 `None`；链表对象的 `head` 指向首个数据节点，空链表的 `head` 为 `None`。只有额外创建且不存业务数据的节点才称为哨兵节点（Sentinel Node）。

> [!example]- 单节点与空链接图示（Single Node and Null Link）
> ![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）/01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）-1742553847583.png]]
> [!example]- 多节点单向链表图示（Multi-node Singly Linked List）
> ![[Attachments/Notes/数据科学（Data Science）/01-编程基础（Programming）/01-Python 编程（Python）/03-数据结构与算法（Data Structures and Algorithms）/01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）/01-数据结构与算法基础（Data Structures and Algorithms Fundamentals）-1742553854902.png]]

### 6.2 完整最小实现（Complete Minimal Implementation）
```python
from dataclasses import dataclass
from typing import Iterator, Optional

@dataclass
class Node:
    item: object
    next: "Optional[Node]" = None

class SinglyLinkedList:
    def __init__(self, node: Optional[Node] = None) -> None:
        self.head = node

    def is_empty(self) -> bool:
        return self.head is None

    def __len__(self) -> int:
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count

    def __iter__(self) -> Iterator[object]:
        current = self.head
        while current is not None:
            yield current.item
            current = current.next

    def append(self, item: object) -> None:
        new_node = Node(item)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

linked_list = SinglyLinkedList()
print(linked_list.is_empty())  # 输出: True
linked_list.append("乔峰")
linked_list.append("虚竹")
linked_list.append("段誉")
print(len(linked_list))        # 输出: 3
print(list(linked_list))       # 输出: ['乔峰', '虚竹', '段誉']
```

### 6.3 操作复杂度（Operation Complexity）

|操作（Operation）|当前实现|说明|
|---|---:|---|
|判断为空|$O(1)$|只检查 `head`|
|长度|$O(n)$|每次从头遍历；维护计数器可换取 $O(1)$|
|遍历|$O(n)$|每个节点访问一次|
|尾部追加|$O(n)$|当前实现需寻找尾节点；维护 `tail` 可降为 $O(1)$|
|已知节点后插入|$O(1)$|直接修改有限个链接|
|按索引查找|$O(n)$|必须从头依次前进|

## 7. 常见错误与边界（Common Errors and Edge Cases）
- 把大 O 当作精确秒数或自动当作紧确界；应结合 $\Omega$、$\Theta$ 与实测数据理解。
- 忽略输入前提。例如二分查找要求有序序列，哈希表平均 $O(1)$ 依赖合理哈希分布。
- 只报告平均情况却没有输入分布假设，或只报告最好情况掩盖最坏性能。
- 把输入本身占用空间与算法额外空间混在一起；报告时应说明度量口径。
- 使用 `== None` 虽可工作，但判断 `None` 单例时应写 `is None`。
- 链表遍历时忘记执行 `current = current.next` 会造成死循环；修改链接顺序错误可能丢失后续链条。
- 链表不是所有场景都比列表高效。Python `list` 的缓存局部性和成熟实现使其在许多日常任务中更快。

## 8. 完成检查（Checklist）
- [ ] 能说明算法的五个基本特性及算法与编程语言的关系。
- [ ] 能区分数据结构、算法和抽象数据类型（ADT）。
- [ ] 能解释 $O$、$\Omega$、$\Theta$ 以及最好、平均、最坏和摊还复杂度。
- [ ] 能根据顺序、循环和分支结构估算主导增长项。
- [ ] 能正确使用 `timeit`，并说明为什么返回值不是固定性能结论。
- [ ] 能比较 Python `list`、`dict`、`set` 和链表的典型操作复杂度。
- [ ] 能实现单链表的判空、长度、遍历与尾部追加，并分析复杂度。
