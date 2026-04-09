"""cleans raw data & make clean dataset"""

"""
02_clean.py
-----------
input: data/reviews_raw.jsonl
output: data/reviews_clean.jsonl.

Cleaning steps:
    1. Remove duplicate reviews
    2. Remove empty or extremely short reviews (< 3 words)
    3. Remove punctuation
    4. Remove special characters and emojis
    5. Convert numbers to text
    6. Remove extra whitespace
    7. Convert all words to lowercase
    8. Remove stop words
    9. Lemmatize the reviews
"""

import json
import os
import re
import unicodedata

import nltk
import spacy
from nltk.corpus import stopwords
from num2words import num2words

# ── Download required NLTK data (safe to run multiple times) ──────────────────
nltk.download("stopwords", quiet=True)

# ── Load spaCy English model ───────────────────────────────────────────────────
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])  # only need tagger

# ── Stop words set ─────────────────────────────────────────────────────────────
STOP_WORDS = set(stopwords.words("english"))

# ── Paths ──────────────────────────────────────────────────────────────────────
INPUT_PATH  = "data/reviews_raw.jsonl"
OUTPUT_PATH = "data/reviews_clean.jsonl"
MIN_WORDS   = 3   # reviews shorter than this are dropped
# ──────────────────────────────────────────────────────────────────────────────


def load_jsonl(path: str) -> list[dict]:
    """Loads a .jsonl file and returns a list of dicts."""
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    print(f"Loaded {len(records)} raw reviews from {path}")
    return records


def save_jsonl(records: list[dict], path: str) -> None:
    """Writes a list of dicts to a .jsonl file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Saved {len(records)} clean reviews → {path}")


# ── Individual cleaning helpers ────────────────────────────────────────────────

def remove_emojis(text: str) -> str:
    """Removes emoji and other non-ASCII unicode symbols."""
    # Strip characters in unicode categories: So (other symbol), Sm, Sk, etc.
    cleaned = []
    for char in text:
        cat = unicodedata.category(char)
        if cat.startswith("S") or cat.startswith("C"):
            cleaned.append(" ")
        else:
            cleaned.append(char)
    return "".join(cleaned)


def convert_numbers(text: str) -> str:
    """Replaces integer tokens with their English word equivalents."""
    tokens = text.split()
    result = []
    for token in tokens:
        if token.isdigit():
            try:
                result.append(num2words(int(token)))
            except Exception:
                result.append(token)
        else:
            result.append(token)
    return " ".join(result)


def remove_punctuation(text: str) -> str:
    """Removes all punctuation characters."""
    return re.sub(r"[^\w\s]", " ", text)


def remove_special_characters(text: str) -> str:
    """Removes non-alphanumeric, non-space characters."""
    return re.sub(r"[^a-zA-Z0-9\s]", " ", text)


def normalize_whitespace(text: str) -> str:
    """Collapses multiple spaces/newlines into a single space."""
    return re.sub(r"\s+", " ", text).strip()


def remove_stopwords(text: str) -> str:
    """Removes English stop words."""
    tokens = text.split()
    return " ".join(t for t in tokens if t not in STOP_WORDS)


def lemmatize(text: str) -> str:
    """Lemmatizes each token using spaCy."""
    doc = nlp(text)
    return " ".join(token.lemma_ for token in doc)


# ── Full cleaning pipeline ─────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """Applies all cleaning steps to a single review text string."""
    text = remove_emojis(text)         # step 1: remove emojis
    text = remove_punctuation(text)    # step 2: remove punctuation
    text = remove_special_characters(text)  # step 3: remove special chars
    text = text.lower()                # step 4: lowercase
    text = convert_numbers(text)       # step 5: numbers → words
    text = normalize_whitespace(text)  # step 6: clean up spaces
    text = remove_stopwords(text)      # step 7: remove stop words
    text = lemmatize(text)             # step 8: lemmatize
    text = normalize_whitespace(text)  # step 9: final whitespace cleanup
    return text


def is_too_short(text: str, min_words: int = MIN_WORDS) -> bool:
    """Returns True if the cleaned text has fewer than min_words tokens."""
    return len(text.split()) < min_words


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    records = load_jsonl(INPUT_PATH)

    # ── Step 1: Remove duplicates by review text ───────────────────────────────
    seen_texts = set()
    unique_records = []
    for r in records:
        text = r.get("text", "").strip()
        if text and text not in seen_texts:
            seen_texts.add(text)
            unique_records.append(r)

    duplicates_removed = len(records) - len(unique_records)
    print(f"Duplicates removed  : {duplicates_removed}")

    # ── Step 2: Clean each review ──────────────────────────────────────────────
    cleaned_records = []
    short_removed = 0

    for r in unique_records:
        cleaned_text = clean_text(r.get("text", ""))

        if is_too_short(cleaned_text):
            short_removed += 1
            continue

        cleaned_record = dict(r)           # preserve all original fields
        cleaned_record["text"] = cleaned_text
        cleaned_records.append(cleaned_record)

    print(f"Too-short removed   : {short_removed}")
    print(f"Final clean count   : {len(cleaned_records)}")

    save_jsonl(cleaned_records, OUTPUT_PATH)

    # ── Summary ────────────────────────────────────────────────────────────────
    print("\n── Cleaning Summary ─────────────────────────────")
    print(f"  Raw reviews       : {len(records)}")
    print(f"  Duplicates removed: {duplicates_removed}")
    print(f"  Too-short removed : {short_removed}")
    print(f"  Clean reviews     : {len(cleaned_records)}")
    print(f"  Output            : {OUTPUT_PATH}")
    print("─────────────────────────────────────────────────")


if __name__ == "__main__":
    main()