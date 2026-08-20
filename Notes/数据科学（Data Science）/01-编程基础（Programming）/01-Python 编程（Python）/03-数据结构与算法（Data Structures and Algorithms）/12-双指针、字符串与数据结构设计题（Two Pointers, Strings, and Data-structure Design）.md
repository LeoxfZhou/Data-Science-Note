---
title: 双指针、字符串与数据结构设计题（Two Pointers, Strings, and Data-structure Design）
status: published
detail_level: comprehensive
published_at: 2026-08-17
updated_at: 2026-08-17
---
# 双指针、字符串与数据结构设计题（Two Pointers, Strings, and Data-structure Design）
## 1. 双指针（Two Pointers）
双指针不是固定算法，而是用两个位置变量表达窗口、区间或相对速度，避免重复扫描。
### 1.1 同向指针（Same-direction Pointers）
- 快慢指针原地移除或压缩元素，例如移动零。
- 滑动窗口（Sliding Window）维护满足条件的连续区间。
- 链表快慢指针用于中点、倒数节点和环检测。
### 1.2 相向指针（Opposite-direction Pointers）
- 有序数组两数之和：和过小移动左指针，过大移动右指针。
- 盛最多水的容器：移动较短边，才有机会提高受限高度。
- 三数之和、四数之和：排序后固定外层元素，内层相向扫描并去重。
```python
from __future__ import annotations

def two_sum_sorted(values: list[int], target: int) -> tuple[int, int] | None:
    left, right = 0, len(values) - 1
    while left < right:
        total = values[left] + values[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None

print(two_sum_sorted([2, 7, 11, 15], 9))  # (0, 1)
```
- 双指针移动规则必须由单调性支撑；无序数组通常不能直接根据和的大小决定方向。
- 排序会改变原索引，题目要求原位置时需保留索引或改用哈希表。

## 2. 滑动窗口（Sliding Window）
窗口通常表示 `[left, right]`：右端扩张引入新元素，条件不满足时左端收缩并移除旧元素。
- 最长无重复子串：记录字符最后出现位置，左边界只能右移不能回退。
- 最小覆盖子串：维护需求计数与已满足种类，满足后尽量收缩。
- 固定长度窗口：每次加入右元素并删除刚离开窗口的左元素。

> [!tip] 大白话理解（Plain-language Intuition）
> 滑动窗口像一把可伸缩的尺子。右端先把候选范围拉长，一旦违反条件，左端就往右缩；每个元素最多从两端各经过一次，所以常能把两层循环降到线性时间。

## 3. 字符串匹配与回文（String Matching and Palindromes）
### 3.1 子串查找（Substring Search）
- 朴素匹配最坏 $O(nm)$。
- KMP（Knuth–Morris–Pratt）用前缀函数/失配表复用已匹配信息，时间 $O(n+m)$。
- Python 生产代码通常使用 `in`、`str.find()`；手写 KMP用于理解或特定流式场景。
### 3.2 最长公共前缀（Longest Common Prefix）
可纵向比较所有字符串同一位置，或以首字符串为候选不断缩短。空输入和空字符串必须定义。
### 3.3 最长回文子串（Longest Palindromic Substring）
- 中心扩展：每个字符和相邻间隙分别作为奇偶中心，时间 $O(n^2)$、空间 $O(1)$。
- 动态规划：记录区间是否回文，时间和空间均 $O(n^2)$。
- Manacher 算法可达 $O(n)$，实现更复杂。
```python
def longest_palindrome(text: str) -> str:
    best_start = best_end = 0

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(text) and text[left] == text[right]:
            left -= 1
            right += 1
        return left + 1, right - 1

    for center in range(len(text)):
        for start, end in (expand(center, center), expand(center, center + 1)):
            if end - start > best_end - best_start:
                best_start, best_end = start, end
    return text[best_start:best_end + 1]

print(longest_palindrome("babad"))  # bab（aba 也是合法最长答案）
```

## 4. LRU 缓存（Least Recently Used Cache）
LRU 淘汰最久未访问的条目。要让查询、更新和淘汰均为 $O(1)$，组合：
- 哈希表：键到节点的直接定位。
- 双向链表：按最近使用次序移动和删除节点。
- 访问或更新后把节点移动到最近使用端；容量满时删除最久未使用端。
- Python 可用 `collections.OrderedDict` 简化实现；并发环境仍需锁。
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.data: OrderedDict[str, int] = OrderedDict()

    def get(self, key: str) -> int | None:
        if key not in self.data:
            return None
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key: str, value: int) -> None:
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)

