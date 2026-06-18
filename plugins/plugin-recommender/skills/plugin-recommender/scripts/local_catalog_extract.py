import re

from local_catalog_common import timestamp


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL)


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
    skill_files = skills_root.glob("*/SKILL.md") if skills_root.exists() else []
    return [
        {"name": skill_file.parent.name, "description": frontmatter_description(skill_file)}
        for skill_file in skill_files
    ]


def display_name(manifest):
    interface = manifest.get("interface", {})
    return interface.get("displayName") or manifest.get("name", "")


def plugin_row(plugin_root, manifest):
    interface = manifest.get("interface", {})
    skills = skill_summaries(plugin_root)
    skill_names = ", ".join(skill["name"] for skill in skills)
    skill_descriptions = " / ".join(skill["description"] for skill in skills if skill["description"])
    description = interface.get("shortDescription") or manifest.get("description", "")
    usage = interface.get("longDescription") or skill_descriptions or description
    return {
        "분류": interface.get("category") or "확인 필요",
        "플러그인명": display_name(manifest),
        "한 줄 설명": description,
        "사용 상황": usage,
        "주요 기능": skill_descriptions or description,
        "대표 스킬": skill_names,
        "계정 연결": "확인 필요",
        "비용/플랜": "확인 필요",
        "주의사항": f"로컬 설치 플러그인에서 자동 감지됨: {plugin_root}",
        "source_path": str(plugin_root),
        "manifest_name": manifest.get("name", ""),
        "detected_at": timestamp(),
    }
