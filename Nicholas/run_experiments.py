"""Generate data, run both algorithms on two cases, and verify identical outputs."""

from __future__ import annotations

import csv
import statistics
from pathlib import Path

from algorithm1 import enumerate_combinations
from algorithm2 import stepwise_filter
from data_generate import generate_dataset
from quiz_query_common import write_results


DATA_FILE = Path("raw_score_dataframe.csv")
RESULTS_DIR = Path("results")
TEST_CASES = [(5, 5), (3, 7)]
REPEATS = 7
K = 4


def main() -> None:
    scores = generate_dataset(30, 30, 811, DATA_FILE)
    RESULTS_DIR.mkdir(exist_ok=True)
    summaries = []

    for case_number, (p, r) in enumerate(TEST_CASES, start=1):
        times1, times2 = [], []
        final1 = final2 = None
        retained = None
        for _ in range(REPEATS):
            result1, elapsed1 = enumerate_combinations(scores, p, r, K)
            result2, elapsed2, retained = stepwise_filter(scores, p, r, K)
            if result1 != result2:
                raise AssertionError(f"Algorithms disagree for P={p}, R={r}")
            final1, final2 = result1, result2
            times1.append(elapsed1)
            times2.append(elapsed2)

        out1 = RESULTS_DIR / f"case{case_number}_algorithm1.csv"
        out2 = RESULTS_DIR / f"case{case_number}_algorithm2.csv"
        write_results(out1, final1, K)
        write_results(out2, final2, K)
        summaries.append(
            {
                "case": case_number,
                "M": scores.shape[0],
                "N": scores.shape[1],
                "P": p,
                "R": r,
                "K": K,
                "qualifying_combinations": len(final1),
                "algorithm1_median_seconds": statistics.median(times1),
                "algorithm2_median_seconds": statistics.median(times2),
                "speedup_algorithm1_over_algorithm2": (
                    statistics.median(times1) / statistics.median(times2)
                    if statistics.median(times2) else float("inf")
                ),
                "retained_K1": retained[0],
                "retained_K2": retained[1],
                "retained_K3": retained[2],
                "retained_K4": retained[3],
            }
        )

    summary_path = RESULTS_DIR / "runtime_summary.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summaries[0].keys())
        writer.writeheader()
        writer.writerows(summaries)

    print("Both algorithms produced identical results for every test case.")
    for row in summaries:
        print(
            f"Case {row['case']}: P={row['P']}, R={row['R']}, "
            f"matches={row['qualifying_combinations']}, "
            f"A1 median={row['algorithm1_median_seconds']:.9f}s, "
            f"A2 median={row['algorithm2_median_seconds']:.9f}s, "
            f"speedup={row['speedup_algorithm1_over_algorithm2']:.2f}x"
        )


if __name__ == "__main__":
    main()
