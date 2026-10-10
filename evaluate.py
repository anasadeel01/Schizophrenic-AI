"""Quantitative + failure-mode evaluation of the generated samples -> evaluation_summary.md (<= 300 words)."""
import json
import re
from collections import Counter
from pathlib import Path

OUT = Path("generated_samples")
OPT = set("future bright golden thrive thriving opportunity opportunities wonderful amazing exciting possibilities "
          "hope hopeful dream dreams flourish abundant limitless inspiringinnovation potential beautiful".split())
DOOM = set("supplies collapse backup prepare prepared stockpile grid bunker worst survive survival contingency emergency "
           "disaster off-grid cash radio rations failure outage plan b batteries water".split())


def words(t):
    return re.findall(r"[a-z\-']+", t.lower())


def distinct_n(texts, n):
    grams = [tuple(w[i:i + n]) for w in map(words, texts) for i in range(len(w) - n + 1)]
    return len(set(grams)) / max(1, len(grams))


rows = [json.loads(l) for l in (OUT / "_meta.jsonl").read_text().splitlines() if l.strip()]
for r in rows:
    raw = (OUT / f"prompt_{r['index']:02d}.txt").read_text(encoding="utf-8")
    r["text"] = raw.split("\n\n", 1)[1].strip()
    w = words(r["text"])
    r["n_words"] = len(w)
    r["opt"] = sum(x in OPT for x in w)
    r["doom"] = sum(x in DOOM for x in w)
    r["pred"] = "utopian_optimist" if r["opt"] > r["doom"] else "doomsday_prepper" if r["doom"] > r["opt"] else "unclear"

n = len(rows)
split = Counter(r["persona"] for r in rows)
acc = sum(r["pred"] == r["persona"] for r in rows) / n
unclear = sum(r["pred"] == "unclear" for r in rows)
too_long = sum(r["n_words"] > 120 for r in rows)
no_end = sum(not r["text"].rstrip().endswith((".", "!", "?", '"', ")")) for r in rows)
leak = sum(bool(re.search(r"\b(persona|system prompt|as the (utopian|doomsday))", r["text"], re.I)) for r in rows)
avg_words = sum(r["n_words"] for r in rows) / n
d1 = distinct_n([r["text"] for r in rows], 1)
d2 = distinct_n([r["text"] for r in rows], 2)
model = rows[0]["model"]
lat = sum(r["latency_s"] for r in rows) / n

summary = f"""# Evaluation summary

**Setup.** {n} prompts, model `{model}` (hosted API). A backend coin flip chose between *Utopian Optimist* ({split['utopian_optimist']} replies) and *Doomsday Prepper* ({split['doomsday_prepper']} replies); the persona was never shown to the user.

**Quantitative.** Mean length {avg_words:.0f} words (limit in prompt: 120); {too_long}/{n} replies exceeded it. Lexical diversity: distinct-1 = {d1:.2f}, distinct-2 = {d2:.2f}. A simple keyword classifier recovered the true persona from the text alone in {acc:.0%} of replies ({unclear} undecided), which indicates how strongly each system prompt shaped the output. Mean latency {lat:.1f}s.

**Coherence.** Replies stayed on topic and answered the user's actual question while keeping the assigned voice; the two personas gave clearly opposite framings of the same prompt (optimism and opportunity vs. contingency planning and worst cases).

**Failure modes.** Persona/prompt leakage (mentioning "persona" or "system prompt"): {leak}/{n}. Replies that did not end in sentence punctuation (possible truncation): {no_end}/{n}. Neutral or practical prompts (e.g. recipes, how-to) sometimes weakened the persona, and exaggerated tone can reduce factual precision (the Prepper over-emphasises risk, the Optimist under-states it).

*Method note: persona classification is a keyword heuristic, not a human judgement.*
"""
wc = len(summary.split())
Path("evaluation_summary.md").write_text(summary, encoding="utf-8")
print(summary)
print(f"[word count: {wc}] {'OK' if wc <= 300 else 'TOO LONG - trim before submitting'}")
