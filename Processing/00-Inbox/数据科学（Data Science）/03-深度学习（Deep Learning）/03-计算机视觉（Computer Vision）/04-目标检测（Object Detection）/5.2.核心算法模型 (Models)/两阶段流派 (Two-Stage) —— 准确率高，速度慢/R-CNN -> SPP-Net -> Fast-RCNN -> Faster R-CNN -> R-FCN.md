## R-CNN：

首先要找到选区（region），这一步叫**Region Proposal**，R-CNN使用的方法是Selective Search ，它延续分析图像信息的思想

**其实就是用一系列规则把数以十万记的框，缩减到2000左右**

（下面和深度学习关系较弱，可以掠过）

> **主要步骤:**使用一种过分割手段，将[图像分割](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E5%9B%BE%E5%83%8F%E5%88%86%E5%89%B2&zhida_source=entity)成小区域 (1k~2k 个)查看现有小区域，按照合并规则合并可能性最高的相邻两个区域。重复直到整张图像合并成一个区域位置输出所有曾经存在过的区域，所谓[候选区域](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E5%80%99%E9%80%89%E5%8C%BA%E5%9F%9F&zhida_source=entity)其中合并规则优先合并以下四种区域：  
> 1. 颜色（[颜色直方图](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E9%A2%9C%E8%89%B2%E7%9B%B4%E6%96%B9%E5%9B%BE&zhida_source=entity)）相近的  
> 2. 纹理（[梯度直方图](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E6%A2%AF%E5%BA%A6%E7%9B%B4%E6%96%B9%E5%9B%BE&zhida_source=entity)）相近的  
> 3. 合并后总面积小的： 保证合并操作的尺度较为均匀，避免一个大区域陆续“吃掉”其他小区域 （例：设有区域a-b-c-d-e-f-g-h。较好的[合并方式](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E5%90%88%E5%B9%B6%E6%96%B9%E5%BC%8F&zhida_source=entity)是：ab-cd-ef-gh -> abcd-efgh -> abcdefgh。 不好的合并方法是：ab-c-d-e-f-g-h ->abcd-e-f-g-h ->abcdef-gh -> abcdefgh）  
> 4. 合并后，总面积在其BBOX中所占比例大的： 保证合并后形状规则。  
> 上述四条规则只涉及区域的颜色直方图、梯度直方图、面积和位置。合并后的区域特征可以直接由子区域特征计算而来，速度较快。

