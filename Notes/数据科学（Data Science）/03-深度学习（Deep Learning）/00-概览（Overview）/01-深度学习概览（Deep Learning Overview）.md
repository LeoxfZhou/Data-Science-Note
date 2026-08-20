---
title: 深度学习概览（Deep Learning Overview）
status: published
published_at: 2026-08-11
---

# 深度学习概览（Deep Learning Overview）
## 1. 定义与核心思想（Definition and Core Idea）
- 深度学习（Deep Learning, DL）是机器学习（Machine Learning, ML）的分支，通常以多层人工神经网络（Artificial Neural Network）为模型架构，从数据中学习分层表示（Hierarchical Representation）。
- “深度”主要指网络包含多个可学习的表示层，而不只是代码量大或训练时间长。
- 低层通常学习边缘、颜色、局部纹理或词形等简单模式，高层把低层模式组合为物体、语义或任务相关表示。
- 与依赖人工设计特征的传统流程相比，深度学习可以从原始或接近原始的数据中自动学习特征；但数据定义、标签设计、目标函数、采样和错误分析仍需要人工完成。
- 深度学习擅长图像、语音、文本等高维数据，但是否优于传统机器学习取决于数据量、任务结构、算力、延迟、可解释性和维护成本。

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/00-概览（Overview）/01-深度学习概览（Deep Learning Overview）/01-深度学习概览（Deep Learning Overview）-20260328152649138.png]]

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/00-概览（Overview）/01-深度学习概览（Deep Learning Overview）/01-深度学习概览（Deep Learning Overview）-20260328152649570.png]]

## 2. 深度学习的主要特点（Key Characteristics）
1. **多层非线性变换（Multi-layer Nonlinear Transformation）**：每层通过线性运算与非线性激活函数（Activation Function）组合，使网络能够表示复杂关系。
2. **自动特征提取（Automatic Feature Extraction）**：模型可以联合学习特征表示与任务输出，减少完全手工特征工程，但不会自动保证学到的特征合理、公平或可泛化。
3. **依赖数据与计算资源（Data and Compute Requirements）**：大型模型通常需要大量数据和 GPU 等加速硬件；迁移学习（Transfer Learning）、预训练（Pretraining）和轻量模型可以降低从零训练成本。
4. **可解释性挑战（Interpretability Challenge）**：深层模型内部表示复杂，常被称为黑箱（Black Box）。特征可视化、归因方法和消融实验可以辅助解释，但不能自动证明因果关系。
5. **端到端学习（End-to-end Learning）**：输入到输出的多个阶段可在同一目标下联合优化，不过端到端结构也会增加定位错误来源和验证中间行为的难度。

## 3. 机器学习与深度学习的区别（Machine Learning vs. Deep Learning）

|维度|传统机器学习（Traditional Machine Learning）|深度学习（Deep Learning）|
|---|---|---|
|特征工程（Feature Engineering）|通常更依赖人工设计和领域经验|可从数据中自动学习分层特征，但仍需人工定义数据与目标|
|数据规模|中小数据上常具有优势|通常随高质量数据增加而显著受益|
|计算成本|常可在 CPU 上高效训练|大型模型往往依赖 GPU 或其他加速器|
|可解释性|线性模型、浅树等通常更容易解释|内部表示复杂，解释难度通常更高|
|典型数据|表格数据（Tabular Data）|图像、音频、文本和多模态数据（Multimodal Data）|
|部署成本|通常较低|可能面临模型体积、延迟、显存和能耗约束|

## 4. 常见模型（Common Models）
### 4.1 卷积神经网络（Convolutional Neural Network, CNN）
- 使用卷积层（Convolutional Layer）提取局部空间特征，并通过权重共享减少参数量。
- 池化层（Pooling Layer）可降低空间分辨率和计算量，但现代架构也可能使用步幅卷积等替代方案。
- 常用于图像分类（Image Classification）、目标检测（Object Detection）和图像分割（Image Segmentation）。

### 4.2 循环神经网络（Recurrent Neural Network, RNN）
- 面向序列数据（Sequential Data），当前状态可以依赖先前输入，因此适合表达时间或顺序依赖。
- 常用于文本、语音和时间序列。标准 RNN 容易遇到长期依赖和梯度消失问题，长短期记忆网络（Long Short-Term Memory, LSTM）和门控循环单元（Gated Recurrent Unit, GRU）通过门控结构进行缓解。

### 4.3 自编码器（Autoencoder）
- 由编码器（Encoder）和解码器（Decoder）组成：编码器将输入压缩为潜在表示（Latent Representation），解码器尝试重建原始输入。
- 常用于降维、表示学习、去噪和异常检测；如果模型容量过大且缺少约束，简单复制输入不一定产生有意义表示。

