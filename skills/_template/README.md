# Skill 模板

复制本目录到新技能文件夹（如 `skills/my-skill/`），**不要**安装此目录。

`SKILL.md` 已设 `metadata.internal: true`，`npx skills add` 一键安装时会自动跳过。

新建步骤：

1. 复制 `skills/_template/` → `skills/<技能名>/`
2. 修改 `SKILL.md` 的 frontmatter 与正文
3. 按需添加 `references/`、`scripts/`、`assets/`
4. 在根目录 [README](../../README.md) 与 [llms.txt](../../llms.txt) 中登记

模板已包含 **验收（Gate）**、**停止条件**、**状态（可选）** 三节，便于从 Prompt 升级为可 Loop 的 Skill。
