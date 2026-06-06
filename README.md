# Review Roundup Automator

Autonomous high-intent review site.

## Mastodon Integration
Now supports --publish-to-mastodon flag.

Add to .env:
MASTODON_INSTANCE=https://mastodon.social
MASTODON_ACCESS_TOKEN=your_token

Full run example:
python scripts/generate_and_update.py --publish-to-devto --publish-to-mastodon

(Previous content remains)