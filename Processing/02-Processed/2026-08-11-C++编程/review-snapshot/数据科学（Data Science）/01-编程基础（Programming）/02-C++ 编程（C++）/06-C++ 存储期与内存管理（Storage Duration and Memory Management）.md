---
title: C++ 存储期与内存管理（Storage Duration and Memory Management）
status: review
detail_level: comprehensive
merge_policy: union-zero-loss
reviewed_at: 2026-08-11
sources:
  - "Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/02-C++ 编程（C++）/函数进阶与内存管理.md"
suggested_target: "Notes/数据科学（Data Science）/01-编程基础（Programming）/02-C++ 编程（C++）/06-C++ 存储期与内存管理（Storage Duration and Memory Management）.md"
operation: 新建
merge_target: null
---

# C++ 存储期与内存管理（Storage Duration and Memory Management）

> [!info] 候选稿状态（Draft Status）
> 本文仅写入 `Processing/01-Review/`，等待人工检查；对应 Inbox 原稿未移动、未删除、未修改。

本文整理栈、动态存储、全局/局部/静态对象以及裸内存管理，并补入现代 C++ 的 RAII 默认方案。

## 三、`new` 和 `delete`，`new []` 和 `delete []`
**概念：** 在 C++ 中，内存就像一块可以自由分配和回收的土地。当我们声明一个变量时，系统会自动在合适的地方（例如栈区）为它分配内存。但有时我们需要在程序运行的过程中动态地申请内存，这时就需要用到 `new` 运算符；当我们不再需要这块内存时，需要使用 `delete` 运算符将其归还给系统，防止“内存垃圾”堆积。
- **`new`****：** 用于在**堆区 (Heap)** 动态地分配一块指定类型的内存空间，并返回指向该内存空间的指针。就像向操作系统申请一块土地的使用权。
- **`delete`****：** 用于释放由 `new` 分配的**单个对象**的内存。就像归还向操作系统申请的单块土地的使用权。
- **`new []`****：** 用于在堆区动态地分配一块**数组**的内存空间，并返回指向数组首元素的指针。就像向操作系统申请一块用于建造多栋房屋的土地的使用权。
- **`delete []`****：** 用于释放由 `new []` 分配的**数组**的内存。必须使用 `delete []` 来释放数组内存，以确保所有数组元素的析构函数都被调用（如果元素是对象的话）。就像归还用于建造多栋房屋的土地的使用权，需要确保每栋房屋都被妥善处理。
**示例代码：**
```cpp
#include <iostream>
int main() {
  // 使用 new 分配一个 int 类型的内存空间
  int* ptr = new int;
  *ptr = 10;
  std::cout << "ptr 指向的值: " << *ptr << std::endl;
  // 使用 delete 释放内存
  delete ptr;
  ptr = nullptr; // 释放后将指针置空，防止悬空 (dangling) 指针
  std::cout << std::endl;
  // 使用 new [] 分配一个包含 5 个 int 类型的数组
  int* arr = new int[5];
  for (int i = 0; i < 5; ++i) {
    arr[i] = i * 2;
  }
  std::cout << "动态分配的数组元素：";
  for (int i = 0; i < 5; ++i) {
    std::cout << arr[i] << " ";
  }
  std::cout << std::endl;
  // 使用 delete [] 释放数组内存
  delete[] arr;
  arr = nullptr; // 释放后将指针置空
  return 0;
}

// 期望输出:
// ptr 指向的值: 10
// 
// 动态分配的数组元素：0 2 4 6 8 
```
**讲解要点：**
- **动态内存分配的必要性：**
    - **灵活地管理内存:** 在程序运行时根据需要动态地申请和释放内存，避免了静态分配内存可能造成的浪费或不足。
    - **创建动态数据结构:** 例如链表、树等，这些数据结构在编译时无法确定大小，需要动态分配内存。
- **`new`** **和** **`delete`** **的使用方法：**
    - `类型* 指针变量 = new 类型;` 分配单个对象的内存。
    - `类型* 指针变量 = new 类型[大小];` 分配数组的内存。
    - `delete 指针变量;` 释放单个对象的内存。
    - `delete[] 指针变量;` 释放数组的内存。
