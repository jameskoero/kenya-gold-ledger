# Contributing

This is a research dataset intended to be citable. The sourcing bar is high on
purpose. Contributions are welcome, but they must protect the integrity that
makes the data usable in a publication.

## Non-negotiable rules

1. **No unsourced claims.** Every data row and every controversy record needs a
   `source`. If you can't source it, it doesn't go in.
2. **No synthetic data.** Do not fabricate results, names, dates, or figures to
   fill gaps. A visible gap is better than an invented value.
3. **No anonymous allegations without corroboration.** Governance and doping
   records require an official ruling/court record or two independent reputable
   sources. Record the accused party's response where one exists.
4. **Record disagreement, don't resolve it.** If sources conflict, capture both
   and their provenance (see `docs/methodology.md`).
5. **Handle welfare and violence material with care.** Items like the Agnes
   Tirop case are structural welfare evidence, not true-crime content. Keep the
   framing sober and sourced.
6. **Respect the controlled vocabularies.** New `category` or `event_type`
   values require a note in `docs/data-schema.md` and a rationale in the PR.

## Workflow

- Open an issue describing the addition or correction before large changes.
- One logical change per pull request.
- If you touch `data/`, re-run `python notebooks/01_medal_analysis.py` and
  confirm the figures still regenerate cleanly.
- Auto-labelled NLP output is proposed as PR records for human confirmation —
  never committed directly to `controversies.json`.

## What's especially wanted

- Expanding silver and bronze medals to per-medal rows (currently Games-level).
- Verified medalist birthplace/training-camp county data for the geospatial layer.
- A properly collected, labelled news corpus for the classifier.
