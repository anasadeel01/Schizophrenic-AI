"""The "Schizophrenic" AI - a backend coin flip decides which personality answers.

The persona is NEVER shown to the end user. It is returned to the caller only so that
the evaluation script can log it (generated_samples/_meta.jsonl).
"""
import argparse
import secrets
import time

import llm
from personas import PERSONAS


def flip_coin() -> str:
    """Cryptographically fair coin flip on the backend."""
    return "utopian_optimist" if secrets.randbelow(2) == 0 else "doomsday_prepper"


def answer(prompt: str, persona: str | None = None, retries: int = 3):
    """Return (text, meta). `persona` can be forced for tests; normally it is None -> coin flip."""
    persona = persona or flip_coin()
    client = llm.get_client()
    last_err = None
    for attempt in range(retries):
        try:
            t0 = time.time()
            resp = client.chat.completions.create(
                model=llm.model_name(),
                messages=[
                    {"role": "system", "content": PERSONAS[persona]},
                    {"role": "user", "content": prompt},
                ],
                temperature=1.0,
            )
            text = (resp.choices[0].message.content or "").strip()
            usage = getattr(resp, "usage", None)
            meta = {
                "persona": persona,
                "model": llm.model_name(),
                "latency_s": round(time.time() - t0, 2),
                "prompt_tokens": getattr(usage, "prompt_tokens", None),
                "completion_tokens": getattr(usage, "completion_tokens", None),
            }
            return text, meta
        except Exception as e:  # rate limit / transient errors
            last_err = e
            time.sleep(2 ** attempt * 2)
    raise RuntimeError(f"LLM call failed after {retries} attempts: {last_err}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--debug", action="store_true", help="reveal which persona answered")
    a = ap.parse_args()
    text, meta = answer(a.prompt)
    print(text)
    if a.debug:
        print(f"\n[debug] persona={meta['persona']} model={meta['model']}")
