#!/usr/bin/env python3
"""Validate objective structure rules for an ai-novel-writer project."""

import argparse
import re
from pathlib import Path


NEW_FILES = (
    "00_作品定位.md",
    "01_角色设定.md",
    "02_故事总纲.md",
    "03_章节规划.md",
    "04_创作进度.md",
    "05_追读账本.md",
)
LEGACY_FILES = (
    "00_作品设定.md",
    "01_角色设定.md",
    "02_故事总纲.md",
    "03_分集大纲.md",
    "04_创作进度.md",
)
PRODUCTION_PATTERNS = (
    re.compile(r"镜头\s*\d+"),
    re.compile(r"(?:图像|图片|视频|画面)提示词"),
    re.compile(r"制作(?:说明|指令)"),
)
PLACEHOLDER_PATTERN = re.compile(r"\b(?:TODO|TBD)\b|待填写", re.IGNORECASE)
EMPTY_FIELD_PATTERN = re.compile(r"^\s*-\s*[^：:\n]+[：:]\s*$", re.MULTILINE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def body_char_count(text: str) -> int:
    without_headings = re.sub(r"(?m)^\s*#+.*$", "", text)
    return len(re.sub(r"\s", "", without_headings))


def check_sequence(paths: list[Path], pattern: re.Pattern[str], label: str) -> list[str]:
    numbers = sorted(
        int(match.group(1))
        for path in paths
        if (match := pattern.search(path.name))
    )
    if not numbers:
        return []
    expected = list(range(1, numbers[-1] + 1))
    if numbers != expected:
        return [f"{label}编号不连续：实际 {numbers}，应为 {expected}"]
    return []


def validate_project(
    project: Path,
    min_chars: int = 0,
    max_chars: int | None = None,
    *,
    legacy: bool = False,
) -> list[str]:
    errors: list[str] = []
    if not project.is_dir():
        return [f"作品目录不存在：{project}"]

    required_files = LEGACY_FILES if legacy else NEW_FILES
    for name in required_files:
        path = project / name
        if not path.is_file():
            errors.append(f"缺少基础资料文件：{name}")
        elif body_char_count(read_text(path)) == 0:
            errors.append(f"基础资料文件没有有效内容：{name}")

    chapters_dir = project / "正文"
    adaptation_dir = project / "漫剧改编"
    if not chapters_dir.is_dir():
        errors.append("缺少正文目录")
        chapter_files: list[Path] = []
    else:
        chapter_files = sorted(chapters_dir.glob("第*章_*.md"))
        if not chapter_files:
            errors.append("正文目录中没有章节文件")

    if not adaptation_dir.is_dir():
        errors.append("缺少漫剧改编目录")
        adaptation_files: list[Path] = []
    else:
        adaptation_files = sorted(adaptation_dir.glob("第*集_*.md"))
        if chapter_files and not adaptation_files:
            errors.append("已有正文但没有漫剧改编资料")

    errors.extend(check_sequence(chapter_files, re.compile(r"第(\d+)章"), "章节"))
    errors.extend(check_sequence(adaptation_files, re.compile(r"第(\d+)集"), "改编资料"))

    for path in chapter_files:
        text = read_text(path)
        count = body_char_count(text)
        if count < min_chars:
            errors.append(f"{path.name} 正文 {count} 字，少于下限 {min_chars} 字")
        if max_chars is not None and count > max_chars:
            errors.append(f"{path.name} 正文 {count} 字，超过上限 {max_chars} 字")
        if any(pattern.search(text) for pattern in PRODUCTION_PATTERNS):
            errors.append(f"{path.name} 混入镜头、提示词或制作指令")

    material_files = [project / name for name in required_files]
    material_files.extend(adaptation_files)
    for path in material_files:
        if not path.is_file():
            continue
        text = read_text(path)
        if PLACEHOLDER_PATTERN.search(text):
            errors.append(f"{path.name} 残留 TODO、TBD 或待填写占位")
        if EMPTY_FIELD_PATTERN.search(text):
            errors.append(f"{path.name} 存在空白列表字段")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="作品目录")
    parser.add_argument("--min-chars", type=int, default=0, help="单章正文最少非空白字符数")
    parser.add_argument("--max-chars", type=int, help="单章正文最多非空白字符数")
    parser.add_argument("--legacy", action="store_true", help="按旧版五文件结构验证")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_project(
        args.project,
        args.min_chars,
        args.max_chars,
        legacy=args.legacy,
    )
    if errors:
        print("验证失败：")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"验证通过：{args.project}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
