---
title: "Hugging Face Transformers 模型加载与任务接口（Hugging Face Transformers Loading and Task APIs）"
tags:
  - data-science/nlp
status: published
created: 2026-08-13
published_at: 2026-08-13
---
# Hugging Face Transformers 模型加载与任务接口（Hugging Face Transformers Loading and Task APIs）

> [!warning] Transformers 接口边界（Transformers API Boundary）
> `pytorch_pretrained_bert` 与早期模型专用类属于历史接口；现代代码优先使用 `transformers` 的 `AutoTokenizer` 与任务对应的 `AutoModelFor...`。模型加载契约以 [Hugging Face 官方模型文档](https://huggingface.co/docs/transformers/en/models)为准。

## Transformers库使用
> [!tip] 大白话理解（Plain-language Intuition）
> Transformer 把序列建模的主要工作交给注意力和逐位置前馈网络。训练时整段序列可用矩阵并行计算；自回归生成时仍必须逐 token 产生，因此训练并行不等于推理也完全并行。
### 1 了解Transformers库

- Huggingface总部位于纽约，是一家专注于自然语言处理、人工智能和分布式系统的创业公司。他们所提供的聊天机器人技术一直颇受欢迎，但更出名的是他们在NLP开源社区上的贡献。Huggingface一直致力于自然语言处理NLP技术的平民化(democratize)，希望每个人都能用上最先进(SOTA, state-of-the-art)的NLP技术，而非困窘于训练资源的匮乏。同时Hugging Face专注于NLP技术，拥有大型的开源社区。尤其是在github上开源的自然语言处理，预训练模型库 Transformers，已被下载超过一百万次，github上超过24000个star。
- Huggingface Transformers 是基于一个开源基于 transformer 模型结构提供的预训练语言库。它支持 Pytorch，Tensorflow2.0，并且支持两个框架的相互转换。Transformers 提供了NLP领域大量state-of-art的 预训练语言模型结构的模型和调用框架。
- 框架支持了最新的各种NLP预训练语言模型，使用者可快速的进行模型调用，并且支持模型further pretraining 和 下游任务fine-tuning。举个例子Transformers 库提供了很多SOTA的预训练模型，比如BERT, GPT-2, RoBERTa, XLM, DistilBert, XLNet, CTRL。
- 社区Transformer的访问地址为： [https://huggingface.co/](https://huggingface.co/) ，见下图。 ![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000147.png]]
- 备注
  - 1 点击 Model链接可查看、下载预训练模型。点击Datasets链接可查看、下载数据集。点击Docs链接可以阅读预训练模型的编程文档，十分方便
  - 2 SOTA（state-of-the-art）是指目前对某项任务“最好的”算法或技术

### 2 Transformers库三层应用结构

- 管道（Pipline）方式：高度集成的极简使用方式，只需要几行代码即可实现一个NLP任务。
- 自动模型（AutoMode）方式：可载入并使用BERTology系列模型。
- 具体模型（SpecificModel）方式：在使用时，需要明确指定具体的模型，并按照每个BERTology系列模型中的特定参数进行调用，该方式相对复杂，但具有较高的灵活度。

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000148.png]]

### 3 管道方式完成多种NLP任务

**注意：若虚拟机中已经安装transformers，以下安装步骤不需再次执行**

```bash
# 注意在执行clone之前，要查看当前是在那个目录下，比如$HOME/nlpdev/目录下
# 克隆huggingface的transfomers文件
git clone https://github.com/huggingface/transformers.git

# 进行transformers文件夹
cd transformers

# 切换transformers到指定版本
git checkout v4.19.0

# 安装transformers包
pip install .
```

```bash
# 安装datasets数据库，
# 注意workon xxx虚拟机开发环境，在虚拟机开发环境下安装
pip install datasets
```

#### 3.1 文本分类任务

- 文本分类是指模型可以根据文本中的内容来进行分类。例如根据内容对情绪进行分类，根据内容对商品分类等。文本分类模型一般是通过有监督训练得到的。对文本内容的具体分类，依赖于训练时所使用的样本标签。

```text
# 导入工具包
import torch
from transformers import pipeline
import numpy as np

# 情感分类任务
def dm01_test_classification():

    # 1 使用中文预训练模型chinese_sentiment
    # 模型下载地址 git clone https://huggingface.co/techthiyanes/chinese_sentiment

    # 2 实例化pipeline对象
    my_model = pipeline(task='sentiment-analysis', model='./chinese_sentiment')
    # my_model = pipeline(task='sentiment-analysis', model='./bert-base-chinese')

    # 3 文本送给模型 进行文本分类
    output = my_model('我爱北京天安门，天安门上太阳升。')
    print('output--->', output)

# 结果输出
        output---> [{'label': 'star 5', 'score': 0.6314294338226318}]
```

- pipeline函数可以自动从官网下载预训练模型，也可以加载本地的预训练模型

> transformer库中预训练模型查找和下载

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000149.png]]

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000150.png]]

#### 3.2 特征提取任务

- 特征抽取任务只返回文本处理后的特征，属于预训练模型的范畴。特征抽取任务的输出结果需要和其他模型一起工作。

```python
# 特征抽取任务
def dm02_test_feature_extraction():
    # 1 下载中文预训练模型 git clone https://huggingface.co/bert-base-chinese

    # 2 实例化pipeline对象 返回模型对象
    my_model = pipeline(task='feature-extraction', model='./bert-base-chinese')

    # 3 给模型送数据 提取语句特征
    output = my_model('人生该如何起头')
    print('output--->', type(output), np.array(output).shape)

# 输出结果
# output---> <class 'list'> (1, 9, 768)
# 7个字变成9个字原因: [CLS] 人 生 该 如 何 起 头 [SEP]
```

- 不带任务头输出：特征抽取任务属于不带任务头输出，本bert-base-chinese模型的9个字，每个字的特征维度是768
- 带头任务头输出：其他有指定任务类型的比如文本分类，完型填空属于带头任务输出，会根据具体任务类型不同输出不同的结果

#### 3.3 完型填空任务

- 完型填空任务又被叫做“遮蔽语言建模任务”，它属于BERT模型训练过程中的子任务。下面完成一个中文场景的完型填空。

