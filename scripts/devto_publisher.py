#!/usr/bin/env python3
"""
Dev.to Publisher for review-roundup-automator

Publishes generated review/roundup articles to Dev.to.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

DEVTO_API_KEY = os.getenv("DEVTO_API_KEY")
DEVTO_API_URL = "https://dev.to/api/articles"


def publish_to_devto(
    title: str,
    body_markdown: str,
    tags: list[str] | None = None,
    canonical_url: str | None = None,
    published: bool = True
) -> dict | None:
    if not DEVTO_API_KEY:
        print("[Dev.to] DEVTO_API_KEY not set. Skipping.")
        return None

    if tags is None:
        tags = ["reviews", "productivity", "tools"]

    payload = {
        "article": {
            "title": title,
            "body_markdown": body_markdown,
            "published": published,
            "tags": tags,
        }
    }
    if canonical_url:
        payload["article"]["canonical_url"] = canonical_url

    headers = {"api-key": DEVTO_API_KEY, "Content-Type": "application/json"}

    try:
        resp = requests.post(DEVTO_API_URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        article = resp.json()
        print(f"[Dev.to] Published: {article.get('url')}")
        return article
    except Exception as e:
        print(f"[Dev.to] Publish failed: {e}")
        return None
