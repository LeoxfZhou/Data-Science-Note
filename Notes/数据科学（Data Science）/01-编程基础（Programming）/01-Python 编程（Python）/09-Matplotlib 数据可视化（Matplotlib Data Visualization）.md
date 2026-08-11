---
title: Matplotlib 数据可视化（Matplotlib Data Visualization）
status: published
published_at: 2026-08-11
---

# Matplotlib 数据可视化（Matplotlib Data Visualization）
## 1. 对象模型与推荐工作方式（Object Model and Recommended Workflow）
- Matplotlib 的核心层级是画布（Figure）→ 坐标系（Axes）→ 图形元素（Artist）。
- `matplotlib.pyplot` 提供类似状态机的隐式接口；第一次调用 `plt.plot()` 等绘图函数时，如果当前没有 Figure 和 Axes，会自动创建它们。
- 学习简单绘图时可以使用 `plt.xxx()`；复杂图形更推荐显式保存 `fig` 和 `ax`，因为对象归属更明确，不容易把后续操作画到错误的坐标系。
- `plt.show()` 启动或接入图形用户界面（Graphical User Interface, GUI）事件循环并显示当前图形；脚本环境、Notebook 和不同后端的阻塞行为可能不同。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(x, y)
ax.set_title("正弦曲线")
plt.show()  # 图形结果: 一个包含正弦曲线的 Figure；无固定控制台输出
```

## 2. `plt.plot()` 折线与标记（Lines and Markers）
### 2.1 调用形式、参数与返回值（Signature, Parameters, and Return Value）
常用调用形式：
```text
plt.plot([x], y, [fmt], *, data=None, **kwargs)
```
- **`x`**：横坐标数据，可省略；省略时默认为 `range(len(y))`。常见输入是一维数组，也支持标量和二维数组。
- **`y`**：纵坐标数据；如果 `x` 或 `y` 是二维数组，每一列可以形成一条数据线。
- **`fmt`**：格式字符串（Format String），可组合颜色、标记和线型，例如 `'go--'` 表示绿色圆形标记加虚线。
- **`data`**：可索引的带标签数据对象，例如字典、结构化 NumPy 数组或 Pandas `DataFrame`；传入后可用字段名指定 `x`、`y`。
- **`color` / `c`**：线条颜色，可使用颜色名、单字符代码、十六进制、RGB/RGBA 元组等。
- **`linestyle` / `ls`**：线型。
- **`linewidth` / `lw`**：线宽，单位为点（Point）。
- **`marker`**：数据点标记样式。
- **`markerfacecolor` / `mfc`**：标记填充颜色。
- **`markeredgecolor` / `mec`**：标记边缘颜色。
- **`markersize` / `ms`**：标记尺寸，单位为点。
- **`label`**：图例标签，后续由 `legend()` 读取。
- **`scalex` / `scaley`**：是否根据数据调整横轴或纵轴视图范围，默认均为 `True`。
- **返回值（Return Value）**：`Line2D` 对象列表；即使只画一条线，也返回列表，因此常用 `line, = ax.plot(...)` 解包。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y = np.sin(x)

line, = plt.plot(
    x,
    y,
    color="skyblue",
    linestyle="-.",
    linewidth=2,
    marker="h",
    markerfacecolor="gold",
    markersize=8,
    label="sin(x)",
)
print(type(line).__name__)  # 输出: Line2D
plt.show()  # 图形结果: 天蓝色点画线、金色六边形标记
```

> [!warning] `fmt` 与关键字冲突（Format-string Conflict）
> `fmt` 和关键字参数可以混用；如果二者对同一属性给出冲突值，关键字参数优先。为了降低阅读歧义，复杂样式建议全部使用具名关键字。

### 2.2 常用线型（Line Styles）

|简写|名称|说明|
|---|---|---|
|`'-'`|`'solid'`|实线|
|`'--'`|`'dashed'`|虚线|
|`'-.'`|`'dashdot'`|点画线|
|`':'`|`'dotted'`|点线|
|`''`、`'None'`、`None` 或空格|无|不绘制连接线，只保留标记|

### 2.3 常用标记（Markers）

