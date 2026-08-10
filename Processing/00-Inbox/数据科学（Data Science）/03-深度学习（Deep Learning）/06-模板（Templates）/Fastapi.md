# FastAPI 核心开发笔记

## 2 | 安装 (Installation)

正式环境 (Production Environment) 需要 ASGI 服务器软件，可安装 Uvicorn 或 Hypercorn。

~~~bash
$ pip install fastapi
$ pip install "uvicorn[standard]"
~~~

---

## 3 | 可选依赖项 (Optional Dependencies)

* **Pydantic 使用：**
  * `ujson`：快速 JSON 格式解析
  * `email_validator`：邮件验证
* **Starlette 使用：**
  * `requests`：使用 `TestClient` 必安
  * `jinja2`：使用默认模板配置必安
  * `python-multipart`：使用 `request.form()` 进行表单解析必安
  * `itsdangerous`：使用中间件 `SessionMiddleware` 必安
  * `pyyaml`：支持 Starlette 的 `SchemaGenerator`
  * `ujson`：使用 `UJSONResponse` 必安
* **FastAPI / Starlette 使用：**
  * `uvicorn`：作为服务器
  * `orjson`：使用 `ORJSONResponse` 必安

> 💡 以上所有依赖可以通过 `pip install "fastapi[all]"` 一键安装。

---

## 4 | 开发 CLI (Development CLI)

* 参考文档：[Typer Documentation](https://fastapi.tiangolo.com/#typer-the-fastapi-of-clis)
* 如果需要开发在终端中使用的 CLI 应用而不是网页 API，可以使用 **Typer**。

---

## 5 | 类型提示 (Type Hints)

Python 3.6 版本新增的特性。

~~~python
# 普通类型
def get_name_with_age(name: str, age: int):
    pass

# 嵌套类型
def process_items(items: List[str]):
    pass
~~~

### 4 大作用
1. 提示程序员参数类型。
2. 帮助 FastAPI 接受请求时校验参数。
3. FastAPI 验证通过后自动转换数据。
4. 让编辑器辅助进行检查。

---

## 6 | 用户指南 (User Guide)

### 6-1 | 第一步 (First Steps)

* 参考文档：[First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)

#### 简单示例
~~~python
# main.py

# 1. 导入
from fastapi import FastAPI

# 2. 实例化
app = FastAPI()

# 3. 定义
@app.get("/")
async def root():
    return {"message": "Hello World"}
~~~

> 📌 `FastAPI` 类直接继承自 `Starlette`。

#### 运行开发服务器 (Development Server)

##### 1. 命令行方式
通过以下指令执行：
~~~bash
$ uvicorn main:app --reload
~~~
* `main`：指代文件 `main.py`
* `app`：`main.py` 中创建的对象，即 `app = FastAPI()`
* `--reload`：文件修改时自动重启服务，⚠️ **仅开发时使用**。

##### 2. 代码方式
在主业务逻辑 `main.py` 中直接定义运行服务器代码，避免手动命令行输入指令：
~~~python
import uvicorn

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True) 
~~~

#### 其他 HTTP 请求方式
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

---

### 6-2 | 自带文档 (Automatic Docs)

* **Swagger 文档**：访问 `http://127.0.0.1:8000/docs`，样式采用 Swagger UI。
* **Redoc 文档**：访问 `http://127.0.0.1:8000/redoc`，样式采用 ReDoc。

以上两种文档均可自定义 URL，也可以关闭：
~~~python
# 自定义与关闭示例
app = FastAPI(docs_url="/documentation", redoc_url=None)
app = FastAPI(redoc_url="/documentation", docs_url=None)
~~~

---

### 6-3 | OpenAPI

FastAPI 根据 OpenAPI 标准给所有 API 以标准的 JSON 格式生成返回值与参数以及接口描述。

#### 查看 openapi.json
默认地址为 `http://127.0.0.1:8000/openapi.json`，也可自定义地址：
~~~python
app = FastAPI(openapi_url="/api/v1/openapi.json")
~~~

---

### 6-4 | 路径参数 (Path Parameters)

* 参考文档：[Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)

#### 定义参数与类型
~~~python
# 定义参数
@app.get("/items/{item_id}") 
async def read_item(item_id):
    pass

# 定义参数类型
@app.get("/items/{item_id}")   
async def read_item(item_id: int):
    pass
~~~

#### 6-4-1 | 接口顺序

* ⚠️ **路径重叠**：路由匹配采取**自上而下**的顺序，靠上的先匹配到。
~~~python
@app.get("/users/me")      # 靠前，优先匹配
@app.get("/users/{user_id}")
~~~
> 💡 Flask 不会出现这种情况，在 Flask 中即使 `/users/me` 放在下面也可以被正确访问到。

* ⚠️ **路径重复**：相同路径可重复注册，但**只有最靠前**的会被匹配。
~~~python
@app.get("/users/me")  
def user_me_1(): 
    pass

