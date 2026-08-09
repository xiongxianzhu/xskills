# AGENTS.md

## 沟通

- 默认使用简体中文回复和编写文档。
- 先说明结果，再补充必要的操作与限制。
- 保持表达简洁，避免重复说明和无关扩展。

## 仓库定位

- `skills/` 存放可重复使用的 Agent Skills。
- `prompts/` 存放单次使用或手动引用的提示词。
- `llms.txt` 提供面向智能体的仓库导航。
- 本仓库不包含应用业务代码。

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

## Git

- 提交信息采用 Conventional Commits。
- 提交描述默认使用简体中文。
- 只暂存当前任务相关文件。
- 不得对 `.gitignore` 忽略的目录或文件执行 `git add`；忽略规则只防未被追踪的文件，显式 `add` 会绕过忽略。
