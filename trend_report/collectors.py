from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from .classifier import classify_repo
from .dummy_data import make_dummy_records
from .models import RepoRecord


class TrendingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if not href:
            return
        parts = [part for part in href.strip("/").split("/") if part]
        if len(parts) == 2 and not any(part in {"topics", "trending", "collections"} for part in parts):
            full_name = "/".join(parts)
            if full_name not in self.links:
                self.links.append(full_name)


def collect(settings, logger) -> list[RepoRecord]:
    today = date.today().isoformat()
    raw_dir = settings.snapshots_dir / today
    raw_dir.mkdir(parents=True, exist_ok=True)

    records: dict[str, RepoRecord] = {}
    errors: list[str] = []

    try:
        for record in collect_github_search(settings, raw_dir, logger):
            records[record.full_name] = record
    except Exception as exc:  # noqa: BLE001
        logger.exception("GitHub Search collection failed")
        errors.append(f"GitHub Search: {exc}")

    for source_name, collector in [
        ("github_trending", collect_github_trending),
        ("oss_insight_trending", collect_oss_insight_trending),
        ("gitstar_ranking", collect_gitstar_ranking),
        ("star_history", collect_star_history_placeholder),
    ]:
        if not settings.raw.get("collection", {}).get("sources", {}).get(source_name, False):
            continue
        try:
            for record in collector(settings, raw_dir, logger):
                records.setdefault(record.full_name, record)
        except Exception as exc:  # noqa: BLE001
            logger.exception("%s collection failed", source_name)
            errors.append(f"{source_name}: {exc}")

    if not records and settings.raw.get("collection", {}).get("include_dummy_on_failure", True):
        logger.warning("No live records collected; writing dummy fallback records. Errors: %s", errors)
        records = {record.full_name: record for record in make_dummy_records()}

    error_path = raw_dir / "errors.json"
    error_path.write_text(json.dumps({"errors": errors}, indent=2), encoding="utf-8")
    return sorted(records.values(), key=lambda record: record.full_name.lower())