@app.get("/users/me")  # 该路由将被忽略
def user_me_2():
    pass
~~~

#### 6-4-2 | 定义参数范围 Enum
编写 API 时若需限定参数的选择范围，可采用标准类型 `Enum`（需要 Python 3.4+）：

~~~python
# 1. 导入
from enum import Enum
from fastapi import FastAPI

app = FastAPI()

# 2. 定义范围
class ModelName(str, Enum):
    al = "alexnet"
    re = "resnet"
    le = "lenet"

# 3. 作为类型给参数
@app.get("/models/{name}")
async def get_model(name: ModelName):
    # 调用值
    name.value
    ModelName.al.value
    
    # 可直接比较
    if name is ModelName.al:
        return {"model_name": name, "message": "Deep Learning FTW!"}
        
    return {"model_name": name}
~~~
> 📌 `return` 中的 `model_name` 会自动转换成相应的值再响应给客户端。

#### 6-4-3 | 路径中的路径 :path
路径也可以作为 URL 参数并被自动转换类型：
~~~python
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
~~~
入参 `file_path` 也可以 `/` 开头，例如请求：`http://127.0.0.1:8000/files//aa.txt`
将收到响应：`{"file_path":"/aa.txt"}`

---

### 6-5 | 地址栏参数 (Query Parameters)

访问时可通过 URL 获取地址栏参数，例如 `/items/?skip=0&limit=10`：
~~~python
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
~~~

如果需要参数非必填（可选参数），可写为：
~~~python
# Python 3.10+ 写法
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    pass

# Python 3.10 以下版本使用 Union
from typing import Union
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    pass
~~~

#### 自动转换
布尔类型也可作为地址栏参数值传递，以下请求的值均被视为 `True`：
* `/items/foo?short=1`
* `/items/foo?short=True`
* `/items/foo?short=true`
* `/items/foo?short=on`
* `/items/foo?short=yes`

多个参数可同时定义，不用关注定义顺序：
~~~python
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    pass
~~~
> 📌 **必填参数**：在定义时不给定默认值即可。

---

### 6-6 | 请求体 (Request Body)

#### 6-6-1 | BaseModel
~~~python
# 1. 引入 BaseModel
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

# 2. 定义 BaseModel
class Item(BaseModel):
    name: str
    desc: str | None = None  # 可选参数

# 3. 作为定义参数
@app.post("/items/")
async def create_item(item: Item):
    item.name  # 各属性可直接使用
    item_dict = item.dict()  # 获取所有数据属性字典
    return item_dict
~~~
请求数据示例：
~~~json
{
    "name": "Foo",
    "desc": "desc 是选填参数，当前键值对可不传！"
}
~~~

#### 6-6-2 | Body()
~~~python
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    desc: str | None = None

@app.put("/items/{item_id}")
async def update_item(item: Item, importance: int = Body()):
    return {"item": item, "importance": importance}
~~~
请求数据示例：
~~~json
{
    "item": {
        "name": "Foo",
        "desc": "The"
    },
    "importance": 5
}
~~~

#### 6-6-3 | Body(embed=True)
`Body(embed=True)` 可要求入参嵌套一层，而其键（Key）就是参数名称。
~~~json
// 使用 Body(embed=True) 时的 JSON 结构
{
    "item": {
        "name": "Foo",
        "desc": "The pretender"
    }
}

// 普通 BaseModel 直接接收时的 JSON 结构
{
    "name": "Foo",
    "desc": "The pretender"
}
~~~

#### 6-6-4 | Field()
`Field` 的工作方式和 `Query`、`Path` 以及 `Body` 相同，包括参数也完全相同，类似于 Django 的表单字段。
~~~python
# 1. 导入
from pydantic import BaseModel, Field

# 2. 定义
class Item(BaseModel):
    description: str | None = Field(default=None, title="The title")
    price: float = Field(gt=0, description="The price")
~~~

#### 6-6-5 | 嵌套模型 (Nested Models)
~~~python
from typing import Union, List, Set, Dict
from pydantic import BaseModel, HttpUrl

# 1. 定义基础模型
class Image(BaseModel):
    url: str  # 也可以使用 pydantic 自带的 HttpUrl，具有验证功能

class ImageValidated(BaseModel):
    url: HttpUrl
    name: str

# 2. 赋给其他类属性
class Item(BaseModel):
    image: Union[Image, None] = None  # 单个嵌套
    images: Union[List[Image], None] = None  # 多个嵌套
~~~
请求数据示例：
~~~json
{
    "image": {"url": "http://example.com/baz.jpg"},
    "images": [
        {"url": "http://example.com/baz.jpg"},
        {"url": "http://example.com/dave.jpg"}
    ]
}
~~~

