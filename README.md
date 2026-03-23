# traceproof

Capture, replay, and share AI failures like real software bugs.

`traceproof` turns one failed LLM interaction into a portable repro bundle with
redacted secrets and a deterministic diff-friendly replay flow.

## Who this is for

`traceproof` is for teams shipping LLM-backed products that keep hitting bugs
they cannot reproduce cleanly:

- agent builders
- AI product engineers
- platform teams supporting prompt, tool, and retrieval stacks
- anyone tired of debugging from screenshots and partial logs

## Why this exists

AI bugs are hard to replay. The prompt changed, a tool returned something
different, retrieval drifted, and the original output is gone. `traceproof`
freezes the context into a bundle you can inspect, diff, and share.

The long-term goal is not generic observability. The wedge is reproducibility:
take one broken run and turn it into an artifact another engineer can actually
use.

## 3-minute quickstart

```bash
python3 -m traceproof.cli capture examples/failed_run.json --output build/failed_run.tpbundle.json
python3 -m traceproof.cli replay build/failed_run.tpbundle.json --candidate examples/fixed_run.json
```

## Current prototype status

Today this repo proves three core ideas:

- a run can be normalized into a stable bundle shape
- obviously sensitive values can be redacted automatically
- the original run can be diffed against a candidate rerun

That is enough to validate the product shape without committing to provider
integrations or a UI too early.

## Commands

- `capture <input> --output <bundle>`: normalize and redact an AI run into a
  shareable bundle
- `replay <bundle> [--candidate <run>]`: inspect a bundle and diff it against a
  second run

## Bundle format

The current bundle shape is JSON and includes:

- prompt and messages
- model settings
- tool calls and results
- retrieved context
- output
- metadata
- redaction report

See `docs/bundle-spec.md` for the current schema and future extensions.

## Project shape

- `src/traceproof/cli.py`: current CLI, redaction logic, bundle normalization,
  and diff output
- `sdk/python.py`: tiny helper for constructing run payloads in Python
- `sdk/typescript/index.ts`: tiny helper for constructing run payloads in
  TypeScript
- `examples/`: one failing run and one fixed comparison run
- `tests/test_cli.py`: end-to-end smoke coverage for capture and replay

## Limitations

- local JSON input only in this starter version
- no provider-specific integrations yet
- redaction is pattern-based and intentionally conservative

## If you continue this project

Start with `docs/next-phase.md`. It defines the next implementation slice:

- split the CLI into reusable modules
- add a real bundle schema contract
- support provider adapters through import wrappers
- improve diff rendering and redaction coverage

`docs/agent-handoff.md` is written so another agent can pick up the repo and
continue without re-planning from scratch.
