# 文档模板（templates）

四类高频文档的**最小结构**：必须出现的章节 + 顺序。按需增删，不要机械套用。所有结构遵循 [SKILL.md 的五原则](../SKILL.md)。

## README

项目入口。目标：30 秒内让读者判断"要不要用"，2 分钟内跑通第一个示例。

```markdown
<div align="center">

# 项目名

[一句话价值主张：解决什么问题，不是堆功能]

[根据仓库事实生成 2–4 枚 Shields.io 徽章，所有 URL 使用 style=for-the-badge]

</div>

## 安装

[最少步骤，通常 1–3 行命令]

## 快速开始

[最简可运行示例 + 预期输出]

## 用法

[常见场景，每场景一个小节或表格]

## 故障排查

[高频错误 + 解决方案]

## 许可

[License 类型]
```

**省略建议**：内部项目可省"许可"；无配置项则不写"配置"；贡献指南可链接到独立 `CONTRIBUTING.md`。

### 完整示例

````markdown
<div align="center">

# filesort

按文件大小排序与导出，支持过滤与递归扫描。

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white&style=for-the-badge)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](./LICENSE)

</div>

## 安装

```bash
pip install filesort
```

## 快速开始

```bash
filesort .
```

输出：

```
1.2 GB    video.mp4
856 MB    dataset.zip
45 MB     photo.jpg
```

## 用法

| 选项 | 说明 |
| --- | --- |
| `-r, --reverse` | 大文件在前 |
| `-n, --number N` | 仅显示前 N 个 |
| `-e, --extension EXT` | 按扩展名过滤 |
| `-o, --output FILE` | 导出 CSV |

找出最大的 10 个视频文件：

```bash
filesort ~/Videos --extension mp4 --reverse --number 10
```

## 故障排查

### "Permission denied"

```bash
sudo filesort /var/log
```

### 无结果

检查过滤是否过严：去掉 `--extension` 再试。

## 许可

MIT
````

## API 文档

接口契约。目标：调用者只读这一段就能正确调用、处理错误。

```markdown
## 函数/端点名

[一句话：做什么]

### 参数

| 名称 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| param1 | string | 是 | 用途 |

### 返回

[返回值与格式]

### 示例

[完整可运行调用 + 预期输出]

### 错误

| 码 | 含义 | 处理 |
| --- | --- | --- |
```

**要点**：参数表四列固定（名称/类型/必填/说明）；示例必须可运行；错误码表覆盖常见失败。

## 教程

手把手。目标：读者跟着做完，得到一个可运行的成果。

```markdown
# [你将构建什么]

[成果预告 + 截图或演示输出]

## 前置条件

- [所需知识]
- [所需软件/版本]

## 步骤 1：[动作]

[指令 + 代码 + 预期结果]

## 步骤 2：[动作]

[继续]

## 下一步

[延伸阅读或进阶任务]
```

**要点**：每步配代码与预期输出；前置条件写明版本；编号连续不断层。

## 变更日志

版本差异。目标：升级者快速判断影响范围与是否需要动作。

```markdown
# 变更日志

## [版本号] - 日期

### Added
- 新增功能（链接到 PR/Issue）

### Changed
- 变更点（含破坏性标注 `!`）

### Fixed
- 修复的问题（链接到 Issue）
```

**分组顺序**（[Keep a Changelog](https://keepachangelog.com/) 约定）：Added / Changed / Deprecated / Removed / Fixed / Security。

**要点**：破坏性变更必须显式标注（`!` 或 `BREAKING`）；每条尽量链接到可追溯的 PR 或 Issue。