```python
# 完型填空任务
def dm03_test_fill_mask():

    # 1 下载预训练模型 全词模型git clone https://huggingface.co/hfl/chinese-bert-wwm

    # 2 实例化pipeline对象 返回一个模型
    my_model = pipeline(task='fill-mask', model='chinese-bert-wwm')

    # 3 给模型送数据 做预测
    input = '我想明天去[MASK]家吃饭。'
    output = my_model(input)

    # 4 输出预测结果
    print('output--->', output)

# 输出结果
    # output--->
    # [{'score': 0.34331339597702026, 'token': 1961, 'token_str': '她', 'sequence': '我 想 明 天 去 她 家 吃 饭.'},
    # {'score': 0.2533259987831116, 'token': 872, 'token_str': '你', 'sequence': '我 想 明 天 去 你 家 吃 饭.'},
    # {'score': 0.1874391734600067, 'token': 800, 'token_str': '他', 'sequence': '我 想 明 天 去 他 家 吃 饭.'},
    # {'score': 0.1273055076599121, 'token': 2769, 'token_str': '我', 'sequence': '我 想 明 天 去 我 家 吃 饭.'},
    # {'score': 0.02162978984415531, 'token': 2644, 'token_str': '您', 'sequence': '我 想 明 天 去 您 家 吃 饭.'}]
```

> 可以在官网在线查找完型填空结果

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000151.png]]

#### 3.4 阅读理解任务

- 阅读理解任务又称为“抽取式问答任务”，即输入一段文本和一个问题，让模型输出结果。

```python
# 阅读理解任务(抽取式问答)
def dm04_test_question_answering():

    # 问答语句
    context = '我叫张三，我是一个程序员，我的喜好是打篮球。'
    questions = ['我是谁？', '我是做什么的？', '我的爱好是什么？']

    # 1 下载模型 git clone https://huggingface.co/luhua/chinese_pretrain_mrc_roberta_wwm_ext_large

    # 2 实例化化pipeline 返回模型
    model = pipeline('question-answering', model='chinese_pretrain_mrc_roberta_wwm_ext_large')

    # 3 给模型送数据 的预测结果
    print(model(context=context, question=questions))

    # 输出结果
    '''
    [{'score': 1.2071758523357623e-12, 'start': 2, 'end': 4, 'answer': '张三'},
     {'score': 2.60890374192968e-06, 'start': 9, 'end': 12, 'answer': '程序员'},
     {'score': 4.1686924134864967e-08, 'start': 18, 'end': 21, 'answer': '打篮球'}]
    '''
```

#### 3.5 文本摘要任务

- 摘要生成任务的输入一一段文本，输出是一段概况、简单的文字。

```text
# 文本摘要任务
def dm05_test_summarization():

    # 1 下载模型 git clone https://huggingface.co/sshleifer/distilbart-cnn-12-6

    # 2 实例化pipline 返回模型
    my_model = pipeline(task = 'summarization', model="distilbart-cnn-12-6")

    # 3 准备文本 送给模型
    text = "BERT is a transformers model pretrained on a large corpus of English data " \
           "in a self-supervised fashion. This means it was pretrained on the raw texts " \
           "only, with no humans labelling them in any way (which is why it can use lots " \
           "of publicly available data) with an automatic process to generate inputs and " \
           "labels from those texts. More precisely, it was pretrained with two objectives:Masked " \
           "language modeling (MLM): taking a sentence, the model randomly masks 15% of the " \
           "words in the input then run the entire masked sentence through the model and has " \
           "to predict the masked words. This is different from traditional recurrent neural " \
           "networks (RNNs) that usually see the words one after the other, or from autoregressive " \
           "models like GPT which internally mask the future tokens. It allows the model to learn " \
           "a bidirectional representation of the sentence.Next sentence prediction (NSP): the models" \
           " concatenates two masked sentences as inputs during pretraining. Sometimes they correspond to " \
           "sentences that were next to each other in the original text, sometimes not. The model then " \
           "has to predict if the two sentences were following each other or not."
    output = my_model(text)

    # 4 打印摘要结果
    print('output--->', output)

# 输出结果
output---> [{'summary_text': ' BERT is a transformers model pretrained on a large corpus of English data in a self-supervised fashion . It was pretrained with two objectives: Masked language modeling (MLM) and next sentence prediction (NSP) This allows the model to learn a bidirectional representation of the sentence .'}]
```

#### 3.6 NER任务

- 实体词识别（NER）任务是NLP中的基础任务。它用于识别文本中的人名（PER）、地名（LOC）、组织（ORG）以及其他实体（MISC）等。例如：(王 B-PER) (小 I-PER) (明 I-PER) (在 O) (办 B-LOC) (公 I-LOC) (室 I-LOC)。其中O表示一个非实体，B表示一个实体的开始，I表示一个实体块的内部。
- 实体词识别本质上是一个分类任务（又叫序列标注任务），实体词识别是句法分析的基础，而句法分析优势NLP任务的核心。```

```python
# NER任务
def dm06_test_ner():

    # 1 下载模型 git clone https://huggingface.co/uer/roberta-base-finetuned-cluener2020-chinese

    # 2 实例化pipeline 返回模型
    model = pipeline('ner', model='roberta-base-finetuned-cluener2020-chinese')

    # 3 给模型送数据 打印NER结果
    print(model('我爱北京天安门，天安门上太阳升。'))

    '''
    [{'entity': 'B-address', 'score': 0.8838121, 'index': 3, 'word': '北', 'start': 2, 'end': 3},
     {'entity': 'I-address', 'score': 0.83543754, 'index': 4, 'word': '京', 'start': 3, 'end': 4},
     {'entity': 'I-address', 'score': 0.4240591, 'index': 5, 'word': '天', 'start': 4, 'end': 5},
     {'entity': 'I-address', 'score': 0.7524443, 'index': 6, 'word': '安', 'start': 5, 'end': 6},
     {'entity': 'I-address', 'score': 0.6949866, 'index': 7, 'word': '门', 'start': 6, 'end': 7},
     {'entity': 'B-address', 'score': 0.65552264, 'index': 9, 'word': '天', 'start': 8, 'end': 9},
     {'entity': 'I-address', 'score': 0.5376768, 'index': 10, 'word': '安', 'start': 9, 'end': 10},
     {'entity': 'I-address', 'score': 0.510813, 'index': 11, 'word': '门', 'start': 10, 'end': 11}]
    '''
```

### 4 自动模型方式完成多种NLP任务
#### 4.1 文本分类任务

- 文本分类是指模型可以根据文本中的内容来进行分类。例如根据内容对情绪进行分类，根据内容对商品分类等。文本分类模型一般是通过有监督训练得到的。对文本内容的具体分类，依赖于训练时所使用的样本标签。

```python
# 导入工具包
import torch
from transformers import AutoConfig, AutoModel, AutoTokenizer
from transformers import AutoModelForSequenceClassification, AutoModelForMaskedLM, AutoModelForQuestionAnswering
# AutoModelForSeq2SeqLM：文本摘要
# AutoModelForTokenClassification：ner
from transformers import AutoModelForSeq2SeqLM, AutoModelForTokenClassification

