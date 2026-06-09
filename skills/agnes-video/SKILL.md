---
name: agnes-video
description: 使用 Agnes-Video-V2.0（Sapiens AI）生成视频，支持文生视频、图生视频、多图视频与关键帧动画；异步任务式（先建任务再取结果）。当用户要求用 Agnes / agnes-video 生成视频、图片转视频、关键帧过渡、营销短片 / Reels 时使用。
---

# Agnes 生视频（agnes-video）

调用 Agnes-Video-V2.0 生成视频。该接口为**异步**：先 `POST` 建任务拿到 `video_id`，再轮询取结果，完成后视频地址在 `remixed_from_video_id`。优先执行 `scripts/generate.py`（已封装建任务、轮询、下载、帧数校验）。完整接口见 [references/api.md](references/api.md)。

## 前置

- 环境变量 `AGNES_API_KEY`（`Authorization: Bearer <key>`）；公开示例一律用 `YOUR_API_KEY`，**勿**写入真实 key。
- 图生视频 / 多图 / 关键帧的输入图必须是**公网可访问的 HTTPS URL**（无需登录/cookie）；不支持本地文件。

## 工作流程

1. 与用户确认：**prompt、时长（或 `num_frames`+`fps`）、分辨率、输出路径**；图生视频还需输入图 URL 与「动什么、保持什么」。
2. 选模式（脚本自动判断）：无图=文生视频；单图=图生视频；多图=多图视频；`--mode keyframes`=关键帧动画。
3. 生成（建任务→轮询→下载 mp4）：

```bash
# 文生视频（约 5 秒：num_frames 121 / fps 24）
python scripts/generate.py \
  --prompt "A cinematic shot of a cat walking on the beach at sunset, warm golden lighting, realistic motion" \
  --frames 121 --fps 24 --width 1152 --height 768 \
  --out out/cat.mp4

# 图生视频
python scripts/generate.py \
  --prompt "The woman slowly turns and looks back, natural expression, cinematic camera movement" \
  --image https://example.com/image.png \
  --out out/turn.mp4

# 关键帧动画（两张及以上）
python scripts/generate.py \
  --prompt "Smooth cinematic transition between the keyframes, consistent identity, natural motion" \
  --image https://example.com/k1.png --image https://example.com/k2.png \
  --mode keyframes \
  --out out/transition.mp4
```

4. 失败时按 [references/api.md](references/api.md) 「错误码」排查（401 查 key；400 查参数，尤其 `num_frames`；503 稍后重试）。

## 关键约束（务必遵守）

- 模型名固定 `agnes-video-v2.0`。
- **时长**：`seconds = num_frames / frame_rate`；`num_frames ≤ 441` 且须满足 **`8n+1`**（如 81 / 121 / 161 / 241 / 441）；`frame_rate` 取 `1–60`。
- **图位置**：单图图生视频用**顶层** `image`；多图与关键帧用 **`extra_body.image`**；关键帧再加 `extra_body.mode: "keyframes"`。
- 文生视频仅需 `model`、`prompt`。
- 取结果优先用 `video_id`（端点 `GET /agnesapi?video_id=...`），完成后地址字段为 `remixed_from_video_id`。

## 常用时长

| 目标时长 | 参数 |
| --- | --- |
| ~3s | `num_frames 81`, `fps 24` |
| ~5s | `num_frames 121`, `fps 24` |
| ~10s | `num_frames 241`, `fps 24` |
| ~18s | `num_frames 441`, `fps 24` |

## prompt 结构

文生视频：`[主体] + [动作] + [场景] + [运镜] + [光照] + [风格]`。
图/多图/关键帧：说明「动什么、保持什么」「起始→目标如何过渡」。

## 脚本

**scripts/generate.py**：建任务 + 轮询 + 下载，零第三方依赖（标准库）。读取 `AGNES_API_KEY`；`--out` 为 `.mp4` 本地路径；可选 `--seed`、`--negative`、`--poll-interval`、`--timeout`。帧数不合法会直接报错并提示就近的合法值。
