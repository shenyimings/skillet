"""LLM transport. A protocol plus a DeepSeek implementation.

The labeller depends on the `Completion` protocol, not on any provider, so tests inject a
scripted client and never touch the network, and swapping providers is a constructor
argument. The DeepSeek client speaks the OpenAI-compatible chat API and asks for a JSON
object response; configuration comes from the environment (see .env.example), never from
literals in code.
"""

from __future__ import annotations

import json
import os
from typing import Protocol, runtime_checkable


@runtime_checkable
class Completion(Protocol):
    """Anything that can turn a (system, user) pair into a JSON object."""

    def complete_json(self, system: str, user: str) -> dict: ...


class DeepSeekClient:
    """OpenAI-compatible chat client for DeepSeek, returning parsed JSON objects."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float = 60.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("SKILLET_LLM_API_KEY", "")
        self.base_url = (
            base_url or os.environ.get("SKILLET_LLM_BASE_URL", "https://api.deepseek.com")
        ).rstrip("/")
        self.model = model or os.environ.get("SKILLET_LLM_MODEL", "deepseek-v4-flash")
        self.timeout = timeout
        if not self.api_key:
            raise RuntimeError("no SKILLET_LLM_API_KEY set; the semantic tier needs a key")

    def complete_json(self, system: str, user: str) -> dict:
        import httpx

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.0,
            "stream": False,
        }
        resp = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        try:
            parsed = json.loads(content)
        except (json.JSONDecodeError, TypeError):
            return {}
        return parsed if isinstance(parsed, dict) else {}


class ScriptedClient:
    """A deterministic Completion for tests: maps user-text substrings to canned JSON."""

    def __init__(self, responses: dict[str, dict], default: dict | None = None) -> None:
        self._responses = responses
        self._default = default or {"labels": []}
        self.calls: list[tuple[str, str]] = []

    def complete_json(self, system: str, user: str) -> dict:
        self.calls.append((system, user))
        for needle, response in self._responses.items():
            if needle in user:
                return response
        return self._default
