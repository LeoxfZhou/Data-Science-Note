---
title: C++ 自定义数据类型（Custom Data Types）
status: review
detail_level: comprehensive
merge_policy: union-zero-loss
reviewed_at: 2026-08-11
sources:
  - "Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/02-C++ 编程（C++）/自定义数据类型与函数.md"
suggested_target: "Notes/数据科学（Data Science）/01-编程基础（Programming）/02-C++ 编程（C++）/03-C++ 自定义数据类型（Custom Data Types）.md"
operation: 新建
merge_target: null
---

# C++ 自定义数据类型（Custom Data Types）

> [!info] 候选稿状态（Draft Status）
> 本文仅写入 `Processing/01-Review/`，等待人工检查；对应 Inbox 原稿未移动、未删除、未修改。

本文集中整理结构体、枚举和联合体；同一来源中的函数章节已按主题并入函数笔记。

## 结构体、枚举与联合体（Structures, Enumerations, and Unions）
在之前的课程中，我们学习了 C++ 提供的基本数据类型，如 `int`、`float`、`char` 等。但现实世界的数据往往更加复杂，需要我们自定义数据类型 (Custom Data Types) 来更好地描述和管理。本部分将介绍三种强大的自定义数据类型。
### 1. 结构体 (struct)：将数据打包成有意义的整体
- **什么是结构体？**
    - 想象一下，你要描述一个学生的信息。仅仅用一个整数表示学号，一个字符串表示姓名，一个浮点数表示成绩，这些数据是分散的，难以在一个逻辑单元中进行管理。
    - **结构体 (Structure) 是一种自定义的数据类型，它允许你将不同类型的数据组合在一起，形成一个有意义的新的数据类型。** 这个新的数据类型就像一个“包裹”，将相关的各种信息捆绑在一起。
- **定义结构体：设计你的数据“包裹”**

    ```cpp
    struct Student {
        std::string name; // 学生姓名
        int id;           // 学生学号
        float score;      // 学生成绩
    };
    ```

    - `struct` 关键字表明我们正在定义一个结构体。
    - `Student` 是结构体的名称。花括号 `{}` 内部定义了结构体的成员（也称为字段或属性）。
- **使用结构体：创建和访问结构体变量**

    ```cpp
    #include <iostream>
    #include <string>

    struct Student {
        std::string name;
        int id;
        float score;
    };

    int main() {
        // 声明一个 Student 类型的变量 s1
        Student s1;

        // 为 s1 的成员赋值
        s1.name = "Alice";
        s1.id = 2023001;
        s1.score = 95.5;

        // 访问并输出 s1 的成员 (使用点运算符)
        std::cout << "姓名: " << s1.name << std::endl;
        std::cout << "学号: " << s1.id << std::endl;
        std::cout << "成绩: " << s1.score << std::endl;

        return 0;
    }
    ```

- **C++ 中的** **`struct`** **与 C 语言中的** **`struct`** **的主要区别**
    - **成员函数：** C++ 中的 `struct` 不仅可以包含数据成员，还可以包含成员函数 (Member Function)，用于操作结构体内部的数据，能够将数据和行为封装在一起。C 语言的 `struct` 只能包含数据成员。
    - **默认访问权限：** C++ 中 `struct` 的默认成员访问权限是 `public`。
- **`struct`** **和** **`class`** **的异同**
    - **核心区别：** `struct` 的默认成员访问权限和默认继承方式是 `public`；`class` 默认是 `private`。
    - **最佳实践：** 通常使用 `struct` 表示简单的数据集合，而使用 `class` 表示具有复杂行为和需要封装性的抽象数据类型。
- **结构体的应用场景**
    - 表示具有多个相关属性的实体（学生、坐标点等）。
    - 作为函数参数和返回值，传递复杂的数据结构。

### 2. 枚举 (enum)：为整数赋予有意义的名称
- **什么是枚举？**
    - **枚举 (Enumeration) 是一种用户定义的数据类型，它允许你为一组整型常量赋予有意义的名称。** 这样可以避免使用难以理解的魔法数字 (Magic Number)，提高代码可读性。
- **定义枚举类型**

    ```cpp
    enum Weekday {
        Monday,    // 默认值为 0
        Tuesday,   // 默认值为 1
        Wednesday, // 默认值为 2
        Thursday,  // 默认值为 3
        Friday,    // 默认值为 4
        Saturday,  // 默认值为 5
        Sunday     // 默认值为 6
    };
    ```

- **使用枚举类型**

    ```cpp
    #include <iostream>

    enum Weekday {
        Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
    };

    int main() {
        Weekday today = Wednesday;

        if (today == Wednesday) {
            std::cout << "今天星期三，要努力学习！" << std::endl;
        }

        // 可以显式获取枚举常量的值
        std::cout << "Wednesday 的值是: " << Wednesday << std::endl; // 输出 2
        return 0;
    }
    ```

- **指定枚举常量的值**

    ```cpp
    enum Status {
        Success = 0,
        Warning = 10,
        Error = 20,
    };
    ```

- **枚举的应用场景**
    - 表示状态码、错误码、选项或模式。

### 3. 联合体 (union)：共享内存的特殊数据类型
- **什么是联合体？**
    - **联合体 (Union) 是一种特殊的数据类型，它允许在同一块内存空间存储不同类型的数据。** 任何时候只能有一个成员存储有效的值。
- **定义联合体**

    ```cpp
    union Data {
        int intValue;
        float floatValue;
        char stringValue[20];
    };
    ```

- **使用联合体**

    ```cpp
    #include <iostream>
    #include <cstring>

    union Data {
        int intValue;
        float floatValue;
        char stringValue[20];
    };

    int main() {
        Data data;

        // 存储整数值
        data.intValue = 100;
        std::cout << "intValue: " << data.intValue << std::endl;

        // 存储浮点数值，此时 intValue 的值不再有效
        data.floatValue = 3.14f;
        std::cout << "floatValue: " << data.floatValue << std::endl;

        return 0;
    }

// 期望输出:
// intValue: 100
// floatValue: 3.14
```

    - **注意：** 当给联合体的一个成员赋值时，其他成员的值会变得无效。联合体的大小由其最大的成员的大小决定。
- **联合体的应用场景**
    - **节省内存空间：** 不同时间存储不同类型且不同时使用的数据。
    - **类型双关 (Type Punning)：** 底层编程中查看同一块内存的不同类型解释。

---

> [!important] 现代 C++ 选择（Modern C++ Choices）
> 普通枚举（Unscoped Enumeration）会把枚举项名称注入外围作用域，并可隐式转换为整数；新代码通常优先使用作用域枚举（Scoped Enumeration）`enum class`。联合体同一时刻只有一个活动成员；读取非活动成员不能当作可移植的类型双关（Type Punning）手段。需要类型安全地保存多种候选类型时，优先考虑 `std::variant`。

## 来源与入库建议（Provenance and Suggested Placement）
- **来源文件（Source Files）**：
- `Processing/00-Inbox/数据科学（Data Science）/01-编程基础（Programming）/02-C++ 编程（C++）/自定义数据类型与函数.md`
- **建议目标位置（Suggested Target）**：`Notes/数据科学（Data Science）/01-编程基础（Programming）/02-C++ 编程（C++）/03-C++ 自定义数据类型（Custom Data Types）.md`
- **建议操作（Suggested Operation）**：新建。
- **合并对象（Merge Target）**：无；Notes 中未发现现有 C++ 正文笔记。
- **不确定事项（Open Questions）**：
- 联合体示例保留教学用途；正式工程是否改写为 `std::variant` 由使用场景决定。
