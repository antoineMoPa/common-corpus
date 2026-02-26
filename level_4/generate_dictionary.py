#!/usr/bin/env python3
"""
Generate dictionary definition .corpus files for the most frequent corpus words
that don't yet have an entry.

Usage:
    python generate_dictionary.py            # generate 1 entry (default)
    python generate_dictionary.py -n 10      # generate up to 10 entries
    python generate_dictionary.py -n 0       # dry-run: list next words only

Output: level_4/corpus/dictionary/<word>.corpus  (flat, one file per word)

Reads FAL_KEY from ~/.env (KEY=VALUE format, one per line).
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from collections import Counter

FAL_QUEUE_URL = "https://queue.fal.run/openrouter/router"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_ROOT = os.path.join(SCRIPT_DIR, "corpus")
DICT_DIR = os.path.join(CORPUS_ROOT, "dictionary")

MODEL = "qwen/qwen3-235b-a22b"

SYSTEM_PROMPT = (
    "You are a precise and educational lexicographer writing dictionary entries "
    "for a reading and literacy corpus. Write only the dictionary entry content — "
    "no meta commentary, no markdown formatting. Output plain prose."
)

ENTRY_PROMPT = (
    "Write a clear, concise dictionary definition for the word \"{word}\". "
    "Include: the part of speech, a plain-English definition (1–3 sentences), "
    "and one example sentence. Do not include the word \"{word}:\" as a header — "
    "start directly with the part of speech label (e.g. 'noun.', 'verb.', etc.)."
)


def load_key(name: str) -> str | None:
    env_path = os.path.expanduser("~/.env")
    if not os.path.exists(env_path):
        return None
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                if k.strip() == name:
                    return v.strip()
    return None


def word_frequencies(corpus_root: str) -> list[str]:
    """Walk all .corpus files and return words sorted by frequency (most common first)."""
    counter: Counter = Counter()
    for root, _dirs, files in os.walk(corpus_root):
        # Skip the dictionary dir itself to avoid circular counting
        if os.path.abspath(root).startswith(os.path.abspath(DICT_DIR)):
            continue
        for fname in files:
            if not fname.endswith(".corpus"):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except OSError:
                continue
            words = re.findall(r"[a-zA-Z']+", text.lower())
            for w in words:
                w = w.strip("'")
                if w:
                    counter[w] += 1
    return [word for word, _ in counter.most_common()]


def defined_words(dict_dir: str) -> set[str]:
    """Return the set of words that already have a .corpus file."""
    if not os.path.isdir(dict_dir):
        return set()
    return {
        fname[:-7]  # strip .corpus
        for fname in os.listdir(dict_dir)
        if fname.endswith(".corpus")
    }


def next_words(n: int) -> list[str]:
    """Return up to n words that need definitions, in popularity order."""
    already = defined_words(DICT_DIR)
    result = []
    for word in word_frequencies(CORPUS_ROOT):
        if word not in already:
            result.append(word)
        if len(result) == n:
            break
    return result


def _fal_request(api_key: str, method: str, url: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def generate_one(api_key: str, word: str, model: str) -> str:
    prompt = ENTRY_PROMPT.format(word=word)

    submit = _fal_request(api_key, "POST", FAL_QUEUE_URL, {
        "model": model,
        "system_prompt": SYSTEM_PROMPT,
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 512,
    })
    request_id = submit["request_id"]
    status_url = f"{FAL_QUEUE_URL}/requests/{request_id}/status"
    result_url = f"{FAL_QUEUE_URL}/requests/{request_id}"

    poll_interval = 2
    last_state = None
    while True:
        status = _fal_request(api_key, "GET", status_url)
        state = status.get("status")
        if state != last_state:
            print(f"[{state}] ", end="", flush=True)
            last_state = state
        else:
            print(".", end="", flush=True)
        if state == "COMPLETED":
            break
        if state in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"Request {state}: {status}")
        time.sleep(poll_interval)

    result = _fal_request(api_key, "GET", result_url)
    if result.get("error"):
        raise RuntimeError(result["error"])
    return result["output"].strip()


def main():
    parser = argparse.ArgumentParser(description="Generate dictionary .corpus entries for top missing words")
    parser.add_argument(
        "-n", type=int, default=1,
        help="Number of entries to generate (0 = dry-run, default: 1)",
    )
    parser.add_argument(
        "--model", type=str, default=MODEL,
        help=f"Model to use (default: {MODEL})",
    )
    args = parser.parse_args()

    print("Scanning corpus for word frequencies...", flush=True)
    # For dry-run, peek at a few more so the list is useful
    peek = max(args.n, 20) if args.n == 0 else args.n
    words = next_words(peek if args.n == 0 else args.n)

    if not words:
        print("All frequent words already have definitions.")
        return

    if args.n == 0:
        print(f"\nDry-run — next {len(words)} words without definitions:")
        for w in words:
            print(f"  {w}")
        return

    api_key = load_key("FAL_KEY")
    if not api_key:
        print("ERROR: FAL_KEY not found in ~/.env", file=sys.stderr)
        sys.exit(1)

    os.makedirs(DICT_DIR, exist_ok=True)
    print(f"Generating {len(words)} dictionary entr{'y' if len(words) == 1 else 'ies'} (model: {args.model})...\n")

    for i, word in enumerate(words, 1):
        out_path = os.path.join(DICT_DIR, f"{word}.corpus")
        print(f"[{i}/{len(words)}] {word} ... ", end="", flush=True)
        try:
            content = generate_one(api_key, word, args.model)
            with open(out_path, "w") as f:
                f.write(f'Dictionary entry for "{word.capitalize()}".\n{content}\n')
            print(f"OK ({len(content)} chars)")
        except Exception as e:
            print(f"FAILED: {e}")


if __name__ == "__main__":
    main()
