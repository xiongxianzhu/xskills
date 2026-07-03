---
title: 提示词标题
tags: [tag1, tag2]
when: 什么场景下使用（给人看，非 Agent 自动触发）
variables: [VARIABLE_1, VARIABLE_2]
---

# 提示词标题

## 使用方式

1. 复制下方 **Prompt** 区块内容
2. 将 `{VARIABLE_1}` 等占位符替换为实际值
3. 粘贴到 Cursor / Claude / ChatGPT 等对话中使用

## Prompt

```
在此粘贴完整提示词正文。

可使用 {VARIABLE_1} 作为占位符。
```

## 示例（可选）

**输入上下文：**

（补充背景信息或粘贴代码片段）

**期望输出：**

（描述理想结果，便于日后调优）

## 升级路径（可选）

若任务**重复发生**且**可自动验收**，不必无限加长 Prompt。先做 [Loop 就绪度自检](./meta/loop-readiness-check.md)；通过后复制 [skills/_template/SKILL.md](../skills/_template/SKILL.md) 做成 Skill，并写上 Gate 与停止条件。