### 4.4 生成对抗网络（Generative Adversarial Network, GAN）
- 生成器（Generator）创建候选样本，判别器（Discriminator）区分真实样本与生成样本，二者通过对抗目标共同训练。
- 可用于图像生成、视频合成和数据增强，但训练可能出现不稳定或模式崩溃（Mode Collapse）。

### 4.5 Transformer
- Transformer 使用自注意力机制（Self-attention）建立序列中不同位置之间的关系，不依赖传统循环结构逐步传递状态，因此训练阶段具有更好的并行性。
- 已广泛用于机器翻译、文本生成、摘要、视觉和多模态任务；其注意力计算在长序列下可能带来显著内存与计算开销。
### 4.6 多层感知器（Multi-layer Perceptron, MLP）
- 多层感知器由全连接层（Fully Connected Layer）和激活函数（Activation Function）堆叠而成，每个输出单元通常连接上一层的全部输入特征。
- 适合已经整理为固定长度向量的数据，例如表格特征、传感器统计量、Embedding 后的分类头，以及其他网络最后的预测头（Prediction Head）。
- MLP 不显式利用图像的空间邻域、序列顺序或图结构；对这些数据直接展平会丢失有价值的归纳偏置（Inductive Bias）。
### 4.7 图神经网络（Graph Neural Network, GNN）
- 图神经网络通过消息传递（Message Passing）聚合邻居节点信息，使节点表示同时包含自身属性与局部关系。
- 常用于社交关系、推荐系统、分子性质、知识图谱、交通网络和欺诈团伙检测。
- 图结构错误、邻居采样偏差、过度平滑（Over-smoothing）和大图内存成本是常见边界；普通 MLP 无法自然表达“谁与谁相连”。
### 4.8 扩散模型（Diffusion Model）
- 扩散模型在训练时学习从加噪样本恢复干净数据的去噪过程；生成时从随机噪声出发，经过多步反向去噪得到样本。
- 常用于图像、视频、音频和三维内容生成，也可通过文本、边缘、深度、姿态或参考图进行条件控制（Conditional Control）。
- 生成质量较高但多步采样通常较慢；训练目标、噪声调度（Noise Schedule）、采样器和潜空间编码器会共同影响结果。
### 4.9 网络选型速查（Network Selection Guide）

|数据结构或任务（Data or Task）|优先考虑的网络（Candidate Network）|为什么适合（Why It Fits）|常见限制（Common Limitation）|
|---|---|---|---|
|固定长度表格或特征向量|MLP、Tabular Transformer|直接学习特征间非线性组合|深度模型不一定胜过梯度提升树；需严格验证|
|图像分类与视觉骨干|CNN、ResNet、Vision Transformer (ViT)|CNN 强调局部和平移结构；ViT 建模全局 Patch 关系|数据量、分辨率与算力需求差异大|
|目标检测|YOLO、Faster R-CNN、DETR|同时预测类别和位置|小目标、密集遮挡和实时延迟需单独评估|
|像素级分割|U-Net、DeepLab、Mask R-CNN、SegFormer|融合局部细节与多尺度语义|像素标注昂贵，类别不平衡明显|
|时间序列或短序列|RNN、LSTM、GRU、Temporal CNN|显式处理顺序或局部时间模式|长依赖与并行效率可能受限|
|文本、长序列与多模态|Transformer 及其变体|自注意力建立跨位置关系，易于预训练迁移|长序列注意力成本高|
|图关系数据|GCN、GraphSAGE、GAT|聚合邻居与关系结构|大图采样、动态图和过度平滑复杂|
|重建、压缩与异常检测|Autoencoder、Variational Autoencoder (VAE)|以重建误差或潜变量约束学习表示|高容量模型可能只学会复制输入|
|高保真内容生成|Diffusion Model、GAN|扩散训练通常稳定；GAN 推理快且结果锐利|扩散采样慢；GAN 容易模式崩溃|

## 5. 典型应用场景与模型选型（Applications and Model Selection）
### 5.1 图像分类（Image Classification）
- **任务定义**：回答“图中主要是什么类别”，通常不要求给出目标坐标。
- **典型应用**：猫狗或花卉品种分类、社交媒体照片自动标注、医疗影像病变分类、屏幕划痕与工业良品/次品判断。图像分类只预测整张图的类别；物体检测（Object Detection）还必须预测目标的位置与数量。
- **ResNet / DenseNet**：适合需要较强特征表达的图像分类和迁移学习任务。残差连接（Residual Connection）改善深层网络优化与梯度传播；DenseNet 强调跨层特征复用。它们可用于医疗影像诊断和工业质检，但效果依赖数据和验证设计，不能只由架构名称保证。
- **MobileNet / ShuffleNet**：通过深度可分离卷积（Depthwise Separable Convolution）、分组卷积（Grouped Convolution）或通道重排（Channel Shuffle）降低计算量，适合移动端或边缘设备（Edge Device），例如手机应用的活体检测和小区门禁人脸识别打卡。

