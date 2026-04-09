"""
EECS 4312 - Course Project
Task 4.1 + Task 4.2: Group Reviews Automatically & Generate Personas Automatically
Script: src/05_personas_auto.py

Input: data/reviews_clean.jsonl

Outputs: data/review_groups_auto.json, personas/personas_auto.json, prompts/prompt_auto.json
"""

import os
import json
import random
from openai import OpenAI
from dotenv import load_dotenv
from time import sleep

load_dotenv()  # loads GROQ_API_KEY from .env file

MODEL         = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_API_KEY  = os.environ.get("GROQ_API_KEY")

SAMPLE_SIZE   = 200
BATCH_SIZE    = 50
TARGET_GROUPS = 5
RANDOM_SEED   = 42

INPUT_FILE        = "data/reviews_clean.jsonl"
FALLBACK_FILE     = "data/reviews_raw.jsonl"
GROUPS_OUTPUT     = "data/review_groups_auto.json"
PERSONAS_OUTPUT   = "personas/personas_auto.json"
PROMPTS_FILE      = "prompts/prompt_auto.json"

# Groq Stuff
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def call_llm(prompt: str, temperature: float = 0.2) -> str | None:
    """Send a prompt to the Groq LLM and return the text response."""
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


# Helper Methods
def load_reviews(path: str) -> list[dict]:
    """Load reviews from a JSONL file."""
    reviews = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                reviews.append(json.loads(line))
    return reviews


def safe_json_parse(text: str) -> dict | list | None:
    """Parse JSON from LLM response, stripping markdown fences if present."""
    if text is None:
        return None
    cleaned = text.strip()
    if cleaned.startswith("```"):
        parts = cleaned.split("```")
        # parts[1] will be 'json\n{...}' or just '{...}'
        cleaned = parts[1].lstrip("json").strip() if len(parts) > 1 else cleaned
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to extract the first complete JSON object or array
        for start_char, end_char in [('{', '}'), ('[', ']')]:
            start = cleaned.find(start_char)
            end   = cleaned.rfind(end_char)
            if start != -1 and end != -1:
                try:
                    return json.loads(cleaned[start:end+1])
                except json.JSONDecodeError:
                    pass
        return None


# Discover Groups Prompt
PHASE1_PROMPT_TEMPLATE = """\
You are a software requirements analyst studying user reviews of the Calm app \
(a meditation and sleep app on the Google Play Store).

Below is a sample of {n} user reviews. Your task is to identify exactly {k} \
meaningful, distinct themes that capture the main types of feedback users give.

For each theme:
- Give it a short, descriptive label
- Write a 1-sentence description of what kind of users/feedback belong to it
- Provide 3 representative short example phrases (not full reviews)

Respond ONLY with a valid JSON array. No explanation, no markdown, no preamble.

Format:
[
  {{
    "theme_id": "T1",
    "label": "Short theme label",
    "description": "One sentence describing this group of users and their feedback.",
    "example_phrases": ["phrase 1", "phrase 2", "phrase 3"]
  }}
]

REVIEWS:
{reviews}
"""

def discover_themes(reviews: list[dict]) -> list[dict] | None:
    """Phase 1: Sample reviews and ask the LLM to identify themes."""
    random.seed(RANDOM_SEED)
    sample = random.sample(reviews, min(SAMPLE_SIZE, len(reviews)))

    review_text = "\n".join(
        f"{i+1}. [{r['review_id']}] {r['text'][:300]}"
        for i, r in enumerate(sample)
    )

    prompt = PHASE1_PROMPT_TEMPLATE.format(
        n=len(sample),
        k=TARGET_GROUPS,
        reviews=review_text
    )

    print(f"  Phase 1: Sending {len(sample)} sampled reviews to LLM for theme discovery...")
    raw = call_llm(prompt, temperature=0.3)
    if raw is None:
        print("  Phase 1 FAILED: no response from LLM.")
        return None

    themes = safe_json_parse(raw)
    if not isinstance(themes, list):
        print(f"  Phase 1 FAILED: could not parse JSON.\nRaw response:\n{raw[:500]}")
        return None

    print(f"  Phase 1 SUCCESS: discovered {len(themes)} themes.")
    for t in themes:
        print(f"    {t.get('theme_id','?')} — {t.get('label','?')}")

    return themes