![](https://pica.zhimg.com/v2-50450d9a71c5a88358d90b8d92a2ee2e_1440w.jpg)

然后找到了选区，用了warp（挤压）的方法变成相同尺寸送进CNN分类

> 具体论文里提出了各项异性缩放（直接拉）和各项同性缩放（用平均颜色填充外围）

然后对**2000个特征向量**用于**分类**和**回归边界框（进一步精确定位**），然后采取了一个方法来减少框叫**NMS**

### **先讲一下IOU：**

![](https://pica.zhimg.com/v2-306dc315378c9b3349af296f3ab11e4e_1440w.jpg)

就是算交集在并集的比例

### **NMS（非极大化抑制）**

**这是一个很重要的概念，就是一个图片被划了很多个框，怎么选出最佳的框：**  

![](https://pica.zhimg.com/v2-1fb2425d4e02e3fa83e0cc76576d7e1e_1440w.jpg)

就像上面的图片一样，定位一个车辆，最后算法就找出了一堆的方框，我们需要判别哪些矩形框是没用的

非极大值抑制的方法是：先假设有6个矩形框，根据分类器的类别分类概率做排序**，假设从小到大属于车辆的概率 分别为A、B、C、D、E、F**

(1) 从最大概率矩形框F开始，**分别判断A~E与F的重叠度IOU是否大于某个设定的阈值;**

(2) **假设B、D与F的重叠度超过阈值，那么就扔掉B、D**；并标记第一个矩形框F，是我们保留下来的。

(3) **从剩下的矩形框A、C、E中，选择概率最大的E，然后判断E与A、C的重叠度，重叠度大于一定的阈值，那么就扔掉**；并标记E是我们保留下来的第二个矩形框。**就这样一直重复，找到所有被保留下来的矩形框**

**但是R-CNN也有一些缺点：**

1. R-CNN 的训练是多阶段的（multi-stage）：  
    预训练 CNN→针对检测微调→训练分类器→训练[边界框回归器](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E8%BE%B9%E7%95%8C%E6%A1%86%E5%9B%9E%E5%BD%92%E5%99%A8&zhida_source=entity)

2. R-CNN 的时间空间消耗大：  
为了训练 SVM 分类器和边界框回归器，每个区域的特征都要提取出来，并且存到磁盘上

3. R-CNN 检测慢：

检测时需要提取每个区域的特征（每一个区域单独送入卷积），但生成的区域有重叠，所以计算也有重叠

然后在里面作者Ross Girshick一个人2015出了Fast R-CNN

## Fast R-CNN

它比R-CNN快了非常多

> 训练时间从84小时减少为9.5小时，测试时间从47秒减少为0.32秒，效果基本一样

首次明确提出RoI（region of interest)，**改进如下：**

①卷积不再是对每个Region Proposal进行，而是直接对整张图像

②用Roi Pooling进行特征的尺寸变换，而不是传统的Clip/Warp（因为[全连接层](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E5%85%A8%E8%BF%9E%E6%8E%A5%E5%B1%82&zhida_source=entity)的输入要求尺寸大小一样，因此不能直接把Region Proposal作为输入）

③ 用SoftMax代替原来的SVM分类器（不然要单独分开训练）

![](https://pic3.zhimg.com/v2-4ee0973c00cf37330536c41273f51686_1440w.jpg)

原来rcnn的cnn，分类，回归是三个模块，现在合在一起了（但是最前面的region proposal还是分开的）； faster把region proposal换成了网络然后也合在了一起

RoI pooling就是对cnn最后的结果利用ss的分块结果进行分割，然后再采用最大池化

它把不同的proposal映射到相同的尺寸（原图的1/16）然后划出固定的小方格（7*7），然后每一个进行最大池化，输出进分类和回归器

无论候选区域的原始尺寸如何，RoI [池化层](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E6%B1%A0%E5%8C%96%E5%B1%82&zhida_source=entity)都能保证**输出一个固定大小的特征向量，这对于后续的分类和回归操作**非常重要

这里论文指出，fast RCNN结合了SSPnet

**SSPnet既可以解决把不同大小的图像变成相同大小的特征向量，又可以对RCNN进行[并行计算](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E5%B9%B6%E8%A1%8C%E8%AE%A1%E7%AE%97&zhida_source=entity)加速**

这里的并行指的是所有候选区域共享相同的卷积特征映射，这些[特征映射](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=2&q=%E7%89%B9%E5%BE%81%E6%98%A0%E5%B0%84&zhida_source=entity)可以一次性计算完成，然后被各个候选区域共同使用，也就是从以前的2000个候选区分布进CNN，变成了只进一次卷积

> 注：在这里相同大小的特征向量是前置条件，不然[input vector](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=input+vector&zhida_source=entity)大小不同  
> 而传统[方法误差](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E6%96%B9%E6%B3%95%E8%AF%AF%E5%B7%AE&zhida_source=entity)太大了，直到SSPnet提出了我们才敢这么干

举一个形象的例子：

我们以前是**先把蛋糕切成很多块**（当然选区可以有重叠），然后**一个个进烤箱**

现在是先整体烤好，再用已经确定好的模具来切

### SSPnet

这个也是Kaiming提出的

![](https://pic3.zhimg.com/v2-7795d56a13f66453dc2a44c9b7692348_1440w.jpg)

论文给出了两个传统resize image的方法，分别是剪切和拉伸，但是这样就会有信息损失和几何扭曲

下面的图就是SSP的最大贡献，不同尺寸图像的输入进来，采用相同的分割方法，最后一个格子得到一个值

最后concat的结果就是特征向量

![](https://pic3.zhimg.com/v2-c4ef4874cf75e7e62d136febd8ff718a_1440w.jpg)

都变成了含21个元素的特征向量

下图是从一整张图片进卷积输出的feature map进行SPP操作的情况

![](https://pic4.zhimg.com/v2-e1308b6b710a94c78c3b59cc97deb81b_1440w.jpg)

只对窗口范围内操作

而这种情况和我们的主线更为相似，我们这里的输入的窗口就是RoI

RoI Pooling也是因此得名

然后一年之后（2016），作者[Ross Girshick](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=2&q=Ross+Girshick&zhida_source=entity)又拉上了Kaiming和两个华人整了Faster RCNN

## Faster RCNN

它最大的改动是用[神经网络](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C&zhida_source=entity)集成了区域提议——RPN region proposal network的生成

![](https://pic3.zhimg.com/v2-adeeef999711c07533878b58bc0c58e8_1440w.jpg)

rcnn和fast rcnn是用的外部区域提议（也就是指独立于主目标检测模型/网络的算法）faster rcnn提出了（内部）区域提议(由模型的一部分，即区域提议网络（RPN）生成的。可训练的RPN 直接在特征图上运行，这意味着提议的生成过程是与特征提取过程紧密集成的--所有步骤都在一个统一的框架内完成

RPN的实现方法是对特征图的每一个部分，上面预设k个锚点（anchor）,这9个anchor的大小按照三种[长宽比](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E9%95%BF%E5%AE%BD%E6%AF%94&zhida_source=entity)ratio[1:1，1:2，2:1]设置，具体大小根据输入图像的原始目标大小灵活设置

![](https://pic3.zhimg.com/v2-d2ea938e18639cf2af3703c08e14ab64_1440w.jpg)

![](https://pic2.zhimg.com/v2-6a6b43746124b70a51de9545cf25cd61_1440w.jpg)

结合anchor的RoI Pooling