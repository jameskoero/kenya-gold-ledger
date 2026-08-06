"""
03_governance_density.py
-------------------------
Overlays documented governance/doping incident density against medal output,
per Games. This is the empirical bridge the concept doc calls for: not just
"here are the medals" and separately "here are the scandals", but the two on
one timeline so the relationship is visible rather than asserted.

Method (transparent, reproducible, no smoothing or interpolation): for each
Games year, count how many controversies.json records have a year_range
overlapping a window centred on that Games year. This is a straightforward
overlap count, not a fitted trend — the dataset is not yet large enough to
support anything more sophisticated, and the chart says so directly.

Run:  python notebooks/03_governance_density.py
"""
import json
import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

DATA = Path(__file__).resolve().parent.parent / "data"
VIZ = Path(__file__).resolve().parent.parent / "viz"

games = pd.read_csv(DATA / "medals_by_games.csv")
games = games.dropna(subset=["total"])
games = games[games["total"] > 0].copy()
games["games_year"] = games["games_year"].astype(int)

controversies = json.loads((DATA / "controversies.json").read_text())["records"]


def expand_range(year_range: str) -> tuple[int, int]:
    nums = [int(n) for n in re.findall(r"\d{4}", year_range)]
    if len(nums) == 1:
        return nums[0], nums[0]
    return min(nums), max(nums)


counts = {y: 0 for y in games["games_year"]}
for rec in controversies:
    lo, hi = expand_range(rec["year_range"])
    for y in counts:
        if lo - 2 <= y <= hi + 2:
            counts[y] += 1

games["incident_count"] = games["games_year"].map(counts)

fig, ax1 = plt.subplots(figsize=(11, 5.5))
ax1.bar(games["games_year"].astype(str), games["gold"], color="#D4AF37",
        label="Gold medals", width=0.5)
ax1.set_ylabel("Gold medals", color="#8a6d00")
ax1.tick_params(axis="y", labelcolor="#8a6d00")
ax1.set_xlabel("Games year")
plt.xticks(rotation=45)

ax2 = ax1.twinx()
ax2.plot(games["games_year"].astype(str), games["incident_count"],
         color="#BB0000", marker="o", linewidth=2, markersize=7,
         label="Governance/doping incidents referencing this cycle")
ax2.set_ylabel("Documented incidents (this dataset)", color="#BB0000")
ax2.set_yticks(range(0, int(games["incident_count"].max()) + 2))

fig.suptitle("Gold medals vs. documented governance/doping incidents, per Games cycle",
             fontsize=12, weight="bold", y=1.02)
fig.text(0.5, -0.05,
         "Incident count = controversies.json records whose year_range overlaps this Games cycle.\n"
         "Reflects what this project has documented so far, not a claim of causality either direction.",
         ha="center", fontsize=8, style="italic")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=False, fontsize=9)

plt.tight_layout()
plt.savefig(VIZ / "fig6_governance_vs_medals.png", dpi=150, bbox_inches="tight")
plt.close()

print(games[["games_year", "gold", "incident_count"]].to_string(index=False))
print(f"\nFigure written to {VIZ / 'fig6_governance_vs_medals.png'}")
