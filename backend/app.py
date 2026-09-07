"""
Kenya at Gold: The Governance Ledger -- live API
Serves the medal record, governance/controversy data, and the trained
controversy classifier over HTTP.

Run locally:
    uvicorn backend.app:app --reload

Deploy on Render using the accompanying render.yaml.
"""
import sqlite3
import os
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_PATH = os.path.join(os.path.dirname(__file__), "kenya_gold_ledger.db")

app = FastAPI(
    title="Kenya at Gold: The Governance Ledger -- API",
    description=(
        "Open, source-linked API for Kenya's Olympic medal record cross-referenced "
        "against governance, doping, and welfare history, scored against the "
        "Sports Governance Observer (SGO) framework. Data: CC-BY 4.0. Code: MIT."
    ),
    version="1.0.0",
)

# Allow the frontend (deployed separately, e.g. GitHub Pages) to call this API.
# Once live, tighten this to your actual Pages origin, e.g.
# ["https://jameskoero.github.io"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://kenya-gold-ledger.vercel.app"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@contextmanager
def get_db():
    if not os.path.exists(DB_PATH):
        raise HTTPException(
            status_code=503,
            detail="Database not built yet -- run backend/migrate_to_sqlite.py first.",
        )
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def rows_to_dicts(cursor):
    return [dict(row) for row in cursor.fetchall()]


@app.get("/")
def root():
    return {
        "name": "Kenya at Gold: The Governance Ledger -- API",
        "repo": "https://github.com/jameskoero/kenya-gold-ledger",
        "docs": "/docs",
        "endpoints": [
            "/medals/by-games", "/medals/golds", "/medals/all",
            "/governance/controversies", "/governance/policy-timeline",
            "/governance/scorecard", "/governance/sgo-framework",
            "/geo/medalist-origins", "/predict/controversy-category",
        ],
    }


@app.get("/medals/by-games")
def medals_by_games():
    with get_db() as conn:
        cur = conn.execute("SELECT * FROM medals_by_games")
        return rows_to_dicts(cur)


@app.get("/medals/golds")
def golds(year: int | None = Query(default=None, description="Filter by Games year")):
    with get_db() as conn:
        if year:
            cur = conn.execute("SELECT * FROM golds WHERE Year = ?", (str(year),))
        else:
            cur = conn.execute("SELECT * FROM golds")
        return rows_to_dicts(cur)


@app.get("/medals/all")
def all_medals(medal: str | None = Query(default=None, description="Gold, Silver, or Bronze")):
    with get_db() as conn:
        if medal:
            cur = conn.execute("SELECT * FROM all_medals WHERE Medal = ?", (medal,))
        else:
            cur = conn.execute("SELECT * FROM all_medals")
        return rows_to_dicts(cur)


@app.get("/governance/controversies")
def controversies(
    category: str | None = None,
    year_range_contains: str | None = Query(
        default=None, description="e.g. '2025' matches records whose year_range includes 2025"
    ),
):
    with get_db() as conn:
        query = "SELECT * FROM controversies WHERE 1=1"
        params = []
        if category:
            query += " AND category = ?"
            params.append(category)
        if year_range_contains:
            query += " AND year_range LIKE ?"
            params.append(f"%{year_range_contains}%")
        cur = conn.execute(query, params)
        return rows_to_dicts(cur)


@app.get("/governance/policy-timeline")
def policy_timeline():
    with get_db() as conn:
        cur = conn.execute("SELECT * FROM policy_timeline")
        return rows_to_dicts(cur)


@app.get("/governance/scorecard")
def scorecard():
    with get_db() as conn:
        cur = conn.execute("SELECT * FROM governance_scorecard")
        return rows_to_dicts(cur)


@app.get("/governance/sgo-framework")
def sgo_framework():
    """The 4-dimension SGO/NSGO governance framework this project's scorecard is aligned to."""
    with get_db() as conn:
        cur = conn.execute("SELECT * FROM sgo_framework_dimensions")
        return rows_to_dicts(cur)


@app.get("/geo/medalist-origins")
def medalist_origins(county: str | None = None):
    with get_db() as conn:
        if county:
            cur = conn.execute(
                "SELECT * FROM medalist_origins WHERE county = ?", (county,)
            )
        else:
            cur = conn.execute("SELECT * FROM medalist_origins")
        return rows_to_dicts(cur)


class PredictRequest(BaseModel):
    text: str


@app.post("/predict/controversy-category")
def predict_controversy_category(payload: PredictRequest):
    """
    Runs the trained TF-IDF + ComplementNB classifier from nlp/controversy_classifier.py
    on a piece of news text and returns the predicted controversy category.
    """
    try:
        from nlp.controversy_classifier import load_trained
    except ImportError:
        raise HTTPException(
            status_code=503,
            detail="Classifier module not found -- ensure nlp/ is on the Python path.",
        )
    model = load_trained()
    prediction = model.predict([payload.text])[0]
    return {"text": payload.text, "predicted_category": prediction}
