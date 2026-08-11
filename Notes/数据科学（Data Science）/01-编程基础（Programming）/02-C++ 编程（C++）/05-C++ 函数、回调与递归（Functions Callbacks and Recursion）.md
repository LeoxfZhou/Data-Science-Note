---
title: C++ 函数、回调与递归（Functions, Callbacks, and Recursion）
status: published
published_at: 2026-08-11
---

# C++ 函数、回调与递归（Functions, Callbacks, and Recursion）
## 函数基础（Function Fundamentals）
随着程序规模增大，将所有代码写在一个 `main` 函数中会难以维护。函数是将代码分割成独立模块的重要工具。
### 1. 函数的概念：构建代码模块
- **什么是函数？** 一段独立的代码块，执行特定任务，可被多次调用。像一个“加工厂”，接收“原材料”（输入参数），产出“产品”（返回值）。
- **为什么要使用函数？**
    - **避免代码冗余**。
    - **提高代码可读性**：逻辑模块化，类似书本的章节。
    - **便于代码调试**：快速定位出错模块。
    - **提高代码复用性**。
    
### 2. 函数的定义：如何创建你的代码模块
- **函数定义的语法：**
    
    ```pseudocode
    返回值类型 函数名(参数类型1 参数名1, 参数类型2 参数名2, ...) {
        // 函数体：包含函数要执行的代码
        return 返回值; // 如果返回值类型不是 void
    }
    ```
    
- **函数定义示例：**
    
    ```cpp
    #include <iostream>
    #include <string>
    
    // 定义计算乘积的函数
    int multiply(int a, int b) {
        int product = a * b;
        return product;
    }
    
    // 定义打印问候语的函数（无返回值，用 void）
    void greet(std::string name) {
        std::cout << "你好, " << name << "!" << std::endl;
    }
    ```
    
### 3. 函数的调用：启动代码模块的执行
- **调用语法：** `函数名(实际参数列表);`
- **参数传递 (Parameter Passing)：**
    - **形式参数 (形参, Formal Parameter)：** 函数定义中的占位符。
    - **实际参数 (实参, Actual Parameter)：** 调用时传入的具体值。
- **常用传递方式：**
    - **值传递 (Pass by Value)：** 实参的值复制给形参，函数内部修改不影响外部实参。
    - **引用传递 (Pass by Reference)：** 形参成为实参的别名，使用 `&` 符号，内部修改会直接影响外部。
        
        ```cpp
        void increment(int& num) {
            num++; // 修改形参会影响外部实参
        }
        ```
        
    
    - **常量引用传递 (Pass by Constant Reference)：** 结合引用效率与值传递的安全性，使用 `const` 和 `&`，防止内部修改。
        
        ```cpp
        void printLength(const std::string& str) {
            std::cout << str.length() << std::endl;
            // str[0] = 'A'; // 错误！无法修改常量引用
        }
        ```
        
    
### 4. 函数的应用：实践代码组织的艺术
- **应用场景：**
    - 编写可复用代码（排序、数学计算等）。
    - 模块化编程（分解大型程序结构）。
    - 简化程序逻辑。
    
---

### 函数基础小结（Function Fundamentals Summary）
本章学习了 C++ 中自定义数据类型（`struct`、`enum`、`union`）以及函数的基本概念和使用方法。掌握这些知识对于编写结构良好、功能完善的 C++ 程序至关重要。
---
## 三、函数与指针的深度应用
指针在函数中扮演着重要的角色，可以用于传递数据、返回结果，甚至传递函数本身。
- **指针函数：返回指针的函数 (Function returning a pointer)**
    - 指针函数的返回值是一个指针类型。这使得函数可以返回动态分配的内存地址，或者指向在函数外部定义的变量的地址。
    - 需要注意内存管理，避免返回指向局部变量的指针，因为局部变量在函数执行结束后会被销毁。

