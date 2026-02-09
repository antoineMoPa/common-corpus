# Level 4 — LLM Training Corpus

Generated text corpus for training a small language model. Content is produced by prompting an LLM via [fal.ai](https://fal.ai)'s OpenRouter endpoint.

## Corpus structure

```
corpus/
├── stories/                 # Fiction, organized by word count
│   ├── 200-400w/            # 10 prompts — simple language
│   ├── 400-700w/            # 10 prompts — descriptive, morals
│   ├── 700-1200w/           # 10 prompts — complex plots
│   ├── 1200-1800w/          # 10 prompts — layered themes
│   └── 1800-2500w/          # 10 prompts — literary fiction
└── encyclopedia/            # Non-fiction, 8 categories × 20 subcategories × 5 angles
    ├── science/
    ├── history/
    ├── geography/
    ├── technology/
    ├── arts/
    ├── nature/
    ├── society/
    └── mathematics/
```

**850 total prompts** (50 stories + 800 encyclopedia articles).

Each leaf directory contains a `prompts.txt` and the generated `.corpus` files. Both are tracked in git (corpus files cost money to generate).

### Prompt format

One prompt per line:

```
filename.corpus The prompt text sent to the LLM
```

## Scripts

### `scaffold.py` — Create / rebuild directory structure

Generates all directories and `prompts.txt` files from the data defined in the script. Safe to re-run — overwrites `prompts.txt` files but never touches `.corpus` files.

```bash
python scaffold.py
```

Edit the `STORY_GROUPS` and `ENCYCLOPEDIA` dicts in the script to add or change categories, then re-run.

### `generate.py` — Generate corpus content

Walks every `prompts.txt`, finds missing `.corpus` files, and generates them via fal.ai.

The script reads `FAL_KEY` from `~/.env`:

```
FAL_KEY=your-fal-api-key
```

```bash
# Generate 10 files (default)
python generate.py

# Generate 50 files
python generate.py -n 50

# Dry-run — list missing files without generating
python generate.py -n 0

# Use a different model (default: qwen/qwen-2.5-72b-instruct)
python generate.py --model google/gemini-2.5-flash
```

| Flag | Default | Description |
|------|---------|-------------|
| `-n` | `10` | Max files to generate per run. `0` = dry-run. |
| `--model` | `qwen/qwen-2.5-72b-instruct` | OpenRouter model ID. |

The script is idempotent — it skips any `.corpus` file that already exists. Run it repeatedly to incrementally fill out the corpus.