# 情感分类任务
def dm01_test_classification():

    # 1 加载tokenizer
    my_tokenizer = AutoTokenizer.from_pretrained('./chinese_sentiment')

    # 2 加载模型
    my_model = AutoModelForSequenceClassification.from_pretrained('./chinese_sentiment')

    # 3 文本转张量
    message = '人生该如何起头'

    # 3-1 return_tensors='pt' 返回是二维tensor
    msg_tensor1 = my_tokenizer.encode(text=message, return_tensors='pt', padding=True, truncation=True, max_length=20)
    print('msg_tensor1--->', msg_tensor1)

    # 3-2 不用return_tensors='pt'是一维列表
    msg_list2 = my_tokenizer.encode(text=message, padding=True, truncation=True, max_length=20)
    print('msg_list2--->', msg_list2)
    msg_tensor2 = torch.tensor([msg_list2])
    print('msg_tensor2--->', msg_tensor2)

    # 4 数据送给模型
    # 4-1
    my_model.eval()
    output1 = my_model(msg_tensor2)
    print('情感分类模型头输出outpout1--->', output1)
    # 4-2
    output2 = my_model(msg_tensor2, return_dict=False)
    print('情感分类模型头输出outpout2--->', output2)
```

- AutoTokenizer、AutoModelForSequenceClassification函数可以自动从官网下载预训练模型，也可以加载本地的预训练模型
- AutoModelForSequenceClassification类管理着分类任务，会根据参数的输入选用不同的模型。
- AutoTokenizer的encode()函数使用return_tensors=’pt‘参数和不使用pt参数对文本编码的结果不同
- AutoTokenizer的encode()函数使用padding='max_length'可以按照最大程度进行补齐，俗称打padding
- 调用模型的forward函数输入return_dict=False参数，返回结果也不同

> 程序运行结果

```text
msg_tensor1---> tensor([[ 101,  782, 4495, 6421, 1963,  862, 6629, 1928,  102]])
msg_list2---> [101, 782, 4495, 6421, 1963, 862, 6629, 1928, 102]
msg_tensor2---> tensor([[ 101,  782, 4495, 6421, 1963,  862, 6629, 1928,  102]])
情感分类模型头输出outpout1---> SequenceClassifierOutput(loss=None, logits=tensor([[-2.7387, -1.7528,  0.2273,  2.0507,  1.4128]],
       grad_fn=<AddmmBackward>), hidden_states=None, attentions=None)
情感分类模型头输出outpout2---> (tensor([[-2.7387, -1.7528,  0.2273,  2.0507,  1.4128]],
       grad_fn=<AddmmBackward>),)

#注1:101代表[CLS] 102代表[SEP]
```

#### 4.2 特征提取任务

- 特征抽取任务只返回文本处理后的特征，属于预训练模型的范畴。特征抽取任务的输出结果需要和其他模型一起工作。

```python
# 特征提取任务-不带任务输出头的任务
def dm02_test_feature_extraction():
    # 1 加载tokenizer
    my_tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path='./bert-base-chinese')

    # 2 加载模型
    my_model = AutoModel.from_pretrained(pretrained_model_name_or_path = './bert-base-chinese')

    # 3 文本转张量
    message = ['你是谁', '人生该如何起头']
    msgs_tensor = my_tokenizer.encode_plus(text=message, return_tensors='pt', truncation=True, pad_to_max_length=True, max_length=30)
    print('msgs_tensor--->', msgs_tensor)

    # 4 给模型送数据提取特征
    my_model.eval()
    output = my_model(**msgs_tensor)
    print('不带模型头输出output--->', output)
    print('outputs.last_hidden_state.shape--->', output.last_hidden_state.shape)  # torch.Size([1, 30, 768])
    print('outputs.pooler_output.shape--->', output.pooler_output.shape)  # torch.Size([1, 768])
```

- 不带任务头输出：特征抽取任务属于不带任务头输出，本bert-base-chinese模型的9个字，每个字的特征维度是768
- 带头任务头输出：其他有指定任务类型的比如文本分类，完型填空属于带头任务输出，会根据具体任务类型不同输出不同的结果

> 程序运行结果

```text
msgs_tensor--->
# 1 input_ids对两个句子text2id以后的结果，
# 101表示段落开头，第一个102代表第一个句子结束，第二个102点第二个句子结束
# 后面的0表示 按照编码要求pad_to_max_length=True和max_length=30补充pad零
{'input_ids': tensor([[ 101,  872, 3221, 6443,  102,  782, 4495, 6421, 1963,  862, 6629, 1928,
          102,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
            0,    0,    0,    0,    0,    0]]),
# 2 token_type_ids表示段落标志0代表第一个句子，1代表第二个句子
 'token_type_ids': tensor([[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0]]),
# 3 attention_mask表示注意力机制的掩码数据，1表示有真实数据，0表示是pad数据需要掩码
 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0]])}

# 1 last_hidden_state表示最后一个隐藏层的数据 [1,30,768]
# 2 pooler_output表示池化，也就是对最后一个隐藏层再进行线性变换以后平均池化的结果。分类时候使用。
不带模型头输出output---> BaseModelOutputWithPoolingAndCrossAttentions(
  last_hidden_state=tensor([[[ 0.7001,  0.4651,  0.2427,  ...,  0.5753, -0.4330,  0.1878],
         [ 0.4017,  0.1123,  0.4482,  ..., -0.2614, -0.2649, -0.1497],
         [ 1.2000, -0.4859,  1.1970,  ...,  0.7543, -0.2405, -0.2627],
         ...,
         [ 0.2074,  0.4022, -0.0448,  ..., -0.0849, -0.0766, -0.2134],
         [ 0.0879,  0.2482, -0.2356,  ...,  0.2967, -0.2357, -0.5138],
         [ 0.4944,  0.1340, -0.2387,  ...,  0.2375, -0.1011, -0.3314]]],
       grad_fn=<NativeLayerNormBackward>),
  pooler_output=tensor([[ 0.9996,  1.0000,  0.9995,  0.9412,  0.8629,  0.9592, -0.8144, -0.9654,
          0.9892, -0.9997,  1.0000,  0.9998, -0.1187, -0.9373,  0.9999, -1.0000,
         ...,
         -0.9967,  1.0000,  0.8626, -0.9993, -0.9704, -0.9993, -0.9971,  0.8522]],
       grad_fn=<TanhBackward>),
  hidden_states=None, past_key_values=None, attentions=None, cross_attentions=None)

