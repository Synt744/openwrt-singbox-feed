# Architecture and first release boundary

## Current code

Only the registry metadata linter is implemented. It runs offline on a development machine and has no router permissions. The package, fetcher, parsers, tests against a real sing-box binary, and UI are future work.

## Intended data flow

Operator-managed source registry -> bounded fetch to a temporary staging file -> format parser -> normalized candidate set plus provenance -> structural and sing-box validation -> human review -> atomic activation with backup -> explicit rollback path.

Each candidate should retain a source ID, an immutable Git revision when the source is a GitHub raw file, a content digest, fetch time, and parse result. Logs and reports must redact subscription URLs because provider links can contain bearer-like credentials.

## Source kinds

- github-raw: HTTPS raw file pinned to a full commit SHA. Do not use a moving branch such as main for a production source.
- subscription: HTTPS endpoint chosen by the operator. The endpoint may be mutable and may contain a secret token; store it only in local router configuration or a secret store, never in this public repository.

All sources are treated as untrusted input, even if hosted on GitHub. A repository or subscription contributes data only; it must never contribute shell scripts, package hooks, or executable code.

## Failure behavior

- A timeout, HTTP error, oversized response, parse error, invalid config, or failed sing-box check rejects that candidate.
- A failed refresh does not replace the last known-good active config.
- Activation is a separate action from refresh. The first release should default to review-required; scheduled refresh may prepare a candidate but must not silently route traffic through it.
- Apply by writing a temporary file on the same filesystem, validating it, preserving a backup, then renaming atomically. Keep a recovery command that restores the last known-good file.

## OpenWrt integration direction

The eventual router package should use UCI for explicit source settings, procd for lifecycle management, and the system's installed sing-box executable for validation. A LuCI screen is optional and comes after the CLI/service behavior is testable. Do not edit the active sing-box configuration until the operator chooses a validated candidate.
