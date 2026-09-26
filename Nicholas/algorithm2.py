"""Algorithm 2: build and prune stepwise quiz combinations using student sets."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from quiz_query_common import load_scores, validate_parameters, write_results


def stepwise_filter(scores, p: int, r: float, k: int = 4):
    """Return qualifying K-tuples, runtime, and retained counts at each level."""
    validate_parameters(scores, p, k)
    quiz_ids = list(scores.columns)
    order = {quiz: position for position, quiz in enumerate(quiz_ids)}

    started = time.perf_counter()
    eligible = {
        quiz: frozenset(i for i, value in enumerate(scores[quiz].to_numpy()) if value >= r)
        for quiz in quiz_ids
    }

    level = [((quiz,), students) for quiz, students in eligible.items() if len(students) >= p]
    retained_by_level = [len(level)]

    for size in range(2, k + 1):
        next_level = []
        for combination, students in level:
            last_position = order[combination[-1]]
            for next_position in range(last_position + 1, len(quiz_ids)):
                next_quiz = quiz_ids[next_position]
                common_students = students.intersection(eligible[next_quiz])
                if len(common_students) >= p:
                    next_level.append((combination + (next_quiz,), common_students))
        level = next_level
        retained_by_level.append(len(level))
        if not level:
            retained_by_level.extend([0] * (k - size))
            break

    results = [(combination, len(students)) for combination, students in level]
    elapsed = time.perf_counter() - started
    return results, elapsed, retained_by_level


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("P", type=int, help="minimum number of qualifying students")
    parser.add_argument("R", type=float, help="minimum score on every selected quiz")
    parser.add_argument("--k", type=int, default=4, help="number of quizzes to choose")
    parser.add_argument("--output", type=Path, default=Path("algorithm2_results.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scores = load_scores(args.input_csv)
    results, elapsed, retained = stepwise_filter(scores, args.P, args.R, args.k)
    write_results(args.output, results, args.k)
    print(
        f"Algorithm 2: M={scores.shape[0]}, N={scores.shape[1]}, "
        f"P={args.P}, R={args.R:g}, K={args.k}"
    )
    print("Retained combinations by level: " + ", ".join(
        f"K={level}: {count}" for level, count in enumerate(retained, start=1)
    ))
    print(f"Qualifying combinations: {len(results)}")
    print(f"Core running time: {elapsed:.9f} seconds")
    print(f"Results written to: {args.output}")


if __name__ == "__main__":
    main()
