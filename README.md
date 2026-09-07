# Kenya at Gold: The Governance Ledger

**An open, structured, source-linked dataset connecting Kenya's Olympic medal record to its governance, doping, welfare, and policy history — built to be queried, visualized, modeled, and cited. Now also a live API and dashboard, not just a static archive.**

**Live:** [API](https://kenya-gold-ledger-api.onrender.com/docs) · [Dashboard](https://kenya-gold-ledger.vercel.app)

Kenya has won **124 Olympic medals** (39 gold, 45 silver, 40 bronze through Paris 2024), the highest of any African nation, and nearly all of them from distance running. That story is told everywhere. What isn't told, in any single structured place, is the connective tissue: the diverted sponsorship funds, the anti-doping collapse and recovery, the athletes who die broke or violently, the training system that produces world records in villages with no track, and what the state actually does with the reputational capital its runners generate.

This repository is that place. It treats **every medal as a separately catalogued earning** — with the year, the person(s) awarded, and the surrounding context — and gives **gold medals the highest level of detail**, because the gold is the unit around which the whole national narrative is built.

**Jump to:** [What's different](#what-makes-this-different-from-anything-else-out-there) · [What's in here](#whats-in-here) · [Live API and dashboard](#live-api-and-dashboard) · [Headline analytics](#headline-analytics-all-from-the-datasets-reproducible) · [The ML dimension](#the-ml-dimension) · [Data integrity](#data-integrity) · [Licensing](#licensing) · [Citing this work](#citing-this-work) · [Setup](#setup) · [Status](#status)

## What makes this different from anything else out there

I looked. Olympic datasets are common on GitHub and Kaggle; none are Kenya-specific, and none go past medal counts. The academic literature on Kenyan running (Onywera, Pitsiladis, Tucker and others) is rigorous but answers a physiological and sociocultural question, not a governance one. Sports governance benchmarking exists (Play the Game/KU Leuven's Sports Governance Observer), but it has never been applied to Kenyan athletics specifically. So this repo adds five things I haven't seen done anywhere else, for this country or this sport:

1. **An SGO-aligned governance scorecard** ([`data/sgo_framework.json`](data/sgo_framework.json)) — the first application of the peer-reviewed Sports Governance Observer / National Sports Governance Observer methodology (transparency, democratic processes, internal accountability and control, societal responsibility) to Athletics Kenya and ADAK, rather than a self-invented metric.
2. **A governance network graph** ([`notebooks/02_network_analysis.py`](notebooks/02_network_analysis.py)) — officials, athletes, and incidents as a graph instead of a list, so recurrence across scandals is visible rather than buried in separate news stories.
3. **A governance-vs-medals overlay** ([`notebooks/03_governance_density.py`](notebooks/03_governance_density.py)) — gold medal counts and documented incident density plotted on the same timeline per Games cycle, so the relationship (or its absence) is something you can look at, not something asserted.
4. **A transparent Governance Response Scorecard** ([`notebooks/04_governance_scorecard.py`](notebooks/04_governance_scorecard.py)) — for each era, a plain count of documented problems against documented institutional responses, with every item listed out rather than compressed into an opaque single score. The 2021-2025 era's response ratio (1.67, versus 0.4 in 2016-2020) is the kind of number a sports ministry, a NOC, or an oversight committee could actually use — and the dataset now includes a complete real-world test case for this exact methodology: WADA's September 2025 non-compliance declaration against Kenya/ADAK, followed by its 2026 clearance after a documented corrective action plan.
5. **A live, queryable API and dashboard** ([`backend/`](backend), [`frontend/`](frontend)) — every dataset and the trained ML classifier served over HTTP, plus a browser dashboard that fetches live rather than embedding a static snapshot. Medal history, gold concentration by event, and a filterable governance/doping timeline, all from the same open data. Built for fans, journalists, and researchers as much as for developers.

## What's in here

The tree below is a map, not a link list — GitHub doesn't render links inside code blocks, so use the linked references right after it (or just browse the repo directly) to jump to any specific file.

```
data/
  medals_by_games.csv       Per-Games gold/silver/bronze totals, 1956-2024 (verified, Olympedia)
  golds.csv                 Every one of the 39 golds, individually catalogued (the highlight)
  all_medals.csv            Every medal as one row; golds verified, silver/bronze via builder
  build_all_medals.py       Reproducible scraper that completes all_medals.csv from source
  controversies.json        Sourced governance/doping/welfare incidents, 2015-2026 (schema v0.2)
  sgo_framework.json        Sports Governance Observer framework, adapted for AK/ADAK
  talent_geography_study.json  Published talent-origin study, for validating medalist_origins.csv
  policy_timeline.csv        Government actions and real budget figures by year
  funding_vs_output.csv      Medals vs doping context vs funding, per Games
  governance_scorecard.csv   Output of the transparent scorecard (see below)
  corpus_labels.jsonl        REAL labelled news corpus for the ML classifier
  geo/
    kenya_counties.csv       County reference (region, coordinates)
    medalist_origins.csv     Athlete -> birthplace county (verified seed)
  build_medalist_origins.py  Reproducible builder that enriches origins from source
backend/
  app.py                    FastAPI app serving every dataset + the ML classifier as live endpoints
  migrate_to_sqlite.py       Builds the queryable database the API reads from
  requirements.txt          Pinned dependencies
  render.yaml                Render deployment blueprint (free tier)
frontend/
  index.html                 Static dashboard, fetches live from the API (no embedded data)
  vercel.json                 Deployment config (Vercel, static)
nlp/
  collect_corpus.py          Fetches article text (robots-aware, rate-limited, gitignored cache)
  train.py                   Trains + cross-validates the classifier on the corpus
  controversy_classifier.py  Inference wrapper; load_trained() uses the real model
notebooks/
  01_medal_analysis.py      Reproducible core analysis; regenerates figs 1-4
  02_network_analysis.py    Governance network graph (fig 5)
  03_governance_density.py  Medals-vs-incidents overlay (fig 6)
  04_governance_scorecard.py Transparent scorecard
docs/
  methodology.md            Sourcing rules and confidence model
  literature-review.md       How this positions against existing scholarship
  data-schema.md            Field definitions for every dataset
  concept.md                Full concept and reframing
manuscript/                 Draft academic publication
viz/                        Generated charts + dashboard.html
sources/                    Citation manifest
```

**Direct links to everything in the tree above:**
[`data/medals_by_games.csv`](data/medals_by_games.csv) · [`data/golds.csv`](data/golds.csv) · [`data/all_medals.csv`](data/all_medals.csv) · [`data/build_all_medals.py`](data/build_all_medals.py) · [`data/controversies.json`](data/controversies.json) · [`data/sgo_framework.json`](data/sgo_framework.json) · [`data/talent_geography_study.json`](data/talent_geography_study.json) · [`data/policy_timeline.csv`](data/policy_timeline.csv) · [`data/funding_vs_output.csv`](data/funding_vs_output.csv) · [`data/governance_scorecard.csv`](data/governance_scorecard.csv) · [`data/corpus_labels.jsonl`](data/corpus_labels.jsonl) · [`data/geo/kenya_counties.csv`](data/geo/kenya_counties.csv) · [`data/geo/medalist_origins.csv`](data/geo/medalist_origins.csv) · [`data/build_medalist_origins.py`](data/build_medalist_origins.py) · [`backend/app.py`](backend/app.py) · [`backend/migrate_to_sqlite.py`](backend/migrate_to_sqlite.py) · [`frontend/index.html`](frontend/index.html) · [`nlp/collect_corpus.py`](nlp/collect_corpus.py) · [`nlp/train.py`](nlp/train.py) · [`nlp/controversy_classifier.py`](nlp/controversy_classifier.py) · [`notebooks/01_medal_analysis.py`](notebooks/01_medal_analysis.py) · [`notebooks/02_network_analysis.py`](notebooks/02_network_analysis.py) · [`notebooks/03_governance_density.py`](notebooks/03_governance_density.py) · [`notebooks/04_governance_scorecard.py`](notebooks/04_governance_scorecard.py) · [`docs/methodology.md`](docs/methodology.md) · [`docs/literature-review.md`](docs/literature-review.md) · [`docs/data-schema.md`](docs/data-schema.md) · [`docs/concept.md`](docs/concept.md) · [`manuscript/`](manuscript) · [`viz/`](viz) · [`sources/`](sources)

## Live API and dashboard

The dataset is no longer only static files — it's also served live:

- **API** — [`kenya-gold-ledger-api.onrender.com`](https://kenya-gold-ledger-api.onrender.com/docs) (FastAPI, OpenAPI docs at `/docs`). Endpoints include `/medals/golds`, `/medals/all`, `/governance/controversies`, `/governance/sgo-framework`, `/governance/scorecard`, `/geo/medalist-origins`, and a `POST /predict/controversy-category` endpoint that runs the trained classifier on arbitrary text.
- **Dashboard** — [`kenya-gold-ledger.vercel.app`](https://kenya-gold-ledger.vercel.app) — fetches from the live API at load time rather than embedding a snapshot, so it stays current as the dataset grows.
- Hosted on free tiers (Render + Vercel): the API may take up to ~50 seconds to wake up after a period of inactivity — this is a cold-start delay, not a fault.
- Full deployment instructions, including a from-scratch rebuild path, are in [`DEPLOYMENT.md`](DEPLOYMENT.md).

## Headline analytics (all from the datasets, reproducible)

Running [`python notebooks/01_medal_analysis.py`](notebooks/01_medal_analysis.py) regenerates these from the raw CSVs:

- **97.4%** of Kenya's Olympic golds are in athletics; the only exception is Robert Wangila's 1988 boxing gold.
- **25.6%** of golds have been won by women — every one of them since Pamela Jelimo in 2008.
- **11 of 39 golds** are in the men's 3000m steeplechase alone — the single most productive event in Kenyan Olympic history.
- Best-ever haul: **16 medals at Beijing 2008**; joint-best gold count: **6, at both Beijing 2008 and Rio 2016**.

![Medals per Games](viz/fig1_medals_per_games.png)

## The ML dimension

This is not a static archive. The [`nlp/`](nlp) pipeline **classifies real news coverage** into controversy categories — corruption, doping, anti-doping governance, welfare/gender, geopolitics, migration — so the [`controversies.json`](data/controversies.json) timeline can update from evidence rather than manual curation. It trains on [`data/corpus_labels.jsonl`](data/corpus_labels.jsonl), a corpus of **real published articles** (BBC, AP, Sports Illustrated, Daily Nation, World Athletics and others), not a synthetic seed set. [`collect_corpus.py`](nlp/collect_corpus.py) fetches full article text at runtime (robots-aware, rate-limited, cached locally and never committed for copyright reasons); [`train.py`](nlp/train.py) cross-validates and reports honest per-class metrics. The trained model is also served live via the API's `/predict/controversy-category` endpoint.

The baseline is TF-IDF + Complement Naive Bayes, chosen after measuring it against several alternatives — see [`nlp/README.md`](nlp/README.md) for the comparison. Its numbers are reported honestly: strong on the well-populated classes (doping, corruption), weak on classes with only two examples — which is the correct behaviour of a small-corpus baseline and the reason "grow the corpus" is the documented next task. The interface is model-agnostic, so a fine-tuned transformer drops in later.

Analytical layers (see [`docs/methodology.md`](docs/methodology.md)): time-series of funding vs medal output vs sanction counts, geospatial clustering of medalist origin (via [`data/geo/`](data/geo), now cross-validated against a published talent-origin study in [`data/talent_geography_study.json`](data/talent_geography_study.json)) against county indicators, and network analysis of officials/federations/sanctioned athletes to show how few names recur across scandals.

## Data integrity

Every row carries a `source`, and every claim in [`controversies.json`](data/controversies.json) carries a `confidence` level reflecting the strength of public documentation. **No synthetic data is used anywhere.** Where sources disagree — for example, Olympedia records Kenya's totals as 39-45-40 while some Wikipedia tables show 39-44-41, owing to differing treatment of relay and boxing medals — the discrepancy is recorded, not silently resolved. `controversies.json` is now on schema v0.2, extending original coverage (2015-2021) through the escalating 2022-2024 AIU/ADAK sanction trend, the 2025 WADA non-compliance crisis, and the 2026 clearance — 12 records total, all independently sourced. See [`docs/methodology.md`](docs/methodology.md).

## Licensing

- **Code** ([`nlp/`](nlp), [`notebooks/`](notebooks), [`backend/`](backend), [`frontend/`](frontend)): MIT.
- **Data and documentation** ([`data/`](data), [`docs/`](docs)): Creative Commons Attribution 4.0 (CC-BY 4.0), so the dataset is freely reusable and citable with attribution.

Full text: [`LICENSE`](LICENSE).

## Citing this work

A versioned release will be archived on Zenodo with a DOI (see [`CITATION.cff`](CITATION.cff)). Until then, cite the repository directly. A Country Profile draft for *International Journal of Sport Policy and Politics* is in [`manuscript/`](manuscript).

## Setup

See [`SETUP.md`](SETUP.md) for Colab and Termux commands to run the analysis, the data builders, and the classifier trainer. See [`DEPLOYMENT.md`](DEPLOYMENT.md) for standing up your own copy of the live API and dashboard.

## Status

- **Medal spine** — complete and verified. [`medals_by_games.csv`](data/medals_by_games.csv) and all 39 golds in [`golds.csv`](data/golds.csv) are done.
- **Per-medal expansion** — [`all_medals.csv`](data/all_medals.csv) holds the 39 verified golds plus sourced anchor rows; the remaining silver/bronze rows are completed by running [`data/build_all_medals.py`](data/build_all_medals.py) against source (a committed, reproducible scraper — chosen over hand transcription precisely to avoid memory-based errors). Running it requires network access.
- **Geospatial** — [`data/geo/`](data/geo) ships a factual county reference and a verified origin seed; [`build_medalist_origins.py`](data/build_medalist_origins.py) enriches per-athlete birthplaces from Wikipedia infoboxes, mapping to counties and flagging (never guessing) anything it can't confidently place. Now cross-referenced against a published talent-origin study.
- **Governance framework** — the SGO/NSGO structure is adopted and committed ([`data/sgo_framework.json`](data/sgo_framework.json)); full indicator-by-indicator scoring of Athletics Kenya/ADAK against all four dimensions is the next data-collection task.
- **ML pipeline** — trains on a real labelled news corpus with honest, reproducible evaluation ([`nlp/README.md`](nlp/README.md) has the full comparison of what was tried). Growing the corpus (especially the thin classes) is the top open task.
- **Controversies / policy / funding** — schema v0.2, 12 sourced records spanning 2015-2026; will keep growing, partly via the NLP pipeline's human-reviewed proposals.
- **Live API and dashboard** — deployed and verified working end to end (Render + Vercel, free tier, CORS locked to the dashboard's origin).

Two builders ([`build_all_medals.py`](data/build_all_medals.py), [`build_medalist_origins.py`](data/build_medalist_origins.py)) need a networked environment to run; they're written to run in Termux or any Python environment. Contributions welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md).

