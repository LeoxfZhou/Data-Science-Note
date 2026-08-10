
### 第一部分：重构充填【死磕级全行注释代码】

```Python
# -*- coding: utf-8 -*-
"""
Desc : 三层全连接 BP 神经网络 - 基于 NumPy 实现
**结构**: 输入层 (input_size) → 隐藏层(hidden_size) → 输出层(output_size)

**功能**:
- 前向传播: 输入 → 隐藏层 → 输出层
- 反向传播: 计算梯度
- 参数更新: 更新权重
- 训练循环
- 可视化
"""

import numpy as np  # 导入Python科学计算的核心库NumPy，用于底层高效的矩阵乘法与多维数组运算
import matplotlib.pyplot as plt  # 导入数据可视化绘图库，用于训练后期绘制Loss损失下降曲线
from typing import Tuple, Optional, List  # 导入类型提示组件，提升代码的可读性与IDE静态代码检查的健壮性


# ==================== 激活函数类 ====================


class Activation:
    """激活函数类：集中管理神经网络所有非线性映射及其导数"""

    @staticmethod
    def sigmoid(x: np.ndarray) -> np.ndarray:
        """Sigmoid 激活函数：将输入数值压缩映射至 (0, 1) 区间，常用于二分类或输出层"""
        # np.clip 用于防数值爆炸：将输入限制在 [-500, 500] 之间，防止 np.exp(x) 产生无穷大（inf）导致 NaN 崩溃
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    @staticmethod
    def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
        """Sigmoid 导数：反向传播计算梯度时使用，公式为 f'(x) = f(x) * (1 - f(x))"""
        s = Activation.sigmoid(x)  # 先计算出当前输入的正向 Sigmoid 激活值值
        return s * (1 - s)  # 利用导数简化特性直接返回梯度矩阵

    @staticmethod
    def relu(x: np.ndarray) -> np.ndarray:
        """ReLU 激活函数：修正线性单元，保留正数，将所有负数强制清零，能极大缓解梯度消失"""
        return np.maximum(0, x)  # 逐元素对比，若小于0则返回0，大于0则保留原值

    @staticmethod
    def relu_derivative(x: np.ndarray) -> np.ndarray:
        """ReLU 导数：若输入大于0，导数为1；若输入小于或等于0，导数为0"""
        return (x > 0).astype(float)  # (x > 0) 返回布尔矩阵，通过 astype(float) 将 True 变 1.0，False 变 0.0

    @staticmethod
    def tanh(x: np.ndarray) -> np.ndarray:
        """Tanh 激活函数：双曲正切函数，将输入数值压缩映射至 (-1, 1) 区间，均值为 0，收敛通常快于 Sigmoid"""
        return np.tanh(x)  # 直接调用 NumPy 内置的矩阵级双曲正切运算

    @staticmethod
    def tanh_derivative(x: np.ndarray) -> np.ndarray:
        """Tanh 导数：反向传播计算隐藏层梯度时使用，公式为 f'(x) = 1 - tanh^2(x)"""
        return 1 - np.tanh(x) ** 2  # 直接利用公式返回逐元素求导后的梯度矩阵

    @staticmethod
    def softmax(x: np.ndarray) -> np.ndarray:
        """Softmax 激活函数：用于多分类输出层，将输出的原始分值（Logits）转化为相加为 1 的概率分布"""
        # np.max(..., axis=1, keepdims=True) 用于防溢出小技巧：减去每行的最大值，防止指数阶乘太大导致内存爆掉
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)  # 除以每行指数之和，实现行规范化概率化


# ==================== 损失函数类 ====================

class Loss:
    """损失函数类：集中管理前向预测误差的计算及其反向导数"""

    @staticmethod
    def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """均方误差损失（Mean Squared Error）：常用于回归任务，算预测值与真实值差值的平方均值"""
        return np.mean((y_true - y_pred) ** 2)  # 计算所有元素差值平方后取整体算术平均数

    @staticmethod
    def mse_derivative(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """MSE 对预测值 y_pred 的导数：常用于反向传播起点"""
        # 求导公式：2 * (y_pred - y_true) / N，除以样本总数 y_true.shape[0] 是因为前一步使用了 np.mean
        return 2 * (y_pred - y_true) / y_true.shape[0]

    @staticmethod
    def cross_entropy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """交叉熵损失（Cross Entropy）：常用于分类任务，衡量两个概率分布之间的差异"""
        epsilon = 1e-15  # 定义一个极小的微量，防止 y_pred 恰好等于 0 导致 log(0) 产生负无穷大的计算灾难
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)  # 将预测概率强制拦截限制在 [1e-15, 1 - 1e-15] 之间
        return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))  # 严格执行交叉熵公式，算每行总和后再取批次均值

    @staticmethod
    def cross_entropy_derivative(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """多分类交叉熵对预测值 y_pred 的导数：当配合 Softmax 使用时可以极度化简"""
        epsilon = 1e-15  # 同样定义防止分母为0的极小微量值
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)  # 边界约束安全性拦截
        return (y_pred - y_true) / y_true.shape[0]  # 返回标准的未化简基础导数（注意：除以批次大小以配合平均Loss）


# ==================== 三层 BP 神经网络 ====================
class BPNeuralNetwork:
    """三层全连接 BP 神经网络。结构逻辑：输入层 (X) → 隐藏层 (W1, b1) → 输出层 (W2, b2)"""

    def __init__(self, input_size: int, hidden_size: int, output_size: int,
                 learning_rate: float = 0.01, activation: str = 'sigmoid'):
        """
        初始化神经网络结构参数
        参数:
            input_size: 输入层特征数 (如二维坐标就是2)
            hidden_size: 隐藏层神经元个数 (用于提取高维非线性特征空间)
            output_size: 输出层神经元个数 (如2分类任务就是2)
            learning_rate: 梯度下降更新步伐大小 (学习率)
            activation: 选择隐藏层的激活函数类型 ('sigmoid', 'relu', 'tanh')
        """
        self.input_size = input_size  # 保存输入层特征维度至全局成员变量
        self.hidden_size = hidden_size  # 保存隐藏层神经元节点数至全局成员变量
        self.output_size = output_size  # 保存输出层神经元节点数至全局成员变量
        self.learning_rate = learning_rate  # 保存基础学习率至全局成员变量

        # 动态路由选择隐藏层的激活函数及其导数对齐映射
        if activation == 'relu':  # 匹配 ReLU 流水线
            self.activation = Activation.relu  # 绑定正向激活函数
            self.activation_derivative = Activation.relu_derivative  # 绑定反向导数
        elif activation == 'tanh':  # 匹配 Tanh 流水线
            self.activation = Activation.tanh  # 绑定正向激活函数
            self.activation_derivative = Activation.tanh_derivative  # 绑定反向导数
        else:  # 默认降级匹配标准 sigmoid 流程
            self.activation = Activation.sigmoid  # 绑定正向激活函数
            self.activation_derivative = Activation.sigmoid_derivative  # 绑定反向导数

        # 核心调用：执行网络全部权重与偏置矩阵的初始化创建
        self._initialize_weights()

        # 初始化一个空列表，用于全程追踪记录每一个迭代 Epoch 结束后的 Loss 值，供后续画图
        self.loss_history: List[float] = []

    def _initialize_weights(self):
        """Xavier 权重初始化：根据网络层输入输出维度动态缩放随机初始值，防止模型深层死掉或梯度爆炸"""
        # 输入层 到 隐藏层 的权重 W1。形状：(输入维度, 隐藏层维度)。乘以缩放因子 np.sqrt(2.0 / (输入+输出)) 保持方差稳定
        self.W1 = np.random.randn(self.input_size, self.hidden_size) * \
                  np.sqrt(2.0 / (self.input_size + self.hidden_size))
        self.b1 = np.zeros((1, self.hidden_size))  # 隐藏层偏置 b1，初始化为全0行向量。形状：(1, 隐藏层维度)

        # 隐藏层 到 输出层 的权重 W2。形状：(隐藏层维度, 输出层维度)。同样做标准的 Xavier 均匀缩放处理
        self.W2 = np.random.randn(self.hidden_size, self.output_size) * \
                  np.sqrt(2.0 / (self.hidden_size + self.output_size))
        self.b2 = np.zeros((1, self.output_size))  # 输出层偏置 b2，初始化为全0行向量。形状：(1, 输出层维度)

    def forward(self, X: np.ndarray) -> np.ndarray:
        """
        正向数据流向传播（前向计算预测值）
        参数:
            X: 输入的批量样本矩阵数据。形状：(batch_size, input_size)
        返回:
            输出层经 Sigmoid 激活后的预测概率。形状：(batch_size, output_size)
        """
        # 1. 搬运数据流经【输入层 → 隐藏层】：线性变换 z1 = X · W1 + b1
        # np.dot 执行标准的矩阵乘法：(B, I) 点乘 (I, H) 得到 (B, H)，加上偏置 b1 会利用 NumPy 广播机制自动加到每一行
        self.z1 = np.dot(X, self.W1) + self.b1  
        self.a1 = self.activation(self.z1)  # 非线性激活：将结果输入选定的激活函数，形状保持为 (batch_size, hidden_size)

        # 2. 搬运数据流经【隐藏层 → 输出层】：线性变换 z2 = a1 · W2 + b2
        # (B, H) 点乘 (H, O) 得到 (B, O)，同样加上输出层偏置 b2
        self.z2 = np.dot(self.a1, self.W2) + self.b2  
        self.a2 = Activation.sigmoid(self.z2)  # 固定使用 Sigmoid 激活输出层，将分值变成 0-1 的二分类概率分布 (B, O)

        # 🌟 极其重要：必须把当前批次的输入 X 缓存到类全局变量中，因为反向传播算权重偏置梯度时，必须要拿 X 参与点乘
        self.X = X

        return self.a2  # 返回最终整个网络输出的终点预测概率矩阵

    def backward(self, y_true: np.ndarray, y_pred: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        反向误差流向传播（基于链式法则，自尾部向前倒推算梯度，并就地更新所有权重）
        参数:
            y_true: 真实标签 One-hot 矩阵。形状：(batch_size, output_size)
            y_pred: 前向传播刚算出来的网络预测矩阵 a2。形状：(batch_size, output_size)
        返回:
            当前批次算出的权重梯度元组 (dW1, dW2)，供分析使用
        """
        batch_size = y_true.shape[0]  # 获取当前执行反向传播的批量样本件数，用于后续将总梯度平摊均值化

        # 1. 计算【输出层】的误差项 delta2 (即 损失函数L 对 线性输出z2 的偏导数 dL/dz2)
        # 💡 核心化简面试大坑：由于老师这里同时选用了【交叉熵损失 + 输出层Sigmoid】的最佳黄金组合，两者的复杂导数在数学上精妙抵消
        # 最终化简出的优雅结果直接就是：(预测值 - 真实值) / 样本数。形状保持为 (batch_size, output_size)
        delta2 = (y_pred - y_true) / batch_size  

        # 2. 计算【隐藏层】的误差项 delta1 (根据链式法则，由后层 delta2 往回倒推)
        # 矩阵乘法：输出层误差 delta2(B, O) 点乘 权重转置 W2.T(O, H) 得到回传误差矩阵，形状为 (B, H)
        # 然后使用 `*` 执行【逐元素相乘(Hadamard积)】乘上隐藏层激活前的导数值 activation_derivative(z1)
        delta1 = np.dot(delta2, self.W2.T) * self.activation_derivative(self.z1)

        # 3. 计算【隐藏层 → 输出层】参数的最终梯度
        # dW2 梯度等于：前层激活输出的转置 a1.T(H, B) 点乘 本层误差 delta2(B, O)，得到的形状完美契合 W2 本身 (H, O)
        dW2 = np.dot(self.a1.T, delta2)  
        # db2 梯度等于：把当前批次每一个样本产生的 delta2 误差直接按轴 0 (垂直行方向) 全部加起来，keepdims保持(1, O)形状
        db2 = np.sum(delta2, axis=0, keepdims=True)  

        # 4. 计算【输入层 → 隐藏层】参数的最终梯度
        # dW1 梯度等于：最开始的输入转置 X.T(I, B) 点乘 隐藏层误差 delta1(B, H)，得到的形状完美契合 W1 本身 (I, H)
        dW1 = np.dot(self.X.T, delta1)  
        # db1 梯度等于：同样按轴 0 压扁累加 delta1 矩阵，抽出对偏置项 b1 的更新梯度，形状保持 (1, H)
        db1 = np.sum(delta1, axis=0, keepdims=True)  

        # 5. 就地执行最经典的随机梯度下降（SGD）参数更新逻辑
        self.W2 -= self.learning_rate * dW2  # 输出层权重减去：学习率 * 对应梯度（往坡度下降的反方向走一步）
        self.b2 -= self.learning_rate * db2  # 输出层偏置更新
        self.W1 -= self.learning_rate * dW1  # 隐藏层权重减去：学习率 * 对应梯度
        self.b1 -= self.learning_rate * db1  # 隐藏层偏置更新

        return dW1, dW2  # 将这一批算出来的模型核心权重梯度作为元组安全返回

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 1000,
              batch_size: int = 32, verbose: bool = True) -> List[float]:
        """
        全自动化迭代训练核心主循环
        参数:
            X: 训练集所有特征大矩阵 (n_samples, input_size)
            y: 训练集所有真实标签大矩阵 (n_samples, output_size)
            epochs: 规定大主循环需要完整跑多少轮
            batch_size: 指定小批量梯度下降（Mini-batch GD）每次喂给网络的样本数量
            verbose: 设为True时，会定期在控制台打印Loss战报进度日志
        返回:
            整个生命周期沉淀下来的平均 Loss 历史记录列表
        """
        n_samples = X.shape[0]  # 捕获训练集大池子里一共有多少件样本总数
        self.loss_history = []  # 每次启动训练前，都将历史 Loss 跟踪记录器清空重置

        for epoch in range(epochs):  # 进入 Epoch 外层大循环
            # 💡 深度学习防死记硬背绝招：在每一轮大循环刚开始时，必须把整个数据集的行索引全部随机打乱（洗牌机制）
            indices = np.random.permutation(n_samples)  # 随机生成一套范围在 [0, n_samples) 之间的打乱索引数组
            X_shuffled = X[indices]  # 依照这套乱序索引，重新洗牌提取特征矩阵，确保网络不再死记硬背样本的出场顺序
            y_shuffled = y[indices]  # 依照同样乱序索引，重新洗牌标签矩阵，确保特征和标签始终一一对应

            epoch_loss = 0.0  # 初始化当前这一轮 Epoch 累加的总损失初始分值为 0.0
            n_batches = max(1, n_samples // batch_size)  # 用样本总数整除以批大小，算出当前 Epoch 内部需要切分成多少个 Batch 分批跑

            for i in range(n_batches):  # 进入 Mini-batch 内层小循环，开始分批吞吐喂养数据
                # 动态计算出当前第 i 个批次在打乱数据集里的行指针起止边界
                start_idx = i * batch_size  # 本批次起点
                end_idx = min(start_idx + batch_size, n_samples)  # 本批次终点（用min防止最后不足一个完整 batch 时溢出边界）
                X_batch = X_shuffled[start_idx:end_idx]  # 利用 NumPy 的高级切片机制，切出当前批次的特征小矩阵
                y_batch = y_shuffled[start_idx:end_idx]  # 利用同样的切片机制，切出对应批次的真实标签小矩阵

                # ① 触发前向传播：将这批数据喂进网络，一路前行推演计算出预测结果概率 y_pred
                y_pred = self.forward(X_batch)

                # ② 触发损失评估：调用 Loss 类的交叉熵静态方法，测算当前批次预测值与客观真实值的脱靶误差
                loss = Loss.cross_entropy(y_batch, y_pred)
                epoch_loss += loss  # 将此批次的损失值累加进这一轮 Epoch 的大总帐中

                # ③ 触发反向传播：拿着刚才脱靶的误差，自尾部逆流而上，自动算好梯度并当场更新了 self.W 和 self.b 参数
                self.backward(y_batch, y_pred)

            # 算术平均：用本轮累加的总损失除以总批次数，算出这一整轮 Epoch 跌落下来的平均 Loss
            avg_loss = epoch_loss / n_batches
            self.loss_history.append(avg_loss)  # 将这个极具参考价值的平均 Loss 存进历史追踪器，供画图使用

            # 打印控制日志：为了防止日志疯狂刷屏，设定每跑满 100 轮 Epoch 才在终端打出一份阶段性战报
            if verbose and (epoch + 1) % 100 == 0:
                print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.6f}")

        return self.loss_history  # 整个万轮大迭代彻底谢幕后，返回沉淀下来的完整 Loss 走势列表

    def predict(self, X: np.ndarray) -> np.ndarray:
        """纯净预测函数：外部调用时，直接把特征矩阵丢给前向传播走一遍，返回的就是最终概率矩阵"""
        return self.forward(X)

    def predict_class(self, X: np.ndarray) -> np.ndarray:
        """预测具体离散类别：拿到一堆概率分布后，直接提取每一行里概率最大的那一项的【数字索引编号】"""
        y_pred = self.predict(X)  # 先跑一遍 forward 拿到全套概率分布矩阵 (B, O)
        return np.argmax(y_pred, axis=1)  # 利用 np.argmax 沿着轴 1 (水平列方向) 找出最大数值所在的列编号位置

    def accuracy(self, X: np.ndarray, y: np.ndarray) -> float:
        """评估计算模型在指定数据集上的准确率"""
        y_pred_class = self.predict_class(X)  # 一键提取模型预测出来的数字类别编号数组
        y_true_class = np.argmax(y, axis=1)  # 同样对真实的 One-hot 标签进行反查，转换成原始数字类别编号数组
        return np.mean(y_pred_class == y_true_class)  # 逐元素对比看是否相等，并取平均值（等价于 正确数 / 总数）

    def plot_loss(self, save_path: Optional[str] = None):
        """借助 Matplotlib 工具包，将追踪到的 Loss 走势列表绘制成精美的损失下降曲线图"""
        plt.figure(figsize=(10, 6))  # 新建画布，并指定宽 10 英寸、高 6 英寸的舒适比例
        plt.plot(self.loss_history, linewidth=2)  # 把 loss 历史数组绘制上去，设置线条宽度为 2 像素
        plt.xlabel('Epoch', fontsize=12)  # 为横坐标贴上“Epoch(迭代轮次)”的标签文本，字体设为12号
        plt.ylabel('Loss', fontsize=12)  # 为纵坐标贴上“Loss(误差值)”的标签文本
        plt.title('Training Loss Curve', fontsize=14)  # 为整个图表正上方冠以一个醒目的英文大标题
        plt.grid(True, alpha=0.3)  # 开启淡淡的背景网格线，透明度设为 0.3，方便读数

        if save_path:  # 智能判断：如果调用方指定了本地保存路径
            plt.savefig(save_path, dpi=150, bbox_inches='tight')  # 则调用绘图核心将其保存为高分辨率png，自动裁剪边缘留白
            print(f"损失曲线已保存到：{save_path}")  # 在控制台提示保存大捷

        plt.show()  # 挂起画布，在电脑屏幕上把图形弹窗显现出来

    def save(self, path: str):
        """持久化保存模型：利用 NumPy 专属的 np.savez 将内存中练好的矩阵矩阵字典压缩固化到本地 .npz 文件中"""
        np.savez(path,
                 W1=self.W1, b1=self.b1,  # 压缩写入隐藏层的矩阵参数
                 W2=self.W2, b2=self.b2,  # 压缩写入输出层的矩阵参数
                 input_size=self.input_size,  # 顺带把模型的输入维度数也死牢固化进去
                 hidden_size=self.hidden_size,  # 固化隐藏层神经元数
                 output_size=self.output_size)  # 固化输出层神经元数
        print(f"模型已保存到：{path}")  # 保存成功日志

    def load(self, path: str):
        """复活加载模型：从磁盘读取 .npz 压缩包文件，将各个数字矩阵完好如初地提取填入当前网络的内存中"""
        data = np.load(path)  # 调用 np.load 拆封解压本地文件
        self.W1 = data['W1']  # 恢复重构隐藏层权重 W1
        self.b1 = data['b1']  # 恢复重构隐藏层偏置 b1
        self.W2 = data['W2']  # 恢复重构输出层权重 W2
        self.b2 = data['b2']  # 恢复重构输出层偏置 b2
        self.input_size = int(data['input_size'])  # 强制还原回 Python 基础的整型，恢复输入规格
        self.hidden_size = int(data['hidden_size'])  # 还原恢复隐藏层规格
        self.output_size = int(data['output_size'])  # 还原恢复输出层规格
        print(f"模型已从 {path} 加载")  # 加载成功日志


# ==================== 运行测试业务模块 ====================

def create_xor_data(n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """生成极具学术研究价值的异或（XOR）线性不可分数据集"""
    X = np.random.randn(n_samples, 2)  # 随机生成(N, 2)形状的高斯分布二维坐标特征数据
    y = np.zeros((n_samples, 2))  # 初始化全0的标签矩阵，准备存放 One-hot 编码形式的真值

    for i in range(n_samples):  # 遍历每一行坐标
        # 根据异或逻辑：横纵坐标同号（都在一三象限）定义为类别0，异号（在二四象限）定义为类别1
        if (X[i, 0] > 0 and X[i, 1] > 0) or (X[i, 0] < 0 and X[i, 1] < 0):
            y[i] = [1, 0]  # 划归为类别 0 的 One-hot 样式
        else:
            y[i] = [0, 1]  # 划归为类别 1 的 One-hot 样式

    return X, y  # 返回组装完美的特征和标签数据集


def create_moons_data(n_samples: int = 1000, noise: float = 0.2) -> Tuple[np.ndarray, np.ndarray]:
    """利用 sklearn 科学工具箱直接生成更具难度的双半月形（moons）线性不可分数据集"""
    from sklearn.datasets import make_moons  # 就地临时导入半月数据集的生成器方法
    X, y = make_moons(n_samples=n_samples, noise=noise, random_state=42)  # 生成经典半月数据并混入指定扰动噪声

    # 执行标准的 One-hot 编码大变身
    y_onehot = np.zeros((n_samples, 2))  # 先量身打造一个规格为 (N, 2) 的纯 0 空白板子
    y_onehot[np.arange(n_samples), y] = 1  # 巧妙运用高级索引，在对应原始类别的通道位置利索地戳上 1

    return X, y_onehot  # 返回半月形特征矩阵及标准化 One-hot 编码标签


def main():
    """本地独立测试与实验启动大入口"""
    print("=" * 60)
    print("三层全连接 BP 神经网络 - XOR / 半月问题演示")
    print("=" * 60)

    # 1. 执行数据源构建阶段
    print("\n1. 创建 moons 数据集...")
    X, y = create_moons_data(n_samples=1000)  # 一键生成 1000 组极富挑战的线性不可分月牙坐标点
    print(f"   数据形状：X={X.shape}, y={y.shape}")

    # 2. 严格按照 8:2 的黄金比例划分训练集与测试集
    split_idx = int(0.8 * len(X))  # 计算截断指针所在行的位置编号
    X_train, X_test = X[:split_idx], X[split_idx:]  # 特征特征切开，前80%用于给网络喂养，后20%用于闭卷考试
    y_train, y_test = y[:split_idx], y[split_idx:]  # 标签随特征同比例同步切开
    print(f"   训练集：{X_train.shape[0]} 样本")
    print(f"   测试集：{X_test.shape[0]} 样本")

    # 3. 神经网络对象的完整实例化建立
    print("\n2. 创建神经网络...")
    nn = BPNeuralNetwork(
        input_size=2,      # 坐标是二维的 (x, y)，所以输入层节点数定死为 2
        hidden_size=16,    # 隐藏层开辟 16 个元老级神经元，用于将二维平面扭转映射到高维可分空间
        output_size=2,     # 任务是二分类，所以输出层节点数设定为 2
        learning_rate=0.1, # 设定学习率为 0.1 确保下坡更新速度稳健
        activation='sigmoid' # 隐藏层选用经典的 Sigmoid 函数来做非线性扭转
    )
    print(f"   结构：{nn.input_size} → {nn.hidden_size} → {nn.output_size}")
    print(f"   学习率：{nn.learning_rate}")

    # 4. 触发炼丹模型训练循环
    print("\n3. 开始训练...")
    nn.train(X_train, y_train, epochs=1000, batch_size=32, verbose=True) # 扔进去跑1000轮，每批32样本

    # 5. 闭卷期末大考评估阶段
    print("\n4. 模型评估...")
    train_acc = nn.accuracy(X_train, y_train)  # 测试在看过的训练集上的死记硬背准确率
    test_acc = nn.accuracy(X_test, y_test)    # 测试在完全没看过的测试集上的真正泛化实力准确率
    print(f"   训练集准确率：{train_acc * 100:.2f}%")
    print(f"   测试集准确率：{test_acc * 100:.2f}%")

    # 6. 随机抓取 5 个真实的盲测样本进行可视化的直观对账
    print("\n5. 预测示例...")
    test_samples = 5  # 指定需要抽测比对的件数
    for i in np.random.permutation(len(X_test))[:test_samples]:  # 乱序抽取5个样本索引
        pred = nn.predict(X_test[i:i + 1])[0]  # 前向传播拿到该单样本的概率行数组
        pred_class = np.argmax(pred)  # 挑出模型眼里概率最大的数字分类
        true_class = np.argmax(y_test[i])  # 剥离出真心的客观真实分类
        print(f"   样本 {i + 1}: 预测={pred_class}, 真实={true_class}")  # 实时打印比对双向战报

    # 7. 绘图与模型存档持久化保存
    print("\n6. 绘制损失曲线...")
    nn.plot_loss(save_path='./loss_curve.png')  # 将 Loss 历史列表绘制固化为图片保存在当前目录下

    nn.save('./bp_model.npz')  # 一键将练好的4大矩阵矩阵参数永久封印进本地硬盘压缩包中

    print("\n" + "=" * 60)
    print("全套实验大获全胜，训练完美结束！")
    print("=" * 60)


if __name__ == "__main__":  # 如果该模块作为独立脚本直接触发运行
    main()  # 则立刻点击启动上面的 main 业务逻辑函数
```

