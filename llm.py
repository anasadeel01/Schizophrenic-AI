"""Tiny provider-agnostic LLM wrapper (OpenAI-compatible API).

Default: Google Gemini through its OpenAI-compatible endpoint.
Swap provider with env vars only - no code changes:
  LLM_API_KEY   (fallbacks: GEMINI_API_KEY, OPENAI_API_KEY)
  LLM_BASE_URL  default https://generativelanguage.googleapis.com/v1beta/openai/
  LLM_MODEL     default gemini-3-flash-preview
"""
import os

DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
DEFAULT_MODEL = "gemini-3-flash-preview"


def _secret(name: str):
    val = os.getenv(name)
    if val:
        return val
    try:  # Streamlit Cloud secrets (only if streamlit is installed / running)
        import streamlit as st
        return st.secrets.get(name)
    except Exception:
        return None


def settings() -> dict:
    return {
        "api_key": _secret("LLM_API_KEY") or _secret("GEMINI_API_KEY") or _secret("OPENAI_API_KEY"),
        "base_url": _secret("LLM_BASE_URL") or DEFAULT_BASE_URL,
        "model": _secret("LLM_MODEL") or DEFAULT_MODEL,
    }


def get_client():
    from openai import OpenAI
    s = settings()
    if not s["api_key"]:
        raise RuntimeError("No API key found. Set LLM_API_KEY (see README.md).")
    return OpenAI(api_key=s["api_key"], base_url=s["base_url"])


def model_name() -> str:
    return settings()["model"]
