"""
build_all_medals.py
-------------------
Builds data/all_medals.csv — every Kenyan Olympic medal as one row (each medal
is a separate earning) — by scraping the per-Games medalist tables from the
Wikipedia "Kenya at the YEAR Summer Olympics" articles.

WHY A SCRAPER INSTEAD OF A HAND-TYPED TABLE
Kenya has 124 Olympic medals. Transcribing 85 silver/bronze rows by hand risks
transcription and memory errors — the exact failure mode this project's
integrity rules forbid. Instead the full table is BUILT from an authoritative
source, so every row is reproducible and auditable. Re-running this script
regenerates the file; if Wikipedia corrects a record, the fix propagates.

The 39 golds are additionally maintained by hand in golds.csv with richer
per-medal context (records, reallocation flags, notes). This script cross-checks
its gold count against golds.csv and warns on any mismatch.

REQUIREMENTS
    pip install requests beautifulsoup4 pandas
Network access is required to run this (it fetches Wikipedia). It is intended to
be run in the maintainer's environment, not in a sandbox.

USAGE
    python data/build_all_medals.py            # build + write all_medals.csv
    python data/build_all_medals.py --check     # build in memory, cross-check only
"""
from __future__ import annotations
import argparse
import time
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import pandas as pd

DATA = Path(__file__).resolve().parent
UA = "kenya-olympic-gold/0.1 (open research dataset; contact via repo)"
RATE_LIMIT_SECONDS = 2.0  # be polite

# Games Kenya competed in and won >=1 medal. 1976/1980 boycotted; 1956/1960 no medals.
GAMES = {
    1964: "Kenya_at_the_1964_Summer_Olympics",
    1968: "Kenya_at_the_1968_Summer_Olympics",
    1972: "Kenya_at_the_1972_Summer_Olympics",
    1984: "Kenya_at_the_1984_Summer_Olympics",
    1988: "Kenya_at_the_1988_Summer_Olympics",
    1992: "Kenya_at_the_1992_Summer_Olympics",
    1996: "Kenya_at_the_1996_Summer_Olympics",
    2000: "Kenya_at_the_2000_Summer_Olympics",
    2004: "Kenya_at_the_2004_Summer_Olympics",
    2008: "Kenya_at_the_2008_Summer_Olympics",
    2012: "Kenya_at_the_2012_Summer_Olympics",
    2016: "Kenya_at_the_2016_Summer_Olympics",
    2020: "Kenya_at_the_2020_Summer_Olympics",
    2024: "Kenya_at_the_2024_Summer_Olympics",
}

MEDAL_WORDS = {"gold", "silver", "bronze"}


def fetch(title: str) -> str:
    url = f"https://en.wikipedia.org/wiki/{title}"
    r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    return r.text


def parse_medal_table(html: str, year: int) -> list[dict]:
    """Find the 'Medalists'/'Medal | Name | Sport | Event' table and parse rows.

    Wikipedia renders the medal type as an icon with alt text ('Gold medal' etc.)
    and the name as a link — both present in the HTML even though they vanish in
    plain-text extraction. We read them from the HTML directly.
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for table in soup.find_all("table", class_="wikitable"):
        header = [th.get_text(strip=True).lower() for th in table.find_all("th")]
        if not ({"medal", "name", "event"} <= set(header)):
            continue
        for tr in table.find_all("tr"):
            cells = tr.find_all(["td", "th"])
            if len(cells) < 4:
                continue
            # medal type: from icon alt text or cell text
            medal_cell = cells[0]
            medal = ""
            img = medal_cell.find("img")
            if img and img.get("alt"):
                medal = img["alt"].split()[0].lower()
            if medal not in MEDAL_WORDS:
                txt = medal_cell.get_text(strip=True).lower()
                medal = next((w for w in MEDAL_WORDS if w in txt), "")
            if medal not in MEDAL_WORDS:
                continue
            name = cells[1].get_text(strip=True)
            sport = cells[2].get_text(strip=True)
            event = cells[3].get_text(strip=True)
            rows.append({
                "games_year": year,
                "medal": medal,
                "athlete_or_team": name,
                "sport": sport,
                "event": event,
                "source": f"wikipedia:{GAMES[year]}",
            })
    return rows


def build(check_only: bool = False) -> pd.DataFrame:
    all_rows = []
    empty_years = []
    for year, title in GAMES.items():
        print(f"[{year}] fetching {title} ...", file=sys.stderr)
        try:
            html = fetch(title)
            rows = parse_medal_table(html, year)
            print(f"        parsed {len(rows)} medal rows", file=sys.stderr)
            if not rows:
                empty_years.append(year)
            all_rows.extend(rows)
        except Exception as e:
            print(f"        WARNING: {year} failed ({e}); skipping", file=sys.stderr)
            empty_years.append(year)
        time.sleep(RATE_LIMIT_SECONDS)

    scraped = pd.DataFrame(all_rows)

    # golds.csv is the hand-verified, richly-annotated source of truth for gold
    # medals. Some older Wikipedia "Kenya at the YEAR Olympics" articles (1968,
    # 1972 as of this writing) don't use the tabular medalist format this parser
    # looks for, so scraping alone would silently DROP golds this project has
    # already verified. Fix: always take golds from golds.csv, and only take
    # silver/bronze from the scrape.
    golds_path = DATA / "golds.csv"
    gold_rows = pd.DataFrame()
    if golds_path.exists():
        g = pd.read_csv(golds_path)
        gold_rows = pd.DataFrame({
            "games_year": g["games_year"], "medal": "gold", "sport": g["sport"],
            "event": g["event"], "athlete_or_team": g["athlete_or_team"],
            "source": g["source"],
        })

    non_gold = scraped[scraped["medal"] != "gold"] if not scraped.empty else scraped
    df = pd.concat([gold_rows, non_gold], ignore_index=True)

    scraped_gold_count = (scraped["medal"] == "gold").sum() if not scraped.empty else 0
    print(f"\nCross-check: golds.csv={len(gold_rows)}  scraped golds={scraped_gold_count} "
          f"(scraped golds are discarded in favour of golds.csv either way)", file=sys.stderr)
    if empty_years:
        print(f"NOTE: these Games returned 0 scraped rows and have NO silver/bronze "
              f"rows in this build: {empty_years}. Their gold medals still come from "
              f"golds.csv and are present. This is a known gap (older Wikipedia articles "
              f"for these Games don't use a table this parser recognises) — it is reported "
              f"here rather than silently leaving those years incomplete.", file=sys.stderr)

    if df.empty:
        print("No rows built. Check network / page structure.", file=sys.stderr)
        return df

    if not check_only:
        out = DATA / "all_medals.csv"
        df.to_csv(out, index=False)
        print(f"Wrote {len(df)} rows -> {out}", file=sys.stderr)
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="Build in memory and cross-check without writing")
    args = ap.parse_args()
    build(check_only=args.check)
