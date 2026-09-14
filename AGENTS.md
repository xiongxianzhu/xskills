# AGENTS.md

## 沟通

- 默认使用简体中文回复和编写文档。
- 先说明结果，再补充必要的操作与限制。
- 保持表达简洁，避免重复说明和无关扩展。

### 回答前的澄清流程

- 仅在缺失信息会实质改变结果且无法从上下文合理推断时提问；相关缺口尽量一次收集。
- 信息足够时直接执行，仅说明影响结果的重要假设，不固定输出假设分析或常见错误。
- 等待答案时只暂停依赖该答案的部分，继续独立工作；已有明确授权不重复确认。

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
# 依赖缺失时安装
python -m pip install -r requirements-ci.txt

# 运行全部校验
python -m unittest discover -s tests -v
python scripts/validate_skills.py
git diff --check
```

- 校验前检查依赖，缺失或版本不符时安装 `requirements-ci.txt` 中的依赖，已满足时不重复安装。
- 一批相关 Skill、README 或 llms.txt 修改完成后，交付前统一运行上述校验；通过后仅在新增修改或发现问题时重跑相关检查，不逐个编辑步骤重复全量校验。
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

修改交付按需简要说明；只读问答不套用无关项目：

- 完成了什么。
- 修改了哪些文件或模块。
- 执行了哪些验证及结果。
- 仍有哪些风险、假设或阻塞项。
