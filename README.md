Data Mining Project - Group 19
==============================

_This documentation is aimed to help provide information that explains what the project is about._

Last updated: November 2025

## Table of contents 

1. [Project Description](#project-description) 
2. [Project Organization](#project-organization) 
3. [Getting Started](#getting-started)
4. [Authors](#authors)
5. [More Information](#more-information)

## Project Description 
-----------

This project explores association rule mining using Apriori and FP-Growth algorithms. It introduces an optimized Weighted Apriori method for weighted multidimensional data, improving efficiency by reducing repeated database scans. The algorithm is evaluated through rule analysis on the business categories found on Yelp dataset.

## Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, processed data sets of Yelp data.
    │   └── raw            <- The original, Yelp dataset as obtained from source.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained models and algorithm outputs
    │   ├── mining_strategies.py      <- Strategy pattern for mining algorithms
    │   ├── compare_algorithms.py     <- Main comparison script
    │   ├── algorithm_comparison.csv  <- Generated comparison results
    │   └── mining_results.json       <- Generated raw results
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to process raw data
    │   │   ├── make_dataset.py          <- Main data processing pipeline
    │   │   └── prepare_review_data.py   <- Review-business merging logic
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py        <- Transaction feature engineering
    │   │
    │   ├── models         <- Scripts to train models and compare algorithms
    │   │   ├── mining_strategies.py     <- Strategy pattern implementation
    │   │   └── compare_algorithms.py    <- Algorithm comparison runner
    │   │
    │   └── visualization  <- Scripts to create exploratory and results visualizations
    │       └── plot_comparison.py       <- Generate comparison charts
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://ieeexplore.ieee.org/document/7009124/">An improved algorithm for Mining Association Rule in relational database</a> research paper.</small></p>

## Getting Started
-----------
_This section provides the necessary information for a user to be able to run the code locally._

### Prerequisites 

1. Python 3.8 or higher
2. Git (for cloning the repository)
3. Required Python packages (see `requirements.txt`)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/UnarineLeo/data-mining-project.git
   cd data-mining-project
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .
   ```

### Data Setup

Download the Yelp dataset and place these files in `data/raw/`:
- `yelp_academic_dataset_review.json`
- `yelp_academic_dataset_business.json`

Dataset sources:
- <a target="_blank" href="https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset">Kaggle Dataset</a>
- <a target="_blank" href="https://drive.google.com/drive/folders/12MHKndM9nL8XaauUWqcrkUIpdfV4GBS7?usp=sharing">Google Drive</a>
   ```bash
   python -m src.data.make_dataset
   ```
   
   Or with custom parameters:
   ```bash
   python -m src.data.make_dataset --num-samples 50000 --min-stars 4
   ```

**Output:** `data/processed/review_business_data.jsonl`

#### 2. Build Transaction Features
```bash
python -m src.features.build_features
```

**Output:** 
- `data/processed/transactions_encoded.csv` - One-hot encoded transactions
- `data/processed/user_transactions.pkl` - Raw transaction sets

#### 3. Compare Mining Algorithms
```bash
python -m src.models.compare_algorithms
```

**Output:**
- `models/algorithm_comparison.csv` - Performance comparison table
- `models/mining_results.json` - Detailed results

#### 4. Generate Visualizations
```bash
python -m src.visualization.plot_comparison
```

**Output:** Charts in `reports/figures/`
- Execution time comparison
- Speedup ratios
- Itemsets comparison
- Performance heatmap

### Quick Start (All Steps)

```bash
python -m src.data.make_dataset && \
python -m src.features.build_features && \
python -m src.models.compare_algorithms && \
python -m src.visualization.plot_comparison
```

### Configuration

Adjust parameters in the scripts:

**Data Processing** (`make_dataset.py`):
- `--num-samples`: Number of reviews to process (default: 100,000)
- `--min-stars`: Minimum star rating filter (default: 3)

**Algorithm Comparison** (`compare_algorithms.py` line 167):
- Modify `min_support_values` list to test different thresholds

**Feature Building** (`build_features.py` line 141):
- Set `filter_restaurant=False` to include all business categories


## Authors 
-----------

* Written by : Maishah Dlamini, Khwezi Ntsaluba, Yashvitha Kanaparthy, Unarine Netshifhefhe

## Links 
-----------
* Dataset: <a target="_blank" href="https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset">Kaggle Dataset</a>
* Presentation Link: <a target="_blank" href="https://www.canva.com/design/DAG4OtN1I5I/iURjteA3UJ9OtngxnE5u5w/edit?utm_content=DAG4OtN1I5I&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton">Canva</a>

## More Information 
---------

This project is part of the Data Mining course (COS781) at the University of Pretoria. The project is supervised by Prof. Vukosi Marivate, Dr. Abiodun Modupe and Mr. Willem van Heerden.
