from __future__ import annotations

from collections import Counter


def classify_repo(repo: dict, categories: dict[str, dict[str, list[str]]]) -> tuple[str, list[str]]:
    text_parts = [
        repo.get("full_name", ""),
        repo.get("name", ""),
        repo.get("description", ""),
        repo.get("language", ""),
        " ".join(repo.get("topics") or []),
    ]
    text = " ".join(str(part).lower() for part in text_parts if part)
    scores: Counter[str] = Counter()
    for category, config in categories.items():
        for keyword in config.get("keywords", []):
            keyword_l = keyword.lower()
            if keyword_l in text:
                scores[category] += 2 if " " in keyword_l else 1

    if not scores:
        return "Unclassified", []
    ranked = [category for category, _ in scores.most_common()]
    return ranked[0], ranked
