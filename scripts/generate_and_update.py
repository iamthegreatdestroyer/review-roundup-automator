#/usr/bin/env python3
"""
Core generator for review-roundup-automator

Now includes Mastodon posting.
"""
import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from scripts.llm_client import generate
from scripts.devto_publisher import publish_to_devto
from scripts.mastodon_publisher import post_to_mastodon, create_teaser
from scripts.affiliate_manager import inject_affiliates, get_affiliate_disclosure

load_dotenv()

ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"
TEMPLATES_DIR = ROOT / "templates"
DATA_FILE = ROOT / "data" / "reviews.json"

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)


def load_topics() -> list[dict]:
    if not DATA_FILE.exists():
        return [
            {"topic": "Best Note-Taking Apps 2026", "category": "Productivity"},
            {"topic": "Best Free Project Management Tools", "category": "Collaboration"}
        ]
    with open(DATA_FILE) as f:
        return json.load(f).get("topics", [])


def generate_review_content(topic: dict) -> str:
    topic_name = topic.get("topic")
    category = topic.get("category", "Software")

    system_prompt = """You are a trusted software reviewer. Write honest, scannable roundups with clear winner recommendations. Use markdown. Be practical."""

    prompt = f"""Write a high-quality roundup for: {topic_name} ({category}).

Structure:
- Introduction
- Top tools with pros/cons
- Comparison table
- Clear winner + reasoning
- "Choose this if..." guidance
- Short conclusion

Keep ~600 words."""

    content = generate(prompt, system=system_prompt)
    content = inject_affiliates(content)
    return content


def build_pages(topics: list[dict]):
    DOCS_DIR.mkdir(exist_ok=True)
    template = env.get_template("base.html")

    (DOCS_DIR / "index.html").write_text(template.render(title="Review Roundups", content="<h1>Autonomous Reviews</h1>"))

    for topic in topics:
        content = generate_review_content(topic)
        html = template.render(
            title=topic.get("topic"),
            content=f"<h2>{topic.get('topic')}</h2>\n{content}{get_affiliate_disclosure()}"
        )
        safe = topic.get("topic", "review").lower().replace(" ", "-")[:60]
        (DOCS_DIR / f"{safe}.html").write_text(html)
        print(f"Generated: {topic.get('topic')}")


def publish_if_requested(topics: list[dict], publish_devto: bool, publish_mastodon: bool):
    if not publish_devto and not publish_mastodon:
        return
    for topic in topics[:3]:
        md_content = generate_review_content(topic)
        title = topic.get("topic")
        safe_name = title.lower().replace(" ", "-")[:60]
        page_url = f"https://iamthegreatdestroyer.github.io/review-roundup-automator/{safe_name}.html"

        if publish_devto:
            tags = ["reviews", "productivity", "tools"]
            publish_to_devto(title=title, body_markdown=md_content, tags=tags, canonical_url=page_url)

        if publish_mastodon:
            teaser = create_teaser(title, page_url)
            post_to_mastodon(teaser)


def git_commit_and_push(message: str = None):
    if message is None:
        message = f"Autonomous review update - {datetime.now().strftime('%Y-%m-%d')}"
    try:
        subprocess.run(["git", "add", "docs/"], cwd=ROOT, check=True)
        res = subprocess.run(["git", "commit", "-m", message], cwd=ROOT, capture_output=True, text=True)
        if res.returncode == 0:
            subprocess.run(["git", "push"], cwd=ROOT, check=True)
            print("Pushed.")
        else:
            print("No changes.")
    except Exception as e:
        print(f"Git error: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--publish-to-devto", action="store_true")
    parser.add_argument("--publish-to-mastodon", action="store_true")
    args = parser.parse_args()

    print("=== review-roundup-automator update ===")

    topics = load_topics()
    build_pages(topics)

    if args.publish_to_devto or args.publish_to_mastodon:
        publish_if_requested(topics, args.publish_to_devto, args.publish_to_mastodon)

    if not args.dry_run:
        git_commit_and_push()
    else:
        print("Dry run complete.")

if __name__ == "__main__":
    main()
