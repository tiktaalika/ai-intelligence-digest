from datetime import date
import unittest

from trend_report.classifier import classify_repo
from trend_report.config import load_settings
from trend_report.dummy_data import make_dummy_records
from trend_report.scoring import rank_records
from trend_report.reports import monthly_period, weekly_period


class TrendReportTests(unittest.TestCase):
    def test_weekly_period_is_always_anchored_to_sunday(self):
        settings = load_settings()

        sunday = weekly_period(settings, date(2026, 7, 12))
        delayed_monday = weekly_period(settings, date(2026, 7, 13))

        self.assertEqual(sunday.end, date(2026, 7, 12))
        self.assertEqual(delayed_monday.end, date(2026, 7, 12))
        self.assertEqual(delayed_monday.start, date(2026, 7, 5))

    def test_monthly_period_uses_previous_month_end(self):
        settings = load_settings()
        period = monthly_period(settings, date(2026, 8, 1))

        self.assertEqual(period.start, date(2026, 7, 1))
        self.assertEqual(period.end, date(2026, 7, 31))

    def test_classifier_uses_keywords_and_topics(self):
        settings = load_settings()
        repo = {
            "full_name": "example/vector-agent",
            "description": "Multi-agent retrieval augmented generation framework",
            "topics": ["rag", "agents"],
        }

        category, matched = classify_repo(repo, settings.categories)

        self.assertIn(category, {"AI Agent", "RAG"})
        self.assertIn("AI Agent", matched)
        self.assertIn("RAG", matched)

    def test_dummy_records_rank_with_growth_hints(self):
        settings = load_settings()
        records = make_dummy_records(date(2026, 7, 5))

        ranked = rank_records(records, date(2026, 6, 28), date(2026, 7, 5), settings.scoring)

        self.assertTrue(ranked)
        self.assertGreater(ranked[0].stars_gained, 0)
        self.assertGreater(ranked[0].trend_score, 0)


if __name__ == "__main__":
    unittest.main()
