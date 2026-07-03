<div align="center">

# xskills

跨智能体共用的 **Agent Skills** 集合

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Spec-6366F1?style=for-the-badge&logo=openai&logoColor=white)](https://agentskills.io)
[![Skills CLI](https://img.shields.io/badge/CLI-npx%20skills-0EA5E9?style=for-the-badge&logo=npm&logoColor=white)](https://www.npmjs.com/package/skills)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-5-F59E0B?style=for-the-badge)](./skills/)
[![llms.txt](https://img.shields.io/badge/llms.txt-Navigation-64748B?style=for-the-badge)](./llms.txt)
[![Stars](https://img.shields.io/github/stars/xiongxianzhu/xskills?style=for-the-badge&logo=github&label=Stars&color=181717)](https://github.com/xiongxianzhu/xskills/stargazers)
[![Forks](https://img.shields.io/github/forks/xiongxianzhu/xskills?style=for-the-badge&logo=github&label=Forks&color=181717)](https://github.com/xiongxianzhu/xskills/forks)

</div>

---

> **Agent / LLM**：请先阅读 [`llms.txt`](./llms.txt)（[llmstxt.org](https://llmstxt.org/) 格式），快速对齐本仓库文档导航与技能要点。

## 目录结构

每个技能位于 `skills/<技能名>/`，按需包含：

| 路径 | 说明 |
| --- | --- |
| `SKILL.md` | 入口；YAML 含 `name`、`description`，正文为步骤与约束 |
| `scripts/` | 可执行脚本 / CLI |
| `references/` | 长文档、附录、细则 |
| `assets/` | 模板、示例数据等静态资源 |

全局安装目录通常为 `~/.agents/skills/`（配合 `npx skills add -g`；个别智能体路径以其文档为准）。

## CLI

包名 **`skills`**（非 `skill`），通过 npx 免安装调用。详见 [npm: skills](https://www.npmjs.com/package/skills)。

| 命令 | 说明 |
| --- | --- |
| `npx skills add <源>` | 安装到已检测到的智能体目录 |
| `npx skills add <源> --list` | 列出源内可用技能 |
| `npx skills add <源> --skill <名> -a <智能体> -g -y` | 指定技能、智能体、全局、跳过确认 |
| `npx skills init [名称]` | 生成 `SKILL.md` 模板 |
| `npx skills list` / `ls` | 查看已安装技能 |
| `npx skills list -g` | 查看本地所有已安装的全局技能 |
| `npx skills find [关键词]` | 搜索 / 交互查找 |
| `npx skills update [技能名…]` | 更新 |
| `npx skills remove [技能名…]` / `rm` | 卸载 |

常用选项：`-g` 全局安装 · `-a` 指定智能体（如 `cursor`） · `--copy` 复制而非符号链接。

规范与发现：[skills.sh](https://skills.sh) · [Agent Skills 规范](https://agentskills.io)

## 安装

`npx skills add` 扫描仓库中的 `skills/` 目录；源地址为**仓库根**（非 `skills/` 子路径）。不加 `--skill` 时安装全部技能。

| 场景 | 命令 |
| --- | --- |
| 一键安装全部（推荐） | `npx skills add https://github.com/xiongxianzhu/xskills -g -y` |
| 已克隆，安装全部 | `cd xskills && npx skills add . -g -y` |
| 已克隆，列出可装技能 | `npx skills add . --list` |
| 只装某一个 | `npx skills add . --skill dingtalk-log -g -y` |
| 指定 Agent | `npx skills add . -a cursor -g -y` |

未克隆时，短名与 HTTPS URL 等价：

```bash
npx skills add xiongxianzhu/xskills -g -y
npx skills add xiongxianzhu/xskills --skill api-docs -g -y
```

安装后执行 `npx skills list -g` 确认全局技能已就绪。

## 本仓库技能

文档写作、需求整理、多媒体生成与日常办公辅助：

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| [`api-docs`](./skills/api-docs/SKILL.md) | 按仓库规范编写 API 文档 | [规范](./skills/api-docs/references/specification.md) |
| [`prd-creator`](./skills/prd-creator/SKILL.md) | 编写 PRD / 需求文档 | [模板](./skills/prd-creator/references/template.md) |
| [`agnes-image`](./skills/agnes-image/SKILL.md) | Agnes Image 2.1 Flash 文生图 / 图生图 | [API](./skills/agnes-image/references/api.md) |
| [`agnes-video`](./skills/agnes-video/SKILL.md) | Agnes-Video-V2.0 文生 / 图生 / 多图 / 关键帧 | [API](./skills/agnes-video/references/api.md) |
| [`dingtalk-log`](./skills/dingtalk-log/SKILL.md) | 口语任务润色为钉钉工作日志 | [使用说明](./skills/dingtalk-log/references/usage.md) |

## 推荐技能

| 技能 | 说明 |
| --- | --- |
| [frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | 高完成度前端界面 |
| [find-skills](https://github.com/vercel-labs/skills) | 对话中发现、安装技能 |
| [git-commit](https://skills.sh/github/awesome-copilot/git-commit) | 约定式提交（Conventional Commits） |
| [prd](https://skills.sh/github/awesome-copilot/prd) | 规范化 PRD（本仓库同名：[prd-creator](./skills/prd-creator/SKILL.md)） |
| [to-prd](https://skills.sh/mattpocock/skills/to-prd) | 基于对话与代码库合成 PRD |
| [stitch::extract-design-md](https://skills.sh/google-labs-code/stitch-skills/stitch::extract-design-md) | 从前端源码反推 DESIGN.md |
| [git-branch-naming](https://github.com/laurigates/claude-plugins/tree/main/git-plugin/skills/git-branch-naming) | 分支命名规范 |
| [design-taste-frontend](https://skills.sh/Leonxlnx/taste-skill/design-taste-frontend) | 反模板化落地页 / 作品集，规避 AI 审美痕迹 |
| [skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | 创建、改进 Agent Skill，含评测与描述优化 |
| [vercel-react-best-practices](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices) | Vercel 出品 React / Next.js 性能优化（70+ 规则） |
| [web-design-guidelines](https://skills.sh/vercel-labs/agent-skills/web-design-guidelines) | 按 Web Interface Guidelines 审查 UI（无障碍、UX、性能） |
| [generate-image](https://skills.sh/github/awesome-copilot/generate-image) | 调用 OpenAI / Gemini 生图（自动检测 API Key） |
| [technical-writer](https://github.com/shubhamsaboo/awesome-llm-apps) | 技术文档写作（README、API 文档、教程、变更说明） |
| [karpathy-guidelines](https://github.com/multica-ai/andrej-karpathy-skills) | Karpathy 式编码准则：避免过度设计，精准改动，明确验收标准 |

**批量安装**

```bash
npx skills add anthropics/skills --skill frontend-design -g -y
npx skills add vercel-labs/skills --skill find-skills -g -y
npx skills add github/awesome-copilot --skill git-commit -g -y
npx skills add github/awesome-copilot --skill prd -g -y
npx skills add mattpocock/skills --skill to-prd -g -y
npx skills add github/awesome-copilot --skill create-llms -g -y
npx skills add github/awesome-copilot --skill update-llms -g -y
npx skills add google-labs-code/stitch-skills --skill stitch::extract-design-md -g -y
npx skills add laurigates/claude-plugins --skill git-branch-naming -g -y
npx skills add leonxlnx/taste-skill --skill design-taste-frontend -g -y
npx skills add anthropics/skills --skill skill-creator -g -y
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices -g -y
npx skills add vercel-labs/agent-skills --skill web-design-guidelines -g -y
npx skills add github/awesome-copilot --skill generate-image -g -y
npx skills add shubhamsaboo/awesome-llm-apps --skill technical-writer -g -y
npx skills add multica-ai/andrej-karpathy-skills --skill karpathy-guidelines -g -y
```

## 许可

[MIT License](./LICENSE)
