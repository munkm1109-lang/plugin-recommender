# Plugin Recommender Marketplace

Plugin Recommender is a Codex plugin that recommends useful Codex plugins and skills for a task.

It uses a bundled Korean plugin catalog snapshot and returns recommendations with:

- recommended plugin or skill
- reason for recommendation
- account connection caveats
- cost or plan caveats
- usage notes

## Install In Codex

In the Codex app:

1. Open **Plugins**.
2. Select **Add plugin marketplace**.
3. Fill in:

```text
Source: github.com/<owner>/<repo>
Git ref: main
Sparse path: .
```

4. Add the marketplace.
5. Find **Plugin Recommender** in the plugin directory.
6. Install it.
7. Start a new Codex thread.

Replace `<owner>/<repo>` with this GitHub repository path after publishing.

## CLI Install

```powershell
codex plugin marketplace add <owner>/<repo> --ref main
codex plugin add plugin-recommender@plugin-recommender-marketplace
```

## Usage

Use the plugin explicitly:

```text
@plugin-recommender PDF를 읽고 엑셀 표로 정리해줘
```

or:

```text
$plugin-recommender 제안서를 PPT 발표자료로 만들어줘
```

## Notes

- This is a local Codex plugin marketplace package, not an official OpenAI Plugin Directory listing.
- The bundled catalog is a snapshot and may not include every current Codex plugin.
- The plugin does not send usage data or prompts to the publisher.
- GitHub traffic, clone counts, stars, and release downloads can be used to estimate interest.

## Repository Structure

```text
marketplace.json
plugins/
  plugin-recommender/
    .codex-plugin/
      plugin.json
    skills/
      plugin-recommender/
        SKILL.md
        agents/
          openai.yaml
        scripts/
          plugin_recommender.py
          Codex_플러그인_카탈로그_KR.csv
```

## Feedback

Please open a GitHub issue with:

- the task you tried
- the recommended plugins
- whether the recommendation was useful
- missing plugins or wrong recommendations