|样式|说明|样式|说明|
|---|---|---|---|
|`'.'`|点标记|`','`|像素标记|
|`'o'`|圆形标记|`'v'`|下三角标记|
|`'^'`|上三角标记|`'<'`|左三角标记|
|`'>'`|右三角标记|`'1'`|下三叉标记|
|`'2'`|上三叉标记|`'3'`|左三叉标记|
|`'4'`|右三叉标记|`'8'`|八边形标记|
|`'s'`|方形标记|`'p'`|五边形标记|
|`'P'`|填充加号标记|`'*'`|星形标记|
|`'h'`|六边形 1 标记|`'H'`|六边形 2 标记|
|`'+'`|加号标记|`'x'`|叉号标记|
|`'X'`|填充叉号标记|`'D'`|菱形标记|
|`'d'`|瘦菱形标记|`'|'`|竖线标记|
|`'_'`|横线标记|||

### 2.4 原稿颜色名与十六进制对照（Source Color-name Reference）
以下颜色名按原稿完整保留。十六进制颜色不需要在 Python 字符串中转义 `#`。

|颜色名|十六进制|颜色名|十六进制|颜色名|十六进制|
|---|---|---|---|---|---|
|`aliceblue`|`#F0F8FF`|`antiquewhite`|`#FAEBD7`|`aqua`|`#00FFFF`|
|`bisque`|`#FFE4C4`|`black`|`#000000`|`blanchedalmond`|`#FFEBCD`|
|`burlywood`|`#DEB887`|`cadetblue`|`#5F9EA0`|`chartreuse`|`#7FFF00`|
|`cornsilk`|`#FFF8DC`|`crimson`|`#DC143C`|`cyan`|`#00FFFF`|
|`darkgray`|`#A9A9A9`|`darkgreen`|`#006400`|`darkkhaki`|`#BDB76B`|
|`darkorchid`|`#9932CC`|`darkred`|`#8B0000`|`darksalmon`|`#E9967A`|
|`darkturquoise`|`#00CED1`|`darkviolet`|`#9400D3`|`deeppink`|`#FF1493`|
|`firebrick`|`#B22222`|`floralwhite`|`#FFFAF0`|`forestgreen`|`#228B22`|
|`gold`|`#FFD700`|`goldenrod`|`#DAA520`|`gray`|`#808080`|
|`hotpink`|`#FF69B4`|`indianred`|`#CD5C5C`|`indigo`|`#4B0082`|
|`lavenderblush`|`#FFF0F5`|`lawngreen`|`#7CFC00`|`lemonchiffon`|`#FFFACD`|
|`lightgoldenrodyellow`|`#FAFAD2`|`lightgreen`|`#90EE90`|`lightgray`|`#D3D3D3`|
|`lightskyblue`|`#87CEFA`|`lightslategray`|`#778899`|`lightsteelblue`|`#B0C4DE`|
|`linen`|`#FAF0E6`|`magenta`|`#FF00FF`|`maroon`|`#800000`|
|`aquamarine`|`#7FFFD4`|`azure`|`#F0FFFF`|`beige`|`#F5F5DC`|
|`blue`|`#0000FF`|`blueviolet`|`#8A2BE2`|`brown`|`#A52A2A`|
|`chocolate`|`#D2691E`|`coral`|`#FF7F50`|`cornflowerblue`|`#6495ED`|
|`darkblue`|`#00008B`|`darkcyan`|`#008B8B`|`darkgoldenrod`|`#B8860B`|
|`darkmagenta`|`#8B008B`|`darkolivegreen`|`#556B2F`|`darkorange`|`#FF8C00`|
|`darkseagreen`|`#8FBC8F`|`darkslateblue`|`#483D8B`|`darkslategray`|`#2F4F4F`|
|`deepskyblue`|`#00BFFF`|`dimgray`|`#696969`|`dodgerblue`|`#1E90FF`|
|`fuchsia`|`#FF00FF`|`gainsboro`|`#DCDCDC`|`ghostwhite`|`#F8F8FF`|
|`green`|`#008000`|`greenyellow`|`#ADFF2F`|`honeydew`|`#F0FFF0`|
|`ivory`|`#FFFFF0`|`khaki`|`#F0E68C`|`lavender`|`#E6E6FA`|
|`lightblue`|`#ADD8E6`|`lightcoral`|`#F08080`|`lightcyan`|`#E0FFFF`|
|`lightpink`|`#FFB6C1`|`lightsalmon`|`#FFA07A`|`lightseagreen`|`#20B2AA`|
|`lightyellow`|`#FFFFE0`|`lime`|`#00FF00`|`limegreen`|`#32CD32`|
|`mediumaquamarine`|`#66CDAA`|`mediumblue`|`#0000CD`|`mediumorchid`|`#BA55D3`|
|`mediumpurple`|`#9370DB`|`mediumseagreen`|`#3CB371`|`mediumslateblue`|`#7B68EE`|
|`midnightblue`|`#191970`|`mintcream`|`#F5FFFA`|`mistyrose`|`#FFE4E1`|
|`oldlace`|`#FDF5E6`|`olive`|`#808000`|`olivedrab`|`#6B8E23`|
|`palegoldenrod`|`#EEE8AA`|`palegreen`|`#98FB98`|`paleturquoise`|`#AFEEEE`|
|`peru`|`#CD853F`|`pink`|`#FFC0CB`|`plum`|`#DDA0DD`|
|`rosybrown`|`#BC8F8F`|`royalblue`|`#4169E1`|`saddlebrown`|`#8B4513`|
|`seashell`|`#FFF5EE`|`sienna`|`#A0522D`|`silver`|`#C0C0C0`|
|`snow`|`#FFFAFA`|`springgreen`|`#00FF7F`|`steelblue`|`#4682B4`|
|`tomato`|`#FF6347`|`turquoise`|`#40E0D0`|`violet`|`#EE82EE`|
|`yellow`|`#FFFF00`|`yellowgreen`|`#9ACD32`|||

