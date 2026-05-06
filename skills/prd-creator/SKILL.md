---
name: prd-creator
description: 根据用户提问生成专业规范的项目需求文档（PRD）。在用户要求创建 PRD、撰写需求文档、起草产品需求或记录项目需求时使用。
---

# PRD 创建（prd-creator）

根据用户输入生成可执行、可验收的 PRD；模板与撰稿细则见 [reference/template.md](reference/template.md)。

## 何时使用

- 创建 PRD、需求文档、产品需求、功能需求或需求规格说明

## 工作流程

1. **需求澄清**（必要时）：项目/功能名称、业务背景、目标用户、核心功能点、约束条件。
2. **生成正文**：按 [reference/template.md](reference/template.md) 选择标准版或简化版结构，每条需求可验收、用词规范（应/必须/可/不得），并区分功能与非功能需求、明确范围边界。
3. **落盘**：Markdown，建议路径 `docs/prd-{项目名}.md`。

## 参考文件

- **`reference/template.md`** — PRD 模板、表述规范、常见需求类型与输出撰稿规范
- **`reference/examples.md`** — 简化版 / 标准版示例与澄清对话示例