outputs.last_hidden_state.shape---> torch.Size([1, 30, 768])
outputs.pooler_output.shape---> torch.Size([1, 768])
```

#### 4.3 完型填空任务

- 完型填空任务又被叫做“遮蔽语言建模任务”，它属于BERT模型训练过程中的子任务。下面完成一个中文场景的完型填空。

```python
# 完型填空任务
def dm03_test_fill_mask():

    # 1 加载tokenizer
    modename = "chinese-bert-wwm"
    # modename = "bert-base-chinese"
    my_tokenizer = AutoTokenizer.from_pretrained(modename)

    # 2 加载模型
    my_model = AutoModelForMaskedLM.from_pretrained(modename)

    # 3 文本转张量
    input = my_tokenizer.encode_plus('我想明天去[MASK]家吃饭.', return_tensors='pt')
    print('input--->', input)

    # 4 给模型送数据提取特征
    my_model.eval()
    output = my_model(**input)
    print('output--->', output)
    print('output.logits--->', output.logits.shape) # [1,12,21128]

    # 5 取概率最高
    mask_pred_idx = torch.argmax(output.logits[0][6]).item()
    print('打印概率最高的字:', my_tokenizer.convert_ids_to_tokens([mask_pred_idx]))
```

> 程序运行结果

```text
# 1 input_ids 对句子text2id以后的结果
# 2 token_type_ids 句子分段信息
# 3 attention_mask 句子掩码信息
input---> {'input_ids': tensor([[ 101, 2769, 2682, 3209, 1921, 1343,  103, 2157, 1391, 7649,  119,  102]]), 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])}

# 1 logits表示MASK预测的结果，也是一种分类概率
# 2 output.logits的分类形状 [1, 12, 21128]
# 3 通过 my_tokenizer.convert_ids_to_tokens()函数完成id2text的操作
output---> MaskedLMOutput(loss=None, logits=tensor([[[ -9.9017,  -9.6006,  -9.8032,  ...,  -7.9744,  -7.7402,  -8.2912],
         [-14.3878, -15.0353, -14.7893,  ..., -10.0437, -10.5279,  -9.7544],
         [-14.2215, -14.1145, -14.5770,  ...,  -6.3246,  -4.1784,  -4.6072],
         ...,
         [-14.6938, -16.8133, -15.1296,  ...,  -9.2327,  -8.1931, -15.2430],
         [-10.8649, -11.4887, -11.5731,  ...,  -6.5378,  -0.8715,  -5.3870],
         [-11.8495, -11.8358, -12.0314,  ...,  -8.4242,  -6.2741,  -8.2787]]],
       grad_fn=<AddBackward0>), hidden_states=None, attentions=None)
output.logits---> torch.Size([1, 12, 21128])
打印概率最高的字: ['她']
```

#### 4.4 阅读理解任务

- 阅读理解任务又称为“抽取式问答任务”，即输入一段文本和一个问题，让模型输出结果。

```python
# 阅读理解任务(抽取式问答)
def dm04_test_question_answering():

    # 1 加载tokenizer
    my_tokenizer = AutoTokenizer.from_pretrained('./chinese_pretrain_mrc_roberta_wwm_ext_large')

    # 2 加载模型
    my_model = AutoModelForQuestionAnswering.from_pretrained('./chinese_pretrain_mrc_roberta_wwm_ext_large')

    # 3 文本转张量
    # 文字中的标点符号如果是中文的话，会影响到预测结果 也可以去掉标点符号
    context = '我叫张三 我是一个程序员 我的喜好是打篮球'
    questions = ['我是谁？', '我是做什么的？', '我的爱好是什么？']

    # 4 给模型送数据 模型做抽取式问答
    my_model.eval()
    for question in questions:
        input = my_tokenizer.encode_plus(question, context, return_tensors='pt')
        print('input--->', input)
        output = my_model(**input)
        print('output--->', output)
        start, end = torch.argmax(output.start_logits), torch.argmax(output.end_logits) +1
        answer =  my_tokenizer.convert_ids_to_tokens(input['input_ids'][0][start:end] )
        print('question:', question, 'answer:', answer)
```

> 程序运行结果：

```text
# input_ids表示text2id后结果 # token_type_ids表示句子分段信息 # attention_mask表示句子attention掩码信息
input---> {'input_ids': tensor([[ 101, 2769, 3221, 6443, 8043,  102, 2769, 1373, 2476,  676, 2769, 3221,
          671,  702, 4923, 2415, 1447, 2769, 4638, 1599, 1962, 3221, 2802, 5074,
         4413,  102]]), 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1]])}

# start_logits end_logits分布表示从原文中抽取答案的位置概率
# 比如：start_logits的最大值代表句子答案最可能开始的位置
# 比如：end_logits的最大值代表句子答案可能结束的位置
output---> QuestionAnsweringModelOutput(loss=None, start_logits=tensor([[ -1.9978, -11.4788, -12.6324, -11.8324, -12.4148, -11.9371,  -2.7246,
          -6.6402,   3.9131,  -2.9533,  -7.0866,  -9.5696,  -4.2775,  -8.9042,
           0.5753,  -6.9468,  -7.0469,  -8.5334, -11.3796,  -9.3905, -11.0242,
         -11.1047,  -5.7124,  -2.7293,  -7.5896, -12.6013]],
       grad_fn=<CopyBackwards>), end_logits=tensor([[ -1.3483, -12.0141, -11.6312, -11.6629, -11.9607, -12.0039,  -4.6118,
          -7.4034,  -2.3499,   4.7159,  -7.2880,  -9.5317,  -6.6742,  -6.0915,
          -7.0023,  -4.9691,   1.4515,  -7.8329,  -9.0895, -10.3742,  -8.7482,
          -9.8567,  -7.2930,  -5.8163,  -1.7323, -12.2525]],
       grad_fn=<CopyBackwards>), hidden_states=None, attentions=None)

