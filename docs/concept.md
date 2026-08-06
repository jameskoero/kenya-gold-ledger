# Kenya at Gold: An Open Data & Policy Archive of Kenyan Olympic Excellence

### Concept Document — v2.0 (post-audit revision)

**Scope decisions locked in:** golds + full medal record for context · bilingual English/Swahili · open to contributors from day one.

---

## 1. What the landscape audit found

Before reframing anything, it's worth being honest about what already exists, because a chunk of this space is genuinely crowded.

**Olympic datasets are a saturated GitHub/Kaggle category.** The "120 years of Olympic History" Kaggle dataset (sourced from Olympedia.org) has spawned dozens of repos — KeithGalli's `Olympics-Dataset` (scraped athlete bios + results, 1896–2022), `olympic-history-dataset`, half a dozen Streamlit/Power BI dashboards doing age/gender/medal-count breakdowns. None of them are Kenya-specific, and none go past "here's a chart of medals by country." That's the opening: **the data exists globally, but nobody has built the Kenya-specific, policy-annotated version of it.**

**The academic literature on Kenyan running exists — but it's answering a different question.** Onywera & Pitsiladis (2006, *Journal of Sports Sciences*), Wilber & Pitsiladis (2012), and Tucker, Onywera & Santos-Concejero's *Analysis of the Kenyan Distance-Running Phenomenon* (2015) are the foundational papers here, and they're rigorous — but they're asking "why are Kenyans, and specifically Kalenjin/Nandi runners, physiologically and socioculturally dominant." That's a sports-science and genetics-adjacent question. **Nobody in that literature is asking the governance question**: what happens to the money, who gets exploited, what does the state actually do with its cut of the reputational capital, and where's the accountability trail. That's the gap this project should own.

**The governance and welfare material is real, current, and richly documented — but scattered across news archives, not structured anywhere.** This audit pulled concrete, sourced incidents that should anchor the controversies dataset from day one (all verifiable, none synthetic):