**示例代码:**
```cpp
#include <iostream>
// 指针函数：返回动态分配的 int 数组
int* createArray(int size) {
  int* arr = new int[size];
  for (int i = 0; i < size; ++i) {
    arr[i] = i * 2;
  }
  return arr; // 返回指向动态分配内存的指针
}
int main() {
  int* myArray = createArray(5);
  if (myArray != nullptr) {
    std::cout << "动态数组的元素: ";
    for (int i = 0; i < 5; ++i) {
      std::cout << myArray[i] << " ";
    }
    std::cout << std::endl;
    delete[] myArray; // 记得释放动态分配的内存
    myArray = nullptr;
  }
  return 0;
}

// 期望输出:
// 动态数组的元素: 0 2 4 6 8 
```
- **函数指针：指向函数的指针 (Function Pointer)**
    - 函数指针存储的是函数的入口地址。通过函数指针，我们可以间接地调用函数，可以将函数作为参数传递给其他函数，或者存储在一组函数列表中。
    - 函数指针的声明需要指定函数的返回类型和参数列表。

**示例代码及详细解释:**
```cpp
#include <iostream>
// 一个简单的加法函数
int add(int a, int b) {
  return a + b;
}
// 一个使用函数指针作为参数的函数
void executeOperation(int a, int b, int (*operation)(int, int)) {
  std::cout << "执行结果: " << operation(a, b) << std::endl;
}
int main() {
  // 声明一个指向返回 int，接受两个 int 参数的函数的指针
  int (*funcPtr)(int, int);
  // 将 add 函数的地址赋值给 funcPtr
  funcPtr = add;
  // 通过函数指针调用 add 函数
  int result = funcPtr(5, 3);
  std::cout << "通过函数指针调用 add: " << result << std::endl;
  // 将 add 函数作为参数传递给 executeOperation 函数
  executeOperation(10, 5, add);
  return 0;
}

// 期望输出:
// 通过函数指针调用 add: 8
// 执行结果: 15
```
**关键点总结:**
- 指针函数返回指针，需要注意内存管理。
- 函数指针可以存储函数的地址，实现间接调用和函数作为参数传递。
## 四、函数的重载：提高代码的灵活性
函数重载 (Function Overloading) 允许在同一个作用域内定义多个同名函数，只要它们的参数列表不同（参数的类型、数量或顺序不同）。
- **重载的原理:** 编译器会根据函数调用时提供的参数类型和数量，自动匹配最合适的重载版本。
- **重载的优势:** 提高了代码的可读性和可维护性，可以使用相同的函数名执行相似但针对不同数据类型的操作。
**示例代码及详细解释:**
```cpp
#include <iostream>
// 重载的 sum 函数，处理两个整数
int sum(int a, int b) {
  std::cout << "调用 sum(int, int)" << std::endl;
  return a + b;
}
// 重载的 sum 函数，处理三个整数
int sum(int a, int b, int c) {
  std::cout << "调用 sum(int, int, int)" << std::endl;
  return a + b + c;
}
// 重载的 sum 函数，处理两个 double 类型
double sum(double a, double b) {
  std::cout << "调用 sum(double, double)" << std::endl;
  return a + b;
}
int main() {
  std::cout << "sum(2, 3) = " << sum(2, 3) << std::endl;         // 调用第一个 sum 函数
  std::cout << "sum(2, 3, 4) = " << sum(2, 3, 4) << std::endl;    // 调用第二个 sum 函数
  std::cout << "sum(2.5, 3.5) = " << sum(2.5, 3.5) << std::endl;  // 调用第三个 sum 函数
  return 0;
}

// 期望输出:
// sum(2, 3) = 调用 sum(int, int)
// 5
// sum(2, 3, 4) = 调用 sum(int, int, int)
// 9
// sum(2.5, 3.5) = 调用 sum(double, double)
// 6
```
**关键点总结:**
- 函数重载通过不同的参数列表区分同名函数。
- 编译器根据参数匹配调用相应的重载版本。
## 五、函数的默认参数值：简化函数调用
C++ 允许在函数声明时为参数指定默认参数 (Default Arguments)。当调用函数时，如果没有为带有默认值的参数提供实参，则会使用默认值。
- **默认参数的规则:**
    - 默认参数必须从参数列表的右侧开始定义。也就是说，如果一个参数有默认值，那么它右边的所有参数都必须有默认值。
    - 默认参数值在函数声明中指定，而不是在函数定义中（虽然在定义中也可以指定，但不推荐）。

