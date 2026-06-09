# xskills

个人开发的 **Agent Skills** 集合，与各智能体共用同一套 Skill 约定。

若你是 **大语言模型 / Agent**：请先阅读仓库根目录的 **[llms.txt](llms.txt)**，其中按 [llmstxt.org](https://llmstxt.org/) 整理了本仓库的文档导航与本技能集要点，便于快速对齐上下文。

## Skill 目录结构

每个技能独占一个文件夹，按需包含：

- **`SKILL.md`** — 入口；YAML 前言区至少含 `name`、`description`，正文为智能体须遵循的步骤与约束。
- **`scripts/`** — 可执行脚本或可复用 CLI，供 SKILL 正文引用调用。
- **`references/`** — 长说明、附录、细则，按需拆出以免 `SKILL.md` 过长。
- **`assets/`** — 图片、示例数据、模板等静态资源，`SKILL.md` 中用相对路径引用。

本仓库技能放在 **`skills/<技能名>/`**（如 `api-docs`、`prd-creator`）。

跨多种智能体的通用全局目录多为 **`~/.agents/skills/`**（与 `npx skills add -g` 等配合；个别智能体另有路径时以其文档为准）。

## `npx skills` CLI

包名为 **`skills`**，通过 npx 免安装调用（命令是 **`skills`**，不是 `skill`）。CLI 的官方说明见 npm：[skills](https://www.npmjs.com/package/skills)。

```bash
npx skills add <owner/repo|git-url|本地路径>   # 安装技能到已检测到的智能体目录
npx skills add <源> --list                     # 仅列出源内可用技能
npx skills add <源> --skill <名> -a <智能体> -g -y   # 指定技能、智能体、全局、跳过确认

npx skills init [名称]                         # 生成 SKILL.md 模板
npx skills list                                # 已安装技能（同 npx skills ls）
npx skills find [关键词]                      # 搜索 / 交互查找
npx skills update [技能名…]                    # 更新
npx skills remove [技能名…]                    # 卸载（同 npx skills rm）
```

常用选项：`-g` / `--global` 装到用户目录；`-a` / `--agent` 指定智能体（如 `cursor`、`claude-code`）；`--copy` 复制而非符号链接。发现与规范见 [skills.sh](https://skills.sh)、[Agent Skills 规范](https://agentskills.io)。

## 安装本仓库技能

本仓库内技能均在 **`skills/<技能名>/`** 目录下。`npx skills add` 会**扫描仓库中的 `skills/` 文件夹**；指定仓库根为源时，**不**加 `--skill` 则会**安装其中全部技能**。

**一键安装本仓库全部技能**（推荐）：

```bash
npx skills add https://github.com/xiongxianzhu/xskills -g -y
```

源地址为**仓库根**（或 GitHub 短名 / 本地 `.`），**不是**单独指向 `skills/` 子目录。加 `-g` 装到用户全局技能目录；加 `-a cursor` 等可指定智能体。

当前包含：

| 技能名 | 说明 |
| --- | --- |
| `api-docs` | [编写 API 文档](./skills/api-docs/SKILL.md)（按仓库内 specification 格式） |
| `prd-creator` | [编写 PRD / 需求文档](./skills/prd-creator/SKILL.md) |
| `agnes-image` | [Agnes 生图](./skills/agnes-image/SKILL.md)（Agnes Image 2.1 Flash 文生图 / 图生图） |
| `agnes-video` | [Agnes 生视频](./skills/agnes-video/SKILL.md)（Agnes-Video-V2.0 文生 / 图生 / 多图 / 关键帧） |

**已克隆仓库时**：在克隆根目录执行（`.` 表示当前仓库根）。

```bash
cd xskills

npx skills add . -g -y                       # 安装 skills/ 下全部技能（全局）

npx skills add . --list                      # 仅列出本仓库内可安装的技能
npx skills add . --skill api-docs -g -y      # 只安装 api-docs
npx skills add . --skill prd-creator -g -y   # 只安装 prd-creator

# 指定 Agent（若自动检测不是你用的那个）
npx skills add . -a cursor -g -y
```

**未克隆、从 GitHub 安装**（请将短名与你的 fork 一致；以下为当前上游示例）：

```bash
npx skills add https://github.com/xiongxianzhu/xskills -g -y   # 安装 skills/ 下全部技能

npx skills add xiongxianzhu/xskills --list                     # 仅列出可安装技能
npx skills add xiongxianzhu/xskills --skill api-docs -g -y     # 只安装某一个
```

短名与 HTTPS URL 等价；仅安装单个技能时用 `--skill <名>`。安装后可用 `npx skills list` 确认是否已就绪。

## 推荐

- [frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)：高完成度前端界面
- [find-skills](https://github.com/vercel-labs/skills)：在对话里发现、安装技能，配合 `npx skills find` / `add`
- [git-commit](https://skills.sh/github/awesome-copilot/git-commit)：撰写规范 Git 提交信息（约定式提交 / Conventional Commits）
- [prd](https://skills.sh/github/awesome-copilot/prd)：撰写规范化 PRD / 产品需求文档（本仓库同名能力为 [prd-creator](./skills/prd-creator/SKILL.md)）
- [to-prd](https://skills.sh/mattpocock/skills/to-prd)：基于当前对话与代码库理解合成 PRD（模块拆分、实现/测试决策、Out of Scope；与上文「prd」的访谈式流程互补）
- [stitch::extract-design-md](https://skills.sh/google-labs-code/stitch-skills/stitch::extract-design-md)（来源 [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills)）：从 React/Vue/Tailwind 等**前端源码**反推 **DESIGN.md** 设计系统（色板、字体、间距、组件模式），无需先跑起来；与同仓库基于渲染 HTML 的 `design-md` 互补，便于 Stitch 工作流
- [git-branch-naming](https://github.com/laurigates/claude-plugins/tree/main/git-plugin/skills/git-branch-naming)：分支命名

cli安装:

```sh
npx skills add anthropics/skills --skill frontend-design -g -y
npx skills add vercel-labs/skills --skill find-skills -g -y
npx skills add github/awesome-copilot --skill git-commit -g -y
npx skills add github/awesome-copilot --skill prd -g -y
npx skills add mattpocock/skills --skill to-prd -g -y
npx skills add github/awesome-copilot --skill create-llms -g -y
npx skills add github/awesome-copilot --skill update-llms -g -y
npx skills add google-labs-code/stitch-skills --skill stitch::extract-design-md -g -y
npx skills add laurigates/claude-plugins --skill git-branch-naming -g -y
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```

## 许可

见 [LICENSE](./LICENSE)。