# Assign Reviews Prompt
PHASE2_PROMPT_TEMPLATE = """\
You are a software requirements analyst classifying user reviews of the Calm app.

Below are the {k} review themes you must use:
{themes_block}

Classify each of the following reviews into exactly one theme.
Respond ONLY with a valid JSON array. No explanation, no markdown, no preamble.

Format:
[
  {{"review_id": "R00001", "theme_id": "T1"}},
  ...
]

REVIEWS TO CLASSIFY:
{reviews}
"""

def assign_reviews_to_themes(reviews: list[dict], themes: list[dict]) -> dict[str, str]:
    """Phase 2: Assign every review to a theme in batches."""
    themes_block = "\n".join(
        f"- {t['theme_id']}: {t['label']} — {t['description']}"
        for t in themes
    )
    valid_ids  = {t["theme_id"] for t in themes}
    fallback   = themes[0]["theme_id"]

    assignments: dict[str, str] = {}
    batches = [reviews[i:i+BATCH_SIZE] for i in range(0, len(reviews), BATCH_SIZE)]
    total   = len(batches)

    print(f"  Phase 2: Classifying {len(reviews)} reviews in {total} batches of {BATCH_SIZE}...")

    for idx, batch in enumerate(batches):
        review_text = "\n".join(
            f"{r['review_id']}: {r['text'][:250]}"
            for r in batch
        )
        prompt = PHASE2_PROMPT_TEMPLATE.format(
            k=len(themes),
            themes_block=themes_block,
            reviews=review_text
        )

        raw    = call_llm(prompt, temperature=0.0)
        parsed = safe_json_parse(raw) if raw else None

        if isinstance(parsed, list):
            for item in parsed:
                rid = item.get("review_id")
                tid = item.get("theme_id")
                if rid and tid in valid_ids:
                    assignments[rid] = tid
                elif rid:
                    assignments[rid] = fallback
        else:
            print(f"    Batch {idx+1}/{total}: parse failed, assigning batch to fallback theme.")
            for r in batch:
                assignments[r["review_id"]] = fallback

        print(f"    Batch {idx+1}/{total} done. ({len(assignments)} reviews assigned so far)")
        sleep(0.5)  # rate limiting

    return assignments


def build_groups(reviews: list[dict], themes: list[dict], assignments: dict[str, str]) -> dict:
    """Assemble the review_groups_auto.json structure."""
    theme_to_reviews: dict[str, list[dict]] = {t["theme_id"]: [] for t in themes}
    review_map = {r["review_id"]: r for r in reviews}

    for rid, tid in assignments.items():
        if tid in theme_to_reviews and rid in review_map:
            theme_to_reviews[tid].append(review_map[rid])

    groups = []
    for i, theme in enumerate(themes):
        tid           = theme["theme_id"]
        group_reviews = theme_to_reviews[tid]
        group_id      = f"G{i+1}"

        # Pick up to 5 short example reviews for readability
        examples = sorted(group_reviews, key=lambda r: len(r["text"]))
        examples = [r["text"] for r in examples if len(r["text"]) > 30][:5]

        groups.append({
            "group_id":       group_id,
            "theme":          theme["label"] + " — " + theme["description"],
            "theme_id_ref":   tid,
            "review_ids":     [r["review_id"] for r in group_reviews],
            "example_reviews": examples
        })

    return {"groups": groups}


# Generate Personas Prompt
PHASE3_PROMPT_TEMPLATE = """\
You are a software requirements analyst creating a user persona for a requirements specification.

You are given a review group from the Calm app (a meditation and sleep app). \
Based on the group theme and example reviews below, generate one structured persona \
that represents this group of users.

The persona must include:
- name: a short, descriptive persona name (e.g. "The Frustrated Subscriber")
- description: one sentence summarising who this persona is and what defines them
- goals: a list of 3 specific things this persona wants to achieve using the app
- pain_points: a list of 3 specific frustrations or problems this persona experiences
- context: a list of 2 situations or scenarios in which this persona uses the app
- constraints: a list of 2 requirements or conditions the app must meet for this persona

Respond ONLY with a valid JSON object. No explanation, no markdown, no preamble.

Format:
{{
  "name": "Persona Name",
  "description": "One sentence description.",
  "goals": ["goal 1", "goal 2", "goal 3"],
  "pain_points": ["pain point 1", "pain point 2", "pain point 3"],
  "context": ["context 1", "context 2"],
  "constraints": ["constraint 1", "constraint 2"]
}}

GROUP THEME: {theme}

EXAMPLE REVIEWS FROM THIS GROUP:
{examples}
"""

