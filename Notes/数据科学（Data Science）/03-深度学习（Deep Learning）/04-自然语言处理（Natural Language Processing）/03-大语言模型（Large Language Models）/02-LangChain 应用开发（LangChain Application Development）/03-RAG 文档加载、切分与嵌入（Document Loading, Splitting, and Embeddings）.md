---
title: "RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）"
tags:
  - data-science/deep-learning/nlp/llm/LangChain
status: published
created: 2026-09-07
published_at: 2026-09-07
source_document_version: V1.0.2
target_framework_line: LangChain 1.1.x
---
# RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）
## 检索增强生成（Retrieval-Augmented Generation, RAG）
## RAG 概述
### 大语言模型的局限（LLM Limitations）
#### 知识滞后
LLM 因其具有海量参数，需要花费相当的物力与时间成本进行预训练和微调，同时商用 LLM 还需要进行各种安全测试与风险评估等。因此 LLM 会存在知识滞后的问题。
#### 知识缺失
在专有领域，LLM 无法学习到所有的专业知识细节，因此在面向专业领域知识的提问时，无法给出可靠准确的回答。
#### 幻觉
LLM 在生成回答时，可能会“胡言乱语”，这种现象称之为 LLM 的“幻觉”。“幻觉”可以体现为错误陈述、编造事实、错误的复杂推理或者复杂语境下理解能力不足等。
“幻觉”产生的原因：
- 训练数据存在偏差或错误，模型可能在输出中复现这些问题。
- 模型发生过度泛化，把常见模式误用到特定场景。
- LLM 本身没有真正学习到训练数据中深层次的含义，导致在一些需要深入理解或复杂推理的任务中出错
- LLM 缺乏某些领域的相关知识，在面临这些领域的相关问题时编造不存在的信息
- 大模型生成内容的不可控，尤其是在金融和医疗领域等领域，一次金额评估的错误，一次医疗诊断的失误，哪怕只出现一次都是致命的。但这些错误对于非专业人士来说难以辨识。目前还没有能够百分之百解决这种情况的方案。
### 什么是 RAG
为了改善大模型在时效性、可靠性与准确性方面的不足，各种针对 LLM 优化的方法应运而生。RAG（Retrieval-Augmented Generation，检索增强生成）就是其中一种被广泛研究和应用的优化架构。
RAG 的基本思想为：将传统的生成式大模型和实时信息检索技术相结合，为大模型补充来自外部的相关数据和上下文，来帮助大模型生成更加准确可靠的内容。这使得大模型在生成内容时可以依赖实时与个性化的数据和知识，而非仅仅依赖训练知识。就相当于在大模型回答时给它一本参考书。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）-20260907112000010.png]]
可以说，当应用需求集中在利用大模型去回答特定私有领域的知识，且知识库足够大时，那么除了微调大模型外，RAG 就是非常有效的一种解决方案。LangChain 对这一流程提供了解决方案。
### RAG 的优缺点（Advantages and Limitations）
#### RAG的优点
- 相比提示词工程，RAG 有更丰富的上下文和数据样本，可以不需要用户提供过多的背景描述，就能生成比较符合用户预期的答案。
- 相比于模型微调，RAG 可以提升问答内容的时效性和可靠性。
- 私有数据可以留在自管检索系统中，但检索片段仍可能被发送给外部模型；RAG 本身不自动保证隐私，仍需访问控制、脱敏、传输加密和日志治理。
#### RAG的缺点
- 由于每次问答都涉及外部系统数据检索，因此 RAG 的响应时延相对较高。
- 引用的外部知识数据会消耗大量的模型 Token 资源。
### RAG 流程（RAG Pipeline）
典型 RAG 包含两个主要流程：
- **索引（Indexing）**：从数据源提取数据并构建可检索索引。
- **检索与生成（Retrieval and Generation）**：接收查询、检索相关数据，再把查询和检索结果交给模型生成回答。
索引阶段通常包括：
1. 从数据源加载数据。
2. 将文档切分为文本块（Chunk）。
3. 对文本块生成嵌入向量（Embedding）。
4. 保存文本、元数据与向量索引。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）-20260907112000011.png]]
检索生成阶段通常包括：
1. 对用户查询进行处理和向量化。
2. 使用检索器查找相关文本块，必要时过滤和重排序。
3. 把问题、检索证据和回答约束组合成提示词。
4. 由 LLM 生成答案，并按需要返回引用。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）-20260907112000010.png]]
> [!tip] 大白话解释（Intuition）
> 索引阶段像提前把厚书拆成卡片并做好目录；提问时先从目录里找最相关的几张卡片，再让模型只参考这些卡片作答。检索错了，后面的生成通常也会跟着错，因此 RAG 的质量上限不只由 LLM 决定。
## 文档加载（Document Loading）
数据源可能包含多种格式的文件，如文本文档、Markdown，PDF 等。因此我们首先需要对各种格式的文件进行处理。LangChain 实现和集成了众多文档加载器，方便从不同格式的文件中加载数据。可在 https://docs.langchain.com/oss/python/integrations/document_loaders 查看所有集成的文档加载器。
LangChain 所有文档加载器都实现了 BaseLoader 接口，接口提供了通用的 load（一次加载所有文档） 与 lazy_load（以延迟方式加载文档） 方法，用于从数据源加载数据并处理为 Document 对象。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）-20260907112000012.png]]
LangChain 实现了 Document 抽象，用于表示文本单元及其元数据，它包含三个属性：
- page_content：文本内容字符串。
- metadata：包含元数据的字典，如文档的来源等。
- id：可选，文档标识符。
下面通过Markdown和Docx以及PDF作为例子，来了解下如何对文件进行相关加载和解析。
### 加载 Markdown
MarkDown形式一种半结构化的数据，其原始文本，通过特定语法，标记出了标题、段落、有序列表、无序列表等相关信息，
如下所示，不同的层级的文本，在markdown当中表示的形式不一致：
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）-20260907112000013.png]]
可以使用 Unstructured 文档加载器来加载多种类型的文件，关于如何在 LangChain 中使用 unstructured 生态系统，可参考这里。
Unstructured.io对Markdown的解析流程，如下所示：
##### 按照Markdown结构进行切分，标题等会被切分成单独的element
##### 对于同一个标题下的文本，再按照段落进行切分，不同的段落（通过\n标识）会被切分成多个element。
可使用 langchain集成的UnstructuredMarkdownLoader 来加载 Markdown 文件，示例代码如下所示：
```python
#pip install markdown langchain_community unstructured[md]
def markdown_loader_demo():
    from langchain_community.document_loaders import UnstructuredMarkdownLoader
    loader = UnstructuredMarkdownLoader("./assets/sample.md",encoding="utf-8",mode="elements")
    docs = loader.load()
    for doc in docs:
        print(doc.page_content,end="\n============\n")

if __name__ == "__main__":
    markdown_loader_demo()
```
### 加载 Word 文档（DOCX）
现代的 Word 文档（.docx 格式）本质上也是一种半结构化（Semi-structured）且机器可读（Machine-readable）的文件。
.docx 的本质上是XML 的容器，XML 标签严格规定了文档的层级（比如 <w:p> 代表段落，<w:r> 代表文本运行块）。机器可以利用这些标签精确地提取信息。
但是，由于Word文档对于层级的定义相较于Markdown又更加灵活，我们可以自定义不同层级标题的样式，而这些样式通常只是正文样式，加了手动格式，使得解析库无法按照统一的标准格式将层级进行解析，这个特点给Word解析又带来了难点。
可以使用 LangChain 集成的 Unstructured 加载器解析 `.docx`。`mode="elements"` 会尝试按元素返回内容，但能否可靠识别标题取决于文档是否使用标准标题样式、解析器版本与文档结构；仅靠字号或手工加粗形成的“视觉标题”可能无法恢复为正确层级。
```python
# pip install unstructured[docx]
def word_loader_demo():
    from langchain_community.document_loaders import UnstructuredWordDocumentLoader
    docs = UnstructuredWordDocumentLoader(
        # 文件路径
        file_path="assets/sample.docx",
        # 加载模式:
        #   single 返回单个Document对象
        #   elements 按标题等元素切分文档
        mode="elements",
    ).load()

    for doc in docs[230:260]: # 从文档中间选取30个文档查看结构
        print(doc.page_content)
        print(doc.metadata,end="\n============\n")

if __name__ == "__main__":
    word_loader_demo()
```
对于标题层级信息并不敏感的.docx文件，可以通过上面的loader进行加载。但是，对于标题层级信息敏感的.docx文件，上面的方式，会丢失掉标题层级信息，此时可以通过下面所讲到的Mineru进行处理。
### 加载 PDF
PDF 存在多种来源格式，包括扫描版（图片 PDF）、电子文本版、混合版。并且布局格式也多种多样，包括单列布局、双列布局甚至竖排文本布局。并且包含段落、标题、页眉页脚、表格、数学公式、化学式、特殊符号、图片等各种元素。
因此，PDF 解析存在很多挑战。对于复杂 PDF，需要进行文本提取、布局检测、表格解析、公式识别等处理。
在此处，我们介绍一个开源的，专门用于解析PDF的工具：Mineru。
MinerU是一款将PDF转化为机器可读格式的工具（如markdown、json），可以很方便地抽取为任意格式。
Mineru可以配置使用VLM模型进行文档解析。其开源的opendatalab/MinerU2.5-2509-1.2B(https://huggingface.co/opendatalab/MinerU2.5-2509-1.2B)模型，在各项基础测试当中，都达到了SOTA水平。
下图展示了MinerU2-VLM在多项基准测试当中得分排名：
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）-20260907112000014.jpeg]]
MinerU2.5采用两阶段解析策略：首先对下采样图像进行高效的全局布局分析，然后对文本、公式和表格的原生分辨率裁剪图像进行细粒度内容识别。在大规模、多样化的数据引擎支持下进行预训练和微调，MinerU2.5 在多个基准测试中始终优于通用模型和特定领域模型，同时保持较低的计算开销。MinerU 提供了 PDF、Word、PPT、图片等文件的解析，支持图像提取、OCR、公式、表格解析等功能。
另外，Mineru开源所有代码，支持本地通过Docker方式进行部署，其项目仓库链接：https://github.com/opendatalab/MinerU。Mineru官网也提供了直接调用API的方式，上传文件进行解析。首先需要在官网申请API_KEY，并将其放到环境变量当中
调用上传文件接口示例代码如下：
```python
def mineru_upload_file_demo():
    import requests
    import os
    token = os.getenv("MINERU_TOKEN")
    url = "https://mineru.net/api/v4/file-urls/batch"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
    "files": [
        {"name":"demo.pdf", "data_id": "abcd"}
    ],
    "model_version":"vlm"
    }
    file_path = ["assets/demo.pdf"]
    try:
        response = requests.post(url,headers=header,json=data)
        if response.status_code == 200:
            result = response.json()
            print('上传成功:{}'.format(result))
            batch_id = result['data']['batch_id']
            if result["code"] == 0:
                batch_id = result["data"]["batch_id"]
                urls = result["data"]["file_urls"]
                print('batch_id:{},urls:{}'.format(batch_id, urls))
                for i in range(0, len(urls)):
                    with open(file_path[i], 'rb') as f:
                        res_upload = requests.put(urls[i], data=f)
                        if res_upload.status_code == 200:
                            print(f"{urls[i]} 上传成功")
                        else:
                            print(f"{urls[i]} 上传失败")
            else:
                print('申请上传地址失败：{}'.format(result.get("msg", "未知错误")))
            return batch_id
        else:
            print(f"请求失败，状态码：{response.status_code}，响应内容：{response.text}")
    except Exception as err:
        print(err)
```
上传完成之后，可以通过获取任务结果API来获取解析结果：
```python
def mineru_check_result_demo(batch_id):
    import requests
    import time
    token = os.getenv("MINERU_TOKEN")
    url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    res = requests.get(url, headers=header)
    while res.json()["data"]['extract_result'][0]['state'] != 'done':
        print('当前状态为running，等待3秒后重试')
        time.sleep(3)
        res = requests.get(url, headers=header)
        print(res.status_code)
        print(res.json()["data"]['extract_result'][0]['state'],end="\n\n=========\n\n")
    print('提取结果为:',res.json()["data"]['extract_result'][0]['full_zip_url'])
```
Mineru解析之后，有多种不同的输出格式，具体可参见Mineru官方文档：https://opendatalab.github.io/MinerU/zh/reference/output_files/。
要进行下一步处理，最简单的方式是通过解析之后得到的一个MarkDown文件，再利用MarkDown解析器，进行进一步的解析即可。
## 文档切分（Document Splitting）
### 为什么需要切分（Why Split Documents）
获取 Document 对象后，需要将其切分成 Chunk。之所以要进行切分是出于以下考虑：
##### 后续需要根据提问检索出相关的内容放入 Prompt，如果答案出现在某一个 Document 对象中，那么将检索到的整个 Document 对象直接放入 Prompt 中并不是最优的选择，因为 Document 可能包含非常多无关的信息，这些无效信息会干扰大模型的生成。有研究发现，尽管大模型能够处理长文本输入，但它们在利用长上下文方面存在显著不足。尤其是在多文档问答和键值检索等任务中，当相关信息位于输入文本的中间时，模型的性能显著下降。这种现象表明，当前的语言模型在长输入上下文中未能充分利用信息，尤其是位于中间部分的信息。
##### 大模型存在最大输入的 Token 限制，如果一个 Document 非常大，在输入大模型时会被截断，导致信息缺失。
基于此，一个方法是将完整的 Document 进行分块处理（Chunking），将 Document 切分为一个个小块（Chunk）。无论是在存储还是检索过程中，都将以这些块为基本单位，这样能有效地避免内容噪声干扰和超出最大 Token 的问题。
### 切分策略（Splitting Strategies）
具体切分时，可以采用如下策略，具体采用哪种，主要取决于在实际使用场景当中，对于语义连贯性，完整性的要求：
- **固定长度切分（Fixed-size Splitting）**：按字符数或 Token 数切分，速度快且块大小稳定，但可能在不合适的位置截断句子。
- **递归字符切分（Recursive Character Splitting）**：依次尝试段落、换行、空格、标点等分隔符，尽量保持较大的自然语言单元；当没有合适分隔符且文本仍过长时仍可能退化为更细粒度切分，因此不能保证永远不截断句子。
- **语义切分（Semantic Splitting）**：把相邻句子组成句组，对句组生成嵌入并比较相邻距离，在语义变化超过阈值的位置切分，再按需要合并过短片段。它更重视语义完整性，但计算更慢，块长也可能不均衡。
接下来，我们介绍这三种切分策略当中在保持语义连贯性上面的折中方案：按照特定字符进行切分，langchain为我们提供了一个现成的类：RecursiveCharacterTextSplitter.
### 递归字符切分器（RecursiveCharacterTextSplitter）
RecursiveCharacterTextSplitter（递归字符文本切分器）是最常用的切分器，它由一个字符列表作为参数，默认列表为 ["\n\n", "\n", " ", ""]，并且会尝试按顺序使用这些字符进行切分，直到块足够小。由此尽可能地将所有段落（然后是句子，最后是词）保持在一起，因为这些段落通常看起来是语义上最相关的文本片段。
同时为了保证段之间语义完整，可以设置每个块之间有一部分重叠。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）-20260907112000015.png]]
> [!tip] 大白话解释（Intuition）
> `RecursiveCharacterTextSplitter` 会先尝试按“大缝隙”切，例如段落；块仍太大才改用换行、标点甚至单个字符。`chunk_overlap` 像复印相邻页时多带几行，减少答案恰好被切在边界上的风险，但重叠越多，存储和检索重复也越多。
举例：
```python
# pip install langchain-text-splitters
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredWordDocumentLoader

# 加载文档
docs = UnstructuredWordDocumentLoader(
    file_path="assets/sample.docx", mode="single"
).load()

# 切分为文本块
chunks = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "！", "？", "……", "，", ""],  # 分隔符列表
    chunk_size=400,  # 每个块的最大长度
    chunk_overlap=50,  # 每个块重叠的长度
    length_function=len,  # 可选：计算文本长度的函数，默认为字符串长度，可自定义函数来实现按 token 数切分
    add_start_index=True,  # 可选：块的元数据中添加此块起始索引
).split_documents(docs)

print(chunks)
```
整个切分过程可以通过如下流程图所示：
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）-20260907112000016.svg]]
## 文档嵌入（Document Embeddings）
### 嵌入模型（Embedding Models）
将文档切分成合适的大小之后，就可以使用嵌入模型生成文档的嵌入向量，后续检索时用于与查询的嵌入向量进行相似度计算。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）/03-RAG 文档加载、切分与嵌入（Document Loading, Splitting, and Embeddings）-20260907112000017.png]]
2018年谷歌推出的 BERT 能够将文本嵌入为简单的向量表示，但是 BERT 并未针对有效生成句子嵌入进行优化，由此促使了 Sentence-BERT 的诞生。Sentence-BERT（论文链接：https://arxiv.org/pdf/1908.10084） 调整了 BERT 的架构以及预训练任务以生成包含语义的句子嵌入向量，这些嵌入向量可以通过余弦相似度等相似性指标轻松进行比较，大大降低了查找相似句子等任务的计算开销。
常用嵌入模型：

