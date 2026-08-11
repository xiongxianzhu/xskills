# 贡献指南

感谢你改进 xskills。提交前请保持改动聚焦，并确认内容适合重复使用。

## 新增或修改 Skill

1. 新建 Skill 时复制 [`skills/_template/`](skills/_template/SKILL.md)。
2. 目录名使用小写字母、数字和连字符，例如 `api-docs`。
3. Skill 可位于 `skills/<skill>/`，或按领域放入 `skills/<category>/<skill>/`。
4. 每个 Skill 必须包含 `SKILL.md`，其 frontmatter 至少包含非空的 `name` 和 `description`；`name` 必须与目录名一致。
5. 核心流程保留在 `SKILL.md`，详细规范放入 `references/`，确定性脚本放入 `scripts/`，可复用素材放入 `assets/`。
6. 使用相对链接引用仓库文件，并确认文件和 Markdown 锚点存在。外部链接应优先使用官方或一手资料。
7. 新增、删除或重命名 Skill 时，同步更新 `README.md` 与 `llms.txt` 的数量和索引。

详细要求见[技能质量标准](docs/skill-quality-standards.md)。

## 本地校验

```bash
python -m pip install -r requirements-ci.txt
python -m unittest discover -s tests -v
python scripts/validate_skills.py
git diff --check
```

GitHub Actions 会在提交到 `main` 和 Pull Request 时执行同样的 Skill 校验。

## 提交 Pull Request

- 一个 Pull Request 只处理一个明确主题。
- 使用简体中文说明动机、主要变化和验证结果。
- 提交信息遵循 Conventional Commits，例如 `feat(skill): 新增示例技能`。
- 不提交密钥、令牌、个人数据、缓存或临时生成文件。
- 不覆盖与本次任务无关的已有修改。

提交前确认：

- [ ] frontmatter、目录结构和链接校验通过
- [ ] 触发场景、工作流、输出和停止条件清楚
- [ ] 没有未完成标记或未解释的占位内容
- [ ] `README.md` 与 `llms.txt` 已按需同步
