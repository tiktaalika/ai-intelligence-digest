from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class RepoRecord:
    snapshot_date: str
    full_name: str
    url: str
    description: str
    language: str
    stars: int
    forks: int
    open_issues: int
    last_update: str
    created_at: str
    pushed_at: str
    author: str
    category: str
    matched_categories: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    source: str = "unknown"
    stars_gained_hint: int = 0
    forks_gained_hint: int = 0
    source_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RepoRecord":
        allowed = cls.__dataclass_fields__.keys()
        return cls(**{key: data.get(key) for key in allowed if key in data})