### 第二部分：硬核敲代码笔记：三层 BP 神经网络数学全解析

#### 一、 网络拓扑与符号定义矩阵规格（Shapes）

我们实现的网络由**输入层（Input）**、隐藏层（Hidden）**和**输出层（Output）构成。为了保证高并发的矩阵并行运算，我们定义批次样本数为 $B$ (`batch_size`)。

- **输入样本大矩阵**: $\mathbf{X} \in \mathbb{R}^{B \times I}$ ，其中 $I$ 为 `input_size`（本例中为 $2$）。
- **隐藏层权重与偏置**:
    - $\mathbf{W_1} \in \mathbb{R}^{I \times H}$ ，其中 $H$ 为 `hidden_size`。
    - $\mathbf{b_1} \in \mathbb{R}^{1 \times H}$，通过广播机制自动适配每一行样本。
- **输出层权重与偏置**:
    - $\mathbf{W_2} \in \mathbb{R}^{H \times O}$ ，其中 $O$ 为 `output_size`（本例中为 $2$）。
    - $\mathbf{b_2} \in \mathbb{R}^{1 \times O}$。
- **真实标签矩阵（One-hot）**: $\mathbf{Y} \in \mathbb{R}^{B \times O}$。

#### 二、 前向传播过程（Forward Propagation）

