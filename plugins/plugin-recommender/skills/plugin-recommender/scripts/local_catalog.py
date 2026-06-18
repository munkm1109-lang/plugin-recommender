import re

from local_catalog_common import OVERLAY_PATH, load_overlay, merge_rows
from local_catalog_scan import refresh_overlay, scan_local_plugins


def is_refresh_request(text):
    normalized = re.sub(r"\s+", "", text.lower())
    phrases = [
        "새로운플러그인설치",
        "새플러그인설치",
        "새로플러그인추가",
        "새플러그인추가",
        "플러그인추가",
        "플러그인스캔",
        "플러그인목록새로고침",
        "로컬플러그인새로고침",
        "refreshlocal",
        "scanplugins",
    ]
    return any(phrase in normalized for phrase in phrases)
