import argparse
import json

from local_catalog import is_refresh_request, load_overlay, refresh_overlay
from plugin_recommender import load_catalog, recommend_plugins
from plugin_recommender_output import format_local_plugins, format_recommendations


def parser():
    cli = argparse.ArgumentParser(description="Codex 플러그인 카탈로그 기반 경량 추천기")
    cli.add_argument("query", nargs="?", default="", help="사용자 작업 명령")
    cli.add_argument("--top-k", type=int, default=5, help="추천 개수")
    cli.add_argument("--json", action="store_true", help="JSON으로 출력")
    cli.add_argument("--refresh-local", action="store_true", help="로컬 설치 플러그인을 스캔")
    cli.add_argument("--list-local-plugins", action="store_true", help="로컬 overlay catalog 목록 출력")
    return cli


def print_json(payload):
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))


def handle_refresh(args, base_rows):
    result = refresh_overlay(base_rows)
    if args.json:
        print_json(result)
    else:
        print(f"로컬 플러그인 스캔 완료: {len(result['added'])}개 추가")
        print(f"Overlay catalog: {result['path']}")


def handle_local_list(args):
    rows = load_overlay()
    print_json(rows) if args.json else print(format_local_plugins(rows))


def main():
    cli = parser()
    args = cli.parse_args()
    should_refresh = args.refresh_local or is_refresh_request(args.query)

    if should_refresh:
        handle_refresh(args, load_catalog())
        return
    if args.list_local_plugins:
        handle_local_list(args)
        return
    if not args.query:
        cli.error("query가 필요합니다. 로컬 스캔만 하려면 --refresh-local을 사용하세요.")

    results = recommend_plugins(args.query, top_k=args.top_k)
    print_json(results) if args.json else print(format_recommendations(results))
