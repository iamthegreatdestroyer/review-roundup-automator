#!/bin/bash
# Cron setup for autonomous income generator

# Make sure to run this as the user that owns the repo

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

# Example cron entry (every day at 3 AM)
# 0 3 * * * cd /path/to/repo && /usr/bin/python3 scripts/generate_and_update.py --publish-to-devto --publish-to-mastodon >> logs/cron.log 2>&1

echo "Cron setup complete. Add this to crontab:"
echo "0 3 * * * cd $REPO_DIR && python3 scripts/generate_and_update.py --publish-to-devto --publish-to-mastodon >> logs/cron.log 2>&1"