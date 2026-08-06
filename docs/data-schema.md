# Data schema

## `data/golds.csv` — the highlighted dataset

Each row is one gold medal, treated as a discrete earning.

| field | type | description |
|---|---|---|
| `medal_id` | string | Stable ID, form `G{year}-{seq}` |
| `games_year` | int | Olympic year |
| `host_city` | string | Host city |
| `sport` | string | Sport (Athletics / Boxing) |
| `event` | string | Event name |
| `sex` | enum | `M` / `W` |
| `athlete_or_team` | string | Individual, or "Kenya (relay)" for relays |
| `result` | string | Time/mark where available |
| `is_relay` | bool | True for relay golds |
| `relay_members` | string | Semicolon-separated members if relay |
| `record_at_time` | string | `WR` / `OR` if set at the time, else blank |
| `reallocated` | bool | True if awarded after another athlete's disqualification |
| `notes` | string | Context, caveats, cross-references |
| `confidence` | enum | `high` / `medium` / `low` |
| `source` | string | Provenance |

## `data/medals_by_games.csv` — the spine

| field | type | description |
|---|---|---|
| `games_year` | int | Olympic year |
| `host_city` | string | Host city |
| `season` | string | Summer / Winter |
| `gold`, `silver`, `bronze`, `total` | int | Medal counts (blank for boycotted Games) |
| `olympedia_edition_id` | int | Cross-reference to Olympedia |
| `notes` | string | Context |
| `source` | string | Provenance |

## `data/controversies.json`

Top-level `records` array. Each record:

| field | description |
|---|---|
| `id` | Stable ID |
| `year_range` | Single year or range |
| `category` | `governance_corruption`, `doping`, `anti_doping_governance`, `athlete_welfare_gender`, `politics_geopolitics`, `athlete_migration` |
| `title`, `summary` | Human-readable |
| `people_implicated` | Array; empty where none named |
| `outcome` | Resolution / sanction / rebuttal |
| `linked_medalists` | Cross-references into `golds.csv` where relevant |
| `confidence` | `high` / `medium` / `low` |
| `sources` | Array of URLs |

## `data/policy_timeline.csv`

| field | description |
|---|---|
| `year` | Year of action |
| `event_type` | `institution`, `legislation`, `anti_doping`, `governance`, `strategy`, `policy`, `budget`, `welfare` |
| `description` | What happened |
| `figures` | Monetary/quantitative detail where public |
| `source` | Provenance |

## `data/funding_vs_output.csv`

Per-Games join of medal output against doping context and funding notes — the analytical bridge table for the time-series work described in `methodology.md`.

## Category vocabulary is controlled

The `category` values in `controversies.json` and `event_type` values in `policy_timeline.csv` are closed vocabularies. New categories require a note in this file and a rationale in the pull request, so the NLP classifier's label set stays stable.
