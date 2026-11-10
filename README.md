# OpenWrt sing-box Feed Manager

Companion project for OpenWrt routers running sing-box. It is intended to manage user-selected VPN subscription/source feeds safely; it is not a VPN provider and will not publish a list of live public nodes.

## Why this project

The sing-box core already supports many proxy protocols, and OpenWrt projects provide routing and LuCI management. This project focuses on the gap between a source URL and a router configuration: source provenance, bounded fetching, parsing, validation, review, and safe activation/rollback. It complements rather than replaces HomeProxy-style subscription import.

## Status

**Scaffold only. Not installable and not ready to change router traffic.** The first milestone is an offline source-registry validator. No fetcher, LuCI page, procd service, node testing, or sing-box config writer is implemented yet.

## Planned MVP

1. Add sources explicitly: a pinned GitHub raw file or a subscription URL controlled by the operator.
2. Fetch into a staging area with HTTPS-only transport, time/size limits, redirect policy, and redacted logs.
3. Parse a small, documented set of formats; never execute downloaded content.
4. Normalize and deduplicate candidates, preserve source and revision metadata, then validate the generated config with the installed sing-box binary.
5. Show the candidate diff and require explicit activation. Apply atomically, keep a backup, and support rollback.
6. Keep automatic refresh separate from automatic activation; failed refreshes must leave the active configuration untouched.

A public-source catalog, if added later, will be opt-in and reviewed. No untrusted node is enabled by default. Public VPN endpoints can observe traffic and disappear without notice; use only sources you are entitled to use and trust.

## Repository map

- config/ — disabled example registry and JSON Schema
- scripts/ — offline registry linter; it never fetches source URLs
- src/ — runtime implementation contract and planned module boundaries
- openwrt/ — target integration plan; no package is built yet
- docs/ — architecture and threat model
- tests/ — standard-library unit tests for the linter

## Validate the example

Run from the repository root:

    python3 scripts/validate_registry.py config/sources.example.json
    python3 -m unittest discover -s tests -v

The validator checks metadata only. It does not resolve hosts, download subscriptions, test VPN nodes, or write a sing-box configuration.

## Research references

- [SagerNet/sing-box](https://github.com/SagerNet/sing-box) — upstream proxy engine.
- [nikkinikki-org/OpenWrt-momo](https://github.com/nikkinikki-org/OpenWrt-momo) — OpenWrt transparent-proxy implementation to study for router integration.
- [Synt744/homeproxy-hiddify](https://github.com/Synt744/homeproxy-hiddify) — existing subscription-import work; this project is deliberately scoped to source lifecycle and safe activation.

License: not selected yet. Choose one before accepting external contributions or distributing releases.
