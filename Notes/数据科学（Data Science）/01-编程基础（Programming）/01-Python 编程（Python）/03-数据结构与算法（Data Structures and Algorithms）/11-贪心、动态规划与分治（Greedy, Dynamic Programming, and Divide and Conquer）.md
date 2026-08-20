---
title: 贪心、动态规划与分治（Greedy, Dynamic Programming, and Divide and Conquer）
status: published
detail_level: comprehensive
published_at: 2026-08-17
updated_at: 2026-08-17
---
# 贪心、动态规划与分治（Greedy, Dynamic Programming, and Divide and Conquer）
## 1. 算法设计范式对比（Algorithm-design Paradigms）
- **贪心（Greedy）**：每一步选择当前看来最优的方案，并且不回退。
- **动态规划（Dynamic Programming, DP）**：保存重叠子问题答案，按状态转移组合全局最优解。
- **分治（Divide and Conquer）**：把问题拆成相对独立的子问题，递归求解后合并。
- **回溯（Backtracking）**：枚举决策树，发现前缀不可能成功时撤销并剪枝。

> [!tip] 大白话理解（Plain-language Intuition）
> 贪心像每个路口立刻选最便宜的路；动态规划像把“到每个路口的最佳成本”记下来；分治像把一大摞文件分给几个人处理后汇总；回溯像试密码，发现前几位已经不可能正确就立刻换分支。

## 2. 贪心算法（Greedy Algorithms）
贪心正确通常需要：
- **贪心选择性质（Greedy-choice Property）**：存在一个全局最优解包含当前局部最优选择。
- **最优子结构（Optimal Substructure）**：做出选择后，剩余问题的最优解能组成原问题最优解。
- 正确性应通过交换论证、割性质或数学归纳证明，不能只凭几个样例。

### 2.1 典型问题（Typical Problems）
- Dijkstra：在非负边条件下确定当前距离最小节点。
- Prim、Kruskal：利用最小生成树割性质选择安全边。
- 活动选择：按结束时间最早选择可兼容活动。
- 分数背包（Fractional Knapsack）：按单位价值降序取物，可切分时贪心正确。
- Huffman 编码：反复合并频率最低的两棵树，得到最优前缀编码。
- 集合覆盖的贪心只能给近似解，不保证最少集合数。

### 2.2 贪心局限（Limitations）
- 0-1 背包不能切分物品，按单位价值贪心可能错，应使用动态规划或搜索。
- 任意硬币系统中优先取最大面额不一定得到最少硬币；需证明币制满足条件，否则用 DP。
- 局部最短边不总能构成最短路径；Dijkstra 的正确性依赖非负边。

## 3. 动态规划（Dynamic Programming）
设计 DP 的核心步骤：
1. 定义状态（State）及其精确含义。
2. 写出状态转移（Transition）。
3. 确定基本情况和初始化。
4. 决定计算顺序，保证依赖状态先完成。
5. 从状态表中读取答案，并按需记录决策恢复方案。

### 3.1 自顶向下与自底向上（Top-down and Bottom-up）
- 记忆化搜索是自顶向下，只计算实际访问的状态，但使用调用栈。
- 表格法是自底向上，遍历顺序清晰，通常常数更小并便于空间压缩。
- 空间压缩只有在当前状态仅依赖有限旧层时安全；覆盖顺序必须避免读到本轮新值。

### 3.2 0-1 背包（0-1 Knapsack）
每件物品最多选择一次。令 `dp[c]` 表示容量 `c` 的最大价值，一维压缩时容量必须倒序遍历：
```python
def zero_one_knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    if len(weights) != len(values) or capacity < 0:
        raise ValueError("invalid knapsack input")
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for current in range(capacity, weight - 1, -1):
            dp[current] = max(dp[current], dp[current - weight] + value)
    return dp[capacity]

print(zero_one_knapsack([1, 3, 4], [15, 20, 30], 4))  # 35
```
- 若容量正序遍历，同一物品会在一轮内重复使用，算法变成完全背包（Unbounded Knapsack）。