- **内存泄漏的概念和危害：** 如果使用 `new` 分配了内存，但在不再使用时忘记使用 `delete` 或 `delete[]` 释放，就会导致**内存泄漏 (Memory Leak)**。 随着程序的运行，泄漏的内存会越来越多，最终可能导致程序运行缓慢甚至崩溃。 想象一下你借了别人的土地却一直不归还，最终可能会引发问题。
- **`new`** **失败的情况：** 当系统没有足够的内存来满足 `new` 的请求时，会抛出一个 `std::bad_alloc` 异常。 良好的编程习惯是使用 `try-catch` 块来捕获这个异常并进行处理。
- **悬空指针 (Dangling Pointer)：** 当 `delete` 或 `delete[]` 释放了指针所指向的内存后，该指针就变成了悬空指针，它指向的内存已经无效。 访问悬空指针会导致未定义的行为，程序可能会崩溃或产生不可预测的结果。 因此，在释放内存后，通常会将指针设置为 `nullptr`。
---
## 四、内存中的栈区和堆区 (Stack and Heap)
**概念：** 计算机的内存可以想象成一个巨大的仓库，为了更好地管理这些空间，操作系统将其划分成了不同的区域。其中，栈区和堆区是 C++ 程序员需要重点理解的两个区域。
- **栈区 (Stack):** 就像一个后进先出的箱子。当你调用一个函数时，该函数的局部变量、参数等信息会被放入栈中（入栈），函数执行完毕后，这些信息会被自动移除（出栈）。 栈区的内存由编译器自动管理，效率很高，但大小有限。
- **堆区 (Heap):** 就像一个巨大的、可以自由分配和回收的空地。程序员可以使用 `new` 和 `delete` 手动地在这片区域申请和释放内存。 堆区的大小相对较大，但需要程序员自己管理，如果管理不当容易出现内存泄漏等问题。
**示例代码：**
```cpp
#include <iostream>
int* createOnHeap() {
  int* num = new int(100); // 在堆区分配内存
  return num;
}
void functionOnStack() {
  int localVar = 50; // 在栈区分配内存
  std::cout << "栈区变量 localVar 的地址: " << &localVar << std::endl;
}
int main() {
  // 栈区变量
  int a = 10;
  std::cout << "栈区变量 a 的地址: " << &a << std::endl;
  // 堆区变量
  int* b = new int;
  *b = 20;
  std::cout << "堆区变量 b 的地址: " << b << std::endl;
  functionOnStack();
  int* heapVar = createOnHeap();
  std::cout << "堆区变量 heapVar 的地址: " << heapVar << std::endl;
  std::cout << "堆区变量 heapVar 指向的值: " << *heapVar << std::endl;
  delete heapVar;
  heapVar = nullptr;
  return 0;
}

// 输出模式（地址值依赖本次运行）:
// 栈区变量 a 的地址: <运行时地址>
// 堆区变量 b 的地址: <运行时地址>
// 栈区变量 localVar 的地址: <运行时地址>
// 堆区变量 heapVar 的地址: <运行时地址>
// 堆区变量 heapVar 指向的值: 100
```
**讲解要点：**
- **栈区和堆区的区别：**

|特征|栈区 (Stack)|堆区 (Heap)|
|---|---|---|
|分配和释放|编译器自动分配和释放|程序员手动分配和释放 (`new`/`delete`)|
|存储内容|局部变量、函数参数、函数调用信息|动态分配的内存|
|大小限制|有限，由编译器或操作系统预先设定|相对较大，受系统可用内存限制|
|分配速度|快|相对较慢|
|管理方式|自动管理|手动管理|
- **栈区和堆区的内存分配方式：**
    - **栈区：** 内存分配和释放就像叠盘子一样，后进先出。
    - **堆区：** 内存分配和释放更加灵活，可以在任意时刻申请和释放任意大小的内存块。操作系统维护着一个空闲内存列表，当 `new` 请求内存时，系统会找到合适的空闲块分配出去。
- **栈溢出和堆溢出：**
    - **栈溢出 (Stack Overflow):** 当函数调用层级过深（例如过多的递归调用）或者局部变量占用过多内存时，可能导致栈空间不足，发生栈溢出。
    - **堆溢出 (Heap Overflow):** 通常指缓冲区溢出 (Buffer Overflow)，当向一块堆内存中写入的数据超过了其分配的大小，就可能覆盖相邻的内存区域，导致程序出错甚至安全漏洞。 与本节课讨论的内存管理有所区别，这里指的是非法的内存写入。

---
## 五、全局变量、局部变量、`static` 静态变量
**概念：** 变量根据其声明的位置和 `static` 关键字的使用，拥有不同的作用域和生命周期。
- **全局变量 (Global Variable):** 在所有函数外部定义的变量。它们在程序开始执行时被创建，在程序结束时被销毁，具有**全局作用域**，可以被程序中的任何函数访问。
- **局部变量 (Local Variable):** 在函数内部或复合语句（例如 `if` 语句、循环语句）内部定义的变量。它们在定义时被创建，在所在的代码块执行完毕后被销毁，具有**局部作用域**，只能在其定义的代码块内部被访问。
- **`static`** **静态变量 (Static Variable):**
    - **局部静态变量:** 在函数内部用 `static` 关键字声明的变量。它只在第一次执行到其定义语句时被初始化一次，之后的函数调用不会再次初始化。 它的**生命周期贯穿整个程序执行期间**，但作用域仍然是局部的，只能在定义它的函数内部访问。
    - **全局静态变量:** 在所有函数外部用 `static` 关键字声明的变量。它的作用域被限制在声明它的**源文件**中，其他源文件无法访问。这可以避免命名冲突。