> [!note] 颜色别名（Color Aliases）
> `aqua` 与 `cyan` 都是 `#00FFFF`，`fuchsia` 与 `magenta` 都是 `#FF00FF`。还可以使用单字符颜色代码：`b`、`g`、`r`、`c`、`m`、`y`、`k`、`w`。

## 3. `plt.figure()` 创建和切换画布（Figure Creation and Selection）
### 3.1 隐式创建（Implicit Creation）
如果没有当前 Figure 和 Axes，第一次调用 `plt.plot()` 会自动创建。重复调用 `plt.plot()` 会继续画在当前 Axes 上，而不是每次创建新画布。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
plt.plot(x, 2 * x + 2, color="gold")
plt.plot(x, x**2, color="red")
plt.plot(x, np.sin(x), color="green")
plt.show()  # 图形结果: 同一个 Axes 中有直线、抛物线和正弦曲线
```

### 3.2 显式创建和多个画布（Explicit Creation and Multiple Figures）
常用签名：
```text
plt.figure(num=None, figsize=None, dpi=None, *, facecolor=None, clear=False, **kwargs)
```
- **`num`**：画布编号或名称；已存在同名/同编号 Figure 时会激活该对象，而不是必然新建。
- **`figsize`**：宽和高组成的二元组，单位为英寸。默认来自 `rcParams['figure.figsize']`，常见默认值为 `(6.4, 4.8)`。
- **`dpi`**：每英寸点数（Dots Per Inch），默认来自 `rcParams['figure.dpi']`，常见默认值为 `100`。
- **`facecolor`**：Figure 背景颜色。
- **`clear`**：如果找到已有 Figure，是否清除其中内容，默认 `False`。
- **返回值（Return Value）**：`Figure` 对象。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y = np.sin(x)

first = plt.figure(num=3, figsize=(7, 3), dpi=72, facecolor="red")
plt.plot(x, y)

second = plt.figure(num="画布二", figsize=(7, 3), dpi=72, facecolor="green")
plt.plot(x, y)

print(first is second)  # 输出: False
plt.show()  # 图形结果: 两个独立 Figure，分别具有红色和绿色背景
```

> [!tip] 资源释放（Resource Release）
> 在循环或批量生成图片时应使用 `plt.close(fig)` 释放不再需要的 Figure，否则可能持续占用内存并触发“打开过多 Figure”的警告。

## 4. 中文字体与负号（Chinese Fonts and Minus Signs）
- `font.sans-serif` 是无衬线字体候选列表；`SimHei` 只有在系统已经安装时才能使用。
- `axes.unicode_minus=False` 让坐标轴负号使用 ASCII 连字符而不是 Unicode 负号，可绕过部分中文字体缺少负号字形的问题，但排版语义不如真正的 Unicode 负号。
- 没有任何单一字体覆盖全部 Unicode 字符。跨平台项目应选择实际安装的 CJK 字体，并在部署环境验证。