##### 带有子类型的属性声明
~~~python
class ItemAdvanced(BaseModel):   
    tags1: List[int] = []  # 具有子类型的 List 类型
    tags2: Set[int] = set()  # 具有子类型的 Set 类型
    weights: Dict[int, float] = dict()
~~~
> 📌 如果不需要限定子类型，直接使用 Python 标准的 `list`、`set` 即可。

---

### 6-7 | 入参校验 Query (Query Parameter Validations)

#### 6-7-1 | 定义规则
定义接口时，可以设定校验，让入参符合指定条件（相当于 Form 校验）。
*示例：必填入参 `q` 且其长度最大 50，最小长度为 2*
~~~python
# 1. 导入
from fastapi import FastAPI, Query

app = FastAPI()

# 2. 定义最大最小长度，正则
@app.get("/items/")
async def read_items(q: str | None = Query(min_length=2, max_length=50, regex="^fixedquery$")):
    pass
~~~

#### 6-7-2 | 校验数字大小
接口的整数、浮点数类型入参可验证大小，`Path` 和 `Query` 均支持设定以下参数：
* `gt`: 大于 (`greater than`)
* `ge`: 大于等于 (`greater than or equal`)
* `lt`: 小于 (`less than`)
* `le`: 小于等于 (`less than or equal`)

#### 6-7-3 | 定义选填 & 必填
* **定义选填参数**：`Query(default=None)`
* **定义必填参数**：
  1. 不写 `default=None`
  2. 写为 `default=...` (Ellipsis)
  3. 写为 `Query(default=Required)`，需引入 `from pydantic import Required`

#### 6-7-4 | 接受参数列表
~~~python
from typing import List
from fastapi import Query

async def read_items(q: List[str] | None = Query(default=["foo", "bar"])):
    pass

async def read_items_list(q: list = Query(default=[])):  # list 等同 List[str]
    pass
~~~
对应接收的数据格式：`{"q": ["foo", "bar"]}`

---

### 6-8 | 入参描述 & 别名 & 弃用 (Description, Alias & Deprecation)

使用参数 `title` 或 `description`，这些描述会被用在自动生成的接口文档中。
~~~python
from typing import Union
from fastapi import Query

async def read_items(
    q: Union[str, None] = Query(
        title="Query string",
        description="Query string for the items to search in the database"
    )
):
    pass
~~~

#### 6-8-1 | 入参别名
解决地址栏中的参数名称（如带有连字符）与 Python 变量命名规范不一致的问题：
~~~python
@app.get("/items/")
async def read_items(q: Union[str, None] = Query(alias="item-query")):
    pass
~~~
此时访问 `/items/?item-query=test` 就可以被正确识别并赋值给变量 `q` 了。

#### 6-8-2 | 入参弃用
若需弃用某参数，但仍有旧客户端在使用，可通过以下方式在文档中标记：
~~~python
async def read_items(q: Union[str, None] = Query(deprecated=True)):
    pass
~~~
在 FastAPI 自动生成文档中会将对应参数标记上红色的 **Deprecated** 标签，但实际该参数仍可用。

---

### 6-9 | 入参校验 Path (Path Parameter Validations)

与 `Query` 除了作用对象是路径参数外，其余支持的入参和校验规则都相同。
~~~python
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    q: str, 
    item_id: int = Path(title="The ID of the item to get")
):
    pass
~~~
💡 **小技巧**：如果参数 `q` 没有默认值，且想放在关键字参数 `item_id` 后面，可以在前面放置一个星号 `*`：
~~~python
async def read_items(
    *, 
    item_id: int = Path(title="The ID of the item to get", ge=1), 
    q: str
):
    pass
~~~

---

### 6-10 | 在文档中隐藏参数

定义的参数不需要显示在 Swagger/Redoc 文档中时，使用 `include_in_schema=False`：
~~~python
async def read_items(q: str | None = Query(default=None, include_in_schema=False)):
    pass
~~~

---

### 6-11 | 演示数据 (Declare Request Example Data)

* **方法一**：在 Pydantic 模型中定义 `Config` 与 `schema_extra`，会体现在文档中。
* **方法二**：直接在字段中给出，单个演示数据用 `example`，多个可以使用 `examples`。

~~~python
from typing import Union, Annotated
from pydantic import BaseModel, Field
from fastapi import Body

# 方法一
class Item(BaseModel):
    name: str
    tax: Union[float, None]

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "tax": 3.2
            }
        }

# 方法二
async def update_item(
    tax: Union[float, None] = Field(example=3.2),
    item: Annotated[
        Item, Body(
            examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A normal item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ] = None
):
    pass
~~~
> 📌 方法二的方法亦可在 `Path()`, `Query()`, `Body()` 中定义。

---

### 6-12 | 其他数据类型 (Extra Data Types)

除了常用的数字、字符串、布尔型外，还可用 `UUID`，`datetime`，`frozenset`，`bytes`，`Decimal` 等。
~~~python
from datetime import datetime, timedelta
from typing import Annotated
from uuid import UUID
from fastapi import FastAPI, Body

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start: Annotated[datetime | None, Body()] = None,
    end: Annotated[datetime | None, Body()] = None,
):
    duration = end - start  # 可直接使用原对象支持的数学运算操作
    return {"item_id": item_id, "duration": duration}
