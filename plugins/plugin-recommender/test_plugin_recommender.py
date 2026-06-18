import sys
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent / "skills" / "plugin-recommender" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from local_catalog import is_refresh_request, refresh_overlay  # noqa: E402
from plugin_recommender import recommend_plugins  # noqa: E402
from plugin_recommender_output import format_added_plugins  # noqa: E402


class PluginRecommenderTests(unittest.TestCase):
    def plugin_names(self, query, top_k=5):
        return [item["plugin"] for item in recommend_plugins(query, top_k=top_k)]

    def test_pdf_to_spreadsheet_recommendations(self):
        names = self.plugin_names("PDF를 읽고 엑셀 표로 정리해줘")

        self.assertIn("PDF", names)
        self.assertIn("Spreadsheets", names)

    def test_presentation_recommendation(self):
        names = self.plugin_names("제안서를 PPT 발표자료로 만들어줘", top_k=3)

        self.assertEqual("Presentations", names[0])
        self.assertIn("Documents", names)

    def test_deployment_recommendation(self):
        names = self.plugin_names("웹앱을 GitHub repo에서 Vercel로 배포해줘")

        self.assertIn("Vercel", names)
        self.assertIn("GitHub", names)

    def test_refresh_request_detection(self):
        self.assertTrue(is_refresh_request("새로운 플러그인 설치됐어"))
        self.assertTrue(is_refresh_request("플러그인 스캔 ㄱㄱ"))
        self.assertFalse(is_refresh_request("PDF를 요약해줘"))

    def test_local_overlay_adds_only_missing_plugins(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            plugin_root = root / "demo-plugin"
            manifest_dir = plugin_root / ".codex-plugin"
            skill_dir = plugin_root / "skills" / "demo-skill"
            manifest_dir.mkdir(parents=True)
            skill_dir.mkdir(parents=True)
            (manifest_dir / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "demo-plugin",
                        "description": "Demo plugin.",
                        "interface": {
                            "displayName": "Demo Plugin",
                            "shortDescription": "Helps with demo tasks.",
                            "category": "Productivity",
                        },
                    }
                ),
                encoding="utf-8",
            )
            (skill_dir / "SKILL.md").write_text(
                "---\nname: demo-skill\ndescription: Handles demo workflows.\n---\n",
                encoding="utf-8",
            )
            overlay_path = root / "overlay.json"

            first = refresh_overlay([], scan_roots=[root], path=overlay_path)
            second = refresh_overlay([], scan_roots=[root], path=overlay_path)

            self.assertEqual(1, len(first["added"]))
            self.assertEqual("Demo Plugin", first["added"][0]["플러그인명"])
            self.assertEqual("demo-skill", first["added"][0]["대표 스킬"])
            self.assertEqual(0, len(second["added"]))
            self.assertEqual(1, len(second["rows"]))

    def test_local_overlay_ignores_fixture_plugins(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            plugin_root = root / "fixtures" / "fixture-plugin"
            manifest_dir = plugin_root / ".codex-plugin"
            manifest_dir.mkdir(parents=True)
            (manifest_dir / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "fixture-plugin",
                        "interface": {"displayName": "Fixture Plugin"},
                    }
                ),
                encoding="utf-8",
            )

            result = refresh_overlay([], scan_roots=[root], path=root / "overlay.json")

            self.assertEqual([], result["added"])
            self.assertEqual([], result["rows"])

    def test_format_added_plugins_names_new_plugins(self):
        output = format_added_plugins(
            [
                {
                    "플러그인명": "Demo Plugin",
                    "분류": "Productivity",
                    "한 줄 설명": "Helps with demo tasks.",
                    "대표 스킬": "demo-skill",
                    "source_path": "C:/demo",
                }
            ]
        )

        self.assertIn("새로 추가된 플러그인", output)
        self.assertIn("Demo Plugin", output)
        self.assertIn("demo-skill", output)


if __name__ == "__main__":
    unittest.main()
