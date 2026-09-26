# CSCE 811 Homework 2 - Quiz Combination Query

## Setup

```bash
python -m pip install -r requirements.txt
```

## Generate a dataset

```bash
python data_generate.py --rows 30 --columns 30 --seed 811 --output raw_score_dataframe.csv
```

## Run the algorithms

Here, `P` is the minimum qualifying-student count, `R` is the minimum score on every selected quiz, and `--k` is the number of quizzes.

```bash
python algorithm1.py raw_score_dataframe.csv 5 5 --k 4 --output algorithm1_results.csv
python algorithm2.py raw_score_dataframe.csv 5 5 --k 4 --output algorithm2_results.csv
```

## Reproduce the report experiments

```bash
python run_experiments.py
```

The experiment script uses two cases, repeats each timing seven times, checks that both algorithms return identical ordered results, and writes the median runtimes to `results/runtime_summary.csv`.

The programs infer `M` and `N` from any compatible CSV. The first CSV column must contain student IDs; all remaining columns are quiz IDs containing numeric scores.
