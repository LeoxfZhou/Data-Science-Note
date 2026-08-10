# 数据科学笔记 (Data Science Notes)

这是一个使用 Obsidian 管理的数据科学 (Data Science)、机器学习 (Machine Learning)、深度学习 (Deep Learning)、计算机视觉 (Computer Vision) 和自然语言处理 (Natural Language Processing) 知识库。

## 目录结构 (Directory Structure)

```text
.
├── Notes/                         # 已审核并正式入库的笔记
├── Attachments/                   # 由 Attachment Management 管理的附件
└── Processing/
    ├── 00-Inbox/                  # 待整理原稿
    ├── 01-Review/                 # 已整理、等待人工确认的候选稿
    └── 02-Processed/              # 最近处理原稿的备份
```

## 笔记处理流程 (Note Processing Workflow)

```text
00-Inbox 原稿
    ↓
内容整理、去重、纠错和知识补充
    ↓
01-Review 候选稿
    ↓ 人工确认
Notes 正式笔记
    ↓
02-Processed 保留最近处理原稿
```

## 编写规范 (Writing Conventions)

- 笔记以详细、可学习和可复现为目标，不因追求简短而省略关键细节。
- 中文专业名词后标注英文，例如：虚拟环境 (Virtual Environment)。
- 代码示例应包含关键原因、边界条件和常见错误说明。
- 技术来源不同但知识点相同的内容应合并，避免换一种措辞后重复保留。
- 未经确认的候选稿保留在 `Processing/01-Review/`，不会直接进入 `Notes/`。

## Obsidian 配置 (Obsidian Configuration)

附件根目录为 `Attachments/`，Attachment Management 使用以下路径规则：

```text
${notepath}/${notename}
```

本仓库保留可复用的 Obsidian 配置和插件文件，但忽略工作区布局、缓存及本机认证辅助文件。
