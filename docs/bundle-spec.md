# Bundle Spec

## Current shape

The current starter bundle is JSON with this high-level structure:

```json
{
  "schema_version": 1,
  "kind": "traceproof.bundle",
  "run": {
    "prompt": "",
    "messages": [],
    "model": {},
    "tool_calls": [],
    "retrieval": [],
    "output": {},
    "metadata": {}
  },
  "redaction_report": {
    "count": 0,
    "entries": []
  }
}
```

## Field intent

- `schema_version`: allows future format migration
- `kind`: simple type marker for tools and importers
- `run.prompt`: top-level prompt or instruction string
- `run.messages`: ordered conversation history
- `run.model`: provider/model/settings data needed for debugging context
- `run.tool_calls`: invoked tools, arguments, and results
- `run.retrieval`: retrieved documents or snippets that shaped the answer
- `run.output`: model output captured at failure time
- `run.metadata`: request identifiers and non-core execution metadata
- `redaction_report`: list of changed paths and why they were modified

## Constraints for next iteration

- keep the bundle human-readable JSON for now
- avoid provider-specific keys at the root level
- preserve unknown nested payloads rather than over-normalizing them away
- treat redaction metadata as first-class so users can trust bundle sharing

## Likely future additions

- `environment`: runtime, SDK, and git context
- `attachments`: larger payload references
- `checks`: validation warnings for incomplete captures
- `replay`: optional deterministic replay inputs and fixture references