def generate_personas(groups: list[dict]) -> list[dict]:
    """Phase 3: Generate one persona per review group."""
    personas = []

    print(f"  Phase 3: Generating {len(groups)} personas (one per group)...")

    for group in groups:
        group_id = group["group_id"]
        theme    = group["theme"]
        examples = "\n".join(f"- {ex}" for ex in group["example_reviews"])

        prompt = PHASE3_PROMPT_TEMPLATE.format(theme=theme, examples=examples)

        print(f"    Generating persona for {group_id}: {theme[:60]}...")
        raw    = call_llm(prompt, temperature=0.4)
        parsed = safe_json_parse(raw) if raw else None

        if not isinstance(parsed, dict):
            print(f"    WARNING: Could not parse persona for {group_id}. Using placeholder.")
            parsed = {
                "name":        f"Persona for {group_id}",
                "description": theme,
                "goals":       ["Goal not generated"],
                "pain_points": ["Pain point not generated"],
                "context":     ["Context not generated"],
                "constraints": ["Constraint not generated"]
            }

        persona_id = f"P{len(personas) + 1}"

        # Get up to 6 reviews
        evidence = group["review_ids"][:6]

        personas.append({
            "id":                 persona_id,
            "name":               parsed.get("name", f"Persona {persona_id}"),
            "description":        parsed.get("description", ""),
            "derived_from_group": group_id,
            "goals":              parsed.get("goals", []),
            "pain_points":        parsed.get("pain_points", []),
            "context":            parsed.get("context", []),
            "constraints":        parsed.get("constraints", []),
            "evidence_reviews":   evidence
        })

        sleep(0.5)  # rate limiting

    print(f"  Phase 3 SUCCESS: {len(personas)} personas generated.")
    return personas

def main():
    # Load Reviews
    if os.path.exists(INPUT_FILE):
        print(f"Loading cleaned reviews from {INPUT_FILE}...")
        reviews = load_reviews(INPUT_FILE)
    elif os.path.exists(FALLBACK_FILE):
        print(f"Clean file not found. Falling back to {FALLBACK_FILE}...")
        reviews = load_reviews(FALLBACK_FILE)
    else:
        print(f"ERROR: Neither {INPUT_FILE} nor {FALLBACK_FILE} found. Exiting.")
        return

    print(f"Loaded {len(reviews)} reviews.\n")

    # Discover Themes
    print("=" * 50)
    print("TASK 4.1 — GROUPING REVIEWS")
    print("=" * 50)

    themes = discover_themes(reviews)
    if themes is None:
        print("Aborting: theme discovery failed.")
        return

    print()

    # Assign Reviews
    assignments = assign_reviews_to_themes(reviews, themes)

    # Re-run for any reviews that got no assignment
    unassigned = [r for r in reviews if r["review_id"] not in assignments]
    if unassigned:
        print(f"\n  {len(unassigned)} reviews unassigned — running a second pass...")
        extra = assign_reviews_to_themes(unassigned, themes)
        assignments.update(extra)

    print(f"\n  Total assigned: {len(assignments)} / {len(reviews)}")

    # ── Save review groups ─────────────────────
    os.makedirs("data", exist_ok=True)
    groups_data = build_groups(reviews, themes, assignments)

    with open(GROUPS_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(groups_data, f, indent=2, ensure_ascii=False)
    print(f"\n  Saved → {GROUPS_OUTPUT}")

    print("\n  Group summary:")
    for g in groups_data["groups"]:
        print(f"    {g['group_id']} ({len(g['review_ids'])} reviews): {g['theme'][:75]}...")

    # Generate Personas
    print()
    print("=" * 50)
    print("TASK 4.2 — GENERATING PERSONAS")
    print("=" * 50)

    personas = generate_personas(groups_data["groups"])

    os.makedirs("personas", exist_ok=True)
    personas_data = {"personas": personas}

    with open(PERSONAS_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(personas_data, f, indent=2, ensure_ascii=False)
    print(f"\n  Saved → {PERSONAS_OUTPUT}")

    print("\n  Persona summary:")
    for p in personas:
        print(f"    {p['id']} ({p['derived_from_group']}): {p['name']}")

    # ── Save prompts record ────────────────────
    os.makedirs("prompts", exist_ok=True)
    prompts_record = {
        "prompt": [
            PHASE1_PROMPT_TEMPLATE,
            PHASE2_PROMPT_TEMPLATE,
            PHASE3_PROMPT_TEMPLATE
        ]
    }

    with open(PROMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts_record, f, indent=2, ensure_ascii=False)
    print(f"  Saved → {PROMPTS_FILE}")

    print("\nTasks 4.1 and 4.2 complete.")


if __name__ == "__main__":
    main()