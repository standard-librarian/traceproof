# traceproof

Capture, replay, and share AI failures like real software bugs.

`traceproof` turns one failed LLM interaction into a portable repro bundle with
redacted secrets and a deterministic diff-friendly replay flow.

## Why this exists

AI bugs are hard to replay. The prompt changed, a tool returned something
different, retrieval drifted, and the original output is gone. `traceproof`
freezes the context into a bundle you can inspect, diff, and share.

## 3-minute quickstart

```bash
python3 -m traceproof.cli capture examples/failed_run.json --output build/failed_run.tpbundle.json
python3 -m traceproof.cli replay build/failed_run.tpbundle.json --candidate examples/fixed_run.json
```

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

## Limitations

- local JSON input only in this starter version
- no provider-specific integrations yet
- redaction is pattern-based and intentionally conservative