- **The Nike/Athletics Kenya funds diversion (2015–2018):** IAAF Ethics Board found AK president Isaiah Kiplagat, VP David Okeyo, and treasurer Joseph Kinyua diverted Nike sponsorship "honorarium" payments — including a $500,000 commitment bonus — into a personal-benefit "Clearance Account." Okeyo received a lifetime ban in 2018. [Sports Integrity Initiative](https://www.sportsintegrityinitiative.com/senior-officials-at-athletics-kenya-diverted-nike-payments/), [BBC](https://feeds.bbci.co.uk/sport/athletics/34826145).
- **Rio 2016 chef de mission theft charges:** Stephen Arap Soi charged with stealing KES 25.6 million ($256,000) meant for athlete accommodation; two other officials charged over misappropriated Nike-supplied uniforms. [BBC](https://feeds.bbci.co.uk/news/world-africa-37494559).
- **The 2021 Hassan Wario conviction:** Kenya's then-Sports Cabinet Secretary was convicted for diverting KES 58 million in Rio Olympic preparation funds, sentenced to six years (commuted to a KES 50 million fine). This is a first-order governance-accountability data point most casual coverage of "Kenya at the Olympics" completely omits.
- **WADA non-compliance and the 2016 eligibility crisis:** Kenya's anti-doping body was declared non-compliant with the WADA Code in mid-2016, forcing individual-athlete eligibility review by World Athletics just before Rio. [Wikipedia — Kenya at the 2016 Olympics](https://en.wikipedia.org/wiki/Kenya_at_the_2016_Summer_Olympics).
- **The doping-poverty economy:** Athletics Integrity Unit head Brett Clothier's framing — Kenya's problem is a uniquely large "pyramid" of sub-elite professional-grade runners for whom road-race prize money creates doping incentive, distinct from state-sponsored doping models like Russia's. Kenya committed $5M/year for five years to its own anti-doping overhaul after threats of an outright ban. Over 140–180+ Kenyan athletes sanctioned since 2016. [The Hill/AP](https://thehill.com/homenews/ap/ap-sports/ap-kenyas-crisis-is-unique-and-driven-by-poverty-track-and-fields-anti-doping-head-tells-the-ap/).
- **Gendered welfare and violence:** The 2021 murder of world-record-pace runner Agnes Tirop by her husband put a spotlight on financial exploitation of female athletes by coaches, agents, and family — women athletes reported as carrying "the burden of the whole family" as primary breadwinners. This belongs in the welfare pillar, sourced and handled carefully, not as a headline hook.
- **Current-state government response (useful as the "what's changing now" thread):** Kenya's 2025/26 budget allocated KES 16.69 billion to sport, including KES 241 million to ADAK and KES 245 million to the Kenya Academy of Sports; a revised National Sports Policy (approved April 2025) raised Olympic gold-medal bonuses from $5,800 to $23,200, alongside new mental-health, medical, and post-career transition support commitments. [People Daily](https://peopledaily.digital/business/kenya-unveils-record-sports-funding-in-2025-26-budget), [Pan African Visions](https://panafricanvisions.com/2025/11/kenya-sports-rising-as-government-steps-up-support/).

This is the actual raw material — every figure above is sourced and should go straight into `policy_timeline.csv` and `controversies.json` with citations attached, not paraphrased from memory later.

## 2. Reframed positioning

Given the audit, the project's honest pitch changes from "a comprehensive Kenya Olympics archive" (broad, slightly generic) to something sharper:

> **The first open, structured, source-linked dataset connecting Kenya's Olympic medal record to its governance failures and athlete welfare outcomes — built to be queried, visualized, modeled, and cited, not just read.**

That reframing does three things: it differentiates from the existing physiology literature, it differentiates from the generic Kaggle/GitHub Olympic-dashboard genre, and it gives the project an actual empirical spine (funding vs. medal output vs. scandal timing) instead of just being a well-organized Wikipedia mirror.

## 3. What to add, cut, or change from v0.1

**Add:**
- A `funding_vs_output.csv` table mapping government/Sports Kenya/ADAK budget allocations by year against medal counts and doping-sanction counts — this is the empirical core that makes the "gaps" pillar analytical rather than descriptive.
- A **geographic layer**: birthplace/training-camp county for each medalist, to visualize (not re-litigate) the Rift Valley/Kalenjin concentration already established in the Tucker et al. literature — but tied to *your* open dataset instead of citing their closed one.
- An **NLP/text-mining component**: scrape and classify a corpus of Kenyan and international news coverage (Nation, Standard, BBC, Reuters, World Athletics) by controversy type and year, to auto-populate and continuously update the controversies timeline instead of manually curating it forever. This is also the most "ML" part of the project and the part most defensible as a genuine open-source technical contribution, not just a data-entry exercise.
- A short **literature review document** in `docs/` explicitly citing Onywera, Pitsiladis, Tucker et al. — cite them precisely to show you know the existing field and are deliberately building the adjacent, unaddressed layer.
- **Explicit citation/confidence metadata already planned in v0.1** — keep it, it's the single most important design choice for eventual peer review.

**Cut or de-scope:**
- Don't try to be the definitive source on *why* Kenyans are physiologically dominant — that's someone else's decades-deep literature. Reference it, don't re-derive it.
- Don't attempt full coverage of every sport with zero Kenyan Olympic gold (rugby sevens, boxing, etc.) as a symmetrical pillar — treat "why hasn't this diversified" as a short analytical note inside the gaps pillar, not its own dataset.

## 4. The ML/data-science layer, concretely

Since the ambition is a genuine ML open-source contribution and not just a curated CSV, here's what actual modeling work looks like on this dataset — all defensible on real, non-synthetic data:

- **Trend/time-series analysis**: medal count, doping-sanction count, and funding allocation over time, to identify lagged relationships (does a funding bump follow a scandal, or precede a medal surge?).
- **Text classification**: a lightweight classifier (even a fine-tuned small transformer or a well-engineered TF-IDF + logistic regression baseline is legitimate and citable) to tag scraped news articles by controversy category — corruption, doping, welfare, gender, governance reform.
- **Geospatial clustering**: county-of-origin clustering of medalists against county-level development/education indicators (KNBS data is public) — careful, correlational framing only, explicitly not a genetic or ethnic-determinism claim.
- **Network analysis**: officials, federations, and sanctioned athletes as a graph, to visualize how few names recur across multiple scandals (Kiplagat/Okeyo/Kinyua all appear across the Nike case; useful for showing institutional concentration of governance failure).

## 5. Repo architecture (revised)

```
kenya-olympic-gold/
├── data/
│   ├── medals_raw/            # unprocessed pulls: Olympedia, Wikipedia, IOC
│   ├── medals_clean.csv       # canonical, versioned medal dataset (gold + full record)
│   ├── controversies.json     # structured, sourced incident records
│   ├── policy_timeline.csv    # government/regulatory actions + budget figures by year
│   ├── funding_vs_output.csv  # budget/medal/sanction cross-table
│   └── geo/                   # medalist birthplace/training-camp county data
├── nlp/                       # news-scraping + controversy classifier pipeline
├── notebooks/                 # trend analysis, funding-output correlation, geospatial
├── viz/                       # exported charts + dashboard (Streamlit or Observable)
├── docs/
│   ├── narrative/             # long-form pillar write-ups, EN + SW
│   ├── literature-review.md   # positions this repo against Onywera/Pitsiladis/Tucker
│   └── methodology.md
├── sources/                   # citation manifest, archived links (Wayback)
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── LICENSE                    # CC-BY for data/docs, MIT for code
```

## 6. Publication strategy — made competitive, not aspirational

Two realistic, distinct submission tracks rather than one vague "publish it somewhere":

**Track A — the dataset itself, as a citable artifact.** Release `medals_clean.csv` + `controversies.json` + `policy_timeline.csv` on Zenodo with a DOI (you already have Zenodo experience from Titanic). This alone is citable by other researchers before any narrative paper exists — it's the fastest path to the project being "real" in an academic sense.

**Track B — the analytical paper.** Best-fit target: **International Journal of Sport Policy and Politics** (Taylor & Francis, CiteScore 3.3, SJR Q1 Social Sciences, IF ~2.82). Confirmed direct fit: the journal explicitly solicits work on *"the role and influence of national and sub-national government in relation to sport policy"* and *"the significance of government as regulator, resource provider and competitor."* It also runs a lower-barrier **Country Profile** track specifically meant to document a country's sport-policy landscape — a realistic first submission while the full research article matures. [Journal scope](https://www.tandfonline.com/journals/risp20/about-this-journal).

Secondary target for the welfare/gender angle specifically: **Journal of Sport and Social Issues** — better fit for the Agnes Tirop / athlete-exploitation material than a policy journal, since it's explicitly a social-issues venue rather than a policy-mechanics one.

**What makes this competitive rather than a diary of scandals**: the funding-vs-output empirical layer (§4) is what turns this from "a well-written summary of things that happened" into something with a testable claim a reviewer can evaluate — e.g., "governance scandals cluster in pre-Games years and are followed by short-lived funding increases with no structural reform," tested against your own dataset. Reviewers for a policy journal want a mechanism and an evidence base, not a chronology.

## 7. Phased roadmap (updated)

1. **Phase 0 — Spine:** `medals_clean.csv`, all Kenyan Olympic medals (not just gold) 1964–present, sourced from Olympedia/IOC/Wikipedia cross-checks.
2. **Phase 1 — Controversies + policy timeline:** seed directly from the sourced incidents in §1 above; structure, don't summarize.
3. **Phase 2 — Funding-vs-output table + first trend charts.**
4. **Phase 3 — NLP pipeline** for ongoing controversy classification from news corpus.
5. **Phase 4 — Geospatial + network analysis notebooks.**
6. **Phase 5 — Zenodo dataset release (Track A).**
7. **Phase 6 — Manuscript draft for IJSPP Country Profile → full research article (Track B).**

---

**One open question before build starts:** for the NLP news-scraping component, do you want to build the scraper yourself against public archives, or start from static, manually-collected article sets to avoid scraping/ToS complications with Kenyan news sites early on?