**示例代码及详细解释:**
```cpp
#include <iostream>
// 计算矩形面积，默认宽度为 1
int calculateArea(int length, int width = 1) {
  std::cout << "计算长度为 " << length << ", 宽度为 " << width << " 的矩形面积" << std::endl;
  return length * width;
}
// 打印信息，默认打印次数为 1
void printMessage(const std::string& message, int times = 1) {
  for (int i = 0; i < times; ++i) {
    std::cout << message << std::endl;
  }
}
int main() {
  std::cout << "面积1: " << calculateArea(5) << std::endl;       // 使用默认宽度 1
  std::cout << "面积2: " << calculateArea(5, 3) << std::endl;    // 传递了宽度参数
  printMessage("Hello");                             // 使用默认打印次数 1
  printMessage("World", 3);                          // 传递了打印次数
  return 0;
}

// 期望输出:
// 面积1: 计算长度为 5, 宽度为 1 的矩形面积
// 5
// 面积2: 计算长度为 5, 宽度为 3 的矩形面积
// 15
// Hello
// World
// World
// World
```
**关键点总结:**
- 默认参数在函数声明时指定。
- 调用函数时可以省略有默认值的参数。
- 默认参数必须从右向左定义。
## 六、内联函数：提升程序性能
内联函数 (Inline Function) 是一种编译器优化技术，用于减少函数调用的开销。
- **内联的原理:** 当编译器遇到内联函数的调用时，会尝试将函数体的代码直接插入到调用处，而不是进行实际的函数调用过程（压栈、跳转、返回等）。这类似于宏展开，但内联函数是类型安全的。
- **`inline`** **关键字:** 使用 `inline` 关键字建议编译器将函数内联，但这只是一个请求，编译器可以选择忽略。通常，编译器会考虑函数的复杂度和大小来决定是否内联。
- **适用场景:**
    - 短小、频繁调用的函数是内联的理想选择，例如简单的 getter/setter 方法、小的计算函数等。
    - 不适合内联的情况包括包含循环、递归、复杂控制流的函数，以及函数体过于庞大的函数。过度内联可能导致代码膨胀，反而降低性能。

