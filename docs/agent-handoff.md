# Agent Handoff

## Mission

Continue `traceproof` as a focused open-source reliability tool for AI products.
Do not broaden it into a generic framework.

## What already exists

- CLI command to normalize and redact a captured run
- CLI command to inspect a bundle and diff it against a candidate run
- starter SDK helpers in Python and TypeScript
- example failing and fixed runs
- end-to-end smoke coverage

## What matters most next

- refactor the CLI into modules without changing the user-facing commands
- make the bundle schema explicit and validated
- add one real capture path in Python and one in TypeScript
- improve redaction and diff readability

## Constraints

- keep the tool CLI-first
- keep the bundle JSON and human-readable
- avoid integrating many providers at once
- do not add hosted components
- optimize for a clean 5-minute first success

## Suggested work order

1. Refactor internals into `bundle`, `redaction`, `diffing`, and `io` modules.
2. Add schema validation and targeted unit tests.
3. Implement minimal Python and TypeScript capture adapters.
4. Improve replay output formatting and docs.
5. Refresh README examples to reflect the new adapter-based flow.

## Done means

- existing quickstart still works or is replaced with a clearly better one
- tests cover the new modules
- documentation explains the new adapter flow without requiring code reading
