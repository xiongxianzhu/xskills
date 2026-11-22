"""回归覆盖：漏检后续提示词、全文预算、虚构引用与原台词保真。"""
from __future__ import annotations

import unittest

from grade_evals import extract_prompt_blocks, grade_output, reference_ids


class GradeEvalsTests(unittest.TestCase):
    def failed(self, result):
        return [item["text"] for item in result["expectations"] if not item["passed"]]

    def test_checks_overflow_in_second_block(self):
        result = grade_output("```text\n第一段\n```\n```text\n" + "镜" * 2001 + "\n```", "action-thirty-seconds")
        self.assertEqual(self.failed(result), ["提示词块 2 非空且未超预算"])

    def test_counts_intro_in_entire_response_budget(self):
        result = grade_output("说明" * 450 + "\n```text\n角色展示\n```", "portrait-onetake-budget")
        self.assertIn("全文未超预算", self.failed(result))

    def test_dialogue_with_negative_word_is_valid(self):
        result = grade_output("```text\n男子说道：不要回头，他们来了！\n```", "cyberpunk-chase-16x9")
        self.assertEqual(self.failed(result), [])
        self.assertTrue(result["manual_review_required"])
        self.assertTrue(result["automatic_checks_only"])

    def test_dialogue_only_in_commentary_does_not_count(self):
        result = grade_output("保留：不要回头，他们来了！\n```text\n男子继续奔跑。\n```", "cyberpunk-chase-16x9")
        self.assertTrue(any("保留原文" in item for item in self.failed(result)))

    def test_rejects_invented_reference_in_second_block(self):
        result = grade_output("```text\n第一段\n```\n```text\n参考@图片2的外貌\n```", "action-thirty-seconds")
        self.assertIn("提示词无未声明素材引用", self.failed(result))

    def test_accepts_declared_reference_aliases(self):
        result = grade_output("```text\n@图片 1锁定人物，@Video1只参考运镜，@audio1作配乐。\n```", "reference-roles")
        self.assertEqual(self.failed(result), [])

    def test_normalizes_newlines_before_counting(self):
        result = grade_output("```text\r\n第一行\r\n第二行\r\n```", "bamboo-portrait-9x16")
        self.assertEqual(result["prompt_char_counts"], [7])

    def test_python_block_cannot_stand_in_for_prompt(self):
        result = grade_output("```python\nprint(1)\n```", "bamboo-portrait-9x16")
        self.assertIn("提示词块数量符合任务", self.failed(result))

    def test_unclosed_prompt_is_not_accepted(self):
        result = grade_output("```text\n未闭合内容", "bamboo-portrait-9x16")
        self.assertIn("提示词块数量符合任务", self.failed(result))

    def test_empty_output_fails_even_when_clarification_is_expected(self):
        result = grade_output("", "missing-continuation-state")
        self.assertIn("输出非空", self.failed(result))

    def test_unknown_case_does_not_silently_pass(self):
        with self.assertRaises(ValueError):
            grade_output("```text\n内容\n```", "unknown-case")

    def test_supports_long_and_tilde_fences(self):
        blocks = extract_prompt_blocks("````text\n保留```字符\n````\n~~~text\n第二段\n~~~")
        self.assertEqual(blocks, ["保留```字符", "第二段"])
        self.assertEqual(reference_ids("@图片1与@image1、@音频 2"), {"image1", "audio2"})


if __name__ == "__main__":
    unittest.main()
