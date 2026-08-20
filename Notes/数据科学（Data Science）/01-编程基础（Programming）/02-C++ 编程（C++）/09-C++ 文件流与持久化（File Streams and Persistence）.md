---
title: C++ 文件流与持久化（File Streams and Persistence）
status: published
detail_level: comprehensive
published_at: 2026-08-17
updated_at: 2026-08-17
---
# C++ 文件流与持久化（File Streams and Persistence）
## 1. 文件流类型（File-stream Types）
- `std::ifstream`：输入文件流（Input File Stream）。
- `std::ofstream`：输出文件流（Output File Stream）。
- `std::fstream`：同时读写。
- 头文件为 `<fstream>`；流对象析构时自动关闭文件，但应显式检查打开和读写状态。

## 2. 打开模式（Open Modes）

|模式|含义|
|---|---|
|`std::ios::in`|读取|
|`std::ios::out`|写入|
|`std::ios::app`|每次写入都定位到末尾|
|`std::ios::ate`|打开后初始定位到末尾，之后仍可移动|
|`std::ios::trunc`|打开时截断已有内容|
|`std::ios::binary`|二进制模式|

- 模式可用按位或 `|` 组合。
- `out` 的默认行为可能截断现有文件；需要追加时明确使用 `app`。
- 文件路径应优先使用 `std::filesystem::path`，并明确相对路径基于当前工作目录而非源文件目录。

## 3. 文本文件（Text Files）
```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    std::ifstream input("employees.txt");
    if (!input) {
        std::cerr << "cannot open employees.txt\n";
        return 1;
    }

    std::string line;
    while (std::getline(input, line)) {
        std::cout << line << '\n';
    }
    if (!input.eof()) {
        std::cerr << "read failed before EOF\n";
        return 1;
    }
}
```
- 正确读取循环是 `while (std::getline(stream, line))` 或 `while (stream >> value)`，不要使用 `while (!stream.eof())`；EOF 只有读取失败后才设置。
- `operator>>` 按空白分词，`getline()` 保留行内空格。混用时前一次格式化读取遗留的换行符可能让 `getline()` 立刻读到空行，可用 `std::ws` 消费前导空白。
- 输出后应检查流状态；磁盘满、权限变化等错误可能在写入或刷新阶段才出现。

## 4. 二进制文件（Binary Files）
`read()` 与 `write()` 处理字节序列，但直接序列化对象内存具有严格边界：
- 指针值、虚表指针和动态资源不能直接持久化。
- 填充字节（Padding）、字节序（Endianness）、类型宽度和编译器 ABI 可能变化。
- 含 `std::string`、`std::vector` 或虚函数的对象不能通过 `reinterpret_cast<char*>` 整体写入后可靠恢复。
- 稳定格式应逐字段编码，并记录版本、长度和校验信息；跨平台可使用 JSON、Protocol Buffers、MessagePack 等明确格式。

> [!tip] 大白话理解（Plain-language Intuition）
> 把对象内存整块写进文件，像把“仓库地址”写进清单而不是把仓库里的货物写进去。程序重启后原地址已经无效，所以必须真正序列化字段内容，而不是保存指针。

## 5. 随机访问与位置（Random Access and Positions）
- 输入位置：`tellg()`、`seekg()`。
- 输出位置：`tellp()`、`seekp()`。
- 文本模式的位置不一定等同于简单字节偏移；固定记录随机访问通常使用二进制模式和明确记录布局。
- 每次移动后检查流状态；之前的失败位可能需要先 `clear()` 再 `seekg()`。

## 6. 持久化设计（Persistence Design）
- 使用临时文件写完整内容并原子替换，降低中途崩溃损坏原文件的风险。
- 明确编码，文本通常使用 UTF-8。
- 为记录定义版本字段和迁移策略。
- 对用户输入进行转义或使用成熟 CSV/JSON 库，不能简单用逗号拼接任意文本。
- 敏感信息如密码、令牌不能明文保存；密码使用专用密码哈希算法并加盐。
- 多进程或多线程写同一文件需要锁和冲突策略。

## 7. 常见错误（Common Errors）
- 未检查文件是否成功打开。
- 使用 `while (!eof())` 多处理一次旧数据。
- 默认 `out` 意外截断文件。
- 把对象指针或含动态成员对象原样写入二进制文件。
- 假设相对路径相对于 `.cpp` 文件。
- 读取失败后未区分正常 EOF、格式错误和 I/O 错误。

## 8. 相关笔记（Related Notes）
- [[04-C++ 指针、引用、数组与字符串（Pointers References Arrays and Strings）]]
- [[08-C++ 类、对象、继承与多态（Classes, Inheritance, and Polymorphism）]]
- [[系统案例（System Examples）/03-机房预约系统（Computer Room Reservation System）]]
