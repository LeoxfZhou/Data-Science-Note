---
title: 批归一化与常见归一化方法（Batch Normalization and Common Normalization Methods）
tags:
  - data-science/deep-learning/normalization
  - pytorch/nn
status: published
created: 2026-08-12
published_at: 2026-08-12
---
# 批归一化与常见归一化方法（Batch Normalization and Common Normalization Methods）
## 1. 批归一化（Batch Normalization, BN）解决什么问题
批归一化在训练阶段使用小批次（Mini-batch）的统计量标准化中间激活，并通过可学习仿射参数恢复表示自由度。它常用于卷积网络中改善数值尺度、优化条件与训练稳定性。
**原论文动机（Original Motivation）**：Batch Normalization 论文把减少内部协变量偏移（Internal Covariate Shift, ICS）作为核心动机，即前层参数变化会改变后层输入分布，使后层持续适应移动的目标。
**后续演化/现代理解（Later Development / Modern Understanding）**：后续研究表明，BN 的效果不能只由降低 ICS 解释；更常见的现代解释还包括让优化景观更平滑、改善梯度与参数尺度的条件，以及小批次统计噪声带来的正则化效应。
> [!tip] 大白话理解（Plain-language Intuition）
> 网络每更新一次，后面层收到的数值尺度都可能改变。BN 像在层与层之间放一个自动调音台：训练时根据这一批数据把音量拉回可控范围，再让可学习的旋钮决定最终该多大声。它帮助优化，但不是对所有训练问题的万能保险。
## 2. 数学定义（Mathematical Definition）
对一个归一化集合 $mathcal{B}=\{x_1,\ldots,x_m\}$：
### 2.1 批次均值（Batch Mean）
$$
\mu_{\mathcal{B}}=\frac{1}{m}\sum_{i=1}^{m}x_i
$$
### 2.2 批次方差（Batch Variance）
$$
\sigma_{\mathcal{B}}^2=\frac{1}{m}\sum_{i=1}^{m}(x_i-\mu_{\mathcal{B}})^2
$$
### 2.3 标准化（Normalization）
$$
\hat{x}_i=\frac{x_i-\mu_{\mathcal{B}}}{\sqrt{\sigma_{\mathcal{B}}^2+\epsilon}}
$$
### 2.4 仿射变换（Affine Transformation）
$$
y_i=\gamma\hat{x}_i+\beta
$$
- $epsilon$：数值稳定常数，防止方差接近零时除零或极端放大。
- $gamma$：可学习缩放参数（Scale）。
- $eta$：可学习平移参数（Shift）。
> [!tip] 大白话理解（Plain-language Intuition）
> 前三步先把一组数变成“中心接近 0、尺度接近 1”；最后一步再把它搬到模型真正需要的位置和尺度。没有最后的 $gamma$、$eta$，标准化会不必要地限制这一层能表达的分布。
> [!note] 可逆表达能力（Representational Recovery）
> 对给定统计量，合适的 $gamma$ 与 $eta$ 可以恢复原尺度，但实际实现的分母是 $\sqrt{\sigma^2+\epsilon}$。因此若要精确抵消标准化，应取 $\gamma=\sqrt{\sigma^2+\epsilon}$、$\beta=\mu$；把 $gamma$ 写成单纯的标准差会忽略 $epsilon$。
## 3. `BatchNorm2d` 的归一化轴（Normalization Axes）
输入形状为 `[N, C, H, W]` 时，`BatchNorm2d(C)` 对每个通道独立计算统计量，并在训练阶段跨 `N`、`H`、`W` 聚合：
- 每个通道有一对可学习参数 $gamma_c$、$eta_c$。
- 统计量不在不同通道间混合。
- 由于统计覆盖批次和空间维度，也常称为空间批归一化（Spatial Batch Normalization）。
> [!tip] 大白话理解（Plain-language Intuition）
> 一批图片的同一个特征通道共用一把标尺，例如“竖边通道”自己统计，不和“红色通道”混在一起。标尺会看这一批所有图片和所有空间位置。
## 4. 训练阶段与推理阶段（Training vs. Inference）
### 4.1 训练阶段（Training Mode）
- 使用当前批次统计量完成标准化。
- 默认维护 `running_mean` 与 `running_var`，供推理阶段使用。
- PyTorch 前向标准化使用有偏方差估计（Biased Estimator，相当于 `correction=0`），但写入运行方差时使用无偏估计（Unbiased Estimator，相当于 `correction=1`）。
- 默认运行统计更新形式为：
$$
x_{new}=(1-\text{momentum})x_{old}+\text{momentum}\,x_{batch}
$$
这里的 `momentum` 与优化器动量含义不同。
### 4.2 推理阶段（Evaluation Mode）
- 调用 `model.eval()` 后，默认使用训练期间维护的运行均值与运行方差。
- `eval()` 不会关闭自动微分；推理通常还应配合 `torch.inference_mode()` 或 `torch.no_grad()`。
- 如果 `track_running_stats=False`，训练和评估都使用当前输入的批次统计量；输出会继续依赖批次组成。
> [!tip] 大白话理解（Plain-language Intuition）
> 训练时可以参考“一群人”的平均身高来做标准化；上线时往往一次只有一个人，不能拿单人统计量代表人群，所以改用训练期间积累的长期统计。忘记 `model.eval()` 就相当于上线后还临时改标尺。
## 5. 数值与优化机制（Numerical and Optimization Mechanisms）
### 5.1 $epsilon$ 的数值稳定作用
批次内某通道若几乎常数，方差可能接近零。$epsilon$ 放在平方根内部，使分母保持正值并限制放大倍数；它不能修复输入中的 `NaN` 或 `Inf`。
### 5.2 参数尺度与梯度
忽略偏置、$epsilon$、有限批次估计与符号等边界时，对卷积或线性权重整体乘正比例因子，BN 后的标准化激活可能近似不变。这种尺度不敏感性改变了参数空间与梯度条件，但不表示梯度级数完全不受权重影响。
### 5.3 损失景观平滑（Loss-landscape Smoothing）
经验与理论研究表明，BN 往往使目标函数及其梯度对参数变化更平滑，从而允许更稳定的优化步长。实际可用学习率仍受架构、优化器、批次大小、数据、精度与初始化影响。
> [!tip] 大白话理解（Plain-language Intuition）
> BN 往往把原本忽大忽小、像悬崖一样的更新地形变得更缓一些，让优化器不容易一步踩空。但它不是护栏：学习率开得过大、输入异常或模型设计有问题时仍会发散。
## 6. BN 的优势、限制与常见误区
### 6.1 常见收益
- 改善中间激活的尺度与训练稳定性。
- 常允许使用比无归一化模型更大的学习率，但需要实验验证。
- 降低对某些初始化尺度的敏感性，但不能替代正确初始化。
- 小批次统计引入噪声，可能产生正则化效果。
### 6.2 限制
- **小批次敏感（Small-batch Sensitivity）**：批次很小或样本高度相关时，统计量噪声大；不存在对所有任务都成立的“至少 16”硬阈值。
- **分布迁移（Distribution Shift）**：训练运行统计与推理数据分布不匹配时，性能可能下降。
- **多设备训练（Distributed Training）**：普通 BN 只看单设备局部批次；需要跨设备统计时可考虑同步批归一化（Synchronized Batch Normalization）。
- **可变长度序列（Variable-length Sequence）**：填充、时间轴和批次统计使直接使用 BN 更复杂；RNN 与 Transformer 常采用 LayerNorm。
- **额外状态（State）**：运行统计不是可学习梯度参数，但属于模型状态，保存和加载检查点时必须保留。
### 6.3 不能据此推出的结论
- BN 不能保证彻底消除梯度消失或梯度爆炸。
- BN 不能保证任意高学习率都不发散。
- BN 的正则化效应不能在所有模型中完全替代 Dropout 或权重衰减。
- 在某些卷积块中使用 `Conv → BN → Activation` 是常见结构，但具体顺序取决于架构设计，例如预激活残差网络使用不同顺序。
## 7. PyTorch `nn.BatchNorm2d`
### 7.1 主要参数
```python
torch.nn.BatchNorm2d(
    num_features,
    eps=1e-5,
    momentum=0.1,
    affine=True,
    track_running_stats=True,
    device=None,
    dtype=None,
)
```
- **`num_features`**：输入通道数 `C`。
- **`eps`**：分母中的数值稳定项。
- **`momentum`**：运行统计更新权重，不是优化器动量。
- **`affine=True`**：学习 $gamma$ 与 $eta$。
- **`track_running_stats=True`**：维护推理所用运行统计。
### 7.2 训练和推理行为示例
```python
import torch
from torch import nn

normalizer = nn.BatchNorm2d(3)
inputs = torch.arange(2 * 3 * 2 * 2, dtype=torch.float32).reshape(2, 3, 2, 2)

normalizer.train()
training_output = normalizer(inputs)
print(training_output.shape)  # 输出: torch.Size([2, 3, 2, 2])
print(normalizer.running_mean.shape)  # 输出: torch.Size([3])

normalizer.eval()
with torch.inference_mode():
    inference_output = normalizer(inputs[:1])
print(inference_output.shape)  # 输出: torch.Size([1, 3, 2, 2])
```
### 7.3 卷积块中的偏置
卷积后立即接 `BatchNorm2d(affine=True)` 时，卷积偏置通常可以设为 `False`，因为 BN 的中心化会消除固定偏置，且 $eta$ 已提供可学习平移：
```python
block = nn.Sequential(
    nn.Conv2d(3, 32, kernel_size=3, padding=1, bias=False),
    nn.BatchNorm2d(32),
    nn.ReLU(),
)
```
这是一种常见简化，不适用于所有非标准结构或关闭仿射参数的配置。
## 8. 常见归一化方法对比（Normalization Methods Comparison）

