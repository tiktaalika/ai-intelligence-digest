from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from .dummy_data import make_dummy_records
from .models import RepoRecord
from .scoring import RankedRepo, rank_records
from .storage import append_records, read_records


@dataclass(frozen=True)
class Period:
    label: str
    start: date
    end: date
    output_dir: Path
    top_n: int


def weekly_period(settings, today: date | None = None) -> Period:
    end = today or date.today()
    start = end - timedelta(days=7)
    return Period("weekly", start, end, settings.reports_weekly_dir, int(settings.raw.get("reporting", {}).get("weekly_top_n", 20)))


def monthly_period(settings, today: date | None = None) -> Period:
    end = today or date.today()
    first_this_month = end.replace(day=1)
    previous_end = first_this_month - timedelta(days=1)
    previous_start = previous_end.replace(day=1)
    return Period(
        "monthly",
        previous_start,
        previous_end,
        settings.reports_monthly_dir,
        int(settings.raw.get("reporting", {}).get("monthly_top_n", 30)),
    )


def generate_report(settings, period: Period, logger) -> Path:
    records = read_records(settings.repos_jsonl)
    if not records:
        logger.warning("No normalized records found; adding dummy records for example report.")
        records = make_dummy_records(period.end)
        append_records(settings.repos_jsonl, records)

    ranked = rank_records(records, period.start, period.end, settings.scoring)
    if not ranked:
        logger.warning("No records available for %s; adding dummy records.", period.label)
        records = make_dummy_records(period.end)
        append_records(settings.repos_jsonl, records)
        ranked = rank_records(records, period.start, period.end, settings.scoring)

    period.output_dir.mkdir(parents=True, exist_ok=True)
    report_path = period.output_dir / f"{period.end.isoformat()}-{period.label}-github-trends.md"
    report_path.write_text(render_markdown(settings, period, ranked), encoding="utf-8")
    return report_path


def render_markdown(settings, period: Period, ranked: list[RankedRepo]) -> str:
    top_n = period.top_n
    growth_ranked = sorted(ranked, key=lambda item: (item.stars_gained, item.trend_score), reverse=True)
    stars_ranked = sorted(ranked, key=lambda item: (item.record.stars, item.stars_gained), reverse=True)

    lines: list[str] = []
    lines.append(f"# GitHub {period.label.title()} Trend Report")
    lines.append("")
    lines.append(f"Period: {period.start.isoformat()} to {period.end.isoformat()}")
    lines.append("")
    lines.append("Scoring formula:")
    lines.append("")
    lines.append(
        "`trend_score = "
        f"{settings.scoring.get('normalized_star_growth', 0.55)} * normalized_star_growth + "
        f"{settings.scoring.get('normalized_total_stars', 0.25)} * normalized_total_stars + "
        f"{settings.scoring.get('normalized_recent_activity', 0.10)} * normalized_recent_activity + "
        f"{settings.scoring.get('normalized_fork_growth', 0.10)} * normalized_fork_growth`"
    )
    lines.append("")
    lines.append("If live collection was unavailable, fallback rows are marked with `dummy` as the source.")
    lines.append("")

    lines.append("## Overall Ranking")
    lines.extend(repo_table(ranked[:top_n], include_score=True))
    lines.append("")

    lines.append("## Core Metrics")
    lines.append("")
    lines.append("### Fastest-Growing Repositories")
    lines.extend(repo_table(growth_ranked[:top_n], include_score=False))
    lines.append("")
    lines.append("### Highest Total Stars")
    lines.extend(repo_table(stars_ranked[:top_n], include_score=False))
    lines.append("")

    lines.append("## Category Rankings")
    for category in settings.categories:
        lines.append("")
        lines.append(f"### {category}")
        category_rows = [item for item in ranked if item.record.category == category or category in item.record.matched_categories]
        if not category_rows:
            lines.append("")
            lines.append("No repositories discovered for this category in the current data.")
            continue
        lines.append("")
        lines.append("#### Top by Star Growth")
        lines.extend(repo_table(sorted(category_rows, key=lambda item: item.stars_gained, reverse=True)[:10], include_score=True))
        lines.append("")
        lines.append("#### Top by Total Stars")
        lines.extend(repo_table(sorted(category_rows, key=lambda item: item.record.stars, reverse=True)[:10], include_score=True))
        lines.append("")
        lines.append("#### Newly Emerging")
        emerging = emerging_rows(settings, category_rows)
        lines.extend(repo_table(emerging[:10], include_score=True) if emerging else ["", "No emerging low-star/high-growth repositories found."])
    lines.append("")

    lines.append("## Author / Organization Ranking")
    lines.extend(author_table(ranked))
    lines.append("")
    lines.append("## Collection Notes")
    lines.append("")
    lines.append("- Raw snapshots are stored in `data/snapshots/`.")
    lines.append("- Normalized records are appended to `data/repos.jsonl`.")
    lines.append("- Errors are logged to `data/logs/trend_report.log`.")
    return "\n".join(lines) + "\n"