**示例代码：**
```cpp
#include <iostream>
// 全局变量
static int globalVar = 10;
void func() {
  // 局部变量
  int localVar = 20;
  // static 静态局部变量
  static int staticVar = 30;
  static int* ptr = new int(100);
  std::cout << "函数 func 被调用" << std::endl;
  std::cout << "全局变量: " << globalVar << "，地址: " << &globalVar << std::endl;
  std::cout << "局部变量: " << localVar << "，地址: " << &localVar << std::endl;
  std::cout << "静态变量: " << staticVar << "，地址: " << &staticVar << std::endl;
  localVar++;
  staticVar++;
}
int main() {
  std::cout << "main 函数中的全局变量: " << globalVar << std::endl;
  func();
  func();
  return 0;
}

// 输出模式（地址值依赖本次运行）:
// main 函数中的全局变量: 10
// 函数 func 被调用
// 全局变量: 10，地址: <运行时地址>
// 局部变量: 20，地址: <运行时地址>
// 静态变量: 30，地址: <运行时地址>
// 函数 func 被调用
// 全局变量: 10，地址: <运行时地址>
// 局部变量: 20，地址: <运行时地址>
// 静态变量: 31，地址: <运行时地址>
```
**讲解要点：**
- **三种变量的作用域和生命周期：**

|变量类型|作用域|生命周期|初始化时机|
|---|---|---|---|
|全局变量|整个程序|程序开始到程序结束|程序启动时|
|局部变量|定义它的代码块|定义时创建，代码块结束时销毁|每次进入代码块时|
|静态局部变量|定义它的函数|程序开始到程序结束|第一次执行到定义语句时|
|静态全局变量|声明它的源文件|程序开始到程序结束|程序启动时|
- **`static`** **关键字的作用：**
    - **修饰局部变量:** 延长局部变量的生命周期，使其在函数多次调用之间保持状态。
    - **修饰全局变量:** 限制全局变量的作用域，使其只能在当前源文件中访问。
    - **修饰类的成员变量:** 使类的所有对象共享同一个变量，属于类而不是类的某个特定对象。
    - **修饰类的成员函数:** 使成员函数不依赖于类的具体对象而存在，可以通过类名直接调用。
- **全局变量的使用注意事项：** 虽然全局变量方便访问，但过度使用全局变量会降低代码的模块化程度，增加命名冲突的风险，并可能导致程序难以维护和调试。 应该谨慎使用全局变量，尽可能使用局部变量或将数据封装在类中。
---

> [!warning] 内存管理纠错（Memory Management Corrections）
> “堆溢出”不等同于“堆缓冲区溢出（Heap Buffer Overflow）”：前者常指动态存储耗尽，后者是越界写导致的内存破坏。普通 `new` 分配失败默认抛出 `std::bad_alloc`，只有 `new (std::nothrow)` 才以 `nullptr` 表示失败。原示例中的局部静态裸指针 `static int* ptr = new int(100);` 没有对应 `delete`，会一直保留到进程结束；教学演示可说明生命周期，但工程代码应使用值对象或 `std::unique_ptr`。局部静态变量具有静态存储期，但初始化发生在程序第一次执行到声明处时；自 C++11 起该初始化具有线程安全保证。

## 工程推荐：优先使用 RAII（Prefer RAII in Production）
```cpp
#include <iostream>
#include <memory>
#include <vector>

int main() {
    auto number = std::make_unique<int>(10);  // 独占所有权随作用域自动释放，异常路径也不会泄漏。
    std::vector<int> values{0, 2, 4, 6, 8};  // 容器负责动态数组的容量与释放。
    std::cout << *number << '\n';
    for (int value : values) {
        std::cout << value << ' ';
    }
    std::cout << '\n';
    return 0;

    // 期望输出:
    // 10
    // 0 2 4 6 8
}
```

## 来源与入库建议（Provenance and Suggested Placement）
- **来源文件（Source Files）**：
- `Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/02-C++ 编程（C++）/函数进阶与内存管理.md`
- **建议目标位置（Suggested Target）**：`Notes/数据科学（Data Science）/01-编程基础（Programming）/02-C++ 编程（C++）/06-C++ 存储期与内存管理（Storage Duration and Memory Management）.md`
- **建议操作（Suggested Operation）**：新建。
- **合并对象（Merge Target）**：无；Notes 中未发现现有 C++ 正文笔记。
- **不确定事项（Open Questions）**：
- Valgrind、AddressSanitizer 和平台调试命令可在后续排错笔记中展开。
