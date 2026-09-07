# 🚀 Falcon 9 Launch & Landing Analytics

> **End-to-end data analytics portfolio project** covering data collection, web scraping, data wrangling, SQL analysis, exploratory analysis, interactive visualization, geospatial analysis and predictive modeling.

## Project objective

The project investigates **Falcon 9 first-stage landing success** and the factors associated with launch outcomes. The original work combines:

- SpaceX API data collection
- Wikipedia web scraping
- Pandas-based data wrangling
- SQLite + SQL exploratory analysis
- Statistical / visual EDA
- Feature engineering and one-hot encoding
- Classification models
- Interactive Plotly/Dash visualization
- Folium-based geospatial exploration

The supplied notebooks are preserved in `notebooks/` for traceability. A separate, polished dashboard is provided in `app.py`.

## 📊 Executive snapshot

The dashboard dataset contains **56 launch observations** with a binary landing-success label. In this curated dashboard dataset:

| KPI | Value |
|---|---:|
| Launches | 56 |
| Successful landings | 24 |
| Landing success rate | 42.9% |
| Mean payload | 3,697 kg |
| Median payload | 3,412 kg |

### Key analytical findings

1. **Landing performance improves strongly across the later years represented in the dataset.** The annual success rate rises from 0% in the early years to **77.8% in 2017** in this curated subset, before varying in 2018.
2. **KSC LC-39A has the highest observed landing success rate** among the launch sites represented here: **76.9% (10/13)**.
3. **Payload mass is not a simple linear separator of success.** Successful launches have a higher mean payload in this subset, but the scatter distribution shows substantial overlap between successful and failed outcomes.
4. **Booster generation matters.** The observed success rate increases substantially from the older `v1.0` / `v1.1` generations toward later generations in this dashboard dataset.
5. **Orbit type is associated with different observed success rates**, but some orbit categories have very small sample sizes. These should not be interpreted as causal effects.
6. The original predictive-model notebook reports **83.33% test accuracy for all four models**, so the recorded test results are a tie. Its highest reported cross-validation score is **87.50% for Decision Tree**. See `docs/model_notes.md`.

> **Important:** These findings describe the supplied project datasets, not all SpaceX launches worldwide or the current state of SpaceX operations.

## 🧭 Dashboard

The professional dashboard includes:

- KPI cards for launches, successful landings, success rate and payload
- Interactive filters for launch site, orbit, booster generation and payload range
- Yearly landing-success trend
- Launch-site performance comparison
- Orbit-level success analysis
- Payload-vs-outcome scatter plot
- Launch-site geographic visualization
- Booster-generation performance comparison

Run it locally:

```bash
pip install -r requirements.txt
python app.py
```

Then open the local Dash URL shown in your terminal.

## 🗂️ Repository structure

```text
spacex-falcon9-analytics/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── data/
│   ├── launches_dashboard.csv
│   ├── spacex_launch_dash.csv
│   ├── spacex_web_scraped.csv
│   ├── dataset_part_3.csv
│   └── my_data1.db
├── notebooks/
│   ├── Data Collection With API.ipynb
│   ├── Data Collection with Web Scraping.ipynb
│   ├── Data Wrangling.ipynb
│   ├── Exploratory Data Analysis.ipynb
│   ├── Data Visualization.ipynb
│   ├── Predictive Model.ipynb
│   └── SpaceX_Dashboard_original.py
├── src/
│   └── analysis_queries.sql
├── docs/
│   └── model_notes.md
└── assets/
    ├── success_rate_by_year.png
    ├── success_rate_by_site.png
    └── success_rate_by_orbit.png
```

## 🔬 Analytical workflow

```text
API / Web Scraping
       ↓
Raw launch records
       ↓
Data cleaning + missing-value treatment
       ↓
Landing-success target engineering
       ↓
SQL exploration + statistical EDA
       ↓
Feature engineering / one-hot encoding
       ↓
Classification models
       ↓
Interactive dashboard + business insights
```

## 🤖 Predictive modeling

The supplied predictive notebook evaluates:

- Logistic Regression
- Support Vector Machine
- Decision Tree
- K-Nearest Neighbors

The original notebook uses standardized features and an **80/20 train-test split with `random_state=2`**.

For transparency, the historical notebook results are not silently rewritten. The model-specific notes and reproducibility caveats are documented in [`docs/model_notes.md`](docs/model_notes.md).

## 🧪 SQL analysis

The SQLite database contains the launch records used by the original SQL notebook. Reusable analytical queries are collected in:

`src/analysis_queries.sql`

The original SQL analysis covers launch sites, payload totals, booster versions, first successful ground-pad landing, drone-ship outcomes, outcome frequencies and maximum payload analysis.

## 📓 Notebook walkthrough

| Stage | Notebook | Main output |
|---|---|---|
| 1 | Data Collection With API | API-derived launch and booster attributes |
| 2 | Data Collection with Web Scraping | Wikipedia launch-history dataset |
| 3 | Data Wrangling | Cleaned data + binary landing class |
| 4 | Exploratory Data Analysis | SQL findings + EDA plots |
| 5 | Data Visualization | Interactive launch-site map |
| 6 | Predictive Model | Four classification models |
| 7 | Dashboard | Interactive analytical application |

## ⚠️ Data and reproducibility notes

- The supplied project contains multiple dataset versions with different row counts because they are produced at different stages of the workflow.
- `dataset_part_3.csv` is a feature matrix and does not contain the target label; the original predictive notebook reads its target from a separate `dataset_part_2.csv`.
- The repository therefore keeps the original notebooks intact rather than pretending that every intermediate artifact was generated by one single pipeline.
- The dashboard uses `data/launches_dashboard.csv`, a curated 56-row analytical view derived from the supplied dashboard dataset and matched launch-history fields.

