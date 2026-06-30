#!/usr/bin/env python3
"""Render the rolling AI news digest as a static HTML page."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DIGEST_DIR = ROOT / "data" / "digests"
SITE_DIR = ROOT / "site"
OUT = SITE_DIR / "index.html"
SUMMARY_CACHE = DIGEST_DIR / "site_summaries.json"
COMMON_EVENT_WORDS = {
    "a", "an", "and", "as", "at", "by", "for", "from", "in", "into", "is", "it", "its",
    "new", "of", "on", "or", "s", "says", "the", "to", "with", "report", "reports",
    "reported", "exclusive", "breaking", "news", "via",
}
SOURCE_SUFFIXES = {
    "reuters", "bbc", "cnbc", "forbes", "techcrunch", "bloomberg", "wsj", "financial",
    "times", "guardian", "yahoo", "finance", "ap", "axios", "nytimes", "meta", "openai",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def candidate_dates() -> list[str]:
    dates = []
    for path in DIGEST_DIR.glob("*-candidates.json"):
        match = re.match(r"(\d{4}-\d{2}-\d{2})-candidates\.json$", path.name)
        if match:
            dates.append(match.group(1))
    return sorted(set(dates), reverse=True)


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def format_date(date_slug: str) -> str:
    try:
        return datetime.strptime(date_slug, "%Y-%m-%d").strftime("%A, %B %d, %Y")
    except ValueError:
        return date_slug


def markdown_to_html(markdown: str) -> str:
    """Small markdown subset for stored final digests."""
    lines = []
    in_list = False
    for raw in markdown.splitlines():
        line = raw.strip()
        if not line:
            if in_list:
                lines.append("</ul>")
                in_list = False
            continue
        if line.startswith("**") and line.endswith("**"):
            if in_list:
                lines.append("</ul>")
                in_list = False
            lines.append(f"<h3>{esc(line.strip('*'))}</h3>")
        elif re.match(r"^\d+\.\s", line):
            if in_list:
                lines.append("</ul>")
                in_list = False
            lines.append(f"<p class=\"numbered\">{linkify(esc(line))}</p>")
        elif line.startswith("- "):
            if not in_list:
                lines.append("<ul>")
                in_list = True
            lines.append(f"<li>{linkify(esc(line[2:]))}</li>")
        else:
            if in_list:
                lines.append("</ul>")
                in_list = False
            lines.append(f"<p>{linkify(esc(line))}</p>")
    if in_list:
        lines.append("</ul>")
    return "\n".join(lines)


def linkify(text: str) -> str:
    # The markdown is already escaped, so only recover simple [label](url) links.
    pattern = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
    return pattern.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', text)


def canonical_category(category: str) -> str:
    if category in {"engineering_ai", "cae_ai_engineering"}:
        return "engineering_ai"
    return category


def parse_final_sections(markdown: str) -> dict[str, list[dict[str, str]]]:
    sections = {"general_ai": [], "engineering_ai": []}
    current: str | None = None
    pending: dict[str, str] | None = None
    item_re = re.compile(r"^\d+\.\s+(.+?)。原文：\[([^\]]+)\]\((https?://[^)]+)\)")
    rich_item_re = re.compile(r"^\d+\.\s+\*\*(.+?)\*\*\s*$")
    source_re = re.compile(r"^English source:\s+\[([^\]]+)\]\((https?://[^)]+)\)")
    for raw in markdown.splitlines():
        line = raw.strip()
        normalized_heading = line.strip("# ").strip()
        if normalized_heading in {"**AI Top 10**", "**Top 10 General AI News**", "Top 10 General AI News"}:
            current = "general_ai"
            pending = None
            continue
        if normalized_heading in {
            "**CAE / AI for Engineering Top 5**",
            "**Top 5 Engineering AI News**",
            "Top 5 Engineering AI News",
        }:
            current = "engineering_ai"
            pending = None
            continue
        if normalized_heading in {"Research Radar", "Watchlist Updates", "Why It Matters", "Audit Note"}:
            current = None
            pending = None
            continue
        if line.startswith("**") and line.endswith("**"):
            current = None
            pending = None
            continue
        match = item_re.match(line)
        if current and match:
            headline, source_label, url = match.groups()
            sections[current].append(
                {
                    "headline": headline,
                    "source_label": source_label,
                    "url": url,
                }
            )
            pending = None
            continue
        rich_match = rich_item_re.match(line)
        if current and rich_match:
            pending = {"headline": rich_match.group(1)}
            continue
        source_match = source_re.match(line)
        if current and pending and source_match:
            source_label, url = source_match.groups()
            sections[current].append(
                {
                    "headline": pending["headline"],
                    "source_label": source_label,
                    "url": url,
                }
            )
            pending = None
    return sections


def find_candidate_by_url(data: dict[str, Any], url: str) -> dict[str, Any] | None:
    for key in ("top_100_news_candidates", "top_10_general_ai", "top_5_engineering_ai", "top_5_cae_ai_engineering"):
        for item in data.get(key, []):
            if item.get("url") == url:
                return item
    return None


def hydrate_final_items(data: dict[str, Any], final_path: Path) -> dict[str, list[dict[str, Any]]]:
    parsed = parse_final_sections(final_path.read_text(encoding="utf-8"))
    hydrated: dict[str, list[dict[str, Any]]] = {"general_ai": [], "engineering_ai": []}
    for category, rows in parsed.items():
        for row in rows:
            candidate = find_candidate_by_url(data, row["url"]) or {}
            item = dict(candidate)
            item["url"] = row["url"]
            item["source"] = candidate.get("source") or row["source_label"]
            item["title"] = candidate.get("title") or row["source_label"]
            item["zh_summary"] = row["headline"]
            item["category"] = category
            hydrated[category].append(item)
    return hydrated


def event_tokens(title: str) -> set[str]:
    title = re.sub(r"\s+-\s+[^-]+$", "", title.lower())
    return {
        token
        for token in re.findall(r"[a-z0-9]+", title)
        if len(token) > 2 and token not in COMMON_EVENT_WORDS and token not in SOURCE_SUFFIXES
    }


def canonical_event_key(title: str) -> str | None:
    text = title.lower()
    if "openai" in text and any(term in text for term in ("ipo", "initial public", "go public", "public offering", "stock market", "s-1", "sec")):
        return "openai-ipo"
    if "openai" in text and any(term in text for term in ("price cut", "price cuts", "slashing prices", "drastic price")) and "anthropic" in text:
        return "openai-anthropic-price-war"
    if "visa" in text and any(term in text for term in ("openai", "chatgpt")) and any(term in text for term in ("payment", "payments", "agentic commerce", "ai agent")):
        return "visa-openai-agent-payments"
    if "mastercard" in text and any(term in text for term in ("ai agent", "agent payments", "agentic commerce", "micropayments", "machine-to-machine", "coinbase", "ripple", "onchain")):
        return "mastercard-ai-agent-payments"
    if "microsoft" in text and "claude" in text and any(term in text for term in ("fable", "employee access", "data retention", "data terms", "restricts", "limited")):
        return "microsoft-claude-fable-access"
    if "anthropic" in text and any(term in text for term in ("regulation", "government", "block dangerous", "stronger regulation")):
        return "anthropic-regulation-call"
    if "anthropic" in text and any(term in text for term in ("walks back", "backlash", "restrictions", "sabotaged")):
        return "anthropic-model-restrictions-backlash"
    if "anthropic" in text and any(term in text for term in ("export control", "foreign access", "government order", "taken offline", "shuts down", "suspended", "security fears", "pulled the plug")):
        return "anthropic-export-controls-model-access"
    if "apple" in text and "siri" in text:
        return "apple-siri-ai"
    if "openai" in text and "data center" in text and any(term in text for term in ("ohio", "gigawatt", "nvidia")):
        return "openai-ohio-data-center"
    if "meta" in text and "reliance" in text and "data center" in text:
        return "meta-reliance-india-data-center"
    if "thea energy" in text and any(term in text for term in ("helios", "fusion", "surrogate", "digital twin")):
        return "thea-energy-fusion-digital-twin"
    if "synera" in text and "nvidia" in text and any(term in text for term in ("engineering simulation", "design")):
        return "synera-nvidia-engineering-agents"
    if "simcenter physicsai" in text and "cfd" in text:
        return "siemens-simcenter-physicsai-cfd"
    return None


def is_same_event(left: dict[str, Any], right: dict[str, Any]) -> bool:
    left_key = canonical_event_key(left.get("title", ""))
    right_key = canonical_event_key(right.get("title", ""))
    if left_key and left_key == right_key:
        return True
    left_tokens = event_tokens(left.get("title", ""))
    right_tokens = event_tokens(right.get("title", ""))
    if not left_tokens or not right_tokens:
        return False
    intersection = left_tokens & right_tokens
    smaller = min(len(left_tokens), len(right_tokens))
    union = left_tokens | right_tokens
    if len(intersection) >= 5 and len(intersection) / max(smaller, 1) >= 0.5:
        return True
    if len(intersection) >= 4 and len(intersection) / max(len(union), 1) >= 0.42:
        return True
    return False


def topic_key(item: dict[str, Any]) -> str:
    text = f"{item.get('title', '')} {item.get('text', '')}".lower()
    if any(term in text for term in ("payment", "payments", "agentic commerce", "wallet", "checkout", "stablecoin", "micropayment")):
        return "payments_agent_commerce"
    if any(term in text for term in ("regulation", "policy", "law", "senate", "washington", "government", "safety", "data retention", "data terms")):
        return "policy_safety_governance"
    if any(term in text for term in ("data center", "datacenter", "compute", "gpu", "chip", "nvidia", "oracle", "power grid", "energy")):
        return "infrastructure_compute"
    if any(term in text for term in ("coding", "developer", "software engineering", "ai-native development", "programming")):
        return "software_development"
    if any(term in text for term in ("health", "medical", "medicine", "clinical", "hospital", "drug discovery")):
        return "health_bio"
    if any(term in text for term in ("robot", "robotics", "autonomous vehicle", "drone")):
        return "robotics_autonomy"
    if any(term in text for term in ("model", "claude", "chatgpt", "openai", "anthropic", "deepmind", "llm", "benchmark")):
        return "frontier_models"
    if canonical_category(item.get("category", "")) == "engineering_ai":
        if any(term in text for term in ("cfd", "fea", "cae", "simulation", "surrogate", "digital twin", "neural operator")):
            return "cae_simulation"
    return "other"


def is_excluded(item: dict[str, Any], category: str) -> bool:
    if canonical_category(category) != "engineering_ai":
        return False
    text = f"{item.get('title', '')} {item.get('source', '')} {item.get('text', '')}".lower()
    excluded_terms = {
        "analysts offer insights",
        "industrial goods companies",
        "tsx:cae",
        "forex.com",
        "ai index cfd",
        "capital.com",
        "tradingview",
        "finance magnates",
        "traders",
        "trading",
        "brokers",
        "cfd access",
        "surrogate model virus",
        "chatbots in a simulation",
        "ended the world",
    }
    return any(term in text for term in excluded_terms)


def select_unique(items: list[dict[str, Any]], category: str, limit: int) -> list[dict[str, Any]]:
    category = canonical_category(category)
    max_per_topic = 2
    selected: list[dict[str, Any]] = []
    topic_counts: dict[str, int] = {}
    for item in items:
        if canonical_category(item.get("category", "")) != category:
            continue
        if is_excluded(item, category):
            continue
        if any(is_same_event(item, existing) for existing in selected):
            continue
        topic = topic_key(item)
        if topic_counts.get(topic, 0) >= max_per_topic:
            continue
        selected.append(item)
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
        if len(selected) == limit:
            break
    for item in items:
        if len(selected) == limit:
            break
        if canonical_category(item.get("category", "")) != category:
            continue
        if is_excluded(item, category):
            continue
        if item in selected or any(is_same_event(item, existing) for existing in selected):
            continue
        selected.append(item)
    return selected


def section_items(data: dict[str, Any], category: str, limit: int, fallback_key: str) -> list[dict[str, Any]]:
    category = canonical_category(category)
    pool = data.get("top_100_news_candidates", [])
    selected = select_unique(pool, category, limit)
    if len(selected) >= limit:
        return selected
    fallback = data.get(fallback_key, [])
    for item in fallback:
        if canonical_category(item.get("category", "")) != category:
            item = dict(item)
            item["category"] = category
        if any(is_same_event(item, existing) for existing in selected):
            continue
        selected.append(item)
        if len(selected) == limit:
            break
    return selected


def item_card(item: dict[str, Any], idx: int) -> str:
    title = esc(item.get("title", "Untitled"))
    url = esc(item.get("url", "#"))
    source = esc(item.get("source", "unknown"))
    score = esc(item.get("score", ""))
    reasons = "; ".join(item.get("score_reasons", [])[:3])
    matched = ", ".join(item.get("matched_terms", [])[:6])
    return f"""
      <article class="item">
        <div class="rank">{idx:02d}</div>
        <div>
          <h4><a href="{url}">{title}</a></h4>
          <div class="meta"><span>{source}</span><span>score {score}</span></div>
          <p class="reason">{esc(reasons)}</p>
          <p class="terms">{esc(matched)}</p>
        </div>
      </article>
    """


def render_day(date_slug: str) -> str:
    data = load_json(DIGEST_DIR / f"{date_slug}-candidates.json")
    final_path = DIGEST_DIR / f"{date_slug}-final.md"
    log = data.get("run_log", {})
    general = section_items(data, "general_ai", 10, "top_10_general_ai")
    cae = section_items(data, "engineering_ai", 5, "top_5_engineering_ai")
    search_tasks = data.get("supplemental_search_tasks", [])
    final_html = ""
    if final_path.exists():
        final_html = f"""
          <section class="final">
            <h3>中文日报</h3>
            {markdown_to_html(final_path.read_text(encoding="utf-8"))}
          </section>
        """

    search_html = ""
    if search_tasks:
        search_html = "<details class=\"search\"><summary>Supplemental search tasks</summary>" + "".join(
            f'<a href="{esc(task.get("url"))}">{esc(task.get("source"))}</a>'
            for task in search_tasks
        ) + "</details>"

    return f"""
    <section class="day" id="{date_slug}">
      <header class="day-head">
        <div>
          <p class="eyebrow">{esc(format_date(date_slug))}</p>
          <h2>{esc(date_slug)}</h2>
        </div>
        <div class="audit">
          <span>{esc(log.get("fetched_count", 0))} fetched</span>
          <span>{esc(log.get("filtered_count", 0))} candidates</span>
          <span>{len(log.get("failures", []))} failures</span>
        </div>
      </header>
      {final_html}
      <div class="columns">
        <section>
          <h3>AI Top 10</h3>
          {"".join(item_card(item, idx) for idx, item in enumerate(general, 1))}
        </section>
        <section>
          <h3>Engineering AI Top 5</h3>
          {"".join(item_card(item, idx) for idx, item in enumerate(cae, 1))}
          {search_html}
        </section>
      </div>
    </section>
    """


def load_summaries() -> dict[str, str]:
    if not SUMMARY_CACHE.exists():
        return {}
    return load_json(SUMMARY_CACHE)


def render_page() -> str:
    dates = candidate_dates()
    summaries = load_summaries()
    latest = dates[0] if dates else "No digests yet"
    nav = "".join(f'<a href="#{esc(date)}">{esc(date)}</a>' for date in dates[:20])
    days = "\n".join(render_day_with_summaries(date, summaries) for date in dates)
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Intelligence Digest</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #191815;
      --muted: #6f6a60;
      --line: #d7d0c2;
      --paper: #f8f5ee;
      --panel: #fffdf8;
      --accent: #0b6b5a;
      --accent-2: #c1492e;
      --shadow: 0 22px 70px rgba(47, 38, 24, .11);
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      font-family: Charter, "Iowan Old Style", Georgia, serif;
      background:
        linear-gradient(90deg, rgba(25,24,21,.035) 1px, transparent 1px) 0 0/38px 38px,
        linear-gradient(#fbf8f1, #eee7d8);
      color: var(--ink);
    }}
    .shell {{ max-width: 1180px; margin: 0 auto; padding: 34px 22px 80px; }}
    .hero {{
      position: sticky; top: 0; z-index: 5;
      padding: 22px 0 20px;
      backdrop-filter: blur(18px);
      background: color-mix(in srgb, var(--paper) 78%, transparent);
      border-bottom: 1px solid rgba(25,24,21,.1);
    }}
    .hero-inner {{ max-width: 1180px; margin: 0 auto; padding: 0 22px; display: grid; grid-template-columns: 1fr auto; gap: 20px; align-items: end; }}
    h1 {{ margin: 0; font-size: clamp(30px, 4vw, 56px); line-height: 1; letter-spacing: 0; font-weight: 700; }}
    .subtitle {{ margin: 12px 0 0; color: var(--muted); font-size: 17px; max-width: 680px; }}
    .stamp {{ text-align: right; font-size: 14px; color: var(--muted); }}
    .nav {{ display: flex; gap: 8px; flex-wrap: wrap; margin: 24px 0 28px; }}
    .nav a {{ color: var(--ink); border: 1px solid var(--line); padding: 7px 10px; text-decoration: none; background: rgba(255,255,255,.55); }}
    .day {{ background: var(--panel); border: 1px solid var(--line); box-shadow: var(--shadow); margin: 28px 0; padding: 24px; }}
    .day-head {{ display: flex; justify-content: space-between; gap: 20px; border-bottom: 2px solid var(--ink); padding-bottom: 16px; margin-bottom: 22px; }}
    .eyebrow {{ margin: 0 0 5px; color: var(--accent-2); font-size: 13px; text-transform: uppercase; letter-spacing: .08em; font-family: "Avenir Next", Verdana, sans-serif; }}
    h2 {{ margin: 0; font-size: 38px; }}
    h3 {{ margin: 0 0 14px; font-size: 21px; font-family: "Avenir Next", Verdana, sans-serif; }}
    .audit {{ display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; align-content: start; }}
    .audit span {{ border: 1px solid var(--line); padding: 7px 10px; color: var(--muted); font-family: "Avenir Next", Verdana, sans-serif; font-size: 13px; }}
    .columns {{ display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(300px, .85fr); gap: 24px; }}
    .item {{ display: grid; grid-template-columns: 42px 1fr; gap: 12px; padding: 15px 0; border-top: 1px solid var(--line); }}
    .rank {{ font-family: "Avenir Next", Verdana, sans-serif; color: var(--accent); font-weight: 700; }}
    h4 {{ margin: 0; font-size: 18px; line-height: 1.25; }}
    .zh-summary {{ margin: 0 0 7px; font-size: 18px; line-height: 1.38; font-weight: 700; color: var(--ink); }}
    a {{ color: var(--ink); text-decoration-color: color-mix(in srgb, var(--accent), transparent 40%); text-underline-offset: 3px; }}
    .meta {{ margin-top: 7px; display: flex; flex-wrap: wrap; gap: 8px; font-family: "Avenir Next", Verdana, sans-serif; font-size: 12px; color: var(--muted); }}
    .meta span {{ border: 1px solid var(--line); padding: 4px 7px; }}
    .reason, .terms {{ margin: 8px 0 0; color: var(--muted); font-size: 14px; line-height: 1.4; }}
    .terms {{ color: var(--accent); }}
    .final {{ border: 1px solid var(--line); background: #fbf7ed; padding: 18px; margin-bottom: 24px; }}
    .final p {{ line-height: 1.58; margin: 10px 0; }}
    .numbered {{ border-top: 1px solid var(--line); padding-top: 12px; }}
    details.search {{ margin-top: 18px; border-top: 1px solid var(--line); padding-top: 12px; }}
    details.search a {{ display: block; margin: 8px 0; color: var(--accent); }}
    @media (max-width: 860px) {{
      .hero-inner, .day-head, .columns {{ grid-template-columns: 1fr; }}
      .stamp {{ text-align: left; }}
      .day {{ padding: 18px; }}
      h2 {{ font-size: 30px; }}
    }}
  </style>
</head>
<body>
  <header class="hero">
    <div class="hero-inner">
      <div>
        <h1>AI Intelligence Digest</h1>
        <p class="subtitle">每日 General AI 与 Engineering AI 情报汇总。最新日期在最上面，向下滚动查看历史。</p>
      </div>
      <div class="stamp">Latest<br><strong>{esc(latest)}</strong><br>Generated {esc(generated)}</div>
    </div>
  </header>
  <main class="shell">
    <nav class="nav">{nav}</nav>
    {days}
  </main>
</body>
</html>
"""


