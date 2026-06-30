import unittest
from pathlib import Path

import yaml

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_digest_candidates import Candidate, load_source_registry, select_unique_events, topic_key  # noqa: E402


class SourceRegistryTest(unittest.TestCase):
    def test_sources_yaml_has_required_fields(self) -> None:
        registry = yaml.safe_load((ROOT / "config" / "sources.yaml").read_text(encoding="utf-8"))
        required = {"name", "url", "source_type", "category", "priority", "tags", "notes", "enabled"}
        self.assertGreater(len(registry["sources"]), 50)
        for source in registry["sources"]:
            self.assertTrue(required.issubset(source.keys()), source.get("name"))

    def test_registry_loader_normalizes_enabled_sources(self) -> None:
        registry = load_source_registry()
        self.assertIn("sources", registry)
        self.assertTrue(all(source.get("enabled", True) for source in registry["sources"]))
        self.assertTrue(any(source["category"] == "engineering_ai" for source in registry["sources"]))
        self.assertTrue(any(source["kind"] == "web_search_query" for source in registry["sources"]))

    def test_topic_diversification_limits_initial_selection(self) -> None:
        def item(idx: int, title: str, score: float) -> Candidate:
            return Candidate(
                id=str(idx),
                title=title,
                url=f"https://example.com/{idx}",
                source="test",
                source_kind="rss",
                category="general_ai",
                published_at=None,
                text=title,
                matched_terms=["AI"],
                engagement={},
                score=score,
                score_reasons=[],
            )

        candidates = [
            item(1, "Visa and OpenAI partner on AI payments", 100),
            item(2, "Mastercard launches AI agent payments", 99),
            item(3, "Stripe launches AI agent payments", 98),
            item(4, "Anthropic calls for AI regulation", 80),
            item(5, "OpenAI releases a new frontier model", 79),
        ]
        selected = select_unique_events(candidates, "general_ai", 4)
        topics = [topic_key(candidate) for candidate in selected]
        self.assertEqual(topics.count("payments_agent_commerce"), 2)
        self.assertIn("policy_safety_governance", topics)
        self.assertIn("frontier_models", topics)


if __name__ == "__main__":
    unittest.main()