```python
import matplotlib.pyplot as plt

# 把本机可用的中文字体放在前面；找不到 SimHei 时继续尝试后续字体。
plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False
```

## 5. 坐标轴配置（Axes Configuration）
### 5.1 标签（Axis Labels）
`plt.xlabel()` 和 `plt.ylabel()` 设置当前 Axes 的横纵轴标签，并返回 `Text` 对象。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y = np.sin(x)

plt.plot(x, y)
plt.xlabel("这是 x 轴")
plt.ylabel("这是 y 轴", fontsize=14)
plt.show()  # 图形结果: 正弦曲线带有中文横纵轴标签
```

### 5.2 刻度位置与标签（Tick Positions and Labels）
常用形式：`plt.xticks(ticks=None, labels=None, **kwargs)` 和 `plt.yticks(...)`。
- **`ticks`**：刻度位置序列；传入空列表 `[]` 可隐藏对应轴刻度，但不会关闭坐标系。
- **`labels`**：与刻度位置一一对应的显示文本；省略时显示刻度数值。
- `plt.axis("off")` 会关闭整个坐标体系的可视元素，与只隐藏某一轴刻度不同。
- 手动刻度设置依赖当前 Axes；更复杂代码优先使用 `ax.set_xticks()` 和 `ax.set_yticks()`。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y = np.sin(x)

fig, axs = plt.subplots(2, 2, figsize=(9, 6))
for ax in axs.flat:
    ax.plot(x, y)

axs[0, 0].set_yticks([-1, -0.8, -0.5, -0.1, 1], ["a", "b", "c", "d", "e"])
axs[0, 1].set_xticks([])  # 只隐藏 x 轴刻度
axs[1, 0].axis("off")     # 关闭整个坐标体系
axs[1, 1].set_xticks(np.linspace(-4, 4, 9))
axs[1, 1].set_yticks([-1, -0.8, -0.5, -0.1, 1])
plt.show()  # 图形结果: 四个子图分别展示自定义刻度、隐藏刻度和关闭坐标系
```

### 5.3 边框颜色与可见性（Spine Color and Visibility）
1. `plt.gca()` 获取当前坐标系（Get Current Axes）。
2. `ax.spines['top']`、`'bottom'`、`'left'`、`'right'` 获取四条边框（Spine）。
3. `set_color('none')` 可隐藏边框；也可以使用 `set_visible(False)` 更直接表达隐藏意图。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y = np.sin(x)

plt.plot(x, y)
plt.yticks([-1, -0.8, -0.5, -0.1, 1], ["a", "b", "c", "d", "e"])
ax = plt.gca()
ax.spines["right"].set_color("none")
ax.spines["top"].set_color("none")
ax.spines["left"].set_color("red")
ax.spines["bottom"].set_color("green")
plt.show()  # 图形结果: 上、右边框隐藏，左边框红色，底边框绿色
```

### 5.4 指定刻度所在边框（Tick Position）
使用 `ax.xaxis.set_ticks_position()` 和 `ax.yaxis.set_ticks_position()` 可以让刻度显示在上、下、左或右侧。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y = np.sin(x)

plt.plot(x, y)
ax = plt.gca()
ax.spines["right"].set_color("skyblue")
ax.spines["top"].set_color("blue")
ax.spines["left"].set_color("red")
ax.spines["bottom"].set_color("green")
ax.xaxis.set_ticks_position("top")
ax.yaxis.set_ticks_position("right")
plt.show()  # 图形结果: x 轴刻度在顶部，y 轴刻度在右侧
```

### 5.5 移动边框到数据坐标（Spine Position）
`spine.set_position(('data', value))` 把边框移动到指定数据坐标；坐标范围改变时，其显示位置也会随数据变换更新。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y = np.sin(x)

