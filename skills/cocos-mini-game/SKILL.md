---
name: cocos-mini-game
description: 策划、开发或修改 Cocos Creator 3.8+ 的 2D 微信与抖音小游戏。按请求处理玩法、PRD、广告接入或具体开发任务；仅在用户要求完整新项目时推进全流程。
compatibility: 需要可读写的项目工作区；趋势、平台规则和合规检查需要联网；实际构建需要 Cocos Creator 3.8+ 及对应平台开发者工具。
---

# Cocos Creator 双端小游戏开发

完整新项目从玩法决策和必要文档推进到实施，默认面向 2D IAA 小游戏；局部任务从相关阶段进入。目标平台与功能以用户请求为准，不自动追加双端、广告或发布工作。

## 核心原则

- 复用已有玩法决策、PRD 与授权；仅在方向或范围尚需用户决策时暂停相关工作。
- 公共玩法代码不直接调用 `wx` 或 `tt`，所有平台能力经过统一适配层。
- 只实现用户已授权的范围，不预建商城、复杂社交、实时对战或大型后端。
- 平台政策、API、包体限制和审核规则具有时效性，执行时查询当前官方资料并记录日期。
- 缺少工具、账号、App ID 或真机条件时如实记录阻塞，不声称已经验证。
- 图片可调用当前环境可用的生成工具；音效和 BGM 只交付专业平台生成提示词。

## 工作流

### 阶段 0：识别输入与项目

1. 提取用户给出的主题、目标平台、引擎版本和已有项目路径。
2. 用户说“微信小程序游戏”时，按 [references/project-readiness-and-compliance.md](references/project-readiness-and-compliance.md) 判断其目标是否实际为微信小游戏。
3. 只读检查现有项目结构、Cocos 版本、未提交修改和可用工具。保留用户已有改动。
4. 新项目完整阅读 [references/project-structure.md](references/project-structure.md)，默认使用单仓库：`client/` 承载完整 Cocos 项目，`docs/game/` 承载文档，可选目录按启用条件创建。
5. 新项目默认以 Cocos Creator 3.8+、TypeScript、2D 为基线；已指定平台只实现该平台，平台不明确且影响实施时再询问。
6. 按任务选择入口：仅策划或 PRD 请求交付对应文档后结束；玩法已明确时跳过阶段 1；现有项目局部修改直接进入相关实施阶段，仅更新受影响的文档与检查，不补造三份项目文档。
7. 用户已要求直接开发或批准现有方案时，继续完成授权范围，不重复请求玩法或文档审批。参考文件仅在对应阶段需要时读取，已读且未变化的内容不重读。

### 阶段 1：联网调研与玩法提案

1. 完整阅读：
   - [references/trend-research.md](references/trend-research.md)
   - [references/game-concept.md](references/game-concept.md)
2. 联网查询最近 6–12 个月的榜单、行业报告、代表产品和平台动向。
3. 区分来源事实与推断，不能把旧数据包装成当前趋势。
4. 根据主题给出 2–3 个玩法方向，包含核心循环、用户、IAA 广告点、成本、风险和推荐理由。
5. 明确推荐一个方向，同时保留其他方案的适用条件。

**方向决策：仅在玩法尚未确定且用户未授权自行选择时，请用户选择；只暂停依赖玩法的正式 PRD、代码与素材工作。**

### 阶段 2：项目准备与文档

用户选定玩法后，完整阅读：

- [references/project-readiness-and-compliance.md](references/project-readiness-and-compliance.md)
- [references/project-structure.md](references/project-structure.md)
- [references/prd-template.md](references/prd-template.md)
- [references/project-planning.md](references/project-planning.md)
- 需要后端判断时读取 [references/backend-and-data.md](references/backend-and-data.md)

在目标游戏项目创建或更新：

```text
docs/game/
├── PRD.md
├── progress.md
└── tasks.md
```

PRD 必须包含技术栈和按标准裁剪后的目标项目目录树。三份文档使用一致的功能名称、路径、范围与完成条件，不为未批准能力预建 `server/`、`shared/`、`tools/` 或资源分包目录。

**范围决策：文档仅整理已有授权时直接实施；存在影响范围或成本的未决事项时，只确认这些事项，不要求重复批准三份文档。**

### 阶段 3：实施核心游戏

实施范围已明确并获授权后：

1. 完整阅读 [references/project-structure.md](references/project-structure.md) 与 [references/cocos-architecture.md](references/cocos-architecture.md)。
2. 从 `tasks.md` 选择一个最小、无阻塞任务，标记为进行中。
3. 实现可重复游玩的闭环：启动、进入、核心操作、成功或失败、结算、再次开始。
4. 每完成一个任务就验证产物，并同步更新 `progress.md` 与 `tasks.md`。
5. 实施确需偏离 PRD 的技术栈或目录结构时，先更新 PRD 并说明原因。

### 阶段 4：素材与平台能力

按实际任务完整阅读：

- [references/assets-and-audio.md](references/assets-and-audio.md)
- [references/platform-adapter.md](references/platform-adapter.md)
- [references/wechat-mini-game.md](references/wechat-mini-game.md)
- [references/douyin-mini-game.md](references/douyin-mini-game.md)
- [references/iaa-ads.md](references/iaa-ads.md)

先建立编辑器模拟实现，再实现目标平台适配；单平台请求不增加另一平台。模拟结果必须可识别，不能伪装成真实登录、分享或广告成功。

### 阶段 5：构建、验收与交付

1. 完整阅读：
   - [references/build-and-validation.md](references/build-and-validation.md)
   - [references/release-and-operations.md](references/release-and-operations.md)
2. 新项目先验证 Web Mobile 核心玩法，再验证目标平台构建；局部修改只验证受影响行为与构建。
3. 平台 SDK 能力必须在对应开发者工具或真机验收。
4. 记录已通过、未通过、未执行和受阻项，不混用状态。
5. 最终确保 PRD、进度、任务和实际项目一致。

## 任务循环

每次只推进一个可验证任务：

```text
领取任务 → 标记进行中 → 实施 → 验证 → 回写结果 → 领取下一项
```

验证失败时保留具体错误并修复；同一外部阻塞重复出现时停止重试，记录恢复条件并继续处理不依赖该条件的任务。

## 范围变更

以下能力不在当前授权范围内时，先说明影响并取得用户确认；用户已明确要求时不重复确认，实际外部操作仍遵守其授权边界：

- 支付、内购或混合变现。
- 好友排行榜、开放数据域或复杂社交。
- 实时联网、跨设备云存档、服务端权威奖励或运营后台。
- 3D 玩法或重度物理。
- 自动发布、提审或操作线上账号。

## 交付摘要

最终报告应包含：

- 选定玩法与核心闭环。
- PRD、进度和任务文档路径。
- 主要代码与素材路径。
- 本次涉及的 Web Mobile 或目标平台验证状态。
- 外部阻塞与最短人工操作步骤。
- 音效和 BGM 提示词清单路径。
- 发布前仍需用户完成的账号、合规和真机事项。
