"""
collect_corpus.py
-----------------
Turns the committed label file (data/corpus_labels.jsonl) into a trainable
corpus by fetching each article's full text at runtime and caching it LOCALLY.

WHY IT'S SPLIT THIS WAY
Full news article text is copyrighted and must not be committed to the repo. So:
  * data/corpus_labels.jsonl  (committed)  — url, source, date, label, and an
    ORIGINAL one-line summary written for this project. Shareable.
  * data/medals_raw/news/     (gitignored) — fetched full text, cached locally,
    never committed.
The classifier can train on the richer fetched text when present, and falls back
to the committed summaries so the pipeline is always runnable by anyone who
clones the repo, even before fetching.

GOOD-CITIZEN FETCHING
  * Identifies with a descriptive User-Agent.
  * Checks robots.txt per domain and skips disallowed paths.
  * Rate-limits per domain.
  * Caches by URL hash; never re-fetches what it already has.
Some sources may block automated access or require the maintainer to collect
text manually — that's expected. Missing full text is not an error; the summary
fallback covers it.

REQUIREMENTS
    pip install requests beautifulsoup4

USAGE
    python nlp/collect_corpus.py                 # fetch all uncached articles
    python nlp/collect_corpus.py --status         # show cache coverage only
"""
from __future__ import annotations
import argparse
import hashlib
import json
import time
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse
from urllib import robotparser

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
LABELS = ROOT / "data" / "corpus_labels.jsonl"
CACHE = ROOT / "data" / "medals_raw" / "news"
UA = "kenya-olympic-gold/0.1 (open research dataset; respects robots.txt)"
RATE = 1.0
ROBOTS_TIMEOUT = 5
FETCH_TIMEOUT = 8
_robots_cache: dict[str, robotparser.RobotFileParser] = {}
_last_hit: dict[str, float] = {}


def url_hash(url: str) -> str:
    return hashlib.sha1(url.encode()).hexdigest()[:16]


def load_labels() -> list[dict]:
    rows = []
    with open(LABELS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def allowed_by_robots(url: str) -> bool:
    domain = urlparse(url).netloc
    if domain in _robots_cache:
        rp = _robots_cache[domain]
        return True if rp is None else rp.can_fetch(UA, url)

    # RobotFileParser.read() uses urllib with NO timeout — a slow or dead
    # server on robots.txt hangs this forever, which is what was stalling
    # collection (and made the whole Colab session look frozen). Fetch it
    # with `requests` and a hard timeout instead, then feed the text to the
    # parser manually.
    rp = None
    try:
        r = requests.get(f"https://{domain}/robots.txt",
                          headers={"User-Agent": UA}, timeout=ROBOTS_TIMEOUT)
        if r.status_code == 200:
            rp = robotparser.RobotFileParser()
            rp.parse(r.text.splitlines())
        # non-200 (404, etc.) -> no robots.txt restrictions -> rp stays None -> allowed
    except Exception:
        # Unreachable / timed out / refused: don't block collection on it.
        # Treat as "no robots.txt found", the standard fallback.
        rp = None

    _robots_cache[domain] = rp
    return True if rp is None else rp.can_fetch(UA, url)


def polite_wait(url: str):
    domain = urlparse(url).netloc
    now = time.time()
    delta = now - _last_hit.get(domain, 0)
    if delta < RATE:
        time.sleep(RATE - delta)
    _last_hit[domain] = time.time()


def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    return "\n".join(p for p in paras if len(p) > 40)


def fetch_one(url: str) -> str | None:
    if not allowed_by_robots(url):
        print(f"    robots.txt disallows — skipping", file=sys.stderr, flush=True)
        return None
    polite_wait(url)
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=FETCH_TIMEOUT)
        if r.status_code != 200:
            print(f"    HTTP {r.status_code} — skipping", file=sys.stderr, flush=True)
            return None
        return extract_text(r.text)
    except Exception as e:
        print(f"    fetch error ({e}) — skipping", file=sys.stderr, flush=True)
        return None


def status():
    CACHE.mkdir(parents=True, exist_ok=True)
    labels = load_labels()
    cached = sum(1 for r in labels if (CACHE / f"{url_hash(r['url'])}.json").exists())
    print(f"Corpus: {len(labels)} labelled items; {cached} have cached full text; "
          f"{len(labels) - cached} rely on the committed summary.")


def _collect_one(r: dict) -> tuple[str, bool]:
    """Fetch a single labelled item; returns (source_label, success)."""
    h = url_hash(r["url"])
    out = CACHE / f"{h}.json"
    if out.exists():
        return r["source"], True
    print(f"[{r['source']}] {r['url']}", file=sys.stderr, flush=True)
    text = fetch_one(r["url"])
    if text:
        out.write_text(json.dumps({**r, "full_text": text}, ensure_ascii=False))
        return r["source"], True
    return r["source"], False


def collect(max_workers: int = 8):
    """Fetch every uncached labelled item, in parallel ACROSS domains.

    Politeness (rate limiting, robots.txt) is still enforced per domain via
    `polite_wait` / `allowed_by_robots`, which are keyed by domain and shared
    across threads — so two URLs on the same domain still queue up behind
    each other, but URLs on different domains run concurrently instead of
    waiting in one long sequential line. With ~15 distinct domains in a
    22-item corpus and 5-8 second timeouts, this brings total runtime from
    several minutes down to well under a minute in the common case.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    labels = load_labels()
    by_domain: dict[str, list[dict]] = defaultdict(list)
    for r in labels:
        by_domain[urlparse(r["url"]).netloc].append(r)

    fetched = skipped = 0
    with ThreadPoolExecutor(max_workers=min(max_workers, len(by_domain) or 1)) as ex:
        futures = []
        for domain, items in by_domain.items():
            # one task per domain; each task processes its own items in
            # sequence so the per-domain rate limit is respected
            def run_domain(items=items):
                results = []
                for r in items:
                    results.append(_collect_one(r))
                return results
            futures.append(ex.submit(run_domain))

        for fut in as_completed(futures):
            for source, ok in fut.result():
                if ok:
                    fetched += 1
                else:
                    skipped += 1

    print(f"Done. Fetched/cached {fetched}, skipped {skipped} across "
          f"{len(by_domain)} domains. Skipped items fall back to their "
          f"committed summaries at train time.", file=sys.stderr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--workers", type=int, default=8,
                    help="Max domains fetched in parallel (default 8)")
    args = ap.parse_args()
    status() if args.status else collect(max_workers=args.workers)
