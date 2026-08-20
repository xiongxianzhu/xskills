<div align="center">

# xskills

跨智能体共用的 **Agent Skills** 与**提示词**集合

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Spec-6366F1?style=for-the-badge&logo=openai&logoColor=white)](https://agentskills.io)
[![Skills CLI](https://img.shields.io/badge/CLI-npx%20skills-0EA5E9?style=for-the-badge&logo=npm&logoColor=white)](https://www.npmjs.com/package/skills)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-24-F59E0B?style=for-the-badge)](./skills/)
[![llms.txt](https://img.shields.io/badge/llms.txt-Navigation-64748B?style=for-the-badge)](./llms.txt)
[![Validate Skills](https://img.shields.io/github/actions/workflow/status/xiongxianzhu/xskills/validate-skills.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=Validate%20Skills)](https://github.com/xiongxianzhu/xskills/actions/workflows/validate-skills.yml)
[![Stars](https://img.shields.io/github/stars/xiongxianzhu/xskills?style=for-the-badge&logo=github&label=Stars&color=181717)](https://github.com/xiongxianzhu/xskills/stargazers)
[![Forks](https://img.shields.io/github/forks/xiongxianzhu/xskills?style=for-the-badge&logo=github&label=Forks&color=181717)](https://github.com/xiongxianzhu/xskills/forks)

</div>

---

为 ChatGPT、Cursor、Claude Code 等智能体提供可安装技能（[`skills/`](./skills/)）与可复制提示词（[`prompts/`](./prompts/)）。技能用 [`npx skills`](https://www.npmjs.com/package/skills) 安装；提示词复制或 `@` 引用即可。

> **Agent / LLM**：先读 [`llms.txt`](./llms.txt) 对齐文档导航。

## 快速开始

```bash
npx skills add xiongxianzhu/xskills --list
npx skills add xiongxianzhu/xskills --skill api-docs -g -y
npx skills add xiongxianzhu/xskills --skill prd-creator -g -y
npx skills add xiongxianzhu/xskills --skill docs-writer -g -y
npx skills add xiongxianzhu/xskills --skill cocos-mini-game -g -y
npx skills add xiongxianzhu/xskills --skill write-wechat-articles -g -y
npx skills list -g
```

安装后在对话中说「按 api-docs 规范写接口文档」或「写一篇 AI 音乐公众号文章」即可触发对应技能。更多安装场景见下节。

## 本仓库技能

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| [`api-docs`](./skills/api-docs/SKILL.md) | 按规范编写 API 文档 | [规范](./skills/api-docs/references/specification.md) |
| [`prd-creator`](./skills/prd-creator/SKILL.md) | 编写 PRD / 需求文档 | [模板](./skills/prd-creator/references/template.md) |
| [`agnes-image`](./skills/agnes-image/SKILL.md) | Agnes Image 文生图 / 图生图 | [API](./skills/agnes-image/references/api.md) |
| [`agnes-video`](./skills/agnes-video/SKILL.md) | Agnes Video 文生 / 图生 / 关键帧 | [API](./skills/agnes-video/references/api.md) |
| [`dingtalk-log`](./skills/dingtalk-log/SKILL.md) | 口语任务润色为钉钉工作日志 | [说明](./skills/dingtalk-log/references/usage.md) |
| [`cocos-mini-game`](./skills/cocos-mini-game/SKILL.md) | 从主题、PRD 和任务规划开始，开发微信/抖音双端 Cocos Creator 2D IAA 小游戏 | [PRD 模板](./skills/cocos-mini-game/references/prd-template.md) |
| [`write-wechat-articles`](./skills/write-wechat-articles/SKILL.md) | 编写技术与 AI 创作实践公众号文章，生成可复制的 HTML 富文本预览 | [排版](./skills/write-wechat-articles/references/wechat-formatting.md) |
| [`docs-writer`](./skills/docs-writer/SKILL.md) | 技术文档写作（README / API / 教程 / 变更日志），五原则 + 四类最小结构 | [模板](./skills/docs-writer/references/templates.md) · [风格](./skills/docs-writer/references/style-guide.md) |

`write-wechat-articles` 会将文章保存到 `微信公众号文章/YYYY-MM-DD-短标题/`，并生成 `article.md`、`wechat.md`、`wechat.html` 和 `assets.md`。打开 `wechat.html`，点击“复制到公众号”后可直接粘贴到微信公众号编辑器。

按领域分类的技能容器（catalog 布局，安装命令不变）：

| 分类 | 数量 | 说明 |
| --- | --- | --- |
| [`ai-drama`](./skills/ai-drama/README.md) | 14 | AI 漫剧全链路：小说原作 → 文案 → 分镜 → 视频提示词 → 角色设定 |
| [`ai-music`](./skills/ai-music/README.md) | 2 | AI 音乐：Suno 作词与配器、MV 分镜与视频提示词 |

新建 Skill：复制 [`skills/_template/`](./skills/_template/SKILL.md)（`metadata.internal: true`，不会被一键安装）。

## 参与贡献

提交 Skill 前请阅读[贡献指南](./CONTRIBUTING.md)和[技能质量标准](./docs/skill-quality-standards.md)。仓库会通过 GitHub Actions 自动校验全部 `SKILL.md` 的 frontmatter、目录结构和本地链接。

## 提示词

单次对话行为放 [`prompts/`](./prompts/)，可重复工作流放 `skills/`。索引与新增方式见 [`prompts/README.md`](./prompts/README.md)；Prompt / Skill / Loop 分工见 [Loop 就绪度自检](./prompts/meta/loop-readiness-check.md)。

## 安装

源地址为**仓库根** `xiongxianzhu/xskills`（不是 `skills/` 子路径）。CLI 包名是 **`skills`**（不是 `skill`）。

| 场景 | 命令 |
| --- | --- |
| 列出可装技能 | `npx skills add xiongxianzhu/xskills --list` |
| 安装全部 | `npx skills add xiongxianzhu/xskills -g -y` |
| 安装单个 | `npx skills add xiongxianzhu/xskills --skill api-docs -g -y` |
| 更新全部 | `npx skills update -g -y` |
| 更新单个 | `npx skills update api-docs -g -y` |
| 检查更新 | `npx skills check` |
| 指定 Cursor | `… --skill api-docs -a cursor -g -y` |
| 本地已克隆 | `npx skills add . -g -y` |

常用选项：`-g` 全局 · `-y` 跳过确认 · `-a` 指定智能体 · `--skill` 指定技能 · `--copy` 复制而非符号链接。

其他命令：`list` / `find` / `update` / `remove` / `init`。完整说明见 [npm: skills](https://www.npmjs.com/package/skills)、[skills.sh](https://skills.sh)、[Agent Skills 规范](https://agentskills.io)。

## 推荐技能

| 技能 | 说明 |
| --- | --- |
| [frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | 高完成度前端界面 |
| [shadcn](https://ui.shadcn.com/docs/skills) | shadcn/ui 组件发现、安装与组合；读取 `components.json` |
| [find-skills](https://github.com/vercel-labs/skills) | 对话中发现、安装技能 |
| [git-commit](https://skills.sh/github/awesome-copilot/git-commit) | 约定式提交；说 commit / push 触发提交与推送 |
| [prd](https://skills.sh/github/awesome-copilot/prd) | 规范化 PRD（本仓库：[prd-creator](./skills/prd-creator/SKILL.md)） |
| [stitch::extract-design-md](https://skills.sh/google-labs-code/stitch-skills/stitch::extract-design-md) | 从前端源码反推 DESIGN.md |
| [git-branch-naming](https://github.com/laurigates/claude-plugins/tree/main/git-plugin/skills/git-branch-naming) | 分支命名规范 |
| [design-taste-frontend](https://skills.sh/Leonxlnx/taste-skill/design-taste-frontend) | 反模板化落地页 / 作品集 |
| [skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | 创建与改进 Agent Skill |
| [vercel-react-best-practices](https://skills.sh/vercel-labs/agent-skills/react-best-practices) | Vercel 官方 React / Next.js 性能优化与代码审查指南 |
| [web-design-guidelines](https://skills.sh/vercel-labs/agent-skills/web-design-guidelines) | Web Interface Guidelines 审查 |
| [generate-image](https://skills.sh/github/awesome-copilot/generate-image) | OpenAI / Gemini 生图 |
| [documentation-writer](https://skills.sh/github/awesome-copilot/documentation-writer) | 基于 Diátaxis 框架的技术文档写作 |
| [create-agentsmd](https://skills.sh/github/awesome-copilot/create-agentsmd) | 为仓库生成 AGENTS.md 编码智能体操作指南，与 `create-llms` / `update-llms` 配套 |
| [documentation](https://github.com/anthropics/knowledge-work-plugins/blob/main/engineering/skills/documentation/SKILL.md) | 技术文档写作，覆盖 README、API、架构、运维手册与入职指南；与本仓库 `docs-writer` 对标 |
| [system-design](https://skills.sh/anthropics/knowledge-work-plugins/system-design) | 从需求、规模与约束出发设计系统边界、组件和技术架构 |
| [karpathy-guidelines](https://github.com/multica-ai/andrej-karpathy-skills) | 避免过度设计、精准改动 |
| [grilling](https://skills.sh/mattpocock/skills/grilling) | 拷问式需求访谈：按设计树分轮提问，直到达成共识才动手 |
| [brainstorming](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md) | 写代码前先澄清需求、对比方案、确认设计（Superpowers 入口） |
| [hatch-pet](https://github.com/openai/skills/blob/main/skills/.curated/hatch-pet/SKILL.md) | 创建、修复、校验并打包 Codex 动画宠物与精灵图 |
| [jianying-editor](https://github.com/luoluoluo22/jianying-editor-skill) | 剪映 AI 自动化剪辑（录屏、字幕、Web 动效、导出） |
| [impeccable](https://skills.sh/pbakaus/impeccable/impeccable) | 生产级前端界面，避免通用 AI slop 美学 |
| [diagram-design](https://skills.sh/cathrynlavery/diagram-design/diagram-design) | 单文件 HTML/SVG 图表生成：27 种图型，品牌风格引导，语义模式驱动 |

```bash
npx skills add anthropics/skills --skill frontend-design -g -y
npx skills add shadcn/ui --skill shadcn -g -y
npx skills add vercel-labs/skills --skill find-skills -g -y
npx skills add github/awesome-copilot --skill git-commit -g -y
npx skills add github/awesome-copilot --skill prd -g -y
npx skills add github/awesome-copilot --skill create-llms -g -y
npx skills add github/awesome-copilot --skill update-llms -g -y
npx skills add github/awesome-copilot@create-agentsmd -g -y
npx skills add google-labs-code/stitch-skills --skill stitch::extract-design-md -g -y
npx skills add laurigates/claude-plugins --skill git-branch-naming -g -y
npx skills add leonxlnx/taste-skill --skill design-taste-frontend -g -y
npx skills add anthropics/skills --skill skill-creator -g -y
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices -g -y
npx skills add vercel-labs/agent-skills --skill web-design-guidelines -g -y
npx skills add github/awesome-copilot --skill generate-image -g -y
npx skills add github/awesome-copilot --skill documentation-writer -g -y
npx skills add anthropics/knowledge-work-plugins --skill documentation -g -y
npx skills add anthropics/knowledge-work-plugins --skill system-design -g -y
npx skills add multica-ai/andrej-karpathy-skills --skill karpathy-guidelines -g -y
npx skills add mattpocock/skills --skill grilling -g -y
npx skills add obra/superpowers --skill brainstorming -g -y
npx skills add openai/skills --skill hatch-pet -g -y
npx skills add luoluoluo22/jianying-editor-skill --skill jianying-editor -g -y
npx skills add pbakaus/impeccable@impeccable -g -y
npx skills add cathrynlavery/diagram-design --skill diagram-design -g -y
```

## 故障排查

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `No skills found` | 源路径错误或 `SKILL.md` 前言无效 | 用 `xiongxianzhu/xskills`，勿用 `…/skills` |
| 安装后未生效 | 未全局安装或智能体路径不对 | `npx skills list -g`；加 `-a cursor`；重启 IDE |
| 私有仓库装不上 | CLI 默认克隆公开仓库 | 设为公开，或 `git clone` 后 `npx skills add . -g -y` |
| 权限错误 | 无法写入 `~/.cursor/skills/` 等 | 检查目录权限，或去掉 `-g` 做项目级安装 |

## 发布

推送到 GitHub 即发布，无需 npm：

```bash
git push origin main
```

已安装用户更新：`npx skills update api-docs`。

## 许可

[MIT License](./LICENSE)
