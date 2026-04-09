"""
EECS 4312 - Course Project
Task 4.3: Generate Specifications Automatically
Script: src/06_spec_generate.py

Input:  personas/personas_auto.json
Output: spec/spec_auto.md
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from time import sleep

load_dotenv()

MODEL            = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_API_KEY     = os.environ.get("GROQ_API_KEY")
REQS_PER_PERSONA = 3

PERSONAS_FILE = "personas/personas_auto.json"
OUTPUT_FILE   = "spec/spec_auto.md"

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


# Specification Prompt
SPEC_PROMPT_TEMPLATE = """\
You are a software requirements engineer writing a formal specification for the Calm app \
(a meditation and sleep app on Android).

Using the persona below, generate exactly {n} software requirements that describe \
specific system behaviors the app must support to satisfy this persona's needs.

Each requirement must be specific, measurable, and unambiguous.
Classify each requirement as either:
  - "FR" (Functional Requirement): describes a specific system behavior or feature
  - "NFR" (Non-Functional Requirement): describes a quality attribute such as performance, \
reliability, usability, or security

The acceptance criteria must use Gherkin format: a single string starting with \
"Given", "When", and "Then" on the same line or separated by commas.

Respond ONLY with a valid JSON array. No explanation, no markdown, no preamble.

Format:
[
  {{
    "type": "FR",
    "description": "The system shall...",
    "acceptance_criteria": "Given <precondition>, When <action>, Then <expected result>."
  }}
]

PERSONA:
Name: {name}
Description: {description}
Goals:
{goals}
Pain Points:
{pain_points}
Constraints:
{constraints}
"""


def generate_requirements_for_persona(persona: dict) -> list[dict]:
    """Call LLM to generate requirements for a single persona."""
    prompt = SPEC_PROMPT_TEMPLATE.format(
        n=REQS_PER_PERSONA,
        name=persona["name"],
        description=persona["description"],
        goals="\n".join(f"- {g}" for g in persona.get("goals", [])),
        pain_points="\n".join(f"- {p}" for p in persona.get("pain_points", [])),
        constraints="\n".join(f"- {c}" for c in persona.get("constraints", []))
    )

    raw    = call_llm(prompt, temperature=0.3)
    parsed = safe_json_parse(raw) if raw else None

    if not isinstance(parsed, list):
        print(f"  WARNING: Could not parse requirements for {persona['name']}. Using placeholder.")
        return [{
            "description": f"The system shall support the needs of {persona['name']}.",
            "acceptance_criteria": "Given the user opens the app, When they attempt to use a core feature, Then the feature shall function as expected."
        }]

    return parsed


# Format Markdown
def format_spec_markdown(all_requirements: list[dict]) -> str:
    """Render all requirements into markdown matching the spec_manual.md template."""
    lines = []

    for req in all_requirements:
        lines.append(f"# Requirement ID: {req['req_id']}")
        lines.append(f"- Description: {req['description']}")
        lines.append(f"- Source Persona: {req['persona_name']}")
        lines.append(f"- Traceability: Derived from review group {req['review_group']}")
        lines.append(f"- Acceptance Criteria: {req['acceptance_criteria']}")
        lines.append("")  # blank line between requirements

    return "\n".join(lines)

def main():
    # Load Personas
    if not os.path.exists(PERSONAS_FILE):
        print(f"ERROR: {PERSONAS_FILE} not found. Run 05_personas_auto.py first.")
        return

    with open(PERSONAS_FILE, "r", encoding="utf-8") as f:
        personas_data = json.load(f)

    personas = personas_data.get("personas", [])
    print(f"Loaded {len(personas)} personas from {PERSONAS_FILE}\n")

    # Generate Requirements
    all_requirements = []
    fr_counter  = 1
    nfr_counter = 1

    for persona in personas:
        persona_id   = persona["id"]
        persona_name = persona["name"]
        group_id     = persona.get("derived_from_group", "G?")

        print(f"  Generating requirements for {persona_id} — {persona_name}...")

        reqs = generate_requirements_for_persona(persona)

        for req in reqs:
            req_type = req.get("type", "FR").upper()
            if req_type == "NFR":
                req_id = f"NFR_auto_{nfr_counter}"
                nfr_counter += 1
            else:
                req_id = f"FR_auto_{fr_counter}"
                fr_counter += 1

            all_requirements.append({
                "req_id":              req_id,
                "description":         req.get("description", ""),
                "persona_id":          persona_id,
                "persona_name":        persona_name,
                "review_group":        group_id,
                "acceptance_criteria": req.get("acceptance_criteria", "")
            })

        print(f"    Generated {len(reqs)} requirements. (Total so far: {len(all_requirements)})")
        sleep(0.5)

    print(f"\n  Total requirements generated: {len(all_requirements)}")

    # write to spec_auto.md
    os.makedirs("spec", exist_ok=True)
    spec_md = format_spec_markdown(all_requirements)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(spec_md)

    print(f"  Saved → {OUTPUT_FILE}")
    print("\nTask 4.3 complete.")


if __name__ == "__main__":
    main()