前向传播的实质就是矩阵的**线性仿射变换**叠加**非线性激活映射**：

##### 1. 输入层 $\rightarrow$ 隐藏层

隐藏层的净输入（未激活值） $\mathbf{Z_1}$：

$$\mathbf{Z_1} = \mathbf{X} \cdot \mathbf{W_1} + \mathbf{b_1} \quad \text{, 规格为 } (B \times H)$$

隐藏层经激活函数（如 Sigmoid）处理后的输出值 $\mathbf{A_1}$：

$$\mathbf{A_1} = \sigma(\mathbf{Z_1}) \quad \text{, 规格为 } (B \times H)$$

##### 2. 隐藏层 $\rightarrow$ 输出层

输出层的净输入 $\mathbf{Z_2}$：

$$\mathbf{Z_2} = \mathbf{A_1} \cdot \mathbf{W_2} + \mathbf{b_2} \quad \text{, 规格为 } (B \times O)$$

输出层最终的预测概率值 $\mathbf{A_2}$（即代码中的 `y_pred`）：

$$\mathbf{A_2} = \sigma(\mathbf{Z_2}) \quad \text{, 规格为 } (B \times O)$$

#### 三、 损失函数（Loss Function）

代码中采用**多分类多标签交叉熵损失函数（Cross Entropy Loss）**，其在一个批次上的均值公式为：

