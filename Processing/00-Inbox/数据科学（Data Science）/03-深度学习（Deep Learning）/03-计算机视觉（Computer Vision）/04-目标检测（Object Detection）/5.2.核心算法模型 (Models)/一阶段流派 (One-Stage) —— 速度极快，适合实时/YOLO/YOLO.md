source: https://www.cnblogs.com/yangykaifa/p/19604067

YOLO和Faster RCNN同在2016年提出，YOLO是典型的一阶段法（下面讲的YOLO都指YOLOv1)

**它把目标检测问题化为了回归一个特征向量**的问题

其中P表示目前框里有实例的概率，x、y是框中心点在原图归一化后的比例[点坐标](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E7%82%B9%E5%9D%90%E6%A0%87&zhida_source=entity)（eg：0.1 ；0.6），然后类似的宽w、高h。假如P高于一个阈值的化，就看class的概率 

> 论文在PASCAL VOC检测数据集上进行评估，有20个种类，所以C=20

![](https://pic2.zhimg.com/v2-b2a318dfea6a3bdd9ab6d49221479501_1440w.jpg)

图片被分成了49个框，每个框预测2个bounding box，因此上面的图中有98个bounding box，这里框线的粗细表示P的大小

首先会把图片划成S * S的块，对每一个块预测B个框（Bounding Box）的中心点归一化坐标和宽高

> （w和h是指bounding box在整个图像里面的占比）

所以YOLO做的是用部分去预测整体（狗头预测整个狗），我们只要输入图像，回归特征向量就好了

后面削减框数量的方法也是用的NMS

YOLO和Faster RCNN的对比：

1. YOLO 非常非常块，模型可以一秒45帧，fast YOLO（轻量级）一秒155帧，因为它整个网络架构都是为快设计的
2. 相应的准确率就没有Faster RCNN高

后来YOLO系列反复迭代，越来越强大，也提升了准确率，再后期也能做实例分割的问题如YOLOv8

到这里我们目标检测部分基本讲完了

在介绍实例识别之前，我们再介绍一下语义分割：

## 语义分割与FCN：

![](https://pic3.zhimg.com/v2-61ad8591d5821305f0fc7e479f76b420_1440w.jpg)

语义分割用流畅的边缘(像素级别）把所有相同语义的实例（eg：所有的人）用相同颜色标出来

![](https://pic1.zhimg.com/v2-9db86dc443ff57f953396d9c3f69e2ec_1440w.jpg)

它是实例分割的退化情况

最经典的架构叫做[全卷积网络](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E5%85%A8%E5%8D%B7%E7%A7%AF%E7%BD%91%E7%BB%9C&zhida_source=entity)：

![](https://pic3.zhimg.com/v2-c94821f911754203a4e88fe210bbaeb4_1440w.jpg)

黑：背景 绿：沙发 蓝：狗 棕：猫

叫这个名字是因为它把传统CNN的最后面的全连接层换成了[反卷积层](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E5%8F%8D%E5%8D%B7%E7%A7%AF%E5%B1%82&zhida_source=entity)（全部是卷积了），实现了把[空间映射](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E7%A9%BA%E9%97%B4%E6%98%A0%E5%B0%84&zhida_source=entity)回了图像的相同尺寸，然后再对**每一个像素进行分类预测**

![](https://pic4.zhimg.com/v2-74da30f9ccc7b223adf10845b2c54303_1440w.jpg)

和传统CNN的网络区别

当然只用最后一个小小的去预测整个图肯定效果不好，于是论文采用了Skip Connections，采样之前的池化结果，然后一起来参与复原尺寸的情况（类似[残差连接](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E6%AE%8B%E5%B7%AE%E8%BF%9E%E6%8E%A5&zhida_source=entity)）

![](https://pic1.zhimg.com/v2-f08cfed129e91c78f46acd8dfec4e456_1440w.jpg)

各产生了放大（上采样）32倍，16倍，8倍的预测图

![](https://pic3.zhimg.com/v2-5d456e9bfb1bf0e2ee773ec677b51488_1440w.jpg)

三种预测图和真实情况的展示，易知我们要综合考虑

## 实例分割

这里介绍的是Kaiming的经典模型 Mask R-CNN，这里的R-CNN是指基于Faster R-CNN

我做了一个图来表示R-CNN系列的大体架构演变

![](https://pic4.zhimg.com/v2-a085d9da94e0404b6d59e4747f4c0c1b_1440w.jpg)

> Mask R-CNN在COCO数据集上训练，它是第一个提供实例分割标注的数据集，也可以完成其他任务

Mask R-CNN在**每个感兴趣区域（RoI）**进行一个二分类的语义分割，在这个感兴趣区域**同时做目标检测和分割**，这个分支与用于分类和[目标检测框](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E7%9B%AE%E6%A0%87%E6%A3%80%E6%B5%8B%E6%A1%86&zhida_source=entity)回归的分支并行执行

![](https://pic4.zhimg.com/v2-fef452697c46c4fd632b99a010f9ede1_1440w.jpg)

最后一个层就是我们的FCN层，也就是我们找到一个实例的区域做语义分割

然后Mask R-CNN的Mask这个名字也困惑了我很久，这里的Mask 和NLP任务里面的意义（不能考虑）不同，它是一个CV的术语。我觉得更可以用Photoshop里面的蒙版来理解：

Mask用来指代**一个覆盖在图像上的层，用于指示图像的某些部分，**这些掩码是二值的，通常用 1 表示对象的像素，用 0 表示背景的像素。在实例分割里面，我们会对所有的有实例的区域都分别做一次Mask（而不是用1，2，3，... ，n来表示不同个体）

Mask R-CNN 的还应用[特征金字塔网络](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E7%89%B9%E5%BE%81%E9%87%91%E5%AD%97%E5%A1%94%E7%BD%91%E7%BB%9C&zhida_source=entity)（FPN, Feature Pyramid Network）来提高模型对不同尺寸和比例物体的检测和分割能力

### RoIAlign

这个是Mask R-CNN提出的一种高精度对齐方法，它替换了RoI Pooling

我们来想想RoI Pooling的问题:

![](https://pic2.zhimg.com/v2-0b7cb13334927864a16dee61ca8b55d3_1440w.jpg)

它其实就是对RoI区域切割做最大池化

但是假如模型割出来的部分的边界不是一个整数呢？也就边界在次像素级别呢？

RoI Pooling采取的方法是整数量化（向上取整）

![](https://pic4.zhimg.com/v2-27625d7c8330f52783de70810ee06ced_1440w.jpg)

但是移动了就不准了，这也就是哭脸的原因

然后RoI Align采取了一种传统的[图像处理](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E5%9B%BE%E5%83%8F%E5%A4%84%E7%90%86&zhida_source=entity)方法来解决这个问题

与其移动RoI再每一个块池化出值，不如在原图的每一个块上采样点，用[双线性插值](https://zhida.zhihu.com/search?content_id=236618382&content_type=Article&match_order=1&q=%E5%8F%8C%E7%BA%BF%E6%80%A7%E6%8F%92%E5%80%BC&zhida_source=entity)计算采样点，用采样点替换池化值

![](https://pic3.zhimg.com/v2-3423d6826100cb056970953fa0bfb7f2_1440w.jpg)

用附件的图像像素的点计算黑色采样点

![](https://pic4.zhimg.com/v2-0443e4643cb935565014aec166bdf647_1440w.jpg)

双精度插值：先线性计算（距离当权重）蓝色点，在线性计算率绿点

### FPN

FPN 构建了一个自顶向下的架构，其中深层的高级特征被融合到浅层的低级特征中。这样可以在不同层级上获取多尺度的特征

![](https://pic2.zhimg.com/v2-a100c9646ce6f89bb1d9ab8440a8a96d_1440w.jpg)

深层特征通常能捕捉到更抽象的信息（如物体类别），但空间分辨率较低；浅层特征则具有更高的空间分辨率，但语义信息较少。FPN 通过结合这些不同层级的特征，提供了同时具有高空间分辨率和强语义信息的特征图