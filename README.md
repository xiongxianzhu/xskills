# xskills

个人开发的 **Agent Skills** 集合，与各智能体共用同一套 Skill 约定。

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

## 推荐

- [frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)：高完成度前端界面
- [find-skills](https://github.com/vercel-labs/skills)：在对话里发现、安装技能，配合 `npx skills find` / `add`
- [git-commit](https://skills.sh/github/awesome-copilot/git-commit)：撰写规范 Git 提交信息（约定式提交 / Conventional Commits）

cli安装:

```sh
npx skills add anthropics/skills --skill frontend-design -g -y
npx skills add vercel-labs/skills --skill find-skills -g -y
npx skills add github/awesome-copilot --skill git-commit -g -y
```

## 许可

见 [LICENSE](./LICENSE)。
