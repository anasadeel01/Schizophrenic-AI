"""Run every prompt in prompts.txt through the Schizophrenic AI and save plain-text outputs.

Usage:  python generate_samples.py          (skips prompts that already have an output file)
Writes: generated_samples/prompt_XX.txt  and  generated_samples/_meta.jsonl
"""
import json
import time
from pathlib import Path

import llm
from schizo import answer

OUT = Path("generated_samples")
OUT.mkdir(exist_ok=True)
META = OUT / "_meta.jsonl"

prompts = [p.strip() for p in Path("prompts.txt").read_text(encoding="utf-8").splitlines() if p.strip()]
assert len(prompts) >= 20, "Task requires at least 20 prompts"

done = set()
if META.exists():
    done = {json.loads(l)["index"] for l in META.read_text().splitlines() if l.strip()}

print(f"Model: {llm.model_name()} | {len(prompts)} prompts | {len(done)} already done")
for i, prompt in enumerate(prompts, 1):
    if i in done:
        continue
    text, meta = answer(prompt)
    (OUT / f"prompt_{i:02d}.txt").write_text(f"PROMPT: {prompt}\n\n{text}\n", encoding="utf-8")
    with META.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"index": i, "prompt": prompt, **meta}) + "\n")
    print(f"[{i:02d}/{len(prompts)}] {prompt[:50]!r} -> {len(text.split())} words")
    time.sleep(15)  # reduce free-tier rate-limit errors

print("Done. Now run: python evaluate.py")
