"""Generate a reproducible student-by-quiz score table."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def generate_dataset(rows: int, columns: int, seed: int, output: Path) -> pd.DataFrame:
    if rows < 1 or columns < 1:
        raise ValueError("rows and columns must both be positive")
    rng = np.random.default_rng(seed)
    scores = rng.integers(0, 11, size=(rows, columns))
    frame = pd.DataFrame(
        scores,
        index=[f"S{i}" for i in range(1, rows + 1)],
        columns=[f"Q{i}" for i in range(1, columns + 1)],
    )
    frame.index.name = "student_id"
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output)
    return frame


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=30)
    parser.add_argument("--columns", type=int, default=30)
    parser.add_argument("--seed", type=int, default=811)
    parser.add_argument("--output", type=Path, default=Path("raw_score_dataframe.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frame = generate_dataset(args.rows, args.columns, args.seed, args.output)
    print(f"Created {args.output} with shape {frame.shape} using seed {args.seed}.")
    print(frame.to_string())


if __name__ == "__main__":
    main()
