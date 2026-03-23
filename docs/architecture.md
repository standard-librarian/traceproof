# Architecture

## Current architecture

The prototype is intentionally compact and keeps most behavior inside the CLI:

- JSON loader/writer
- normalization
- redaction
- diff generation
- command dispatch

That made iteration fast, but the next phase should separate concerns so SDK
imports and richer output formats do not bloat one file.

## Recommended module split

- `traceproof/cli.py`: thin command parsing only
- `traceproof/bundle.py`: normalization and schema helpers
- `traceproof/redaction.py`: sensitive key/value rules and reporting
- `traceproof/diffing.py`: comparison and output formatting
- `traceproof/io.py`: loading/writing bundles and runs

## Design principles

- keep bundle creation deterministic
- make redaction safe by default, even if imperfect
- prefer portable JSON over clever serialization
- preserve debugging context before adding abstractions

## Important implementation notes

- normalization should never silently drop useful debugging context beyond the
  intentionally supported top-level shape
- diff output should stay readable in plain terminals
- SDK wrappers should be thin capture helpers, not full frameworks
