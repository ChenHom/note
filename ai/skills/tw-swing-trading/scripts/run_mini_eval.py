#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "SKILL.md"
QUERIES_MD = ROOT / "references" / "eval_queries.md"

POSITIVE_HINTS = {
    "波段", "breakout", "pullback", "拉回", "拉回買點", "趨勢", "支撐", "minervini", "trim", "停損", "持倉", "watchlist quality", "entry quality", "假突破", "觀察名單"
}
NEGATIVE_HINTS = {
    "當沖", "supplement", "intraday_event_signals", "frontmatter", "description", "benchmark", "baseline", "dockerfile", "旅遊", "財報", "情緒"
}


def parse_frontmatter_description(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return ""
    for line in m.group(1).splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return ""


def parse_queries(md: str) -> dict[str, list[str]]:
    buckets = {"positive": [], "boundary": [], "negative": []}
    current = None
    for raw in md.splitlines():
        line = raw.strip()
        if line == "## Positive Cases":
            current = "positive"
            continue
        if line == "## Adjacent / Boundary Cases":
            current = "boundary"
            continue
        if line == "## Negative Cases":
            current = "negative"
            continue
        if current and re.match(r"^\d+\. ", line):
            buckets[current].append(re.sub(r"^\d+\. ", "", line))
    return buckets


def score_query(query: str, description: str) -> dict:
    q = query.lower()
    d = description.lower()
    pos = sum(1 for hint in POSITIVE_HINTS if hint.lower() in q and hint.lower() in d)
    neg = sum(1 for hint in NEGATIVE_HINTS if hint.lower() in q)
    return {"positive_overlap": pos, "negative_hits": neg, "score": pos - neg}


def expected_pass(bucket: str, score: int) -> bool:
    if bucket == "positive":
        return score > 0
    return score <= 0


def main() -> None:
    description = parse_frontmatter_description(SKILL_MD.read_text(encoding="utf-8"))
    queries = parse_queries(QUERIES_MD.read_text(encoding="utf-8"))
    results = []
    for bucket, items in queries.items():
        for idx, query in enumerate(items, start=1):
            scoring = score_query(query, description)
            results.append({
                "id": f"{bucket}-{idx}",
                "bucket": bucket,
                "query": query,
                **scoring,
                "passed": expected_pass(bucket, scoring["score"]),
            })
    summary = {
        "total": len(results),
        "passed": sum(1 for r in results if r["passed"]),
        "failed": sum(1 for r in results if not r["passed"]),
    }
    summary["pass_rate"] = round(summary["passed"] / summary["total"], 4) if summary["total"] else 0.0
    print(json.dumps({"summary": summary, "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