### 5.2 目标检测（Object Detection）
- **任务定义**：同时预测对象类别与边界框（Bounding Box），回答“是什么”和“在哪里”。
- **YOLO 系列**：一阶段检测器（One-stage Detector），通常重视实时速度和端到端部署，常用于自动驾驶感知、安防和无人机。不同版本、输入尺寸和硬件的速度与精度差异很大，不能把任一版本视为所有工业任务的绝对最优。
- **应用示例**：自动驾驶中的行人和车辆避障、安防摄像头的违规入侵报警、无人机抓拍、卫星遥感图像分析，以及对漏检率要求较高的疾病筛查。
- **Faster R-CNN**：两阶段检测器（Two-stage Detector），先生成候选区域再分类与回归，常用于更重视精度且可接受较高延迟的场景。小目标检测能力受输入分辨率、特征金字塔、标注质量和训练策略影响，模型架构本身不能保证不漏检。

### 5.3 图像分割（Image Segmentation）
- **任务定义**：为像素预测类别或实例归属，输出比边界框更精细的轮廓。
- **U-Net**：编码器—解码器 U 形结构使用跳跃连接（Skip Connection）融合不同尺度特征，广泛用于细胞或器官轮廓提取、医疗影像和工业精细缺陷分割。在迁移学习、数据增强、目标形态较稳定且标注质量高等条件下，数百张图像可能训练出可用模型，但样本数量本身不保证效果。
- **Mask R-CNN / YOLOv8-Seg 等分割模型**：实例分割（Instance Segmentation）可区分同类别的不同实例，例如为一堆相互重叠的苹果分别描边、指导机械臂抓取，或在自动驾驶中精确区分道路与人行道像素。

### 5.4 人脸识别与图像生成（Face Recognition and Image Generation）
- **人脸识别（Face Recognition）**：根据面部特征完成身份验证或身份分类，可用于手机解锁和安防监控。实际系统还需要处理活体检测、光照、姿态、遮挡、隐私和误识别风险。
- **图像生成（Image Generation）**：根据文本、图像或其他条件生成新图像，可用于艺术风格迁移、图像超分辨率（Image Super-resolution）和老旧照片修复。

### 5.5 生成式人工智能与可控生成（Generative AI and Controlled Generation）
- **Stable Diffusion**：具有成熟开源生态的潜在扩散模型（Latent Diffusion Model），可用于文生图、图生图、风格转换、电商内容和视觉设计。模型能力与许可因具体版本而异，不宜写成永久性的“最强”。
- **应用示例**：游戏公司原画生成、电商模特自动换衣、广告海报生成、视频合成和其他人工智能生成内容（AI-generated Content, AIGC）。
- **ControlNet**：为扩散模型加入额外空间条件，例如人体姿态、线稿边缘、深度图或分割图，从而更严格地控制构图。例如根据火柴人骨架生成遵循指定动作的人像，或把毛坯房照片转换为保持原结构的精装房效果图。

### 5.6 自然语言处理（Natural Language Processing, NLP）
- **序列依赖（Sequential Dependency）**：文本后续内容常依赖前文语义，模型需要建立跨位置关系。
- **机器翻译（Machine Translation）**：把一种语言自动转换为另一种语言，例如 Google 翻译和实时语音翻译。
- **情感分析（Sentiment Analysis）**：判断文本是正面、负面还是中性，例如社交媒体监控和产品评论分析。
- **文本生成（Text Generation）**：生成符合上下文、语法和任务要求的文本，例如自动写作助手和新闻生成。
- **语音识别（Speech Recognition）**：把语音转换为文字，例如 Siri、Alexa 等智能助手和自动字幕。
- **聊天机器人（Chatbot）**：理解用户输入并生成响应，例如客服机器人、虚拟助手和 GPT 类模型。

### 5.7 推荐系统（Recommendation System）
- 电影和音乐推荐根据历史评分、播放和跳过行为生成个性化结果，例如 Netflix 和 Spotify。
- 电商推荐根据购买、浏览和上下文推荐商品，例如亚马逊和淘宝。
- 社交媒体推荐根据互动和内容特征推荐信息或社交关系，例如 Facebook 和 Instagram。
- 深度模型不是推荐系统唯一方案；数据反馈回路、曝光偏差、多样性和长期用户价值同样关键。

