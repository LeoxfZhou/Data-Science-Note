---
title: "Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）"
tags:
  - data-science/deep-learning/nlp/llm/LangChain
status: published
created: 2026-09-07
published_at: 2026-09-07
source_document_version: V1.0.2
target_framework_line: LangChain 1.1.x
---
# Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）
## 向量存储与检索（Vector Storage and Retrieval）
### 向量数据库（Vector Database）
假设你是一名摄影师，拍了大量的照片。为了方便管理和查找，你决定将这些照片存储到一个数据库中。传统的关系型数据库（如 MySQL、PostgreSQL 等）可以帮助你存储照片的元数据，比如拍摄时间、地点、相机型号等。
但是，当你想要根据照片的内容（如颜色、纹理、物体等）进行搜索时，传统数据库可能无法满足你的需求，因为它们通常以数据表的形式存储数据，并使用查询语句进行精确搜索。那么此时，向量数据库就可以派上用场。
我们可以构建一个多维的空间使得每张照片特征都存在于这个空间内，并用已有的维度进行表示，比如时间、地点、相机型号、颜色….此照片的信息将作为一个点，存储于其中。以此类推，即可在该空间中构建出无数的点，而后我们将这些点与空间坐标轴的原点相连接，就成为了一条条向量，当这些点变为向量之后，即可利用向量的计算进一步获取更多的信息。当要进行照片的检索时，也会变得更容易更快捷。
注意，在向量数据库中进行检索时，并不是检索唯一的匹配结果，而是查询和目标向量最为相似的一些向量，具有模糊性。
延伸思考一下，只要对图片、视频、商品等素材进行向量化，就可以实现以图搜图、视频相关推荐、相似商品推荐等功能。
> [!tip] 大白话解释（Intuition）
> 关系型数据库擅长回答“编号等于 42 的记录在哪”，向量数据库擅长回答“哪几条记录和这个问题最像”。它保存的不只是原文，还保存模型生成的坐标；查询时比较坐标距离，因此返回的是相似候选而不是唯一精确答案。
### 常用向量数据库（Common Vector Databases）
LangChain提供了众多向量存储的集成，包括开源的本地向量存储与云托管的私有向量存储。并公开了一个标准接口，可以轻松地在向量存储之间进行交换。
常用向量数据库：

|向量数据库|描述|
|---|---|
|FAISS|一个用于高效相似性搜索和密集向量聚类的库|
|Chroma|开源的轻量级向量数据库，有极简的 API|
|Milvus|开源的专为向量搜索设计的云原生数据库。性能强悍，功能丰富。覆盖轻量级的原型开发到十亿级向量的大规模生产系统|
|Pgvector|开源关系型数据库 PostgreSQL 的扩展，为PostgreSQL增加了向量数据类型和相似性搜索功能|
|Redis|开源内存数据结构存储，现已原生支持向量相似性搜索功能|
|Elasticsearch|开源分布式搜索和分析引擎，提供了一个基于文档的数据库，结构化、非结构化和向量数据通过高效的列式存储统一管理|
这里我们使用 Milvus 作为向量存储。
### Milvus 介绍与部署
#### Milvus 架构（Milvus Architecture）
Milvus因其强大的性能（可支持数百亿级别的向量存储和检索），以及可扩缩容等相关特点，在实际生产环境下，使用非常普遍。
Milvus的架构如下图所示：
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）-20260907112000018.png]]
Milvus 的组件解耦良好，其中三个最关键的任务 —— 搜索、数据插入以及索引 / 压缩 —— 被设计为易于并行化的进程，复杂逻辑被分离出来。这确保了相应的查询节点、数据节点和索引节点能够独立地进行纵向和横向扩展，从而优化性能和成本效率。
#### 集合与数据类型（Collection and Data Types）
Milvus 通过 数据库—Collections—实体 的结构管理数据。Collections 和实体就类似关系型数据库中的表和记录。具体来说，Collection 是一个二维表，具有固定的列和变化的行。每列代表一个字段，每行代表一个实体。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）-20260907112000019.png]]
Collection 通过 Collection Schema 来定义有哪些字段以及字段的类型、索引等。
以下是Milvus所支持的数据类型：

