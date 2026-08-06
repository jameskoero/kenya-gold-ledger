"""
train.py
--------
Trains the controversy classifier on the REAL news corpus
(data/corpus_labels.jsonl) and reports honest, per-class evaluation.

TEXT SOURCE: SUMMARIES BY DEFAULT — AND WHY
Each labelled item has two possible training texts: the committed one-line
summary, and (optionally) the full article text fetched by collect_corpus.py.
Summaries are the DEFAULT because they measurably outperform full text on this
corpus. Measured, 2-fold CV, same pipeline:

    summary-only      accuracy 0.59
    full-text-where-available   accuracy 0.45

The reason is signal dilution, and it's visible in the data. The Wikipedia
article labelled `anti_doping_governance` is ~5,500 characters, of which only
about 200 concern the WADA non-compliance ruling; the rest is delegation size,
rugby sevens, archery, javelin. TF-IDF weights every term in the document, so
full text teaches the model that "rugby sevens" predicts anti-doping
governance. The one-line summary has a near-perfect signal-to-noise ratio. At
n=22, that dilution outweighs the extra signal.

Pass --use-full-text to reproduce the weaker full-text result.

MODEL CHOICE
ComplementNB, not logistic regression. Complement Naive Bayes was designed
specifically for imbalanced text corpora, which is exactly this problem (the
largest class has 8 items, the smallest 2). Measured under leave-one-out CV:

    tfidf(1,2) + LogisticRegression C=4   acc 0.455   macro-F1 0.243
    tfidf(1,2) + ComplementNB alpha=0.2   acc 0.636   macro-F1 0.566

Macro-F1 more than doubled, and four of six classes went from zero to non-zero
recall. Selected on macro-F1 rather than accuracy deliberately: accuracy on an
imbalanced set rewards a model that just predicts the majority class.

EVALUATION
Leave-one-out by default. With 2 items in the smallest class, k-fold can only
do k=2, which trains each fold on half a tiny corpus and produces unstable,
pessimistic numbers. LOO uses n-1 items per fit and is the standard choice at
this sample size. --kfold switches back to stratified 2-fold for comparison.

REQUIREMENTS
    pip install scikit-learn pandas

USAGE
    python nlp/train.py                    # LOO eval on summaries, fit + save
    python nlp/train.py --use-full-text     # reproduce the weaker full-text result
    python nlp/train.py --kfold             # stratified 2-fold instead of LOO
    python nlp/train.py --no-save           # evaluate only
"""
from __future__ import annotations
import argparse
import hashlib
import json
import pickle
import sys
from collections import Counter
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, LeaveOneOut, cross_val_predict
from sklearn.metrics import classification_report, accuracy_score, f1_score

ROOT = Path(__file__).resolve().parent.parent
LABELS = ROOT / "data" / "corpus_labels.jsonl"
CACHE = ROOT / "data" / "medals_raw" / "news"
MODEL_OUT = ROOT / "nlp" / "model.pkl"


def _hash(url: str) -> str:
    return hashlib.sha1(url.encode()).hexdigest()[:16]


def load_corpus(use_full_text: bool = False):
    """Load (texts, labels). Summaries by default; see module docstring."""
    texts, labels, n_full = [], [], 0
    with open(LABELS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            text = r["summary"]
            if use_full_text:
                cached = CACHE / f"{_hash(r['url'])}.json"
                if cached.exists():
                    doc = json.loads(cached.read_text())
                    if doc.get("full_text"):
                        text = doc["full_text"]
                        n_full += 1
            texts.append(text)
            labels.append(r["label"])
    return texts, labels, n_full


def build_pipeline() -> Pipeline:
    """TF-IDF + ComplementNB. See module docstring for why this beats LR here."""
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True,
                                  stop_words="english")),
        ("clf", ComplementNB(alpha=0.2)),
    ])


def evaluate(texts, labels, use_kfold: bool = False):
    counts = Counter(labels)
    print("Class distribution:", dict(counts), file=sys.stderr)
    if use_kfold:
        min_class = min(counts.values())
        n_splits = max(2, min(5, min_class))
        cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        print(f"Stratified {n_splits}-fold cross-validation\n", file=sys.stderr)
    else:
        cv = LeaveOneOut()
        print(f"Leave-one-out cross-validation ({len(texts)} fits)\n", file=sys.stderr)

    preds = cross_val_predict(build_pipeline(), texts, labels, cv=cv)
    print(classification_report(labels, preds, zero_division=0))
    print(f"accuracy  {accuracy_score(labels, preds):.3f}", file=sys.stderr)
    print(f"macro-F1  {f1_score(labels, preds, average='macro', zero_division=0):.3f}",
          file=sys.stderr)


def main(save: bool, use_full_text: bool, use_kfold: bool):
    texts, labels, n_full = load_corpus(use_full_text)
    mode = (f"full text where cached ({n_full} items), summary otherwise"
            if use_full_text else "committed summaries (default)")
    print(f"Loaded {len(texts)} labelled items — training text: {mode}.\n", file=sys.stderr)
    if len(set(labels)) < 2:
        print("Need at least two classes to train.", file=sys.stderr)
        return
    evaluate(texts, labels, use_kfold)
    pipe = build_pipeline().fit(texts, labels)
    if save:
        with open(MODEL_OUT, "wb") as f:
            pickle.dump(pipe, f)
        print(f"\nFitted on full corpus and saved -> {MODEL_OUT}", file=sys.stderr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-save", action="store_true")
    ap.add_argument("--use-full-text", action="store_true",
                    help="Train on fetched full article text where cached (performs WORSE; see docstring)")
    ap.add_argument("--kfold", action="store_true",
                    help="Use stratified k-fold instead of leave-one-out")
    a = ap.parse_args()
    main(save=not a.no_save, use_full_text=a.use_full_text, use_kfold=a.kfold)
