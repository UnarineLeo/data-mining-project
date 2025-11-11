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
    ├── models             <- Apriori, FP-Growth, and Weighted Algorithms.
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
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://ieeexplore.ieee.org/document/7009124/">An improved algorithm for Mining Association Rule in relational database</a> research paper.</small></p>

## Getting Started
-----------
_This section provides the necessary information for a user to be able to run the code locally._

### Prerequisites 

1. Have a Google Account, to access Google Drive and Google Colabs

### Usage 

To test the code, follow these steps:

1. Create a Google Drive shortcut for the yelp dataset <a target="_blank" href="https://drive.google.com/drive/folders/12MHKndM9nL8XaauUWqcrkUIpdfV4GBS7?usp=sharing">here</a>.

2. Download the following python notebook to generate the frequent itemsets and association rules using the Apriori, FP-Growth and Weighted Apriori algorithms. The notebook is located at: ``src/models/association_rules_efficiency.ipynb``

3. Run the notebook on Google Colab or Jupyter Notebook.


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
