# NLP pipeline

The ML core: turn a stream of real news coverage into structured, reviewable
additions to `data/controversies.json` instead of curating that file by hand.

## Files

- `data/corpus_labels.jsonl` — the REAL labelled corpus. Each line is an actual
  published article (URL, source, date, label) plus a one-line original summary
  written for this project. No copyrighted article body is committed.
- `collect_corpus.py` — fetches article full text at runtime, in parallel across
  domains (sequential within a domain), respecting robots.txt and rate limits.
  Caches to `data/medals_raw/news/` (gitignored).
- `train.py` — trains and evaluates the classifier, saves `model.pkl`.
- `controversy_classifier.py` — inference wrapper. `load_trained()` loads the
  trained model; predictions below a confidence threshold route to human review.

## Run it

    python nlp/train.py                  # LOO eval on summaries, fit + save
    python nlp/collect_corpus.py          # optional: fetch full text
    python nlp/train.py --use-full-text    # reproduce the weaker full-text result
    python nlp/train.py --kfold            # 2-fold instead of leave-one-out

## Two findings worth stating plainly

**1. Curated summaries beat full scraped articles, by a lot.**

Same pipeline, same 22 items, only the training text differs (2-fold CV):

| Training text | Accuracy |
|---|---|
| Committed one-line summaries | 0.59 |
| Full article text where available | 0.45 |

Full text *lost* 14 accuracy points. The cause is signal dilution and it's
visible in the data: the Wikipedia article labelled `anti_doping_governance`
runs ~5,500 characters, of which roughly 200 concern the WADA ruling — the rest
is delegation size, rugby sevens, archery, javelin throwers. TF-IDF weights
every term, so full text teaches the model that "rugby sevens" predicts
anti-doping governance. A one-line summary is almost pure signal. At n=22 the
dilution outweighs the extra information.

This is why summaries are the default. `--use-full-text` reproduces the weaker
result rather than hiding it.

**2. ComplementNB substantially beats logistic regression on imbalanced text.**

Leave-one-out CV, summary corpus:

| Model | Accuracy | Macro-F1 |
|---|---|---|
| tfidf(1,2) + LogisticRegression C=4 (original) | 0.455 | 0.243 |
| tfidf(1,2) + ComplementNB alpha=0.2 (current) | **0.636** | **0.566** |

Macro-F1 more than doubled. Four of six classes went from zero recall to
non-zero; `politics_geopolitics` reached 1.00 F1 and `athlete_migration` 0.67.
Complement Naive Bayes was designed for exactly this situation — imbalanced text
corpora — where the largest class (8 items) is four times the smallest (2).

Model selection used macro-F1, not accuracy, on purpose: accuracy on an
imbalanced set rewards a classifier that just predicts the majority class.

Evaluation is leave-one-out by default. With 2 items in the smallest class,
k-fold caps at k=2, which trains each fold on half a tiny corpus and gives
unstable, pessimistic numbers.

## Honest remaining limits

`athlete_welfare_gender` still scores 0.00 — two training examples is not
enough for the model to learn it, and no amount of tuning fixes that. Growing
the corpus, especially the thin classes, remains the highest-leverage task and
no model change substitutes for it.

## Path forward

1. **Grow the corpus** — priority is the three thinnest classes.
2. **Re-evaluate** — watch per-class recall on those classes.
3. **Revisit full text** — with a much larger corpus, or with extraction that
   targets the label-relevant passage rather than the whole page, full text
   should eventually overtake summaries. It does not yet, and this repo reports
   that rather than assuming it.
4. **Swap the model** — a fine-tuned transformer once the labelled set justifies
   it. The `ControversyClassifier` interface is unchanged.
5. **Human-in-the-loop writes** — above-threshold auto-labels become PROPOSED
   `controversies.json` records in a pull request; a person confirms before merge.
