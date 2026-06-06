# review-roundup-automator

> Automated High-Intent Review & Roundup Site

**Latest Update**: Dev.to auto-publishing + improved prompts implemented.

## New Capabilities

- Run with `--publish-to-devto` to automatically publish review articles to Dev.to.
- Significantly improved prompt quality for better, more consistent roundups.

## Quick Commands

```bash
python scripts/generate_and_update.py --dry-run
python scripts/generate_and_update.py --publish-to-devto
```

Make sure `DEVTO_API_KEY` is configured in your `.env` file.

*Scaffolding + Dev.to integration by Grok — June 2026*