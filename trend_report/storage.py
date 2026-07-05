from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from .models import RepoRecord


def ensure_dirs(paths: list[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def append_records(path: Path, records: list[RepoRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")


def read_records(path: Path) -> list[RepoRecord]:
    if not path.exists():
        return []
    records: list[RepoRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            records.append(RepoRecord.from_dict(json.loads(line)))
    return records


def latest_records_by_repo(records: list[RepoRecord]) -> dict[str, RepoRecord]:
    latest: dict[str, RepoRecord] = {}
    for record in records:
        current = latest.get(record.full_name)
        if current is None or record.snapshot_date > current.snapshot_date:
            latest[record.full_name] = record
    return latest


def records_by_repo(records: list[RepoRecord]) -> dict[str, list[RepoRecord]]:
    grouped: dict[str, list[RepoRecord]] = defaultdict(list)
    for record in records:
        grouped[record.full_name].append(record)
    for repo_records in grouped.values():
        repo_records.sort(key=lambda item: item.snapshot_date)
    return dict(grouped)
