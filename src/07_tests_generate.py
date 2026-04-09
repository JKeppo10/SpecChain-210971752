"""
EECS 4312 - Course Project
Task 4.4: Generate Validation Tests Automatically
Script: src/07_tests_generate.py

Input:  spec/spec_auto.md
Output: tests/tests_auto.json
"""

import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv
from time import sleep

load_dotenv()

MODEL        = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

SPEC_FILE   = "spec/spec_auto.md"
OUTPUT_FILE = "tests/tests_auto.json"

# Groq Stuff
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def call_llm(prompt: str, temperature: float = 0.3) -> str | None:
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"  [LLM ERROR] {e}")
        return None


def safe_json_parse(text: str) -> dict | list | None:
    if text is None:
        return None
    cleaned = text.strip()
    if cleaned.startswith("```"):
        parts = cleaned.split("```")
        cleaned = parts[1].lstrip("json").strip() if len(parts) > 1 else cleaned
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        for start_char, end_char in [('{', '}'), ('[', ']')]:
            start = cleaned.find(start_char)
            end   = cleaned.rfind(end_char)
            if start != -1 and end != -1:
                try:
                    return json.loads(cleaned[start:end+1])
                except json.JSONDecodeError:
                    pass
        return None


# read spec_auto.md
def parse_spec(spec_path: str) -> list[dict]:
    """
    Parse spec_auto.md into a list of requirement dicts.
    Expected format per requirement:
      # Requirement ID: FR_auto_1
      - Description: ...
      - Source Persona: ...
      - Traceability: ...
      - Acceptance Criteria: ...
    """
    requirements = []

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split on requirement headings
    blocks = re.split(r'(?=^# Requirement ID:)', content, flags=re.MULTILINE)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        req = {}

        # Requirement ID
        id_match = re.search(r'^# Requirement ID:\s*(.+)$', block, re.MULTILINE)
        if not id_match:
            continue
        req["req_id"] = id_match.group(1).strip()

        # Description
        desc_match = re.search(r'^- Description:\s*(.+)$', block, re.MULTILINE)
        req["description"] = desc_match.group(1).strip() if desc_match else ""

        # Source Persona
        persona_match = re.search(r'^- Source Persona:\s*(.+)$', block, re.MULTILINE)
        req["persona"] = persona_match.group(1).strip() if persona_match else ""

        # Traceability
        trace_match = re.search(r'^- Traceability:\s*(.+)$', block, re.MULTILINE)
        req["traceability"] = trace_match.group(1).strip() if trace_match else ""

        # Acceptance Criteria
        ac_match = re.search(r'^- Acceptance Criteria:\s*(.+)$', block, re.MULTILINE)
        req["acceptance_criteria"] = ac_match.group(1).strip() if ac_match else ""

        requirements.append(req)

    return requirements


# Prompt to generate test scenarios
TEST_PROMPT_TEMPLATE = """\
You are a software QA engineer writing validation tests for the Calm app (a meditation \
and sleep app on Android).

Given the requirement below, generate exactly 2 structured test scenarios that validate it. \
Each scenario should test a different aspect or condition of the requirement.

Respond ONLY with a valid JSON array. No explanation, no markdown, no preamble.

Format:
[
  {{
    "scenario": "Short description of what this test validates.",
    "steps": [
      "Step 1: ...",
      "Step 2: ...",
      "Step 3: ..."
    ],
    "expected_result": "What should happen if the requirement is correctly implemented."
  }},
  {{
    "scenario": "Short description of what this test validates.",
    "steps": [
      "Step 1: ...",
      "Step 2: ...",
      "Step 3: ..."
    ],
    "expected_result": "What should happen if the requirement is correctly implemented."
  }}
]

REQUIREMENT ID: {req_id}
DESCRIPTION: {description}
ACCEPTANCE CRITERIA: {acceptance_criteria}
"""


def generate_tests_for_requirement(req: dict) -> list[dict]:
    """Call LLM to generate 2 test scenarios for a single requirement."""
    prompt = TEST_PROMPT_TEMPLATE.format(
        req_id=req["req_id"],
        description=req["description"],
        acceptance_criteria=req["acceptance_criteria"]
    )

    raw    = call_llm(prompt, temperature=0.3)
    parsed = safe_json_parse(raw) if raw else None

    if not isinstance(parsed, list):
        print(f"  WARNING: Could not parse tests for {req['req_id']}. Using placeholders.")
        return [
            {
                "scenario":        f"Validate primary behaviour of {req['req_id']}.",
                "steps":           ["Step 1: Set up the test environment.",
                                    "Step 2: Perform the action described in the requirement.",
                                    "Step 3: Observe the system response."],
                "expected_result": "The system behaves as described in the requirement."
            },
            {
                "scenario":        f"Validate edge case behaviour of {req['req_id']}.",
                "steps":           ["Step 1: Set up the test environment with an edge case condition.",
                                    "Step 2: Perform the action described in the requirement.",
                                    "Step 3: Observe the system response."],
                "expected_result": "The system handles the edge case as described in the requirement."
            }
        ]

    return parsed

def main():
    # Load spec
    if not os.path.exists(SPEC_FILE):
        print(f"ERROR: {SPEC_FILE} not found. Run 06_spec_generate.py first.")
        return

    requirements = parse_spec(SPEC_FILE)
    print(f"Parsed {len(requirements)} requirements from {SPEC_FILE}\n")

    # Generate 2 test scenarios
    tests = []
    test_counter = 1

    for req in requirements:
        req_id = req["req_id"]
        print(f"  Generating 2 tests for {req_id}...")

        results = generate_tests_for_requirement(req)

        for result in results:
            tests.append({
                "test_id":         f"T_auto_{test_counter}",
                "requirement_id":  req_id,
                "scenario":        result.get("scenario", ""),
                "steps":           result.get("steps", []),
                "expected_result": result.get("expected_result", "")
            })
            test_counter += 1

        sleep(0.5)

    print(f"\n  Total tests generated: {len(tests)}")

    # Save to test_auto.json
    os.makedirs("tests", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"tests": tests}, f, indent=2, ensure_ascii=False)

    print(f"  Saved → {OUTPUT_FILE}")
    print("\nTask 4.4 complete.")


if __name__ == "__main__":
    main()