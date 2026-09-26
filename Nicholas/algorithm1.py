"""Algorithm 1: enumerate every K-quiz combination and test all students."""

from __future__ import annotations

import argparse
import itertools
import time
from pathlib import Path

import numpy as np

from quiz_query_common import load_scores, validate_parameters, write_results


def enumerate_combinations(scores, p: int, r: float, k: int = 4):
    """Return qualifying quiz combinations, their counts, and core runtime."""
    validate_parameters(scores, p, k)
    quiz_ids = list(scores.columns)
    passing = scores.to_numpy() >= r
    results: list[tuple[tuple[str, ...], int]] = []

    started = time.perf_counter()
    for indices in itertools.combinations(range(len(quiz_ids)), k):
        count = int(np.all(passing[:, indices], axis=1).sum())
        if count >= p:
            results.append((tuple(quiz_ids[i] for i in indices), count))
    elapsed = time.perf_counter() - started
    return results, elapsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("P", type=int, help="minimum number of qualifying students")
    parser.add_argument("R", type=float, help="minimum score on every selected quiz")
    parser.add_argument("--k", type=int, default=4, help="number of quizzes to choose")
    parser.add_argument("--output", type=Path, default=Path("algorithm1_results.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scores = load_scores(args.input_csv)
    results, elapsed = enumerate_combinations(scores, args.P, args.R, args.k)
    write_results(args.output, results, args.k)
    print(
        f"Algorithm 1: M={scores.shape[0]}, N={scores.shape[1]}, "
        f"P={args.P}, R={args.R:g}, K={args.k}"
    )
    print(f"Qualifying combinations: {len(results)}")
    print(f"Core running time: {elapsed:.9f} seconds")
    print(f"Results written to: {args.output}")


if __name__ == "__main__":
    main()