def repo_table(rows: list[RankedRepo], include_score: bool) -> list[str]:
    headers = [
        "Rank",
        "Repository",
        "Description",
        "Language",
        "Stars",
        "Stars Gained",
        "Forks",
        "Last Update",
        "Category",
        "Author/Org",
    ]
    if include_score:
        headers.append("Trend Score")
    headers.append("Source")
    lines = ["", "| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for idx, item in enumerate(rows, start=1):
        record = item.record
        row = [
            str(idx),
            f"[{record.full_name}]({record.url})",
            clean_cell(record.description),
            record.language or "-",
            str(record.stars),
            str(item.stars_gained),
            str(record.forks),
            record.last_update or "-",
            record.category,
            record.author,
        ]
        if include_score:
            row.append(f"{item.trend_score:.4f}")
        row.append(record.source)
        lines.append("| " + " | ".join(row) + " |")
    return lines


def emerging_rows(settings, rows: list[RankedRepo]) -> list[RankedRepo]:
    max_stars = int(settings.raw.get("reporting", {}).get("emerging_max_total_stars", 2500))
    min_growth = int(settings.raw.get("reporting", {}).get("emerging_min_growth", 5))
    emerging = [item for item in rows if item.record.stars <= max_stars and item.stars_gained >= min_growth]
    emerging.sort(key=lambda item: (item.stars_gained, -item.record.stars), reverse=True)
    return emerging


def author_table(rows: list[RankedRepo]) -> list[str]:
    grouped: dict[str, list[RankedRepo]] = defaultdict(list)
    for item in rows:
        grouped[item.record.author].append(item)
    summary = []
    for author, author_rows in grouped.items():
        repo_count = len({item.record.full_name for item in author_rows})
        total_stars = sum(item.record.stars for item in author_rows)
        growth = sum(item.stars_gained for item in author_rows)
        appearances = len(author_rows)
        categories = sorted({item.record.category for item in author_rows})
        note = f"Relevant across {', '.join(categories[:3])}." if categories else "Relevant repository owner."
        summary.append((author, repo_count, total_stars, growth, appearances, note))
    summary.sort(key=lambda item: (item[3], item[2], item[1]), reverse=True)

    lines = [
        "",
        "| Rank | Author/Org | Relevant Repos | Total Stars | Star Growth | Ranking Appearances | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for idx, (author, repo_count, total_stars, growth, appearances, note) in enumerate(summary[:20], start=1):
        lines.append(f"| {idx} | {author} | {repo_count} | {total_stars} | {growth} | {appearances} | {note} |")
    return lines


def clean_cell(value: str) -> str:
    value = (value or "").replace("\n", " ").replace("|", "/").strip()
    if len(value) > 110:
        return value[:107] + "..."
    return value or "-"
