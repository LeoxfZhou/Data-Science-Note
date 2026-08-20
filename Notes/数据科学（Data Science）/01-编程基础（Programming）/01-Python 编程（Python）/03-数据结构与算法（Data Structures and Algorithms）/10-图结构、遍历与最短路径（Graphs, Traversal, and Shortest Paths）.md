---
title: 图结构、遍历与最短路径（Graphs, Traversal, and Shortest Paths）
status: published
detail_level: comprehensive
published_at: 2026-08-17
updated_at: 2026-08-17
---
# 图结构、遍历与最短路径（Graphs, Traversal, and Shortest Paths）
## 1. 图的基本概念（Graph Fundamentals）
图（Graph）由顶点集合 $V$ 和边集合 $E$ 构成，记作 $G=(V,E)$。
- 无向图（Undirected Graph）的边没有方向；有向图（Directed Graph）的边从起点指向终点。
- 加权图（Weighted Graph）的边带权重，可表示距离、费用、时间或容量。
- 无向图节点的度（Degree）是相邻边数；有向图分入度（In-degree）和出度（Out-degree）。
- 路径（Path）是相邻顶点序列；简单路径不重复顶点。
- 环（Cycle）是起点与终点相同的非空路径。
- 连通图（Connected Graph）中任意两点可达；有向图需区分强连通（Strongly Connected）和弱连通（Weakly Connected）。
- 稠密图边数接近 $|V|^2$；稀疏图边数远小于该数量级。

## 2. 图的表示（Graph Representations）
### 2.1 邻接表（Adjacency List）
每个顶点保存出边列表，空间为 $O(|V|+|E|)$，适合稀疏图，也是多数图算法的默认表示。
### 2.2 邻接矩阵（Adjacency Matrix）
$|V|\times|V|$ 矩阵直接记录边或权重，判断特定边为 $O(1)$，空间为 $O(|V|^2)$，适合稠密图或矩阵算法。
### 2.3 边列表（Edge List）
直接保存 `(起点, 终点, 权重)`，适合 Bellman–Ford 和 Kruskal 等按边扫描的算法。

> [!tip] 大白话理解（Plain-language Intuition）
> 邻接表像每个人的通讯录，只记录真正认识的人；邻接矩阵像全班两两关系表，即使两人不认识也占一个格子。关系稀疏时通讯录更省空间。

## 3. 深度优先与广度优先（DFS and BFS）
### 3.1 深度优先搜索（Depth-first Search, DFS）
DFS 沿一条分支走到底再回退，使用递归调用栈或显式栈。
- 用于连通分量、环检测、拓扑排序、路径枚举和回溯。
- 必须在入栈或进入递归时标记已访问，避免环导致无限循环。
### 3.2 广度优先搜索（Breadth-first Search, BFS）
BFS 按距离层次扩展，使用队列。在无权图中首次到达某点时得到最少边数路径。
```python
from collections import deque

Graph = dict[str, list[str]]

def bfs_distances(graph: Graph, start: str) -> dict[str, int]:
    distances = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in distances:
                distances[neighbor] = distances[node] + 1
                queue.append(neighbor)
    return distances

graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
print(bfs_distances(graph, "A"))
# 期望输出:
# {'A': 0, 'B': 1, 'C': 1, 'D': 2}
```
- 邻接表下 DFS/BFS 时间均为 $O(|V|+|E|)$，空间为 $O(|V|)$。
- 不连通图若要覆盖所有顶点，应从每个尚未访问的顶点重新启动遍历。

## 4. 拓扑排序（Topological Sort）
拓扑序只存在于有向无环图（Directed Acyclic Graph, DAG），要求每条边 $u\to v$ 中 $u$ 排在 $v$ 前。
### 4.1 Kahn 算法（Kahn's Algorithm）
1. 计算全部入度。
2. 把入度为 0 的节点入队。
3. 取出节点并删除其出边；新入度为 0 的节点入队。
4. 输出节点数少于顶点总数说明存在有向环。
```python
def topological_sort(graph: Graph) -> list[str]:
    indegree = {node: 0 for node in graph}
    for neighbors in graph.values():
        for neighbor in neighbors:
            indegree.setdefault(neighbor, 0)
            indegree[neighbor] += 1
    queue = deque(node for node, degree in indegree.items() if degree == 0)
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    if len(order) != len(indegree):
        raise ValueError("graph contains a directed cycle")
    return order

print(topological_sort({"study": ["exam"], "sleep": ["exam"], "exam": []}))
# 可能输出之一:
# ['study', 'sleep', 'exam']
```
- 多个入度为 0 的节点会产生多个合法拓扑序；需要字典序最小时可改用最小堆。
- DFS 三色标记也可拓扑排序：未访问、访问中、已完成；遇到“访问中”节点代表回边和环。

