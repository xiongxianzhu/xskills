#!/usr/bin/env python3
"""Agnes-Video-V2.0 生视频脚本（仅用标准库）。

异步流程：POST 建任务 -> 轮询 video_id -> status=completed 后下载 mp4。
已封装的易错点：
- num_frames 必须 <= 441 且满足 8n+1
- 单图=顶层 image；多图/关键帧=extra_body.image；关键帧加 extra_body.mode
- 取结果用 GET /agnesapi?video_id=...，完成后视频地址在 remixed_from_video_id
"""
import argparse
import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

CREATE_URL = "https://apihub.agnes-ai.com/v1/videos"
RESULT_URL = "https://apihub.agnes-ai.com/agnesapi"
MODEL = "agnes-video-v2.0"

# 跳过 SSL 证书校验。
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE


def validate_frames(n: int) -> None:
    if n > 441:
        sys.exit(f"num_frames 必须 <= 441，当前 {n}")
    if n % 8 != 1:
        lower = (n - 1) // 8 * 8 + 1
        upper = lower + 8
        sys.exit(f"num_frames 必须满足 8n+1，当前 {n}；就近合法值：{lower} 或 {upper}")


def check_urls(images) -> None:
    for u in images:
        if not (u.startswith("http://") or u.startswith("https://")):
            sys.exit(f"输入图必须为公网 URL（不支持本地文件 / Data URI）：{u}")


def build_body(args) -> dict:
    body = {
        "model": args.model,
        "prompt": args.prompt,
        "width": args.width,
        "height": args.height,
        "num_frames": args.frames,
        "frame_rate": args.fps,
    }
    if args.seed is not None:
        body["seed"] = args.seed
    if args.negative:
        body["negative_prompt"] = args.negative

    images = args.image or []
    check_urls(images)
    if args.mode == "keyframes" or len(images) > 1:
        if not images:
            sys.exit("关键帧 / 多图模式需要至少一张 --image")
        extra = {"image": images}
        if args.mode == "keyframes":
            extra["mode"] = "keyframes"
        body["extra_body"] = extra
    elif len(images) == 1:
        body["image"] = images[0]
    return body


def http_json(url: str, api_key: str, data=None) -> dict:
    headers = {"Authorization": f"Bearer {api_key}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers,
                                 method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        sys.exit(f"请求失败 HTTP {e.code}: {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"网络错误: {e.reason}")


def poll(video_id: str, model: str, api_key: str, interval: int, timeout: int) -> str:
    query = urllib.parse.urlencode({"video_id": video_id, "model_name": model})
    url = f"{RESULT_URL}?{query}"
    deadline = time.time() + timeout
    while time.time() < deadline:
        res = http_json(url, api_key)
        status = res.get("status")
        progress = res.get("progress", 0)
        if status == "completed":
            video_url = res.get("remixed_from_video_id")
            if not video_url:
                sys.exit(f"已完成但无视频地址: {json.dumps(res)[:300]}")
            return video_url
        if status == "failed":
            sys.exit(f"生成失败: {json.dumps(res.get('error'))}")
        print(f"  状态 {status} 进度 {progress}% ...")
        time.sleep(interval)
    sys.exit(f"轮询超时（{timeout}s），video_id={video_id}")


def main() -> None:
    p = argparse.ArgumentParser(description="Agnes-Video-V2.0 生视频")
    p.add_argument("--prompt", required=True, help="视频内容描述")
    p.add_argument("--out", required=True, help="输出 mp4 路径，如 out/x.mp4")
    p.add_argument("--image", action="append", help="输入图公网 URL（可重复）")
    p.add_argument("--mode", choices=["keyframes"], help="关键帧动画模式")
    p.add_argument("--width", type=int, default=1152)
    p.add_argument("--height", type=int, default=768)
    p.add_argument("--frames", type=int, default=121, help="num_frames，<=441 且 8n+1")
    p.add_argument("--fps", type=int, default=24, help="frame_rate，1-60")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--negative", help="negative_prompt")
    p.add_argument("--model", default=MODEL)
    p.add_argument("--poll-interval", type=int, default=5)
    p.add_argument("--timeout", type=int, default=600)
    args = p.parse_args()

    validate_frames(args.frames)
    if not (1 <= args.fps <= 60):
        sys.exit("frame_rate 必须在 1-60")

    api_key = os.environ.get("AGNES_API_KEY")
    if not api_key:
        sys.exit("缺少环境变量 AGNES_API_KEY")

    created = http_json(CREATE_URL, api_key, data=build_body(args))
    video_id = created.get("video_id")
    if not video_id:
        sys.exit(f"建任务未返回 video_id: {json.dumps(created)[:300]}")
    print(f"任务已创建 video_id={video_id}，开始轮询...")

    video_url = poll(video_id, args.model, api_key, args.poll_interval, args.timeout)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with urllib.request.urlopen(video_url, timeout=120, context=SSL_CTX) as resp:
        with open(args.out, "wb") as f:
            f.write(resp.read())
    print(f"已保存: {args.out}")


if __name__ == "__main__":
    main()