plt.plot(x, y)
ax = plt.gca()
ax.spines["right"].set_color("none")
ax.spines["top"].set_color("none")
ax.spines["left"].set_color("red")
ax.spines["bottom"].set_color("green")
ax.spines["left"].set_position(("data", 0))
ax.spines["bottom"].set_position(("data", -0.1))
plt.show()  # 图形结果: 左边框移动到 x=0，底边框移动到 y=-0.1
```

## 6. `plt.legend()` 图例（Legend）
支持以下主要调用形式：
```python
plt.legend()
plt.legend(handles, labels)
plt.legend(handles=handles)
plt.legend(labels)
```
- **`handles`**：要加入图例的 Artist 列表，例如 `Line2D`。
- **`labels`**：图例文字；与 `handles` 同时传入时，两者长度应相同，否则会截断到较短长度。
- **`loc`**：图例位置，默认通常为 `'best'`；大数据图上自动寻找最少遮挡位置可能较慢。
- **`fontsize`**：图例字体大小。
- **`frameon`**：是否绘制图例边框背景。
- **`edgecolor`**：图例边框颜色。
- **`facecolor`**：图例背景颜色。
- **返回值（Return Value）**：`Legend` 对象。
- 只传 `labels` 会按 Artist 顺序隐式配对，顺序变化时容易标错，官方文档不推荐；优先在绘图时设置 `label`，或同时显式传入 `handles` 和 `labels`。
- 标签以下划线 `_` 开头的 Artist 默认不参加自动图例；没有有效标签时直接调用 `legend()` 可能产生警告并得到空图例。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y1 = 2 * x + 1
y2 = np.sin(x)

fig, axs = plt.subplots(1, 3, figsize=(13, 3))

axs[0].plot(x, y1, color="blue", label="直线")
axs[0].plot(x, y2, color="green", label="曲线")
axs[0].legend(loc="lower right", fontsize=10, frameon=True,
              edgecolor="red", facecolor="yellow")

line1, = axs[1].plot(x, y1, color="blue")
line2, = axs[1].plot(x, y2, color="green")
axs[1].legend(handles=[line1, line2], labels=["直线", "曲线"])

line3, = axs[2].plot(x, y1, color="blue", label="原始标签")
axs[2].legend(handles=[line3], labels=["线条 1"])

plt.show()  # 图形结果: 三种图例创建方式，第三个图例覆盖原始标签
```

## 7. `plt.text()` 数据坐标文字（Text Annotation）
常用签名：`plt.text(x, y, s, **kwargs)`。
- **`x` / `y`**：默认位于数据坐标系中的文字锚点。
- **`s`**：文字内容。
- **`fontsize` / `size`**：字号。
- **`color`**：文字颜色。
- **`ha`**：水平对齐（Horizontal Alignment），常用 `'left'`、`'right'`、`'center'`。
- **`va`**：垂直对齐（Vertical Alignment），常用 `'top'`、`'bottom'`、`'center'`。
- **返回值（Return Value）**：`Text` 对象。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y = np.sin(x)

plt.plot(x, y)
plt.text(x=1.1, y=0.6, s="y = sin(x)", size=16, color="red")
plt.show()  # 图形结果: 曲线上方约 (1.1, 0.6) 处显示红色说明文字
```

> [!note] 坐标变换（Coordinate Transform）
> `text()` 默认使用数据坐标；如果需要把文字固定在 Axes 的相对位置，可使用对象接口并传入 `transform=ax.transAxes`，此时 `(0, 0)` 到 `(1, 1)` 表示 Axes 左下到右上。

## 8. 散点图（Scatter Plot）
常用签名：`plt.scatter(x, y, s=None, c=None, marker=None, alpha=None, linewidths=None, edgecolors=None, **kwargs)`。
- **`x` / `y`**：点的横纵坐标；底层会把输入展平，点数应能相互广播或匹配。
- **`s`**：标记面积，单位为点平方（Points Squared）；不是标记直径。
- **`c`**：单一颜色、颜色序列或用于颜色映射的数值序列。单个 RGB/RGBA 数值序列可能与数值映射产生歧义，单色优先使用 `color=`。
- **`marker`**：标记样式，默认通常为 `'o'`。
- **`alpha`**：透明度，通常在 `0` 到 `1` 之间。
- **`linewidths`**：标记边缘线宽。
- **`edgecolors`**：标记边缘颜色。
- **边缘影响（Edge Effect）**：非零边缘线宽会向标记边界内外各扩展约一半线宽，可能让小标记的实际视觉尺寸明显变大。
- **返回值（Return Value）**：`PathCollection`。

```python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)  # 固定种子，确保每次生成相同样本
x1 = rng.normal(0, 1, 100)
y1 = rng.normal(0, 1, 100)
x2 = rng.normal(0, 1, 100)
y2 = rng.normal(0, 1, 100)