### 5.8 多模态大模型（Multimodal Large Model）
- 多模态模型联合处理文本、图像、音频或视频，使模型能够完成跨模态检索、视觉问答、图文生成和语音交互。
- 多模态能力不等于所有输入都被可靠理解；仍需针对每种模态和组合场景分别评估幻觉（Hallucination）、对齐误差、隐私和安全边界。

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/00-概览（Overview）/01-深度学习概览（Deep Learning Overview）/01-深度学习概览（Deep Learning Overview）-20260328152651015.png]]

## 6. 经典深度学习项目结构（Canonical Deep-learning Project Structure）
> [!tip] 大白话理解（Plain-language Intuition）
> 项目目录的核心目的不是“文件越多越专业”，而是把数据处理、模型定义、训练、评估和推理拆开。这样修改模型时不会意外改坏数据处理，预测脚本也不必复制训练代码。

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/00-概览（Overview）/01-深度学习概览（Deep Learning Overview）/01-深度学习概览（Deep Learning Overview）-20260820123000001.png]]

```text
project_name/
├── data/
│   ├── raw/                 # 原始数据：尽量只读，避免处理过程覆盖唯一来源。
│   └── processed/           # 可由 process.py 重新生成的训练输入。
├── logs/                    # TensorBoard、指标、运行日志与实验记录。
├── models/                  # 检查点（Checkpoint）和最终权重；大文件通常不提交 Git。
├── src/
│   ├── config.py            # 路径、超参数、随机种子和设备配置。
│   ├── process.py           # 清洗、切分、编码并保存处理结果。
│   ├── tokenizer.py         # 文本项目可选：词表、分词与序列编码。
│   ├── dataset.py           # Dataset、DataLoader、采样和批处理拼接。
│   ├── model.py             # 只定义网络结构与 forward() 数据流。
│   ├── train.py             # 训练循环、反向传播、验证、日志和保存。
│   ├── evaluate.py          # 在固定数据划分上计算指标与错误分析。
│   └── predict.py           # 加载正式权重，对新输入执行推理。
├── tests/                   # 可选：形状、数据边界和关键函数测试。
├── requirements.txt         # 依赖与版本；也可以使用 pyproject.toml。
└── README.md                # 安装、数据准备、训练、评估和推理命令。
```
### 6.1 各模块的职责边界（Module Boundaries）
- **`data/raw/`**：保存不可替代的原始数据。处理脚本不能在此原地覆盖文件，避免清洗错误破坏来源。
- **`data/processed/`**：只保存可复现的派生数据；需要记录生成参数、Tokenizer 版本、类别映射和数据划分随机种子。
- **`config.py`**：集中管理路径与超参数，但令牌（Token）、密码和私人地址不得写入公开配置；应使用环境变量或本地忽略文件。
- **`dataset.py`**：负责“怎样取一个样本、怎样组成一个 Batch”，不负责更新模型参数。
- **`model.py`**：负责输入张量到输出张量的映射；不把训练轮数、文件路径或日志代码塞进 `forward()`。
- **`train.py`**：协调模型、损失函数（Loss Function）、优化器（Optimizer）、调度器（Scheduler）和检查点。
- **`evaluate.py`**：固定模型参数，只计算验证/测试指标；必须调用 `model.eval()`，并在无需梯度时使用 `torch.no_grad()` 或 `torch.inference_mode()`。
- **`predict.py`**：复用与训练一致的预处理和类别映射；不能在推理脚本中重新发明另一套 Tokenizer。
### 6.2 典型执行顺序（Execution Order）
1. `python -m src.process`：把原始数据转换为可训练格式。
2. `python -m src.train`：训练并保存最佳检查点，同时记录配置和指标。
3. `python -m src.evaluate`：对固定验证集或测试集执行一次性评估。
4. `python -m src.predict`：加载审核通过的权重，处理新样本。
### 6.3 最小配置示例（Minimal Configuration Example）
```python
# src/config.py
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrainConfig:
    # 由当前文件位置推导项目根目录，避免把个人绝对路径写进公开代码。
    project_root: Path = Path(__file__).resolve().parent.parent
    batch_size: int = 64
    learning_rate: float = 1e-3
    epochs: int = 30
    seed: int = 42

    @property
    def raw_data_dir(self) -> Path:
        return self.project_root / "data" / "raw"

    @property
    def model_dir(self) -> Path:
        return self.project_root / "models"


config = TrainConfig()
print(config.raw_data_dir.name)  # 'raw'
print(config.model_dir.name)  # 'models'
```
> [!warning] 项目差异（Project-specific Variation）
> 图中的 `tokenizer.py` 对 NLP 项目很常见，但纯图像项目可能改为 `transforms.py`；大型项目还会增加 `configs/`、`scripts/`、`metrics.py`、`callbacks.py`、`checkpoints/` 和实验追踪。目录应服从职责边界，不需要机械复制固定模板。

