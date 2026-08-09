#!/usr/bin/env python3
"""Report high-confidence structural repetition in a novel project."""

import argparse
import re
from pathlib import Path


REQUIRED_SECTIONS = {
    "00_作品定位.md": "## 叙事声纹",
    "03_章节规划.md": "## 章节结构指纹",
    "04_创作进度.md": "## 最近五章节奏轨迹",
}
CHAPTER_NUMBER_PATTERN = re.compile(r"第(\d+)章")
SYSTEM_END_PATTERN = re.compile(
    r"系统(?:提示|通知|结算|奖励|任务)|"
    r"任务(?:完成|结算)|奖励(?:到账|发放)|状态(?:更新|刷新)"
)
MIN_REPEATED_CHARS = 24


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def chapter_number(path: Path) -> int:
    match = CHAPTER_NUMBER_PATTERN.search(path.name)
    return int(match.group(1)) if match else 0


def normalized_paragraphs(text: str) -> list[str]:
    paragraphs = []
    for paragraph in re.split(r"\n\s*\n", text):
        stripped = paragraph.strip()
        if not stripped or stripped.startswith("#"):
            continue
        normalized = re.sub(r"\s+", "", stripped)
        if len(normalized) >= MIN_REPEATED_CHARS:
            paragraphs.append(normalized)
    return paragraphs


def boundary_paragraphs(path: Path) -> tuple[set[str], set[str]]:
    paragraphs = normalized_paragraphs(read_text(path))
    return set(paragraphs[:3]), set(paragraphs[-3:])


def audit_project(project: Path, *, legacy: bool = False) -> list[str]:
    warnings: list[str] = []
    if not project.is_dir():
        return [f"作品目录不存在：{project}"]

    if not legacy:
        for filename, heading in REQUIRED_SECTIONS.items():
            path = project / filename
            if path.is_file() and heading not in read_text(path):
                warnings.append(f"{filename} 缺少栏目：{heading.removeprefix('## ')}")

    chapters_dir = project / "正文"
    if not chapters_dir.is_dir():
        return warnings

    chapters = sorted(chapters_dir.glob("第*章_*.md"), key=chapter_number)
    system_endings = []
    for path in chapters:
        compact = re.sub(r"\s+", "", read_text(path))
        system_endings.append(bool(SYSTEM_END_PATTERN.search(compact[-600:])))

    for index in range(len(chapters) - 2):
        if all(system_endings[index : index + 3]):
            names = "、".join(path.name for path in chapters[index : index + 3])
            warnings.append(f"连续三章在结尾使用系统结算或状态更新：{names}")

    for first, second in zip(chapters, chapters[1:]):
        first_opening, first_ending = boundary_paragraphs(first)
        second_opening, second_ending = boundary_paragraphs(second)
        if first_opening & second_opening:
            warnings.append(f"相邻章节存在较长的完全重复开头：{first.name}、{second.name}")
        if first_ending & second_ending:
            warnings.append(f"相邻章节存在较长的完全重复结尾：{first.name}、{second.name}")

    return warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="作品目录")
    parser.add_argument("--legacy", action="store_true", help="跳过新项目栏目检查")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    warnings = audit_project(args.project, legacy=args.legacy)
    if not warnings:
        print(f"未发现高置信度叙事模式警告：{args.project}")
        return 0

    print("叙事模式警告：")
    for warning in warnings:
        print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
