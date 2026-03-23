# Next Phase

## Goal

Turn the prototype into a small but credible developer tool that can capture
real application runs through lightweight adapters rather than handcrafted JSON.

## Scope for the next implementation phase

### 1. Internal refactor

- split `cli.py` into reusable modules
- keep command behavior unchanged while refactoring
- add unit tests for redaction and diffing independently of subprocess tests

### 2. Stronger bundle contract

- formalize the bundle schema in code
- validate required top-level fields
- preserve extra nested data in `model`, `tool_calls`, `retrieval`, and
  `metadata`
- print clear validation errors for malformed input

### 3. Real capture adapters

- add one Python adapter for wrapping an LLM call path
- add one TypeScript adapter with the same conceptual shape
- adapter output should match the bundle spec without requiring users to
  handcraft JSON

### 4. Better redaction

- support configurable extra sensitive keys
- redact obvious auth headers and provider secrets more reliably
- emit warnings when a run appears incomplete or risky to share

### 5. Better replay output

- group diff lines by section
- highlight output changes separately from metadata changes
- show a short replay summary before the diff

## Acceptance criteria

- a developer can wrap one Python call path and generate a valid bundle
- a developer can wrap one TypeScript call path and generate a valid bundle
- malformed input fails fast with useful error messages
- secret-looking values are redacted in the default example and at least one
  new fixture
- subprocess tests and unit tests both pass locally

## Non-goals

- browser UI
- hosted backend
- provider-specific dashboards
- full deterministic rerun against live providers