**示例代码及详细解释:**
```cpp
#include <iostream>
// 内联函数：计算两个整数的最大值
inline int max(int a, int b) {
  return a > b ? a : b;
}
// 内联函数：计算平方
inline double square(double x) {
  return x * x;
}
int main() {
  int x = 10, y = 5;
  // 编译器可能会将 max(x, y) 的代码直接替换到这里
  std::cout << "最大值: " << max(x, y) << std::endl;
  double num = 3.5;
  // 编译器可能会将 square(num) 的代码直接替换到这里
  std::cout << "平方: " << square(num) << std::endl;
  return 0;
}

// 期望输出:
// 最大值: 10
// 平方: 12.25
```
**内联函数的注意事项:**
- **声明和定义:** 通常，内联函数的声明和定义应该放在同一个头文件中，以便编译器在编译调用处时能够看到函数体。
- **`inline`** **的建议性:** `inline` 只是对编译器的建议，编译器最终决定是否内联。
- **调试难度:** 内联函数可能使调试更加困难，因为代码在编译后被展开，单步调试时可能看不到独立的函数调用。
## 本章总结（Chapter Summary）
本章深入学习了 C++ 中关于字符串常量、二维数组与行指针、函数与指针的应用、函数的重载、默认参数值以及内联函数等重要概念。这些知识是构建复杂 C++ 程序的基石，理解和熟练运用它们对于编写高效、可维护的代码至关重要。在接下来的学习中，我们将继续探索更多 C++ 的强大特性。
## 一、回调函数 (Callback Functions)
- 概念：在编程中，回调函数就是将一个函数的_指针_像参数一样传递给另一个函数，这样接收方函数就可以在合适的时机“反过来调用”你传递给它的函数。
**作用：**
- **解耦合 (Decoupling):** 回调函数允许我们分离操作的执行者和操作的具体内容。调用者不需要知道被调用者具体做什么，只需要知道如何通知它完成。
- **提升代码的灵活性和可扩展性:** 通过传递不同的回调函数，我们可以让同一个函数执行不同的操作，而无需修改其内部代码。这就像你可以通过不同的“通知方式”（例如电话、短信）来接收外卖送达的消息。
- **实现事件驱动编程:** 在图形界面、异步编程等场景中，回调函数常用于处理事件的发生。
**示例代码：**
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
// 回调函数：打印消息
void printMessage(int num) {
  std::cout << "回调函数被调用，数字为: " << num << std::endl;
}
// 回调函数：打印数字的平方
void printSquare(int num) {
  std::cout << "回调函数被调用，数字的平方为: " << num * num << std::endl;
}
// 接收回调函数指针作为参数的函数
void callFunction(void (*callback)(int), int num) {
  std::cout << "callFunction 正在执行，准备调用回调函数..." << std::endl;
  callback(num); // 调用传入的回调函数
  std::cout << "callFunction 执行完毕。" << std::endl;
}
// 一个更实际的例子：使用回调函数进行自定义排序
bool compareAscending(int a, int b) {
  return a < b;
}
bool compareDescending(int a, int b) {
  return a > b;
}
void sortNumbers(std::vector<int>& nums, bool (*compare)(int, int)) {
  std::sort(nums.begin(), nums.end(), compare);
}
int main() {
  // 将 printMessage 函数的指针传递给 callFunction
  callFunction(printMessage, 10);
  std::cout << std::endl;
  // 将 printSquare 函数的指针传递给 callFunction
  callFunction(printSquare, 5);
  std::cout << std::endl;
  // 使用回调函数进行排序
  std::vector<int> numbers = {3, 1, 4, 1, 5, 9, 2, 6};
  std::cout << "排序前：";
  for (int num : numbers) {
    std::cout << num << " ";
  }
  std::cout << std::endl;
  sortNumbers(numbers, compareAscending);
  std::cout << "升序排序后：";
  for (int num : numbers) {
    std::cout << num << " ";
  }
  std::cout << std::endl;
  sortNumbers(numbers, compareDescending);
  std::cout << "降序排序后：";
  for (int num : numbers) {
    std::cout << num << " ";
  }
  std::cout << std::endl;
  return 0;
}

