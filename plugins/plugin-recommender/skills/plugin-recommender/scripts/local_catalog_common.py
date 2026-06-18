import json
import re
from datetime import datetime, timezone
from pathlib import Path


OVERLAY_PATH = Path.home() / ".codex" / "plugin-recommender" / "local_catalog_overlay.json"
PLUGIN_JSON = ".codex-plugin/plugin.json"


def default_scan_roots():
    home = Path.home()
    roots = [
        home / ".codex" / "plugins" / "cache",
        home / ".codex" / ".tmp" / "marketplaces",
        home / "plugins",
    ]
    return [path for path in roots if path.exists()]


def normalize_plugin_key(value):
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def catalog_keys(rows):
    keys = set()
    for row in rows:
        values = [row.get("플러그인명", ""), row.get("manifest_name", "")]
        values.append(values[0].replace(" ", "-"))
        keys.update(normalize_plugin_key(value) for value in values if value)
    return keys


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return None


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def load_overlay(path=OVERLAY_PATH):
    payload = read_json(path)
    return payload.get("rows", []) if payload else []


def save_overlay(rows, path=OVERLAY_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": 1, "updated_at": timestamp(), "rows": rows}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def merge_rows(base_rows, overlay_rows):
    merged = list(base_rows)
    known = catalog_keys(merged)
    for row in overlay_rows:
        keys = [
            normalize_plugin_key(row.get("플러그인명", "")),
            normalize_plugin_key(row.get("manifest_name", "")),
        ]
        if known.intersection(keys):
            continue
        merged.append(row)
        known.update(keys)
    return merged
