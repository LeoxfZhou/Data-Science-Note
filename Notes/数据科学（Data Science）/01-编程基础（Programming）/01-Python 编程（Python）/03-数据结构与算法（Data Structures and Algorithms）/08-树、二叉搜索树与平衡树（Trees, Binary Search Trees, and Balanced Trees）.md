---
title: 树、二叉搜索树与平衡树（Trees, Binary Search Trees, and Balanced Trees）
status: published
detail_level: comprehensive
published_at: 2026-08-17
updated_at: 2026-08-17
---
# 树、二叉搜索树与平衡树（Trees, Binary Search Trees, and Balanced Trees）
## 1. 树的基本术语（Tree Terminology）
树（Tree）由节点和边组成，具有唯一根节点（Root），除根外每个节点恰有一个父节点（Parent）。
- **子节点（Child）**、**兄弟节点（Sibling）**、**祖先（Ancestor）**、**后代（Descendant）**描述相对关系。
- **叶节点（Leaf）**没有子节点；**内部节点（Internal Node）**至少有一个子节点。
- 节点的度（Degree）是子节点数；树的度是所有节点度的最大值。
- 深度（Depth）通常是根到节点的边数；高度（Height）通常是节点到最深叶的边数。必须明确空树和单节点树采用的约定。
- 子树（Subtree）由某节点及其全部后代构成；森林（Forest）是若干互不相交的树。

> [!tip] 大白话理解（Plain-language Intuition）
> 树像组织结构图：每个人只有一个直接上级，但可以有多个下属。深度是“从老板向下数到我”，高度是“从我向下最多还能数几层”。

## 2. 二叉树（Binary Tree）
二叉树每个节点最多有左、右两个孩子，二者有顺序，不能随意互换。
- 第 $i$ 层最多有 $2^i$ 个节点（根为第 0 层）。
- 高度为 $h$ 的满二叉树（Full/Perfect Binary Tree）有 $2^{h+1}-1$ 个节点。
- 完全二叉树（Complete Binary Tree）除最后一层外均填满，最后一层从左到右连续；适合数组存储。
- 满二叉树、完全二叉树和“每个节点要么 0 个要么 2 个孩子”的严格二叉树在不同教材中术语可能不同，应以结构定义为准。

### 2.1 存储方式（Storage Representations）
- **链接存储（Linked Representation）**：节点保存 `left`、`right`，适合形状不规则的树。
- **数组存储（Array Representation）**：完全二叉树按层序紧凑存放，索引关系与堆相同。
- 稀疏树使用数组会浪费大量空槽，通常使用链接存储。

## 3. 树遍历（Tree Traversal）
- 前序遍历（Preorder）：根 → 左 → 右，适合复制、序列化和前缀表达式。
- 中序遍历（Inorder）：左 → 根 → 右；二叉搜索树中得到非递减序列。
- 后序遍历（Postorder）：左 → 右 → 根，适合释放子树、计算目录大小和后缀表达式。
- 层序遍历（Level-order）：按深度从浅到深，使用队列，是广度优先搜索（BFS）。
```python
from __future__ import annotations

from collections import deque
from dataclasses import dataclass

@dataclass
class TreeNode:
    value: int
    left: TreeNode | None = None
    right: TreeNode | None = None

def preorder(root: TreeNode | None) -> list[int]:
    if root is None:
        return []
    result: list[int] = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.value)
        # 栈后进先出，所以先压右子树，确保左子树先访问。
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return result

def level_order(root: TreeNode | None) -> list[list[int]]:
    if root is None:
        return []
    queue = deque([root])
    levels: list[list[int]] = []
    while queue:
        level: list[int] = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.value)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        levels.append(level)
    return levels

root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
print(preorder(root))  # [1, 2, 4, 5, 3]
print(level_order(root))  # [[1], [2, 3], [4, 5]]
```

### 3.1 递归与迭代边界（Recursive and Iterative Boundaries）
- 递归实现与定义一致，但调用栈空间为 $O(h)$；退化树高度 $h=n$ 时可能触发 `RecursionError`。
- 前序和中序用显式栈容易迭代化；后序需要记录“是否已展开”或使用双栈。
- 层序遍历必须按当前队列长度分层，不能在同一轮把新入队节点也算进当前层。

## 4. 二叉搜索树（Binary Search Tree, BST）
BST 对每个节点维持顺序不变量：左子树键小于当前键，右子树键大于当前键；重复键策略必须由实现明确规定。
- 查询、插入和删除平均为 $O(\log n)$，最坏退化为 $O(n)$。
- 最小值沿左链接到底，最大值沿右链接到底。
- 前驱（Predecessor）是更小键中的最大者；后继（Successor）是更大键中的最小者。
- 范围查询可利用顺序不变量剪枝，不必访问无关子树。

