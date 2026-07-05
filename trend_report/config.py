from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "trend_report.yaml"


@dataclass(frozen=True)
class Settings:
    root: Path
    config_path: Path
    data_dir: Path
    snapshots_dir: Path
    reports_weekly_dir: Path
    reports_monthly_dir: Path
    repos_jsonl: Path
    log_file: Path
    raw: dict[str, Any]

    @property
    def categories(self) -> dict[str, dict[str, list[str]]]:
        return self.raw["categories"]

    @property
    def scoring(self) -> dict[str, float]:
        return self.raw["scoring"]


def load_settings(config_path: str | Path | None = None) -> Settings:
    path = Path(config_path) if config_path else DEFAULT_CONFIG
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    root = ROOT
    return Settings(
        root=root,
        config_path=path,
        data_dir=root / "data",
        snapshots_dir=root / "data" / "snapshots",
        reports_weekly_dir=root / "reports" / "weekly",
        reports_monthly_dir=root / "reports" / "monthly",
        repos_jsonl=root / "data" / "repos.jsonl",
        log_file=root / "data" / "logs" / "trend_report.log",
        raw=raw,
    )
