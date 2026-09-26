"""Small regression suite comparing both implementations across varied inputs."""

from __future__ import annotations

import numpy as np
import pandas as pd

from algorithm1 import enumerate_combinations
from algorithm2 import stepwise_filter


def main() -> None:
    for seed in range(5):
        rng = np.random.default_rng(seed)
        scores = pd.DataFrame(
            rng.integers(0, 11, size=(12, 8)),
            index=[f"S{i}" for i in range(12)],
            columns=[f"Q{i}" for i in range(8)],
        )
        for k in (1, 2, 3, 4):
            for p, r in ((1, 10), (3, 7), (5, 5), (12, 0), (13, 5)):
                result1, _ = enumerate_combinations(scores, p, r, k)
                result2, _, _ = stepwise_filter(scores, p, r, k)
                assert result1 == result2, (seed, k, p, r)
    print("PASS: both algorithms agreed on 100 varied parameter cases.")


if __name__ == "__main__":
    main()
