from __future__ import annotations

import argparse
import json
import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


SENSITIVE_KEY_RE = re.compile(r"(api[_-]?key|token|secret|password)", re.IGNORECASE)
SENSITIVE_VALUE_RE = re.compile(r"(sk-[A-Za-z0-9]+|Bearer\s+[A-Za-z0-9._-]+)")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def redact(value: Any, redactions: list[dict[str, str]], path: str = "$") -> Any:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, item in value.items():
            child_path = f"{path}.{key}"
            if SENSITIVE_KEY_RE.search(key):
                redactions.append({"path": child_path, "reason": "sensitive-key"})
                result[key] = "[REDACTED]"
            else:
                result[key] = redact(item, redactions, child_path)
        return result
    if isinstance(value, list):
        return [redact(item, redactions, f"{path}[{index}]") for index, item in enumerate(value)]
    if isinstance(value, str) and SENSITIVE_VALUE_RE.search(value):
        redactions.append({"path": path, "reason": "sensitive-value"})
        return SENSITIVE_VALUE_RE.sub("[REDACTED]", value)
    return value


def normalize_run(run: dict[str, Any]) -> dict[str, Any]:
    required = {
        "prompt": run.get("prompt", ""),
        "messages": run.get("messages", []),
        "model": run.get("model", {}),
        "tool_calls": run.get("tool_calls", []),
        "retrieval": run.get("retrieval", []),
        "output": run.get("output", {}),
        "metadata": run.get("metadata", {}),
    }
    return required


def capture_command(args: argparse.Namespace) -> int:
    source = load_json(Path(args.input))
    normalized = normalize_run(source)
    redactions: list[dict[str, str]] = []
    bundle = {
        "schema_version": 1,
        "kind": "traceproof.bundle",
        "run": redact(deepcopy(normalized), redactions),
        "redaction_report": {
            "count": len(redactions),
            "entries": redactions,
        },
    }
    write_json(Path(args.output), bundle)
    print(f"bundle written to {args.output}")
    print(f"redactions: {len(redactions)}")
    return 0


def diff_runs(original: dict[str, Any], candidate: dict[str, Any]) -> list[str]:
    lines: list[str] = []

    def compare(left: Any, right: Any, path: str) -> None:
        if type(left) is not type(right):
            lines.append(f"{path}: type {type(left).__name__} -> {type(right).__name__}")
            return
        if isinstance(left, dict):
            keys = sorted(set(left) | set(right))
            for key in keys:
                child = f"{path}.{key}"
                if key not in left:
                    lines.append(f"{child}: added {json.dumps(right[key], sort_keys=True)}")
                elif key not in right:
                    lines.append(f"{child}: removed")
                else:
                    compare(left[key], right[key], child)
            return
        if isinstance(left, list):
            if left != right:
                lines.append(f"{path}: list changed")
            return
        if left != right:
            lines.append(f"{path}: {json.dumps(left)} -> {json.dumps(right)}")

    compare(original, candidate, "$")
    return lines


def replay_command(args: argparse.Namespace) -> int:
    bundle = load_json(Path(args.bundle))
    original_run = bundle["run"]

    print("bundle summary")
    print(f"- schema: {bundle['schema_version']}")
    print(f"- prompt chars: {len(original_run['prompt'])}")
    print(f"- messages: {len(original_run['messages'])}")
    print(f"- tool calls: {len(original_run['tool_calls'])}")
    print(f"- retrieval docs: {len(original_run['retrieval'])}")
    print(f"- redactions: {bundle['redaction_report']['count']}")

    if not args.candidate:
        return 0

    candidate_run = normalize_run(load_json(Path(args.candidate)))
    diff_lines = diff_runs(original_run, candidate_run)
    if not diff_lines:
        print("diff: no changes")
        return 0

    print("diff:")
    for line in diff_lines:
        print(f"- {line}")
    return 0


def parser() -> argparse.ArgumentParser:
    app = argparse.ArgumentParser(prog="traceproof")
    subparsers = app.add_subparsers(dest="command", required=True)

    capture = subparsers.add_parser("capture", help="Create a redacted repro bundle.")
    capture.add_argument("input")
    capture.add_argument("--output", required=True)
    capture.set_defaults(func=capture_command)

    replay = subparsers.add_parser("replay", help="Inspect or diff a bundle.")
    replay.add_argument("bundle")
    replay.add_argument("--candidate")
    replay.set_defaults(func=replay_command)
    return app


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