question: 我是谁？ answer: ['张', '三']
question: 我是做什么的？ answer: ['程', '序', '员']
question: 我的爱好是什么？ answer: ['打', '篮', '球']
```

#### 4.5 文本摘要任务

- 摘要生成任务的输入一一段文本，输出是一段概况、简单的文字。

```python
# 文本摘要任务
def dm05_test_summarization():
    text = "BERT is a transformers model pretrained on a large corpus of English data " \
           "in a self-supervised fashion. This means it was pretrained on the raw texts " \
           "only, with no humans labelling them in any way (which is why it can use lots " \
           "of publicly available data) with an automatic process to generate inputs and " \
           "labels from those texts. More precisely, it was pretrained with two objectives:Masked " \
           "language modeling (MLM): taking a sentence, the model randomly masks 15% of the " \
           "words in the input then run the entire masked sentence through the model and has " \
           "to predict the masked words. This is different from traditional recurrent neural " \
           "networks (RNNs) that usually see the words one after the other, or from autoregressive " \
           "models like GPT which internally mask the future tokens. It allows the model to learn " \
           "a bidirectional representation of the sentence.Next sentence prediction (NSP): the models" \
           " concatenates two masked sentences as inputs during pretraining. Sometimes they correspond to " \
           "sentences that were next to each other in the original text, sometimes not. The model then " \
           "has to predict if the two sentences were following each other or not."

    # 1 加载tokenizer
    my_tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path="distilbart-cnn-12-6")

    # 2 加载模型
    my_model = AutoModelForSeq2SeqLM.from_pretrained(pretrained_model_name_or_path='distilbart-cnn-12-6')

    # 3 文本转张量
    input = my_tokenizer([text], return_tensors='pt')
    # print('input--->', input)

    # 4 送给模型做摘要
    my_model.eval()
    output = my_model.generate(input.input_ids)
    print('output--->', output)

    # 5 处理摘要结果
    # 5-1 decode 的 skip_special_tokens 参数可以去除 token 前面的特殊字符
    print([my_tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in output])

    # 5-2 convert_ids_to_tokens 函数只能将 ids 还原为 token
    # print(my_tokenizer.convert_ids_to_tokens(output[0]))
```

> 程序运行结果：

```text
output---> tensor([[    2,     0, 11126,   565,    16,    10,  7891,   268,  1421, 11857,
         26492,    15,    10,   739, 42168,     9,  2370,   414,    11,    10,
          1403,    12, 16101, 25376,  2734,   479,    85,    21, 11857, 26492,
            19,    80, 10366,    35, 31755,   196,  2777, 19039,    36, 10537,
           448,    43,     8,   220,  3645, 16782,    36,   487,  4186,    43,
            20,  3092, 10146, 26511,  1626,    80, 24397, 11305,    25, 16584,
           148, 11857, 32155,   479,  7411,    51, 20719,     7, 11305,    14,
            58,   220,     7,   349,    97,    11,     5,  1461,  2788,     6,
          2128,    45,   479,     2]])

['BERT is a transformers model pretrained on a large corpus of English data in a self-supervised fashion . It was pretrained with two objectives: Masked language modeling (MLM) and next sentence prediction (NSP) The models concatenates two masked sentences as inputs during pretraining . Sometimes they correspond to sentences that were next to each other in the original text, sometimes not .']
```

#### 4.6 NER任务

- 实体词识别（NER）任务是NLP中的基础任务。它用于识别文本中的人名（PER）、地名（LOC）、组织（ORG）以及其他实体（MISC）等。例如：(王 B-PER) (小 I-PER) (明 I-PER) (在 O) (办 B-LOC) (公 I-LOC) (室 I-LOC)。其中O表示一个非实体，B表示一个实体的开始，I表示一个实体块的内部。
- 实体词识别本质上是一个分类任务（又叫序列标注任务），实体词识别是句法分析的基础，而句法分析优势NLP任务的核心。```

```python
# NER任务
def dm06_test_ner():
    # 1 加载tokenizer 加载模型 加载配置文件
    # https://huggingface.co/uer/roberta-base-finetuned-cluener2020-chinese
    my_tokenizer = AutoTokenizer.from_pretrained('roberta-base-finetuned-cluener2020-chinese')
    my_model = AutoModelForTokenClassification.from_pretrained('roberta-base-finetuned-cluener2020-chinese')
    config = AutoConfig.from_pretrained('roberta-base-finetuned-cluener2020-chinese')

    # 2 数据张量化
    inputs = my_tokenizer.encode_plus('我爱北京天安门，天安门上太阳升', return_tensors='pt')
    print('inputs--->', inputs.input_ids.shape, inputs.input_ids) # torch.Size([1, 17])

    # 3 送入模型 预测ner概率 每个字预测的标签概率
    my_model.eval()
    logits = my_model(inputs.input_ids).logits
    print('logits--->', logits.shape)           # torch.Size([1, 17, 32])

    # 4 对预测数据 进行显示
    input_tokens = my_tokenizer.convert_ids_to_tokens(inputs.input_ids[0])
    print('input_tokens--->', input_tokens)
    outputs = []

    for token, value in zip(input_tokens, logits[0]):

        if token in my_tokenizer.all_special_tokens:
            continue

        # 获得每个字预测概率最大的标签索引
        idx = torch.argmax(value).item()

        # 打印索引对应标签
        outputs.append((token, config.id2label[idx]))

    print(outputs)
```

> 程序运行结果

```text
inputs---> torch.Size([1, 17]) tensor([[ 101, 2769, 4263, 1266,  776, 1921, 2128, 7305, 8024, 1921, 2128, 7305,
          677, 1922, 7345, 1285,  102]])

logits---> torch.Size([1, 17, 32])

input_tokens---> ['[CLS]', '我', '爱', '北', '京', '天', '安', '门', '，', '天', '安', '门', '上', '太', '阳', '升', '[SEP]']

[('我', 'O'), ('爱', 'O'), ('北', 'B-address'), ('京', 'I-address'), ('天', 'I-address'), ('安', 'I-address'), ('门', 'I-address'), ('，', 'O'), ('天', 'B-address'), ('安', 'I-address'), ('门', 'I-address'), ('上', 'O'), ('太', 'O'), ('阳', 'O'), ('升', 'O')]
```

### 5 具体模型方式完成NLP任务
#### 5.1 完型填空任务

- 完型填空任务又被叫做“遮蔽语言建模任务”，它属于BERT模型训练过程中的子任务。下面完成一个中文场景的完型填空。

```python
# 具体模型完型填空任务
def dm01_test_bert_fill_mask():

    # 1 加载tokenizer
    modename = "bert-base-chinese"
    my_tokenizer = BertTokenizer.from_pretrained(modename)

    # 2 加载模型
    my_model = BertForMaskedLM.from_pretrained(modename)

    # 3 文本转张量
    input = my_tokenizer.encode_plus('我想明天去[MASK]家吃饭', return_tensors='pt')
    print('input--->', input)

    # 4 给模型送数据提取特征
    output = my_model(**input)
    print('output--->', output)
    print('output.logits--->', output.logits.shape)  # [1,11,21128]

    # 5 取概率最高
    mask_pred_idx = torch.argmax(output.logits[0][6]).item()
    print('打印概率最高的字:', my_tokenizer.convert_ids_to_tokens([mask_pred_idx]))
```

> 程序运行结果