// 期望输出:
// callFunction 正在执行，准备调用回调函数...
// 回调函数被调用，数字为: 10
// callFunction 执行完毕。
// 
// callFunction 正在执行，准备调用回调函数...
// 回调函数被调用，数字的平方为: 25
// callFunction 执行完毕。
// 
// 排序前：3 1 4 1 5 9 2 6 
// 升序排序后：1 1 2 3 4 5 6 9 
// 降序排序后：9 6 5 4 3 2 1 1 
```
**讲解要点：**
- **函数指针的声明方式：** `void (*callback)(int)` 声明了一个指向返回值为 `void`，接受一个 `int` 类型参数的函数的指针。
- **如何将函数指针作为参数传递：** 直接将函数名作为参数传递即可，函数名在大多数情况下会被隐式转换为函数指针。
- **回调函数的实际应用场景：**
    - **事件处理:** 例如，在图形用户界面 (GUI) 编程中，按钮点击事件的处理函数就是一个回调函数。
    - **排序算法定制:** 如上面的 `sortNumbers` 示例，可以根据不同的比较规则进行排序。
    - **异步操作完成后的通知:** 当一个耗时的操作（例如网络请求）完成后，通过回调函数通知程序。
    - **插件机制:** 允许在不修改原有代码的情况下，通过注册回调函数来扩展程序的功能。

---
## 二、函数的递归调用 (Recursive Function Calls)
**概念：** 想象一下你面前放着两面镜子互相反射，你会看到一个无限延伸的影像。递归调用就像这样，一个函数在执行的过程中，直接或间接地调用了自身。为了避免无限循环，递归必须有一个明确的结束条件。
**关键：**
- **递归的终止条件 (Base Case)：** 这是递归函数不再调用自身的条件，是递归能够结束的根本保证。就像镜子迷宫的出口。
- **递归的递推关系 (Recursive Step)：** 定义了如何将问题分解为更小的、与原问题结构相同的子问题。就像在镜子迷宫中找到通往下一个反射点的路。
**示例代码：**
```cpp
#include <iostream>
// 计算阶乘
int factorial(int n) {
  std::cout << "计算 " << n << " 的阶乘" << std::endl;
  // 递归终止条件
  if (n == 0) {
    std::cout << "到达终止条件，返回 1" << std::endl;
    return 1;
  }
  // 递归调用
  int result = n * factorial(n - 1);
  std::cout << n << " 的阶乘计算完成，结果为 " << result << std::endl;
  return result;
}
// 使用递归计算斐波那契数列
int fibonacci(int n) {
  if (n <= 1) {
    return n;
  }
  return fibonacci(n - 1) + fibonacci(n - 2);
}
int main() {
  int num = 5;
  std::cout << num << " 的阶乘是: " << factorial(num) << std::endl;
  std::cout << std::endl;
  std::cout << "斐波那契数列第 10 项是: " << fibonacci(10) << std::endl;
  return 0;
}

