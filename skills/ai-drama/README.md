# AI 漫剧技能（ai-drama）

存放 AI 漫剧 / 漫剧短视频全链路的 Agent Skills，覆盖从小说原作到最终视频提示词的完整工作流。

## 工作流概览

```
小说原作 → 漫剧文案 → 分镜脚本 → 视频提示词
            ↘ 角色设定（贯穿全流程）
```

三类技能协同：**剧本与文案** 产出故事底稿，**分镜与提示词** 把底稿拆成可生成的镜头，**角色设定** 提供人物视觉基础。

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

### 剧本与文案

| 技能 | 说明 |
| --- | --- |
| [`ai-novel-writer`](./ai-novel-writer/SKILL.md) | 创作、续写、诊断和修改追读优先的番茄/红果式男女频网文，并生成独立漫剧交接资料 |
| [`novel-to-script`](./novel-to-script/SKILL.md) | 把小说文本改编为视频分镜脚本，含角色卡、场景拆分、画面提示词、声音标注 |
| [`manju-short-video-polish`](./manju-short-video-polish/SKILL.md) | 将小说原文润色为漫剧短视频文案（第一人称、黄金钩子、高完播） |

### 分镜与提示词

| 技能 | 说明 |
| --- | --- |
| [`industrial-storyboard`](./industrial-storyboard/SKILL.md) | 故事脚本 → 工业级电影分镜（机位/景别/运镜/光影/音效），可直接喂 AI 视频模型 |
| [`director-storyboard-sheet`](./director-storyboard-sheet/SKILL.md) | 分镜脚本 → 电影级导演故事板（Storyboard Sheet）完整提示词 |
| [`seedance-storyboard`](./seedance-storyboard/SKILL.md) | Seedance 2.0 / 即梦 / 小云雀沉浸式短片分镜，4–15 秒、横竖屏、≤2000 字中文提示词 |
| [`jimeng-split-prompts`](./jimeng-split-prompts/SKILL.md) | 把分镜脚本拆成即梦可生成的短视频提示词（每段 ≤15 秒 ≤2000 字） |

### 角色设定（提示词）

| 技能 | 说明 |
| --- | --- |
| [`guofeng-beauty-portrait`](./guofeng-beauty-portrait/SKILL.md) | 国漫 CG 美女头像提示词，1:1 |
| [`guofeng-beauty-halfbody`](./guofeng-beauty-halfbody/SKILL.md) | 国漫 CG 美女上半身提示词，9:16 |
| [`guofeng-beauty-turnaround`](./guofeng-beauty-turnaround/SKILL.md) | 古风美女四视图设定板提示词，16:9，8+ 种古风风格 |
| [`guofeng-handsome-male-turnaround`](./guofeng-handsome-male-turnaround/SKILL.md) | 古风帅气男主四视图设定板提示词，16:9 |
| [`guofeng-character-3d-sheet`](./guofeng-character-3d-sheet/SKILL.md) | 超写实 3D 国漫 CG 角色四视图设定板提示词 |
| [`chibi-character-redraw`](./chibi-character-redraw/SKILL.md) | 任意参考角色 → Q 版轻写实（3 头身、白底、收藏级手办）重绘提示词，严格锁定原角色识别度 |
| [`character-design-board`](./character-design-board/SKILL.md) | 横版角色设定板（黑金版式 + 主肖像 + 三视图 + 多细节栏目，16:9 收藏级设定稿） |
