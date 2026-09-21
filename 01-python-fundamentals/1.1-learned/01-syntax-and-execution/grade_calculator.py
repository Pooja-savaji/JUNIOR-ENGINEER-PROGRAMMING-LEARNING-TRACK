"""Student Grade and GPA Calculator in Pure Python.

Covers: data collections (lists, dictionaries), statistical aggregates (mean, median,
standard deviation, min/max), conditional grade scale mapping, and ASCII histograms.
"""

import math
from typing import Dict, List, Optional, Tuple


GRADE_SCALE: List[Tuple[float, str, float]] = [
    (93.0, "A", 4.0),
    (90.0, "A-", 3.7),
    (87.0, "B+", 3.3),
    (83.0, "B", 3.0),
    (80.0, "B-", 2.7),
    (77.0, "C+", 2.3),
    (73.0, "C", 2.0),
    (70.0, "C-", 1.7),
    (67.0, "D+", 1.3),
    (60.0, "D", 1.0),
    (0.0, "F", 0.0),
]


def score_to_letter_and_gpa(percentage: float) -> Tuple[str, float]:
    """Map a percentage score (0-100) to Letter Grade and 4.0 GPA."""
    for min_score, letter, gpa in GRADE_SCALE:
        if percentage >= min_score:
            return letter, gpa
    return "F", 0.0


def calculate_weighted_grade(components: List[Tuple[str, float, float]]) -> Tuple[float, str, float]:
    """Calculate weighted grade from list of (name, score_percent, weight_fraction).

    Args:
        components: List of tuples (component_name, score, weight).
                    Weights should sum to 1.0 (or 100).
    """
    if not components:
        return 0.0, "F", 0.0

    total_weight = sum(w for _, _, w in components)
    if total_weight <= 0:
        raise ValueError("Total weights must be greater than 0.")

    # Normalize weights if entered as percentages (e.g. 40 instead of 0.40)
    multiplier = 1.0 if total_weight <= 1.05 else (1.0 / total_weight)

    weighted_sum = sum(score * (w * multiplier) for _, score, w in components)
    final_percentage = round(weighted_sum, 2)
    letter, gpa = score_to_letter_and_gpa(final_percentage)
    return final_percentage, letter, gpa


def compute_statistics(scores: List[float]) -> Dict[str, float]:
    """Compute mean, median, standard deviation, min, and max for a list of scores."""
    if not scores:
        return {}

    n = len(scores)
    mean = sum(scores) / n
    sorted_scores = sorted(scores)

    # Median
    mid = n // 2
    if n % 2 == 0:
        median = (sorted_scores[mid - 1] + sorted_scores[mid]) / 2.0
    else:
        median = sorted_scores[mid]

    # Standard Deviation
    variance = sum((x - mean) ** 2 for x in scores) / n
    std_dev = math.sqrt(variance)

    return {
        "count": float(n),
        "mean": round(mean, 2),
        "median": round(median, 2),
        "std_dev": round(std_dev, 2),
        "min": round(sorted_scores[0], 2),
        "max": round(sorted_scores[-1], 2),
    }


def draw_histogram(scores: List[float]) -> None:
    """Print an ASCII distribution chart of letter grades."""
    counts: Dict[str, int] = {letter: 0 for _, letter, _ in GRADE_SCALE}
    for s in scores:
        let, _ = score_to_letter_and_gpa(s)
        counts[let] = counts.get(let, 0) + 1

    print("\n📊 Grade Distribution Histogram:")
    print("-" * 40)
    for _, letter, _ in GRADE_SCALE:
        bar = "█" * counts[letter]
        print(f"  {letter:<3} | {bar:<25} ({counts[letter]})")
    print("-" * 40)


def run_grade_calculator_cli():
    """Interactive CLI menu for grade calculations."""
    print("=" * 55)
    print("           🎓 PYTHON GRADE & GPA CALCULATOR        ")
    print("=" * 55)

    while True:
        print("\nOptions:")
        print("  1. 📝 Calculate Single Course Weighted Grade")
        print("  2. 👥 Analyze Batch of Class Scores")
        print("  3. 🔍 Score to Letter Grade Lookup")
        print("  0. 🚪 Exit")

        choice = input("\nEnter choice (0-3): ").strip()

        if choice == "0":
            print("\nThank you for using Grade Calculator! Goodbye! 👋\n")
            break

        if choice == "1":
            print("\n--- Weighted Course Grade Calculator ---")
            components = []
            print("Enter grade components (type 'done' when finished):")
            while True:
                name = input("  Component name (e.g., Midterm, HW) or 'done': ").strip()
                if name.lower() == "done":
                    break
                if not name:
                    continue
                try:
                    score = float(input(f"    Score for {name} (0-100): ").strip())
                    weight = float(input(f"    Weight for {name} (e.g. 0.25 or 25): ").strip())
                    components.append((name, score, weight))
                except ValueError:
                    print("    [Error] Invalid number. Skipping this item.")

            if components:
                final_pct, letter, gpa = calculate_weighted_grade(components)
                print("\n" + "=" * 45)
                print(f"Final Score : {final_pct:.2f}%")
                print(f"Letter Grade: {letter}")
                print(f"GPA Equivalent: {gpa:.1f} / 4.0")
                print("=" * 45)
            else:
                print("No components entered.")

        elif choice == "2":
            print("\n--- Batch Class Scores Analysis ---")
            print("Enter scores separated by spaces or commas (e.g. 85, 92, 78, 64, 99):")
            raw_input = input("Scores: ").strip()
            # Clean separators
            raw_items = raw_input.replace(",", " ").split()
            scores = []
            for item in raw_items:
                try:
                    s = float(item)
                    if 0 <= s <= 100:
                        scores.append(s)
                except ValueError:
                    pass

            if not scores:
                print("[Error] No valid scores entered.")
                continue

            stats = compute_statistics(scores)
            print("\n" + "=" * 45)
            print("             CLASS PERFORMANCE STATS        ")
            print("=" * 45)
            print(f"Total Students : {int(stats['count'])}")
            print(f"Class Average  : {stats['mean']:.2f}%")
            print(f"Median Score   : {stats['median']:.2f}%")
            print(f"Highest Score  : {stats['max']:.2f}%")
            print(f"Lowest Score   : {stats['min']:.2f}%")
            print(f"Std Deviation  : {stats['std_dev']:.2f}")
            print("=" * 45)

            draw_histogram(scores)

        elif choice == "3":
            try:
                score = float(input("\nEnter numeric score (0-100): ").strip())
                letter, gpa = score_to_letter_and_gpa(score)
                print(f"Score: {score:.1f}% -> Letter Grade: {letter} | GPA: {gpa:.1f}")
            except ValueError:
                print("[Error] Please enter a valid number.")


if __name__ == "__main__":
    run_grade_calculator_cli()
