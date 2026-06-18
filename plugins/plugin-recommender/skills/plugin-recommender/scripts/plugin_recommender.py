import csv
import gzip
from pathlib import Path

from local_catalog import load_overlay, merge_rows, refresh_overlay
from scoring import build_reason, normalize, rule_scores, text_score


CATALOG_PATH = Path(__file__).with_name("Codex_플러그인_카탈로그_KR.csv.gz")


def load_catalog(catalog_path=CATALOG_PATH):
    opener = gzip.open if catalog_path.suffix == ".gz" else open
    with opener(catalog_path, "rt", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"카탈로그가 비어 있습니다: {catalog_path}")
    return rows


def load_effective_catalog(catalog_path=CATALOG_PATH, refresh_local=False):
    rows = load_catalog(catalog_path)
    if refresh_local:
        refresh_overlay(rows)
    return merge_rows(rows, load_overlay())


def build_recommendation(row, score, reasons):
    return {
        "plugin": row.get("플러그인명", ""),
        "category": row.get("분류", ""),
        "score": score,
        "reason": build_reason(row, reasons, score),
        "account_connection": row.get("계정 연결", ""),
        "cost_plan": row.get("비용/플랜", ""),
        "notes": row.get("주의사항", ""),
    }


def score_catalog_rows(rows, query_tokens, rule_score_map, reason_map):
    ranked = []
    for row in rows:
        plugin = row.get("플러그인명", "")
        score = text_score(query_tokens, row) + rule_score_map.get(plugin, 0)
        if score > 0:
            ranked.append(build_recommendation(row, score, reason_map.get(plugin, [])))
    return ranked


def top_unique_recommendations(ranked, top_k):
    ranked.sort(key=lambda item: (-item["score"], item["plugin"]))
    deduped = []
    seen = set()
    for item in ranked:
        if item["plugin"] in seen:
            continue
        seen.add(item["plugin"])
        deduped.append(item)
        if len(deduped) >= top_k:
            break
    return deduped


def recommend_plugins(query, top_k=5, catalog_path=CATALOG_PATH, refresh_local=False):
    rows = load_effective_catalog(catalog_path, refresh_local=refresh_local)
    query_tokens = normalize(query).split()
    rules, reasons = rule_scores(query)
    ranked = score_catalog_rows(rows, query_tokens, rules, reasons)
    return top_unique_recommendations(ranked, top_k)


if __name__ == "__main__":
    from plugin_recommender_cli import main

    main()
