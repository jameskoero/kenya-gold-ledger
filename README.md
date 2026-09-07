# 🏅 Kenya at Gold: The Governance Ledger

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ComplementNB-F7931E?style=for-the-badge)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-C9A84C?style=for-the-badge)](LICENSE)
[![Data](https://img.shields.io/badge/Data-100%25%20Open%20(CC--BY--4.0)-2ECC71?style=for-the-badge)](data)

[![Docs](https://img.shields.io/badge/API%20Docs-Swagger-85EA2D?style=flat-square&logo=swagger&logoColor=black)](https://kenya-gold-ledger-api.onrender.com/docs)
[![Live API](https://img.shields.io/badge/Live%20API-Render-46E3B7?style=flat-square&logo=render)](https://kenya-gold-ledger-api.onrender.com)
[![Dashboard](https://img.shields.io/badge/Dashboard-Live%20on%20Vercel-000000?style=flat-square&logo=vercel)](https://kenya-gold-ledger.vercel.app)
[![Governance Framework](https://img.shields.io/badge/Governance-SGO%2FNSGO%20aligned-1E2327?style=flat-square)](data/sgo_framework.json)

**An open, structured, source-linked dataset connecting Kenya's Olympic medal record to its governance, doping, welfare, and policy history — cross-referenced against the peer-reviewed Sports Governance Observer framework, served live as an API and dashboard, not just static files.**

> Every medal individually catalogued. Every controversy sourced, dated, and confidence-rated. **No synthetic data anywhere** — where a value isn't verifiable from a real source, it's flagged, not invented.

---

## 🔴 Live Deployments

| Service | URL | Status |
|---|---|---|
| **API** | [kenya-gold-ledger-api.onrender.com/docs](https://kenya-gold-ledger-api.onrender.com/docs) | ✅ Live — Python (FastAPI) on Render |
| **SGO Governance Framework endpoint** | [`/governance/sgo-framework`](https://kenya-gold-ledger-api.onrender.com/governance/sgo-framework) | ✅ Live — 4 dimensions |
| **Controversies endpoint** | [`/governance/controversies`](https://kenya-gold-ledger-api.onrender.com/governance/controversies) | ✅ Live — 12 sourced records |
| **Dashboard** | [kenya-gold-ledger.vercel.app](https://kenya-gold-ledger.vercel.app) | ✅ Live — static, fetches from the API in real time |

> ⚠️ The API runs on Render's free tier — first request after idle may take 30–60s to cold-start. Subsequent requests return quickly.

**Confirmed root response** (`GET /`):
```json
{
  "name": "Kenya at Gold: The Governance Ledger -- API",
  "repo": "https://github.com/jameskoero/kenya-gold-ledger",
  "docs": "/docs",
  "endpoints": [
    "/medals/by-games", "/medals/golds", "/medals/all",
    "/governance/controversies", "/governance/policy-timeline",
    "/governance/scorecard", "/governance/sgo-framework",
    "/geo/medalist-origins", "/predict/controversy-category"
  ]
}
```

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [What Makes This Different](#-what-makes-this-different)
- [Headline Analytics](#-headline-analytics)
- [Dataset](#-dataset)
- [Architecture](#️-architecture)
- [Project Structure](#-project-structure)
- [Local Setup](#️-local-setup)
- [API Reference](#-api-reference)
- [Live Dashboard](#️-live-dashboard)
- [Governance Framework (SGO/NSGO)](#-governance-framework-sgonsgo)
- [Data Integrity & Sourcing](#-data-integrity--sourcing)
- [Roadmap](#️-roadmap)
- [Author](#-author)
- [License](#-license)

---

## 🌍 Project Overview

Kenya has won **124 Olympic medals** (39 gold, 45 silver, 40 bronze through Paris 2024) — the highest of any African nation, and nearly all of them from distance running. That story is told everywhere. What isn't told, in any single structured place, is the connective tissue: the diverted sponsorship funds, the anti-doping collapse and recovery, the athletes who die broke or violently, the training system that produces world records in villages with no track, and what the state actually does with the reputational capital its runners generate.

This repository is that place — every medal catalogued as a separate earning, gold medals given the highest level of detail, and the whole record cross-referenced against a real, peer-reviewed governance benchmarking methodology instead of an invented metric.

**Coverage:** All Kenyan Olympic medals 1964–2024 · governance/doping/welfare incidents 2015–2026 · SGO/NSGO governance framework applied to Athletics Kenya and ADAK

---

## 🏆 What Makes This Different

I looked. Olympic datasets are common on GitHub and Kaggle; none are Kenya-specific, and none go past medal counts. Sports governance benchmarking exists (Play the Game/KU Leuven's Sports Governance Observer), but it has never been applied to Kenyan athletics specifically.

| # | Feature | Why it's novel |
|---|---|---|
| 1 | **SGO-aligned governance scorecard** ([`data/sgo_framework.json`](data/sgo_framework.json)) | First application of the peer-reviewed SGO/NSGO methodology to Athletics Kenya and ADAK |
| 2 | **Governance network graph** ([`notebooks/02_network_analysis.py`](notebooks/02_network_analysis.py)) | Officials, athletes, and incidents as a graph, so recurrence across scandals is visible |
| 3 | **Governance-vs-medals overlay** ([`notebooks/03_governance_density.py`](notebooks/03_governance_density.py)) | Medal counts and incident density on the same timeline, per Games cycle |
| 4 | **Governance Response Scorecard** ([`notebooks/04_governance_scorecard.py`](notebooks/04_governance_scorecard.py)) | Documented problems vs. documented institutional responses, fully itemised — includes the complete real-world WADA 2025 crisis → 2026 clearance test case |
| 5 | **Live API + dashboard** ([`backend/`](backend), [`frontend/`](frontend)) | Every dataset and the trained ML classifier served over HTTP; dashboard fetches live, never embeds a stale snapshot |

---

## 📊 Headline Analytics

Running [`python notebooks/01_medal_analysis.py`](notebooks/01_medal_analysis.py) regenerates these from the raw CSVs:

| Metric | Value |
|---|---|
| Golds in athletics | **97.4%** (only exception: Robert Wangila's 1988 boxing gold) |
| Golds won by women | **25.6%** — every one since Pamela Jelimo, 2008 |
| Golds in men's 3000m steeplechase | **11 of 39** — most productive single event |
| Best-ever medal haul | **16 medals, Beijing 2008** |
| Joint-best gold count | **6, Beijing 2008 and Rio 2016** |
| Governance response ratio, 2021–2025 era | **1.67** (vs. 0.40 in 2016–2020) |
| Sourced controversy records | **12**, spanning 2015–2026, schema v0.2 |

![Medals per Games](viz/fig1_medals_per_games.png)

---

## 📁 Dataset

All data carries a `source` field and a `confidence` rating. **No synthetic data is used anywhere.**

| File | Description |
|---|---|
| [`golds.csv`](data/golds.csv) | All 39 golds, individually catalogued, verified |
| [`medals_by_games.csv`](data/medals_by_games.csv) | Per-Games totals, 1956–2024 (Olympedia) |
| [`all_medals.csv`](data/all_medals.csv) | Every medal as one row |
| [`controversies.json`](data/controversies.json) | 12 sourced governance/doping/welfare incidents, 2015–2026, schema v0.2 |
| [`sgo_framework.json`](data/sgo_framework.json) | Sports Governance Observer framework, adapted for Athletics Kenya/ADAK |
| [`talent_geography_study.json`](data/talent_geography_study.json) | Published talent-origin study, for validating `medalist_origins.csv` |
| [`policy_timeline.csv`](data/policy_timeline.csv) | Government actions and real budget figures by year |
| [`funding_vs_output.csv`](data/funding_vs_output.csv) | Medals vs. doping context vs. funding, per Games |
| [`governance_scorecard.csv`](data/governance_scorecard.csv) | Output of the transparent scorecard |
| [`corpus_labels.jsonl`](data/corpus_labels.jsonl) | Real labelled news corpus for the ML classifier |
| [`geo/kenya_counties.csv`](data/geo/kenya_counties.csv) · [`geo/medalist_origins.csv`](data/geo/medalist_origins.csv) | County reference and athlete birthplace mapping |

---

## 🏗️ Architecture

```
Static, sourced data (data/*.csv, *.json)
        |
        v
+--------------------------------------------+
|         migrate_to_sqlite.py                |
|   Builds backend/kenya_gold_ledger.db       |
|   from every CSV + JSON file, no invented   |
|   rows -- missing sources are skipped       |
+--------------------------------------------+
        |
        v
+--------------------------------------------+
|              FastAPI (backend/app.py)       |
|   /medals/*  /governance/*  /geo/*          |
|   POST /predict/controversy-category        |
|   (TF-IDF + ComplementNB classifier)        |
+--------------------------------------------+
        |  CORS locked to the dashboard origin
        v
+--------------------------------------------+
|      Static dashboard (frontend/index.html) |
|      Fetches live -- no embedded snapshot   |
+--------------------------------------------+
```

---

## 📂 Project Structure

```
kenya-gold-ledger/
├── data/
│   ├── golds.csv, medals_by_games.csv, all_medals.csv
│   ├── controversies.json          # 12 sourced records, schema v0.2
│   ├── sgo_framework.json          # SGO/NSGO governance framework
│   ├── talent_geography_study.json
│   ├── policy_timeline.csv, funding_vs_output.csv, governance_scorecard.csv
│   ├── corpus_labels.jsonl
│   ├── geo/kenya_counties.csv, geo/medalist_origins.csv
│   ├── build_all_medals.py, build_medalist_origins.py
│
├── backend/
│   ├── app.py                      # FastAPI app -- all live endpoints
│   ├── migrate_to_sqlite.py        # Builds the queryable database
│   ├── requirements.txt, render.yaml
│
├── frontend/
│   ├── index.html                  # Static dashboard, live API-driven
│   ├── vercel.json
│
├── nlp/
│   ├── collect_corpus.py, train.py, controversy_classifier.py
│
├── notebooks/
│   ├── 01_medal_analysis.py
│   ├── 02_network_analysis.py      # Governance network graph
│   ├── 03_governance_density.py    # Medals-vs-incidents overlay
│   ├── 04_governance_scorecard.py  # Transparent scorecard
│
├── docs/
│   ├── methodology.md, literature-review.md, data-schema.md, concept.md
│
├── manuscript/                     # Draft academic publication
├── viz/                            # Generated charts + dashboard.html
├── sources/                        # Citation manifest
├── DEPLOYMENT.md, SETUP.md, CITATION.cff, LICENSE, requirements.txt
└── README.md
```

---

## 🛠️ Local Setup

```bash
# 1. Clone
git clone https://github.com/jameskoero/kenya-gold-ledger.git
cd kenya-gold-ledger

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Build the database from the source data
python backend/migrate_to_sqlite.py

# 4. Start the API
uvicorn backend.app:app --reload
# Docs: http://localhost:8000/docs

# 5. Open the dashboard
# Open frontend/index.html directly in a browser, or serve it statically,
# and point its API base URL field at http://localhost:8000
```

Full Colab and Termux commands (including the data builders and classifier trainer) are in [`SETUP.md`](SETUP.md). Full deployment instructions for standing up your own copy of the live API and dashboard are in [`DEPLOYMENT.md`](DEPLOYMENT.md).

---

## 🔌 API Reference

**Base URL:** [`https://kenya-gold-ledger-api.onrender.com`](https://kenya-gold-ledger-api.onrender.com/docs)

| Endpoint | Method | Description |
|---|---|---|
| `/medals/golds` | GET | All 39 golds; optional `?year=` filter |
| `/medals/all` | GET | Every medal; optional `?medal=Gold\|Silver\|Bronze` filter |
| `/medals/by-games` | GET | Per-Games medal totals |
| `/governance/controversies` | GET | All 12 sourced records; optional `?category=` and `?year_range_contains=` filters |
| `/governance/sgo-framework` | GET | The 4-dimension SGO/NSGO governance framework |
| `/governance/scorecard` | GET | Governance Response Scorecard output |
| `/governance/policy-timeline` | GET | Government policy/funding actions by year |
| `/geo/medalist-origins` | GET | Athlete birthplace to county; optional `?county=` filter |
| `/predict/controversy-category` | POST | Runs the trained classifier on submitted text |

**Example -- `POST /predict/controversy-category`:**

Request:
```json
{ "text": "ADAK suspended 12 more athletes after out-of-competition testing" }
```

Response:
```json
{ "text": "ADAK suspended 12 more athletes after out-of-competition testing", "predicted_category": "doping" }
```

---

## 🖥️ Live Dashboard

**URL:** <https://kenya-gold-ledger.vercel.app>

A static, zero-build dashboard built to show medal history, gold concentration by event, and the governance/controversy timeline -- fetching directly from the live API rather than embedding a snapshot, so it stays current as the dataset grows.

| Feature | Description |
|---|---|
| **Live connection status** | Confirms the configured API base URL is reachable before rendering data |
| **Golds by Games table** | Pulled live from `/medals/golds` |
| **Governance/controversies table** | Pulled live from `/governance/controversies` |
| **SGO framework table** | Pulled live from `/governance/sgo-framework` |

### Stack

```
Frontend  : Static HTML + vanilla JS (no build step)
Hosting   : Vercel (auto-deploy from GitHub main branch)
API       : kenya-gold-ledger-api.onrender.com (FastAPI on Render)
```

---

## 🏛️ Governance Framework (SGO/NSGO)

This project adopts the **Sports Governance Observer / National Sports Governance Observer** methodology (Arnout Geeraert, KU Leuven, for Play the Game / Danish Institute for Sports Studies) -- originally applied to national federations in 15+ countries -- and structures it for Athletics Kenya and ADAK across its four standard dimensions:

| Dimension | What it measures |
|---|---|
| **Transparency** | Public reporting of decisions, finances, testing statistics |
| **Democratic processes** | Free/fair elections, athlete involvement in decisions |
| **Internal accountability and control** | Separation of powers, independent disciplinary processes |
| **Societal responsibility** | Athlete welfare, anti-discrimination, community impact |

Full indicator-by-indicator scoring against all four dimensions is the next open data-collection task -- see [`data/sgo_framework.json`](data/sgo_framework.json) and [`docs/methodology.md`](docs/methodology.md).

---

## 🔒 Data Integrity & Sourcing

> This project uses **100% sourced, verifiable data**. Where a claim can't be confirmed against a real, cited source, it is flagged as a gap rather than filled in.

- ✅ Every row in every dataset carries a `source`
- ✅ Every `controversies.json` record carries a `confidence` rating reflecting strength of public documentation
- ✅ Contested figures (e.g. Olympedia's 39-45-40 vs. some Wikipedia tables' 39-44-41) are recorded as discrepancies, not silently resolved
- ✅ **No synthetic data anywhere** -- reproducible builders ([`build_all_medals.py`](data/build_all_medals.py), [`build_medalist_origins.py`](data/build_medalist_origins.py)) scrape from source rather than being hand-transcribed
- ✅ Creative Commons CC-BY-4.0 -- all data and documentation openly reusable with attribution

See full [`docs/methodology.md`](docs/methodology.md).

---

## 🗓️ Roadmap

- [x] Medal spine -- complete and verified (all 39 golds, full medals-by-Games record)
- [x] Governance/controversy dataset -- schema v0.2, 12 sourced records, 2015-2026
- [x] SGO/NSGO governance framework adopted and structured for Athletics Kenya/ADAK
- [x] ML classifier trained on a real labelled news corpus (TF-IDF + ComplementNB)
- [x] Live FastAPI backend deployed on Render, CORS-locked
- [x] Live static dashboard deployed on Vercel, fetching from the API
- [ ] Full indicator-by-indicator SGO scoring of Athletics Kenya/ADAK
- [ ] Growing the ML training corpus (especially thin classes)
- [ ] Per-medal expansion -- remaining silver/bronze rows via `build_all_medals.py`
- [ ] Zenodo DOI archival
- [ ] Journal submission -- Country Profile, *International Journal of Sport Policy and Politics*

---

## 👤 Author

**James Koero** -- ML Engineer & Researcher | Kisumu, Kenya

[![GitHub](https://img.shields.io/badge/GitHub-jameskoero-181717?style=flat-square&logo=github)](https://github.com/jameskoero) [![LinkedIn](https://img.shields.io/badge/LinkedIn-jameskoero-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/jameskoero)

Academic collaborators:
- **Prof. Samuel Liyala** -- JOOUST, Kenya
- **Prof. Johan Loeckx** -- Vrije Universiteit Brussel (VUB AI Lab), Belgium

---

## 📜 License

- **Code** ([`nlp/`](nlp), [`notebooks/`](notebooks), [`backend/`](backend), [`frontend/`](frontend)): **MIT** -- see [`LICENSE`](LICENSE).
- **Data and documentation** ([`data/`](data), [`docs/`](docs)): **Creative Commons Attribution 4.0 (CC-BY 4.0)**.

A versioned release will be archived on Zenodo with a DOI (see [`CITATION.cff`](CITATION.cff)). Until then, cite the repository directly.

---

*Built in Kisumu, Kenya*
