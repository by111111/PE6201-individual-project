"""OpenRouter adapter and defensive JSON parser.

The adapter isolates the only external network dependency, records basic
operational metadata, and translates transport/provider failures into a single
application exception. No API key is stored in code or output artifacts.
"""

from __future__ import annotations

import json
import os
import re
import time
from urllib import error, request

class ProviderError(Exception):
    """Raised when provider communication or model-output parsing fails."""

    pass

class OpenRouterProvider:
    """Minimal chat-completions client configured through environment values."""

    def __init__(self, model: str | None = None):
        """Load the model and API key while initialising telemetry fields."""
        self.model = model or os.getenv("OPENROUTER_MODEL", "openai/gpt-4.1-mini")
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.last_cost_usd = None
        self.last_usage = {}
        self.last_latency_seconds = None
        if not self.api_key:
            raise ProviderError("OPENROUTER_API_KEY is missing")

    def generate(self, messages: list[dict], *, json_mode: bool = True) -> str:
        """Send messages to OpenRouter and return text from the first choice."""
        payload = {"model": self.model, "messages": messages, "temperature": 0.2}
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        started = time.perf_counter()
        req = request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=60) as response:
                body = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:250]
            raise ProviderError(f"HTTP {exc.code}: {detail}") from exc
        except (error.URLError, TimeoutError) as exc:
            raise ProviderError(f"Network error: {exc}") from exc
        finally:
            self.last_latency_seconds = round(time.perf_counter() - started, 3)
        usage = body.get("usage", {})
        self.last_usage = usage
        self.last_cost_usd = usage.get("cost")
        try:
            return body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError("No model content returned") from exc

def parse_plan(raw: str) -> dict:
    """Parse a model response as a JSON object or raise ``ProviderError``."""
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ProviderError("Model did not return valid JSON") from exc
    if not isinstance(result, dict):
        raise ProviderError("Model JSON must be an object")
    return result
