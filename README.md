## Predicting Price Moves with News Sentiment

This repository contains your solution for the **Nova Financial Solutions – Predicting Price Moves with News Sentiment** challenge.

The goal is to:
- **Run EDA** on financial news (headlines, publishers, dates).
- **Compute technical indicators** (MA, RSI, MACD, etc.) on stock prices.
- **Perform sentiment analysis** on headlines and **measure correlation** between sentiment and stock returns.

The work is organized in three tasks (Task 1–3) matching the challenge description.

---

### 1. Project structure

Recommended structure (implemented here):

```text
.vscode/
  settings.json

.github/
  workflows/
    unittests.yml

data/
  README.md

notebooks/
  __init__.py
  README.md
  task1_eda_news.ipynb
  task2_tech_indicators.ipynb
  task3_sentiment_correlation.ipynb

scripts/
  __init__.py
  README.md

src/
  __init__.py
  config.py
  data_loading.py
  text_eda.py
  sentiment.py
  technical_indicators.py
  correlation.py

tests/
  __init__.py
  test_smoke.py
```

---

### 2. Environment setup

#### 2.1. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate   # Windows (PowerShell)
```

#### 2.2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note on TA-Lib / PyNance**  
> TA-Lib may require system libraries to be installed first on macOS (e.g. via `brew install ta-lib`).  
> If installation fails, resolve the system dependency and then re-run `pip install -r requirements.txt`.

#### 2.3. Jupyter kernel

```bash
python -m ipykernel install --user --name news-sentiment-env
```

Select this kernel in VS Code / Jupyter when running notebooks.

---

### 3. Data locations

- **News dataset (FNSPID)**: place the CSV in `data/raw/` (or update the notebook paths).
  - Expected minimal columns: `headline`, `url`, `publisher`, `date`, `stock`.
- **Stock price data**:
  - Either download CSVs to `data/raw/` (with OHLCV columns), **or**
  - Let the notebooks use `yfinance` to download prices on the fly.

See `data/README.md` for details and naming conventions.

---

### 4. Git & GitHub workflow (per challenge)

#### 4.1. Initial setup

1. **Create a GitHub repository** (e.g. `nova-news-sentiment`).
2. In this folder:
   ```bash
   git init
   git remote add origin <your-github-repo-url>
   git add .
   git commit -m "Initial scaffold for Nova news sentiment project"
   git push -u origin main
   ```

#### 4.2. Branching model

- **Task 1** (EDA):
  - Create branch: `task-1`
  - Work on EDA in `notebooks/task1_eda_news.ipynb` and helper modules in `src/`.
  - Commit frequently (at least ~3 times per day) with descriptive messages.
  - Open a Pull Request (PR) from `task-1` → `main` and merge after review.

- **Task 2** (Technical indicators):
  - Create branch: `task-2` from updated `main`.
  - Implement indicators in `notebooks/task2_tech_indicators.ipynb` and `src/technical_indicators.py`.
  - PR `task-2` → `main` and merge.

- **Task 3** (Sentiment & correlation):
  - Create branch: `task-3` from updated `main`.
  - Implement sentiment scoring and correlation analysis in `notebooks/task3_sentiment_correlation.ipynb`, plus `src/sentiment.py` and `src/correlation.py`.
  - PR `task-3` → `main` and merge.

This structure demonstrates **branching, PRs, and CI** as requested.

---

### 5. Continuous Integration (CI)

GitHub Actions is configured via `.github/workflows/unittests.yml` to:
- Install dependencies.
- Run a small smoke test (`tests/test_smoke.py`).

Extend `tests/` with:
- Unit tests for data-prep functions.
- Tests validating indicators and sentiment scoring.

---

### 6. Notebook overview (how to use)

- **Task 1 – EDA (`task1_eda_news.ipynb`)**
  - Load FNSPID news data.
  - Compute **headline length statistics**.
  - Count **articles per publisher** and per **stock**.
  - Analyze **publication dates / times**: daily / weekly trends, spikes, and distributions.
  - Basic **keyword / topic exploration** using NLP (n-grams, word clouds, simple topic hints).

- **Task 2 – Technical indicators (`task2_tech_indicators.ipynb`)**
  - Load OHLCV data (from CSV or `yfinance`).
  - Compute **MA, RSI, MACD** with TA-Lib / PyNance.
  - Visualize prices with overlays and indicator subplots.
  - Discuss patterns and potential trading signals.

- **Task 3 – Sentiment & correlation (`task3_sentiment_correlation.ipynb`)**
  - Clean and align **news** and **price** data by date (and optionally time).
  - Compute **headline sentiment scores** (TextBlob / NLTK).
  - Aggregate to **daily sentiment per stock**.
  - Compute **daily returns** and test **Pearson correlation** between sentiment and returns.
  - Summarize findings and propose **investment strategies** using sentiment as a signal.

---

### 7. Suggested next steps for you

1. Place the **FNSPID news CSV** into `data/raw/` and update the path in `task1_eda_news.ipynb`.
2. Run through **Task 1 notebook** top-to-bottom to generate EDA plots and tables.
3. Share key plots / findings in your interim report (publisher activity, sentiment distributions, time-of-day patterns).
4. Then continue with **Task 2** and **Task 3** notebooks following the structure already scaffolded here.


