#!/usr/bin/env python3
"""校验仓库内所有 Agent Skill 的结构、frontmatter 和 Markdown 链接。"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|\Z)", re.DOTALL)
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data"}


@dataclass(frozen=True, order=True)
class ValidationError:
    path: str
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: [{self.code}] {self.message}"


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path, root: Path, errors: list[ValidationError]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(
            ValidationError(_display_path(path, root), "FILE_READ", f"无法按 UTF-8 读取：{exc}")
        )
        return None


def _parse_frontmatter(
    path: Path, text: str, root: Path, errors: list[ValidationError]
) -> dict[str, object] | None:
    display = _display_path(path, root)
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        errors.append(
            ValidationError(display, "FRONTMATTER", "文件必须以完整的 YAML frontmatter 开头")
        )
        return None

    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        detail = str(exc).splitlines()[0]
        errors.append(ValidationError(display, "FRONTMATTER_YAML", f"YAML 无效：{detail}"))
        return None

    if not isinstance(metadata, dict):
        errors.append(ValidationError(display, "FRONTMATTER_TYPE", "frontmatter 必须是键值映射"))
        return None
    return metadata


def _validate_layout(path: Path, skills_root: Path, root: Path) -> list[ValidationError]:
    errors: list[ValidationError] = []
    display = _display_path(path, root)
    parts = path.relative_to(skills_root).parts
    if len(parts) not in {2, 3}:
        errors.append(
            ValidationError(
                display,
                "DIRECTORY_DEPTH",
                "仅支持 skills/<skill>/SKILL.md 或 skills/<category>/<skill>/SKILL.md",
            )
        )
        return errors

    skill_dir = parts[-2]
    if skill_dir != "_template" and not NAME_PATTERN.fullmatch(skill_dir):
        errors.append(
            ValidationError(display, "SKILL_DIRECTORY", "Skill 目录名必须使用小写 kebab-case")
        )

    if len(parts) == 3 and not NAME_PATTERN.fullmatch(parts[0]):
        errors.append(
            ValidationError(display, "CATEGORY_DIRECTORY", "分类目录名必须使用小写 kebab-case")
        )
    return errors


def _extract_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def _slugify_heading(heading: str) -> str:
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = re.sub(r"!?(?:\[([^\]]*)\])\([^)]*\)", r"\1", heading)
    heading = heading.replace("`", "").lower().strip()
    chars: list[str] = []
    for char in heading:
        category = unicodedata.category(char)
        if char == "-" or char.isspace() or category[0] in {"L", "N", "M"}:
            chars.append(char)
    return re.sub(r"\s+", "-", "".join(chars).strip())


def _heading_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    counts: defaultdict[str, int] = defaultdict(int)
    for match in HEADING_PATTERN.finditer(text):
        base = _slugify_heading(match.group(1))
        if not base:
            continue
        count = counts[base]
        anchor = base if count == 0 else f"{base}-{count}"
        counts[base] += 1
        anchors.add(anchor)
    return anchors


def _validate_links(
    path: Path,
    text: str,
    root: Path,
    errors: list[ValidationError],
    markdown_cache: dict[Path, str | None],
) -> None:
    display = _display_path(path, root)
    for match in LINK_PATTERN.finditer(text):
        target = _extract_link_target(match.group(1))
        if not target:
            continue

        parsed = urlsplit(target)
        if parsed.scheme.lower() in EXTERNAL_SCHEMES or target.startswith("//"):
            continue
        if parsed.scheme:
            continue
        if parsed.path.startswith("/"):
            errors.append(
                ValidationError(display, "ABSOLUTE_LINK", f"仓库文件请使用相对链接：{target}")
            )
            continue

        relative_path = unquote(parsed.path)
        linked_path = path if not relative_path else (path.parent / relative_path).resolve()
        try:
            linked_path.relative_to(root.resolve())
        except ValueError:
            errors.append(
                ValidationError(display, "LINK_OUTSIDE_REPOSITORY", f"链接超出仓库范围：{target}")
            )
            continue

        if not linked_path.exists():
            errors.append(ValidationError(display, "BROKEN_LINK", f"目标不存在：{target}"))
            continue

        anchor = unquote(parsed.fragment).lower()
        if not anchor:
            continue
        if linked_path.suffix.lower() not in {".md", ".mdx"}:
            errors.append(
                ValidationError(display, "ANCHOR_TARGET", f"锚点只能指向 Markdown 文件：{target}")
            )
            continue

        if linked_path not in markdown_cache:
            markdown_cache[linked_path] = _read_text(linked_path, root, errors)
        linked_text = markdown_cache[linked_path]
        if linked_text is not None and anchor not in _heading_anchors(linked_text):
            errors.append(ValidationError(display, "BROKEN_ANCHOR", f"锚点不存在：{target}"))


def validate_repository(root: Path) -> list[ValidationError]:
    """返回仓库内所有 Skill 校验错误。"""
    root = root.resolve()
    skills_root = root / "skills"
    errors: list[ValidationError] = []
    if not skills_root.is_dir():
        return [ValidationError("skills", "SKILLS_DIRECTORY", "缺少 skills/ 目录")]

    skill_files = sorted(skills_root.rglob("SKILL.md"))
    if not skill_files:
        return [ValidationError("skills", "NO_SKILLS", "未找到任何 SKILL.md")]

    names: defaultdict[str, list[Path]] = defaultdict(list)
    markdown_cache: dict[Path, str | None] = {}

    for path in skill_files:
        errors.extend(_validate_layout(path, skills_root, root))
        text = _read_text(path, root, errors)
        if text is None:
            continue
        markdown_cache[path.resolve()] = text
        metadata = _parse_frontmatter(path, text, root, errors)
        if metadata is not None:
            for field in ("name", "description"):
                value = metadata.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(
                        ValidationError(
                            _display_path(path, root),
                            "REQUIRED_FIELD",
                            f"frontmatter 字段 {field!r} 必须是非空字符串",
                        )
                    )

            name = metadata.get("name")
            if isinstance(name, str) and name.strip():
                name = name.strip()
                names[name].append(path)
                if name != path.parent.name:
                    errors.append(
                        ValidationError(
                            _display_path(path, root),
                            "NAME_MISMATCH",
                            f"name {name!r} 必须与目录名 {path.parent.name!r} 一致",
                        )
                    )
                if name != "_template" and not NAME_PATTERN.fullmatch(name):
                    errors.append(
                        ValidationError(
                            _display_path(path, root),
                            "SKILL_NAME",
                            "name 必须使用小写 kebab-case",
                        )
                    )

        _validate_links(path, text, root, errors, markdown_cache)

    for name, paths in names.items():
        if len(paths) > 1:
            locations = "、".join(_display_path(path, root) for path in paths)
            for path in paths:
                errors.append(
                    ValidationError(
                        _display_path(path, root),
                        "DUPLICATE_NAME",
                        f"Skill 名称 {name!r} 重复：{locations}",
                    )
                )

    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="仓库根目录，默认自动定位",
    )
    args = parser.parse_args()
    errors = validate_repository(args.root)
    if errors:
        print(f"校验失败：发现 {len(errors)} 个问题。", file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    count = len(list((args.root / "skills").rglob("SKILL.md")))
    print(f"校验通过：共检查 {count} 个 SKILL.md。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
