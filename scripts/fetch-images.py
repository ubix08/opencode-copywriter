#!/usr/bin/env python3
"""
Image fetcher for technical articles.
Replaces image placeholder comments with real images from Pexels (photos) or Hugging Face (diagrams).

Usage:
    python3 scripts/fetch-images.py <article.md> [--pexels-key KEY] [--hf-token TOKEN] [--dry-run]

Placeholder format in markdown:
    <!-- image: query="search terms" type="photo|diagram" alt="descriptive alt text" -->

Output:
    - Downloads images to content/images/
    - Replaces placeholders with ![alt](content/images/filename.jpg)
    - Prints summary of actions taken
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)

# Constants
PEXELS_API_URL = "https://api.pexels.com/v1/search"
HF_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
IMAGES_DIR = "content/images"
MAX_RETRIES = 2
REQUEST_TIMEOUT = 30


def slugify(text: str) -> str:
    """Convert text to a safe filename slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = text[:60]  # Keep filename reasonable
    return text or "image"


def find_placeholders(content: str) -> list[dict]:
    """Find all image placeholder comments in markdown content."""
    pattern = r'<!--\s*image:\s*query="([^"]+)"\s+type="([^"]+)"\s+alt="([^"]+)"\s*-->'
    matches = re.finditer(pattern, content)
    placeholders = []
    for m in matches:
        placeholders.append({
            "full_match": m.group(0),
            "query": m.group(1),
            "type": m.group(2),
            "alt": m.group(3),
            "start": m.start(),
            "end": m.end(),
        })
    return placeholders


