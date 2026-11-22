#!/usr/bin/env python3
"""检查 Seedance 评估输出的确定性约束；创作质量另行人工评审。"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


EVALS_PATH = Path(__file__).resolve().parents[1] / "evals" / "evals.json"
REFERENCE_PATTERN = re.compile(r"@(图片|视频|音频|image|video|audio)\s*(\d+)(?![0-9A-Za-z_])", re.IGNORECASE)
REFERENCE_KINDS = {"图片": "image", "视频": "video", "音频": "audio"}


def normalized_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def extract_prompt_blocks(text: str) -> list[str]:
    """读取顶层 text 或无语言围栏，避免把 Python/JSON 代码算成提示词。"""
    blocks: list[str] = []
    marker = None
    lines: list[str] = []
    accept = False
    for line in normalized_text(text).splitlines():
        if marker is None:
            match = re.fullmatch(r" {0,3}(`{3,}|~{3,})([^\n]*)", line)
            if match:
                marker = match.group(1)
                accept = match.group(2).strip().lower() in {"", "text"}
                lines = []
        elif re.fullmatch(r" {0,3}" + re.escape(marker[0]) + "{" + str(len(marker)) + r",}\s*", line):
            if accept:
                blocks.append(normalized_text("\n".join(lines)))
            marker = None
        else:
            lines.append(line)
    return blocks


def reference_ids(text: str) -> set[str]:
    return {
        REFERENCE_KINDS.get(kind.lower(), kind.lower()) + str(int(number))
        for kind, number in REFERENCE_PATTERN.findall(text)
    }


def load_case(name: str, path: Path = EVALS_PATH) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    matches = [case for case in data["evals"] if case["name"] == name]
    if len(matches) != 1:
        raise ValueError(f"评估名称不存在或不唯一：{name}")
    return matches[0]


def grade_output(content: str, eval_name: str) -> dict:
    case = load_case(eval_name)
    rules = case["deterministic"]
    text = normalized_text(content)
    blocks = extract_prompt_blocks(text)
    checks: list[dict] = []

    def check(label: str, passed: bool, evidence: str) -> None:
        checks.append({"text": label, "passed": passed, "evidence": evidence})

    check("输出非空", bool(text), f"全文 {len(text)} 字符")
    minimum = rules.get("min_prompt_blocks", 1)
    maximum = rules.get("max_prompt_blocks")
    valid_count = len(blocks) >= minimum and (maximum is None or len(blocks) <= maximum)
    check("提示词块数量符合任务", valid_count, f"{len(blocks)} 块；最少 {minimum}，最多 {maximum if maximum is not None else '不限定'}")

    limit = rules.get("max_prompt_chars", 2000)
    for index, block in enumerate(blocks, 1):
        check(f"提示词块 {index} 非空且未超预算", bool(block) and len(block) <= limit, f"{len(block)}/{limit} 字符")

    if "max_output_chars" in rules:
        output_limit = rules["max_output_chars"]
        check("全文未超预算", len(text) <= output_limit, f"{len(text)}/{output_limit} 字符，包含说明与围栏")

    for required in rules.get("required_prompt_text", []):
        check(f"提示词保留原文：{required}", any(required in block for block in blocks), "仅检查生成提示词，不以外部说明代替")

    allowed = set().union(*(reference_ids(label) for label in rules.get("allowed_references", [])))
    used = set().union(*(reference_ids(block) for block in blocks))
    unexpected = sorted(used - allowed)
    check("提示词无未声明素材引用", not unexpected, f"未声明：{unexpected}" if unexpected else f"引用：{sorted(used)}")

    passed = sum(item["passed"] for item in checks)
    return {
        "eval": eval_name,
        "automatic_checks_only": True,
        "expectations": checks,
        "passed_count": passed,
        "total_count": len(checks),
        "pass_rate": passed / len(checks),
        "prompt_char_counts": [len(block) for block in blocks],
        "manual_review_required": case["criteria"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="待评估的 Markdown 输出；只读，不自动写报告")
    parser.add_argument("--eval", required=True, help="evals.json 中的 name")
    args = parser.parse_args()
    try:
        result = grade_output(args.output.read_text(encoding="utf-8"), args.eval)
    except (OSError, UnicodeError, ValueError, KeyError) as exc:
        parser.exit(2, f"评估失败：{exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed_count"] == result["total_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
