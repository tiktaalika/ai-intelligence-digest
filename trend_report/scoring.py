from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from .models import RepoRecord
from .storage import records_by_repo


@dataclass
class RankedRepo:
    record: RepoRecord
    stars_gained: int
    forks_gained: int
    trend_score: float
    recent_activity: float


def rank_records(records: list[RepoRecord], start: date, end: date, weights: dict[str, float]) -> list[RankedRepo]:
    grouped = records_by_repo(records)
    candidates: list[tuple[RepoRecord, int, int, float]] = []
    for repo_records in grouped.values():
        latest = latest_on_or_before(repo_records, end)
        if latest is None:
            continue
        baseline = latest_on_or_before(repo_records, start)
        if baseline is None or baseline.full_name == latest.full_name and baseline.snapshot_date == latest.snapshot_date:
            stars_gained = latest.stars_gained_hint
            forks_gained = latest.forks_gained_hint
        else:
            stars_gained = max(0, latest.stars - baseline.stars)
            forks_gained = max(0, latest.forks - baseline.forks)
        recent_activity = activity_score(latest, end)
        candidates.append((latest, stars_gained, forks_gained, recent_activity))

    max_growth = max([item[1] for item in candidates] or [1])
    max_stars = max([item[0].stars for item in candidates] or [1])
    max_forks = max([item[2] for item in candidates] or [1])

    ranked: list[RankedRepo] = []
    for record, stars_gained, forks_gained, recent_activity in candidates:
        score = (
            weights.get("normalized_star_growth", 0.55) * safe_norm(stars_gained, max_growth)
            + weights.get("normalized_total_stars", 0.25) * safe_norm(record.stars, max_stars)
            + weights.get("normalized_recent_activity", 0.10) * recent_activity
            + weights.get("normalized_fork_growth", 0.10) * safe_norm(forks_gained, max_forks)
        )
        ranked.append(RankedRepo(record, stars_gained, forks_gained, round(score, 4), recent_activity))
    ranked.sort(key=lambda item: (item.trend_score, item.stars_gained, item.record.stars), reverse=True)
    return ranked


def latest_on_or_before(records: list[RepoRecord], day: date) -> RepoRecord | None:
    selected = None
    for record in records:
        record_day = date.fromisoformat(record.snapshot_date)
        if record_day <= day:
            selected = record
    return selected


def activity_score(record: RepoRecord, end: date) -> float:
    raw = record.pushed_at or record.last_update or record.snapshot_date
    raw = raw[:10]
    try:
        pushed_day = datetime.fromisoformat(raw).date()
    except ValueError:
        return 0.0
    age_days = max(0, (end - pushed_day).days)
    if age_days <= 7:
        return 1.0
    if age_days <= 30:
        return 0.7
    if age_days <= 90:
        return 0.4
    return 0.1


def safe_norm(value: int | float, max_value: int | float) -> float:
    if max_value <= 0:
        return 0.0
    return min(1.0, max(0.0, float(value) / float(max_value)))