$$\mathcal{L} = -\frac{1}{B} \sum_{i=1}^{B} \sum_{k=1}^{O} y_{ik} \ln(a_{2,ik})$$

#### 四、 反向传播核心：微积分链式法则推导（Backward Propagation）

反向传播的本质就是计算损失函数 $\mathcal{L}$ 对每个参数矩阵的偏导数。为了推导直观，我们引入**误差项（Error Term）** $\delta$，它定义为**损失 $\mathcal{L}$ 对某一全连接层净输入 $\mathbf{Z}$ 的偏导数**。

##### 1. 输出层的误差项 $\delta_2$（大厂经典面试题化简）

我们需要计算：

$$\delta_2 = \frac{\partial \mathcal{L}}{\partial \mathbf{Z_2}}$$

根据链式法则：

$$\frac{\partial \mathcal{L}}{\partial z_{2,ik}} = \frac{\partial \mathcal{L}}{\partial a_{2,ik}} \cdot \frac{\partial a_{2,ik}}{\partial z_{2,ik}}$$

- **第一步：损失对预测值的求导**

    $$\frac{\partial \mathcal{L}}{\partial a_{2,ik}} = -\frac{1}{B} \cdot \frac{y_{ik}}{a_{2,ik}}$$

- **第二步：输出层激活函数 Sigmoid 对其输入的求导**

    $$\frac{\partial a_{2,ik}}{\partial z_{2,ik}} = \sigma'(z_{2,ik}) = a_{2,ik}(1 - a_{2,ik})$$

