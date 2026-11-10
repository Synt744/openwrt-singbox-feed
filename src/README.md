# Runtime module contract

The runtime is not implemented yet. Planned boundaries:

- registry: validate local UCI/source metadata and redact secrets in diagnostics
- fetch: HTTPS-only, bounded time/size, explicit redirect handling, stage-only writes
- parse: strict supported formats; data is never executed
- normalize: stable IDs, deduplication, source/revision provenance
- validate: generated sing-box config checked with the installed binary
- activate: separate operator action, atomic file replacement, backup and rollback

The router implementation should avoid a Python runtime dependency. The current Python script under scripts/ is only an offline development-time registry linter.
