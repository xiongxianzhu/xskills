---
title: Loop 就绪度自检
tags: [meta, loop, automation, skill]
when: 重复任务想自动化、或犹豫该用 Prompt 还是 Skill / Loop 时使用
variables: []
---

# Loop 就绪度自检

判断一项工作是否值得做成 **Loop**（目标 → 执行 → 验收 → 不通过重来），还是继续用 **Prompt** 或人工即可。

思路来源：[黄仁勋：Prompt 正在过时，Loop 才是新范式](https://baijiahao.baidu.com/s?id=1868955285851748417)（量子位，2026-06-25）。

## 使用方式

1. 复制下方 **Prompt**，填入你的任务描述
2. 让 Agent 按四条件逐项回答「是 / 否 / 部分」
3. 根据结论选择：继续 Prompt、升级 Skill，或设计完整 Loop

也可 `@prompts/meta/loop-readiness-check.md` 后直接描述任务。

## Prompt

```
请对以下任务做 Loop 就绪度自检，逐项回答「是 / 否 / 部分」，并给出最终建议（继续用 Prompt / 做成 Skill / 设计 Loop）。

## 四条件

1. 任务会重复发生吗？（同一类活会反复做，而非一次性）
2. 有自动化验收手段吗？（测试、Lint、格式规范、对照 checklist，机器能判对错）
3. Token 预算扛得住吗？（多轮迭代成本可接受，且能设上限）
4. Agent 有「高级工程师级」工具吗？（读写文件、终端、API、足够上下文）

## 补充原则

- 写代码的和验代码的应分开（执行者与验收者不能是同一套无约束自检）
- 必须设硬停止条件：最大迭代次数、Token 上限或时间上限
- 长任务需要 STATE.md 等状态文件，不依赖对话记忆
- 不适合 Loop 的：架构选型、鉴权/支付、产品方向等需要人判断的事

## 指标

唯一有用的衡量：每个被接受的改动，平均成本是多少。若接受率低于 50%，说明 Loop 在亏钱，应缩小范围或回到人工。

## 我的任务

（在此描述任务）
```

## 决策对照

| 四条件通过数 | 建议 |
| --- | --- |
| 0–1 | 用 [`prompts/`](../README.md) 或 [`clarify-before-execute`](./clarify-before-execute.md)，不必建 Loop |
| 2–3 | 可做成 [`skills/`](../../skills/_template/SKILL.md)（工作流 + Gate），人工触发 |
| 4 | 值得设计 Loop：触发器 + Skill/上下文 + STATE + 独立 Gate |

## 与 xskills 的对应

| 层级 | 仓库位置 | 作用 |
| --- | --- | --- |
| Prompt | `prompts/` | 单次行为约束（如先提问再执行） |
| Skill | `skills/` | 可重复工作流 + references 验收 |
| Loop | Skill + Gate + 停止条件 +（可选）STATE | Agent 自转直到通过或撞预算 |

## 期望效果

- 避免为一次性任务过度自动化
- 重复、可验收的任务有清晰升级路径
- 不跳过「理解任务本身」——你可以外包执行，但不能外包理解
