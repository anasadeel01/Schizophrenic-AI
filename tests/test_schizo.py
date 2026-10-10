import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import schizo  # noqa: E402
from personas import PERSONAS  # noqa: E402


def fake_client(reply="hello"):
    c = MagicMock()
    c.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=reply))],
        usage=SimpleNamespace(prompt_tokens=10, completion_tokens=5))
    return c


def test_coin_is_roughly_fair():
    c = Counter(schizo.flip_coin() for _ in range(2000))
    assert set(c) == set(PERSONAS)
    assert 800 < c["utopian_optimist"] < 1200


def test_system_prompt_matches_persona_and_is_not_leaked():
    client = fake_client("The future is bright!")
    with patch("schizo.llm.get_client", return_value=client), patch("schizo.llm.model_name", return_value="m"):
        for persona in PERSONAS:
            text, meta = schizo.answer("hi", persona=persona)
            sent = client.chat.completions.create.call_args.kwargs["messages"]
            assert sent[0]["content"] == PERSONAS[persona]
            assert meta["persona"] == persona and text == "The future is bright!"


def test_at_least_20_prompts():
    lines = [l for l in Path("prompts.txt").read_text().splitlines() if l.strip()]
    assert len(lines) >= 20 and len(set(lines)) == len(lines)