cache = LRUCache(2)
cache.put("a", 1); cache.put("b", 2); cache.get("a"); cache.put("c", 3)
print(cache.get("b"), cache.get("a"), cache.get("c"))  # None 1 3
```

## 5. LFU 缓存（Least Frequently Used Cache）
LFU 先淘汰访问频率最低项，频率相同再按最久未使用淘汰。
- 哈希表保存键到 `(值, 频率, 节点)`。
- 每个频率维护一个 LRU 双向链表或 `OrderedDict`。
- 维护当前最小频率，才能 $O(1)$ 找到淘汰桶。
- 更新频率时从旧桶删除、加入新桶；旧最小桶变空后递增最小频率。
- LFU 比 LRU 状态更多，边界包括更新已有键、容量 0、频率桶清理和同频次序。

## 6. 跳表与随机层级（Skip List and Random Levels）
跳表在有序链表上增加多级索引，期望查询、插入、删除为 $O(\log n)$，最坏 $O(n)$。
- 随机层级通常以固定概率继续上升，层数分布近似几何分布。
- 插入先记录每层前驱，再生成层级并更新多层链接。
- 随机性影响形状，不影响有序性；测试可注入固定随机种子。
- 并发跳表还需要额外同步或无锁设计，教学单线程实现不能直接用于并发。

## 7. 随机数与采样（Random Numbers and Sampling）
线性同余生成器（Linear Congruential Generator, LCG）：
$$
X_{n+1}=(aX_n+c)\bmod m
$$
- 参数决定周期和统计质量；LCG 不适合密码学。
- Python `random` 适合模拟和普通采样，不适合令牌、密码和安全随机数；安全用途使用 `secrets`。
- 洗牌应使用 Fisher–Yates，不能为每个元素随机一个排序键来假装均匀洗牌。
- 蓄水池采样（Reservoir Sampling）可在未知长度流中均匀选取固定数量样本。

## 8. 设计型题目（Design Problems）
### 8.1 最小栈（Min Stack）
主栈保存值，辅助栈保存到当前位置的最小值；压栈、弹栈和取最小值均为 $O(1)$。重复最小值必须重复记录或保存计数。
### 8.2 TinyURL
- 生成唯一短码并映射到长 URL；需处理冲突、持久化、过期、访问控制和滥用。
- 可使用自增 ID 的 Base62 编码或安全随机码；哈希截断必须处理碰撞。
- 不应把私人 URL、令牌或凭据直接暴露在公开映射中。
### 8.3 Twitter Feed
- 关注图、发帖时间线和获取最近动态是不同职责。
- 拉取时可对每个关注者的有序推文流执行多路归并；大规模系统需权衡 fan-out on write 与 fan-out on read。
- 取消关注自己、重复关注、时间戳单调性和分页游标是重要边界。

## 9. 股票动态规划（Stock-trading Dynamic Programming）
统一状态为“第 `day` 天结束时，持有或不持有股票的最大收益”，再增加交易次数、手续费或冷冻期维度。
- 单次交易：跟踪历史最低价格或两状态 DP。
- 无限次交易：每段正差价均可吸收；同一天不能同时依赖更新后的状态。
- 手续费：在买入或卖出的一侧扣一次，不能重复扣。
- 冷冻期：买入状态依赖两天前的不持有状态。
- 最多两次或 $k$ 次交易：维护交易次数维度；当 $k\ge n/2$ 时等价于无限次交易。

## 10. 常见错误（Common Errors）
- 双指针缺少单调性依据。
- 滑动窗口左边界回退，导致重复计数。
- LRU 只用队列，查询或中间删除退化为 $O(n)$。
- LFU 忘记同频率下的 LRU 规则。
- 用非安全伪随机数生成密码或公开短码。
- 设计题只写核心容器，不定义容量、并发、持久化、失败和过期契约。
- 股票 DP 在同一轮错误复用已更新状态，等价于允许不符合题意的同日交易。

## 11. 相关笔记（Related Notes）
- [[06-递归、栈、队列与双端队列（Recursion, Stacks, Queues, and Deques）]]
- [[11-贪心、动态规划与分治（Greedy, Dynamic Programming, and Divide and Conquer）]]
