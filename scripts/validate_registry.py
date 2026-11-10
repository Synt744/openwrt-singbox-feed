#!/usr/bin/env python3
"""Offline metadata checks for the source registry. Never makes network requests."""

import argparse
import ipaddress
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
SHA_RE = re.compile(r"^[a-fA-F0-9]{40}$")
KINDS = {"github-raw", "subscription"}
FORMATS = {"sing-box-json", "share-links"}
SOURCE_KEYS = {"id", "kind", "url", "revision", "format", "enabled", "trust", "maxBytes"}


def validate_registry(data):
    if not isinstance(data, dict):
        raise ValueError("registry: expected an object")
    if set(data) - {"$schema", "schemaVersion", "sources"}:
        raise ValueError("registry: contains unsupported fields")
    version = data.get("schemaVersion")
    if type(version) is not int or version != 1:
        raise ValueError("registry: schemaVersion must be 1")
    sources = data.get("sources")
    if not isinstance(sources, list) or len(sources) > 20:
        raise ValueError("sources: expected an array with at most 20 entries")

    seen = set()
    for index, source in enumerate(sources):
        where = f"sources[{index}]"
        if not isinstance(source, dict):
            raise ValueError(f"{where}: expected an object")
        if set(source) - SOURCE_KEYS:
            raise ValueError(f"{where}: contains unsupported fields")
        required = SOURCE_KEYS - {"revision"}
        if required - set(source):
            raise ValueError(f"{where}: missing required fields")

        source_id = source["id"]
        if not isinstance(source_id, str) or not ID_RE.fullmatch(source_id):
            raise ValueError(f"{where}.id: invalid identifier")
        if source_id in seen:
            raise ValueError(f"{where}.id: duplicate identifier")
        seen.add(source_id)

        kind = source["kind"]
        if not isinstance(kind, str) or kind not in KINDS:
            raise ValueError(f"{where}.kind: unsupported source kind")
        fmt = source["format"]
        if not isinstance(fmt, str) or fmt not in FORMATS:
            raise ValueError(f"{where}.format: unsupported format")
        if kind == "github-raw" and fmt != "sing-box-json":
            raise ValueError(f"{where}.format: github-raw currently requires sing-box-json")
        if not isinstance(source["enabled"], bool):
            raise ValueError(f"{where}.enabled: expected a boolean")
        if source["trust"] != "untrusted":
            raise ValueError(f"{where}.trust: must be untrusted")
        size = source["maxBytes"]
        if isinstance(size, bool) or not isinstance(size, int) or not 1024 <= size <= 1048576:
            raise ValueError(f"{where}.maxBytes: expected an integer from 1024 to 1048576")

        url = source["url"]
        if not isinstance(url, str):
            raise ValueError(f"{where}.url: expected an HTTPS URL")
        parsed = None
        try:
            parsed = urlsplit(url)
            host = parsed.hostname
        except ValueError:
            host = None
        if parsed is None or parsed.scheme != "https" or not host or parsed.username or parsed.password or parsed.fragment:
            raise ValueError(f"{where}.url: must be HTTPS without embedded credentials or fragment")
        host = host.lower()
        if host == "localhost" or host.endswith((".localhost", ".local")) or "." not in host:
            raise ValueError(f"{where}.url: local or single-label hosts are not allowed")
        try:
            address = ipaddress.ip_address(host)
        except ValueError:
            address = None
        if address is not None and not address.is_global:
            raise ValueError(f"{where}.url: non-public IP addresses are not allowed")

        if kind == "github-raw":
            if host != "raw.githubusercontent.com":
                raise ValueError(f"{where}.url: github-raw must use raw.githubusercontent.com")
            revision = source.get("revision")
            if not isinstance(revision, str) or not SHA_RE.fullmatch(revision):
                raise ValueError(f"{where}.revision: expected a full 40-character commit SHA")
            if revision.lower() not in parsed.path.lower().split("/"):
                raise ValueError(f"{where}.revision: URL path must contain the pinned commit SHA")
        elif "revision" in source:
            raise ValueError(f"{where}.revision: only github-raw supports a pinned revision")


def main():
    parser = argparse.ArgumentParser(description="Validate source-registry metadata without network access")
    parser.add_argument("registry", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.registry.read_text(encoding="utf-8"))
        validate_registry(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Invalid registry: {exc}", file=sys.stderr)
        return 1
    print(f"OK: {len(data['sources'])} source definition(s); no source content fetched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
