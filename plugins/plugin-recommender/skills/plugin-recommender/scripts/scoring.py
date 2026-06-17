import re

from catalog_data import RULES, USAGE_OVERRIDES


TOKEN_RE = re.compile(r"[a-z0-9가-힣+#.-]+", re.IGNORECASE)


def normalize(text):
    return " ".join(TOKEN_RE.findall(text.lower()))


def term_matches_query(term, normalized_query, query_tokens):
    normalized_term = normalize(term)
    if len(normalized_term) <= 1:
        return normalized_term in query_tokens
    return normalized_term in normalized_query


def matched_terms(rule, normalized_query, query_tokens):
    return [term for term in rule["terms"] if term_matches_query(term, normalized_query, query_tokens)]


def apply_rule_scores(scores, reasons, rule, matched):
    reason = f"작업 키워드 매칭: {', '.join(matched[:3])}"
    for plugin, score in rule["plugins"].items():
        scores[plugin] = scores.get(plugin, 0) + score
        reasons.setdefault(plugin, []).append(reason)


def rule_scores(query):
    normalized = normalize(query)
    query_tokens = set(normalized.split())
    scores = {}
    reasons = {}
    for rule in RULES:
        matched = matched_terms(rule, normalized, query_tokens)
        if matched:
            apply_rule_scores(scores, reasons, rule, matched)
    return scores, reasons


def text_score(query_tokens, row):
    searchable = normalize(
        " ".join(
            [
                row.get("분류", ""),
                row.get("플러그인명", ""),
                row.get("한 줄 설명", ""),
                row.get("사용 상황", ""),
                row.get("주요 기능", ""),
                row.get("대표 스킬", ""),
            ]
        )
    )
    score = 0
    for token in query_tokens:
        if len(token) < 2:
            continue
        if token == normalize(row.get("플러그인명", "")):
            score += 20
        elif token in searchable:
            score += 3
    return score


def build_reason(row, explicit_reasons, score):
    parts = []
    if explicit_reasons:
        parts.extend(explicit_reasons[:2])
    parts.append(USAGE_OVERRIDES.get(row.get("플러그인명", ""), row.get("사용 상황", "사용 상황 확인 필요")))
    return " / ".join(parts)