### 4.1 删除节点（Deletion）
1. 无孩子：父节点链接改为 `None`。
2. 一个孩子：父节点越过目标，直接连接该孩子。
3. 两个孩子：用中序后继（右子树最小节点）或前驱替换目标键，再删除替代节点。

> [!tip] 大白话理解（Plain-language Intuition）
> 删除有两个孩子的节点不能简单拔掉，否则会把两棵子树断开。先找排序中紧挨着它的后继来“顶班”，再删除后继原位置；后继最多只有一个右孩子，第二次删除就简单了。

```python
class BinarySearchTree:
    def __init__(self) -> None:
        self.root: TreeNode | None = None

    def insert(self, value: int) -> None:
        if self.root is None:
            self.root = TreeNode(value)
            return
        current = self.root
        while True:
            if value == current.value:
                return  # 本实现采用集合语义，忽略重复键。
            if value < current.value:
                if current.left is None:
                    current.left = TreeNode(value)
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = TreeNode(value)
                    return
                current = current.right

    def contains(self, value: int) -> bool:
        current = self.root
        while current is not None:
            if value == current.value:
                return True
            current = current.left if value < current.value else current.right
        return False

bst = BinarySearchTree()
for number in [4, 2, 6, 1, 3, 5, 7]:
    bst.insert(number)
print(bst.contains(5), bst.contains(8))  # True False
```

## 5. AVL 树（AVL Tree）
AVL 树是高度平衡 BST，任一节点左右子树高度差的绝对值不超过 1。
- 平衡因子（Balance Factor）常定义为 `left_height - right_height`。
- 插入或删除后沿祖先路径更新高度，并在首次或所有失衡点旋转。
- LL 情况右旋，RR 情况左旋，LR 先左旋子节点再右旋，RL 先右旋子节点再左旋。
- 查询、插入和删除最坏均为 $O(\log n)$；严格平衡带来较快查询，但更新旋转较频繁。

## 6. 红黑树（Red-black Tree）
红黑树通过颜色约束提供较宽松平衡：
1. 节点为红或黑。
2. 根通常视为黑色。
3. 空叶（NIL）为黑色。
4. 红节点不能有红孩子。
5. 从任一节点到其后代 NIL 的路径具有相同黑节点数。
- 高度不超过约 $2\log_2(n+1)$，操作最坏为 $O(\log n)$。
- 插入修复围绕父节点、叔叔节点和祖父节点执行重新着色与旋转。
- 删除黑节点可能造成“黑高不足”，修复比插入复杂。
- 标准库映射/集合可能使用红黑树，但 Python `dict`、`set` 是哈希表，不是红黑树。

> [!tip] 大白话理解（Plain-language Intuition）
> AVL 像要求两边书架高度几乎一样，查找很稳但每次增删更爱调整；红黑树允许稍微歪一些，用较少调整换取仍然有上界的高度。

## 7. B 树与多路搜索树（B-tree and Multiway Search Trees）
B 树节点可保存多个有序键和多个孩子，用较高分支因子降低树高，适合磁盘、数据库索引和文件系统。
- 一个含 $k$ 个键的内部节点通常有 $k+1$ 个孩子。
- 除根外节点必须满足最小占用率；所有叶位于同一深度。
- 插入时满节点分裂并把中间键提升到父节点。
- 删除时若节点低于最小键数，需要向兄弟借键或与兄弟合并，并可能向上递归修复。
- B+ 树把记录或记录指针集中在叶节点，叶节点通常链成有序链，适合范围扫描。
- B 树不是二叉树；“B-树”中的短横线通常不是“减号”。

## 8. 树算法常见题型（Common Tree Problems）
- 对称树：成对比较左树的左与右树的右、左树的右与右树的左。
- 最大/最小深度：递归或 BFS；最小深度遇到首个叶节点即可返回。
- 翻转树：交换每个节点的左右子树。
- 根据前序+中序或中序+后序重建：根划分中序区间；键必须能唯一定位或明确重复处理。
- 最近公共祖先（Lowest Common Ancestor）：BST 可利用键范围，普通二叉树需从左右子树汇总。
- 表达式树：后序遍历求值，前序/中序/后序分别对应前缀、中缀和后缀表达式。

## 9. 常见错误（Common Errors）
- 混淆节点高度、节点深度和树层数的起始约定。
- 把普通二叉树误认为 BST，错误使用中序有序性质。
- BST 重复键策略不一致，导致查询、删除或排名结果不确定。
- 删除两孩子节点时只复制后继键，却忘记删除后继原节点。
- 旋转后没有更新父链接、根链接或节点高度。
- 递归遍历退化树时忽略调用栈上限。

## 10. 相关笔记（Related Notes）
- [[07-优先队列、堆与并查集（Priority Queues, Heaps, and Disjoint Sets）]]
- [[09-哈希表与排序算法（Hash Tables and Sorting Algorithms）]]
- [[10-图结构、遍历与最短路径（Graphs, Traversal, and Shortest Paths）]]