plt.scatter(x1, y1, s=90, color="green", marker="D", alpha=0.2,
            linewidths=2, edgecolors="red")
plt.scatter(x2, y2, s=90, color="yellow", marker="D", alpha=0.8,
            linewidths=2, edgecolors="black")
plt.show()  # 图形结果: 两组透明度和边框颜色不同的菱形散点
```

## 9. 条形图（Bar Plot）
常用签名：`plt.bar(x, height, width=0.8, bottom=None, *, align='center', **kwargs)`。
- **`x`**：条形横坐标或分类标签。
- **`height`**：条形高度。
- **`width`**：条形宽度，默认 `0.8`；可为标量或逐条设置。
- **`color`**：填充颜色。
- **`edgecolor`**：边框颜色。
- **`alpha`**：透明度。
- **`linewidth`**：边框线宽。
- **`bottom`**：条形底边的纵坐标，可用于堆叠或从非零位置开始。
- **`align`**：`'center'` 表示 `x` 对准条形中心，`'edge'` 表示对准左边缘；若使用负 `width` 配合 `'edge'`，可对准右边缘。
- **返回值（Return Value）**：`BarContainer`。

### 9.1 正负镜像条形图（Positive-negative Mirrored Bars）
```python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)
x = np.arange(1, 11)
h1 = rng.integers(20, 35, 10)
h2 = rng.integers(15, 40, 10)

plt.bar(x, h1, bottom=0.5)
plt.bar(x, -h2, bottom=-0.5)
for index in range(len(x)):
    plt.text(x[index], h1[index] + 0.5, str(h1[index]), ha="center")
    plt.text(x[index], -h2[index] - 0.5, str(h2[index]), va="top", ha="center")
plt.yticks(range(-40, 31, 10), [40, 30, 20, 10, 0, 10, 20, 30])
plt.show()  # 图形结果: 以零附近为中心的上下镜像条形图，并显示数值标签
```

### 9.2 并列条形图（Grouped Bars）
```python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)
x = np.arange(1, 25, 2.5)
h1 = rng.integers(20, 35, 10)
h2 = rng.integers(15, 40, 10)

plt.bar(x, h1, width=0.8, align="edge")
plt.bar(x - 0.4, h2, width=0.8)
for index in range(len(x)):
    plt.text(x[index] + 0.4, h1[index], str(h1[index]), size=8, ha="center")
    plt.text(x[index] - 0.4, h2[index], str(h2[index]), size=8, ha="center")
plt.xticks(x)
plt.show()  # 图形结果: 每个刻度附近显示两组错开的条形及数值标签
```

## 10. `plt.imshow()` 显示二维栅格或图像（Image Display）
常用签名：`plt.imshow(X, cmap=None, norm=None, *, aspect=None, interpolation=None, alpha=None, vmin=None, vmax=None, origin=None, extent=None, **kwargs)`。
- **`X`** 支持以下主要形状：
  - `(M, N)`：二维标量数据，通过归一化（Normalization）和颜色映射（Colormap）转换为颜色。
  - `(M, N, 3)`：RGB 数据，浮点值通常在 `[0, 1]`，整数值通常在 `[0, 255]`。
  - `(M, N, 4)`：带透明通道的 RGBA 数据。
- **`cmap`**：二维标量数据的颜色映射；当前常见默认值是 `'viridis'`。若要显示灰度，可使用 `'gray'` 或原稿中的反向灰度映射 `'Greys'`。
- **`norm` / `vmin` / `vmax`**：控制标量数据如何映射到颜色范围。
- **`alpha`**：透明度，可为标量或与数据兼容的数组。
- RGB/RGBA 输入已经包含颜色，`cmap` 会被忽略；超出合法范围的 RGB/RGBA 值会被裁剪。
- 实际渲染像素数由 Axes 尺寸与 Figure DPI 决定，和输入数组尺寸不一致时会发生重采样（Resampling）。
- **返回值（Return Value）**：`AxesImage`。

```python
import matplotlib.pyplot as plt
import numpy as np

data = np.array([
    [0, 50, 200],
    [200, 100, 0],
    [0, 150, 200],
])

