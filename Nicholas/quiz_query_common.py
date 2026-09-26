"""Shared input validation and result-writing helpers."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


def load_scores(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, index_col=0)
    if frame.empty or frame.shape[1] == 0:
        raise ValueError("the input CSV must contain at least one student and one quiz")
    if not frame.index.is_unique or not frame.columns.is_unique:
        raise ValueError("student IDs and quiz IDs must be unique")
    numeric = frame.apply(pd.to_numeric, errors="raise")
    if numeric.isna().any().any():
        raise ValueError("scores cannot contain missing values")
    return numeric


def validate_parameters(frame: pd.DataFrame, p: int, k: int) -> None:
    if p < 1:
        raise ValueError("P must be at least 1")
    if k < 1:
        raise ValueError("K must be at least 1")
    if k > frame.shape[1]:
        raise ValueError(f"K={k} exceeds the number of quizzes N={frame.shape[1]}")


def write_results(path: Path, results: list[tuple[tuple[str, ...], int]], k: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = [f"quiz_{i}" for i in range(1, k + 1)] + ["count"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for combination, count in results:
            writer.writerow([*combination, count])