## 7. 停车场系统选型示例（Parking-system Selection Example）
面对“智能停车场计费系统”需求，可以按任务拆分，而不是直接选择一个大模型：
1. 使用目标检测器定位车辆或车牌；YOLO 是强调实时性的候选之一。
2. 裁剪车牌区域后，使用字符识别模型或光学字符识别（Optical Character Recognition, OCR）读取号码。ResNet 可作为视觉骨干（Backbone）的一种思路，但完整车牌识别通常还需要序列建模、文本解码和规则校验。
3. 如果部署到算力有限的摄像头或边缘设备，可评估 MobileNet 等轻量骨干、量化（Quantization）、剪枝（Pruning）或硬件推理引擎。
4. 系统还必须处理夜间、反光、遮挡、倾斜、无牌车、重复入场、计费规则和人工复核；模型精度只是完整系统的一部分。

## 8. 损失函数：原理、选型与代码（Loss Functions: Principles, Selection, and Code）
### 8.1 损失函数在训练中的作用（Role in Training）
- 损失函数（Loss Function）把模型预测与真实目标之间的差异压缩为一个可优化的标量。
- 反向传播（Backpropagation）计算损失对每个参数的梯度；优化器沿着能降低损失的方向更新参数。
- “损失较低”只表示更符合当前目标函数和数据，不自动等于业务指标更好、公平性更高或泛化更强。
> [!tip] 大白话理解（Plain-language Intuition）
> 损失函数像评分规则：模型做完题后，它决定错在哪里、错得多严重。评分规则选错，即使分数不断下降，模型也可能学成错误的方向。
### 8.2 互斥多分类交叉熵（Multi-class Cross-entropy）
- 适用于每个样本只属于一个类别的任务，例如手写数字十分类、图片物种分类和单标签文本分类。
- 对目标类别 $y$，单样本交叉熵可写为：
$$
L=-\log\left(\frac{e^{z_y}}{\sum_{c=1}^{C}e^{z_c}}\right)
$$
- $z_c$ 是未归一化得分（Logit）。PyTorch `nn.CrossEntropyLoss()` 内部已经组合 `LogSoftmax` 与负对数似然，因此不要提前对输入执行 `Softmax`。
- 常见输入形状是 `[N, C]`，目标是形状 `[N]` 的 `torch.long` 类别索引；语义分割常用 `[N, C, H, W]` 对 `[N, H, W]`。
### 8.3 二分类与多标签交叉熵（Binary and Multi-label Cross-entropy）
- 二分类与多标签分类把每个输出看成独立的“是/否”判断。
- 二元交叉熵（Binary Cross-entropy, BCE）为：
$$
L=-\left[y\log\sigma(z)+(1-y)\log(1-\sigma(z))\right]
$$
- `nn.BCEWithLogitsLoss()` 把 Sigmoid 与 BCE 合并，并利用稳定的数值计算，通常优于手动 `sigmoid()` 后再调用 `nn.BCELoss()`。
- 输入与目标必须具有相同形状，目标通常是 `[0,1]` 范围的浮点张量。类别不平衡时可设置 `pos_weight`，但必须检查广播（Broadcasting）是否落在正确的类别维。
### 8.4 回归损失（Regression Losses）
- **均方误差（Mean Squared Error, MSE）**：$L=\frac{1}{N}\sum_i(\hat y_i-y_i)^2$。平方项会强烈惩罚大误差，适合误差近似高斯分布、需要强调大偏差的回归任务，但对异常值敏感。
- **平均绝对误差（Mean Absolute Error, MAE）**：$L=\frac{1}{N}\sum_i|\hat y_i-y_i|$。对异常值更稳健，但在零点处不可导，框架使用次梯度（Subgradient）处理。
- **平滑 L1（Smooth L1）/Huber 损失**：小误差区域使用平方项，大误差区域使用绝对值项，在稳定梯度与异常值鲁棒性之间折中，常用于边界框回归（Bounding-box Regression）。
### 8.5 视觉、序列与表征学习中的复合损失（Composite Losses）

