#!/usr/bin/env python3
"""Robust Ollama LLM client (shared pattern).

See saas-alternatives-directory version for full comments."""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "gemma2:2b")


def generate(prompt: str, system: str | None = None, temperature: float = 0.7) -> str:
    url = f"{BASE_URL}/api/generate"
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature}
    }
    if system:
        payload["system"] = system
    try:
        response = requests.post(url, json=payload, timeout=180)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"[LLM Error] {e}")
        return "[LLM generation failed - check Ollama]"


def is_ollama_available() -> bool:
    try:
        return requests.get(f"{BASE_URL}/api/tags", timeout=5).status_code == 200
    except:
        return False
