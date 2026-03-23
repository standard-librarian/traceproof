# Traceproof Overview

## Product thesis

Modern AI teams can observe failures, but they still struggle to reproduce
them. `traceproof` is a reproducibility tool first.

The core job to be done is:

> Turn one confusing AI failure into a stable bundle another engineer can
> replay, inspect, and fix.

That framing matters. If the project drifts into generic tracing,
observability, or evaluation infrastructure too early, the value proposition
gets weaker and the first-run story gets slower.

## Target user

Primary user:

- engineer responsible for shipping or debugging an LLM-based product

Typical failure cases:

- the model output changed and nobody knows why
- a tool call behaved unexpectedly
- retrieved context drifted
- a secret leaked into logs or repro notes
- an issue gets handed to another engineer with incomplete context

## Current prototype

The current prototype is intentionally narrow:

- input is local JSON
- output is a redacted JSON bundle
- replay is currently an inspection and diff flow, not a live model rerun

This is enough to validate the artifact model before integrating real SDKs or
providers.

## Product boundaries

In scope for the near term:

- bundle generation
- redaction
- run comparison
- transportable debugging artifacts
- import wrappers for common provider calls

Out of scope for the near term:

- hosted observability
- prompt IDE features
- benchmarking platforms
- broad agent orchestration
- large plugin ecosystems
