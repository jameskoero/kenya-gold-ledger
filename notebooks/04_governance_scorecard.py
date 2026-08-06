"""
04_governance_scorecard.py
---------------------------
Builds a transparent, reproducible "Governance Response Scorecard" per era —
not a black-box index, but a documented count of (a) governance/doping
incidents recorded and (b) institutional/policy responses recorded in the
same window, so the ratio of "problems documented" to "responses documented"
is visible per era. This is the kind of summary a sport ministry, a NOC, or
an oversight committee could actually use, and — as far as this project's
own audit found — nobody has built it for Kenya specifically.

The scorecard deliberately does NOT compress this into one opaque number.
It reports the two counts side by side per era, plus the specific items
behind each count, so a policymaker can check the reasoning rather than
trust a score.

Run:  python notebooks/04_governance_scorecard.py
"""
import json
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"

controversies = json.loads((DATA / "controversies.json").read_text())["records"]
policy = pd.read_csv(DATA / "policy_timeline.csv")

ERAS = [
    ("1955-1999", 1955, 1999),
    ("2000-2015", 2000, 2015),
    ("2016-2020", 2016, 2020),
    ("2021-2025", 2021, 2025),
]

RESPONSE_TYPES = {"anti_doping", "governance", "strategy", "policy", "budget", "welfare"}
PROBLEM_CATEGORIES = {"governance_corruption", "doping", "anti_doping_governance",
                       "athlete_welfare_gender"}


def year_in_era(year: int, lo: int, hi: int) -> bool:
    return lo <= year <= hi


rows = []
for label, lo, hi in ERAS:
    problems = []
    for rec in controversies:
        if rec["category"] not in PROBLEM_CATEGORIES:
            continue
        years = [int(y) for y in rec["year_range"].replace("present", "2026").split("-")]
        rec_lo, rec_hi = years[0], years[-1]
        if rec_lo <= hi and rec_hi >= lo:
            problems.append(rec["title"])

    responses = []
    for _, r in policy.iterrows():
        if r["event_type"] in RESPONSE_TYPES and year_in_era(int(r["year"]), lo, hi):
            responses.append(f"{int(r['year'])}: {r['description'][:70]}")

    rows.append({
        "era": label,
        "problems_documented": len(problems),
        "responses_documented": len(responses),
        "response_ratio": round(len(responses) / max(len(problems), 1), 2),
        "problem_items": problems,
        "response_items": responses,
    })

print("=== Governance Response Scorecard (transparent, per era) ===\n")
for r in rows:
    print(f"{r['era']}  |  problems: {r['problems_documented']}  "
          f"responses: {r['responses_documented']}  "
          f"ratio: {r['response_ratio']}")
    for p in r["problem_items"]:
        print(f"    [problem]  {p}")
    for resp in r["response_items"]:
        print(f"    [response] {resp}")
    print()

out = pd.DataFrame(rows)[["era", "problems_documented", "responses_documented", "response_ratio"]]
out.to_csv(DATA / "governance_scorecard.csv", index=False)
print(f"Summary table written to {DATA / 'governance_scorecard.csv'}")
print("\nNote: a ratio near or above 1.0 means documented institutional responses keep pace")
print("with documented problems in that era; below 1.0 means problems are outpacing responses")
print("AS RECORDED IN THIS DATASET — a research signal to investigate further, not a verdict.")
