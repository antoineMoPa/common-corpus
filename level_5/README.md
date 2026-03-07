# Level 5 — Structured Output Corpus

Previous levels train free-form text generation (simple sentences → prose → encyclopedia articles).
Level 5 trains **structured output**: given a natural-language input, emit valid JSON matching a schema.

## Categories

- **`tool_use/`** — natural language → JSON function call + response (~28 domains, ~200 files)
- **`json_qa/`** — context sentence → JSON answer extraction (single-field and multi-field)

## Example formats

**tool_use**
```
Available Tools: get_temperature | get_humidity | ...
Call Schema: { "func_call": "string", "location": "string", "unit": "celsius|fahrenheit" }
Response Schema: { "value": number, "unit": "string", "timestamp": "string" }
---
Question: What is the temperature in Paris right now?
Call: { "func_call": "get_temperature", "location": "Paris", "unit": "celsius" }
Response: { "value": 18, "unit": "celsius", "timestamp": "2024-03-15T14:32:00Z" }
```

**json_qa**
```
Context: The truck arrived at the warehouse at 6:45 AM on Tuesday.
Input: {"question": "When did the truck arrive?"}
Output: {"answer": "6:45 AM on Tuesday"}
```

## Usage

```bash
python scaffold.py          # create dirs + prompts.txt files (safe to re-run)
python generate.py -n 0     # dry-run: list missing files
python generate.py -n 50 -p 8   # generate 50 files, 8 in parallel
```

Requires `FAL_KEY=...` in `~/.env`.
