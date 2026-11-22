# AI 漫剧技能（ai-drama）

存放 AI 漫剧 / 漫剧短视频全链路的 Agent Skills，覆盖从选题立项到成片发布的完整工作流。

## 工作流概览

```
选题 → 集纲 → 剧本 → 角色资产 → 分镜 → 逐镜提示词 → 配音配乐 → 剪辑成片
                          ↘ 角色设定（贯穿全流程）
```

四类技能协同：**全流程制片** 串起各环节并给出排产与验收门槛，**剧本与文案** 产出故事底稿，**分镜与提示词** 把底稿拆成可生成的镜头，**角色设定** 提供人物视觉基础。

## 目录约定

每个技能仍遵循仓库根 [AGENTS.md](../../AGENTS.md) 的 Skill 约定：

```
skills/ai-drama/<技能名>/SKILL.md
skills/ai-drama/<技能名>/references/...
skills/ai-drama/<技能名>/scripts/...
```

`npx skills` 支持 catalog 布局（`skills/<category>/<name>/SKILL.md`），安装命令不变：

```bash
npx skills add xiongxianzhu/xskills --list
npx skills add xiongxianzhu/xskills --skill <技能名> -g -y
```

## 技能索引

### 全流程制片

| 技能 | 说明 |
| --- | --- |
| [`ai-drama-production`](./ai-drama-production/SKILL.md) | AI 漫剧从选题到成片的全流程：选题钩子、集纲、声画对位、角色一致性、分镜、即梦 / Seedance 提示词、配音配乐与剪辑发布；支持 16:9 / 9:16，未指定时默认 16:9 |

### 剧本与文案

| 技能 | 说明 |
| --- | --- |
| [`ai-novel-writer`](./ai-novel-writer/SKILL.md) | 根据动态趋势选题并创作、续写和诊断追读优先的网文，支持多平台书名同名检测、叙事反模式控制与漫剧固定视觉资产管理 |
| [`novel-to-script`](./novel-to-script/SKILL.md) | 把小说文本改编为视频分镜脚本，含角色卡、场景拆分、画面提示词、声音标注 |
| [`manju-short-video-polish`](./manju-short-video-polish/SKILL.md) | 将小说原文润色为漫剧短视频文案（第一人称、黄金钩子、高完播） |

### 分镜与提示词

| 技能 | 说明 |
| --- | --- |
| [`industrial-storyboard`](./industrial-storyboard/SKILL.md) | 故事脚本 → 工业级电影分镜（机位/景别/运镜/光影/音效），可直接喂 AI 视频模型 |
| [`director-storyboard-sheet`](./director-storyboard-sheet/SKILL.md) | 分镜脚本 → 电影级导演故事板（Storyboard Sheet）完整提示词 |
| [`seedance-storyboard`](./seedance-storyboard/SKILL.md) | Seedance 2.0+ 导演分镜：剧情 / 角色 PV / 动作 / 广告，素材绑定、时间预算、跨镜连续性、独立分段提示词与局部视频编辑，按实际版本适配 |
| [`jimeng-split-prompts`](./jimeng-split-prompts/SKILL.md) | 把分镜脚本拆成即梦可生成的短视频提示词（每段 ≤15 秒 ≤2000 字） |

### 角色设定（提示词）

| 技能 | 说明 |
| --- | --- |
| [`guofeng-beauty-portrait`](./guofeng-beauty-portrait/SKILL.md) | 国漫 CG 美女头像提示词，1:1 |
| [`guofeng-beauty-halfbody`](./guofeng-beauty-halfbody/SKILL.md) | 国漫 CG 美女上半身提示词，9:16 |
| [`guofeng-beauty-turnaround`](./guofeng-beauty-turnaround/SKILL.md) | 古风美女四视图设定板提示词，16:9，8+ 种古风风格 |
| [`guofeng-handsome-male-turnaround`](./guofeng-handsome-male-turnaround/SKILL.md) | 古风帅气男主四视图设定板提示词，16:9 |
| [`guofeng-character-3d-sheet`](./guofeng-character-3d-sheet/SKILL.md) | 超写实 3D 国漫 CG 角色四视图设定板提示词 |
| [`character-turnaround-sheet`](./character-turnaround-sheet/SKILL.md) | 通用人类与类人角色三视图提示词，支持文字、角色卡与参考图特征锁定 |
| [`chibi-character-redraw`](./chibi-character-redraw/SKILL.md) | 任意参考角色 → Q 版轻写实（3 头身、白底、收藏级手办）重绘提示词，严格锁定原角色识别度 |
| [`character-design-board`](./character-design-board/SKILL.md) | 横版角色设定板（黑金版式 + 主肖像 + 三视图 + 多细节栏目，16:9 收藏级设定稿） |
