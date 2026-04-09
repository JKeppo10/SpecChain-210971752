"""
EECS 4312 - Course Project
Task 7: Ensure Reproducibility
Script: src/run_all.py

Executes the full automated pipeline from start to finish.
Does NOT run manual or hybrid steps (those require human judgment).

Steps executed:
    1. 02_clean.py          → loads raw reviews and produces cleaned dataset
    2. 05_personas_auto.py  → groups reviews + generates personas (LLM)
    3. 06_spec_generate.py  → generates specifications (LLM)
    4. 07_tests_generate.py → generates validation tests (LLM)
    5. 08_metrics.py        → computes metrics for the auto pipeline

Files produced at each stage:
    1. data/reviews_clean.jsonl, data/dataset_metadata.json
    2. data/review_groups_auto.json, personas/personas_auto.json, prompts/prompt_auto.json
    3. spec/spec_auto.md
    4. tests/tests_auto.json
    5. metrics/metrics_auto.json

Usage:
    python src/run_all.py
"""

import subprocess
import sys
import os


def run_step(step_num: int, description: str, script: str, piped_input: str = None):
    """Run a single pipeline step and exit on failure."""
    print(f"\n{'='*60}")
    print(f"  STEP {step_num}: {description}")
    print(f"  Script: {script}")
    print(f"{'='*60}")

    result = subprocess.run(
        [sys.executable, script],
        input=piped_input,
        text=True
    )

    if result.returncode != 0:
        print(f"\n  ERROR: Step {step_num} failed with exit code {result.returncode}.")
        print(f"  Fix the error in {script} before re-running.")
        sys.exit(result.returncode)

    print(f"\n  Step {step_num} complete.")


def main():
    print("\n" + "="*60)
    print("  EECS 4312 — SpecChain Automated Pipeline")
    print("  run_all.py — Full automated workflow")
    print("="*60)

    # Confirm we're running from the project root
    if not os.path.exists("src"):
        print("ERROR: Please run this script from the project root directory.")
        print("  Usage: python src/run_all.py")
        sys.exit(1)

    # ── Step 1: Load raw dataset and clean ────────────────────────
    # Reads:   data/reviews_raw.jsonl
    # Writes:  data/reviews_clean.jsonl, data/dataset_metadata.json
    run_step(1, "Load raw dataset and clean reviews", "src/02_clean.py")

    # ── Step 2: Group reviews + generate personas ──────────────────
    # Reads:   data/reviews_clean.jsonl
    # Writes:  data/review_groups_auto.json
    #          personas/personas_auto.json
    #          prompts/prompt_auto.json
    run_step(2, "Group reviews and generate personas (LLM)", "src/05_personas_auto.py")

    # ── Step 3: Generate specifications ───────────────────────────
    # Reads:   personas/personas_auto.json
    # Writes:  spec/spec_auto.md
    run_step(3, "Generate specifications (LLM)", "src/06_spec_generate.py")

    # ── Step 4: Generate validation tests ─────────────────────────
    # Reads:   spec/spec_auto.md
    # Writes:  tests/tests_auto.json
    run_step(4, "Generate validation tests (LLM)", "src/07_tests_generate.py")

    # ── Step 5: Compute metrics ────────────────────────────────────
    # Reads:   all auto pipeline artifacts
    # Writes:  metrics/metrics_auto.json
    # Passes "3" to select the "auto" pipeline in the interactive prompt
    run_step(5, "Compute metrics for automated pipeline", "src/08_metrics.py", piped_input="3\n")

    print("\n" + "="*60)
    print("  Automated pipeline complete.")
    print("  All output files have been generated:")
    print("    data/reviews_clean.jsonl")
    print("    data/review_groups_auto.json")
    print("    personas/personas_auto.json")
    print("    prompts/prompt_auto.json")
    print("    spec/spec_auto.md")
    print("    tests/tests_auto.json")
    print("    metrics/metrics_auto.json")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()