```text
# input_ids表示text2id后结果 # token_type_ids表示句子分段信息 # attention_mask表示句子attention掩码信息
input---> {'input_ids': tensor([[ 101, 2769, 2682, 3209, 1921, 1343,  103, 2157, 1391, 7649,  102]]), 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])}

output---> MaskedLMOutput(loss=None, logits=tensor([[[ -8.1771,  -8.1008,  -8.1191,  ...,  -6.8355,  -6.9482,  -6.9834],
         [ -8.2775,  -8.1251,  -8.1655,  ...,  -6.8471,  -7.4265,  -6.1365],
         [-14.1093, -13.1037, -14.6324,  ...,  -6.0959,  -3.7550,  -5.7456],
         ...,
         [-16.2103, -16.7243, -15.9876,  ...,  -5.9727,  -8.2757,  -7.3852],
         [-13.5615, -13.7670, -13.4497,  ...,  -7.8282,  -4.9095,  -9.1699],
         [-10.3200, -10.1068, -10.4439,  ...,  -6.6468,  -7.0597,  -7.5027]]],
       grad_fn=<AddBackward0>), hidden_states=None, attentions=None)

output.logits---> torch.Size([1, 11, 21128])
```

## 加载和使用预训练模型 old
### 1 加载和使用预训练模型的工具

- 在这里我们使用Transformers工具包进行模型的加载和使用.
- 这些预训练模型由世界先进的NLP研发团队huggingface提供.
- **注意: 下面使用的代码需要国外服务器的资源, 在国内使用的时候, 国内的网站下载可能会出现在原地卡死不动, 或是网络连接超时等一些网络报错, 均是网络问题, 不是代码问题, 这个可以先行跳过, 把主要逻辑梳理完成即可**

### 2 加载和使用预训练模型的步骤

- 第一步: 确定需要加载的预训练模型并安装依赖包.
- 第二步: 加载预训练模型的映射器tokenizer.
- 第三步: 加载带/不带头的预训练模型.
- 第四步: 使用模型获得输出结果.

#### 2.1 确定需要加载的预训练模型并安装依赖包

- 能够加载哪些模型可以参考前一小结中的常用预训练模型
- 这里假设我们处理的是中文文本任务, 需要加载的模型是BERT的中文模型: bert-base-chinese
- 在使用工具加载模型前需要安装必备的依赖包:

```bash
pip install tqdm boto3 requests regex sentencepiece sacremoses
```

#### 2.2 加载预训练模型的映射器tokenizer

```python
import torch
from transformers import AutoTokenizer, AutoModel, AutoModelForMaskedLM, AutoModelForSequenceClassification, AutoModelForQuestionAnswering

mirror='https://mirrors.tuna.tsinghua.edu.cn/help/hugging-face-models/'

def demo24_1_load_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese",mirror='https://mirrors.tuna.tsinghua.edu.cn/help/hugging-face-models/')
    print("tokenizer--->", tokenizer)

demo24_1_load_tokenizer()
```

#### 2.3 加载带/不带头的预训练模型

- 加载预训练模型时我们可以选择带头或者不带头的模型
- 这里的'头'是指模型的任务输出层, 选择加载不带头的模型, 相当于使用模型对输入文本进行特征表示.
- 选择加载带头的模型时, 有三种类型的'头'可供选择, AutoModelForMaskedLM (语言模型头), AutoModelForSequenceClassification (分类模型头), AutoModelForQuestionAnswering (问答模型头)
- 不同类型的'头', 可以使预训练模型输出指定的张量维度. 如使用'分类模型头', 则输出尺寸为(1,2)的张量, 用于进行分类任务判定结果.

```python
# 加载不带头的预训练模型
def demo24_2_load_model():

    # 加载的预训练模型的名字
    model_name = 'bert-base-chinese'

    print('加载不带头的预训练模型')
    model =AutoModel.from_pretrained(model_name)
    print('model--->', model)

    # 加载带有语言模型头的预训练模型
    print('加载带有语言模型头的预训练模型')
    lm_model =AutoModelForMaskedLM.from_pretrained(model_name)
    print('lm_model--->', lm_model)

    # 加载带有分类模型头的预训练模型
    print('加载带有分类模型头的预训练模型')
    classification_model = AutoModelForSequenceClassification.from_pretrained(model_name)
    print('classification_model--->', classification_model)

    # 加载带有问答模型头的预训练模型
    print('加载带有问答模型头的预训练模型')
    qa_model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    print('qa_model--->', qa_model)

demo24_2_load_model()
```

#### 2.4 使用模型获得输出结果
##### 1 使用不带头的模型进行输出

```python
def demo24_3_load_AutoModel():

    # 加载的预训练模型的名字
    model_name = 'bert-base-chinese'

    tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese",mirror=mirror)

    # 2 加载model
    model = AutoModel.from_pretrained(model_name)

    # 3 使用tokenizer 文本数值化
    # 输入的中文文本
    input_text = "人生该如何起头"

    # 使用tokenizer进行数值映射
    indexed_tokens = tokenizer.encode(input_text)

    # 打印映射后的结构
    print("indexed_tokens:", indexed_tokens)

    # 将映射结构转化为张量输送给不带头的预训练模型
    tokens_tensor = torch.tensor([indexed_tokens])

    # 4 使用不带头的预训练模型获得结果
    with torch.no_grad():
        encoded_layers, _ = model(tokens_tensor, return_dict=False)
        # encoded_layers, _ = model(tokens_tensor)

    print("不带头的模型输出结果:", encoded_layers)
    print("不带头的模型输出结果的尺寸:", encoded_layers.shape)

demo24_3_load_AutoModel()
```

> - 输出效果:

```text
# tokenizer映射后的结果, 101和102是起止符,
# 中间的每个数字对应"人生该如何起头"的每个字.
indexed_tokens: [101, 782, 4495, 6421, 1963, 862, 6629, 1928, 102]

不带头的模型输出结果: tensor([[[ 0.5421,  0.4526, -0.0179,  ...,  1.0447, -0.1140,  0.0068],
         [-0.1343,  0.2785,  0.1602,  ..., -0.0345, -0.1646, -0.2186],
         [ 0.9960, -0.5121, -0.6229,  ...,  1.4173,  0.5533, -0.2681],
         ...,
         [ 0.0115,  0.2150, -0.0163,  ...,  0.6445,  0.2452, -0.3749],
         [ 0.8649,  0.4337, -0.1867,  ...,  0.7397, -0.2636,  0.2144],
         [-0.6207,  0.1668,  0.1561,  ...,  1.1218, -0.0985, -0.0937]]])

# 输出尺寸为1x9x768, 即每个字已经使用768维的向量进行了表示,
# 我们可以基于此编码结果进行接下来的自定义操作, 如: 编写自己的微调网络进行最终输出.
不带头的模型输出结果的尺寸: torch.Size([1, 9, 768])
```

##### 2 使用带有语言模型头的模型进行输出

