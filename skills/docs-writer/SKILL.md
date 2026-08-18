---
name: docs-writer
description: 编写清晰的技术文档：README、API、教程、变更日志，并规范 README 的 Shields.io 徽章与顶部排版。当用户要求写文档、写 README、修改 README 徽章、文档化接口、写教程、写发布说明，或提到 docs、documentation、README、badge、shields、tutorial、changelog、release notes 时使用。
---

# 技术文档写作（docs-writer）

按五原则与四类文档最小结构，产出可扫描、带可运行示例的 Markdown 文档。规则与模板见 [references/style-guide.md](references/style-guide.md) 与 [references/templates.md](references/templates.md)。

## 何时使用

- 撰写或修订 README、项目说明、安装与快速上手
- 文档化 API、函数、CLI 参数、配置项
- 编写教程、上手指南、分步教学
- 撰写变更日志、发布说明、迁移指引
- 解释架构、设计决策、复杂技术概念

## 何时不使用

- 写业务代码注释、commit message、PR 描述 → 直接写，不用此 skill
- 接口契约的强约束规范 → 用 [`api-docs`](../api-docs/SKILL.md)（本仓库）
- PRD / 需求文档 → 用 [`prd-creator`](../prd-creator/SKILL.md)（本仓库）

## 写作五原则

| 原则 | 要点 | 反例 |
| --- | --- | --- |
| **目标先行** | 先答"为什么用"，再讲"怎么用" | 开头堆功能列表 |
| **示例胜过描述** | 每个概念配可运行代码 + 预期输出 | 只写文字不演示 |
| **渐进披露** | Quick Start 在前，深潜在后；复杂主题用链接隔离 | 一上来铺全部配置 |
| **可扫描** | 描述性标题、3 项以上用列表、代码加语言标签 | 大段无层级散文 |
| **主动 + 现在时** | "运行 X 返回 Y"，不是"X 被运行后 Y 被返回" | 被动语态连串 |

## 文档类型选择

按读者意图选型，而非按内容罗列：

| 读者想… | 文档类型 | 最小结构见 |
| --- | --- | --- |
| 评估/上手项目 | README | [README 模板](references/templates.md#readme) |
| 调用接口/函数 | API 文档 | [API 文档模板](references/templates.md#api-文档) |
| 跟着做完成一个任务 | 教程 | [教程模板](references/templates.md#教程) |
| 了解版本变化 | 变更日志 | [变更日志模板](references/templates.md#变更日志) |
| 理解概念/设计 | 解释性文档 | 用 README 或独立文章，遵循同样五原则 |

## README 专用规则

处理目标文件名为 `README.md` 的任务时，必须读取 [README 模板](references/templates.md#readme) 和 [README 头部与徽章](references/style-guide.md#readme-头部与徽章)，再按以下顺序执行：

1. **检查头部**：识别第一个 H1、简介、Logo、导航、已有居中容器和全部 `img.shields.io` 图片 URL。
2. **补充徽章**：没有 Shields.io 徽章时，从仓库文件提取可靠事实，默认添加 2–4 枚技术栈、许可证、CI 或版本徽章；信息不足时减少数量，不虚构状态。
3. **统一样式**：将所有 Shields.io URL 的 `style` 参数新增或替换为 `for-the-badge`，保留其他参数、图片文本和链接目标。
4. **居中头部**：居中显示 Logo、项目主标题、简介和徽章区；复用已有 `<div align="center">`，避免嵌套或重复元素。
5. **保护正文**：在第一个 H2 前结束居中区域，不重排后续章节，不修改非 Shields 图片。
6. **核对事实**：许可证、CI、版本、覆盖率和下载量等徽章必须能从仓库或可信发布源验证；无法确认时不添加并说明缺失依据。

README 以外的文档不自动应用上述徽章规则，除非用户明确要求。

## 工作流程

1. **定类型与读者**：确认上述哪类文档，读者是新手/中级/专家。
2. **套最小结构**：从 [templates.md](references/templates.md) 取对应骨架，只保留必要章节；README 先执行上方专用规则。
3. **填示例**：每个概念给可运行代码 + 预期输出；补充常见错误与解决。
4. **风格校对**：按 [style-guide.md](references/style-guide.md) 逐项过（语态、格式、术语、反模式）。
5. **链接检查**：确认内部锚点、外部链接、相对路径有效。

## 验收（Gate）

**执行者与验收者分离**：写产出的 Agent 不得在无约束下自判「已完成」。

| 角色 | 说明 |
| --- | --- |
| 执行 | 主 Agent 按工作流程产出 |
| 验收 | 对照 [style-guide.md 的反模式清单](references/style-guide.md#常见反模式校对清单) 逐项校对；至少抽检 1 个代码示例的可运行性 |

验收不通过时：带着具体错误信息修正，进入下一轮（见下方停止条件）。

## 停止条件

| 类型 | 上限 |
| --- | --- |
| 自修订迭代 | 单文档最多 3 轮 |
| Token / 成本 | 单任务预算上限（按你的工具设定） |
| 时间 | 单次运行不超过 N 分钟 |

任一条件触达即停止，汇总当前进度交人工处理。

## 参考文件

- **[references/templates.md](references/templates.md)** — README、API 文档、教程、变更日志的最小结构与示例
- **[references/style-guide.md](references/style-guide.md)** — 语态人称、格式约定、代码示例规范与常见反模式
