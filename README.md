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
- Removed English stop words and lemmatized tokens using spaCy

## Repository Structure

```
data/         — raw and cleaned datasets, review group files
personas/     — persona files for all three pipelines
spec/         — specification files for all three pipelines
tests/        — validation test files for all three pipelines
metrics/      — metric files and summary for all three pipelines
prompts/      — LLM prompts used in the automated pipeline
src/          — all executable Python scripts
reflection/   — final reflection
```

## How to Run

**1. Validate the repository structure:**
```bash
python src/00_validate_repo.py
```

**2. Run the full automated pipeline** (cleans raw data, groups reviews, generates personas, specs, tests, and computes metrics):
```bash
python src/run_all.py
```

Results will be available in `metrics/metrics_auto.json` and `reflection/reflection.md`.

## Notes

- The automated pipeline requires a valid `GROQ_API_KEY` set in a `.env` file in the project root.
- All LLM calls use `meta-llama/llama-4-scout-17b-16e-instruct` via the Groq API.