~~~

---

### 6-13 | Cookie

~~~python
from typing import Annotated
from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
~~~
> 📌 用法与 `Query()`、`Path()` 相同。如果不使用 `Cookie()` 进行显式声明，参数会被识别为地址栏参数。

---

### 6-14 | Header

~~~python
from typing import Annotated
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
~~~
> 📌 由于 Python 不允许变量名中使用减号 `-`，因此 FastAPI 会自动转换请求头中的 `-` 为下划线 `_`（如 `user_agent` 接收 `User-Agent`）。如果不需要自动转化，可以设置 `convert_underscores=False`。

#### 重复的头部
如果需要接受名称相同的多个 Header，将类型设为 `list` 或 `List` 即可：
~~~python
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}
~~~
*可以接收如下形式的重复头部：*
`X-Token: foo`
`X-Token: bar`

---

### 6-15 | 响应模型 response_model (Response Model)

* **需求**：入参是 `BaseModel` 类型，如果直接返回，文档中会对其进行说明，但实际需要返回一个字典，如果直接返回字典，IDE 会提示返回值与定义时的不一致。
* **解决方法**：使用 `response_model` 参数进行声明。

~~~python
from typing import Any
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

# 返回单个数据
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item

# 返回多个数据
@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
~~~
> 💡 **提示**：建议将路由函数返回值类型提示写为 `Any`，以避免 IDE 类型检查时产生不必要的报错。

#### 6-15-1 | response_model 优先级
当同时定义了函数的返回类型提示与 `response_model` 时，FastAPI **优先使用** `response_model` 的配置进行数据过滤和序列化。

#### 6-15-2 | 返回相同类型
~~~python
# ⚠️ 生产环境绝对不要这样写!!!!
@app.post("/user/", response_model=UserIn)
async def create_user(user: UserIn) -> UserIn:
    return user
~~~
> ⚠️ **安全警告**：如果直接将包含敏感信息（如 `password`）的输入模型作为输出返回，多个用户同时操作时，敏感数据极有可能泄漏。

**【正确写法】**：定义两个模型，一个处理接口入参，一个处理接口响应值。
~~~python
from pydantic import BaseModel, EmailStr

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(BaseUser):
    password: str

@app.post("/user/", response_model=BaseUser)
async def create_user(user: UserIn) -> BaseUser:
    # 这样敏感的 password 字段就不会被返回给前端了 
    return user
~~~

#### 6-15-3 | 停用响应类型
~~~python
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/portal", response_model=None) 
async def get_portal(teleport: bool = False) -> Response | dict:
    # 必须写 response_model=None，否则会报错
    # 因为 Response | dict 不是合法的 Pydantic 类型
    if teleport:
        return RedirectResponse(url="https://example.com")
    return {"message": "Here"}
~~~

#### 6-15-4 | 排除空字段
**问题**：响应模型的属性有默认值，但实际数据中没有存储对应值，需要从最终的返回值中自动省略它们。
**解决方法**：通过配置 `response_model_exclude_unset=True` 来达成此目的。

~~~python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
}

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
~~~
当请求 `foo` 时，响应结果将不会包含未手动赋值的默认字段：
`{"name": "Foo", "price": 50.2}`
> 📌 FastAPI 会优先采用数据中手动定义的值，而不是模型定义的默认值。

#### 6-15-5 | 排除/包含指定字段
`response_model_include` 和 `response_model_exclude` 可作为响应中排除、包含少量字段的快捷方法（接收 `set`、`list` 或 `tuple`）。

~~~python
# 包含指定字段
@app.get("/items/{item_id}/name", response_model=Item, response_model_include={"name", "description"})
async def read_item_name(item_id: str):
    return items[item_id]

# 排除指定字段
@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]
~~~

---

### 6-16 | 状态码 (Response Status Code)

定义响应的状态码，可以使用自带的常量 `status`，也可以直接填写整数：
~~~python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED) 
async def create_item(name: str):
    return {"name": name}

# 或者直接写整数
@app.post("/items-shortcut/", status_code=201)
async def create_item_shortcut(name: str):
    return {"name": name}
~~~

---

### 6-17 | 表单 Form (Request Forms)

使用前需先安装：`pip install python-multipart`

~~~python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}
~~~
> ⚠️ **注意**：发送请求时，请求头必须包含 `Content-Type: multipart/form-data`，否则会触发 422 验证错误。这两个字段是以 form-field 形式提交的，而不是请求体中的 JSON 数据。
> 📌 **提示**：`Form` 类直接继承自 `Body`。

