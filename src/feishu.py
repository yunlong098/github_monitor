from __future__ import annotations

import time
from datetime import datetime, timezone, timedelta

import requests

MAX_RETRIES = 3
INITIAL_BACKOFF = 2


def _build_card(repos: list[dict], date_str: str) -> dict:
    elements = []

    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md", "content": f"📅 {date_str}"},
    })

    elements.append({"tag": "hr"})

    for i, repo in enumerate(repos, 1):
        stars_info = repo["total_stars"]
        if repo["today_stars"]:
            stars_info += f" ({repo['today_stars']})"
        lang_info = f" · {repo['language']}" if repo["language"] else ""

        text = (
            f"**<font color='blue'>{i}. [{repo['name']}]({repo['url']})</font>**\n"
            f"{repo['description']}\n"
            f"⭐ {stars_info}{lang_info}"
        )
        elements.append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": text},
        })

    elements.append({"tag": "hr"})

    elements.append({
        "tag": "note",
        "elements": [
            {
                "tag": "plain_text",
                "content": "数据来源：GitHub Trending · 每日自动推送",
            }
        ],
    })

    return {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": "📊 GitHub Trending Top 10"},
                "template": "blue",
            },
            "elements": elements,
        },
    }


def send_feishu_card(webhook_url: str, repos: list[dict]) -> bool:
    date_str = (
        datetime.now(timezone(timedelta(hours=8)))
        .strftime("%Y-%m-%d %H:%M")
    )
    payload = _build_card(repos, date_str)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                webhook_url,
                json=payload,
                timeout=15,
                headers={"Content-Type": "application/json"},
            )
            data = resp.json()
            if data.get("code", -1) == 0 or resp.status_code == 200:
                return True
            print(f"[attempt {attempt}] feishu response: {data}")
        except requests.RequestException as e:
            print(f"[attempt {attempt}] request error: {e}")

        if attempt < MAX_RETRIES:
            backoff = INITIAL_BACKOFF * (2 ** (attempt - 1))
            print(f"retrying in {backoff}s...")
            time.sleep(backoff)

    return False
