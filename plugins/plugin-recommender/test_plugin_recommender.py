import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent / "skills" / "plugin-recommender" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from plugin_recommender import recommend_plugins  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