// 期望输出:
// 5 的阶乘是: 计算 5 的阶乘
// 计算 4 的阶乘
// 计算 3 的阶乘
// 计算 2 的阶乘
// 计算 1 的阶乘
// 计算 0 的阶乘
// 到达终止条件，返回 1
// 1 的阶乘计算完成，结果为 1
// 2 的阶乘计算完成，结果为 2
// 3 的阶乘计算完成，结果为 6
// 4 的阶乘计算完成，结果为 24
// 5 的阶乘计算完成，结果为 120
// 120
// 
// 斐波那契数列第 10 项是: 55
```
**讲解要点：**
- **递归的优缺点：**
    - **优点：** 某些问题用递归解决思路清晰、代码简洁，易于理解。
    - **缺点：** 每次递归调用都需要保存现场信息（例如函数参数、局部变量等），占用栈空间，如果递归深度过大，可能导致**栈溢出 (Stack Overflow)**。同时，递归可能会存在重复计算的问题，例如在计算斐波那契数列时。
- **递归与迭代的比较：** 迭代通常使用循环结构实现，效率更高，占用内存更少，但某些问题的迭代实现可能比较复杂。大多数可以用递归解决的问题，也可以用迭代解决。
- **避免无限递归：** 务必确保递归函数有一个明确的终止条件，并且每次递归调用都逐步接近该终止条件。
- **栈溢出的风险：** 了解栈空间的限制，避免过深的递归调用。
---

## 六、函数的指针传参和引用传参
**概念：** 当我们调用一个函数时，需要将一些数据传递给函数进行处理。C++ 提供了三种常用的参数传递方式：值传递、指针传递和引用传递。
- **值传递 (Pass by Value):** 在调用函数时，将实参的值**复制一份**传递给形参。函数内部对形参的修改不会影响到实参的值。就像你复印了一份文件给别人，别人在复印件上修改不会影响你的原件。
- **指针传递 (Pass by Pointer):** 在调用函数时，将实参的**内存地址**传递给形参。形参是一个指针变量，指向实参的内存地址。函数内部可以通过解引用指针来修改实参的值。就像你把你的房子的钥匙给了别人，别人可以通过钥匙进入你的房子并进行修改。
- **引用传递 (Pass by Reference):** 在调用函数时，将实参的**别名**传递给形参。形参是实参的一个别名，它们指向同一块内存空间。函数内部对形参的修改会直接影响到实参的值。就像你给你的房子起了个外号，别人叫外号和叫正式名字都是指的同一栋房子，对房子的任何操作都会反映在两个名字上。
**示例代码：**
```cpp
#include <iostream>
// 值传递
void swapByValue(int a, int b) {
  std::cout << "值传递函数内部：交换前 a = " << a << ", b = " << b << std::endl;
  int temp = a;
  a = b;
  b = temp;
  std::cout << "值传递函数内部：交换后 a = " << a << ", b = " << b << std::endl;
}
// 指针传递
void swapByPointer(int* a, int* b) {
  std::cout << "指针传递函数内部：交换前 *a = " << *a << ", *b = " << *b << std::endl;
  int temp = *a;
  *a = *b;
  *b = temp;
  std::cout << "指针传递函数内部：交换后 *a = " << *a << ", *b = " << *b << std::endl;
}
// 引用传递
void swapByReference(int& a, int& b) {
  std::cout << "引用传递函数内部：交换前 a = " << a << ", b = " << b << std::endl;
  int temp = a;
  a = b;
  b = temp;
  std::cout << "引用传递函数内部：交换后 a = " << a << ", b = " << b << std::endl;
}
int main() {
  int x = 10, y = 20;
  std::cout << "交换前：x = " << x << ", y = " << y << std::endl;
  // 值传递
  swapByValue(x, y);
  std::cout << "值传递后：x = " << x << ", y = " << y << std::endl;
  // 指针传递
  swapByPointer(&x, &y);
  std::cout << "指针传递后：x = " << x << ", y = " << y << std::endl;
  // 引用传递
  swapByReference(x, y);
  std::cout << "引用传递后：x = " << x << ", y = " << y << std::endl;
  return 0;
}

// 期望输出:
// 交换前：x = 10, y = 20
// 值传递函数内部：交换前 a = 10, b = 20
// 值传递函数内部：交换后 a = 20, b = 10
// 值传递后：x = 10, y = 20
// 指针传递函数内部：交换前 *a = 10, *b = 20
// 指针传递函数内部：交换后 *a = 20, *b = 10
// 指针传递后：x = 20, y = 10
// 引用传递函数内部：交换前 a = 20, b = 10
// 引用传递函数内部：交换后 a = 10, b = 20
// 引用传递后：x = 10, y = 20
```
**讲解要点：**
- **三种传参方式的区别：**

|传参方式|传递内容|是否会修改实参|效率 (一般情况下)|使用场景|
|---|---|---|---|---|
|值传递|实参的值|否|低 (需要复制)|不需要修改实参，传递简单数据类型|
|指针传递|实参的地址|是|中|需要修改实参，传递大型数据结构，动态内存管理|
|引用传递|实参的别名|是|高 (无需复制)|需要修改实参，语法更简洁|
- **指针和引用的概念：**
    - **指针：** 一个存储内存地址的变量。可以通过解引用操作符 () 访问指针所指向的内存。
    - **引用：** 一个变量的别名，它和被引用的变量指向同一块内存空间。引用在声明时必须初始化，并且一旦绑定就不能重新绑定到其他变量。
- **二级指针的应用场景：** 二级指针是指向指针的指针。常用于以下场景：
    - **修改指针本身：** 例如，在一个函数中动态分配内存并需要修改调用者传递进来的指针变量，使其指向新分配的内存。
    - **处理指针数组或指针的指针：** 例如，`char **argv` 是命令行参数的常见形式，就是一个指向字符指针数组的指针。

---
