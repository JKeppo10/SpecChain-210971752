"""imports or reads your raw dataset; if you scraped, include scraper here"""

"""
01_collect_or_import.py
-----------------------
Collects reviews for the Calm app from the Google Play Store
and saves them to data/reviews_raw.jsonl.

Requirements:
    pip install google-play-scraper

Usage:
    python src/01_collect_or_import.py
"""

import json
import os
import time
from datetime import datetime

from google_play_scraper import reviews, Sort


# ── Configuration ──────────────────────────────────────────────────────────────
APP_ID       = "com.calm.android"          # Calm's Google Play package ID
TARGET_COUNT = 5000                        # Aim for up to 5,000 reviews
LANG         = "en"                        # English reviews only
COUNTRY      = "us"                        # US store
BATCH_SIZE   = 200                         # Reviews fetched per API call
OUTPUT_PATH  = "data/reviews_raw.jsonl"
# ──────────────────────────────────────────────────────────────────────────────


def collect_reviews(app_id: str, target: int) -> list[dict]:
    """
    Fetches up to `target` reviews from the Play Store in batches.
    Returns a list of review dicts, each assigned a unique review_id.
    """
    all_reviews = []
    continuation_token = None
    batch_num = 0

    print(f"Starting collection for app: {app_id}")
    print(f"Target: {target} reviews\n")

    while len(all_reviews) < target:
        remaining = target - len(all_reviews)
        count = min(BATCH_SIZE, remaining)

        try:
            result, continuation_token = reviews(
                app_id,
                lang=LANG,
                country=COUNTRY,
                sort=Sort.NEWEST,
                count=count,
                continuation_token=continuation_token,
            )
        except Exception as e:
            print(f"[ERROR] API call failed on batch {batch_num}: {e}")
            break

        if not result:
            print("No more reviews available from the store.")
            break

        all_reviews.extend(result)
        batch_num += 1
        print(f"  Batch {batch_num:>3}: fetched {len(result):>4} reviews  |  "
              f"total so far: {len(all_reviews):>5}")

        # Stop if the API has no more pages
        if continuation_token is None:
            print("Reached end of available reviews.")
            break

        # Be polite to the API
        time.sleep(0.5)

    print(f"\nCollection complete. Total fetched: {len(all_reviews)}")
    return all_reviews


def format_review(raw: dict, idx: int) -> dict:
    """
    Normalises a raw google-play-scraper review dict into a clean record
    with a deterministic review_id.
    """
    return {
        "review_id": f"R{idx:05d}",          # e.g. R00001
        "app_id":    APP_ID,
        "author":    raw.get("userName", ""),
        "rating":    raw.get("score", None),
        "date":      raw.get("at").strftime("%Y-%m-%d") if raw.get("at") else None,
        "text":      raw.get("content", ""),
        "thumbs_up": raw.get("thumbsUpCount", 0),
        "app_version": raw.get("appVersion", ""),
        "reply_text":  raw.get("replyContent", ""),
        "collected_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def save_jsonl(records: list[dict], path: str) -> None:
    """Writes a list of dicts to a .jsonl file (one JSON object per line)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Saved {len(records)} reviews → {path}")


def main() -> None:
    raw_reviews = collect_reviews(APP_ID, TARGET_COUNT)

    # Remove any reviews with no text content
    raw_reviews = [r for r in raw_reviews if r.get("content", "").strip()]
    print(f"After removing blank-text reviews: {len(raw_reviews)}")

    formatted = [format_review(r, i + 1) for i, r in enumerate(raw_reviews)]
    save_jsonl(formatted, OUTPUT_PATH)

    # Quick summary
    print("\n── Summary ──────────────────────────────────")
    print(f"  App            : {APP_ID}")
    print(f"  Reviews saved  : {len(formatted)}")
    print(f"  Output file    : {OUTPUT_PATH}")
    print("─────────────────────────────────────────────")


if __name__ == "__main__":
    main()