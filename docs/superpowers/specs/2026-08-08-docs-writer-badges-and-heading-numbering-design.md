# docs-writer 徽章与标题编号设计

## 1. 背景

`docs-writer` 已提供 README、API 文档、教程和变更日志模板，但尚未统一 Shields.io 徽章的视觉样式、标题区域对齐方式和正文标题编号。本设计为这些 Markdown 文档增加默认排版规则，同时保留用户明确要求和外部规范的优先级。

## 2. 目标

- Markdown 使用 Shields.io 徽章时，默认采用 `for-the-badge` 样式。
- 使用 Shields.io 徽章时，默认居中显示 H1、简介和徽章区。
- H2 及更深正文标题默认使用完整层级编号，所有编号末尾都带句点。
- README 和其他文档模板提供一致、可复制的写法。
- 修改已有文档时避免无关重排。

## 3. 非目标

- 不要求所有 Markdown 文档必须使用徽章。
- 不居中 H2、H3、H4 等正文标题。
- 不修改仓库根目录现有 `README.md`。
- 不新增自动格式化或检查脚本。
- 不覆盖用户明确指定的样式、对齐或编号规则。

## 4. 方案

采用“主流程 + 风格指南 + 模板”三层约束：

1. `SKILL.md` 声明默认排版行为和覆盖优先级。
2. `references/style-guide.md` 记录精确规则与校对项。
3. `references/templates.md` 在 README、API 文档、教程和变更日志模板中展示规范写法。

该方案比只修改主入口更不容易遗漏具体语法，也避免为简单格式规则增加脚本维护成本。

## 5. Shields.io 规则

当文档使用 `https://img.shields.io/` 图片 URL 时：

- URL 默认包含 `style=for-the-badge`。
- URL 没有查询参数时使用 `?style=for-the-badge`。
- URL 已有其他查询参数时使用 `&style=for-the-badge`。
- URL 已有 `style` 参数时替换其值，不重复添加参数。
- 用户明确指定其他 shields 样式时保留用户选择。

默认头部结构：

```markdown
<div align="center">

# 项目名

一句话价值主张。

[![构建状态](https://img.shields.io/badge/build-passing-22C55E?style=for-the-badge)](https://example.com/build)
[![许可](https://img.shields.io/badge/license-MIT-6366F1?style=for-the-badge)](./LICENSE)

</div>
```

居中范围仅包含 H1、紧随其后的简介和徽章区。正文从居中容器结束后开始，H2 及以下标题保持左对齐。

## 6. 正文标题编号

H1 作为文档标题，不编号。H2 及以下标题使用继承父级的完整层级编号，编号末尾统一带句点：

```markdown
# 文档标题

## 1. 安装
### 1.1. 环境要求
### 1.2. 安装步骤
#### 1.2.1. Windows

## 2. 快速开始
### 2.1. 基本用法
```

编号规则：

- H2 使用 `1.`、`2.`、`3.` 依次递增。
- H3 使用 `1.1.`、`1.2.`、`2.1.` 等完整父子编号。
- H4 及更深层级继续追加数字，并在末尾保留句点。
- 同级编号连续；新增、删除或移动章节后同步重排受影响章节。
- 不跳过标题层级，例如 H2 后不直接使用 H4。

## 7. 模板适配

- README：H1 保持不编号；若使用 shields，头部按居中示例组织；安装、快速开始、用法等章节从 `1.` 开始连续编号。
- API 文档：独立文档按完整层级编号；作为其他文档中的片段时继承所在文档的编号，不擅自从 `1.` 重启。
- 教程：H2 步骤章节按文档顺序编号，H3/H4 继承父级编号。
- 变更日志：H2 版本章节与 H3 变更类别也使用层级编号；若用户要求严格遵循既有标准版式，则保留该标准格式。

## 8. 优先级与已有文档

规则优先级从高到低：

1. 用户当前明确要求。
2. 项目内已有且明确的文档规范或必须遵循的外部标准。
3. 已有文档中一致使用的格式。
4. 本设计定义的 `docs-writer` 默认格式。

修改已有文档时，只规范本次新增或改动的 shields 徽章和相关标题。若文档已有明确且一致的编号体系，沿用现有体系，不为套用默认规则重排无关章节。

## 9. 修改范围

- `skills/docs-writer/SKILL.md`
- `skills/docs-writer/references/style-guide.md`
- `skills/docs-writer/references/templates.md`

不新增 Skill，不修改 `README.md` 和 `llms.txt` 的数量或索引。

## 10. 验收标准

- 三个文件对默认规则、例外和已有文档策略表述一致。
- README 模板包含 `for-the-badge` 和居中头部示例。
- 所有模板的 H2/H3/H4 示例采用末尾带句点的完整层级编号。
- `SKILL.md` frontmatter、名称和目录名保持一致。
- 新增内容不包含未完成标记或占位说明。
- 本地 Markdown 链接可解析，代码围栏闭合。
- `git diff --check` 无空白错误。