- **第三步：组合相乘化简**

    $$\frac{\partial \mathcal{L}}{\partial z_{2,ik}} = \left( -\frac{1}{B} \cdot \frac{y_{ik}}{a_{2,ik}} \right) \cdot \Big( a_{2,ik}(1 - a_{2,ik}) \Big) = \frac{1}{B} (a_{2,ik} - y_{ik})$$

写成完整的矩阵形式，即代码中的 `delta2` 变量：

$$\delta_2 = \frac{1}{B} (\mathbf{A_2} - \mathbf{Y}) \quad \text{, 规格为 } (B \times O)$$

> 💡 **笔记心得**：这也是为什么代码里的 `delta2` 根本没有显式调用 `sigmoid_derivative` 的原因！因为**交叉熵损失的分母**与**Sigmoid导数的乘项**在数学上**精妙地消掉了**。这种组合既优雅，又在工程上避免了由于预测值接近 0 或 1 导致的梯度消失。

##### 2. 隐藏层误差项 $\delta_1$ 的往回倒推

根据链式法则，损失向后传导必须流经权重 $\mathbf{W_2}$ 以及隐藏层的激活导数：

$$\delta_1 = \frac{\partial \mathcal{L}}{\partial \mathbf{Z_1}} = \left( \frac{\partial \mathcal{L}}{\partial \mathbf{Z_2}} \cdot \mathbf{W_2}^T \right) \odot \sigma'(\mathbf{Z_1})$$

