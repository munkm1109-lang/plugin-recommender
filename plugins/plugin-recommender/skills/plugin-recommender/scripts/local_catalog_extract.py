import re

from local_catalog_common import read_json, timestamp


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)


def first_value(*values, default=""):
    picked = list(filter(None, values))
    return picked[0] if picked else default


def frontmatter_description(skill_path):
    try:
        text = skill_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""
    match = FRONTMATTER_RE.match(text)
    lines = match.group(1).splitlines() if match else []
    descriptions = [
        line.split(":", 1)[1].strip().strip("\"'")
        for line in lines
        if line.strip().startswith("description:")
    ]
    return descriptions[0] if descriptions else ""


def skill_summaries(plugin_root):
    skills_root = plugin_root / "skills"
    skill_files = skills_root.glob("*/SKILL.md")
    return [
        {"name": skill_file.parent.name, "description": frontmatter_description(skill_file)}
        for skill_file in skill_files
    ]


def display_name(manifest):
    interface = manifest.get("interface", {})
    return first_value(interface.get("displayName"), manifest.get("name"))


def app_connection_required(plugin_root):
    app_config = read_json(plugin_root / ".app.json") or {}
    apps = app_config.get("apps", {})
    return any(config.get("required") for config in apps.values() if isinstance(config, dict))


def service_description(manifest):
    interface = manifest.get("interface", {})
    name = display_name(manifest)
    developer = first_value(
        interface.get("developerName"),
        manifest.get("author", {}).get("name"),
        default="확인 필요",
    )
    category = first_value(interface.get("category"), default="확인 필요")
    website = first_value(interface.get("websiteURL"), manifest.get("homepage"))
    base = f"{name}는 {developer}에서 제공하는 {category} 서비스 또는 플러그인입니다."
    return f"{base} 웹사이트: {website}" if website else base


def connection_label(plugin_root):
    if app_connection_required(plugin_root):
        return "필요: 외부 서비스 계정 또는 워크스페이스 연결 필요"
    return "확인 필요"


def cost_label(manifest):
    license_name = manifest.get("license", "")
    if license_name.lower() == "proprietary":
        return "외부 서비스 플랜/권한 확인 필요"
    return "확인 필요"


def plugin_row(plugin_root, manifest):
    interface = manifest.get("interface", {})
    skills = skill_summaries(plugin_root)
    skill_names = ", ".join(skill["name"] for skill in skills)
    skill_descriptions = " / ".join(skill["description"] for skill in skills if skill["description"])
    description = first_value(interface.get("shortDescription"), manifest.get("description"))
    usage = first_value(interface.get("longDescription"), skill_descriptions, description)
    return {
        "분류": first_value(interface.get("category"), default="확인 필요"),
        "플러그인명": display_name(manifest),
        "한 줄 설명": description,
        "서비스 설명": service_description(manifest),
        "사용 상황": usage,
        "플러그인 기능": usage,
        "주요 기능": first_value(skill_descriptions, description),
        "대표 스킬": skill_names,
        "계정 연결": connection_label(plugin_root),
        "비용/플랜": cost_label(manifest),
        "주의사항": f"로컬 설치 플러그인에서 자동 감지됨: {plugin_root}",
        "source_path": str(plugin_root),
        "manifest_name": manifest.get("name", ""),
        "detected_at": timestamp(),
    }
