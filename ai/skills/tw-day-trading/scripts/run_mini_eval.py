#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "SKILL.md"
QUERIES_MD = ROOT / "references" / "eval_queries.md"

POSITIVE_HINTS = {
    "當沖", "盤前", "checklist", "vwap", "量能", "大盤", "supplement",
    "intraday", "event", "force exit", "force-exit", "qtds",
    "quantitative-trading-decision-system", "盤中", "停損", "停利"
}

NEGATIVE_HINTS = {
    "波段", "frontmatter", "description", "benchmark", "baseline", "blind",
    "regression", "dockerfile", "旅遊", "財報", "情緒", "skill 建出來",
    "新 trading skill", "新 skill"
}


def parse_frontmatter_description(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return ""
    fm = m.group(1)
    for line in fm.splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return ""


def parse_queries(md: str) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {"positive": [], "boundary": [], "negative": []}
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
    if bucket == "boundary":
        return score <= 0
    if bucket == "negative":
        return score <= 0
    return False


def main() -> None:
    skill_text = SKILL_MD.read_text(encoding="utf-8")
    description = parse_frontmatter_description(skill_text)
    queries = parse_queries(QUERIES_MD.read_text(encoding="utf-8"))

    results = []
    for bucket, items in queries.items():
        for idx, query in enumerate(items, start=1):
            scoring = score_query(query, description)
            passed = expected_pass(bucket, scoring["score"])
            results.append({
                "id": f"{bucket}-{idx}",
                "bucket": bucket,
                "query": query,
                **scoring,
                "passed": passed,
            })

    summary = {
        "total": len(results),
        "passed": sum(1 for r in results if r["passed"]),
        "failed": sum(1 for r in results if not r["passed"]),
    }
    summary["pass_rate"] = round(summary["passed"] / summary["total"], 4) if summary["total"] else 0.0

    payload = {"summary": summary, "results": results}
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
