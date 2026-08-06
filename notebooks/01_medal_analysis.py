"""
01_medal_analysis.py
Reproducible analysis of Kenya's Olympic medal record from the project's
canonical datasets. Generates all figures in ../viz/ from real data only.

Run:  python notebooks/01_medal_analysis.py
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
VIZ = Path(__file__).resolve().parent.parent / "viz"
VIZ.mkdir(exist_ok=True)

KEN_RED = "#BB0000"
KEN_GREEN = "#006600"
GOLD = "#D4AF37"
SILVER = "#9AA0A6"
BRONZE = "#A97142"

plt.rcParams.update({"font.family": "serif", "axes.grid": True,
                     "grid.alpha": 0.25, "axes.axisbelow": True})

games = pd.read_csv(DATA / "medals_by_games.csv")
golds = pd.read_csv(DATA / "golds.csv")

# Only competed Games (drop boycotts/no-medal rows for the medal trend where NaN)
competed = games.dropna(subset=["total"]).copy()
competed = competed[competed["total"] > 0].copy()
competed["games_year"] = competed["games_year"].astype(int)
competed = competed.sort_values("games_year")

# ---- Figure 1: stacked medal totals per Games ----
fig, ax = plt.subplots(figsize=(11, 5.5))
x = competed["games_year"].astype(str)
ax.bar(x, competed["gold"], label="Gold", color=GOLD)
ax.bar(x, competed["silver"], bottom=competed["gold"], label="Silver", color=SILVER)
ax.bar(x, competed["bronze"], bottom=competed["gold"] + competed["silver"],
       label="Bronze", color=BRONZE)
ax.set_title("Kenya Olympic medals per Summer Games (medals as earnings, gold highlighted)",
             fontsize=13, weight="bold")
ax.set_ylabel("Medals")
ax.set_xlabel("Games")
ax.legend(frameon=False)
ax.axvspan(-0.5, -0.5, alpha=0)  # noop keep axis
plt.xticks(rotation=45)
fig.text(0.12, -0.02, "Boycotted Games (1976 Montreal, 1980 Moscow) omitted. Source: Olympedia.",
         fontsize=8, style="italic")
plt.tight_layout()
plt.savefig(VIZ / "fig1_medals_per_games.png", dpi=150, bbox_inches="tight")
plt.close()

# ---- Figure 2: cumulative gold count over time ----
gold_by_year = golds.groupby("games_year").size().reset_index(name="golds")
gold_by_year = gold_by_year.sort_values("games_year")
gold_by_year["cumulative"] = gold_by_year["golds"].cumsum()

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(gold_by_year["games_year"], gold_by_year["cumulative"],
        marker="o", color=GOLD, linewidth=2.2, markeredgecolor="black", markersize=7)
for _, r in gold_by_year.iterrows():
    ax.annotate(f"+{int(r.golds)}", (r.games_year, r.cumulative),
                textcoords="offset points", xytext=(0, 9), fontsize=8, ha="center")
ax.set_title("Cumulative Kenyan Olympic gold medals, 1968-2024", fontsize=13, weight="bold")
ax.set_ylabel("Cumulative golds")
ax.set_xlabel("Games year")
plt.tight_layout()
plt.savefig(VIZ / "fig2_cumulative_golds.png", dpi=150, bbox_inches="tight")
plt.close()

# ---- Figure 3: golds by event (concentration) ----
ev = golds["event"].value_counts()
fig, ax = plt.subplots(figsize=(10, 5.5))
ev.sort_values().plot(kind="barh", ax=ax, color=KEN_GREEN)
ax.set_title("Where Kenya's Olympic golds come from, by event", fontsize=13, weight="bold")
ax.set_xlabel("Number of gold medals (1968-2024)")
ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
plt.tight_layout()
plt.savefig(VIZ / "fig3_golds_by_event.png", dpi=150, bbox_inches="tight")
plt.close()

# ---- Figure 4: golds by sex over time ----
sx = golds.copy()
sx["sex"] = sx["sex"].map({"M": "Men", "W": "Women"})
pivot = sx.pivot_table(index="games_year", columns="sex", values="medal_id",
                       aggfunc="count", fill_value=0)
fig, ax = plt.subplots(figsize=(11, 5))
pivot.plot(kind="bar", ax=ax, color={"Men": KEN_RED, "Women": KEN_GREEN})
ax.set_title("Kenyan Olympic golds by athlete sex, per Games", fontsize=13, weight="bold")
ax.set_ylabel("Golds")
ax.set_xlabel("Games year")
ax.legend(frameon=False, title="")
plt.xticks(rotation=45)
fig.text(0.12, -0.02, "First female Olympic gold: Pamela Jelimo, 800m, Beijing 2008.",
         fontsize=8, style="italic")
plt.tight_layout()
plt.savefig(VIZ / "fig4_golds_by_sex.png", dpi=150, bbox_inches="tight")
plt.close()

# ---- Printed summary stats (real) ----
total_g = int(competed["gold"].sum())
total_s = int(competed["silver"].sum())
total_b = int(competed["bronze"].sum())
print("=== Kenya Olympic medal summary (Summer Games, from datasets) ===")
print(f"Golds: {total_g} | Silvers: {total_s} | Bronzes: {total_b} | Total: {total_g+total_s+total_b}")
print(f"Gold rows individually catalogued in golds.csv: {len(golds)}")
print(f"Share of golds that are athletics: "
      f"{(golds['sport'].eq('Athletics').mean()*100):.1f}%")
print(f"Share of golds won by women: {(golds['sex'].eq('W').mean()*100):.1f}%")
print("Steeplechase golds:", int(golds['event'].eq('3000m steeplechase').sum()))
print("Figures written to viz/")
