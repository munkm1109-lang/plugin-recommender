import argparse
import csv
import json
import re
from pathlib import Path


CATALOG_PATH = Path(__file__).with_name("Codex_플러그인_카탈로그_KR.csv")


RULES = [
    {
        "terms": ["ppt", "powerpoint", "발표", "발표자료", "슬라이드", "프레젠테이션"],
        "plugins": {"Presentations": 120, "Documents": 12, "PDF": 8},
    },
    {
        "terms": ["pdf", "피디에프"],
        "plugins": {"PDF": 80, "Documents": 16},
    },
    {
        "terms": ["엑셀", "excel", "xlsx", "스프레드시트", "spreadsheet", "표로", "표를", "테이블", "csv"],
        "plugins": {"Spreadsheets": 80, "Data Analytics": 14},
    },
    {
        "terms": ["문서", "word", "docx", "보고서", "제안서", "메모"],
        "plugins": {"Documents": 55, "PDF": 8, "Presentations": 6},
    },
    {
        "terms": ["figma", "피그마", "디자인", "ui", "ux", "화면", "프로토타입", "컴포넌트"],
        "plugins": {"Figma": 80, "Product Design": 24},
    },
    {
        "terms": ["이미지", "그림", "아이콘", "시각자료", "비주얼"],
        "plugins": {"Product Design": 45, "Figma": 20},
    },
    {
        "terms": ["배포", "호스팅", "deploy", "deployment", "vercel"],
        "plugins": {"Vercel": 90, "GitHub": 18, "Browser": 10},
    },
    {
        "terms": ["github", "깃허브", "repo", "repository", "pr", "pull request", "issue", "이슈"],
        "plugins": {"GitHub": 90, "CodeRabbit": 20},
    },
    {
        "terms": ["브라우저", "browser", "localhost", "웹사이트", "화면확인"],
        "plugins": {"Browser": 70, "Chrome": 35},
    },
    {
        "terms": ["chrome", "크롬", "로그인 세션", "쿠키"],
        "plugins": {"Chrome": 80, "Browser": 18},
    },
    {
        "terms": ["데이터", "분석", "대시보드", "dashboard", "kpi", "지표", "차트", "리포트"],
        "plugins": {"Data Analytics": 80, "Spreadsheets": 18},
    },
    {
        "terms": ["notion", "노션", "task", "태스크", "업무관리"],
        "plugins": {"Notion": 80},
    },
    {
        "terms": ["메일", "email", "gmail", "outlook", "수신함"],
        "plugins": {"Gmail": 70, "Outlook Email": 70},
    },
    {
        "terms": ["캘린더", "calendar", "일정", "미팅", "회의"],
        "plugins": {"Google Calendar": 75, "Outlook Calendar": 55},
    },
]


USAGE_OVERRIDES = {
    "Presentations": "PPTX 발표자료 생성, 편집, 렌더링, 슬라이드 검수가 필요한 작업에 사용합니다.",
    "Documents": "Word/DOCX 문서 작성, 편집, 구조화, 문서형 산출물 생성에 사용합니다.",
    "PDF": "PDF 읽기, 추출, 생성, 렌더링, 시각 검수가 필요한 작업에 사용합니다.",
    "Spreadsheets": "Excel/XLSX/CSV 표 작성, 정리, 계산, 스프레드시트 산출물 생성에 사용합니다.",
    "Data Analytics": "데이터 분석, KPI 진단, 리포트, 대시보드 작성에 사용합니다.",
    "Vercel": "웹앱 배포, 호스팅, Vercel 프로젝트 확인과 배포 상태 점검에 사용합니다.",
    "GitHub": "저장소, 이슈, PR, 코드리뷰, GitHub 기반 개발 흐름에 사용합니다.",
    "Browser": "로컬 웹앱, localhost, 웹 화면 확인과 브라우저 테스트에 사용합니다.",
    "Chrome": "기존 Chrome 로그인 세션, 쿠키, 탭 상태가 필요한 웹 작업에 사용합니다.",
}


TOKEN_RE = re.compile(r"[a-z0-9가-힣+#.-]+", re.IGNORECASE)


def normalize(text):
    return " ".join(TOKEN_RE.findall(text.lower()))


def load_catalog(catalog_path=CATALOG_PATH):
    with open(catalog_path, "r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"카탈로그가 비어 있습니다: {catalog_path}")
    return rows


def rule_scores(query):
    normalized = normalize(query)
    query_tokens = set(normalized.split())
    scores = {}
    reasons = {}
    for rule in RULES:
        matched = []
        for term in rule["terms"]:
            normalized_term = normalize(term)
            if len(normalized_term) <= 1:
                is_match = normalized_term in query_tokens
            else:
                is_match = normalized_term in normalized
            if is_match:
                matched.append(term)
        if not matched:
            continue
        for plugin, score in rule["plugins"].items():
            scores[plugin] = scores.get(plugin, 0) + score
            reasons.setdefault(plugin, []).append(f"작업 키워드 매칭: {', '.join(matched[:3])}")
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


def recommend_plugins(query, top_k=5, catalog_path=CATALOG_PATH):
    rows = load_catalog(catalog_path)
    query_tokens = normalize(query).split()
    rules, reasons = rule_scores(query)
    ranked = []

    for row in rows:
        plugin = row.get("플러그인명", "")
        score = text_score(query_tokens, row) + rules.get(plugin, 0)
        if score <= 0:
            continue
        ranked.append(
            {
                "plugin": plugin,
                "category": row.get("분류", ""),
                "score": score,
                "reason": build_reason(row, reasons.get(plugin, []), score),
                "account_connection": row.get("계정 연결", ""),
                "cost_plan": row.get("비용/플랜", ""),
                "notes": row.get("주의사항", ""),
            }
        )

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
