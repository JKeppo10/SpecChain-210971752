"""
EECS 4312 - Course Project
Task 7: Ensure Reproducibility
Script: src/00_validate_repo.py

Checks whether all required folders and files exist in the repository.
Prints a clear message for each file indicating found or missing status.

Usage:
    python src/00_validate_repo.py
"""

import os

# ── All required files ─────────────────────────────────────────────────────────
REQUIRED_FILES = [
    # Data
    "data/reviews_raw.jsonl",
    "data/reviews_clean.jsonl",
    "data/dataset_metadata.json",
    "data/review_groups_manual.json",
    "data/review_groups_auto.json",
    "data/review_groups_hybrid.json",

    # Personas
    "personas/personas_manual.json",
    "personas/personas_auto.json",
    "personas/personas_hybrid.json",

    # Specifications
    "spec/spec_manual.md",
    "spec/spec_auto.md",
    "spec/spec_hybrid.md",

    # Tests
    "tests/tests_manual.json",
    "tests/tests_auto.json",
    "tests/tests_hybrid.json",

    # Metrics
    "metrics/metrics_manual.json",
    "metrics/metrics_auto.json",
    "metrics/metrics_hybrid.json",
    "metrics/metrics_summary.json",

    # Prompts
    "prompts/prompt_auto.json",

    # Source scripts
    "src/00_validate_repo.py",
    "src/01_collect_or_import.py",
    "src/02_clean.py",
    "src/03_manual_coding_template.py",
    "src/04_personas_manual.py",
    "src/05_personas_auto.py",
    "src/06_spec_generate.py",
    "src/07_tests_generate.py",
    "src/08_metrics.py",
    "src/run_all.py",

    # Docs
    "README.md",
    "reflection/reflection.md",
]


def main():
    print("Checking repository structure...")

    missing = []

    for filepath in REQUIRED_FILES:
        if os.path.exists(filepath):
            print(f"  {filepath} found")
        else:
            print(f"  {filepath} MISSING")
            missing.append(filepath)

    print()

    if missing:
        print(f"Repository validation INCOMPLETE — {len(missing)} file(s) missing:")
        for f in missing:
            print(f"  - {f}")
    else:
        print("Repository validation complete")


if __name__ == "__main__":
    main()