```python
def demo24_4_load_AutoLM():

    # 1 加载 tokenizer
    # 加载的预训练模型的名字
    model_name = 'bert-base-chinese'

    tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese",mirror=mirror)

    # 2 加载model
    lm_model =AutoModelForMaskedLM.from_pretrained(model_name)

    # 3 使用tokenizer 文本数值化
    # 输入的中文文本
    input_text = "人生该如何起头"

    # 使用tokenizer进行数值映射
    indexed_tokens = tokenizer.encode(input_text)

    # 打印映射后的结构
    print("indexed_tokens:", indexed_tokens)

    # 将映射结构转化为张量输送给不带头的预训练模型
    tokens_tensor = torch.tensor([indexed_tokens])

    # 使用带有语言模型头的预训练模型获得结果
    with torch.no_grad():
        lm_output = lm_model(tokens_tensor,return_dict=False)

    print("带语言模型头的模型输出结果:", lm_output)
    print("带语言模型头的模型输出结果的尺寸:", lm_output[0].shape)

demo24_4_load_AutoLM()
```

> - 输出效果:

```text
带语言模型头的模型输出结果: (tensor([[[ -7.9706,  -7.9119,  -7.9317,  ...,  -7.2174,  -7.0263,  -7.3746],
         [ -8.2097,  -8.1810,  -8.0645,  ...,  -7.2349,  -6.9283,  -6.9856],
         [-13.7458, -13.5978, -12.6076,  ...,  -7.6817,  -9.5642, -11.9928],
         ...,
         [ -9.0928,  -8.6857,  -8.4648,  ...,  -8.2368,  -7.5684, -10.2419],
         [ -8.9458,  -8.5784,  -8.6325,  ...,  -7.0547,  -5.3288,  -7.8077],
         [ -8.4154,  -8.5217,  -8.5379,  ...,  -6.7102,  -5.9782,  -7.6909]]]),)

# 输出尺寸为1x9x21128, 即每个字已经使用21128维的向量进行了表示,
# 同不带头的模型一样, 我们可以基于此编码结果进行接下来的自定义操作, 如: 编写自己的微调网络进行最终输出.
带语言模型头的模型输出结果的尺寸: torch.Size([1, 9, 21128])
```

##### 3 使用带有分类模型头的模型进行输出

```python
def demo24_5_load_AutoSeqC():

    # 1 加载 tokenizer
    # 加载的预训练模型的名字
    model_name = 'bert-base-chinese'

    tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese",mirror=mirror)

    # 2 加载model
    classification_model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # 3 使用tokenizer 文本数值化
    # 输入的中文文本
    input_text = "人生该如何起头"

    # 使用tokenizer进行数值映射
    indexed_tokens = tokenizer.encode(input_text)

    # 打印映射后的结构
    print("indexed_tokens:", indexed_tokens)

    # 将映射结构转化为张量输送给不带头的预训练模型
    tokens_tensor = torch.tensor([indexed_tokens])

    # 使用带有分类模型头的预训练模型获得结果
    with torch.no_grad():
        classification_output = classification_model(tokens_tensor)

    print("带分类模型头的模型输出结果:", classification_output)
    print("带分类模型头的模型输出结果的尺寸:", classification_output[0].shape)

demo24_5_load_AutoSeqC()
```

> - 输出效果:

```text
带分类模型头的模型输出结果: (tensor([[-0.0649, -0.1593]]),)
# 输出尺寸为1x2, 可直接用于文本二分问题的输出
带分类模型头的模型输出结果的尺寸: torch.Size([1, 2])
```

##### 4 使用带有问答模型头的模型进行输出

```python
def demo24_6_load_AutoQA():

    # 1 加载 tokenizer
    # 加载的预训练模型的名字
    model_name = 'bert-base-chinese'
    tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese",mirror=mirror)

    # 2 加载model
    qa_model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    # 3 使用
    # 使用带有问答模型头的模型进行输出时, 需要使输入的形式为句子对
    # 第一条句子是对客观事物的陈述
    # 第二条句子是针对第一条句子提出的问题
    # 问答模型最终将得到两个张量,
    # 每个张量中最大值对应索引的分别代表答案的在文本中的起始位置和终止位置
    input_text1 = "我家的小狗是黑色的"
    input_text2 = "我家的小狗是什么颜色的呢?"

    # 映射两个句子
    indexed_tokens = tokenizer.encode(input_text1, input_text2)
    print("句子对的indexed_tokens:", indexed_tokens)

    # 输出结果: [101, 2769, 2157, 4638, 2207, 4318, 3221, 7946, 5682, 4638, 102, 2769, 2157, 4638, 2207, 4318, 3221, 784, 720, 7582, 5682, 4638, 1450, 136, 102]
    #
    # 用0，1来区分第一条和第二条句子
    segments_ids = [0] * 11 + [1] * 14

    # 转化张量形式
    segments_tensors = torch.tensor([segments_ids])
    tokens_tensor = torch.tensor([indexed_tokens])

    # 使用带有问答模型头的预训练模型获得结果
    with torch.no_grad():
        start_logits, end_logits = qa_model(tokens_tensor, token_type_ids=segments_tensors, return_dict=False)

    print("带问答模型头的模型输出结果:", (start_logits, end_logits))
    print("带问答模型头的模型输出结果的尺寸:", (start_logits.shape, end_logits.shape))  # (torch.Size([1, 25]), torch.Size([1, 25]))

demo24_6_load_AutoQA()
```

> - 输出效果:

```text
句子对的indexed_tokens: [101, 2769, 2157, 4638, 2207, 4318, 3221, 7946, 5682, 4638, 102, 2769, 2157, 4638, 2207, 4318, 3221, 784, 720, 7582, 5682, 4638, 1450, 136, 102]

带问答模型头的模型输出结果: (tensor([[ 0.2574, -0.0293, -0.8337, -0.5135, -0.3645, -0.2216, -0.1625, -0.2768,
         -0.8368, -0.2581,  0.0131, -0.1736, -0.5908, -0.4104, -0.2155, -0.0307,
         -0.1639, -0.2691, -0.4640, -0.1696, -0.4943, -0.0976, -0.6693,  0.2426,
          0.0131]]), tensor([[-0.3788, -0.2393, -0.5264, -0.4911, -0.7277, -0.5425, -0.6280, -0.9800,
         -0.6109, -0.2379, -0.0042, -0.2309, -0.4894, -0.5438, -0.6717, -0.5371,
         -0.1701,  0.0826,  0.1411, -0.1180, -0.4732, -0.1541,  0.2543,  0.2163,
         -0.0042]]))

# 输出为两个形状1x25的张量, 他们是两条句子合并长度的概率分布,
# 第一个张量中最大值所在的索引代表答案出现的起始索引,
# 第二个张量中最大值所在的索引代表答案出现的终止索引.
带问答模型头的模型输出结果的尺寸: (torch.Size([1, 25]), torch.Size([1, 25]))
```