## 5. 单源最短路径（Single-source Shortest Paths）
### 5.1 Dijkstra 算法（Dijkstra's Algorithm）
Dijkstra 适用于所有边权非负的图。每次确定当前距离最小的未完成节点，并松弛（Relax）其出边。
```python
from heapq import heappop, heappush
from math import inf

WeightedGraph = dict[str, list[tuple[str, float]]]

def dijkstra(graph: WeightedGraph, start: str) -> tuple[dict[str, float], dict[str, str]]:
    distance = {node: inf for node in graph}
    distance[start] = 0.0
    previous: dict[str, str] = {}
    heap = [(0.0, start)]
    while heap:
        current_distance, node = heappop(heap)
        if current_distance != distance[node]:
            continue  # 跳过已经被更短路径替代的旧堆条目。
        for neighbor, weight in graph.get(node, []):
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights")
            candidate = current_distance + weight
            if candidate < distance.get(neighbor, inf):
                distance[neighbor] = candidate
                previous[neighbor] = node
                heappush(heap, (candidate, neighbor))
    return distance, previous

weighted = {"A": [("B", 2), ("C", 5)], "B": [("C", 1)], "C": []}
print(dijkstra(weighted, "A")[0])  # {'A': 0.0, 'B': 2.0, 'C': 3.0}
```
- 二叉堆邻接表实现为 $O((|V|+|E|)\log |V|)$。
- 负边会破坏“取出的最小距离已经最终确定”的前提。

### 5.2 Bellman–Ford 算法（Bellman–Ford Algorithm）
对全部边重复松弛 $|V|-1$ 轮，适用于负边；再做一轮仍能改进则存在从起点可达的负权环。
- 时间 $O(|V||E|)$，空间 $O(|V|)$。
- 某一轮没有更新可提前结束。
- 负权环使“最短路径”没有有限下界。

### 5.3 Floyd–Warshall 算法（Floyd–Warshall Algorithm）
动态规划计算任意两点最短路径：
$$
d_{ij}^{(k)}=\min\left(d_{ij}^{(k-1)}, d_{ik}^{(k-1)}+d_{kj}^{(k-1)}\right)
$$
- 时间 $O(|V|^3)$，空间 $O(|V|^2)$。
- 可处理负边；若最终 `distance[i][i] < 0`，存在负权环。
- 需要恢复路径时维护下一跳或前驱矩阵。

## 6. 最小生成树（Minimum Spanning Tree, MST）
MST 适用于连通无向加权图，连接所有顶点、无环且总权最小，共有 $|V|-1$ 条边。
### 6.1 Prim 算法（Prim's Algorithm）
从一个顶点开始，每次选择连接已选集合与未选集合的最轻边。最小堆实现适合邻接表。
### 6.2 Kruskal 算法（Kruskal's Algorithm）
按边权从小到大扫描；若边两端属于不同并查集则加入并合并集合。
- 排序主导时间为 $O(|E|\log |E|)$。
- 不连通图得到最小生成森林（Minimum Spanning Forest），不能宣称得到单棵 MST。

> [!tip] 大白话理解（Plain-language Intuition）
> Prim 从一个已建区域向外铺最便宜的路；Kruskal 把全地图道路按价格排序，只要不会形成环就采用。两者目标相同，但观察角度不同。

## 7. 路径恢复与正确性边界（Path Reconstruction and Boundaries）
- 最短距离数组只给长度；要输出路径必须在松弛成功时记录前驱。
- 从终点沿前驱回溯到起点后需要反转。
- 不可达节点距离保持无穷，不能尝试恢复路径。
- 无向边在邻接表中通常要加入两个方向；漏掉反向边会把图错误地变成有向图。
- 权重代表概率或容量时，最短路加法模型未必适用，需要对数变换或最大流等其他算法。

## 8. 常见错误（Common Errors）
- BFS 出队后才标记，导致同一节点重复入队。
- Dijkstra 用于负边。
- 拓扑排序没有检查输出数量，静默返回不完整序列。
- Kruskal 不做并查集判环。
- Floyd–Warshall 原地更新时循环顺序错误；中间点 `k` 必须在最外层。
- 把 MST 当成任意两点最短路径树；MST 优化总边权，不保证每对顶点路径最短。

## 9. 相关笔记（Related Notes）
- [[07-优先队列、堆与并查集（Priority Queues, Heaps, and Disjoint Sets）]]
- [[11-贪心、动态规划与分治（Greedy, Dynamic Programming, and Divide and Conquer）]]