fig, axs = plt.subplots(1, 3, figsize=(9, 3))
axs[0].imshow(data)
axs[0].set_title("默认颜色映射")
axs[1].imshow(data, cmap="Greys")
axs[1].set_title("反向灰度")
axs[2].imshow(data, cmap="Greys", alpha=0.3)
axs[2].set_title("30% 不透明度")
plt.show()  # 图形结果: 同一 3×3 数据以三种映射方式显示
```

## 11. 子图与嵌套坐标系（Subplots and Nested Axes）
### 11.1 `plt.subplot()`（Stateful Subplot API）
常用签名：`plt.subplot(nrows, ncols, index, **kwargs)`。
- **`nrows` / `ncols`**：子图网格行数和列数。
- **`index`**：位置从 `1` 开始，左上角为 `1`，按行向右递增；也可用二元组表示跨多个网格位置。
- **返回值（Return Value）**：创建或找到的 `Axes`。
- Matplotlib 3.8 以前，新建的重叠 Axes 可能被自动删除；3.8 起不再自动删除，若需要移除应显式调用 `Axes.remove()`。
- 常规网格布局更推荐 `plt.subplots()`，它一次返回 Figure 和 Axes 数组，避免频繁切换当前状态。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y1 = 2 * x + 1
y2 = x**2
y3 = np.sin(x)
y4 = np.tan(x)

plt.figure()
plt.subplot(2, 2, 1)
plt.plot(x, y1)
plt.subplot(2, 2, 2)
plt.plot(x, y2)
plt.subplot(2, 2, 3)
plt.plot(x, y3)
plt.subplot(2, 2, 4)
plt.plot(x, y4)

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(x, y1)
plt.subplot(2, 3, 4)
plt.plot(x, y2)
plt.subplot(2, 3, 5)
plt.plot(x, y3)
plt.subplot(2, 3, 6)
plt.plot(x, y4)
plt.show()  # 图形结果: 第一个 Figure 为 2×2；第二个 Figure 上方一幅、下方三幅
```

### 11.2 `plt.subplots()`（Recommended Grid API）
`plt.subplots(nrows=1, ncols=1, *, sharex=False, sharey=False, squeeze=True, **fig_kw)` 一次创建 Figure 和 Axes 集合。
- 单个子图时 `ax` 是单一 `Axes`。
- `1×N` 或 `N×1` 且 `squeeze=True` 时返回一维 Axes 数组。
- `N×M` 且两者都大于 `1` 时返回二维 Axes 数组。
- `squeeze=False` 可强制始终返回二维数组。
- `sharex` / `sharey` 控制轴共享；共享后不能直接“取消共享”。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 200)
fig, axs = plt.subplots(2, 2, sharex=True, figsize=(8, 5))
axs[0, 0].plot(x, np.sin(x))
axs[0, 1].plot(x, np.cos(x))
axs[1, 0].plot(x, np.sin(2 * x))
axs[1, 1].plot(x, np.cos(2 * x))
plt.show()  # 图形结果: 共享 x 轴的 2×2 曲线网格
```

### 11.3 `plt.axes()` 创建图中图（Inset-like Axes）
`plt.axes([left, bottom, width, height])` 使用 Figure 坐标创建 Axes，四个值通常在 `0` 到 `1` 之间，分别表示左下角位置和宽高占 Figure 的比例。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y1 = 2 * x + 1
y2 = x**2
y3 = np.sin(x)

plt.figure()
main_ax = plt.axes([0.1, 0.1, 0.8, 0.8])
main_ax.set_title("直线")
main_ax.plot(x, y1)

upper_left_ax = plt.axes([0.2, 0.6, 0.25, 0.25])
upper_left_ax.set_title("抛物线")
upper_left_ax.plot(x, y2)

lower_right_ax = plt.axes([0.6, 0.2, 0.25, 0.25])
lower_right_ax.set_title("正弦曲线")  # 原稿误写为“余弦曲线”，实际绘制的是 sin(x)
lower_right_ax.plot(x, y3)

plt.show()  # 图形结果: 一个主坐标系中叠放两个较小坐标系
```