## huggingface平台使用指南 old
### 1 huggingface介绍

Huggingface总部位于纽约，是一家专注于自然语言处理、人工智能和分布式系统的创业公司。他们所提供的聊天机器人技术一直颇受欢迎，但更出名的是他们在NLP开源社区上的贡献。Huggingface一直致力于自然语言处理NLP技术的平民化(democratize)，希望每个人都能用上最先进(SOTA, state-of-the-art)的NLP技术，而非困窘于训练资源的匮乏。同时Hugging Face专注于NLP技术，拥有大型的开源社区。尤其是在github上开源的自然语言处理，预训练模型库 Transformers，已被下载超过一百万次，github上超过24000个star。Transformers 提供了NLP领域大量state-of-art的 预训练语言模型结构的模型和调用框架。

### 2 使用步骤

- 第一步: 在https://huggingface.co/join上创建一个帐户
- 第二步: 在可视化界面登陆用户
- 第三步: 在huggingface上创建模型仓库
- 第四步: 通过git把本地模型，上传到HuggingFace平台的模型仓库中
- 第五步: 通过git clone进行模型下载
- 第六步: 加载下载的模型

#### 2.1 创建一个帐户

在 [https://huggingface.co/join](https://huggingface.co/join) 上创建一个帐户

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000137.png]]

#### 2.2 登录

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000138.png]]

#### 2.3 在huggingface上创建模型仓库

- 在huggingFace平台上注册完毕后，会弹出欢迎页面： [https://huggingface.co/welcome](https://huggingface.co/welcome) 该页面显示了详细的上传模型，下载模型的方法。
- 详细如下：

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000139.png]]

- 通过界面在huggingface上创建模型仓库
- 点击个人头像，点击创建模型命令【new Mode】

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000140.png]]

- 输入【自己名称】、【模型名称】

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000141.png]]

- 显示自己创建的模型

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000142.png]]

#### 2.4 上传本地模型到平台

通过git把本地模型，上传到HuggingFace平台的模型仓库中

##### 1 页面发布步骤介绍

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000143.png]]

##### 2 git clone操作

先通过git clone操作把huggingface服务器上的文件目录给“拉”下来在本地路径下，执行如下命令：

```text
# xxx/mymodel04 --> 这个是你在huggingface上创建的代码仓库, 根据自己的情况适当更换一下.
git clone https://huggingface.co/xxx/mymodel04
```

注意点:

- 在本地会出现一个mymodel04文件夹
- 在执行git clone之前确保本地文件夹是否已经存在mymodel04，避免本地文件被覆盖。或者把已经存在的mymodel04目录修改名字.

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000144.png]]

##### 3 把我们要上传的模型文件copy到本地mymodel04文件夹中

- 先将目录先切换至mymodel04文件夹中

```bash
cd mymodel04
```

- 根据目录结构，选中把bert_finetuning_test目录下的模型文件上传到huggingFace平台，需要把bert_finetuning_test目录下的模型文件，copy到mymodel04目录下。

```text
cp -r /root/transformers/examples/pytorch/text-classification/bert-base-uncased-finetuning  .
```

##### 4 上传本地mymodel04文件夹中的模型文件，到服务器mymodel04中

```text
git add .       # 把本地待上传的模型文件与hugging平台建立关联
git commit -m "commit from $USER" # 添加评注
git push    # 向huggingface平台上传模型文件
```

注意点: git push 向服务器上传模型文件，需要两次输入密码

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000145.png]]

##### 5 确认模型是否已经上传到HuggingFace平台上

![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-工具与框架（Tools and Frameworks）/05-Hugging Face Transformers（Hugging Face Transformers）/05-Hugging Face Transformers（Hugging Face Transformers）-20260813120000146.png]]

#### 2.5 通过git clone进行模型下载

```text
git clone https://huggingface.co/xxx/mymodel4
```

#### 2.6 加载下载的模型

```python
import torch
from transformers import AutoModel, AutoTokenizer

# 网络加载
tokenizer = AutoTokenizer.from_pretrained('xxx/mymodel4')
model = AutoModel.from_pretrained('xxx/mymodel4')

index = tokenizer.encode("Talk is cheap", "Please show me your code!")
# 102是bert模型中的间隔(结束)符号的数值映射
mark = 102

# 找到第一个102的索引, 即句子对的间隔符号
k = index.index(mark)

# 句子对分割id列表, 由0，1组成, 0的位置代表第一个句子, 1的位置代表第二个句子
segments_ids = [0]*(k + 1) + [1]*(len(index) - k - 1)
# 转化为tensor
tokens_tensor = torch.tensor([index])
segments_tensors = torch.tensor([segments_ids])

# 使用评估模式
with torch.no_grad():
    # 使用模型预测获得结果
    result = model(tokens_tensor, token_type_ids=segments_tensors)
    # 打印预测结果以及张量尺寸
    print(result)
    print(result[0].shape)
```

> - 输出效果:

```text
(tensor([[[-0.1591,  0.0816,  0.4366,  ...,  0.0307, -0.0419,  0.3326],
         [-0.3387, -0.0445,  0.9261,  ..., -0.0232, -0.0023,  0.2407],
         [-0.0427, -0.1688,  0.5533,  ..., -0.1092,  0.1071,  0.4287],
         ...,
         [-0.1800, -0.3889, -0.1001,  ..., -0.1369,  0.0469,  0.9429],
         [-0.2970, -0.0023,  0.1976,  ...,  0.3776, -0.0069,  0.2029],
         [ 0.7061,  0.0102, -0.4738,  ...,  0.2246, -0.7604, -0.2503]]]), tensor([[-3.5925e-01,  2.0294e-02, -2.3487e-01,  4.5763e-01, -6.1821e-02,
          2.4697e-02,  3.8172e-01, -1.8212e-01,  3.4533e-01, -9.7177e-01,
          1.1063e-01,  7.8944e-02,  8.2582e-01,  1.9020e-01,  6.5513e-01,
         -1.8114e-01,  3.9617e-02, -5.6230e-02,  1.5207e-01, -3.2552e-01,
          ...
          1.4417e-01,  3.0337e-01, -6.6146e-01, -9.6959e-02,  8.9790e-02,
          1.2345e-01, -5.9831e-02,  2.2399e-01,  8.2549e-02,  6.7749e-01,
          1.4473e-01,  5.4490e-01,  5.9272e-01,  3.4453e-01, -8.9982e-02,
         -1.2631e-01, -1.9465e-01,  6.5992e-01]]))
torch.Size([1, 12, 768])
```
