# Plugin Recommender

Codex에서 작업을 시작하기 전에 “이 작업에는 어떤 플러그인이나 스킬을 쓰면 좋을까?”를 추천해주는 로컬 Codex 플러그인입니다.

예를 들어 아래처럼 물어볼 수 있습니다.

```text
@plugin-recommender PDF를 읽고 엑셀 표로 정리해줘
```

그러면 `PDF`, `Spreadsheets`, `Documents`처럼 작업에 맞는 후보와 추천 이유를 한국어로 알려줍니다.

## 설치 방법

Codex 앱에서:

1. **Plugins**를 엽니다.
2. **Add plugin marketplace** 또는 **플러그인 마켓플레이스 추가**를 누릅니다.
3. 아래 값을 입력합니다.

```text
Source: munkm1109-lang/plugin-recommender
Git ref: main
Sparse path: 비워두기
```

4. marketplace를 추가합니다.
5. Plugin Directory에서 **Plugin Recommender**를 찾아 설치합니다.
6. 새 Codex thread를 열어 사용합니다.

만약 Sparse path 입력이 필요하다고 나오면 아래처럼 두 줄을 입력하세요.

```text
.agents/plugins
plugins
```

## CLI 설치

Codex CLI를 쓰는 경우:

```powershell
codex plugin marketplace add munkm1109-lang/plugin-recommender --ref main
codex plugin add plugin-recommender@plugin-recommender-marketplace
```

## 사용 예시

플러그인 추천이 필요한 작업에서는 자동으로 추천이 제안될 수 있습니다.

예를 들어:

```text
깃에 배포해줘
```

Codex는 작업에 맞는 플러그인을 먼저 추천하고, 바로 실행하지 않고 확인을 요청합니다.

```text
이 작업에는 GitHub 플러그인이 저장소 관리와 배포 흐름에 적합합니다.
GitHub 플러그인을 사용하시겠습니까?
```

사용자가 `Yes`, `승인`, `좋아`, `진행`처럼 명확히 승인한 뒤에만 추천 플러그인 사용을 이어갑니다.

추천된 플러그인이 설치되어 있지 않거나 외부 계정 연결이 필요한 경우에는, 먼저 설치 또는 연결을 요청하고 사용자가 연결 완료를 알려준 뒤 작업을 이어갑니다.

명시적으로 추천만 받고 싶다면 아래처럼 호출할 수 있습니다.

```text
@plugin-recommender PDF를 읽고 엑셀 표로 정리해줘
```

```text
@plugin-recommender 제안서를 PPT 발표자료로 만들어줘
```

```text
@plugin-recommender GitHub PR 리뷰에 맞는 플러그인을 추천해줘
```

환경에 따라 `$` 호출을 쓰는 경우에는 아래처럼 사용할 수도 있습니다.

```text
$plugin-recommender PDF를 읽고 엑셀 표로 정리해줘
```

## 로컬 플러그인 스캔

설치된 플러그인이 카탈로그에 아직 없다면, 아래처럼 말해서 로컬 플러그인 목록을 새로 스캔할 수 있습니다.

```text
@plugin-recommender 플러그인 스캔 ㄱㄱ
```

또는:

```text
@plugin-recommender 새로운 플러그인 설치됐어
```

내부적으로는 설치된 플러그인의 manifest와 skill 설명을 읽어서, 기존 카탈로그에 없는 플러그인만 로컬 overlay catalog에 추가합니다. 기본 제공 카탈로그 파일은 수정하지 않습니다.

로컬 overlay 위치:

```text
%USERPROFILE%\.codex\plugin-recommender\local_catalog_overlay.json
```

CLI로 직접 실행할 수도 있습니다.

```powershell
python "<plugin-recommender skill path>\scripts\plugin_recommender.py" --refresh-local
python "<plugin-recommender skill path>\scripts\plugin_recommender.py" --list-local-plugins
```

## 추천 결과에 포함되는 정보

- 추천 플러그인 또는 스킬
- 추천 이유
- 계정 연결 필요 여부
- 비용/플랜 주의사항
- 사용 시 참고할 점

## 주의사항

- 이 플러그인은 OpenAI 공식 Plugin Directory에 등록된 공식 플러그인이 아닙니다.
- 현재는 GitHub marketplace를 통해 설치하는 베타 버전입니다.
- 포함된 플러그인 카탈로그는 특정 시점의 스냅샷이라 최신 Codex 플러그인 전체를 보장하지 않습니다.
- 로컬 스캔은 사용자의 PC에 설치된 플러그인 metadata를 읽어 개인 overlay catalog에 저장합니다.
- 사용자의 프롬프트나 사용 기록을 개발자에게 전송하지 않습니다.
- 외부 계정 연결 없이 로컬에서 추천 스크립트를 실행합니다.

## Repository 구조

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
          catalog_data.py
          local_catalog.py
          local_catalog_common.py
          local_catalog_extract.py
          local_catalog_scan.py
          plugin_recommender.py
          plugin_recommender_cli.py
          plugin_recommender_output.py
          scoring.py
          Codex_플러그인_카탈로그_KR.csv.gz
```

## 피드백

추천이 틀렸거나 빠진 플러그인이 있으면 GitHub Issue로 알려주세요.

Issue에 아래 내용을 적어주면 개선에 도움이 됩니다.

- 입력한 작업 내용
- 추천된 플러그인
- 추천이 맞았는지 여부
- 빠졌다고 생각하는 플러그인
