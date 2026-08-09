#!/usr/bin/env python3
"""Tests for high-confidence narrative pattern warnings."""

import tempfile
import unittest
from pathlib import Path

from audit_narrative_patterns import audit_project


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_project(root: Path, *, legacy: bool = False) -> None:
    if legacy:
        write(root / "00_作品设定.md", "# 作品设定\n\n旧作内容。\n")
        write(root / "03_分集大纲.md", "# 分集大纲\n\n旧作内容。\n")
        write(root / "04_创作进度.md", "# 创作进度\n\n旧作内容。\n")
        return

    write(root / "00_作品定位.md", "# 作品定位\n\n## 叙事声纹\n\n具体内容。\n")
    write(root / "03_章节规划.md", "# 章节规划\n\n## 章节结构指纹\n\n具体内容。\n")
    write(root / "04_创作进度.md", "# 创作进度\n\n## 最近五章节奏轨迹\n\n具体内容。\n")


def write_chapter(root: Path, number: int, body: str) -> None:
    write(
        root / "正文" / f"第{number:04d}章_测试.md",
        f"# 第{number:04d}章 测试\n\n{body}\n",
    )


class AuditNarrativePatternsTests(unittest.TestCase):
    def test_three_consecutive_system_endings_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_project(root)
            for number in range(1, 4):
                write_chapter(root, number, f"第{number}章发生了不同事件。\n\n【系统提示：任务完成，奖励已发放】")

            warnings = audit_project(root)

            self.assertTrue(any("连续三章" in warning and "系统" in warning for warning in warnings))

    def test_two_system_endings_do_not_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_project(root)
            for number in range(1, 3):
                write_chapter(root, number, "人物完成行动。\n\n【系统提示：任务完成】")

            warnings = audit_project(root)

            self.assertFalse(any("连续三章" in warning and "系统" in warning for warning in warnings))

    def test_repeated_long_opening_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_project(root)
            repeated = "雨从午夜一直下到天亮，檐沟里的水声像从未停过的旧钟摆。"
            write_chapter(root, 1, f"{repeated}\n\n甲采取行动。")
            write_chapter(root, 2, f"{repeated}\n\n乙采取另一种行动。")

            warnings = audit_project(root)

            self.assertTrue(any("重复开头" in warning for warning in warnings))

    def test_repeated_long_ending_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_project(root)
            repeated = "他把没有寄出的信压回木匣，知道这一次沉默已经改变了两个人。"
            write_chapter(root, 1, f"甲采取行动。\n\n{repeated}")
            write_chapter(root, 2, f"乙采取另一种行动。\n\n{repeated}")

            warnings = audit_project(root)

            self.assertTrue(any("重复结尾" in warning for warning in warnings))

    def test_missing_new_sections_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_project(root)
            write(root / "03_章节规划.md", "# 章节规划\n\n只有普通规划。\n")

            warnings = audit_project(root)

            self.assertTrue(any("章节结构指纹" in warning for warning in warnings))

    def test_legacy_mode_skips_new_section_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_project(root, legacy=True)

            warnings = audit_project(root, legacy=True)

            self.assertFalse(any("缺少栏目" in warning for warning in warnings))


if __name__ == "__main__":
    unittest.main()
