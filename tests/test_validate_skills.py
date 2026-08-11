from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_skills import validate_repository


class ValidateSkillsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        (self.root / "skills").mkdir()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_skill(
        self,
        relative_directory: str,
        *,
        name: str | None = None,
        description: str = "测试技能",
        body: str = "# 使用说明\n",
    ) -> Path:
        directory = self.root / "skills" / relative_directory
        directory.mkdir(parents=True, exist_ok=True)
        skill_name = name if name is not None else directory.name
        path = directory / "SKILL.md"
        path.write_text(
            f"---\nname: {skill_name}\ndescription: {description}\n---\n\n{body}",
            encoding="utf-8",
        )
        return path

    def error_codes(self) -> set[str]:
        return {error.code for error in validate_repository(self.root)}

    def test_accepts_top_level_and_category_skills(self) -> None:
        self.write_skill("simple-skill")
        self.write_skill("ai-drama/story-skill")
        self.assertEqual(validate_repository(self.root), [])

    def test_accepts_internal_template(self) -> None:
        self.write_skill("_template")
        self.assertEqual(validate_repository(self.root), [])

    def test_rejects_missing_or_invalid_frontmatter(self) -> None:
        path = self.write_skill("broken-skill")
        path.write_text("# 无 frontmatter\n", encoding="utf-8")
        self.assertIn("FRONTMATTER", self.error_codes())

        path.write_text("---\nname: [\n---\n", encoding="utf-8")
        self.assertIn("FRONTMATTER_YAML", self.error_codes())

    def test_rejects_missing_required_fields(self) -> None:
        path = self.write_skill("missing-field")
        path.write_text("---\nname: missing-field\n---\n", encoding="utf-8")
        self.assertIn("REQUIRED_FIELD", self.error_codes())

    def test_rejects_name_mismatch_and_duplicate_names(self) -> None:
        self.write_skill("first-skill", name="shared-name")
        self.write_skill("category/second-skill", name="shared-name")
        codes = self.error_codes()
        self.assertIn("NAME_MISMATCH", codes)
        self.assertIn("DUPLICATE_NAME", codes)

    def test_rejects_invalid_directory_layout_and_names(self) -> None:
        self.write_skill("too/deep/nested-skill")
        self.write_skill("BadCategory/good-skill")
        self.write_skill("BadSkill")
        codes = self.error_codes()
        self.assertIn("DIRECTORY_DEPTH", codes)
        self.assertIn("CATEGORY_DIRECTORY", codes)
        self.assertIn("SKILL_DIRECTORY", codes)

    def test_checks_relative_links_and_ignores_external_links(self) -> None:
        self.write_skill(
            "linked-skill",
            body="[存在](references/guide.md) [缺失](references/missing.md) "
            "[官网](https://example.com)\n",
        )
        reference = self.root / "skills/linked-skill/references/guide.md"
        reference.parent.mkdir()
        reference.write_text("# 指南\n", encoding="utf-8")
        errors = validate_repository(self.root)
        self.assertEqual([error.code for error in errors], ["BROKEN_LINK"])

    def test_checks_local_and_cross_file_anchors(self) -> None:
        self.write_skill(
            "anchor-skill",
            body=(
                "# 使用说明\n"
                "[本页](#使用说明) [跨文件](references/guide.md#配置方法) "
                "[错误](references/guide.md#不存在)\n"
            ),
        )
        reference = self.root / "skills/anchor-skill/references/guide.md"
        reference.parent.mkdir()
        reference.write_text("# 配置方法\n", encoding="utf-8")
        errors = validate_repository(self.root)
        self.assertEqual([error.code for error in errors], ["BROKEN_ANCHOR"])


if __name__ == "__main__":
    unittest.main()
