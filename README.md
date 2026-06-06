# review-roundup-automator

> Automated High-Intent Review & Roundup Site — Now with working LLM generation!

**Status (June 2026)**: Core engine implemented and ready to run.

## What's Implemented
- Shared robust `llm_client.py`
- `generate_and_update.py` that:
  - Loads review topics
  - Uses high-quality prompts for buyer-intent roundups
  - Generates HTML pages via Jinja2 into `docs/`
  - Includes git commit/push automation
- Example data in `data/reviews.example.json`
- Clean base template

## Quick Test

```bash
ollama pull gemma2:2b
python scripts/generate_and_update.py --dry-run
# Check docs/ for generated review pages
python scripts/generate_and_update.py   # Full run with commit/push
```

This is one of the highest-ROI models. Expand the topics list in `data/reviews.json` for more pages.

*Scaffolding + core implementation by Grok — June 2026*