"""computes metrics: coverage/traceability/ambiguity/testability"""

"""
08_metrics.py
-------------
Computes metrics for a given pipeline (manual, hybrid, or auto)
and saves results to the appropriate metrics file.

Usage:
    python src/08_metrics.py

You will be prompted to select which pipeline to compute metrics for.
"""

import json
import os
import re

# ── Pipeline configuration ─────────────────────────────────────────────────────
PIPELINES = {
    "manual": {
        "personas_file":     "personas/personas_manual.json",
        "spec_file":         "spec/spec_manual.md",
        "tests_file":        "tests/tests_manual.json",
        "groups_file":       "data/review_groups_manual.json",
        "output_file":       "metrics/metrics_manual.json",
    },
    "hybrid": {
        "personas_file":     "personas/personas_hybrid.json",
        "spec_file":         "spec/spec_hybrid.md",
        "tests_file":        "tests/tests_hybrid.json",
        "groups_file":       "data/review_groups_hybrid.json",
        "output_file":       "metrics/metrics_hybrid.json",
    },
    "auto": {
        "personas_file":     "personas/personas_auto.json",
        "spec_file":         "spec/spec_auto.md",
        "tests_file":        "tests/tests_auto.json",
        "groups_file":       "data/review_groups_auto.json",
        "output_file":       "metrics/metrics_auto.json",
    },
}

REVIEWS_FILE = "data/reviews_clean.jsonl"

# ── Ambiguous terms to flag in requirements ────────────────────────────────────
AMBIGUOUS_TERMS = [
    "fast", "quickly", "slow", "easy", "easily", "simple", "simply",
    "better", "best", "good", "nice", "user-friendly", "intuitive",
    "reasonable", "appropriate", "sufficient", "adequate", "efficient",
    "seamless", "smooth", "robust", "all else being equal", "as needed",
    "as appropriate", "in a timely manner", "regularly", "frequently",
    "occasionally", "minimal", "excessive", "significant", "several",
    "many", "some", "few", "large", "small", "high quality"
]

# ── Helpers ────────────────────────────────────────────────────────────────────

def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def count_jsonl_lines(path: str) -> int:
    count = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                count += 1
    return count


def parse_requirements(spec_path: str) -> list[dict]:
    """
    Parses requirements from a spec markdown file.
    Returns a list of dicts with keys: id, description, acceptance_criteria, source_persona.
    """
    requirements = []
    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"(?=# Requirement ID:)", content)

    for block in blocks:
        if "# Requirement ID:" not in block:
            continue

        req_id_match = re.search(r"# Requirement ID:\s*(\S+)", block)
        desc_match   = re.search(r"- Description:\s*(.+)", block)
        ac_match     = re.search(r"- Acceptance Criteria:\s*(.+)", block)
        persona_match = re.search(r"- Source Persona:\s*(.+)", block)

        requirements.append({
            "id":                  req_id_match.group(1).strip()  if req_id_match  else "",
            "description":         desc_match.group(1).strip()    if desc_match    else "",
            "acceptance_criteria": ac_match.group(1).strip()      if ac_match      else "",
            "source_persona":      persona_match.group(1).strip() if persona_match else "",
        })

    return requirements


def is_ambiguous(req: dict) -> bool:
    """Returns True if the requirement description or acceptance criteria contains ambiguous language."""
    text = (req["description"] + " " + req["acceptance_criteria"]).lower()
    return any(term in text for term in AMBIGUOUS_TERMS)


def count_traceability_links(requirements: list[dict]) -> int:
    """
    Counts explicit traceability links:
    - 1 link per requirement → persona (Source Persona field)
    - 1 link per requirement → group (Traceability field in spec)
    = 2 per requirement minimum.
    """
    return len(requirements) * 2


def compute_review_coverage(groups_data: dict, total_reviews: int) -> float:
    """Ratio of reviews assigned to at least one group over total cleaned reviews."""
    assigned = set()
    for g in groups_data["groups"]:
        for rid in g["review_ids"]:
            assigned.add(rid)
    return round(len(assigned) / total_reviews, 4) if total_reviews > 0 else 0.0


def compute_traceability_ratio(requirements: list[dict]) -> float:
    """Proportion of requirements with an explicit Source Persona reference."""
    if not requirements:
        return 0.0
    traced = sum(1 for r in requirements if r["source_persona"].strip())
    return round(traced / len(requirements), 4)


def compute_testability_rate(requirements: list[dict], tests_data: dict) -> float:
    """Proportion of requirements that have at least one associated test."""
    if not requirements:
        return 0.0
    tested_req_ids = set(t["requirement_id"] for t in tests_data["tests"])
    tested = sum(1 for r in requirements if r["id"] in tested_req_ids)
    return round(tested / len(requirements), 4)


def compute_ambiguity_ratio(requirements: list[dict]) -> float:
    """Proportion of requirements containing ambiguous or non-measurable language."""
    if not requirements:
        return 0.0
    ambiguous = sum(1 for r in requirements if is_ambiguous(r))
    return round(ambiguous / len(requirements), 4)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("── 08_metrics.py ─────────────────────────────────────────")
    print("Which pipeline would you like to compute metrics for?")
    print("  1. manual")
    print("  2. hybrid")
    print("  3. auto")
    choice = input("Enter 1, 2, or 3: ").strip()

    pipeline_map = {"1": "manual", "2": "hybrid", "3": "auto"}
    if choice not in pipeline_map:
        print("Invalid choice. Exiting.")
        return

    pipeline = pipeline_map[choice]
    config   = PIPELINES[pipeline]
    print(f"\nComputing metrics for pipeline: {pipeline}\n")

    # ── Load files ─────────────────────────────────────────────────────────────
    print("Loading files...")
    total_reviews = count_jsonl_lines(REVIEWS_FILE)
    personas_data = load_json(config["personas_file"])
    tests_data    = load_json(config["tests_file"])
    groups_data   = load_json(config["groups_file"])
    requirements  = parse_requirements(config["spec_file"])

    # ── Compute metrics ────────────────────────────────────────────────────────
    dataset_size        = total_reviews
    persona_count       = len(personas_data["personas"])
    requirements_count  = len(requirements)
    tests_count         = len(tests_data["tests"])
    traceability_links  = count_traceability_links(requirements)
    review_coverage     = compute_review_coverage(groups_data, total_reviews)
    traceability_ratio  = compute_traceability_ratio(requirements)
    testability_rate    = compute_testability_rate(requirements, tests_data)
    ambiguity_ratio     = compute_ambiguity_ratio(requirements)

    metrics = {
        "pipeline":            pipeline,
        "dataset_size":        dataset_size,
        "persona_count":       persona_count,
        "requirements_count":  requirements_count,
        "tests_count":         tests_count,
        "traceability_links":  traceability_links,
        "review_coverage":     review_coverage,
        "traceability_ratio":  traceability_ratio,
        "testability_rate":    testability_rate,
        "ambiguity_ratio":     ambiguity_ratio,
    }

    # ── Print results ──────────────────────────────────────────────────────────
    print("\n── Results ───────────────────────────────────────────────")
    for key, value in metrics.items():
        print(f"  {key:<25} {value}")

    # ── Save output ────────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(config["output_file"]), exist_ok=True)
    with open(config["output_file"], "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nSaved → {config['output_file']}")
    print("──────────────────────────────────────────────────────────")


if __name__ == "__main__":
    main()