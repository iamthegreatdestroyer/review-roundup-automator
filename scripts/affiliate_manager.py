#!/usr/bin/env python3
"""
Centralized Affiliate Link Manager (shared across projects)

Usage:
    from scripts.affiliate_manager import get_affiliate_url, inject_affiliates
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
AFFILIATES_FILE = ROOT / "data" / "affiliates.json"

_affiliates_cache = None


def load_affiliates() -> dict:
    global _affiliates_cache
    if _affiliates_cache is None:
        if AFFILIATES_FILE.exists():
            with open(AFFILIATES_FILE) as f:
                _affiliates_cache = json.load(f)
        else:
            _affiliates_cache = {}
    return _affiliates_cache


def get_affiliate_url(tool_name: str) -> str | None:
    affiliates = load_affiliates()
    key = tool_name.lower().strip()

    if key in affiliates:
        return affiliates[key]

    variations = {
        "notion": "notion",
        "obsidian": "obsidian",
        "anytype": "anytype",
        "logseq": "logseq",
        "bitwarden": "bitwarden",
    }
    for variant, canonical in variations.items():
        if variant in key and canonical in affiliates:
            return affiliates[canonical]

    return None


def inject_affiliates(markdown: str) -> str:
    affiliates = load_affiliates()
    if not affiliates:
        return markdown

    result = markdown

    tool_patterns = [
        (r"\bNotion\b", affiliates.get("notion")),
        (r"\bObsidian\b", affiliates.get("obsidian")),
        (r"\bAnytype\b", affiliates.get("anytype")),
        (r"\bLogseq\b", affiliates.get("logseq")),
        (r"\bBitwarden\b", affiliates.get("bitwarden")),
        (r"\bMattermost\b", affiliates.get("mattermost")),
    ]

    for pattern, url in tool_patterns:
        if url:
            result = re.sub(pattern, f"[{pattern[2:-2]}]({url})", result, count=1)

    return result


def get_affiliate_disclosure() -> str:
    return "\n\n*Some links in this article are affiliate links. If you make a purchase through them, I may earn a small commission at no extra cost to you.*"
