# Deploying Kenya at Gold: The Governance Ledger

Repo: https://github.com/jameskoero/kenya-gold-ledger
Backend: Render (FastAPI + SQLite)
Frontend: Vercel (static, API-driven)

I can't push to GitHub or connect Render/Vercel from this sandbox (no network access here) —
these steps run in your usual Termux or Colab environment.

## 1. Add the new files to your repo
- `data/sgo_framework.json` -- SGO/NSGO governance framework (new)
- `data/controversies.json` -- replaces the old file; already merged old+new, v0.2
- `data/talent_geography_study.json` -- new, validates medalist_origins.csv
- `backend/app.py`, `backend/migrate_to_sqlite.py`, `backend/requirements.txt`, `backend/render.yaml`
- `frontend/index.html`, `frontend/vercel.json`

## 2. Build and sanity-check the database locally
```
pip install -r backend/requirements.txt --break-system-packages
python backend/migrate_to_sqlite.py
uvicorn backend.app:app --reload
```
Visit http://localhost:8000/docs -- confirm `/governance/controversies` and
`/governance/sgo-framework` return real rows before pushing anything.

## 3. Commit and push
```
git config user.email "jameskoero@users.noreply.github.com"
git add data/ backend/ frontend/ DEPLOYMENT.md
git commit -m "Add SGO framework, merged 2022-2026 controversies, FastAPI backend, Vercel-ready frontend"
git push origin main
```

## 4. Deploy the backend on Render
1. Render dashboard -> New -> Blueprint
2. Connect the `kenya-gold-ledger` repo -- it reads `backend/render.yaml` automatically
3. Deploy; note the resulting URL, e.g. `https://kenya-gold-ledger-api.onrender.com`

## 5. Deploy the frontend on Vercel
1. Vercel dashboard -> Add New -> Project -> import `kenya-gold-ledger`
2. Set **Root Directory** to `frontend/` (Vercel picks up `vercel.json` automatically --
   no build step needed, it's a static HTML file)
3. Deploy; Vercel gives you a URL like `https://kenya-gold-ledger.vercel.app`
4. Before or right after deploying, edit `frontend/index.html`'s `#api-base` input
   default value to your actual Render URL from step 4, so visitors don't have to
   type it in manually -- commit and push (Vercel auto-redeploys)

## 6. Lock down CORS
In `backend/app.py`, change `allow_origins=["*"]` to your real Vercel domain, e.g.
```python
allow_origins=["https://kenya-gold-ledger.vercel.app"],
```
once the frontend is live, so the API only serves your dashboard. Push again to
trigger Render's auto-redeploy.

## 7. Optional: custom domain
If you want a custom domain later, Vercel's Project -> Settings -> Domains
handles that directly -- no extra config needed beyond DNS.
