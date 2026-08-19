# AGENTS.md

## 沟通

- 默认使用简体中文回复和编写文档。
- 先说明结果，再补充必要的操作与限制。
- 保持表达简洁，避免重复说明和无关扩展。

### 回答前的澄清流程

处理用户提出的问题时，不直接给出最终答案。先向用户说明：

1. 问题中没有明确说出、但已默认成立的假设。
2. 仍缺少的关键信息，以及这些信息可能如何改变答案。
3. 人们处理这类问题时最常犯的一个错误。

完成上述分析后，只向用户提出一个最关键的问题。该问题必须帮助 Agent 理解用户的真实目标和具体情况，避免给出任何人都能套用的通用建议。

等待用户回答后，再给出最终输出。

## Git

- 提交信息采用 Conventional Commits，例如 `feat(auth): 添加路由守卫`。
- 提交描述默认使用简体中文。
- 只暂存当前任务相关文件；提交前检查暂存内容，不得夹带日志、构建产物、编辑器文件或敏感信息。
- 不得对 `.gitignore` 忽略的目录或文件执行 `git add`；忽略规则只防未被追踪的文件，显式 `add` 会绕过忽略。
- 用户明确调用 `git-commit` Skill 时，提交当前任务相关改动后推送当前分支。
- 当前分支没有上游时，将上游设置为 `origin` 的同名分支后推送。
- 没有可提交改动但存在未推送提交时，只执行推送，不创建空提交。
- 提交失败时不继续推送；推送失败时保留本地提交，并报告失败原因和当前状态。
- 禁止强制推送、覆盖远端历史或暂存无关文件来规避失败。

## 项目概览

- 本仓库是跨智能体共用的 Agent Skills 与提示词集合，纯 Markdown 文档仓库，无应用业务代码、无构建产物。
- 面向 ChatGPT、Cursor、Claude Code 等智能体分发，通过 `npx skills add xiongxianzhu/xskills` 安装。
- 推送到 GitHub 即发布，无需 npm 发布流程。

## 仓库定位

- `skills/` 存放可重复使用的 Agent Skills。
- `prompts/` 存放单次使用或手动引用的提示词。
- `llms.txt` 提供面向智能体的仓库导航。
- `docs/skill-quality-standards.md` 是技能质量标准。
- `tests/` 与 `scripts/validate_skills.py` 负责 Skill 结构校验。

## 本地校验

```bash
# 安装校验依赖（一次性）
python -m pip install -r requirements-ci.txt

# 运行全部校验
python -m unittest discover -s tests -v
python scripts/validate_skills.py
git diff --check
```

- 首次校验前必须先安装依赖，否则 `validate_skills.py` 无法运行。
- 修改 Skill、README 或 llms.txt 后必须重新运行校验。
- GitHub Actions 在 `main` 分支提交和 Pull Request 时执行相同校验，本地通过即可避免 CI 失败。

## Skill 约定

- 新增 Skill 在仓库根目录的 `skills/<技能名>/` 下创建。
- AI 漫剧相关 Skill 放在 `skills/ai-drama/`，AI 音乐相关 Skill 放在 `skills/ai-music/`；其他通用 Skill 放在 `skills/<技能名>/` 扁平布局。
- Skill 目录名使用小写字母、数字和连字符。
- 每个 Skill 必须包含 `SKILL.md`。
- `SKILL.md` 的 YAML frontmatter 至少包含 `name` 和 `description`。
- 将核心流程保留在 `SKILL.md`，详细规范按需放入 `references/`。
- 只有可重复、需要确定性执行的逻辑才放入 `scripts/`。
- 不在 Skill 目录中新增 README、变更日志或重复说明文档。
- Skill 之间相互独立。不要在 Skill 内引用其他 Skill 的文件；如需指向，用纯文本名称。
- 新增、删除或重命名 Skill 时，同步更新 `README.md` 和 `llms.txt` 的数量与索引。

## 修改原则

- 保留用户已有的未提交修改，不覆盖或整理无关内容。
- 只修改当前任务需要的文件，不顺手重构相邻内容。
- 不提交密钥、令牌、个人数据、缓存或生成的临时文件。
- 新增链接后检查目标文件是否存在。

## 验证

- 检查 `SKILL.md` 的 frontmatter、名称和目录名是否一致。
- 检查新增文件中是否残留 `TODO`、`TBD` 或占位说明。
- 运行 `git diff --check`，确保没有空白错误。
- 修改脚本时，至少运行一个代表性示例。
- 完成后报告已验证项目和未能执行的检查。

## Pull Request

- 一个 Pull Request 只处理一个明确主题。
- 用简体中文说明动机、主要变化和验证结果。
- 提交前确认校验全部通过，`README.md` 与 `llms.txt` 已按需同步。

## 发布

- 推送到 `main` 即发布：`git push origin main`。
- 已安装用户通过 `npx skills update <技能名>` 或 `npx skills update -g -y` 更新。

## 完成报告

每次交付说明：

- 完成了什么。
- 修改了哪些文件或模块。
- 执行了哪些验证及结果。
- 仍有哪些风险、假设或阻塞项。