|任务（Task）|常用损失（Common Loss）|原理与边界（Principle and Boundary）|
|---|---|---|
|语义分割（Semantic Segmentation）|交叉熵、Dice Loss、Focal Loss|交叉熵逐像素分类；Dice 强调整体重叠；Focal 降低易分类样本权重。常组合使用，但权重需要验证|
|目标检测（Object Detection）|分类损失 + IoU/GIoU/DIoU/CIoU + 对象性损失|类别、位置和是否存在目标是不同子目标，不能用单一损失替代全部|
|序列生成（Sequence Generation）|Token 级交叉熵|通常忽略 Padding Token；训练目标与自由生成质量仍存在暴露偏差（Exposure Bias）|
|语音转写（Speech Transcription）|CTC Loss、序列到序列交叉熵|CTC 对齐未知的输入/输出序列；需要合法的输入长度和目标长度|
|自编码器（Autoencoder）|MSE、BCE、感知损失（Perceptual Loss）|根据输入范围与重建目标选择；像素误差低不一定视觉质量高|
|度量与对比学习（Metric and Contrastive Learning）|Triplet Loss、InfoNCE|拉近正样本、推远负样本；采样策略和温度参数会显著影响训练|
|生成对抗网络（GAN）|对抗损失及其变体|生成器与判别器构成动态博弈，两个损失的数值不能单独代表生成质量|
### 8.6 PyTorch 损失函数示例（PyTorch Loss Examples）
```python
import torch
from torch import nn

# 互斥三分类：输入是 logits，目标是类别索引。
class_logits = torch.tensor([[2.0, 0.5, -1.0], [0.2, 0.1, 1.8]])
class_targets = torch.tensor([0, 2])
cross_entropy = nn.CrossEntropyLoss()(class_logits, class_targets)
print(f"CrossEntropy: {cross_entropy.item():.4f}")  # CrossEntropy: 0.2834

# 二分类/多标签：logits 与浮点目标形状相同，不先手动做 Sigmoid。
binary_logits = torch.tensor([1.5, -0.5, 0.2])
binary_targets = torch.tensor([1.0, 0.0, 1.0])
binary_loss = nn.BCEWithLogitsLoss()(binary_logits, binary_targets)
print(f"BCEWithLogits: {binary_loss.item():.4f}")  # BCEWithLogits: 0.4245

# 回归：同一组误差下比较 MSE 与 L1。
predictions = torch.tensor([2.5, 0.0, 2.0])
targets = torch.tensor([3.0, -0.5, 2.0])
mse = nn.MSELoss()(predictions, targets)
mae = nn.L1Loss()(predictions, targets)
print(f"MSE: {mse.item():.4f}")  # MSE: 0.1667
print(f"MAE: {mae.item():.4f}")  # MAE: 0.3333
```
> [!warning] 任务与张量契约（Task and Tensor Contract）
> 选择损失时必须同时核对输出形状（Shape）、目标编码、类别是否互斥、输入是 Logit 还是概率、Padding、类别不平衡和归约方式（Reduction）。完整推导与更多边界见 [[02-神经网络损失函数与输出契约（Neural Network Loss Functions and Output Contracts）]]。
## 9. 优化器：原理、选型与代码（Optimizers: Principles, Selection, and Code）
### 9.1 基本更新原理（Basic Update Principle）
- 设参数为 $\theta_t$、学习率为 $\eta$、当前梯度为 $g_t=\nabla_\theta L(\theta_t)$，最基本的梯度下降更新为：
$$
\theta_{t+1}=\theta_t-\eta g_t
$$
- 学习率过大可能跨过低损失区域并发散；过小会收敛缓慢或长期停留在平坦区域。
- 小批量随机梯度包含噪声，这能帮助探索参数空间，但也会使损失曲线抖动。
> [!tip] 大白话理解（Plain-language Intuition）
> 梯度告诉模型“当前位置最陡的上坡方向”，优化器就朝反方向下山。Momentum 记住之前的方向；Adam 还会根据每个参数近期梯度的大小自动调节步幅。
### 9.2 常用优化器（Common Optimizers）
- **随机梯度下降（Stochastic Gradient Descent, SGD）**：直接用当前小批量梯度更新。实现简单、内存小，充分调参后常用于 CNN；但对学习率和调度器较敏感。
- **动量（Momentum）**：维护梯度的指数移动平均（Exponential Moving Average），在方向稳定时加速，在来回震荡方向上相互抵消。
- **AdaGrad**：累计历史平方梯度，使频繁更新的参数学习率逐渐变小；适合稀疏特征，但学习率可能衰减过度。
- **RMSProp**：改用平方梯度的指数移动平均，避免 AdaGrad 分母无限累积，常用于非平稳目标和传统 RNN 训练。
- **Adam**：同时维护梯度一阶矩与二阶矩并做偏差修正，早期收敛通常较快，是通用实验基线。
- **AdamW**：把权重衰减（Weight Decay）从 Adam 的矩估计中解耦，常用于 Transformer、预训练模型微调和现代视觉模型。
### 9.3 优化器选型表（Optimizer Selection Table）

