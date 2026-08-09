#!/usr/bin/env python3
"""Tests for ai-novel-writer project validation."""

import tempfile
import unittest
from pathlib import Path

from validate_project import validate_project


VALID_BODY = "沈弦推开门。" * 280


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_project(root: Path, *, legacy: bool = False, body: str = VALID_BODY) -> None:
    names = [
        "00_作品设定.md" if legacy else "00_作品定位.md",
        "01_角色设定.md",
        "02_故事总纲.md",
        "03_分集大纲.md" if legacy else "03_章节规划.md",
        "04_创作进度.md",
    ]
    if not legacy:
        names.append("05_追读账本.md")
    for name in names:
        write(root / name, f"# {name[:-3]}\n\n有效内容。\n")
    write(root / "正文" / "第001章_开始.md", f"# 第001章 开始\n\n{body}\n")
    write(
        root / "漫剧改编" / "第001集_改编资料.md",
        "# 第001集 改编资料\n\n- 对应正文：第001章\n- 本集目标：确认线索\n",
    )


class ValidateProjectTests(unittest.TestCase):
    def test_valid_new_project_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_project(root)
            self.assertEqual(validate_project(root, 1500, 2500, legacy=False), [])

    def test_new_project_requires_retention_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_project(root)
            (root / "05_追读账本.md").unlink()
            errors = validate_project(root, 1500, 2500, legacy=False)
            self.assertTrue(any("05_追读账本.md" in error for error in errors))

    def test_legacy_mode_accepts_old_file_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_project(root, legacy=True)
            self.assertEqual(validate_project(root, 1500, 2500, legacy=True), [])

    def test_short_chapter_fails_minimum(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_project(root, body="太短了。" * 30)
            errors = validate_project(root, 1500, 2500, legacy=False)
            self.assertTrue(any("少于下限" in error for error in errors))

    def test_production_instructions_in_body_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_project(root, body=VALID_BODY + "\n镜头1：推进画面。")
            errors = validate_project(root, 1500, 2500, legacy=False)
            self.assertTrue(any("制作指令" in error for error in errors))

    def test_chapter_numbers_must_be_continuous(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_project(root)
            write(root / "正文" / "第003章_跳号.md", f"# 第003章 跳号\n\n{VALID_BODY}\n")
            errors = validate_project(root, 1500, 2500, legacy=False)
            self.assertTrue(any("章节编号不连续" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
