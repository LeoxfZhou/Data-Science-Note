---
title: "SQL、MySQL 与 Redis 速查表（SQL, MySQL, and Redis Cheat Sheet）"
tags:
  - data-science/cheat-sheet
  - database
status: published
detail_level: comprehensive-cheat-sheet
verified_at: 2026-09-10
version_scope: "SQL:2016 常用子集；MySQL 8.x；Redis 7.x"
---
# SQL、MySQL 与 Redis 速查表（SQL, MySQL, and Redis Cheat Sheet）
## 1. 安装、导入与版本范围（Setup and Version Scope）
SQL 操作用参数化查询；事务中明确提交/回滚。Redis 是内存数据结构服务，不代替需要复杂关系约束的数据库。
> [!important] 版本边界（Version Boundary）
> 本页只整理公开、稳定或长期常用的接口。版本敏感行为以 `version_scope` 和文末官方文档为准；升级依赖后应重新运行示例与测试。
## 2. Python 数据库驱动包（Python Database Driver Packages）
### 2.1 PyMySQL（PyMySQL）
- **安装包（Distribution）**：`PyMySQL`。
- **导入模块（Import Module）**：`pymysql`。
- **安装命令（Installation）**：`python -m pip install -U PyMySQL`。
- **用途（Purpose）**：通过 Python DB-API 访问 MySQL/MariaDB。
- **正式笔记（Detailed Note）**：[[06-爬虫数据存储：MySQL 与 Redis（Crawler Data Storage）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|连接|`pymysql.connect(host=..., user=..., password=..., database=...)`|建立网络连接并返回 Connection|
|字典游标|`cursorclass=pymysql.cursors.DictCursor`|查询行返回字典|
|执行|`cursor.execute(sql, params)`|返回受影响行数并改变事务状态|
|取一行|`cursor.fetchone()`|返回一行或 `None`|
|取全部|`cursor.fetchall()`|返回剩余行序列|
|提交|`connection.commit()`|持久化当前事务，具有数据库副作用|
|回滚|`connection.rollback()`|撤销当前未提交事务|
|关闭|`connection.close()`|释放连接资源|

```python
import os
import pymysql

# connection = pymysql.connect(
#     host=os.getenv("MYSQL_HOST", "127.0.0.1"),
#     user=os.environ["MYSQL_USER"],
#     password=os.environ["MYSQL_PASSWORD"],
#     database=os.environ["MYSQL_DATABASE"],
#     autocommit=False,
# )
# 连接依赖外部数据库；写操作必须使用参数化 SQL 并显式提交或回滚。
print(pymysql.paramstyle)  # 输出: pyformat
```
### 2.2 redis-py（Redis Python Client）
- **安装包（Distribution）**：`redis`。
- **导入模块（Import Module）**：`redis`。
- **安装命令（Installation）**：`python -m pip install -U redis`。
- **用途（Purpose）**：访问 Redis 字符串、哈希、集合、队列、事务和连接池。
- **正式笔记（Detailed Note）**：[[06-爬虫数据存储：MySQL 与 Redis（Crawler Data Storage）]]。

|功能（Operation）|实际写法（Python Usage）|返回值与状态变化|
|---|---|---|
|客户端|`redis.Redis.from_url(url, decode_responses=True)`|返回惰性连接客户端|
|连通检查|`client.ping()`|请求成功返回 `True`|
|写字符串|`client.set(key, value, ex=seconds, nx=True)`|写入并返回成功状态|
|读字符串|`client.get(key)`|返回值或 `None`|
|哈希写入|`client.hset(name, mapping=data)`|返回新增字段数|
|列表入队|`client.rpush(key, *values)`|修改列表并返回新长度|
|管道|`client.pipeline(transaction=True)`|返回批处理/事务管道|
|扫描|`client.scan_iter(match=pattern, count=100)`|惰性返回键；避免生产环境使用 `KEYS *`|

```python
import redis

client = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)
print(client.connection_pool.connection_kwargs["port"])  # 输出: 6379
# ping/get/set 会连接外部 Redis；示例不执行写入，也不提供固定服务输出。
```
- **边界（Boundary）**：连接对象创建不代表服务可用；键过期、序列化格式和命名空间必须由应用统一管理。
## SQL 查询与聚合（SQL Query and Aggregation）
逻辑顺序约为 FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT。

|功能（Operation）|实际写法（SQL / Python Usage）|返回值与状态变化|
|---|---|---|
|选择列|`SELECT col1, col2 FROM table;`|返回结果集|
|条件过滤|`WHERE score >= %s AND status = %s`|过滤行；参数由驱动绑定|
|排序分页|`ORDER BY created_at DESC LIMIT %s OFFSET %s`|返回指定窗口|
|去重|`SELECT DISTINCT col FROM table;`|返回唯一组合|
|聚合|`COUNT(*), SUM(x), AVG(x), MIN(x), MAX(x)`|每组返回聚合值|
|分组|`GROUP BY key`|每个键产生一组|
|聚合后过滤|`HAVING COUNT(*) > 1`|过滤分组结果|
|条件表达式|`CASE WHEN cond THEN a ELSE b END`|返回逐行条件值|
|空值替代|`COALESCE(a, b, default)`|返回首个非 NULL 值|
|集合查询|`UNION ALL`|拼接结果并保留重复|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```sql
SELECT department, COUNT(*) AS n, AVG(score) AS avg_score
FROM employees
WHERE active = 1
GROUP BY department
HAVING COUNT(*) >= 2
ORDER BY avg_score DESC;
-- 输出取决于数据库当前数据。
```
## 连接、子查询与窗口（Joins, Subqueries, and Windows）
连接前先判断一对一、一对多或多对多，避免意外笛卡尔积。

|功能（Operation）|实际写法（SQL / Python Usage）|返回值与状态变化|
|---|---|---|
|内连接|`a INNER JOIN b ON a.id = b.a_id`|仅返回匹配行|
|左连接|`a LEFT JOIN b ON ...`|保留 a 全部行，未匹配 b 为 NULL|
|交叉连接|`a CROSS JOIN b`|返回笛卡尔积|
|存在判断|`WHERE EXISTS (SELECT 1 FROM b WHERE ...)`|按相关子查询返回布尔过滤|
|公共表表达式|`WITH cte AS (...) SELECT ...`|定义查询级临时结果|
|递归 CTE|`WITH RECURSIVE ...`|递归生成层级或序列|
|行号|`ROW_NUMBER() OVER (PARTITION BY k ORDER BY t)`|返回每组连续编号|
|排名|`RANK() OVER (...)`|并列值同排名并留间隔|
|滞后值|`LAG(value) OVER (ORDER BY time)`|返回前一行值|
|滚动聚合|`SUM(x) OVER (ORDER BY t ROWS BETWEEN ... )`|返回不缩减行数的窗口结果|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```sql
WITH ranked AS (
  SELECT user_id, score,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY score DESC) AS rn
  FROM attempts
)
SELECT user_id, score FROM ranked WHERE rn = 1;
-- 输出为每位用户的最高分记录。
```
## 写入、约束与事务（Mutation, Constraints, and Transactions）
约束在数据库层保护不变量；事务提供原子性。

|功能（Operation）|实际写法（SQL / Python Usage）|返回值与状态变化|
|---|---|---|
|插入|`INSERT INTO t (a,b) VALUES (%s,%s);`|新增行并返回受影响行数|
|批量插入|`INSERT INTO t (...) VALUES (...), (...);`|一次新增多行|
|更新|`UPDATE t SET status=%s WHERE id=%s;`|修改匹配行；必须检查条件|
|删除|`DELETE FROM t WHERE id=%s;`|删除匹配行；高风险外部副作用|
|主键|`PRIMARY KEY (id)`|强制唯一且非空|
|唯一约束|`UNIQUE (email)`|阻止重复值|
|外键|`FOREIGN KEY (...) REFERENCES ...`|维护引用完整性|
|事务开始|`START TRANSACTION;`|开启显式事务|
|提交|`COMMIT;`|永久提交事务变更|
|回滚|`ROLLBACK;`|撤销未提交变更|
|幂等更新|`INSERT ... ON DUPLICATE KEY UPDATE ...`|MySQL 插入或更新|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- 属于数据库写入操作，不提供固定输出。
```
## MySQL 索引、执行计划与 Python 驱动（MySQL and Drivers）
索引加速读取但增加写入成本；以真实查询计划验证。

|功能（Operation）|实际写法（SQL / Python Usage）|返回值与状态变化|
|---|---|---|
|创建索引|`CREATE INDEX idx_name ON t (a, b);`|创建 B-tree 索引|
|唯一索引|`CREATE UNIQUE INDEX ...`|创建并强制唯一|
|执行计划|`EXPLAIN ANALYZE SELECT ...`|执行并返回实际计划与耗时|
|表结构|`SHOW CREATE TABLE t;`|返回建表语句|
|连接|`mysql.connector.connect(**config)`|返回连接；有网络/数据库副作用|
|参数查询|`cursor.execute(sql, params)`|执行绑定参数查询，返回 None|
|批量执行|`cursor.executemany(sql, rows)`|执行多组参数|
|取一行|`cursor.fetchone()`|返回行或 None|
|取全部|`cursor.fetchall()`|返回剩余行列表|
|提交连接|`connection.commit()`|提交事务|
|回滚连接|`connection.rollback()`|撤销事务|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import os, mysql.connector
conn = mysql.connector.connect(host=os.environ["DB_HOST"], user=os.environ["DB_USER"], password=os.environ["DB_PASSWORD"])
with conn.cursor(dictionary=True) as cur:
    cur.execute("SELECT id, name FROM users WHERE id = %s", (1,))
    row = cur.fetchone()
conn.close()
# 数据库读取结果取决于外部状态。
```
## Redis 常用数据结构（Redis Data Structures）
选择键过期策略、序列化格式和原子性；不要用 `KEYS *` 扫描生产库。

|功能（Operation）|实际写法（SQL / Python Usage）|返回值与状态变化|
|---|---|---|
|字符串写入|`SET key value EX seconds NX`|成功返回 OK，条件不满足返回空|
|字符串读取|`GET key`|返回字节/字符串或空|
|计数|`INCR key`|原子递增并返回新整数|
|哈希写入|`HSET key field value`|返回新增字段数|
|哈希读取|`HGETALL key`|返回字段值映射|
|列表入队|`LPUSH key value`|返回列表长度|
|阻塞出队|`BRPOP key timeout`|返回键和值或超时空值|
|集合加入|`SADD key member`|返回新增成员数|
|有序集合|`ZADD key score member`|返回新增成员数|
|范围排名|`ZRANGE key start stop WITHSCORES`|返回成员及分数|
|过期|`EXPIRE key seconds`|返回是否设置成功|
|扫描|`SCAN cursor MATCH pattern COUNT n`|返回新游标与键列表|

### 参数与边界（Parameters and Boundaries）
- **输入检查（Input Validation）**：先确认类型、形状、编码、空值与取值范围。
- **副作用（Side Effect）**：区分返回新对象、原地修改与外部状态变更。
- **失败处理（Failure Handling）**：捕获具体异常并保留足够上下文，不用空的 `except` 吞掉错误。

### 组合示例（Combined Example）
```python
import redis
r = redis.Redis.from_url("redis://localhost:6379/0", decode_responses=True)
with r.pipeline(transaction=True) as pipe:
    result = pipe.hset("user:1", mapping={"name": "A"}).expire("user:1", 3600).execute()
print(result)  # 依赖本地 Redis，典型结果为 [1, True]
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
- [[06-爬虫数据存储：MySQL 与 Redis（Crawler Data Storage）]]
- [[07-Scrapy 与 Scrapy-Redis 框架（Scrapy and Scrapy-Redis Frameworks）]]
## 官方参考（Official References）
- [PyMySQL 文档](https://pymysql.readthedocs.io/)
- [redis-py 文档](https://redis.readthedocs.io/)
- [MySQL 8.4 参考](https://dev.mysql.com/doc/refman/8.4/en/)
- [Redis 命令参考](https://redis.io/docs/latest/commands/)