def search_pexels(query: str, api_key: str) -> dict | None:
    """Search Pexels for a photo. Returns the best match or None."""
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": 3, "orientation": "landscape"}

    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.get(PEXELS_API_URL, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                data = resp.json()
                photos = data.get("photos", [])
                if photos:
                    photo = photos[0]
                    return {
                        "url": photo["src"]["large"],
                        "original": photo["src"]["original"],
                        "photographer": photo.get("photographer", "Unknown"),
                        "photographer_url": photo.get("photographer_url", ""),
                        "alt": photo.get("alt", ""),
                    }
                return None
            elif resp.status_code == 401:
                print(f"  Pexels auth error (401). Check your API key.")
                return None
            elif resp.status_code == 429:
                wait = 2 ** attempt
                print(f"  Pexels rate limited. Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  Pexels error: {resp.status_code}")
                return None
        except requests.RequestException as e:
            print(f"  Pexels request failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(2 ** attempt)
    return None


def generate_hf_image(prompt: str, hf_token: str) -> bytes | None:
    """Generate an image using Hugging Face FLUX.1-schnell. Returns image bytes or None."""
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json",
    }
    # Enhance prompt for technical diagrams
    enhanced_prompt = (
        f"Technical illustration: {prompt}. "
        f"Clean, professional, minimalist style. "
        f"White background, clear labels, modern design. "
        f"No text, no words, just visual elements."
    )
    payload = {
        "inputs": enhanced_prompt,
        "parameters": {
            "num_inference_steps": 4,
            "guidance_scale": 3.5,
            "width": 1024,
            "height": 576,
        },
    }

    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.post(HF_API_URL, headers=headers, json=payload, timeout=REQUEST_TIMEOUT * 2)
            if resp.status_code == 200:
                return resp.content
            elif resp.status_code == 503:
                # Model loading
                retry_after = resp.headers.get("retry-after", "30")
                wait = int(retry_after) if retry_after.isdigit() else 30
                print(f"  HF model loading. Waiting {wait}s...")
                time.sleep(min(wait, 60))
            elif resp.status_code == 401:
                print(f"  HF auth error (401). Check your token.")
                return None
            elif resp.status_code == 429:
                wait = 2 ** attempt
                print(f"  HF rate limited. Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  HF error: {resp.status_code} - {resp.text[:200]}")
                return None
        except requests.RequestException as e:
            print(f"  HF request failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(2 ** attempt)
    return None


def download_image(url: str, filename: str) -> bool:
    """Download an image from URL to content/images/filename."""
    os.makedirs(IMAGES_DIR, exist_ok=True)
    filepath = os.path.join(IMAGES_DIR, filename)

    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT, stream=True)
        if resp.status_code == 200:
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            size = os.path.getsize(filepath)
            print(f"  Downloaded: {filepath} ({size:,} bytes)")
            return True
        else:
            print(f"  Download failed: {resp.status_code}")
            return False
    except requests.RequestException as e:
        print(f"  Download error: {e}")
        return False


def save_image_bytes(data: bytes, filename: str) -> bool:
    """Save image bytes to content/images/filename."""
    os.makedirs(IMAGES_DIR, exist_ok=True)
    filepath = os.path.join(IMAGES_DIR, filename)

    try:
        with open(filepath, "wb") as f:
            f.write(data)
        size = os.path.getsize(filepath)
        print(f"  Saved: {filepath} ({size:,} bytes)")
        return True
    except IOError as e:
        print(f"  Save error: {e}")
        return False


def process_article(filepath: str, pexels_key: str | None, hf_token: str | None, dry_run: bool = False) -> dict:
    """Process an article file, replacing image placeholders with real images."""
    with open(filepath, "r") as f:
        content = f.read()

    placeholders = find_placeholders(content)
    if not placeholders:
        print("No image placeholders found.")
        return {"found": 0, "replaced": 0, "failed": 0, "skipped": 0}

    print(f"Found {len(placeholders)} image placeholder(s).\n")

    results = {"found": len(placeholders), "replaced": 0, "failed": 0, "skipped": 0}
    replacements = []

    for i, ph in enumerate(placeholders, 1):
        query = ph["query"]
        ptype = ph["type"]
        alt = ph["alt"]
        print(f"[{i}/{len(placeholders)}] {ptype}: '{query}'")

        if dry_run:
            print(f"  [DRY RUN] Would fetch {ptype} for '{query}'")
            results["skipped"] += 1
            continue

        image_url = None
        filename = None

        if ptype == "photo":
            if not pexels_key:
                print(f"  Skipped: No Pexels API key configured.")
                results["skipped"] += 1
                continue

            photo = search_pexels(query, pexels_key)
            if photo:
                slug = slugify(query)
                # Use hash to avoid filename collisions
                file_hash = hashlib.md5(query.encode()).hexdigest()[:6]
                filename = f"{slug}-{file_hash}.jpg"
                if download_image(photo["url"], filename):
                    image_url = f"{IMAGES_DIR}/{filename}"
                    # Add photographer credit as HTML comment
                    credit = f"<!-- Photo by {photo['photographer']} from Pexels: {photo['photographer_url']} -->"
                    replacements.append((ph["full_match"], f"![{alt}]({image_url})\n\n{credit}"))
                    results["replaced"] += 1
                else:
                    print(f"  Failed to download photo.")
                    results["failed"] += 1
            else:
                print(f"  No photo found for '{query}'.")
                results["failed"] += 1

        elif ptype == "diagram":
            if not hf_token:
                print(f"  Skipped: No Hugging Face token configured.")
                results["skipped"] += 1
                continue

            print(f"  Generating diagram (this may take 30-60s)...")
            image_data = generate_hf_image(query, hf_token)
            if image_data:
                slug = slugify(query)
                file_hash = hashlib.md5(query.encode()).hexdigest()[:6]
                filename = f"{slug}-{file_hash}.png"
                if save_image_bytes(image_data, filename):
                    image_url = f"{IMAGES_DIR}/{filename}"
                    replacements.append((ph["full_match"], f"![{alt}]({image_url})"))
                    results["replaced"] += 1
                else:
                    print(f"  Failed to save diagram.")
                    results["failed"] += 1
            else:
                print(f"  Failed to generate diagram.")
                results["failed"] += 1
        else:
            print(f"  Unknown type: {ptype}")
            results["failed"] += 1

        print()

    # Apply replacements to content (in reverse order to preserve positions)
    if replacements and not dry_run:
        for old, new in reversed(replacements):
            content = content.replace(old, new, 1)

        with open(filepath, "w") as f:
            f.write(content)
        print(f"Updated {filepath} with {len(replacements)} image(s).")

    return results


def main():
    parser = argparse.ArgumentParser(description="Fetch images for technical articles")
    parser.add_argument("article", help="Path to the markdown article file")
    parser.add_argument("--pexels-key", help="Pexels API key (or set PEXELS_API_KEY env var)")
    parser.add_argument("--hf-token", help="Hugging Face token (or set HF_TOKEN env var)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without fetching")
    parser.add_argument("--output-json", help="Output results as JSON to this file")
    args = parser.parse_args()

    pexels_key = args.pexels_key or os.environ.get("PEXELS_API_KEY")
    hf_token = args.hf_token or os.environ.get("HF_TOKEN")

    if not os.path.isfile(args.article):
        print(f"Error: File not found: {args.article}")
        sys.exit(1)

    if not pexels_key and not hf_token:
        print("Error: No API keys provided. Set --pexels-key, --hf-token, or environment variables.")
        print("  Pexels API key: https://www.pexels.com/api/")
        print("  Hugging Face token: https://huggingface.co/settings/tokens")
        sys.exit(1)

    print(f"Processing: {args.article}")
    if args.dry_run:
        print("Mode: DRY RUN (no images will be fetched)\n")
    else:
        print(f"Pexels: {'configured' if pexels_key else 'not configured'}")
        print(f"Hugging Face: {'configured' if hf_token else 'not configured'}")
        print()

    results = process_article(args.article, pexels_key, hf_token, args.dry_run)

    print(f"\nSummary: {results['found']} found, {results['replaced']} replaced, {results['failed']} failed, {results['skipped']} skipped")

    if args.output_json:
        with open(args.output_json, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {args.output_json}")

    sys.exit(0 if results["failed"] == 0 and results["skipped"] == 0 else 1)


if __name__ == "__main__":
    main()