### 3.3 常见 DP 模型（Common DP Models）
- Fibonacci：`dp[i] = dp[i-1] + dp[i-2]`，可压缩为两个变量。
- 网格不同路径：上方与左方路径数之和。
- Bellman–Ford：按允许边数逐层松弛，可视为 DP。
- 零钱兑换最少数量：`dp[amount] = min(dp[amount-coin] + 1)`。
- 零钱兑换组合数：硬币在外层可避免把不同顺序重复计数。
- 钢条切割和整数拆分：枚举第一段，再组合剩余最优解。
- 最长公共子序列（LCS）：字符相同取对角线加 1，否则取上方与左方最大值。
- 最长公共子串要求连续，不匹配时状态归零。
- 最长上升子序列可用 $O(n^2)$ DP，或用二分维护最小结尾做到 $O(n\log n)$。
- Catalan 数用于不同 BST、合法括号序列等递归组合结构。
- 打家劫舍：当前选择与前一个状态互斥。
- 旅行商问题可用位掩码 DP，时间约 $O(n^2 2^n)$，只适合较小 $n$。
- 股票问题的状态维度包括天数、是否持有、交易次数和冷冻期/手续费。

## 4. 分治算法（Divide and Conquer）
分治包含拆分、递归求解和合并。子问题通常相互独立，不像 DP 那样大量重叠。
- 二分查找：只进入一半区间。
- 归并排序：两半排序后线性合并。
- 快速排序：按基准分区后分别排序。
- 合并 $k$ 个有序链表：两两分治合并。
- 快速选择：只进入包含目标秩的一侧。
- 快速幂：利用 $x^n=(x^{n/2})^2$，指数减半。
```python
def fast_power(base: float, exponent: int) -> float:
    if exponent < 0:
        if base == 0:
            raise ZeroDivisionError("zero cannot have a negative exponent")
        return 1.0 / fast_power(base, -exponent)
    result = 1.0
    factor = base
    while exponent:
        if exponent & 1:
            result *= factor
        factor *= factor
        exponent >>= 1
    return result

print(fast_power(2, 10), fast_power(2, -2))  # 1024.0 0.25
```

## 5. 回溯算法（Backtracking）
回溯模板包含：当前路径、可选集合、结束条件、做选择、递归、撤销选择。
```python
def permutations(values: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    used = [False] * len(values)
    path: list[int] = []

    def search() -> None:
        if len(path) == len(values):
            result.append(path.copy())
            return
        for index, value in enumerate(values):
            if used[index]:
                continue
            used[index] = True
            path.append(value)
            search()
            path.pop()          # 撤销路径状态。
            used[index] = False # 撤销选择标记。

    search()
    return result

print(permutations([1, 2]))  # [[1, 2], [2, 1]]
```

### 5.1 去重与剪枝（Deduplication and Pruning）
- 全排列 II：先排序；同一层若前一个相同值尚未被使用，跳过当前值。
- 组合问题通过 `start` 索引避免排列顺序重复。
- 组合总和要区分元素可重复使用、每个元素只能一次、输入是否含重复值。
- N 皇后维护列、主对角线 `row-col`、副对角线 `row+col` 集合。
- 数独使用行、列、宫候选集合，并优先选择候选最少的空格。
- 剪枝只能排除不可能产生有效答案的分支，不能仅因“当前看起来较差”就删掉未证明的分支。

## 6. 选择范式（Choosing a Paradigm）

|问题特征|优先考虑|
|---|---|
|局部选择可证明安全|贪心|
|最优子结构且子问题重叠|动态规划|
|子问题相对独立且可合并|分治|
|需要枚举方案并可提前判死|回溯|
|状态空间巨大但存在单调性|二分、双指针或贪心|

## 7. 常见错误（Common Errors）
- 只展示贪心样例而没有正确性条件。
- DP 状态含义含糊，导致初始化与答案位置错误。
- 一维背包遍历方向错误。
- 回溯忘记撤销可变状态，分支相互污染。
- 把指数级回溯误报为多项式复杂度。
- 分治递归区间没有严格缩小。
- 空输入、容量 0、负指数和无解状态没有定义。

## 8. 相关笔记（Related Notes）
- [[09-哈希表与排序算法（Hash Tables and Sorting Algorithms）]]
- [[10-图结构、遍历与最短路径（Graphs, Traversal, and Shortest Paths）]]
- [[12-双指针、字符串与数据结构设计题（Two Pointers, Strings, and Data-structure Design）]]
