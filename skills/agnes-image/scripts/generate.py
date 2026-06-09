#!/usr/bin/env python3
"""Agnes Image 2.1 Flash 生图脚本（仅用标准库）。

文生图 / 图生图均走同一端点。请求体的几个易错点已在此封装：
- response_format 放在 extra_body 内（url / b64_json）
- 文生图 Base64 用顶层 return_base64
- 图生图通过 extra_body.image 传入（本地文件自动转 Data URI）
"""
import argparse
import base64
import json
import mimetypes
import os
import ssl
import sys
import urllib.request
import urllib.error

API_URL = "https://apihub.agnes-ai.com/v1/images/generations"
MODEL = "agnes-image-2.1-flash"
TIMEOUT = 360

# 跳过 SSL 证书校验（规避 macOS 自带 Python 缺少 CA 证书导致的
# CERTIFICATE_VERIFY_FAILED）。
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE


def to_image_ref(ref: str) -> str:
    """公网 URL 原样返回；本地文件读成 Data URI Base64。"""
    if ref.startswith("http://") or ref.startswith("https://") or ref.startswith("data:"):
        return ref
    if not os.path.isfile(ref):
        sys.exit(f"输入图不存在: {ref}")
    mime = mimetypes.guess_type(ref)[0] or "image/png"
    with open(ref, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{data}"


def build_body(args) -> dict:
    body = {"model": args.model, "prompt": args.prompt, "size": args.size}
    extra = {}
    if args.image:
        extra["image"] = [to_image_ref(x) for x in args.image]

    if args.raw_base64:
        if args.image:
            extra["response_format"] = "b64_json"
        else:
            body["return_base64"] = True
    else:
        extra["response_format"] = "url"

    if extra:
        body["extra_body"] = extra
    return body


def call_api(body: dict, api_key: str) -> dict:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CTX) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        sys.exit(f"请求失败 HTTP {e.code}: {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"网络错误: {e.reason}")


def save_result(item: dict, out: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    if item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=TIMEOUT, context=SSL_CTX) as resp:
            with open(out, "wb") as f:
                f.write(resp.read())
    elif item.get("b64_json"):
        with open(out, "wb") as f:
            f.write(base64.b64decode(item["b64_json"]))
    else:
        sys.exit(f"响应中无图片数据: {json.dumps(item)[:300]}")


def main() -> None:
    p = argparse.ArgumentParser(description="Agnes Image 2.1 Flash 生图")
    p.add_argument("--prompt", required=True, help="文本指令")
    p.add_argument("--size", default="1024x768", help="输出尺寸，如 1024x768")
    p.add_argument("--out", required=True, help="输出文件路径，如 out/x.png")
    p.add_argument("--image", action="append", help="图生图输入（URL 或本地文件，可重复）")
    p.add_argument("--model", default=MODEL)
    p.add_argument("--raw-base64", action="store_true", help="请求 Base64 输出而非 URL")
    args = p.parse_args()

    api_key = os.environ.get("AGNES_API_KEY")
    if not api_key:
        sys.exit("缺少环境变量 AGNES_API_KEY")

    resp = call_api(build_body(args), api_key)
    data = resp.get("data") or []
    if not data:
        sys.exit(f"响应无 data: {json.dumps(resp)[:300]}")
    save_result(data[0], args.out)
    print(f"已保存: {args.out}")


if __name__ == "__main__":
    main()
