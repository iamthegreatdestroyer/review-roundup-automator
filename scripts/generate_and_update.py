#!/usr/bin/env python3
"""
Core generator for review-roundup-automator

Generates high-intent review and roundup pages using local LLM.

Focus: Buyer-intent content like "Best Note-Taking Apps 2026", pros/cons, winner picks, affiliate-friendly CTAs.
"""

import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from scripts.llm_client import generate, is_ollama_available

load_dotenv()

ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"
TEMPLATES_DIR = ROOT / "templates"
DATA_FILE = ROOT / "data" / "reviews.json"

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)


def load_review_topics() -> list[dict]:
    if not DATA_FILE.exists():
        # Fallback example
        return [
            {"topic": "Best Note-Taking Apps 2026", "category": "Productivity"},
            {"topic": "Best Free Project Management Tools", "category": "Collaboration"}
        ]
    with open(DATA_FILE) as f:
        return json.load(f).get("topics", [])


def generate_review_content(topic: dict) -> str:
    """Generate a high-converting review/roundup using LLM."""
    topic_name = topic.get("topic")
    category = topic.get("category", "Software")

    system_prompt = "You are an expert, trustworthy software reviewer. Write clear, helpful roundups for people evaluating tools. Include honest pros/cons, a clear winner recommendation, and natural affiliate-friendly language without being pushy. Use markdown."

    prompt = f"""Write a high-quality roundup article for: {topic_name} in the {category} space.

Structure:
- Engaging intro (who this is for)
- Top 5 tools with short description + key pros/cons
- Comparison table (markdown)
- Clear winner / best overall pick with reasoning
- "Who should choose what" guidance
- Short conclusion with CTA style (e.g. "If you're looking to...")

Keep total under 700 words. Make it useful and scannable."""

    return generate(prompt, system=system_prompt)


def build_pages(topics: list[dict]):
    DOCS_DIR.mkdir(exist_ok=True)
    template = env.get_template("base.html")

    # Index
    (DOCS_DIR / "index.html").write_text(template.render(
        title="Review Roundups",
        content="<h1>High-Intent Software Reviews & Roundups</h1><p>Autonomously generated.</p>"
    ))

    for topic in topics:
        content = generate_review_content(topic)
        html = template.render(
            title=topic.get("topic"),
            content=f"<h2>{topic.get('topic')}</h2>\n{content}"
        )
        safe = topic.get("topic", "review").lower().replace(" ", "-")[:50]
        (DOCS_DIR / f"{safe}.html").write_text(html)
        print(f"Generated: {topic.get('topic')}")


def git_commit_and_push(message: str = None):
    if message is None:
        message = f"Autonomous review update - {datetime.now().strftime('%Y-%m-%d')}"
    try:
        subprocess.run(["git", "add", "docs/"], cwd=ROOT, check=True)
        res = subprocess.run(["git", "commit", "-m", message], cwd=ROOT, capture_output=True, text=True)
        if res.returncode == 0:
            subprocess.run(["git", "push"], cwd=ROOT, check=True)
            print("Pushed successfully.")
        else:
            print("Nothing to commit or commit skipped.")
    except Exception as e:
        print(f"Git error: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print("=== review-roundup-automator update ===")

    if not is_ollama_available():
        print("Ollama not available - using fallback mode.")

    topics = load_review_topics()
    build_pages(topics)

    if not args.dry_run:
        git_commit_and_push()
    else:
        print("Dry run complete. Check docs/ folder.")

if __name__ == "__main__":
    main()
