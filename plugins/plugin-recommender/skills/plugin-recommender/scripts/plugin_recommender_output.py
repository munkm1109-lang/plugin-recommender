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


def format_local_plugins(rows):
    if not rows:
        return "로컬 overlay catalog에 추가된 플러그인이 없습니다."

    lines = []
    for index, row in enumerate(rows, start=1):
        lines.append(f"{index}. {row.get('플러그인명', '')} ({row.get('분류', '')})")
        lines.append(f"   - 설명: {row.get('한 줄 설명', '')}")
        lines.append(f"   - 대표 스킬: {row.get('대표 스킬', '')}")
        lines.append(f"   - 위치: {row.get('source_path', '')}")
    return "\n".join(lines)
