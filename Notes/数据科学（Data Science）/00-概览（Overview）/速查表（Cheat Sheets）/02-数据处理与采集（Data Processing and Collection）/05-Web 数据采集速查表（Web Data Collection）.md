---
title: "Web 数据采集速查表（Web Data Collection Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - web-scraping
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "Python 3.11+；Requests 2.x；HTTPX 0.27+；Beautiful Soup 4.x；lxml 5.x/6.x；Selenium 4.x；Scrapy 2.x"
---
# Web 数据采集速查表（Web Data Collection Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
遵守 robots.txt、网站条款、版权、隐私和访问频率限制。Cookie、令牌、账号标识必须来自环境变量，不得写入代码、日志或 Git。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 2. 包级安装与导入索引（Package Installation and Import Index）
### 2.1 Requests 同步 HTTP（Requests Synchronous HTTP）
- **安装包（Distribution）**：`requests`。
- **导入模块（Import Module）**：`requests`。
- **安装命令（Installation）**：`python -m pip install -U requests`。
- **用途（Purpose）**：同步 HTTP 请求、会话、Cookie 与流式下载。
- **正式笔记（Detailed Note）**：[[04-HTTP 请求与反爬处理（HTTP Requests and Anti-scraping）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|GET|`requests.get(url, params=..., timeout=(3, 30))`|发起网络请求并返回 Response|
|会话|`requests.Session()`|返回持有连接池与 Cookie 的会话|
|状态检查|`response.raise_for_status()`|错误状态抛 `HTTPError`|
|JSON|`response.json()`|返回解码对象或抛 JSON 解码异常|

```python
import requests

request = requests.Request("GET", "https://example.com", params={"page": 1})
prepared = request.prepare()
print(prepared.method, prepared.url)  # 输出: GET https://example.com/?page=1
```
### 2.2 HTTPX 同步与异步 HTTP（HTTPX Sync and Async HTTP）
- **安装包（Distribution）**：`httpx`。
- **导入模块（Import Module）**：`httpx`。
- **安装命令（Installation）**：`python -m pip install -U httpx`。
- **用途（Purpose）**：统一同步/异步客户端、连接池、HTTP/2 与细粒度超时。
- **正式笔记（Detailed Note）**：[[04-HTTP 请求与反爬处理（HTTP Requests and Anti-scraping）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|同步客户端|`httpx.Client(timeout=10)`|返回可复用连接池客户端|
|异步客户端|`httpx.AsyncClient(timeout=10)`|返回异步客户端，必须关闭|
|GET|`client.get(url, params=...)`|返回 Response|
|状态检查|`response.raise_for_status()`|错误状态抛 `HTTPStatusError`|
|细分超时|`httpx.Timeout(10, connect=3)`|返回超时配置|

```python
import httpx

request = httpx.Request("POST", "https://example.com/api", json={"ok": True})
print(request.method, request.headers["content-type"])  # 输出: POST application/json
```
### 2.3 Beautiful Soup HTML 解析（Beautiful Soup HTML Parsing）
- **安装包（Distribution）**：`beautifulsoup4`。
- **导入模块（Import Module）**：`bs4`。
- **安装命令（Installation）**：`python -m pip install -U beautifulsoup4`；常与 `lxml` 解析器配合。
- **用途（Purpose）**：容错 HTML/XML 树解析和 CSS 选择器查询。
- **正式笔记（Detailed Note）**：[[03-网页解析：正则、XPath 与 Beautiful Soup（Web Parsing）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|解析|`BeautifulSoup(markup, 'html.parser')`|返回文档树|
|单个 CSS 查询|`soup.select_one(selector)`|返回首个 Tag 或 `None`|
|多个 CSS 查询|`soup.select(selector)`|返回 Tag 列表|
|查找|`soup.find(name, attrs=...)`|返回首个 Tag 或 `None`|
|文本|`tag.get_text(' ', strip=True)`|返回拼接后的字符串|
|安全属性|`tag.get('href')`|返回属性值或 `None`|

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup('<a class="item" href="/p">标题</a>', "html.parser")
link = soup.select_one("a.item")
print(link.get_text(strip=True), link.get("href"))  # 输出: 标题 /p
```
### 2.4 lxml XPath 与高速解析（lxml XPath and Parsing）
- **安装包（Distribution）**：`lxml`。
- **导入模块（Import Module）**：`lxml`。
- **安装命令（Installation）**：`python -m pip install -U lxml`。
- **用途（Purpose）**：高性能 HTML/XML 解析、XPath 和 CSSSelector。
- **正式笔记（Detailed Note）**：[[03-网页解析：正则、XPath 与 Beautiful Soup（Web Parsing）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|HTML 解析|`lxml.html.fromstring(text)`|返回 Element|
|XPath|`root.xpath(expression)`|返回节点、字符串、数字或布尔列表|
|序列化|`etree.tostring(node, encoding='unicode')`|返回字符串|
|XML 安全解析|`etree.fromstring(data, parser=parser)`|返回 Element；不可信 XML 应禁用实体与网络|

```python
from lxml import html

root = html.fromstring("<ul><li>A</li><li>B</li></ul>")
print(root.xpath("//li/text()"))  # 输出: ['A', 'B']
```
### 2.5 Selenium 浏览器自动化（Selenium Browser Automation）
- **安装包（Distribution）**：`selenium`。
- **导入模块（Import Module）**：`selenium`。
- **安装命令（Installation）**：`python -m pip install -U selenium`。
- **用途（Purpose）**：控制真实浏览器、等待动态页面、执行交互与获取渲染后 DOM。
- **正式笔记（Detailed Note）**：[[05-Selenium 浏览器自动化（Selenium Browser Automation）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|启动 Chrome|`webdriver.Chrome(options=options)`|启动浏览器进程并返回驱动|
|访问页面|`driver.get(url)`|执行网络导航并改变当前页面|
|定位元素|`driver.find_element(By.CSS_SELECTOR, selector)`|返回 WebElement 或抛异常|
|显式等待|`WebDriverWait(driver, 10).until(condition)`|返回条件结果或抛 TimeoutException|
|点击|`element.click()`|触发页面交互并可能改变 DOM|
|退出|`driver.quit()`|关闭窗口、会话与驱动进程|

```python
from selenium.webdriver.common.by import By

locator = (By.CSS_SELECTOR, "article a.title")
print(locator)  # 输出: ('css selector', 'article a.title')
# 真正启动浏览器需要本机浏览器/驱动并会访问网络；务必在 finally 中 driver.quit()。
```
### 2.6 Scrapy 与 ItemAdapter（Scrapy and ItemAdapter）
- **安装包（Distribution）**：`Scrapy`、`itemadapter`。
- **导入模块（Import Module）**：`scrapy`、`itemadapter`。
- **安装命令（Installation）**：`python -m pip install -U Scrapy itemadapter`。
- **用途（Purpose）**：事件驱动爬虫、请求调度、中间件、Item 管线与统一 Item 访问。
- **正式笔记（Detailed Note）**：[[07-Scrapy 与 Scrapy-Redis 框架（Scrapy and Scrapy-Redis Frameworks）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|定义爬虫|`class MySpider(scrapy.Spider): ...`|声明可被 Scrapy 加载的爬虫|
|生成请求|`scrapy.Request(url, callback=..., errback=...)`|返回未调度 Request|
|CSS 选择|`response.css(selector).getall()`|返回字符串列表|
|XPath 选择|`response.xpath(expression).get()`|返回首个字符串或 `None`|
|适配 Item|`ItemAdapter(item)`|返回统一映射接口，不复制数据|
|读取字段|`adapter.get(field, default)`|返回字段值或默认值|

```python
import scrapy
from itemadapter import ItemAdapter

item = {"title": "Example"}
adapter = ItemAdapter(item)
adapter["url"] = "https://example.com"
request = scrapy.Request(adapter["url"])
print(adapter["title"], request.method)  # 输出: Example GET
```
### 2.7 Scrapy-Redis 分布式调度（Scrapy-Redis Distributed Scheduling）
- **安装包（Distribution）**：`scrapy-redis`。
- **导入模块（Import Module）**：`scrapy_redis`。
- **安装命令（Installation）**：`python -m pip install -U scrapy-redis`。
- **用途（Purpose）**：用 Redis 共享请求队列、去重集合和起始 URL。
- **正式笔记（Detailed Note）**：[[07-Scrapy 与 Scrapy-Redis 框架（Scrapy and Scrapy-Redis Frameworks）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|Redis Spider|`class Spider(RedisSpider)`|从 Redis 键持续读取起始 URL|
|起始键|`redis_key = 'spider:start_urls'`|指定外部队列键名|
|调度器|`SCHEDULER='scrapy_redis.scheduler.Scheduler'`|把请求队列迁移到 Redis|
|持久队列|`SCHEDULER_PERSIST=True`|进程退出后保留队列与去重状态|

```python
from scrapy_redis.spiders import RedisSpider

class ProductSpider(RedisSpider):
    name = "products"
    redis_key = "products:start_urls"

print(ProductSpider.name, ProductSpider.redis_key)  # 输出: products products:start_urls
```
- **状态边界（State Boundary）**：生产环境要为不同项目设置独立 namespace；清理 Redis 键会丢失队列和去重状态。
### 2.8 ddddocr 验证码识别（ddddocr Captcha Recognition）
- **安装包（Distribution）**：`ddddocr`。
- **导入模块（Import Module）**：`ddddocr`。
- **安装命令（Installation）**：`python -m pip install -U ddddocr`。
- **用途（Purpose）**：本地图片验证码分类与滑块匹配。
- **正式笔记（Detailed Note）**：[[04-HTTP 请求与反爬处理（HTTP Requests and Anti-scraping）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|分类器|`ddddocr.DdddOcr(show_ad=False)`|加载模型并返回识别器|
|文字识别|`ocr.classification(image_bytes)`|返回识别字符串|
|滑块匹配|`ocr.slide_match(target, background)`|返回匹配坐标字典|

```python
import ddddocr

ocr = ddddocr.DdddOcr(show_ad=False)
# text = ocr.classification(open("captcha.png", "rb").read())
# 会读取本地图片并加载模型；识别结果依赖图像，且只能用于获授权的自动化场景。
```
### 2.9 PyExecJS 与 PyCryptodome（JavaScript Execution and Cryptography）
- **安装包（Distribution）**：`PyExecJS`、`pycryptodome`。
- **导入模块（Import Module）**：`execjs`、`Crypto`。
- **安装命令（Installation）**：`python -m pip install PyExecJS pycryptodome`；`PyExecJS` 还需要 Node.js 等 JavaScript 运行时。
- **用途（Purpose）**：复用页面 JavaScript 算法，以及执行标准加密/编码操作。
- **正式笔记（Detailed Note）**：[[08-逆向分析与加密基础（Reverse Engineering and Cryptography Basics）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|编译 JavaScript|`execjs.compile(source)`|启动/连接 JS 运行时并返回上下文|
|调用函数|`context.call(name, *args)`|返回可序列化结果或抛运行时异常|
|SHA-256|`SHA256.new(data).hexdigest()`|返回十六进制摘要，不修改输入|
|AES 密钥|`AES.new(key, mode, iv=...)`|返回有内部状态的密码对象|
|随机字节|`get_random_bytes(length)`|返回密码学安全随机 bytes|

```python
import execjs
from Crypto.Hash import SHA256

context = execjs.compile("function add(a, b) { return a + b; }")
print(context.call("add", 2, 3))  # 输出: 5
print(SHA256.new(b"abc").hexdigest())  # 输出: ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
```
- **安全边界（Security Boundary）**：不得执行来源不可信的 JavaScript；加密示例不得自行设计协议，密钥与 IV 必须来自安全配置并遵循所选算法要求。
### 2.10 cryptography 与 pyOpenSSL（TLS and Cryptography Bindings）
- **安装包（Distribution）**：`cryptography`、`pyOpenSSL`。
- **导入模块（Import Module）**：`cryptography`、`OpenSSL`。
- **安装命令（Installation）**：`python -m pip install -U cryptography pyOpenSSL`；不要长期固定正式笔记中的旧版本作为通用解法。
- **用途（Purpose）**：现代密码学原语、证书与 OpenSSL Python 绑定；Scrapy/Twisted 的 TLS 链路可能间接依赖它们。
- **正式笔记（Detailed Note）**：[[07-Scrapy 与 Scrapy-Redis 框架（Scrapy and Scrapy-Redis Frameworks）]]、[[08-逆向分析与加密基础（Reverse Engineering and Cryptography Basics）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|生成 Fernet 密钥|`Fernet.generate_key()`|返回 URL-safe 随机 bytes|
|加密|`Fernet(key).encrypt(data)`|返回带认证的密文 token|
|解密|`Fernet(key).decrypt(token, ttl=None)`|返回明文；无效/过期 token 抛异常|
|TLS 上下文|`SSL.Context(method)`|返回 OpenSSL 上下文|

```python
from cryptography.fernet import Fernet
from OpenSSL import SSL

key = Fernet.generate_key()
token = Fernet(key).encrypt(b"data")
print(Fernet(key).decrypt(token))  # 输出: b'data'
print(hasattr(SSL, "Context"))  # 输出: True
```
- **兼容边界（Compatibility Boundary）**：`cryptography`、`pyOpenSSL`、OpenSSL、Twisted 和 Python 版本必须兼容；遇到属性缺失应先升级成兼容组合，不盲目照搬旧版降级命令。
### 2.11 pywin32 Windows 集成（pywin32 Windows Integration）
- **安装包（Distribution）**：`pywin32`，仅适用于 Windows。
- **导入模块（Import Module）**：按功能为 `win32api`、`win32com`、`win32service` 等，不存在统一 `import pywin32`。
- **安装命令（Installation）**：在 Windows 环境执行 `python -m pip install -U pywin32`。
- **用途（Purpose）**：访问 Win32 API、COM、服务和 Windows 特有系统能力；部分旧工具链可能间接需要。
- **正式笔记（Detailed Note）**：[[07-Scrapy 与 Scrapy-Redis 框架（Scrapy and Scrapy-Redis Frameworks）]] 的 Windows 环境说明。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|系统版本|`win32api.GetVersionEx()`|返回 Windows 版本元组|
|COM 分派|`win32com.client.Dispatch(prog_id)`|启动/连接 COM 对象并返回代理|
|Windows 服务|`win32serviceutil.QueryServiceStatus(name)`|返回服务状态元组|

```python
import sys

if sys.platform == "win32":
    import win32api
    print(win32api.GetVersionEx()[0])
else:
    print("pywin32 仅适用于 Windows")  # 输出（macOS/Linux）: pywin32 仅适用于 Windows
```
### 2.12 Twisted 事件驱动网络（Twisted Event-driven Networking）
- **安装包（Distribution）**：`Twisted`。
- **导入模块（Import Module）**：`twisted`。
- **安装命令（Installation）**：通常由 Scrapy 自动解析兼容版本；需要直接使用时执行 `python -m pip install -U Twisted`。
- **用途（Purpose）**：Scrapy 底层的事件循环、异步网络协议和 Deferred 回调模型。
- **正式笔记（Detailed Note）**：[[07-Scrapy 与 Scrapy-Redis 框架（Scrapy and Scrapy-Redis Frameworks）]]。

```python
from twisted.internet.defer import succeed

deferred = succeed(2)
deferred.addCallback(lambda value: value * 3)
deferred.addCallback(lambda value: print(value))  # 输出: 6
```
- **版本边界（Version Boundary）**：不要从历史笔记复制某个旧 wheel 文件名；让当前 Python、Scrapy、Twisted 与 OpenSSL 依赖解析为兼容组合。
## HTTP 请求与会话（Requests and Sessions）
先处理超时、状态码、编码、重试与限速，再解析内容。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|GET|`requests.get(url, params=params, timeout=(3,30))`|返回 Response|
|POST 表单|`requests.post(url, data=form, timeout=30)`|返回 Response|
|POST JSON|`requests.post(url, json=payload, timeout=30)`|返回 Response|
|会话|`requests.Session()`|返回复用连接与 Cookie 的 Session|
|状态检查|`response.raise_for_status()`|错误状态抛 HTTPError|
|响应文本|`response.text`|返回按检测编码解码的 str|
|响应字节|`response.content`|返回 bytes|
|响应 JSON|`response.json()`|返回 Python 对象或抛解码异常|
|流式读取|`response.iter_content(chunk_size=8192)`|返回字节块迭代器|
|自定义头|`session.headers.update(headers)`|原地修改会话默认头|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import requests
response = requests.get("https://example.com", timeout=(3.05, 30))
response.raise_for_status()
print(response.status_code, response.headers.get("content-type"))
# 网络结果会变化，不提供固定输出。
```
## HTML 与 CSS/XPath 解析（HTML Parsing）
选择器应基于稳定语义属性，并对缺失节点做显式处理。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|解析 HTML|`BeautifulSoup(html, 'html.parser')`|返回 BeautifulSoup 文档|
|首个 CSS 节点|`soup.select_one('article h2')`|返回 Tag 或 None|
|全部 CSS 节点|`soup.select('a[href]')`|返回 Tag 列表|
|文本|`node.get_text(' ', strip=True)`|返回清理后的 str|
|属性|`node.get('href')`|返回属性值或 None|
|删除节点|`node.decompose()`|从树移除并销毁节点|
|解析 XML/HTML|`lxml.html.fromstring(content)`|返回 Element|
|XPath|`root.xpath('//a/@href')`|返回匹配列表|
|绝对链接|`urllib.parse.urljoin(base, href)`|返回规范化 URL|
|查询参数|`urllib.parse.urlencode(params)`|返回编码后的查询串|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from bs4 import BeautifulSoup
from urllib.parse import urljoin
html = '<article><h2>Title</h2><a href="/x">Go</a></article>'
soup = BeautifulSoup(html, "html.parser")
print(soup.select_one("h2").get_text(strip=True))
print(urljoin("https://example.com/base/", soup.a["href"]))
# 期望输出:
# Title
# https://example.com/x
```
## Selenium 动态页面（Selenium Browser Automation）
用显式等待同步页面状态，避免固定 sleep；结束时关闭浏览器。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|启动浏览器|`webdriver.Chrome(options=options)`|返回 WebDriver，有 UI/进程副作用|
|打开页面|`driver.get(url)`|导航并返回 None|
|单元素|`driver.find_element(By.CSS_SELECTOR, selector)`|返回 WebElement；未找到抛 NoSuchElementException|
|多元素|`driver.find_elements(...)`|返回列表，未找到为空|
|显式等待|`WebDriverWait(driver, seconds).until(condition)`|返回条件值或抛 TimeoutException|
|点击|`element.click()`|触发交互，返回 None|
|输入|`element.send_keys(text)`|输入按键，返回 None|
|属性|`element.get_attribute(name)`|返回字符串或 None|
|截图|`driver.save_screenshot(path)`|写图片并返回成功布尔值|
|关闭|`driver.quit()`|关闭全部窗口与驱动进程|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
try:
    driver.get("https://example.com")
    heading = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
    print(heading.text)
finally:
    driver.quit()
# 浏览器和网络操作有外部副作用。
```
## Scrapy 抓取流程（Scrapy Crawling）
Spider 产生 Request 或 Item；Pipeline 负责清洗、验证与持久化。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|定义爬虫|`class ItemSpider(scrapy.Spider)`|创建 Spider 类型|
|初始地址|`start_urls = [...]`|调度初始 GET 请求|
|生成请求|`yield scrapy.Request(url, callback=self.parse)`|加入调度队列|
|CSS 取首项|`response.css('h1`|text').get()::返回字符串或 None|
|CSS 取全部|`response.css('a`|attr(href)').getall()::返回字符串列表|
|XPath|`response.xpath('//h1/text()').get()`|返回首个值或 None|
|跟随链接|`response.follow(href, callback=...)`|返回 Request|
|复制请求|`request.replace(headers=..., dont_filter=True)`|返回新 Request|
|输出 Item|`yield {'field': value}`|交给 Pipeline/Feed Export|
|运行|`scrapy crawl spider -O output.jsonl`|运行爬虫并覆盖输出文件|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import scrapy
class TitleSpider(scrapy.Spider):
    name = "titles"
    start_urls = ["https://example.com"]
    def parse(self, response):
        yield {"title": response.css("h1::text").get()}
# 网络抓取与文件导出有外部副作用。
```
## 数据校验、存储与增量（Validation, Storage, and Incremental Runs）
抓取结果先标准化、验证、去重，再批量持久化。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|数据模型|`pydantic.BaseModel`|定义并验证字段类型|
|URL 去重|`hashlib.sha256(canonical_url.encode()).hexdigest()`|返回稳定摘要|
|内容摘要|`hashlib.sha256(content).hexdigest()`|返回十六进制哈希|
|时间戳|`datetime.now(timezone.utc).isoformat()`|返回 UTC ISO 字符串|
|JSON Lines|`json.dumps(item, ensure_ascii=False)`|返回单行 JSON|
|CSV 写入|`csv.DictWriter(...).writerow(item)`|写一行，有文件副作用|
|SQLite 参数写入|`cursor.execute(sql, params)`|执行参数化语句|
|幂等更新|`INSERT ... ON CONFLICT ... DO UPDATE`|重复键时更新|
|缓存验证|`If-None-Match / If-Modified-Since`|服务未变时可返回 304|
|限速|`time.sleep(delay) / AutoThrottle`|降低请求频率|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import hashlib
from urllib.parse import urlsplit, urlunsplit
url = "HTTPS://Example.com/path#fragment"
p = urlsplit(url)
canonical = urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path, p.query, ""))
print(canonical)
print(len(hashlib.sha256(canonical.encode()).hexdigest()))
# 期望输出:
# https://example.com/path
# 64
```
## 失败恢复与安全（Recovery and Security）
对暂时性失败有限重试；对认证失败、解析结构变化与法律限制立即停止。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|指数退避|`delay = min(cap, base * 2 ** attempt)`|返回当前等待秒数|
|尊重 Retry-After|`response.headers.get('Retry-After')`|返回服务端等待建议或 None|
|代理配置|`proxies={'https': os.environ['HTTPS_PROXY']}`|从环境读取代理|
|凭据读取|`os.environ['SCRAPY_LOGIN_COOKIE']`|返回本地环境值；缺失抛 KeyError|
|Cookie 解析|`session.cookies.update(cookie_dict)`|原地更新 CookieJar|
|日志脱敏|`logger.info('request_id=%s', request_id)`|只记录非敏感标识|
|响应尺寸限制|`读取 Content-Length 并限制流式累计字节`|超过阈值时停止|
|内容类型检查|`response.headers.get('content-type')`|返回 MIME 信息|
|编码兜底|`response.encoding = response.apparent_encoding`|原地覆盖推测编码|
|断点记录|`保存游标、页码或最近主键`|产生本地状态，有外部副作用|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import os
cookie = os.getenv("SCRAPY_LOGIN_COOKIE")
print(cookie is None or isinstance(cookie, str))
# 期望输出:
# True
```
## 高频工作模式（Common Workflows）
- **最小闭环（Minimum Loop）**：先用最小输入跑通读取、转换、验证与输出，再替换真实数据。
- **组合优先（Composition First）**：把解析、业务逻辑和 I/O 分层，便于单元测试和复用。
- **可观测性（Observability）**：在边界处记录输入规模、关键参数、耗时和异常，不记录凭据。
- **可复现性（Reproducibility）**：固定随机种子、依赖版本和配置，并保存数据与模型版本。
## 常见错误与排查（Common Errors and Troubleshooting）
- **类型或形状不匹配**：先打印 `type`、`dtype`、`shape`，再检查广播、索引和设备。
- **隐式修改**：链式操作前确认是否原地修改；必要时显式复制并写测试。
- **边界遗漏**：至少覆盖空输入、单元素、重复值、极端值和非法参数。
- **版本漂移**：遇到弃用警告时查询当前官方迁移说明，不长期屏蔽警告。
## 相关详细笔记（Detailed Notes）
- [[01-Python 爬虫前置基础（Python Prerequisites for Web Scraping）]]
- [[02-HTML 与 CSS 页面结构（HTML and CSS Page Structure）]]
- [[03-网页解析：正则、XPath 与 Beautiful Soup（Web Parsing）]]
- [[04-HTTP 请求与反爬处理（HTTP Requests and Anti-scraping）]]
- [[05-Selenium 浏览器自动化（Selenium Browser Automation）]]
- [[06-爬虫数据存储：MySQL 与 Redis（Crawler Data Storage）]]
- [[07-Scrapy 与 Scrapy-Redis 框架（Scrapy and Scrapy-Redis Frameworks）]]
- [[08-逆向分析与加密基础（Reverse Engineering and Cryptography Basics）]]
## 官方参考（Official References）
- [Requests 文档](https://requests.readthedocs.io/en/latest/)
- [Beautiful Soup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Selenium Python 文档](https://www.selenium.dev/documentation/webdriver/)
- [Scrapy 文档](https://docs.scrapy.org/en/latest/)
- [HTTPX 文档](https://www.python-httpx.org/)
- [lxml 文档](https://lxml.de/)
- [Scrapy-Redis 官方仓库](https://github.com/rmax/scrapy-redis)
- [ItemAdapter 文档](https://docs.scrapy.org/en/latest/topics/item-pipeline.html)
- [PyCryptodome 文档](https://www.pycryptodome.org/)
