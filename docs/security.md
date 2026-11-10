# Threat model and safety defaults

## Assets

- Router administration and LAN availability
- VPN provider credentials embedded in subscription URLs
- Active sing-box configuration and the operator's routing decisions
- Device traffic metadata visible to the selected VPN endpoint

## Threats

- A public repository changes a source file or is compromised.
- A subscription response contains malformed, huge, or intentionally confusing data.
- A token in a URL leaks through logs, screenshots, shell history, or a public commit.
- A bad update breaks connectivity or silently changes which proxy sees traffic.
- A downloaded file is mistaken for executable software.

## Required defaults

- No live node lists or credentials committed to this repository.
- Example sources are disabled and use a non-working placeholder URL.
- HTTPS only; enforce request timeout, maximum response size, and a redirect policy before implementing fetch.
- Never log full source URLs; redact query strings and sensitive path segments.
- Never execute fetched data. Parse only explicitly supported formats.
- Treat node settings as untrusted until reviewed; validate generated JSON with sing-box before activation.
- Refresh and activate are separate operations. Keep the last known-good config and provide rollback.
- Pin GitHub raw sources to a commit SHA. Pinning proves which bytes were fetched, not that those bytes are trustworthy.
- Publish source metadata and a content digest, not source contents that may contain credentials.

## Not a security guarantee

A successful parse or sing-box config check does not establish that a VPN endpoint is safe, private, lawful, or available. The operator chooses and trusts the endpoints. Use only sources you are authorized to use and understand that a VPN endpoint can observe traffic.
