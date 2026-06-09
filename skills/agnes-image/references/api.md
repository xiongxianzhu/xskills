# Agnes Image 2.1 Flash API 参考

来源：[agnes-ai.com 文档](https://agnes-ai.com/doc/agnes-image-21-flash)。模型由 Sapiens AI 提供，支持文生图与图生图，针对高信息密度图像做了优化。

## 端点与鉴权

| 项 | 值 |
| --- | --- |
| Base URL | `https://apihub.agnes-ai.com` |
| Endpoint | `POST https://apihub.agnes-ai.com/v1/images/generations` |
| Content-Type | `application/json` |
| 鉴权 | `Authorization: Bearer YOUR_API_KEY` |
| 模型名 | `agnes-image-2.1-flash` |
| 价格 | 约 $0.003 / 张 |
| 建议超时 | 60s–360s |

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | string | 是 | `agnes-image-2.1-flash` |
| `prompt` | string | 是 | 生成 / 编辑指令 |
| `size` | string | 是 | 输出尺寸，如 `1024x768` |
| `image` | string[] | 图生图必填 | 输入图：公网 URL 或 Data URI Base64 |
| `return_base64` | boolean | 否 | **文生图** Base64 输出（顶层） |
| `extra_body` | object | 否 | 高级参数容器 |
| `extra_body.response_format` | string | 否 | `url` 或 `b64_json` |

## 输出位置

- URL 输出：`data[0].url`
- Base64 输出：`data[0].b64_json`

## 四种调用

### 1. 文生图 → URL

```bash
curl https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "A luminous floating city above a misty canyon at sunrise, cinematic realism",
    "size": "1024x768",
    "extra_body": { "response_format": "url" }
  }'
```

### 2. 文生图 → Base64（顶层 `return_base64`）

```bash
-d '{
  "model": "agnes-image-2.1-flash",
  "prompt": "A clean product photo of a glass cube on a white studio background",
  "size": "1024x768",
  "return_base64": true
}'
```

### 3. 图生图（URL 输入 → URL 输出）

```bash
-d '{
  "model": "agnes-image-2.1-flash",
  "prompt": "Transform into a rain-soaked cyberpunk night, preserve the original composition",
  "size": "1024x768",
  "extra_body": {
    "image": ["https://example.com/input-image.png"],
    "response_format": "url"
  }
}'
```

### 4. 图生图（Data URI Base64 输入）

```text
data:image/png;base64,BASE64_HERE
```

```bash
-d '{
  "model": "agnes-image-2.1-flash",
  "prompt": "Make the object matte black while preserving the original composition",
  "size": "1024x768",
  "extra_body": {
    "image": ["data:image/png;base64,BASE64_HERE"],
    "response_format": "b64_json"
  }
}'
```

## 响应示例

URL 输出：

```json
{ "created": 1780000000, "data": [ { "url": "https://storage.googleapis.com/agnes-aigc/xxx.png", "b64_json": null, "revised_prompt": null } ] }
```

Base64 输出：

```json
{ "created": 1780000000, "data": [ { "url": null, "b64_json": "iVBORw0KGgoAAA...", "revised_prompt": null } ] }
```

## 常见错误

1. **`response_format` 放在顶层** → 报错。必须放 `extra_body` 内。
2. **图生图传了 `tags: ["img2img"]`** → 不需要，删除；只在 `image` 数组给输入图。
3. **输入图 URL 不可访问** → 用公网 HTTPS、无需登录/cookie 的图；否则改用 Data URI Base64。
4. **请求超时** → 提高客户端超时到 60s–360s。
5. **图生图缺 `image`** → 图生图必须提供 `image` 数组。

> 文档存在一处措辞不一致：「Important Notes」称 `image` 放在**顶层**数组，但所有 curl 示例把 `image` 放在 `extra_body` 内。本技能脚本按**示例**实现（`extra_body.image`）。若服务端行为变化导致图生图失败，可尝试改为顶层 `image`。