写成代码中的矩阵表达式（`delta1`）：

$$\delta_1 = (\delta_2 \cdot \mathbf{W_2}^T) \odot \text{activation\_derivative}(\mathbf{Z_1}) \quad \text{, 规格为 } (B \times H)$$

_(注：其中 $\odot$ 代表 Hadamard 积，即 NumPy 中的逐元素星号 `*` 乘法)_

##### 3. 计算四项核心权重的梯度

拿到误差项 $\delta_2$ 和 $\delta_1$ 后，由控制变量法，对权重矩阵的偏导数只需将其**前一层的输入转置**点乘**本层的误差项**即可：

- **输出层权重与偏置梯度（`dW2`, `db2`）**:

    $$\mathbf{dW_2} = \frac{\partial \mathcal{L}}{\partial \mathbf{W_2}} = \mathbf{A_1}^T \cdot \delta_2 \quad \text{, 规格为 } (H \times B) \cdot (B \times O) = (H \times O)$$

    $$\mathbf{db2} = \frac{\partial \mathcal{L}}{\partial \mathbf{b_2}} = \sum_{\text{row}=1}^{B} \delta_2 \quad \text{, 规格为 } (1 \times O)$$

- **隐藏层权重与偏置梯度（`dW1`, `db1`）**:

    $$\mathbf{dW_1} = \frac{\partial \mathcal{L}}{\partial \mathbf{W_1}} = \mathbf{X}^T \cdot \delta_1 \quad \text{, 规格为 } (I \times B) \cdot (B \times H) = (I \times H)$$

    $$\mathbf{db1} = \frac{\partial \mathcal{L}}{\partial \mathbf{b_1}} = \sum_{\text{row}=1}^{B} \delta_1 \quad \text{, 规格为 } (1 \times H)$$

#### 五、 梯度下降更新规则（Gradient Descent）

在主循环中，模型利用算好的梯度（偏导数），朝着梯度的**反方向**（坡度最陡峭的下方）迈出大小为 $\eta$（学习率 `learning_rate`）的一步，实现进化：

$$\mathbf{W_2} \leftarrow \mathbf{W_2} - \eta \cdot \mathbf{dW_2}$$

$$\mathbf{b_2} \leftarrow \mathbf{b_2} - \eta \cdot \mathbf{db2}$$

$$\mathbf{W_1} \leftarrow \mathbf{W_1} - \eta \cdot \mathbf{dW_1}$$

$$\mathbf{b_1} \leftarrow \mathbf{b_1} - \eta \cdot \mathbf{db1}$$

把这套矩阵维度背后的微积分链式法则逻辑理通后，配合上方的逐行源码注释，这次的基于 NumPy 纯手写 BP 的作业和原理你就已经彻底吃透了！