# Agnes-Video-V2.0 API 参考

来源：[agnes-ai.com 文档](https://agnes-ai.com/doc/agnes-video-v20)。模型由 Sapiens AI 提供，支持文生视频、图生视频、多图视频与关键帧动画，**异步任务式**。

## 端点与鉴权

| 项 | 值 |
| --- | --- |
| 建任务 | `POST https://apihub.agnes-ai.com/v1/videos` |
| 取结果（推荐） | `GET https://apihub.agnes-ai.com/agnesapi?video_id=<VIDEO_ID>` |
| 取结果（兼容） | `GET https://apihub.agnes-ai.com/v1/videos/{task_id}` |
| 鉴权 | `Authorization: Bearer YOUR_API_KEY` |
| 模型名 | `agnes-video-v2.0` |
| 价格 | 标准 $0.005/秒（当前 $0/秒） |

取结果可附加 `&model_name=<MODEL>`；当使用上游原始 video id、非默认模型或需显式指定模型时使用，提供后该参数优先。

## 建任务参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | string | 是 | `agnes-video-v2.0` |
| `prompt` | string | 是 | 视频内容描述 |
| `image` | string/array | 否 | 图 URL（单图图生视频用） |
| `mode` | string | 否 | 如 `ti2vid`、`keyframes` |
| `height` | int | 否 | 默认 `768` |
| `width` | int | 否 | 默认 `1152` |
| `num_frames` | int | 否 | `≤ 441` 且满足 `8n+1` |
| `frame_rate` | number | 否 | `1–60` |
| `num_inference_steps` | int | 否 | 推理步数 |
| `seed` | int | 否 | 随机种子（可复现） |
| `negative_prompt` | string | 否 | 负向提示 |
| `extra_body.image` | array | 否 | 多图视频 / 关键帧的输入图 |
| `extra_body.mode` | string | 否 | 如 `keyframes` |

## 四种调用（建任务）

| 模式 | 图位置 | 额外 |
| --- | --- | --- |
| 文生视频 | 无 | 仅 `model`+`prompt`（+尺寸/帧） |
| 图生视频 | 顶层 `image`（字符串 URL） | — |
| 多图视频 | `extra_body.image`（数组） | — |
| 关键帧动画 | `extra_body.image`（数组） | `extra_body.mode: "keyframes"` |

```bash
# 文生视频
curl -X POST https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{ "model": "agnes-video-v2.0", "prompt": "A cinematic shot of a cat walking on the beach at sunset", "height": 768, "width": 1152, "num_frames": 121, "frame_rate": 24 }'

# 图生视频
-d '{ "model": "agnes-video-v2.0", "prompt": "The woman slowly turns around", "image": "https://example.com/image.png", "num_frames": 121, "frame_rate": 24 }'

# 多图视频
-d '{ "model": "agnes-video-v2.0", "prompt": "Smooth transformation between two references", "extra_body": { "image": ["https://example.com/1.png","https://example.com/2.png"] }, "num_frames": 121, "frame_rate": 24 }'

# 关键帧动画
-d '{ "model": "agnes-video-v2.0", "prompt": "Smooth transition between keyframes", "extra_body": { "image": ["https://example.com/k1.png","https://example.com/k2.png"], "mode": "keyframes" }, "num_frames": 121, "frame_rate": 24 }'
```

## 建任务响应

返回 `task_id` 与 `video_id`（新接入用 `video_id` 取结果）：

```json
{ "id": "task_xxx", "task_id": "task_xxx", "video_id": "video_xxx", "object": "video",
  "model": "agnes-video-v2.0", "status": "queued", "progress": 0, "created_at": 1780457477,
  "seconds": "10.0", "size": "1280x768" }
```

## 取结果响应

完成后最终视频地址在 **`remixed_from_video_id`**：

```json
{ "id": "task_xxx", "video_id": "video_xxx", "model": "agnes-video-v2.0", "object": "video",
  "status": "completed", "progress": 100, "seconds": "10.0", "size": "1280x768",
  "remixed_from_video_id": "https://storage.googleapis.com/agnes-aigc/.../video_xxx.mp4", "error": null }
```

## 任务状态

`queued`（排队）→ `in_progress`（生成中）→ `completed`（完成）/ `failed`（失败）。

## 时长控制

`seconds = num_frames / frame_rate`；`num_frames ≤ 441` 且满足 `8n+1`；`frame_rate` 1–60。

| 目标 | 参数 |
| --- | --- |
| ~3s | `num_frames 81`, `frame_rate 24` |
| ~5s | `num_frames 121`, `frame_rate 24` |
| ~10s | `num_frames 241`, `frame_rate 24` |
| ~18s | `num_frames 441`, `frame_rate 24` |

## 错误码

| 码 | 说明 |
| --- | --- |
| 400 | 请求无效，检查参数（尤其 `num_frames`） |
| 401 | 未授权，检查 API Key |
| 404 | 任务 / 视频不存在 |
| 500 | 服务端错误 |
| 503 | 服务繁忙，稍后重试 |