|场景（Scenario）|常用起点（Typical Starting Point）|调参重点（Tuning Focus）|
|---|---|---|
|经典 CNN 从零训练|带 Momentum 的 SGD、AdamW|SGD 通常需要 Warmup、较长训练和明确的学习率衰减|
|Transformer / BERT 微调|AdamW|较小学习率、权重衰减、Warmup、梯度裁剪和分层学习率|
|小型原型或未知任务|Adam / AdamW|先建立可靠基线，再比较泛化、速度和显存|
|稀疏参数或高维稀疏特征|AdaGrad、SparseAdam|确认梯度确实是稀疏形式，并监控有效学习率|
|传统 RNN 与非平稳序列|Adam、RMSProp|梯度裁剪、序列长度和隐藏状态处理|
|超大批量训练|SGD/LARS/LAMB 等|学习率缩放、Warmup、同步成本与数值稳定性|
### 9.4 一次完整参数更新（One Complete Parameter Update）
```python
import torch
from torch import nn

model = nn.Linear(2, 1, bias=False)
with torch.no_grad():
    model.weight.copy_(torch.tensor([[1.0, -1.0]]))

inputs = torch.tensor([[2.0, 1.0]])
targets = torch.tensor([[0.0]])
loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

optimizer.zero_grad()       # 清除上一步累积梯度；PyTorch 默认会累积 .grad。
predictions = model(inputs)
loss = loss_fn(predictions, targets)
loss.backward()             # 只计算梯度，还没有改变参数。
optimizer.step()            # 使用当前梯度真正更新参数。

weights = [round(value, 1) for value in model.weight.detach().flatten().tolist()]
print(weights)  # [0.6, -1.2]

# AdamW 的典型构造；weight_decay 与 Adam 的矩估计解耦。
adamw = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)
print(type(adamw).__name__)  # AdamW
```
### 9.5 调度器、梯度裁剪与停止条件（Schedulers, Clipping, and Stopping）
- **学习率调度器（Learning-rate Scheduler）**：训练初期 Warmup 可避免大步长破坏随机初始化或预训练权重；后期余弦退火（Cosine Annealing）或分段衰减可帮助细化参数。
- **梯度裁剪（Gradient Clipping）**：在 `loss.backward()` 后、`optimizer.step()` 前限制梯度范数，常用于 RNN 和大模型训练；它缓解梯度爆炸，但不能修复错误数据或错误损失。
- **早停（Early Stopping）**：根据验证集指标停止训练，不能用测试集反复选择停止轮次，否则会造成测试集泄漏。
- **混合精度（Mixed Precision）**：可降低显存并提高吞吐，但需要正确的梯度缩放与数值检查。
- 完整推导、Momentum、AdaGrad、RMSProp、Adam 与学习率调度见 [[04-梯度下降、优化器与学习率调度（Gradient Descent, Optimizers, and Learning-rate Scheduling）]]。
## 10. 任务、网络、输出、损失与优化器组合（End-to-end Selection Matrix）

