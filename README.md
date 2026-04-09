# EECS4312_W26_SpecChain

## Application: Calm

Calm is a meditation and sleep app available on the Google Play Store. This project applies three requirements engineering pipelines — manual, automated, and hybrid — to transform user reviews into structured personas, specifications, and validation tests.

## Dataset

- `data/reviews_raw.jsonl` contains the 5,000 collected reviews.
- `data/reviews_clean.jsonl` contains the cleaned dataset.
- The cleaned dataset contains **3,944 reviews**.

**Collection method:** Reviews were collected from the Google Play Store using the `google-play-scraper` Python library via `src/01_collect_or_import.py`, sorting by newest and targeting 5,000 reviews.

**Cleaning steps applied:**
- Removed 178 duplicate reviews
- Removed 878 empty or extremely short reviews (fewer than 3 words)
- Removed emojis, unicode symbols, punctuation, and special characters
- Converted numbers to English word equivalents
- Normalized whitespace and converted to lowercase
- Removed English stop words and lemmatized tokens using spaCy (`en_core_web_sm`)

## Repository Structure

```
data/
  reviews_raw.jsonl           — raw collected reviews
  reviews_clean.jsonl         — cleaned dataset
  dataset_metadata.json       — collection and cleaning details
  review_groups_manual.json   — manually created review groups
  review_groups_auto.json     — automatically generated review groups
  review_groups_hybrid.json   — human-refined review groups

personas/
  personas_manual.json        — manually created personas
  personas_auto.json          — automatically generated personas
  personas_hybrid.json        — human-refined personas

spec/
  spec_manual.md              — manually written requirements
  spec_auto.md                — automatically generated requirements
  spec_hybrid.md              — human-refined requirements

tests/
  tests_manual.json           — manually written validation tests
  tests_auto.json             — automatically generated validation tests
  tests_hybrid.json           — human-refined validation tests

metrics/
  metrics_manual.json         — metrics for the manual pipeline
  metrics_auto.json           — metrics for the automated pipeline
  metrics_hybrid.json         — metrics for the hybrid pipeline
  metrics_summary.json        — side-by-side comparison of all three pipelines

prompts/
  prompt_auto.json            — LLM prompts used in the automated pipeline

src/
  00_validate_repo.py         — validates all required files are present
  01_collect_or_import.py     — collects reviews from the Google Play Store
  02_clean.py                 — cleans and preprocesses raw reviews
  03_manual_coding_template.py
  04_personas_manual.py
  05_personas_auto.py         — groups reviews and generates personas (LLM)
  06_spec_generate.py         — generates specifications from personas (LLM)
  07_tests_generate.py        — generates validation tests from spec (LLM)
  08_metrics.py               — computes pipeline metrics
  run_all.py                  — runs the full automated pipeline end to end

reflection/
  reflection.md               — comparison and discussion of all three pipelines
```

## How to Run

**1. Run the full automated pipeline:**
```bash
python src/run_all.py
```

`run_all.py` automatically installs all required dependencies, cleans the raw dataset, generates review groups, personas, specifications, and validation tests using the LLM, and computes metrics. No manual setup is required beyond providing a valid API key (see Notes below).

**2. Validate that all required files were generated:**
```bash
python src/00_validate_repo.py
```

Results will be available in `metrics/metrics_auto.json`. For a full comparison across all three pipelines see `metrics/metrics_summary.json`, and for a discussion of findings see `reflection/reflection.md`.

## Notes

- The automated pipeline requires a valid `GROQ_API_KEY` set in a `.env` file in the project root:
  ```
  GROQ_API_KEY=your_key_here
  ```
- All LLM calls use `meta-llama/llama-4-scout-17b-16e-instruct` via the Groq API.
- The `.env` file is listed in `.gitignore` and will not be committed to the repository.
- Dependencies installed automatically by `run_all.py`: `nltk`, `spacy`, `num2words`, `openai`, `python-dotenv`, and the `en_core_web_sm` spaCy language model.