def collect_github_search(settings, raw_dir: Path, logger) -> list[RepoRecord]:
    since = (datetime.now(timezone.utc) - timedelta(days=45)).date().isoformat()
    limit = int(settings.raw.get("collection", {}).get("per_category_limit", 25))
    delay = float(settings.raw.get("collection", {}).get("request_delay_seconds", 1.0))
    headers = request_headers(settings)
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    records: dict[str, RepoRecord] = {}
    for category, config in settings.categories.items():
        keywords = config.get("keywords", [])[:6]
        per_keyword = max(3, min(10, limit // max(1, len(keywords)) + 1))
        for keyword in keywords:
            query_term = f'"{keyword}"' if " " in keyword else keyword
            query = f"{query_term} in:name,description pushed:>={since} stars:>10"
            params = urllib.parse.urlencode({"q": query, "sort": "stars", "order": "desc", "per_page": per_keyword})
            url = f"https://api.github.com/search/repositories?{params}"
            logger.info("Fetching GitHub Search for %s keyword %s", category, keyword)
            try:
                payload = get_json(url, headers, raw_dir / f"github_search_metadata_{slug(category)}_{slug(keyword)}.json")
            except Exception as exc:  # noqa: BLE001
                logger.exception("GitHub Search failed for %s keyword %s", category, keyword)
                if "rate limit" in str(exc).lower():
                    return list(records.values())
                continue
            for item in payload.get("items", []):
                record = github_item_to_record(item, settings, "github_search")
                if record.category == "Unclassified":
                    record.category = category
                    record.matched_categories = [category]
                records[record.full_name] = record
            if len([record for record in records.values() if category in record.matched_categories or record.category == category]) >= limit:
                break
            time.sleep(delay)
    return list(records.values())


def collect_github_trending(settings, raw_dir: Path, logger) -> list[RepoRecord]:
    headers = request_headers(settings)
    html = get_text("https://github.com/trending?since=weekly", headers, raw_dir / "github_trending_weekly.html")
    parser = TrendingParser()
    parser.feed(html)
    records: list[RepoRecord] = []
    for full_name in parser.links[:50]:
        category, matched = classify_repo({"full_name": full_name}, settings.categories)
        if category == "Unclassified":
            continue
        records.append(minimal_record(full_name, category, matched, "github_trending"))
    logger.info("Parsed %s relevant GitHub Trending repositories", len(records))
    return records


def collect_oss_insight_trending(settings, raw_dir: Path, logger) -> list[RepoRecord]:
    headers = request_headers(settings)
    text = get_text("https://ossinsight.io/collections/trending-repos", headers, raw_dir / "oss_insight_trending.html")
    return records_from_repo_links(text, settings, "oss_insight_trending", logger)


def collect_gitstar_ranking(settings, raw_dir: Path, logger) -> list[RepoRecord]:
    headers = request_headers(settings)
    text = get_text("https://gitstar-ranking.com/repositories", headers, raw_dir / "gitstar_ranking.html")
    return records_from_repo_links(text, settings, "gitstar_ranking", logger)


def collect_star_history_placeholder(settings, raw_dir: Path, logger) -> list[RepoRecord]:
    note = {
        "status": "not_scraped",
        "reason": "Star History is primarily useful as a visual validation source; GitHub snapshots are used for numeric growth.",
    }
    (raw_dir / "star_history_note.json").write_text(json.dumps(note, indent=2), encoding="utf-8")
    logger.info("Recorded Star History placeholder note")
    return []


def records_from_repo_links(text: str, settings, source: str, logger) -> list[RepoRecord]:
    parser = TrendingParser()
    parser.feed(text)
    records: list[RepoRecord] = []
    for full_name in parser.links[:80]:
        category, matched = classify_repo({"full_name": full_name}, settings.categories)
        if category == "Unclassified":
            continue
        records.append(minimal_record(full_name, category, matched, source))
    logger.info("Parsed %s relevant repositories from %s", len(records), source)
    return records


def github_item_to_record(item: dict[str, Any], settings, source: str) -> RepoRecord:
    category, matched = classify_repo(item, settings.categories)
    owner = item.get("owner") or {}
    return RepoRecord(
        snapshot_date=date.today().isoformat(),
        full_name=item.get("full_name", ""),
        url=item.get("html_url", ""),
        description=item.get("description") or "",
        language=item.get("language") or "",
        stars=int(item.get("stargazers_count") or 0),
        forks=int(item.get("forks_count") or 0),
        open_issues=int(item.get("open_issues_count") or 0),
        last_update=(item.get("updated_at") or "")[:10],
        created_at=item.get("created_at") or "",
        pushed_at=item.get("pushed_at") or "",
        author=owner.get("login") or item.get("full_name", "").split("/", 1)[0],
        category=category,
        matched_categories=matched,
        topics=item.get("topics") or [],
        source=source,
    )


def minimal_record(full_name: str, category: str, matched: list[str], source: str) -> RepoRecord:
    today = date.today().isoformat()
    return RepoRecord(
        snapshot_date=today,
        full_name=full_name,
        url=f"https://github.com/{full_name}",
        description="Discovered from trending source; run GitHub Search/API collection for full metadata.",
        language="",
        stars=0,
        forks=0,
        open_issues=0,
        last_update=today,
        created_at="",
        pushed_at="",
        author=full_name.split("/", 1)[0],
        category=category,
        matched_categories=matched,
        source=source,
    )


def request_headers(settings) -> dict[str, str]:
    user_agent = settings.raw.get("collection", {}).get("user_agent", "github-trend-monitor/0.1")
    return {"User-Agent": user_agent, "Accept": "application/vnd.github+json"}


def get_json(url: str, headers: dict[str, str], cache_path: Path) -> dict[str, Any]:
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {url}: {body[:300]}") from exc
    cache_path.write_text(data, encoding="utf-8")
    return json.loads(data)


def get_text(url: str, headers: dict[str, str], cache_path: Path, redirects: int = 2) -> str:
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        if exc.code in {301, 302, 303, 307, 308} and redirects > 0:
            location = exc.headers.get("Location")
            if location:
                return get_text(urllib.parse.urljoin(url, location), headers, cache_path, redirects - 1)
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {url}: {body[:300]}") from exc
    cache_path.write_text(data, encoding="utf-8")
    return data


def slug(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "_" for char in value).strip("_")