|任务（Task）|网络（Network）|输出契约（Output Contract）|常用损失（Loss）|常用优化器起点（Optimizer Start）|
|---|---|---|---|---|
|图像互斥分类|ResNet、EfficientNet、ViT|`[N,C]` Logits|CrossEntropy|SGD + Momentum 或 AdamW|
|二分类/多标签分类|CNN、MLP、Transformer|`[N]` 或 `[N,C]` Logits|BCEWithLogits|AdamW 或 SGD|
|目标检测|YOLO、Faster R-CNN、DETR|类别 + 边界框 + 对象性/匹配结果|分类损失 + IoU 系列 + 回归损失|SGD 或 AdamW，遵循实现默认配方起步|
|语义分割|U-Net、DeepLab、SegFormer|`[N,C,H,W]` Logits|CrossEntropy + Dice/Focal|AdamW 或 SGD|
|连续值回归|MLP、CNN、Transformer|与目标相同的连续张量|MSE、L1、Smooth L1|AdamW、Adam 或 SGD|
|文本分类|BERT、Transformer、RNN/LSTM/GRU|类别 Logits|CrossEntropy 或 BCEWithLogits|AdamW；传统 RNN 也常用 Adam|
|机器翻译与文本生成|Encoder-Decoder Transformer、Decoder-only Transformer|`[N,T,V]` 词表 Logits|忽略 Padding 的 Token 级 CrossEntropy|AdamW + Warmup/Schedule|
|图节点/图分类|GCN、GraphSAGE、GAT|节点或图级 Logits|CrossEntropy / BCEWithLogits|Adam / AdamW|
|重建与异常检测|Autoencoder、VAE|与输入同形的重建结果及可选分布参数|MSE/BCE + KL 等正则项|Adam / AdamW|
|生成图像|Diffusion Model、GAN|噪声/速度/数据预测，或真假得分|去噪目标、对抗损失及感知损失|AdamW（扩散）或 Adam（GAN 常见起点）|
> [!warning] 组合不是固定答案（Recipes Are Not Guarantees）
> 表格提供的是合理起点，不是永久最佳配置。最终选择必须在相同数据划分、指标、训练预算和随机种子下比较，并结合延迟、显存、稳定性和业务错误成本。
### 10.1 PyTorch 官方接口参考（Official PyTorch API References）
- [CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)：互斥分类的 Logit、目标形状、类别权重与 `ignore_index` 契约。
- [BCEWithLogitsLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html)：Sigmoid 与 BCE 的稳定组合，以及 `pos_weight` 的广播边界。
- [AdamW](https://docs.pytorch.org/docs/stable/generated/torch.optim.AdamW.html)：解耦权重衰减、默认参数与优化器状态加载要求。
- [Conv2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.modules.conv.Conv2d.html)：卷积输入输出形状与 `stride`、`padding`、`dilation`、`groups` 参数。
- [TransformerEncoderLayer](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html)：参考 Transformer 编码层的维度、头数、前馈层、归一化顺序与 `batch_first`。
## 11. 发展脉络（Historical Development）
### 11.1 早期探索（Early Exploration）
- 20 世纪 40 年代，沃伦·麦卡洛克（Warren McCulloch）和沃尔特·皮茨（Walter Pitts）提出早期人工神经元计算模型。
- 1958 年，弗兰克·罗森布拉特（Frank Rosenblatt）提出感知器（Perceptron），可完成线性可分的二分类任务。
- 20 世纪 60 年代已出现多层网络相关探索，但计算能力、训练方法和数据规模限制了应用。

### 11.2 训练突破与低潮（Training Breakthrough and Slowdown）
- 1986 年，大卫·鲁梅尔哈特（David Rumelhart）、杰弗里·辛顿（Geoffrey Hinton）和罗纳德·威廉姆斯（Ronald Williams）等系统推广误差反向传播（Backpropagation）训练多层网络。
- 当时算力、数据和训练稳定性仍有限，支持向量机（Support Vector Machine, SVM）和决策树等方法在许多任务中更具优势。

### 11.3 复兴与视觉突破（Revival and Vision Breakthroughs）
- 2006 年前后，深度信念网络（Deep Belief Network, DBN）和逐层无监督预训练推动深层网络重新受到关注。
- 2012 年，AlexNet 在 ImageNet 大规模视觉识别挑战赛中显著降低分类错误率，展示 GPU、大数据和深层 CNN 的组合潜力；引用具体提升百分比时必须同时给出所用指标与比较基线。
- 2014 年，伊恩·古德费洛（Ian Goodfellow）等提出生成对抗网络，推动生成模型研究。
- 2015 年，何恺明（Kaiming He）等提出残差网络（Residual Network, ResNet），缓解深层网络的优化退化问题并改善梯度传播。它不能被简化为彻底解决所有梯度消失或梯度爆炸问题。

### 11.4 现代阶段（Modern Era）
- 2016 年，AlphaGo 战胜李世石，使深度强化学习（Deep Reinforcement Learning）在复杂决策任务中的能力进入公众视野，并常被视为当代人工智能发展阶段的代表事件之一。

> [!tip] 大白话理解（Plain-language Intuition）
> 传统流程常需要人先规定“看哪些特征”，深度学习则让模型从大量样本中逐层学出表示：靠近输入的层识别简单模式，后面的层把这些模式组合成更抽象的结构。它不是凭空理解数据，而是用大量参数、训练数据和损失反馈逐步调整内部表示。
- 2017 年，Transformer 架构提出，成为后续预训练语言模型的重要基础。
- 2018 年前后，BERT 和 GPT 系列代表基于 Transformer 的预训练语言模型快速发展。
- 2022 年，ChatGPT 推动大语言模型（Large Language Model, LLM）和人工智能生成内容（AI-generated Content, AIGC）进入大规模交互应用阶段。

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/00-概览（Overview）/01-深度学习概览（Deep Learning Overview）/01-深度学习概览（Deep Learning Overview）-20260328152650708.png]]