|模型|机构|描述|
|---|---|---|
|bge-large-zh|北京智源研究院（BAAI）|开源，向量维度1024，序列长度512|
|bge-base-zh|BAAI|开源，向量维度768，序列长度512|
|bge-small-zh|BAAI|开源，向量维度512，序列长度512|
|bge-m3|BAAI|开源，多语言，向量维度1024，序列长度8192|
|text-embedding-3-small|OpenAI|多语言，向量维度1536，序列长度8192|
|text-embedding-3-large|OpenAI|多语言，向量维度3072，序列长度8192|
### 通过 LangChain 完成文档嵌入
LangChain 定义了嵌入（Embeddings）接口，核心方法包括批量嵌入文档与嵌入单个查询。下面用等价的最小抽象类展示接口形状：
```python
from abc import ABC, abstractmethod

class Embeddings(ABC):
    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed search docs.

        Args:
            texts: List of text to embed.

        Returns:
            List of embeddings.
        """

    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        """Embed query text.

        Args:
            text: Text to embed.

        Returns:
            Embedding.
        """
```
该Embedding的具体实现类有：HuggingFaceEmbeddings，OpenAIEmbeddings等。
要使用 Hugging Face 开源模型生成文本嵌入，可以通过 `HuggingFaceEmbeddings` 实例加载本地或远端模型。下面假设模型已经放在项目的 `assets/models/` 中：
```python
# pip install sentence-transformers langchain_huggingface
def embedding_demo():

    from langchain_huggingface import HuggingFaceEmbeddings
    embed_model = HuggingFaceEmbeddings(
        model_name=r'.\assets\models\bge-base-zh-v1.5'
    )

    # 单文本嵌入
    query = "你好，世界"
    query_result = embed_model.embed_query(query)
    print(len(query_result))
    print(query_result[0:10])

    # 多文本嵌入
    docs = ["你好，世界", "你好，世界"]
    res = embed_model.embed_documents(docs)
    print(type(res))

if __name__ == "__main__":
    embedding_demo()
```