def item_card_with_summary(item: dict[str, Any], idx: int, summaries: dict[str, str]) -> str:
    title = esc(item.get("title", "Untitled"))
    url = esc(item.get("url", "#"))
    source = esc(item.get("source", "unknown"))
    score = esc(item.get("score", ""))
    summary = esc(item.get("zh_summary") or summaries.get(item.get("id", ""), ""))
    reasons = "; ".join(item.get("score_reasons", [])[:2])
    summary_html = f'<p class="zh-summary">{summary}</p>' if summary else ""
    return f"""
      <article class="item">
        <div class="rank">{idx:02d}</div>
        <div>
          {summary_html}
          <h4><a href="{url}">{title}</a></h4>
          <div class="meta"><span>{source}</span><span>score {score}</span></div>
          <p class="reason">{esc(reasons)}</p>
        </div>
      </article>
    """


def render_day_with_summaries(date_slug: str, summaries: dict[str, str]) -> str:
    data = load_json(DIGEST_DIR / f"{date_slug}-candidates.json")
    final_path = DIGEST_DIR / f"{date_slug}-final.md"
    log = data.get("run_log", {})
    if final_path.exists():
        final_items = hydrate_final_items(data, final_path)
        general = final_items["general_ai"]
        cae = final_items["engineering_ai"]
    else:
        general = section_items(data, "general_ai", 10, "top_10_general_ai")
        cae = section_items(data, "engineering_ai", 5, "top_5_engineering_ai")
    search_tasks = data.get("supplemental_search_tasks", [])

    search_html = ""
    if search_tasks:
        search_html = "<details class=\"search\"><summary>Supplemental search tasks</summary>" + "".join(
            f'<a href="{esc(task.get("url"))}">{esc(task.get("source"))}</a>'
            for task in search_tasks
        ) + "</details>"

    return f"""
    <section class="day" id="{date_slug}">
      <header class="day-head">
        <div>
          <p class="eyebrow">{esc(format_date(date_slug))}</p>
          <h2>{esc(date_slug)}</h2>
        </div>
        <div class="audit">
          <span>{esc(log.get("fetched_count", 0))} fetched</span>
          <span>{esc(log.get("filtered_count", 0))} candidates</span>
          <span>{len(log.get("failures", []))} failures</span>
        </div>
      </header>
      <div class="columns">
        <section>
          <h3>AI Top 10</h3>
          {"".join(item_card_with_summary(item, idx, summaries) for idx, item in enumerate(general, 1))}
        </section>
        <section>
          <h3>Engineering AI Top 5</h3>
          {"".join(item_card_with_summary(item, idx, summaries) for idx, item in enumerate(cae, 1))}
          {search_html}
        </section>
      </div>
    </section>
    """


def main() -> int:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render_page(), encoding="utf-8")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
