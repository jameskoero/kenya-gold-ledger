"""
build_medalist_origins.py
-------------------------
Enriches data/geo/medalist_origins.csv with birthplace/county for every medalist
by reading the 'Born' field from each athlete's Wikipedia infobox.

WHY A BUILDER, NOT HAND ENTRY
Birthplaces for ~100 athletes cannot be filled from memory without fabrication
risk. This reads the birthplace directly from each athlete's Wikipedia infobox,
maps the stated place to a Kenyan county via a fuzzy lookup against
kenya_counties.csv, and records confidence + source per row. Places it cannot
confidently map are left blank and flagged, never guessed.

The Rift Valley / Kalenjin concentration this reveals is already established in
the literature (Onywera et al., Tucker et al.); the point here is to tie that
pattern to THIS project's open, per-athlete, sourced dataset rather than to a
closed one — and to do it reproducibly.

REQUIREMENTS
    pip install requests beautifulsoup4 pandas rapidfuzz
Requires network. Intended for the maintainer's environment.

USAGE
    python data/build_medalist_origins.py            # enrich + write
    python data/build_medalist_origins.py --dry-run   # report, don't write
"""
from __future__ import annotations
import argparse
import re
import time
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import pandas as pd

try:
    from rapidfuzz import process, fuzz
    HAVE_FUZZ = True
except ImportError:
    HAVE_FUZZ = False

DATA = Path(__file__).resolve().parent
GEO = DATA / "geo"
UA = "kenya-olympic-gold/0.1 (open research dataset)"
RATE = 2.0


def load_athletes() -> list[str]:
    """Every distinct individual medalist from all_medals.csv (skip relays)."""
    am = pd.read_csv(DATA / "all_medals.csv")
    names = (am.loc[~am["athlete_or_team"].str.contains("relay", case=False, na=False),
                    "athlete_or_team"].dropna().unique().tolist())
    return sorted(names)


def wiki_birthplace(name: str) -> str | None:
    """Read the 'Born' infobox row from an athlete's Wikipedia page."""
    title = name.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{title}"
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, "html.parser")
        infobox = soup.find("table", class_=re.compile("infobox"))
        if not infobox:
            return None
        for tr in infobox.find_all("tr"):
            th = tr.find("th")
            if th and "born" in th.get_text(strip=True).lower():
                td = tr.find("td")
                if td:
                    return td.get_text(" ", strip=True)
    except Exception:
        return None
    return None


def map_to_county(birth_text: str, counties: list[str]) -> tuple[str, str]:
    """Return (county, confidence). Blank county if no confident match."""
    if not birth_text:
        return "", "none"
    # direct substring match first
    for c in counties:
        if c.lower() in birth_text.lower():
            return c, "high"
    if HAVE_FUZZ:
        match, score, _ = process.extractOne(birth_text, counties, scorer=fuzz.partial_ratio)
        if score >= 90:
            return match, "medium"
    return "", "low"  # found a birthplace but couldn't map it — flag, don't guess


def main(dry_run: bool):
    counties = pd.read_csv(GEO / "kenya_counties.csv")["county"].tolist()
    existing = pd.read_csv(GEO / "medalist_origins.csv")
    known = set(existing["athlete_or_team"])

    new_rows = []
    for name in load_athletes():
        if name in known:
            continue
        print(f"  {name} ...", file=sys.stderr, end="")
        bt = wiki_birthplace(name)
        county, conf = map_to_county(bt or "", counties)
        print(f" born='{bt}' -> county='{county}' ({conf})", file=sys.stderr)
        new_rows.append(dict(
            athlete_or_team=name, birthplace_county=county, confidence=conf,
            source=f"wikipedia:{name.replace(' ', '_')}" if bt else "",
            notes=(bt or "birthplace not found on Wikipedia"),
        ))
        time.sleep(RATE)

    merged = pd.concat([existing, pd.DataFrame(new_rows)], ignore_index=True)
    mapped = (merged["birthplace_county"].astype(str).str.len() > 0).sum()
    print(f"\nMapped {mapped}/{len(merged)} medalists to a county.", file=sys.stderr)
    if not dry_run:
        merged.to_csv(GEO / "medalist_origins.csv", index=False)
        print("Wrote medalist_origins.csv", file=sys.stderr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    main(ap.parse_args().dry_run)
