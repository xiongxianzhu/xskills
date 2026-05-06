---
name: api-docs
description: 按项目规范编写 API 文档。使用场景：用户要求写接口文档、补充 API 说明、为第三方或内部接口编写文档时。
---

# API 文档（api-docs）

按 [reference/specification.md](reference/specification.md) 编写 API 文档，保证格式统一、可供第三方或前端对接。

## 何时使用

- 撰写、补充或修订接口说明、对接文档
- 为第三方或内部调用方提供可实现的 API 描述

## 工作流程

1. 从路由与实现代码提取真实路径、参数名、类型与错误码，避免编造字段。
2. 遵守规范中的章节结构、表格列、Markdown 约束与「禁止省略」条款。
3. 版式与接口小节写法对照 [reference/examples.md](reference/examples.md)；若为已有文档增量编辑，保持与既有小节风格一致。

## 参考文件

- **`reference/specification.md`** — 章节结构、参数表约定与禁止省略规则
- **`reference/examples.md`** — 虚构「图书管理系统」完整示例