---

### 6-18 | 上传文件 (Request Files)

同样需要依赖 `python-multipart` 包。

~~~python
from typing import Annotated
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# 方法一：上传的文件会完全存在内存中，适合小型文件
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):  
    return {"file_size": len(file)}

# 方法二：使用 UploadFile，文件超过限制时会存在磁盘中
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

# 上传多个文件
@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [f.filename for f in files]}

# 用 File() 添加额外设定
@app.post("/uploadfiles-desc/")
async def create_upload_files_desc(
    files: Annotated[list[UploadFile], File(description="Multiple files as UploadFile")]
):
    return {"filenames": [f.filename for f in files]}
~~~
> 📌 **提示**：`File` 类直接继承自 `Form`。

#### 6-18-1 | UploadFile 的优势与特性
与直接使用 `bytes` 类型相比，`UploadFile` 具有以下优点：
1. 上传的文件如果超过最大限制，会自动存储在磁盘中，避免内存溢出。
2. 可以方便地获取上传文件的元信息 (Metadata)，例如文件名、MIME 类型。
3. 文件对象拥有自己的类文件接口，其底层生成的是 `SpooledTemporaryFile` 对象，可以直接传给其他只处理文件流的代码。

##### 常用属性与异步方法
* `filename`：原始文件名。
* `content_type`：MIME 类型。
* `file`：`SpooledTemporaryFile` “类文件”对象。
* `await file.read(size)`：读取文件内容。
* `await file.write(data)`：写入数据。
* `await file.seek(offset)`：移动文件指针。
* `await file.close()`：关闭文件。

调用这些方法时需要采用异步方式：
~~~python
contents = await myfile.read()
~~~
当然也可以绕过异步，直接通过底层对象调用：
~~~python
contents = myfile.file.read()
~~~

---

### 6-19 | 返回异常 (Handling Errors)

#### 6-19-1 | HTTPException
~~~python
from fastapi import FastAPI, HTTPException

app = FastAPI()
items = {"foo": "The Foo Wrestlers"}

@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        # 注意：这里使用 raise 抛出异常，而不是 return！
        raise HTTPException(
            status_code=404,
            detail="Item not found",  # 响应体中的错误详情
            headers={"X-Error": "There goes my error"},  # 自定义响应头
        )
    return {"item": items[item_id]}
~~~
`detail` 的值会以键值对形式出现在响应体中（也可以传入 `dict` 或 `list`）：
~~~json
{
  "detail": "Item not found"
}
~~~
> 📌 FastAPI 自定义的 `HTTPException` 继承自 Starlette 的 `HTTPException`，允许在抛出时添加自定义响应头。

#### 6-19-2 | 自定义异常
~~~python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# 1. 自定义一个异常类
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

# 2. 自定义错误处理方法，并通过装饰器绑定处理的异常
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something"},
    )

# 3. 在业务逻辑需要的地方抛出异常
@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
~~~

#### 6-19-3 | 覆写原生错误响应
可以通过异常处理器直接捕获并覆写 FastAPI 原生的请求验证错误 `RequestValidationError`：
~~~python
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

# 示例一：返回纯文本
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

# 示例二：在响应中返回请求体中的原始数据，辅助排查问题
@app.exception_handler(RequestValidationError)
async def advanced_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}), # 包含被拒绝的 body 原数据
    )
~~~

---

### 6-20 | 接口说明 (Path Operation Configuration)

#### 6-20-1 | tags
可以在自动生成文档中标记分类。
~~~python
from enum import Enum
from fastapi import FastAPI

app = FastAPI()

# 方法一：直接传入字符串列表
@app.get("/items/", tags=["items"])
async def read_items():
    return []

# 方法二：使用 Enum 避免硬编码 (Hard Code)
class Tags(Enum):
    items = "items"
    users = "users"

@app.get("/users/", tags=[Tags.users])
async def read_users():
    return []
~~~

##### 为 Tag 定义元信息 (Metadata)
~~~python
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]
app = FastAPI(openapi_tags=tags_metadata)
~~~

#### 6-20-2 | summary 与 description
~~~python
@app.post(
    "/items/",
    summary="Create an item",
    description="Create an item with all the information",
)
async def create_item(item: Item):
    return item
~~~

