---
name: plugin-recommender
description: Recommend relevant Codex plugins and skills for a user's task from a bundled Korean catalog. Use when a task clearly maps to a Codex plugin or external workflow, such as GitHub/repo work, deployment, browser testing, PDF/document/spreadsheet work, data analysis, dashboards, design/Figma, email, calendar, Notion, automation, or when the user asks which plugin, skill, app, connector, or tool to use.
---

# Plugin Recommender

Use this skill to recommend Codex plugins or skills for a user task from the local catalog.

## Workflow

1. Identify the user's task text.
2. Run the bundled recommender script with the task text.
3. Return the best recommendation in Korean with a short reason.
4. Include caveats from the output: account connection, cost/plan, and notes.
5. If this skill was invoked implicitly, do not execute another plugin, connector, app, or external tool immediately.
6. First ask for confirmation with this shape:

```text
이 작업에는 <plugin> 플러그인이 <reason> 때문에 적합합니다.
계정 연결: <account connection>
비용/플랜: <cost/plan>

<plugin> 플러그인을 사용하시겠습니까?
```

7. Proceed only if the user clearly answers yes, yes please, ok, 진행, 승인, 좋아, 응, or another unambiguous approval.
8. If the recommended plugin needs an external account or connector and the capability is not available, tell the user that the connection is required. Ask them to connect it, then continue after they confirm the connection is complete.
9. After approval, use the recommended plugin's available skills or tools when present. If the tool is not already available, use tool discovery when available. If no callable capability exists, explain the blocker and offer the closest safe fallback.
10. Do not treat the recommendation as mandatory; override it when the current request, available tools, or safety constraints require a better route.

## Explicit Invocation

If the user explicitly invokes `@plugin-recommender` or `$plugin-recommender`, provide recommendations directly. Ask the confirmation question only when the user is asking you to continue into execution with the recommended plugin.

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

If no recommendation is found, ask for a more specific task description or fall back to the compressed catalog file in `scripts/Codex_플러그인_카탈로그_KR.csv.gz`.
