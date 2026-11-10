# OpenWrt integration plan

This directory is a design stub, not an installable package. No init script, UCI service, LuCI page, or active sing-box config writer has been added.

## Intended deployment shape

- OpenWrt package/feed with a small runtime that uses the system sing-box binary.
- UCI-managed source IDs and refresh policy; subscription URLs stay on the router and are never committed.
- procd-managed service or scheduled job only after the CLI behavior is tested.
- Candidate output stored separately from the active profile. Validate first, show a diff, then require explicit activation and preserve rollback state.
- LuCI is a later optional front end; the first usable release should work over SSH and be recoverable locally.

## Compatibility

OpenWrt versions, CPU architectures, package dependencies, and flash/RAM requirements have not yet been tested. Do not install this scaffold on a router. Record real device and release checks before declaring support.
