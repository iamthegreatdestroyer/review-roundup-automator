# review-roundup-automator

> Automated High-Intent Review & Roundup Site

**Latest Update**: Centralized Affiliate Link System added.

## New Feature: Affiliate Management

- Affiliate links are centrally managed in `data/affiliates.json`.
- Relevant links are automatically injected into generated reviews.
- Standard affiliate disclosure is included.

Edit `data/affiliates.json` to add your affiliate programs.

## Quick Commands

```bash
python scripts/generate_and_update.py --dry-run
python scripts/generate_and_update.py --publish-to-devto
```

*Scaffolding + Affiliate system by Grok — June 2026*