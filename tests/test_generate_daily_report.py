import unittest

from scripts.generate_daily_report import build_report, topic_label


class DailyReportTests(unittest.TestCase):
    def test_build_report_handles_empty_sections(self):
        payload = {
            "run_log": {
                "generated_at": "2026-07-10T07:02:35+00:00",
                "fetched_count": 0,
                "filtered_count": 0,
                "duplicate_count": 0,
                "source_count": 0,
                "failures": [],
            },
            "top_10_general_ai": [],
            "top_5_engineering_ai": [],
            "top_5_medical_bio_ai": [],
            "research_radar": [],
            "watchlist_updates": [],
        }

        report = build_report("2026-07-10", payload)

        self.assertIn("# AI Engineering Daily Report - 2026-07-10", report)
        self.assertIn("今日这一栏没有可发布条目", report)
        self.assertIn("## Why It Matters", report)

    def test_topic_label_prefers_cae_signals(self):
        item = {
            "title": "Open-source AI Datasets for AI Physics Model Training",
            "text": "simulation CFD surrogate model dataset",
        }

        self.assertEqual(topic_label(item), "CAE / simulation")


if __name__ == "__main__":
    unittest.main()
