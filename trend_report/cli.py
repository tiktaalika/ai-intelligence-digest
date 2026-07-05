from __future__ import annotations

import argparse

from .collectors import collect
from .config import load_settings
from .logging_utils import configure_logging
from .reports import generate_report, monthly_period, weekly_period
from .storage import append_records, ensure_dirs


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Monitor GitHub repository trends and generate Markdown reports.")
    parser.add_argument("command", choices=["collect", "weekly", "monthly", "all"])
    parser.add_argument("--config", default=None, help="Path to YAML config. Defaults to config/trend_report.yaml.")
    args = parser.parse_args(argv)

    settings = load_settings(args.config)
    ensure_dirs([settings.snapshots_dir, settings.reports_weekly_dir, settings.reports_monthly_dir, settings.log_file.parent])
    logger = configure_logging(settings.log_file)

    if args.command in {"collect", "all"}:
        records = collect(settings, logger)
        append_records(settings.repos_jsonl, records)
        logger.info("Wrote %s normalized records to %s", len(records), settings.repos_jsonl)
        print(f"Collected {len(records)} repositories")
        print(f"Normalized records: {settings.repos_jsonl}")

    if args.command in {"weekly", "all"}:
        path = generate_report(settings, weekly_period(settings), logger)
        logger.info("Generated weekly report at %s", path)
        print(f"Weekly report: {path}")

    if args.command in {"monthly", "all"}:
        path = generate_report(settings, monthly_period(settings), logger)
        logger.info("Generated monthly report at %s", path)
        print(f"Monthly report: {path}")