#### 6-20-3 | 从 docstring 中获取
如果接口描述过长且需要换行排版，可以直接写在函数的 `docstring` 中，FastAPI 支持识别并渲染 Markdown 语法：
~~~python
@app.post("/items-doc/")
async def create_item_doc(item: Item):
    """
    Create an item with all the information:
    
    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
~~~
> 📌 文档字符串中的描述会被自动输出到 `/docs` 页面中。

#### 6-20-4 | response_description
用于自定义自动生成文档中接口响应值的描述，FastAPI 默认值为 `"Successful response"`：
~~~python
@app.post("/items/", response_description="The created item")
async def create_item(item: Item):
    return item
~~~

#### 6-20-5 | 弃用接口
可以在文档中为接口标记 `deprecated`，标记后接口在文档中会变灰显示，但实际接口依旧可以正常调用：
~~~python
@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"element_id": "Foo"}]
~~~

---

### 6-21 | jsonable_encoder

当需要将 Pydantic 数据对象 (Data Objects) 或其他特殊 Python 对象转换为兼容 JSON 格式的普通 Python 数据类型（如 `dict`）时，可使用 `jsonable_encoder`。其底层也是 FastAPI 用于转换数据的核心方法：

~~~python
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    price: float

item = Item(name='aa', description='test', price=1.0)

# 转换 Pydantic 模型
data = jsonable_encoder(item)
print(data)  # 输出: {'name': 'aa', 'description': 'test', 'price': 1.0}

# 转换其他标准对象
print(jsonable_encoder(datetime.now()))  # 输出: '2022-10-13T21:31:21.016772'
~~~
> 📌 转换后，数据可直接使用 Python 标准库 `json.dumps()` 输出。

#### 用于数据更新的实际应用
~~~python
items = {"foo": {"name": "Foo", "price": 50.2}}

@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded
~~~

---

### 6-22 | 更新模型数据 (Body Updates)

* Pydantic 模型的 `.dict(exclude_unset=True)` 可以排除非手动设定的值，即过滤掉未传的默认值。
* Pydantic 模型的 `.copy(update=update_data)` 可用于基于新字典快速更新并返回一个新模型实例。

~~~python
@app.put("/items-update/{item_id}")
async def update_item_data(item_id: str, item: Item):
    # 1. 过滤掉未传入的参数
    update_data = item.dict(exclude_unset=True)
    
    # 2. 模拟从数据库取出原有数据模型
    stored_item_model = Item(**{"name": "Foo", "price": 50.2})
    
    # 3. 混合更新模型数据
    updated_item = stored_item_model.copy(update=update_data)
    return updated_item
~~~

---

### 6-23 | 依赖注入 (Dependency Injection)

**【常见使用场景】**：代码重复使用、共用同一个数据库连接、权限验证等。
FastAPI 可自动将请求中的数据先传入指定方法并调用，将返回值赋给路径函数的入参，以此实现代码复用。该依赖注入系统兼容：所有关系型数据库、NoSQL 数据库、外部包以及外部 API 等。

#### 6-23-1 | 创建函数依赖
~~~python
from typing import Union
from fastapi import Depends, FastAPI

app = FastAPI()

# 1. 定义会被复用的参数函数
async def common_parameters(q: Union[str, None] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# 2. 添加依赖，注意只写名称，绝对不要带括号调用！！
@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
~~~
> ⚠️ **注意**：`Depends()` 内部只能传一个参数，且该参数必须是可调用的 (`callable`)。
> 📌 通过 `def` 定义的依赖函数可以传给 `async def` 的路径操作函数，反之 `async def` 定义的依赖也可以传给 `def` 函数。

#### 6-23-2 | “存储”依赖
通过 `Annotated` 将定义好的依赖组合起来，方便多处复用：
~~~python
from typing import Annotated

CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get("/users/")
async def read_users(commons: CommonsDep):
    return commons
~~~

#### 6-23-3 | 创建类依赖
~~~python
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

# 标准写法
@app.get("/items-class/")
async def read_items_class(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    return commons

# 简便写法（当类型提示与Depends内类一致时，Depends内可留空）
@app.get("/items-class-shortcut/")
async def read_items_shortcut(commons: Annotated[CommonQueryParams, Depends()]):
    return commons
~~~

#### 6-23-4 | 依赖嵌套
~~~python
from typing import Annotated
from fastapi import Cookie, Depends, FastAPI

app = FastAPI()

# 1. 第一个基础依赖
def query_extractor(q: str | None = None):
    return q

# 2. 写入并嵌套到另一个依赖中
def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q

# 3. 最终在接口中使用
@app.get("/items/")
async def read_query(query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]):
    return {"query_or_default": query_or_default}
~~~
> 📌 **依赖缓存**：在一个路径操作函数中重复使用同一个依赖时，在同一次请求中 FastAPI 不会重复调用该依赖，而是会直接使用缓存的结果。如果不希望使用缓存，可添加参数 `use_cache=False`：
> `async def needy_dependency(fresh_value: Annotated[str, Depends(get_value, use_cache=False)]):`

#### 6-23-5 | 装饰器依赖
某些情况下，不需要在函数内获取依赖函数的返回值，只需要它执行验证或通用业务逻辑，此时可以直接在路径装饰器上添加：
~~~python
from fastapi import Header, HTTPException, Depends

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

@app.get("/items/", dependencies=[Depends(verify_token)])
async def read_items():
    return [{"item": "Foo"}]
~~~

#### 6-23-6 | 全局依赖
直接将依赖加载到整个 APP 实例上，作用于全局所有的路径操作函数：
~~~python
app = FastAPI(dependencies=[Depends(verify_token)])
~~~

#### 6-23-7 | yield 依赖
FastAPI 支持依赖函数在返回结果给接口后，继续执行额外的逻辑（例如关闭连接），此时需要使用 `yield` 代替 `return`。
*示例：返回数据库连接并确保最终关闭*
~~~python
async def get_db():
    db = DBSession()
    try:
        yield db  # 将连接注入到业务函数中
    finally:
        db.close()  # 请求响应结束后，自动执行关闭逻辑
~~~

---

### 6-24 | 安全 (Security)

* **OAuth2**：一个规范，定义了几种处理身份认证和授权的方法。它没有指定如何加密通信，期望应用程序必须使用 HTTPS 进行安全通信。
* **OAuth1**：与 OAuth2 完全不同且更为复杂，包含了如何加密通信的规范，目前已不再广泛使用。
* **OpenID Connect**：一个基于 OAuth2 的扩展，明确了一些 OAuth2 中相对模糊的内容。
* **OpenAPI**：旧称 Swagger，用于构建和描述 API 的开放规范。

#### OAuth2PasswordBearer 的使用示例
~~~python
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# 指定获取 token 的 URL 路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # 对应 /token 接口

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
~~~

---

### 6-25 | 中间件 (Middleware)

中间件 (Middleware) 支持在请求处理之前和响应处理之后拦截并执行特定操作。
* **定义方式**：使用 `@app.middleware('http')` 装饰器。
* **入参要求**：必须接受 `request` 对象以及用于向下传递的 `call_next` 函数。

~~~python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    
    # 1. 往下执行请求获取响应对象
    response = await call_next(request)
    
    # 2. 后置处理计算耗时
    process_time = time.time() - start_time
    # 自定义添加响应头
    response.headers["X-Process-Time"] = str(process_time)  
    return response
~~~

---

### 6-26 | 跨域中间件 CORSMiddleware (CORS Middleware)

用于快速配置跨域 (CORS - Cross-Origin Resource Sharing) 权限。

~~~python
# 1. 引入中间件类
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

# 2. 定义信任的来源域名列表
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

# 3. 将中间件添加到 app 中
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # 是否支持跨域传输 Cookie
    allow_methods=["*"],     # 允许哪些 HTTP 请求方式 (GET, POST等)
    allow_headers=["*"],     # 允许携带哪些请求头
)
~~~
##### 其他可选高级设置项
* `max_age`：设置浏览器缓存 CORS 预检响应的最大时间（单位为秒）。
* `allow_origin_regex`：可以使用正则表达式字符串来定义符合规则的域名。
* `expose_headers`：定义允许跨域向浏览器暴露的自定义响应头部。

---

### 6-27 | 关系型数据库 (SQL Databases)

可以通过安装 `SQLAlchemy` 库来完成操作数据库。该章节内容主要为操作型项目架构，需结合实际动手实践。
* 参考官方文档：[SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)

---

### 6-28 | 多文件项目 (Bigger Applications)

#### 6-28-1 | APIRouter
**问题**：两个不同业务逻辑的 `.py` 文件如果都各自实例化了 `app = FastAPI()`，但在启动运行 Uvicorn 服务器时只能指定系统中的某一个独立 `app` 对象。
**解决方案**：引入 `APIRouter`（可将其视为迷你版的 `FastAPI`，支持其几乎所有参数）。

~~~python
# ----- 在子业务路由模块中 (e.g., users.py) -----
# 1. 引入
from fastapi import APIRouter

# 2. 实例化 router
router = APIRouter()

# 3. 使用 router 定义 API 路由，替代直接使用 app
@router.get("/users/")
async def get_users():
    return [{"username": "root"}]

# ----- 在主入口文件 main.py 中 -----
from fastapi import FastAPI
from users import router as users_router

app = FastAPI()

# 4. 在主实例 app 中进行注册导入，否则不会生效
app.include_router(users_router)
~~~
> 📌 路由之间也可以互相嵌套包含：`router.include_router(other_router)`。

#### 6-28-2 | 为路由加参
可以在包含注册时为一整组路由添加路径前缀 `prefix`（注意：⚠️ **前缀的结尾绝不能加 `/`**）：
~~~python
router = APIRouter(prefix="/items")
~~~
同一个 `router` 实例可以在主应用中根据实际需要被多次引入，并赋予不同的前缀。

为了避免路由的具体功能配置（如标签、依赖）分散在各个不同的子文件中，建议在 `app.include_router` 挂载注册时集中定义：
~~~python
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
~~~

#### 6-28-3 | 相对引用规范
在大型多文件项目中引用内部模块时，可采用点号形式进行相对导入：
* `.pkg.main import *`：从当前文件所在包的目录中找到模块 `pkg` 的文件 `main` 并引入所有。
* `..pkg.main import *`：从当前文件所在包的**父级目录**中找到对应的模块。
* `...pkg.main import *`：从当前文件所在包的**父级的父级目录**中找到对应的模块。

---

### 6-29 | 后台任务 (Background Tasks)

后台任务 (Background Tasks) 支持在系统完全返回请求响应后，继续在后台异步执行代码，不需要让客户端停在原地等待其执行完毕。

#### 6-29-1 | BackgroundTasks 直接作为参数
~~~python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

# 1. 定义具体的后台任务函数（同步或异步函数均可）
def task_func(param_a):
    # 执行耗时操作，例如写入 log 文件或发送邮件
    pass

# 2. 在路由中直接声明 BackgroundTasks 参数
@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    # 3. 调用 add_task() 触发，不需要写 async 或 await 关键字
    background_tasks.add_task(task_func, email)
    return {"message": "Notification sent in the background"}
~~~

#### 6-29-2 | 作为依赖注入使用
~~~python
from typing import Annotated
from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

# 依赖函数中同样支持注入 BackgroundTasks
def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q

@app.post("/send-notification-adv/{email}")
async def send_notification_adv(
    email: str, 
    background_tasks: BackgroundTasks, 
    q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
~~~

#### 6-29-3 | 什么时候该用 Celery?
如果执行的是极度繁琐、耗费大量 CPU 资源的复杂计算任务，则**不推荐**开后台任务直接在 FastAPI 进程中运行，使用功能更强大的分布式任务队列 **Celery** 效果更佳。
> 📌 FastAPI 自带的后台任务更适合需要快速获取 FastAPI 进程在内存中的资源（如共享变量、数据库连接对象）的情况，以及各种轻量级的“小型”后台任务。

---

### 6-30 | 元信息 (Metadata)

#### 6-30-1 | APP 级别元信息配置
可以在实例化 `FastAPI` 时传入各类参数，用以丰富和说明文档的全局信息：

| 参数名称 | 类型 | 描述 |
| :--- | :--- | :--- |
| `title` | `str` | API 文档的大标题。 |
| `description` | `str` | API 的简短详细介绍（支持使用 Markdown 语法）。 |
| `version` | `str` | 自定义应用软件的版本号，而非 OpenAPI 的版本。例如 `2.5.0`。 |
| `terms_of_service` | `str` | 指向 API 服务条款的有效 URL 地址。 |
| `contact` | `dict` | 开放 API 的联系人相关信息，可包含多个配置字段。 |
| `license_info` | `dict` | 开源证书协议相关信息。 |

##### 元信息配置示例
~~~python
from fastapi import FastAPI

description = """
ChimichangApp API helps you do awesome stuff.

