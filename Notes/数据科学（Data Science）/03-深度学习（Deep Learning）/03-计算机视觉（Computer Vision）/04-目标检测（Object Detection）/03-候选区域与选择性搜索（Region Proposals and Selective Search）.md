---
title: 候选区域与选择性搜索（Region Proposals and Selective Search）
tags:
  - data-science/deep-learning/computer-vision/object-detection/region-proposals
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# 候选区域与选择性搜索（Region Proposals and Selective Search）
## 1. 候选区域问题（Region Proposal Problem）
候选区域（Region Proposal）是在执行昂贵分类前，先提出一组可能包含目标的图像区域。好的候选算法需要兼顾：
- **高召回率（High Recall）**：尽量覆盖所有真实目标。
- **较少候选数（Few Proposals）**：减少后续特征提取与分类计算。
- **类别无关性（Class Independence）**：不局限于训练过的某一类外观。
- **多尺度与多形状（Multi-scale and Multi-shape）**：覆盖大小、比例和轮廓差异。
### 1.1 滑动窗口的代价（Cost of Sliding Windows）
滑动窗口（Sliding Window）在多个位置、尺度和长宽比上裁剪区域并分类。限制窗口集合可用于固定视角的人脸或行人场景，但通用检测会产生海量高度重叠候选。
> [!tip] 大白话理解（Plain-language Intuition）
> 滑动窗口像拿许多大小不同的相框在图片上逐格移动；选择性搜索先看图像本身有哪些相似区域，再重点组合这些区域，少做许多明显无意义的尝试。
## 2. 选择性搜索的核心思想（Selective Search）
选择性搜索（Selective Search）结合了分割（Segmentation）的图像结构信息与穷举搜索追求高覆盖率的目标。算法从细粒度区域开始，反复合并相邻且相似的区域，收集每个层级产生的最小外接框作为候选。
![[03-候选区域与选择性搜索（Region Proposals and Selective Search）-20260623170138007.png]]
### 2.1 基本流程（Core Procedure）
1. **过分割（Over-segmentation）**：原方法使用 Felzenszwalb–Huttenlocher 基于图的分割算法，把图像划分为无重叠小区域，形成集合 $R$。
2. **建立邻接关系（Adjacency）**：只为相邻区域计算相似度，形成候选对集合 $S$。
3. **贪婪合并（Greedy Merge）**：选择相似度最高的相邻区域 $r_i,r_j$，合并为 $r_t=r_i\cup r_j$。
4. **更新相似度（Similarity Update）**：删除与旧区域有关的相似度，计算新区域与相邻区域的相似度。
5. **收集候选框（Proposal Collection）**：保存初始区域与合并区域的最小外接矩形。
6. **终止（Termination）**：没有可合并相邻区域，或合并成覆盖整幅图像的区域。
![[03-候选区域与选择性搜索（Region Proposals and Selective Search）-20260623165745595.png|340]]
> [!tip] 大白话理解（Plain-language Intuition）
> 一开始把图像打碎成很多小拼图；每次找最像、又挨着的两块拼起来。小块可能覆盖物体零件，中块可能覆盖单个物体，大块可能覆盖物体组合，所以整个合并树自然提供多尺度候选。
## 3. 多样性策略（Diversification Strategies）
单一分割与相似度设置容易偏向某种目标外观。选择性搜索运行多组互补配置，再合并候选：
- **颜色空间（Color Spaces）**：可使用 RGB、灰度强度 $I$、Lab、HSV、归一化 rgb、rgI、C 与 H 等表示。
- **初始分割参数（Initial Segmentation Parameters）**：改变尺度或平滑参数，得到不同粒度的初始区域。
- **相似度组合（Similarity Combinations）**：选择颜色、纹理、尺寸和填充相似度的不同子集。
- **快模式与质量模式（Fast and Quality Modes）**：少量策略降低耗时，更多策略提高覆盖率但增加候选与计算。
> [!warning] 数量不是固定 API 契约（Counts Are Not a Universal Contract）
> 原论文研究了多种颜色空间和策略组合；具体库的 `fast`、`quality` 等预设不一定完整复现论文全部配置。使用时应以实现文档和参数为准。
## 4. 四类相似度（Four Similarity Terms）
综合相似度可写为：
$$
s(r_i,r_j)=a_1s_{color}+a_2s_{texture}+a_3s_{size}+a_4s_{fill},\quad a_k\in\{0,1\}
$$
不同策略启用不同相似度项。
### 4.1 颜色相似度（Color Similarity）
为区域构建 $L_1$ 归一化颜色直方图 $C_i$，用直方图交集衡量。来源示例对三个颜色通道各使用 25 个 bin，拼接为 75 维向量；通道数与 bin 数属于实现设置：
$$
s_{color}(r_i,r_j)=\sum_k\min(C_i^k,C_j^k)
$$
合并后的直方图按区域大小加权更新：
$$
C_t=\frac{|r_i|C_i+|r_j|C_j}{|r_i|+|r_j|}
$$
![[03-候选区域与选择性搜索（Region Proposals and Selective Search）-20260623171151554.png]]
### 4.2 纹理相似度（Texture Similarity）
原稿使用每个颜色通道的多个高斯微分方向建立纹理直方图，并通过直方图交集比较。以 3 个通道、8 个方向、每个方向 10 个 bin 为例，可组成 $3\times8\times10=240$ 维描述子；具体维度取决于实现。
![[03-候选区域与选择性搜索（Region Proposals and Selective Search）-20260623171216046.png]]
### 4.3 尺寸相似度（Size Similarity）
$$
s_{size}(r_i,r_j)=1-\frac{|r_i|+|r_j|}{|I|}
$$
其中 $|I|$ 是整幅图像面积。该项优先推动较小区域合并，避免大区域过早吞并全部邻域。
### 4.4 填充相似度（Fill Similarity）
令 $B_{ij}$ 为包住 $r_i$ 与 $r_j$ 的最小外接框：
$$
s_{fill}(r_i,r_j)=1-\frac{|B_{ij}|-|r_i|-|r_j|}{|I|}
$$
两区域若能紧密填充外接框，则空隙小、相似度高；距离远或组合形状松散时相似度低。
![[03-候选区域与选择性搜索（Region Proposals and Selective Search）-20260623171315899.png|511]]
![[03-候选区域与选择性搜索（Region Proposals and Selective Search）-20260623171403280.png]]
## 5. 候选排序与去重（Ranking and Deduplication）
- 合并层级、区域大小与策略来源可用于候选排序。
- 多组策略可能产生相同或近似框，必须去重并限制候选数量。
- 来源排序说明让较早生成的区域获得较高优先级，并可累加同一区域在不同策略中重复出现的权重；具体论文实现还用随机数打破相同优先级。需要复现结果时应固定随机种子并记录库版本。
- 选择性搜索本身生成类别无关候选，不直接完成目标分类；早期 R-CNN 再为候选区域提取 CNN 特征，并用类别分类器与边界框回归器处理。
## 6. 局限与演化（Limitations and Evolution）
- 依赖 CPU 图像分割和贪婪区域合并，难以与检测网络共同端到端训练。
- 对颜色和纹理相似性敏感；低对比度、复杂纹理或极小目标可能产生差候选。
- 候选数仍可能达到数千，后续逐区域处理成本高。
- Faster R-CNN 使用与检测器共享卷积特征的区域生成网络（Region Proposal Network, RPN）代替外部选择性搜索，使候选学习纳入网络训练。
## 参考资料（References）
- [Selective Search for Object Recognition](https://doi.org/10.1007/s11263-013-0620-5)
- [Faster R-CNN](https://arxiv.org/abs/1506.01497)