|类别|表示形式|Milvus 类型|描述|
|---|---|---|---|
|向量字段|密集向量|FLOAT_VECTOR|32位浮点数列表|
|向量字段|密集向量|FLOAT16_VECTOR|16位半精度浮点数列表|
|向量字段|密集向量|BFLOAT16_VECTOR|16位浮点数列表，精度稍低，但指数范围与 Float32 相同|
|向量字段|密集向量|INT8_VECTOR|8位有符号整数向量|
|向量字段|稀疏向量|SPARSE_FLOAT_VECTOR|非零数字及其序列号列表|
|向量字段|二进制向量|BINARY_VECTOR|一个0和1的列表|
|标量字段|标量字段|VARCHAR|字符串|
|标量字段|标量字段|BOOL|存储true或false|
|标量字段|标量字段|INT|INT8、INT16、INT32、INT64|
|标量字段|标量字段|FLOAT|32位浮点数|
|标量字段|标量字段|DOUBLE|64位双精度浮点数|
|标量字段|标量字段|ARRAY|相同数据类型元素的有序集合|
|标量字段|标量字段|JSON|结构化的键值数据|
一个 Collection Schema 有一个主键、一个或多个向量字段以及若干标量字段。Milvus 版本和服务端配置会限制向量字段数量：常见默认上限是 4，可通过服务端配置提高，不能把固定数字当作所有部署的永久限制。主键用于唯一标识实体，只接受 `INT64` 或 `VARCHAR`。若创建 Collection 时启用 `auto_id=True`，插入数据时不应再提供主键值。
向量字段是最重要的字段，可以分为稠密向量或者是稀疏向量。
稠密向量通常由基于 Transformer Encoder 架构的深度学习模型（如 Sentence-BERT）生成。
稀疏向量用于表示文本中的关键词及其对应权重，其构建方式经历了从早期基于 TF-IDF 等统计方法的传统词袋模型，到如今基于深度学习模型的学习式构建方法的发展演进。
使用深度学习模型构建稀疏向量的原理如下图所示（分词过程和稠密向量生成当中类似）：
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）-20260907112000020.png]]
通过深度学习模型生成一个稀疏向量时，不再“只看一句话的总体意思”，而是让模型推理：这句话里哪些词重要、重要到什么程度，并把这些重要词单独拎出来加权表示。
下面以BGE-M3为例，来展示稠密向量和稀疏向量的不同：
```python
# pip install FlagEmbedding==1.3.5
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel(model_name_or_path="assets/models/bge-m3")

res = model.encode(["标量字段通常用来存储一些元数据，并可以在搜索时通过元数据进行过滤"],return_sparse=True,return_dense=True)
print('encode结果为：',res,end='\n\n')
# 1、打印稀疏向量
print('稀疏向量为：',res["lexical_weights"],end='\n\n')
# 2、将稀疏向量当中的id转换为token，并打印
sparse_vecs = model.convert_id_to_token(res["lexical_weights"])
print('稀疏向量转换为token后的结果为：',sparse_vecs,end='\n\n')
# 3、打印稠密向量
print('稠密向量为：',res["dense_vecs"],end='\n\n')
```
标量字段通常用来存储一些元数据，并可以在搜索时通过元数据进行过滤，以提高搜索结果的正确性。
#### Milvus索引
索引是建立在数据之上的附加结构，可以加快搜索速度。不同字段数据类型适用不同的索引类型。
#### 稠密向量
稠密向量可使用 HNSW（分层导航小世界）索引。
HNSW （分层导航小世界）是当下常用的一种基于图的索引算法，可以提高搜索高维浮点数向量时的性能。它具有出色的搜索精度和低延迟，但需要较高的内存开销来维护其分层图结构。该算法构建了一个多层图（类似不同缩放级别的地图），底层包含所有数据点，而上层则由从底层采样的数据点子集组成。在这种层次结构中，每一层都包含代表数据点的节点，节点之间由表示其接近程度的边连接。上层提供远距离跳转，以快速接近目标，而下层则进行细粒度搜索，以获得最准确的结果。其工作原理如下：
- 入口点：搜索从顶层的一个固定入口点开始，该入口点是图中的一个预定节点。
- 贪婪搜索：算法贪婪地移动到当前层的近邻，直到无法再接近查询向量为止。上层起到导航作用，作为粗过滤器，为下层的精细搜索找到潜在的入口点。
- 层层下降：一旦当前层达到局部最小值，算法就会利用预先建立的连接跳转到下层，并重复贪婪搜索。
- 最后细化：这一过程一直持续到最底层，在最底层进行最后的细化步骤，找出最近的邻居。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）-20260907112000021.png]]
> [!tip] 大白话解释（Intuition）
> HNSW 像先看全国地图跳到目标城市，再看街区地图接近目标，最后在小路中精细搜索。它用额外内存保存“捷径”，换取低延迟；因为不会逐个比较全部向量，所以召回率通常很高但不保证 100%。
另外一种稠密向量所支持的索引类型是FLAT, FLAT 索引是用于对浮点向量进行索引和搜索的最简单、最直接的方法之一。它采用暴力搜索的方式，每个查询向量直接与数据集中的每个向量进行比较，无需任何高级的预处理或数据结构化操作。这种方法能保证准确性，提供 100% 的召回率，因为每一个潜在的匹配项都会被评估。
#### 稀疏向量
SPARSE_INVERTED_INDEX 索引是 Milvus 用于高效存储和搜索稀疏向量的一种索引类型。这种索引类型利用倒排索引的原理，为稀疏数据创建高效的搜索结构。
以下是倒排索引示意图：
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）-20260907112000022.png]]
在实际查询时，先通过倒排索引查询到包含query当中token的文档有哪些，然后计算查询和各个文档之间的相似度分数。 标
在计算查询和文档之间的相似度分数时，有两种指标类型（metric type）:
- IP: 即Inner Product内积，例如查询所对应的稀疏向量为：{27:0.7, 100:0.4}，doc1所对应的稀疏向量为：{27:0.5, 100:0.3, 5369:0.6}，则相似度分数为similarity = (0.5×0.7) + (0.3×0.4) = 0.35 + 0.12 = 0.47
- BM25: 通过对 query 与文档中重合的词项进行加权求和，综合考虑词频（TF）、逆文档频率（IDF: 反映了一个词在全部文档当中的重要性，词出现的文档数量越少，IDF越高）以及文档长度归一化，从而计算二者的相关性得分。
#### Milvus 部署（Milvus Deployment）
Milvus 提供了多个版本以在不同场景下选择合适的使用方式：
- Milvus Lite：本地轻量化运行，通过 pip install pymilvus[milvus-lite] 即可安装。但 Milvus Lite 有一些限制，比如 Milvus Lite 仅支持 FLAT 索引类型。无论在 Collections 中指定了哪种索引类型，它都使用 FLAT 类型。另外，Milvus Lite仅支持在MacOs和Linux上面使用。
- Milvus Standalone：单点部署，支持通过 Docker 部署。
- Milvus Distributed：分布式部署，支持在 Kubernetes 集群上部署。
原稿课程环境使用 Milvus Standalone，并通过课程提供的离线镜像与 `standalone_embed.sh` / `standalone.bat` 启动脚本部署；这些本地课程资源的具体文件名已移入本批次的“课程资源与行政信息”归档。长期笔记应按当前 Milvus 官方 Docker Compose 文档取得镜像和启动配置，避免依赖未记录版本的离线包。
启动完成后，可以通过 Milvus 官方图形化客户端 Attu 查看数据。下面是连接本机 `127.0.0.1:19530` 的界面示例；生产环境不得使用空口令或把真实令牌写入截图。
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）-20260907112000023.png]]
### 创建集合（Create a Collection）
正如前面介绍，Milvus当中的数据，存储到独立的Collection当中。创建Collection可以分为以下步骤：
##### 构建schema信息；
##### 添加索引；
##### 创建collection。
示例代码如下所示：
```python
# pip install pymilvus
def get_milvus_client():
    from pymilvus import MilvusClient
    client = MilvusClient(
        uri="http://localhost:19530",
        token="",
    )
    res = client.list_collections()
    print(res)

    return client

def build_schema():
    from pymilvus import MilvusClient, DataType
    return (
        MilvusClient.create_schema(
            # 自动为id字段赋值
            auto_id=True,
        )
        # 添加 id 字段，类型为整数，设置为主键
        .add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        # 添加 vector 字段，类型为浮点数向量，维度为 1024
        .add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
        # 添加 text 字段，类型为字符串，最大长度为 1500
        .add_field(field_name="text", datatype=DataType.VARCHAR, max_length=1500)
        # 添加 metadata 字段，类型为 JSON
        .add_field(field_name="metadata", datatype=DataType.JSON)
        .add_field(field_name="sparse_vector",datatype=DataType.SPARSE_FLOAT_VECTOR)
    )

def build_index():
    from pymilvus import MilvusClient, DataType
    index_params = MilvusClient.prepare_index_params()
    index_params.add_index(
        field_name="vector",  # 建立索引的字段
        index_type="HNSW",  # 索引类型
        metric_type="L2",  # 向量相似度度量方式
    )
    index_params.add_index(
        field_name="sparse_vector",
        index_type="SPARSE_INVERTED_INDEX",
        metric_type="IP",
    )
    return index_params

def create_collection(client):
    from pprint import pprint
    if client.has_collection(collection_name="demo_collection"):
        client.drop_collection(collection_name="demo_collection")
    if not client.has_collection(collection_name="demo_collection"):
        print("collection demo_collection not exists, create it")
        client.create_collection(
            collection_name="demo_collection",  # collection 名称
            schema=build_schema(),  # collection 的 schema
            index_params=build_index(),  # collection 的 index
        )
        # 查看 collection
        print(client.list_collections())

        # 查看 collection 描述
        pprint(client.describe_collection(collection_name="demo_collection"))
create_collection(get_milvus_client())
```
### 实体操作（Entity Operations）
在创建完了collection之后，就可以“增删”操作。
#### 插入实体（Insert Entities）
将数据构建成List[Dict]形式，其中List表示批量数据，Dict表示符合创建collection时所定义的schema结构的数据，构建完成后，即可通过client.insert方法，将数据插入到指定的collection当中去，示例代码如下：
```python
from pymilvus import MilvusClient,DataType
def get_client():
    return MilvusClient(uri="http://localhost:19530",token="")

def insert_data(client:MilvusClient,collection_name:str):
    """
    构建数据，并插入到collection中
    """

    # 1、加载一个文件:此处以assets/sample.docx文件为例
    from langchain_community.document_loaders import UnstructuredWordDocumentLoader
    doc_list = UnstructuredWordDocumentLoader("assets/sample.docx",mode="single").load()
    # 2、切分文件
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50,separators=["\n\n","\n","。"])
    splitted_doc_list =text_splitter.split_documents(doc_list)
    splitted_doc_list = splitted_doc_list[0:20]

    # 查看当前文本列表当中最大的文本长度
    max_len = max(len(doc.page_content.encode("utf-8")) for doc in splitted_doc_list)
    print('当前最大长度是：',max_len)
    # 3、构建向量：稠密向量，稀疏向量

    from FlagEmbedding import BGEM3FlagModel

    model = BGEM3FlagModel("assets/models/bge-m3") # 需要安装 带cuda的torch

    all_vectors = model.encode([doc.page_content for doc in splitted_doc_list],return_dense=True,return_sparse=True)

    dense_vectors = all_vectors["dense_vecs"]
    sparse_vectors = all_vectors['lexical_weights']

    # 4、准备数据：组装成List[Dict]
    insert_data_list=[]
    for  doc, dense_vector, sparse_vector in zip(splitted_doc_list,dense_vectors,sparse_vectors):
        insert_data_list.append({
            "vector":dense_vector,
            "sparse_vector":sparse_vector,
            "metadata":doc.metadata,
            "text":doc.page_content
        })

    # 5、调用client.insert()方法，插入数据
    res = client.insert(
        collection_name=collection_name,
        data=insert_data_list
    )
    # 有多少条数据插入成功
    print(res)
```
#### 删除实体（Delete Entities）
删除实体，可以调用MilvusClient的delete方法，该同样也可以通过传递id列表，或者是通过其他字段过滤条件来进行删除，该方法返回结果为一个字典，包含了一个delete_count键，值为删除的数据条数，示例代码如下所示：
```python
def delete_demo(client):
    res = client.delete(
        collection_name="demo_collection",
        # 过滤条件，仅删除 id 在指定范围内的实体,也可以传递其他字段的过滤条件
        filter="id in [463480757150366907, 463480757150366908]",
    )
    print(res)

if __name__ == "__main__":
    client = get_milvus_client()
    delete_demo(client)
```
### Milvus 检索（Milvus Search）
Milvus 支持多种检索方式。对向量字段，Milvus 支持精确检索（KNN）以及近似近邻检索（ANN）。对标量字段，Milvus 提供条件过滤能力，主要用于配合向量检索进行结果筛选，其能力和定位不同于传统关系型数据库普通检索。
#### 向量检索（Vector Search）
通过调用client.search，传入需要检索的query向量，以及需要和query向量进行比较的向量字段，即可进行向量检索。
在执行向量检索时，通常需要关注以下参数：
- 查询向量（query vector）：表示待检索对象的向量表示，维度需与集合中向量字段一致。
- 向量字段（anns_field）：指定参与检索的向量字段名称。
- TopK（limit）：返回相似度最高的结果数量。
- metric_type：指定相似度计算方式，如 COSINE、L2 或 IP，需与索引和向量语义保持一致。
另外向量检索还支持同时使用稠密向量和稀疏向量，进行混合检索，并配置重排序器，来对两路召回结果进行一个重排序。
重排序（Reranker）是指在初步检索（Recall）完成后，对候选结果进行二次排序优化的过程。其目标不是扩大召回范围，而是在已有候选集内提升排序质量和结果相关性。在典型的检索系统中，重排序通常位于向量检索或混合检索之后，用于融合多路检索结果或引入更精细的排序策略。
此处介绍RRFReranker。RRFRanker 策略的主要工作流程如下：
##### 收集搜索排名：收集来自向量搜索各路径的结果排名（rank_1、rank_2）。
##### 合并排名：根据公式转换各路径的排名（rank_rrf_1、rank_rrf_2）。
计算公式涉及 N，N 代表检索器的数量。ranki (d) 是第 i 个检索器生成的文档 d 的排名位置。k 是一个平滑参数，通常设置为 60。
对文档 $d$，倒数排名融合（Reciprocal Rank Fusion, RRF）分数为：
$$
\operatorname{RRF}(d)=\sum_{i=1}^{N}\frac{1}{k+\operatorname{rank}_i(d)}
$$
> [!tip] 大白话解释（Intuition）
> RRF 不直接比较两套检索器不可比的原始分数，而只看“排第几”。一个文档如果在稠密检索和关键词检索中都名列前茅，融合后就会获得更高排名。
##### 聚合排名：基于合并后的排名对搜索结果进行重新排序，以生成最终结果。
其示意图如下：
![[Attachments/Notes/数据科学（Data Science）/03-深度学习（Deep Learning）/04-自然语言处理（Natural Language Processing）/03-大语言模型（Large Language Models）/02-LangChain 应用开发（LangChain Application Development）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）/04-Milvus 向量存储与检索（Milvus Vector Storage and Retrieval）-20260907112000024.png]]
向量检索示例代码如下：
```python
from typing import Any, Dict, List, Tuple
COLLECTION_NAME = "demo_collection"

def get_milvus_client(uri: str = "http://localhost:19530", token: str = ""):
    from pymilvus import MilvusClient

    return MilvusClient(uri=uri, token=token)

def get_bge_m3_model():
    from FlagEmbedding import BGEM3FlagModel

    return BGEM3FlagModel(model_name_or_path="./assets/models/bge-m3")

def encode_query(model, query: str) -> Tuple[List[float], Dict[int, float]]:
    all_embeddings = model.encode([query], return_dense=True, return_sparse=True)
    dense_vec = all_embeddings["dense_vecs"][0]
    sparse_raw = all_embeddings["lexical_weights"][0]
    sparse_vec = {
        int(token_id): float(weight)
        for token_id, weight in sparse_raw.items()
    }
    return dense_vec, sparse_vec

def print_hits(title: str, hits: List[dict]):
    print("\n" + "=" * 20)
    print(title)
    print("=" * 20)
    for i, hit in enumerate(hits, start=1):
        entity = hit.get("entity", {})
        print(
            {
                "rank": i,
                "id": entity.get("id"),
                "distance": hit.get("distance"),
                "text": entity.get("text"),
                "metadata": entity.get("metadata"),
            }
        )

def dense_vector_search_example(client, query: str, limit: int = 5):
    model = get_bge_m3_model()
    dense_vec, _ = encode_query(model, query)

    results = client.search(
        collection_name=COLLECTION_NAME,
        data=[dense_vec],
        anns_field="vector",
        limit=limit,
        search_params={"metric_type": "L2"},
        output_fields=["id", "text", "metadata"],
    )
    print_hits("稠密向量检索（vector）", results[0])
    return results

def sparse_vector_search_example(client, query: str, limit: int = 5):
    model = get_bge_m3_model()
    _, sparse_vec = encode_query(model, query)

    results = client.search(
        collection_name=COLLECTION_NAME,
        data=[sparse_vec],
        anns_field="sparse_vector",
        limit=limit,
        search_params={"metric_type": "IP"},
        output_fields=["id", "text", "metadata"],
    )
    print_hits("稀疏向量检索（sparse_vector）", results[0])
    return results

def hybrid_vector_search_example_rrf(client, query: str, limit: int = 5):
    from pymilvus import AnnSearchRequest, RRFRanker

    model = get_bge_m3_model()
    dense_vec, sparse_vec = encode_query(model, query)

    dense_req = AnnSearchRequest(
        data=[dense_vec],
        anns_field="vector",
        param={"metric_type": "L2"},
        limit=limit,
    )
    sparse_req = AnnSearchRequest(
        data=[sparse_vec],
        anns_field="sparse_vector",
        param={"metric_type": "IP"},
        limit=limit,
    )

    results = client.hybrid_search(
        collection_name=COLLECTION_NAME,
        reqs=[dense_req, sparse_req],
        ranker=RRFRanker(k=60),
        limit=limit,
        output_fields=["id", "text", "metadata"],
    )
    print_hits("混合向量检索（RRF 融合稠密+稀疏）", results[0])
    return results
```
#### 标量检索（Scalar Query）
标量检索（或标量查询）是指不涉及向量相似度计算，仅基于标量字段条件对数据进行筛选和返回的检索方式。
标量检索示例代码如下所示：
```python
def scalar_query_examples(client, like_keyword: str = "大模型"):
    # 对text字段进行检索
    try:
        like_res = client.query(
            collection_name=COLLECTION_NAME,
            filter=f'text like "%{like_keyword}%"',
            output_fields=["id", "text"],
            limit=5,
        )
        print("\n" + "=" * 20)
        print(f'标量检索（query: text like "%{like_keyword}%"）')
        print("=" * 20)
        for row in like_res:
            print({"id": row.get("id"), "text": row.get("text")})
    except Exception as e:
        print("VARCHAR like 过滤失败：", e)

    # 对metadata字段进行检索
    try:
        json_res = client.query(
            collection_name=COLLECTION_NAME,
            filter='metadata["source"] like "%sample%"',
            output_fields=["id", "metadata"],
            limit=5,
        )
        print("\n" + "=" * 20)
        print('标量检索（query: metadata["source"] like "%sample%"）')
        print("=" * 20)
        for row in json_res:
            print({"id": row.get("id"), "metadata": row.get("metadata")})
    except Exception as e:
        print("JSON 过滤失败（metadata 结构不匹配或不支持该表达式）：", e)
```
## 基于检索结果生成回答（Generation）
查找到相关数据之后，就可以将所有的数据，放到和LLM交互的上下文当中，让LLM基于完整的上下文信息来进行生成。
```python
def rag_demo(client, query: str):
    from langchain_openai import ChatOpenAI
    # 加载模型
    llm = ChatOpenAI(model="gpt-4o-mini")
    retrieval_res = hybrid_vector_search_example_rrf(client=client, query=query)
    # 构建上下文
    hits = retrieval_res[0]
    context = "\n".join(
        hit.get("entity", {}).get("text", "") for hit in hits
    )
    message_list=[
        {"role": "system", "content": "你是一个专业的法律问答机器人，请根据上下文回答问题，当上下文无法回答问题时，请回答“根据上下文无法回答该问题”"},
        {"role": "user", "content": f"根据以下上下文回答问题：{context}\n问题：{query}"}
    ]

    # 生成文本
    res = llm.invoke(message_list)
    print(res.content)

if __name__ == "__main__":
    client = get_milvus_client()
    rag_demo(client, "不动产被占有了怎么办？")
```
