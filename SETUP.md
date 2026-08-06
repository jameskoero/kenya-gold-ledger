# Setup

Two ways I run this: on my phone via Termux, or on Google Colab when I want
to run the network builders or don't want to burn mobile data on installs.
Colab is also the easiest way for anyone else to reproduce the analysis
without touching their own machine.

## Google Colab

Paste each block into its own cell, in order.

**1. Get the code onto Colab**

The repo isn't pushed to GitHub yet, so `git clone` against
`jameskoero/kenya-olympic-gold` won't work until that exists. Two ways to
get the code onto Colab in the meantime:

*Option A — upload the zip directly (works right now):*

```python
from google.colab import files
uploaded = files.upload()   # choose kenya-olympic-gold.zip from the file picker
!unzip -q kenya-olympic-gold.zip
%cd kenya-olympic-gold
!pip install -q -r requirements.txt
!pip install -q beautifulsoup4 rapidfuzz networkx
```

*Option B — once I've created the GitHub repo and pushed to it:*

```python
!git clone https://github.com/jameskoero/kenya-olympic-gold.git
%cd kenya-olympic-gold
!pip install -q -r requirements.txt
!pip install -q beautifulsoup4 rapidfuzz networkx
```

To get to Option B: create an empty repo named `kenya-olympic-gold` at
github.com/new under my account, then from a terminal with the unzipped
folder:

```bash
cd kenya-olympic-gold
git init
git add -A
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/jameskoero/kenya-olympic-gold.git
git push -u origin main
```

Pushing needs a GitHub personal access token as the password when prompted
(GitHub retired plain password auth) — Settings → Developer settings →
Personal access tokens → generate one with `repo` scope, and paste it in
place of a password when `git push` asks.

**2. Regenerate the core medal analysis and figures**

```python
!python notebooks/01_medal_analysis.py
```

**3. Run the governance network analysis**

```python
!python notebooks/02_network_analysis.py
```

**4. Run the medals-vs-governance overlay**

```python
!python notebooks/03_governance_density.py
```

**5. Build the transparent Governance Response Scorecard**

```python
!python notebooks/04_governance_scorecard.py
```

**6. View any figure inline**

```python
from IPython.display import Image
Image("viz/fig6_governance_vs_medals.png")
```

**7. Open the interactive dashboard directly in Colab**

```python
from IPython.display import IFrame
IFrame("viz/dashboard.html", width=900, height=700)
```

**8. Run the two data builders (need network access, which Colab has)**

```python
!python data/build_all_medals.py --check
!python data/build_all_medals.py
```

```python
!python data/build_medalist_origins.py --dry-run
!python data/build_medalist_origins.py
```

**9. Train the controversy classifier on the real corpus**

```python
!python nlp/collect_corpus.py --status
!python nlp/collect_corpus.py
!python nlp/train.py
```

**10. Run a prediction against the trained model**

```python
import sys
sys.path.append('.')
from nlp.controversy_classifier import ControversyClassifier

clf = ControversyClassifier.load_trained()
pred = clf.predict("A federation official was accused of diverting sponsorship funds")
print(pred.label, pred.probability)
```

**11. Save any output back to my own machine**

```python
from google.colab import files
files.download("data/all_medals.csv")
```

**12. Push updates back to GitHub**

Only works once the repo exists on GitHub and has a `origin` remote set (see
Option B above, or the one-time `git init` / `git remote add origin` steps
in it). If I uploaded via Option A and never ran those, `git push` here will
fail the same way the original clone did — there's no remote to push to yet.

```python
!git config user.email "jmskoero@gmail.com"
!git config user.name "James Koero"
!git add -A
!git commit -m "Update: run builders, regenerate figures, retrain classifier"
!git push
```

## Termux (phone)

```bash
pkg install python git
git clone https://github.com/jameskoero/kenya-olympic-gold.git
cd kenya-olympic-gold
pip install -r requirements.txt
pip install beautifulsoup4 rapidfuzz networkx
python notebooks/01_medal_analysis.py
python notebooks/02_network_analysis.py
python notebooks/03_governance_density.py
python notebooks/04_governance_scorecard.py
python nlp/train.py
```

The two data builders (`build_all_medals.py`, `build_medalist_origins.py`)
and the corpus collector (`collect_corpus.py`) work the same way in Termux,
but they're slow over mobile data since each fetches one page per item with
a rate limit between requests. Better to run those from Colab when I can,
and pull the results back down to my phone after.

## What each script actually needs

| Script | Needs network | Runtime (rough) |
|---|---|---|
| `notebooks/01_medal_analysis.py` | No | Seconds |
| `notebooks/02_network_analysis.py` | No | Seconds |
| `notebooks/03_governance_density.py` | No | Seconds |
| `notebooks/04_governance_scorecard.py` | No | Seconds |
| `data/build_all_medals.py` | Yes | ~1 min (14 Games pages) |
| `data/build_medalist_origins.py` | Yes | Several minutes (one page per athlete, rate-limited) |
| `nlp/collect_corpus.py` | Yes | ~1-2 min (22 articles, rate-limited) |
| `nlp/train.py` | No (uses whatever's cached) | Seconds |

`viz/dashboard.html` needs nothing at all — it's a single file with the data
embedded directly in it. I can open it straight from my phone's file manager
or a browser, no server, no network, no Colab.
