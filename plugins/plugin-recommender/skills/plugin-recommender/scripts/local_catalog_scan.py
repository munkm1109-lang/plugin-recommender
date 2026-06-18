from pathlib import Path

from local_catalog_common import (
    OVERLAY_PATH,
    PLUGIN_JSON,
    catalog_keys,
    default_scan_roots,
    load_overlay,
    merge_rows,
    normalize_plugin_key,
    read_json,
    save_overlay,
)
from local_catalog_extract import display_name, plugin_row


def path_parts(path):
    return str(path).replace("\\", "/").split("/")


def is_fixture_path(path):
    return "fixtures" in map(str.lower, path_parts(path))


def remove_fixture_rows(rows):
    return [row for row in rows if not is_fixture_path(row.get("source_path", ""))]


def iter_plugin_roots(scan_roots):
    seen = set()
    for root in scan_roots:
        for manifest_path in root.rglob("plugin.json"):
            if is_fixture_path(manifest_path):
                continue
            if not manifest_path.as_posix().endswith(PLUGIN_JSON):
                continue
            plugin_root = manifest_path.parents[1]
            resolved = str(plugin_root.resolve())
            if resolved in seen:
                continue
            seen.add(resolved)
            yield plugin_root


def is_known_plugin(manifest, known):
    candidates = [manifest.get("name", ""), display_name(manifest)]
    candidate_keys = set(map(normalize_plugin_key, filter(None, candidates)))
    return bool(known.intersection(candidate_keys))


def add_known_plugin(row, known):
    known.add(normalize_plugin_key(row["플러그인명"]))
    known.add(normalize_plugin_key(row.get("manifest_name", "")))


def scan_local_plugins(existing_rows, scan_roots=None):
    known = catalog_keys(existing_rows)
    rows = []
    for plugin_root in iter_plugin_roots(scan_roots or default_scan_roots()):
        manifest = read_json(plugin_root / PLUGIN_JSON)
        if not manifest or is_known_plugin(manifest, known):
            continue
        row = plugin_row(plugin_root, manifest)
        if row["플러그인명"]:
            rows.append(row)
            add_known_plugin(row, known)
    return rows


def refresh_current_rows(rows):
    refreshed = []
    for row in rows:
        plugin_root = Path(row.get("source_path", ""))
        manifest = read_json(plugin_root / PLUGIN_JSON)
        if not manifest:
            refreshed.append(row)
            continue
        updated = plugin_row(plugin_root, manifest)
        updated["detected_at"] = row.get("detected_at", updated["detected_at"])
        refreshed.append(updated)
    return refreshed


def refresh_overlay(base_rows, scan_roots=None, path=None):
    overlay_path = path or OVERLAY_PATH
    current = refresh_current_rows(remove_fixture_rows(load_overlay(overlay_path)))
    known_rows = merge_rows(base_rows, current)
    discovered = scan_local_plugins(known_rows, scan_roots=scan_roots)
    updated = merge_rows(current, discovered)
    save_overlay(updated, overlay_path)
    return {"rows": updated, "added": discovered, "path": overlay_path}
