from __future__ import annotations

from typing import Any


def build_run(
    *,
    prompt: str,
    messages: list[dict[str, Any]],
    model: dict[str, Any],
    output: dict[str, Any],
    tool_calls: list[dict[str, Any]] | None = None,
    retrieval: list[dict[str, Any]] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "prompt": prompt,
        "messages": messages,
        "model": model,
        "tool_calls": tool_calls or [],
        "retrieval": retrieval or [],
        "output": output,
        "metadata": metadata or {},
    }
