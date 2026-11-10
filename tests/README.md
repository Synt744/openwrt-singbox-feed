# Tests

The current unit tests cover the offline registry linter only. They do not perform network access and do not launch sing-box.

Before a router release, add tests for hostile/malformed source input, size and timeout limits, credential redaction, parser fixtures, sing-box config validation, atomic activation, rollback, and supported OpenWrt package targets. Never put real subscription URLs or node credentials in fixtures.
