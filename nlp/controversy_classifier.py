"""
controversy_classifier.py
-------------------------
A transparent baseline for classifying news text about Kenyan athletics into
the project's controlled controversy vocabulary. The interface is
model-agnostic: the TF-IDF + logistic-regression baseline here can be swapped
for a fine-tuned transformer without changing how the rest of the pipeline
calls it.

The label set is the controlled vocabulary from docs/data-schema.md:
    governance_corruption, doping, anti_doping_governance,
    athlete_welfare_gender, politics_geopolitics, athlete_migration

Design principles:
  * No synthetic training data shipped. The seed set below is a small,
    hand-labelled set of REAL summaries drawn from controversies.json, used
    only to make the baseline runnable and demonstrable. Real deployment
    requires a properly collected, labelled news corpus (see nlp/README.md).
  * Every prediction returns a probability, so low-confidence auto-labels can
    be routed to human review before touching controversies.json.

Usage:
    python nlp/controversy_classifier.py --demo
    from nlp.controversy_classifier import ControversyClassifier
"""
from __future__ import annotations
import argparse
import json
import pickle
from dataclasses import dataclass
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"

LABELS = [
    "governance_corruption",
    "doping",
    "anti_doping_governance",
    "athlete_welfare_gender",
    "politics_geopolitics",
    "athlete_migration",
]

# Small, REAL, hand-labelled seed set (paraphrased from sourced incidents in
# controversies.json). Purpose: make the baseline runnable end-to-end. This is
# NOT a substitute for a collected corpus.
SEED = [
    ("Athletics Kenya officials diverted Nike sponsorship honorarium payments into a clearance account for personal benefit", "governance_corruption"),
    ("The Olympic team chef de mission was charged with stealing millions meant for athletes accommodation in Rio", "governance_corruption"),
    ("The former sports cabinet secretary was convicted of diverting Olympic preparation funds", "governance_corruption"),
    ("An IAAF council member received a lifetime ban for skimming federation sponsorship money", "governance_corruption"),
    ("The marathon runner was banned after testing positive for the blood booster EPO", "doping"),
    ("More than one hundred and forty Kenyan runners have been sanctioned for doping offences since 2016", "doping"),
    ("A pharmacist in Eldoret admitted selling EPO to runners without prescription", "doping"),
    ("The world record holder was suspended over abnormal biological passport values", "doping"),
    ("Kenya was declared non-compliant with the World Anti-Doping Code before the Rio Games", "anti_doping_governance"),
    ("The government committed five million dollars a year to anti-doping to avoid a blanket ban", "anti_doping_governance"),
    ("The Anti-Doping Agency of Kenya was established to increase testing and education", "anti_doping_governance"),
    ("The killing of a young female runner exposed the financial exploitation of women athletes by relatives and agents", "athlete_welfare_gender"),
    ("Women athletes bear the burden of supporting entire extended families as primary breadwinners", "athlete_welfare_gender"),
    ("A former Olympic champion struggled to pay hospital bills after retirement", "athlete_welfare_gender"),
    ("Kenya boycotted the Montreal Games over New Zealand sporting ties to apartheid South Africa", "politics_geopolitics"),
    ("Kenya joined the United States led boycott of the Moscow Olympics", "politics_geopolitics"),
    ("Kenyan born runners switched allegiance to Bahrain and Qatar for financial incentives", "athlete_migration"),
    ("Some athletes who moved to the Gulf later sought to reclaim Kenyan citizenship", "athlete_migration"),
]


@dataclass
class Prediction:
    label: str
    probability: float
    all_scores: dict


class ControversyClassifier:
    """Model-agnostic wrapper. Swap `._build_model()` for a transformer later."""

    def __init__(self):
        self.pipeline: Pipeline | None = None

    def _build_model(self) -> Pipeline:
        return Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
            ("clf", LogisticRegression(max_iter=1000, C=4.0)),
        ])

    def fit(self, texts, labels):
        self.pipeline = self._build_model()
        self.pipeline.fit(texts, labels)
        return self

    def fit_seed(self):
        """Train on the tiny in-code seed set. For a quick demo only —
        prefer the real corpus via `nlp/train.py`, then `load_trained()`."""
        texts = [t for t, _ in SEED]
        labels = [y for _, y in SEED]
        return self.fit(texts, labels)

    @classmethod
    def load_trained(cls):
        """Load the model trained on the real corpus by nlp/train.py.

        Run `python nlp/train.py` first to produce model.pkl. Falls back with a
        clear error if it isn't there yet."""
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "model.pkl not found. Run `python nlp/train.py` to train on the "
                "real corpus (data/corpus_labels.jsonl) first."
            )
        inst = cls()
        with open(MODEL_PATH, "rb") as f:
            inst.pipeline = pickle.load(f)
        return inst

    def predict(self, text: str, review_threshold: float = 0.55) -> Prediction:
        if self.pipeline is None:
            raise RuntimeError("Call fit()/fit_seed() first.")
        classes = list(self.pipeline.named_steps["clf"].classes_)
        probs = self.pipeline.predict_proba([text])[0]
        scores = {c: round(float(p), 4) for c, p in zip(classes, probs)}
        top = max(scores, key=scores.get)
        return Prediction(label=top, probability=scores[top], all_scores=scores)

    @staticmethod
    def needs_human_review(pred: Prediction, threshold: float = 0.55) -> bool:
        """Low-confidence predictions must be reviewed before writing to data."""
        return pred.probability < threshold


def _demo():
    clf = ControversyClassifier().fit_seed()
    samples = [
        "A steeplechase medallist was handed a three year ban after a positive test for a masking agent",
        "The federation president was accused of pocketing money paid by the kit sponsor",
        "A retired champion says she was left with nothing after her manager took most of her prize money",
        "Athletes born in Kenya are increasingly competing under Gulf state flags",
    ]
    print("== Controversy classifier demo (baseline, seed-trained) ==\n")
    for s in samples:
        p = clf.predict(s)
        flag = "  <-- REVIEW" if ControversyClassifier.needs_human_review(p) else ""
        print(f"text : {s}")
        print(f"label: {p.label}  (p={p.probability}){flag}")
        print(f"top3 : {dict(sorted(p.all_scores.items(), key=lambda kv: -kv[1])[:3])}\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="Run the seed-trained demo")
    args = ap.parse_args()
    if args.demo:
        _demo()
    else:
        print("Import ControversyClassifier, or run with --demo. See nlp/README.md.")
