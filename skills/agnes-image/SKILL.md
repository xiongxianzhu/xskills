---
name: agnes-image
description: 使用 Agnes Image 2.1 Flash（Sapiens AI）生成或编辑图片，支持文生图与图生图、URL/Base64 输出、自定义尺寸。当用户要求用 Agnes / agnes-image 生图、出海报封面、产品图、图生图改图、风格迁移时使用。
---

# Agnes 生图（agnes-image）

调用 Agnes Image 2.1 Flash 完成**文生图**与**图生图**。优先执行 `scripts/generate.py`，避免手写易错的请求体。完整接口细节见 [references/api.md](references/api.md)。

## 前置

- 环境变量 `AGNES_API_KEY`（请求头 `Authorization: Bearer <key>`）；**切勿**把真实 key 写进代码或文档，公开示例一律用 `YOUR_API_KEY`。
- 生图耗时数秒到数十秒，客户端超时建议 60s–360s。

## 工作流程

1. 与用户确认：**prompt、尺寸（如 `1024x768`）、输出路径**；图生图还需**输入图**（公网 HTTPS URL 或本地文件）与「保留/改变」要求。
2. 按 [推荐 prompt 结构](#prompt-结构) 组织描述。
3. 调脚本生成（默认文生图、URL 输出后自动下载到本地）：

```bash
# 文生图
python scripts/generate.py \
  --prompt "A luminous floating city above a misty canyon at sunrise, cinematic realism, wide-angle, high visual density" \
  --size 1024x768 \
  --out out/city.png

# 图生图（输入可为公网 URL 或本地文件，本地文件自动转 Data URI）
python scripts/generate.py \
  --prompt "Transform into a rain-soaked cyberpunk night with neon reflections, preserve the original composition" \
  --size 1024x768 \
  --image https://example.com/input.png \
  --out out/cyberpunk.png
```

4. 失败时按 [references/api.md](references/api.md) 的「常见错误」排查（最常见：`response_format` 放错层级、img2img 缺 `image`、输入图不可公网访问）。

## 关键约束（务必遵守）

- 模型名固定 `agnes-image-2.1-flash`。
- `response_format`（`url` / `b64_json`）必须放在 **`extra_body`** 内，**不可**放顶层。
- 文生图要 Base64：用**顶层** `return_base64: true`。
- 图生图：在 `image` 数组传输入图；**不要**传 `tags: ["img2img"]`。
- 文生图必填 `model`、`prompt`、`size`。

## prompt 结构

```text
[主体] + [场景/环境] + [风格] + [光照] + [构图] + [质量要求]
```

图生图改用：`[改变要求] + [新风格/场景] + [增删元素] + [需保留的元素]`，明确「改什么、保留什么」。

## 脚本

**scripts/generate.py**：封装请求体与输出处理。零第三方依赖（标准库）。

```bash
python scripts/generate.py --prompt "..." --size 1024x768 --out out/x.png   # 文生图→下载
python scripts/generate.py --prompt "..." --image in.png --out out/y.png    # 图生图
python scripts/generate.py --prompt "..." --out out/z.png --raw-base64      # 强制 Base64 输出
```

- 读取 `AGNES_API_KEY`；`--out` 为 `.png` 等本地路径。
- URL 输出会自动下载保存；Base64 输出会解码保存。
