# 提示词库

本目录存放**按需手动使用**的提示词，与 [`skills/`](../skills/) 中的 Agent Skills 分离：

| | `prompts/` | `skills/` |
| --- | --- | --- |
| 使用方式 | 复制粘贴或 `@` 引用文件 | `npx skills add` 安装后 Agent 自动遵循 |
| 格式 | 普通 Markdown | `SKILL.md` + YAML 前言 |
| 适用 | 单段 Prompt，单次对话行为 | 多步工作流；可重复任务的 Loop 雏形 |

## 目录

| 分类 | 路径 | 说明 |
| --- | --- | --- |
| 编码 | [`coding/`](./coding/) | 代码审查、重构、调试、架构讨论 |
| 写作 | [`writing/`](./writing/) | 技术博客、文档、邮件、汇报 |
| 设计 | [`design/`](./design/) | UI 评审、设计系统、视觉方向 |
| 元提示 | [`meta/`](./meta/) | 提示词优化、**Loop 就绪度**、执行前澄清、输出格式约束 |

## 新增提示词

1. 复制 [`_template.md`](./_template.md) 到对应分类目录
2. 文件名使用 `kebab-case.md`（如 `code-review.md`）
3. 填写 frontmatter 与 **Prompt** 正文
4. 在本文件「索引」表格中追加一行

## 索引

| 文件 | 说明 |
| --- | --- |
| [`meta/clarify-before-execute.md`](./meta/clarify-before-execute.md) | 先提问澄清需求，确认后再执行 |
| [`meta/loop-readiness-check.md`](./meta/loop-readiness-check.md) | 四条件自检：该用 Prompt、Skill 还是 Loop |

## 何时做成 Skill？

满足以下 **2 条以上** 时，考虑迁入 `skills/` 并写成 Skill：

- 需要 Agent **自动识别场景**并执行多步流程
- 附带 **scripts/** 或 API 调用
- 需要 **`npx skills add` 全局安装**
- 内容已是完整操作手册，而非一段 Prompt
