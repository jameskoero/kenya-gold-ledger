# Methodology

## Sourcing hierarchy

Data is admitted in this order of preference:

1. **Primary statistical sources** — Olympedia (maintained by the OlyMADMen statisticians), IOC official results, World Athletics records. The medal spine (`medals_by_games.csv`, `golds.csv`) is built on these.
2. **Primary institutional sources** — ADAK/WADA/AIU disclosures, Kenyan government budget documents and strategic plans (e.g. the Ministry of Sports 2023-2027 Strategic Plan), IAAF/World Athletics ethics rulings, court and tribunal records.
3. **Reputable secondary reporting** — BBC, Reuters, AP, the Sports Integrity Initiative, Nation, Standard, and specialist athletics outlets, used for narrative and controversy detail with explicit attribution.

Forums, unsourced blogs, and social media are not admissible as primary evidence.

## The confidence model

Every record in `controversies.json` carries a `confidence` value:

- **high** — corroborated by two or more independent reputable sources, or by an official ruling/court record.
- **medium** — reported by a single reputable source, or well-established but with contested details.
- **low** — credible but thinly documented; flagged for follow-up before any publication use.

Confidence reflects **strength of documentation, not editorial endorsement**. A high-confidence record of an *allegation* means the allegation is well-documented, not that guilt is established. Where an accused party has responded, the response is recorded in the same entry.

## Recording disagreement instead of resolving it

Sources genuinely conflict on Kenya's aggregate medal counts. Olympedia's "medals by sport" table gives **39 gold / 45 silver / 40 bronze** (Athletics 38-44-35 plus Boxing 1-1-5). Some Wikipedia summary tables give **39 / 44 / 41**. The difference arises from how relay/team medals and one boxing medal are counted across the two systems. This project **records both figures and their provenance** rather than picking one; `medals_by_games.csv` follows Olympedia's per-Games breakdown, which sums to the Olympedia totals.

The same principle applies to contested doping and corruption cases: the dataset stores the claim, the source, the outcome, and any documented rebuttal.

## The "each medal is an earning" principle

The user-facing design treats every medal as a discrete, separately catalogued unit rather than as a number in a tally. Gold medals receive the fullest treatment (`golds.csv`: athlete, event, result, record status, reallocation flag, and contextual note per row) because the gold is the unit around which national narrative, reward policy, and welfare consequences are organised. Silver and bronze are captured at Games level in `medals_by_games.csv` and will be expanded to per-medal rows as the dataset matures.

## Handling reallocated and later-tainted medals

Two golds carry special flags:

- **Asbel Kiprop, 2008 1500m** — originally silver, elevated to gold after winner Rashid Ramzi (Bahrain) was stripped for CERA. `reallocated = TRUE`.
- **Jemima Sumgong, 2016 marathon** — won clean at the Games; her 2017 out-of-competition EPO ban did **not** strip the Olympic title. Recorded as a retained gold with a linked note in `controversies.json`.

These are recorded factually, without moralising, and cross-referenced between `golds.csv` and `controversies.json`.

## Reproducibility

All published figures are generated from the CSVs by `notebooks/01_medal_analysis.py`. No figure contains a hand-entered number. Re-running the script after any data update regenerates the analytics, so the visuals can never silently drift from the data.

## Roadmap for analytical rigour (toward publication)

1. **Time-series** — align funding allocations, medal counts, and doping-sanction counts by year to test lagged relationships (e.g. do funding increases follow scandals rather than precede medal surges?).
2. **Geospatial** — medalist birthplace/training-camp county against public KNBS county development and education indicators. Framed strictly as correlational and explicitly **not** as a genetic or ethnic-determinism claim; that terrain is already covered, and contested, in the existing physiology literature.
3. **Network analysis** — officials, federations, and sanctioned athletes as a graph, to quantify how concentrated governance failure is among a small recurring set of actors.

Each analytical claim intended for the manuscript must be reproducible from committed data and code.
