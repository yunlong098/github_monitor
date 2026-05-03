from __future__ import annotations

import requests
from bs4 import BeautifulSoup


def fetch_trending(limit: int = 10) -> list[dict]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(
        "https://github.com/trending?since=daily",
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    articles = soup.select("article.Box-row")

    repos = []
    for article in articles[:limit]:
        a_tag = article.select_one("h2 a")
        full_name = a_tag["href"].strip("/") if a_tag else "unknown"

        desc_tag = article.select_one("p.col-9")
        desc = desc_tag.get_text(strip=True) if desc_tag else ""

        lang_tag = article.select_one("[itemprop='programmingLanguage']")
        lang = lang_tag.get_text(strip=True) if lang_tag else ""

        total_stars = ""
        for tag in article.select("a.Link--muted"):
            href = tag.get("href", "")
            if href.endswith("/stargazers"):
                total_stars = tag.get_text(strip=True)
                break

        today_tag = article.select_one("span.d-inline-block.float-sm-right")
        today_stars = today_tag.get_text(strip=True) if today_tag else ""

        repos.append({
            "name": full_name,
            "url": f"https://github.com/{full_name}",
            "description": desc,
            "language": lang,
            "total_stars": total_stars,
            "today_stars": today_stars,
        })

    return repos