|方法（Method）|典型统计范围（以 `NCHW` 为例）|依赖批次大小|常见场景|
|---|---|---|---|
|批归一化（BatchNorm）|每个通道跨 `N,H,W`|是|常规 CNN、大中型批次|
|层归一化（LayerNorm）|每个样本的指定末尾维度|否|Transformer、RNN、通用序列模型|
|实例归一化（InstanceNorm）|每个样本、每个通道跨 `H,W`|否|风格迁移、生成模型|
|组归一化（GroupNorm）|每个样本、每组通道跨组内 `C,H,W`|否|检测、分割、小批次 CNN|
|可切换归一化（Switchable Normalization）|学习组合 BN、IN、LN 等统计|实现相关|希望由模型学习统计组合的研究或特定架构|

### 8.1 层归一化（Layer Normalization, LN）
对每个样本内部的指定特征维度求统计量，不依赖其他样本。它适合批次大小变化大或序列长度场景，但在 CNN 上是否优于 BN 取决于架构与任务。
### 8.2 实例归一化（Instance Normalization, IN）
对每个样本的每个通道跨空间位置归一化，削弱单张图像的全局对比度与风格统计，因此常用于图像风格化。
### 8.3 组归一化（Group Normalization, GN）
把通道分成 `G` 组，每组在单个样本内跨 `(C/G) × H × W` 求统计量。它不依赖批次大小，常用于显存限制导致小批次的检测与分割任务；通道数必须能被组数整除。
### 8.4 可切换归一化（Switchable Normalization, SN）
通过可学习权重组合不同归一化统计。概念形式可写为：
$$
\hat{h}=\gamma\frac{h-\sum_k w_k\mu_k}{\sqrt{\sum_k w'_k\sigma_k^2+\epsilon}}+\beta
$$
其训练成本、实现细节与收益依赖论文和代码版本，不能简单视为所有任务都优于固定归一化方法。
> [!tip] 大白话理解（Plain-language Intuition）
> 这些方法最大的区别是“拿谁来一起算平均值”：BN 找同批同通道的伙伴，LN 看自己整层特征，IN 看自己单个通道，GN 把自己的通道分组。批次小的时候，少依赖别的样本通常更稳定。
## 9. 排错清单（Troubleshooting Checklist）
- 验证准确率异常：检查是否调用 `model.eval()`，以及推理是否使用正确运行统计。
- 微调后性能下降：检查是否冻结了参数却仍让 BN 运行统计更新，或反之。
- 小批次训练震荡：比较 GroupNorm、LayerNorm、冻结 BN、同步 BN 或梯度累积；梯度累积不会自动扩大单次 BN 统计批次。
- 加载检查点缺少键：确认 `running_mean`、`running_var`、`num_batches_tracked` 与 `affine` 设置一致。
- 出现 `NaN`：检查输入、学习率、混合精度、极端方差与 `eps`；不能只调大 `eps` 而忽略上游异常。
## 10. 关联笔记与参考资料（Related Notes and References）
- [[神经网络参数初始化与梯度流（Neural Network Initialization and Gradient Flow）]]
- [[模型欠拟合、过拟合与泛化（Model Underfitting, Overfitting, and Generalization）]]
- [PyTorch `BatchNorm2d` 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html)
- [Batch Normalization 原论文](https://arxiv.org/abs/1502.03167)
- [How Does Batch Normalization Help Optimization?](https://proceedings.neurips.cc/paper/2018/hash/905056c1ac1dad141560467e0a99e1cf-Abstract.html)
