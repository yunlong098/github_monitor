import os
import sys
from datetime import datetime

from .trending import fetch_trending
from .feishu import send_feishu_card


def main():
    webhook_url = os.environ.get("FEISHU_WEBHOOK_URL")
    if not webhook_url:
        print("ERROR: FEISHU_WEBHOOK_URL environment variable not set")
        sys.exit(1)

    print(f"[{datetime.now()}] fetching trending repos...")
    try:
        repos = fetch_trending(limit=10)
    except Exception as e:
        print(f"ERROR: failed to fetch trending: {e}")
        sys.exit(1)

    if not repos:
        print("WARNING: no trending repos found, skipping notification")
        sys.exit(0)

    print(f"[{datetime.now()}] found {len(repos)} repos, sending to feishu...")
    success = send_feishu_card(webhook_url, repos)
    if not success:
        print("ERROR: failed to send feishu notification after retries")
        sys.exit(1)

    print(f"[{datetime.now()}] notification sent successfully")


if __name__ == "__main__":
    main()