## 12. `plt.savefig()` 保存图形（Saving Figures）
常用签名：`plt.savefig(fname, *, transparent=None, dpi='figure', format=None, metadata=None, bbox_inches=None, pad_inches=0.1, facecolor='auto', edgecolor='auto', backend=None, **kwargs)`。
- **`fname`**：文件路径、类路径对象或二进制文件对象。
- **`format`**：显式输出格式，例如 `'png'`、`'pdf'`、`'svg'`；省略时通常由扩展名推断。
- **`dpi`**：输出分辨率；`'figure'` 使用当前 Figure 的 DPI。
- **`transparent`**：是否让 Figure 和 Axes 背景透明。
- **`bbox_inches='tight'`**：尝试裁剪到包含全部 Artist 的紧凑边界。
- **`pad_inches`**：紧凑边界周围的额外留白。
- `plt.savefig()` 保存当前 Figure。使用对象接口 `fig.savefig()` 更不容易在多画布程序中保存错对象。
- 若显式给出 `format`，文件名会按原样使用，Matplotlib 不会强制让扩展名与格式一致。

### 12.1 保存静态图（Save a Static Figure）
```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

output_path = Path("img.jpg")
x = np.linspace(-3, 3, 50)
fig, ax = plt.subplots()
ax.plot(x, x**2)
fig.savefig(output_path, dpi=150, bbox_inches="tight")
plt.close(fig)  # 文件副作用: 在当前目录创建 img.jpg；无固定控制台输出
```

### 12.2 动态更新并保存最后一帧（Animation-like Update and Final Frame）
原稿在循环中用 `plt.clf()` 清除上一帧、`plt.pause()` 暂停，再在循环结束后保存最终画面。下面保留该行为并使用更清晰的变量名：
```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

output_path = Path("img.jpg")
x = np.linspace(-3, 3, 50)
accumulated_y: list[float] = []

for value in x**2:
    accumulated_y.append(float(value))
    plt.clf()               # 每轮清除上一帧，否则所有历史 Artist 会叠加并持续占用资源
    plt.plot(accumulated_y)
    plt.pause(0.1)          # 让 GUI 有机会刷新；实际暂停时长受后端和系统调度影响

plt.savefig(output_path)    # 文件副作用: 只保存循环结束时的最后一帧
plt.close()
```

## 13. 常见错误与排错（Common Errors and Troubleshooting）
- **图画到错误画布**：多 Figure 程序中过度依赖当前状态；改用 `fig, ax = plt.subplots()` 并调用 `ax.plot()`。
- **中文显示方框**：配置的字体未安装或不含目标字形；先确认操作系统字体，再设置 `font.sans-serif` 候选列表。
- **负号乱码**：字体缺少 Unicode 负号；可换字体，或在接受 ASCII 连字符取代负号时设置 `axes.unicode_minus=False`。
- **图例为空**：没有为 Artist 设置有效 `label`，或标签以下划线开头；绘图时设置 `label` 后再调用 `legend()`。
- **图例文字和线条对应错误**：只传 `labels` 导致按隐式顺序配对；同时传入 `handles` 与 `labels`。
- **散点大小异常**：把 `s` 当直径或边长；它表示面积，边缘线宽也会改变视觉尺寸。
- **`imshow()` 颜色不符合预期**：二维数组使用了默认伪彩色；显式设置 `cmap`、`vmin` 和 `vmax`。
- **保存空白或错误 Figure**：在 `show()`、`close()` 或切换当前 Figure 后调用了 `plt.savefig()`；优先持有 `fig` 并调用 `fig.savefig()`。
- **循环产生内存警告**：创建大量 Figure 后没有关闭；每次完成保存后调用 `plt.close(fig)`。
- **随机图每次不同**：没有固定随机种子；使用 `np.random.default_rng(seed)` 并记录种子。
- **重叠 Axes 未自动消失**：Matplotlib 3.8 起 `subplot()` 不再自动删除重叠 Axes；保存对象引用并显式调用 `ax.remove()`。

## 14. 参考资料（References）
- [Matplotlib `plot()` 官方文档](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html)
- [Matplotlib `legend()` 官方文档](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html)
- [Matplotlib `imshow()` 官方文档](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html)
- [Matplotlib `subplot()` 官方文档](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplot.html)
- [Matplotlib `subplots()` 官方文档](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html)
- [Matplotlib `savefig()` 官方文档](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)
- [Matplotlib 字体说明](https://matplotlib.org/stable/users/explain/text/fonts.html)
