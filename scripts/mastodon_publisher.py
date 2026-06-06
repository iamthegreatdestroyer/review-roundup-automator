#/usr/bin/env python3
"""
Mastodon Publisher for review-roundup-automator
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

MASTODON_INSTANCE = os.getenv("MASTODON_INSTANCE", "https://mastodon.social")
MASTODON_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")

def post_to_mastodon(status: str, visibility: str = "public") -> dict | None:
    if not MASTODON_TOKEN:
        print("[Mastodon] No token.")
        return None

    url = f"{MASTODON_INSTANCE}/api/v1/statuses"
    headers = {"Authorization": f"Bearer {MASTODON_TOKEN}", "Content-Type": "application/json"}
    payload = {"status": status, "visibility": visibility}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=20)
        resp.raise_for_status()
        print(f"[Mastodon] Posted: {resp.json().get('url')}")
        return resp.json()
    except Exception as e:
        print(f"[Mastodon] Failed: {e}")
        return None

def create_teaser(topic: str, url: str) -> str:
    return f"New roundup: {topic}\n\n{url}\n#reviews #tools"