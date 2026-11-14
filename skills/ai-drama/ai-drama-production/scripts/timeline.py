#!/usr/bin/env python3
"""漫剧分镜时长与台词字数校验。

用法：
    python timeline.py plan --duration 75 --shots 28 --cps 4.5
    python timeline.py plan --duration 75 --shots 4 --weights 1.2,1,1,0.8
    python timeline.py check --csv 分镜.csv --duration 75 --cps 4.5

`plan` 按权重把单集时长分配到每个镜头，并给出每镜台词字数上限。
`check` 校验 CSV（表头 shot,duration,chars）的总时长与每镜语速。
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Sequence


def _parse_weights(raw: str | None, shots: int) -> list[float]:
    if not raw:
        return [1.0] * shots
    try:
        weights = [float(part) for part in raw.split(",") if part.strip()]
    except ValueError as exc:
        raise ValueError("--weights 必须是逗号分隔的数字") from exc
    if len(weights) != shots:
        raise ValueError(f"--weights 需要 {shots} 个数字，实际 {len(weights)} 个")
    if any(weight <= 0 for weight in weights):
        raise ValueError("--weights 的每个数字都必须大于 0")
    return weights


def _allocate(total: float, weights: Sequence[float]) -> list[float]:
    """按权重分配时长，保留一位小数，余数补给最长的镜头，保证总和一致。"""
    weight_sum = sum(weights)
    durations = [round(total * weight / weight_sum, 1) for weight in weights]
    diff = round(total - sum(durations), 1)
    if diff:
        index = durations.index(max(durations))
        durations[index] = round(durations[index] + diff, 1)
    return durations


def plan(duration: float, shots: int, cps: float, weights: str | None) -> int:
    try:
        shares = _parse_weights(weights, shots)
    except ValueError as exc:
        print(f"参数错误：{exc}", file=sys.stderr)
        return 2

    durations = _allocate(duration, shares)
    start = 0.0
    total_chars = 0
    print(f"单集时长 {duration:g} 秒，{shots} 镜，语速 {cps:g} 字/秒")
    print()
    print("| 镜号 | 起 | 止 | 时长 | 台词字数上限 | 建议口播字数 |")
    print("| --- | --- | --- | --- | --- | --- |")
    for index, shot_duration in enumerate(durations, start=1):
        end = round(start + shot_duration, 1)
        limit = int(shot_duration * cps)
        advice = int(limit * 0.8)
        total_chars += advice
        print(f"| {index} | {start:.1f}s | {end:.1f}s | {shot_duration:.1f}s | {limit} | {advice} |")
        start = end

    print()
    print(f"合计：{round(sum(durations), 1):g} 秒，建议口播总字数 ≤ {total_chars} 字")
    return 0


def check(csv_path: Path, duration: float, cps: float) -> int:
    if not csv_path.is_file():
        print(f"找不到文件：{csv_path}", file=sys.stderr)
        return 2

    problems: list[str] = []
    total_duration = 0.0
    total_chars = 0
    rows = 0

    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = {"shot", "duration", "chars"} - set(reader.fieldnames or [])
        if missing:
            print(f"CSV 缺少列：{', '.join(sorted(missing))}", file=sys.stderr)
            return 2
        for row in reader:
            rows += 1
            shot = (row["shot"] or "").strip() or f"第{rows}行"
            try:
                shot_duration = float(row["duration"])
                chars = int(row["chars"])
            except (TypeError, ValueError):
                problems.append(f"{shot}：duration 或 chars 不是数字")
                continue
            if shot_duration <= 0:
                problems.append(f"{shot}：时长必须大于 0")
                continue
            if chars < 0:
                problems.append(f"{shot}：字数不能为负")
                continue
            total_duration += shot_duration
            total_chars += chars
            actual_cps = chars / shot_duration
            if actual_cps > cps:
                limit = int(shot_duration * cps)
                problems.append(
                    f"{shot}：{chars} 字 / {shot_duration:g} 秒 = {actual_cps:.1f} 字/秒，超过 {cps:g}，建议 ≤ {limit} 字"
                )

    if rows == 0:
        print("CSV 没有数据行。", file=sys.stderr)
        return 2

    avg_shot = total_duration / rows
    print(f"镜头数：{rows}，总时长：{total_duration:.1f} 秒，平均镜长：{avg_shot:.2f} 秒")
    print(f"台词总字数：{total_chars}，全片语速：{total_chars / total_duration:.2f} 字/秒")

    diff = abs(total_duration - duration)
    if diff > 0.5:
        problems.append(f"总时长 {total_duration:.1f} 秒，与目标 {duration:g} 秒相差 {diff:.1f} 秒（容差 0.5 秒）")
    if avg_shot > 4.0:
        problems.append(f"平均镜长 {avg_shot:.2f} 秒超过 4 秒，画面容易失去节奏")

    if problems:
        print()
        print(f"发现 {len(problems)} 个问题：", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        return 1

    print("校验通过。")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="漫剧分镜时长与台词字数校验")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="按时长与镜头数生成排期")
    plan_parser.add_argument("--duration", type=float, required=True, help="单集时长（秒）")
    plan_parser.add_argument("--shots", type=int, required=True, help="镜头数")
    plan_parser.add_argument("--cps", type=float, default=4.5, help="语速（字/秒），默认 4.5")
    plan_parser.add_argument("--weights", help="逗号分隔的镜头权重，长度需等于镜头数")

    check_parser = subparsers.add_parser("check", help="校验分镜 CSV")
    check_parser.add_argument("--csv", type=Path, required=True, help="CSV 路径，表头 shot,duration,chars")
    check_parser.add_argument("--duration", type=float, required=True, help="目标单集时长（秒）")
    check_parser.add_argument("--cps", type=float, default=4.5, help="语速上限（字/秒），默认 4.5")

    args = parser.parse_args(argv)
    if args.duration <= 0:
        print("参数错误：--duration 必须大于 0", file=sys.stderr)
        return 2

    if args.command == "plan":
        if args.shots <= 0:
            print("参数错误：--shots 必须大于 0", file=sys.stderr)
            return 2
        return plan(args.duration, args.shots, args.cps, args.weights)
    return check(args.csv, args.duration, args.cps)


if __name__ == "__main__":
    raise SystemExit(main())
