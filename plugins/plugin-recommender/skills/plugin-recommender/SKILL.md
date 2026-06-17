---
name: plugin-recommender
description: Recommend relevant Codex plugins and skills from the local Korean plugin catalog. Use only when the user explicitly invokes this skill, such as @plugin-recommender, @plugin, @skill, or asks to recommend plugins/skills for a specific task.
---

# Plugin Recommender

Use this skill to recommend Codex plugins or skills for a user task from the local catalog.

## Workflow

1. Identify the user's task text after the explicit invocation.
2. Run the bundled recommender script with the task text.
3. Return the top recommendations in Korean.
4. Include caveats from the output: account connection, cost/plan, and notes.
5. Do not treat the recommendation as mandatory; choose the final tool or plugin based on task fit and available capabilities.

## Command

Run from any directory:

```powershell
python "<skill-dir>\scripts\plugin_recommender.py" "<user task>" --top-k 5
```

For machine-readable output:

```powershell
python "<skill-dir>\scripts\plugin_recommender.py" "<user task>" --top-k 5 --json
```

Resolve `<skill-dir>` to the directory containing this `SKILL.md`. On a default Windows install, that is usually `%USERPROFILE%\.codex\skills\plugin-recommender`.

## Output Guidance

Summarize the result as:

- 추천 플러그인/스킬
- 추천 이유
- 계정 연결 필요 여부
- 비용/플랜 주의사항
- 실제 사용 여부 판단

If no recommendation is found, ask for a more specific task description or fall back to the catalog file in `scripts/Codex_플러그인_카탈로그_KR.csv`.
