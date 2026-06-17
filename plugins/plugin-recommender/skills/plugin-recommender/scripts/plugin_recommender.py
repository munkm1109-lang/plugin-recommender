import argparse
import csv
import gzip
import json
from pathlib import Path

from scoring import build_reason, normalize, rule_scores, text_score


CATALOG_PATH = Path(__file__).with_name("Codex_플러그인_카탈로그_KR.csv.gz")


def load_catalog(catalog_path=CATALOG_PATH):
    opener = gzip.open if catalog_path.suffix == ".gz" else open
    with opener(catalog_path, "rt", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"카탈로그가 비어 있습니다: {catalog_path}")
    return rows


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


def recommend_plugins(query, top_k=5, catalog_path=CATALOG_PATH):
    rows = load_catalog(catalog_path)
    query_tokens = normalize(query).split()
    rules, reasons = rule_scores(query)
    ranked = score_catalog_rows(rows, query_tokens, rules, reasons)
    return top_unique_recommendations(ranked, top_k)


def format_recommendations(results):
    if not results:
        return "추천할 플러그인을 찾지 못했습니다. 작업 설명을 더 구체적으로 입력하세요."

    lines = []
    for index, item in enumerate(results, start=1):
        lines.append(f"{index}. {item['plugin']} ({item['category']})")
        lines.append(f"   - 추천 이유: {item['reason']}")
        lines.append(f"   - 계정 연결: {item['account_connection']}")
        lines.append(f"   - 비용/플랜: {item['cost_plan']}")
        lines.append(f"   - 주의사항: {item['notes']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Codex 플러그인 카탈로그 기반 경량 추천기")
    parser.add_argument("query", help="사용자 작업 명령")
    parser.add_argument("--top-k", type=int, default=5, help="추천 개수")
    parser.add_argument("--json", action="store_true", help="JSON으로 출력")
    args = parser.parse_args()

    results = recommend_plugins(args.query, top_k=args.top_k)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_recommendations(results))


if __name__ == "__main__":
    main()