## Items

You can **read items**.
"""

app = FastAPI(
    title="ChimichangApp",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={"name": "Deadpoolio the Amazing"},
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
~~~

---

### 6-31 | 静态资源 StaticFiles (Static Files)

用于将静态资源 (Static Files) 的物理文件夹目录直接挂载到指定的外部 URL 访问路径上。

~~~python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 将物理目录为 "static" 的文件夹挂载到访问路由 "/static" 下
app.mount("/static", StaticFiles(directory="static"), name="static")
~~~

---

### 6-32 | 测试 (Testing)

Starlette 的测试模块主要基于 `HTTPX`，而 `HTTPX` 又是完全基于广受欢迎的 `requests` 库风格进行设计的，因此测试可以直接完美接入并使用 `pytest` 框架。

#### 6-32-1 | TestClient
> ⚠️ **前提条件**：使用该类前必须先通过命令行安装 `pip install httpx`，否则系统会抛出 `ModuleNotFoundError` 错误。

~~~python
# ----- main.py -----
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

# ----- test_main.py -----
# 1. 导入测试客户端
from fastapi.testclient import TestClient
from main import app

# 2. 传入导入的 app 实例化客户端对象
client = TestClient(app)

# 3. 规范：用 test_ 开头的函数名称声明独立的测试用例 (Test Cases)
def test_read_main():
    response = client.get("/", headers={"X-Token": "asdas"})
    # 4. 使用 Python 标准关键字 assert 进行断言判断
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
~~~
定义好测试文件后，在控制台安装 `pip install pytest` 并进入对应目录下执行 `pytest` 指令，即可自动运行检查所有断言。

---

### 6-33 | 排除故障 (Debugging)

在开发过程中遇到问题，可以充分利用各类主流集成开发环境（IDE，如 PyCharm 或 VSCode）自带的调试工具进行断点和单步调试。这属于开发工具的基本使用方法，与 FastAPI 框架本身的 API 设计无太大直接关系。

---
**END**