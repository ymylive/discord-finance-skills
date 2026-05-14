#!/usr/bin/env python3
"""Dump Discord API message payloads from the local desktop cache."""

from __future__ import annotations

import argparse
import json
import re
import zlib
from pathlib import Path
from typing import Any


NEEDLE = b"https://discord.com/api/v9/channels/"


def default_cache_dir() -> Path:
    return Path.home() / "Library/Application Support/discord/Cache/Cache_Data"


def text_for_message(message: dict[str, Any]) -> str:
    parts: list[str] = []
    if message.get("content"):
        parts.append(message["content"])
    for embed in message.get("embeds") or []:
        for key in ("title", "description"):
            if embed.get(key):
                parts.append(embed[key])
        for field in embed.get("fields") or []:
            name = field.get("name", "")
            value = field.get("value", "")
            if name or value:
                parts.append(f"{name}: {value}".strip())
        footer = embed.get("footer") or {}
        if footer.get("text"):
            parts.append(footer["text"])
    return "\n".join(parts)


def iter_payloads(cache_dir: Path, channel_ids: set[str] | None):
    for path in cache_dir.iterdir():
        if not path.is_file():
            continue
        try:
            blob = path.read_bytes()
        except OSError:
            continue
        start = 0
        while True:
            index = blob.find(NEEDLE, start)
            if index < 0:
                break
            start = index + 1
            gzip_pos = blob.find(b"\x1f\x8b", index)
            if gzip_pos < 0:
                continue
            url = blob[index:gzip_pos].decode("utf-8", "ignore")
            match = re.search(r"/channels/(\d+)/messages", url)
            if not match:
                continue
            channel_id = match.group(1)
            if channel_ids and channel_id not in channel_ids:
                continue
            try:
                decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)
                payload = json.loads(decompressor.decompress(blob[gzip_pos:]))
            except Exception:
                continue
            if isinstance(payload, list):
                yield channel_id, url, payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, default=default_cache_dir())
    parser.add_argument("--channel", action="append", dest="channels", help="Discord channel/thread id. Repeatable.")
    parser.add_argument("--contains", action="append", default=[], help="Keep messages whose text contains this string.")
    parser.add_argument("--out", type=Path, help="Write JSON to this path instead of stdout.")
    args = parser.parse_args()

    channel_ids = set(args.channels or []) or None
    result: dict[str, dict[str, Any]] = {}
    needles = args.contains

    for channel_id, url, payload in iter_payloads(args.cache_dir, channel_ids):
        channel = result.setdefault(channel_id, {"urls": [], "messages": {}})
        channel["urls"].append(url)
        for message in payload:
            if not isinstance(message, dict) or not message.get("id"):
                continue
            text = text_for_message(message)
            if needles and not any(needle in text for needle in needles):
                continue
            message = dict(message)
            message["_text"] = text
            channel["messages"][message["id"]] = message

    for channel in result.values():
        channel["urls"] = sorted(set(channel["urls"]))
        channel["messages"] = sorted(channel["messages"].values(), key=lambda item: item.get("timestamp", ""))

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
