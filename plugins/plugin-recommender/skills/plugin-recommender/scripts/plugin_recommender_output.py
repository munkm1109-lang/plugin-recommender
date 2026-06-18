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
        lines.append(f"   - 서비스: {row.get('서비스 설명') or row.get('한 줄 설명', '')}")
        lines.append(f"   - 연결 필요성: {row.get('계정 연결', '확인 필요')}")
        lines.append(f"   - 플러그인 기능: {row.get('플러그인 기능') or row.get('주요 기능', '')}")
        lines.append(f"   - 대표 스킬: {row.get('대표 스킬', '') or '없음'}")
        lines.append(f"   - 위치: {row.get('source_path', '')}")
    return "\n".join(lines)


def format_added_plugins(rows):
    if not rows:
        return "새로 추가된 플러그인은 없습니다. 이미 카탈로그에 있거나 이전 스캔에서 추가된 상태입니다."

    lines = ["새로 추가된 플러그인:"]
    for index, row in enumerate(rows, start=1):
        lines.append(f"{index}. {row.get('플러그인명', '')} ({row.get('분류', '')})")
        lines.append(f"   - 서비스: {row.get('서비스 설명') or row.get('한 줄 설명', '')}")
        lines.append(f"   - 연결 필요성: {row.get('계정 연결', '확인 필요')}")
        lines.append(f"   - 플러그인 기능: {row.get('플러그인 기능') or row.get('주요 기능', '')}")
        lines.append(f"   - 대표 스킬: {row.get('대표 스킬', '') or '없음'}")
        lines.append(f"   - 위치: {row.get('source_path', '')}")
    return "\n".join(lines)
