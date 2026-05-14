#!/usr/bin/env python3
"""Download and convert Discord finance report PDFs from a cache dump."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPORT_RE = re.compile(r"aio-report:v1:us:([A-Z0-9.\-]+):(research|timing):(\d{4}-\d{2}-\d{2})")
TITLE_RE = re.compile(r"\(([A-Z][A-Z0-9.\-]{0,8})\).*?(深度研究|择时分析)")
DATE_RE = re.compile(r"美股(?:深度研究|择时分析)\s*[· ]+(\d{4}-\d{2}-\d{2})")
VERDICT_RE = re.compile(r"判定[:：]\s*[^A-Z]*(BUY|HOLD|PASS|SELL|ENTER_NOW|WAIT_PULLBACK|WAIT_BREAKOUT|NOT_YET)")


@dataclass
class ReportMessage:
    ticker: str
    kind: str
    date: str
    verdict: str | None
    channel_id: str
    message_id: str
    timestamp: str
    attachment_count: int
    text_head: str
    message: dict[str, Any]


def load_cache(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"cache JSON must be an object: {path}")
    return data


def message_text(message: dict[str, Any]) -> str:
    if isinstance(message.get("_text"), str):
        return message["_text"]
    parts: list[str] = []
    if message.get("content"):
        parts.append(str(message["content"]))
    for embed in message.get("embeds") or []:
        if not isinstance(embed, dict):
            continue
        for key in ("title", "description"):
            if embed.get(key):
                parts.append(str(embed[key]))
        footer = embed.get("footer") or {}
        if isinstance(footer, dict) and footer.get("text"):
            parts.append(str(footer["text"]))
    return "\n".join(parts)


def report_identity(text: str, timestamp: str) -> tuple[str, str, str] | None:
    match = REPORT_RE.search(text)
    if match:
        return match.group(1), match.group(2), match.group(3)

    title = TITLE_RE.search(text)
    if not title:
        return None

    ticker = title.group(1)
    kind = "research" if title.group(2) == "深度研究" else "timing"
    date_match = DATE_RE.search(text)
    date = date_match.group(1) if date_match else timestamp[:10]
    return ticker, kind, date


def iter_reports(cache: dict[str, Any]) -> list[ReportMessage]:
    reports: list[ReportMessage] = []
    for channel_id, channel in cache.items():
        if not isinstance(channel, dict):
            continue
        for message in channel.get("messages") or []:
            if not isinstance(message, dict):
                continue
            text = message_text(message)
            identity = report_identity(text, str(message.get("timestamp", "")))
            if not identity:
                continue
            ticker, kind, date = identity
            verdict_match = VERDICT_RE.search(text)
            attachments = [a for a in message.get("attachments") or [] if isinstance(a, dict)]
            reports.append(
                ReportMessage(
                    ticker=ticker,
                    kind=kind,
                    date=date,
                    verdict=verdict_match.group(1) if verdict_match else None,
                    channel_id=str(channel_id),
                    message_id=str(message.get("id", "")),
                    timestamp=str(message.get("timestamp", "")),
                    attachment_count=len(attachments),
                    text_head=text.splitlines()[0] if text else "",
                    message=message,
                )
            )
    return reports


def latest_reports(reports: list[ReportMessage]) -> list[ReportMessage]:
    latest: dict[tuple[str, str], ReportMessage] = {}
    for report in reports:
        key = (report.ticker, report.kind)
        current = latest.get(key)
        if current is None or (report.date, report.timestamp, report.message_id) > (
            current.date,
            current.timestamp,
            current.message_id,
        ):
            latest[key] = report
    return sorted(latest.values(), key=lambda item: (item.ticker, item.kind))


def selected_reports(
    reports: list[ReportMessage],
    *,
    latest_only: bool,
    buy_only: bool,
    tickers: set[str] | None,
) -> list[ReportMessage]:
    pool = latest_reports(reports) if latest_only else reports
    latest_research = {r.ticker: r for r in latest_reports(reports) if r.kind == "research"}

    selected: list[ReportMessage] = []
    for report in pool:
        if tickers and report.ticker not in tickers:
            continue
        research = latest_research.get(report.ticker)
        if buy_only and (research is None or research.verdict != "BUY"):
            continue
        selected.append(report)
    return sorted(selected, key=lambda item: (item.ticker, item.kind, item.date, item.message_id))


def safe_filename(name: str) -> str:
    return Path(name).name.replace("/", "_")


def download_pdf(attachment: dict[str, Any], destination: Path, timeout: int) -> tuple[str, str | None]:
    urls = [attachment.get("url"), attachment.get("proxy_url")]
    last_error: str | None = None
    for url in [u for u in urls if isinstance(u, str) and u]:
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "application/pdf,*/*",
                },
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                destination.write_bytes(response.read())
            return "downloaded", None
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            last_error = repr(exc)
    return "failed", last_error or "no usable attachment url"


def convert_pdf(pdf_path: Path, txt_path: Path, pdftotext: str | None) -> tuple[str, str | None]:
    if txt_path.exists():
        return "existing", None
    if not pdf_path.exists():
        return "missing_pdf", None
    if pdftotext is None:
        return "skipped_missing_pdftotext", "pdftotext not found"
    try:
        subprocess.run(
            [pdftotext, "-layout", str(pdf_path), str(txt_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )
        return "converted", None
    except (subprocess.SubprocessError, OSError) as exc:
        return "failed", repr(exc)


def process_reports(args: argparse.Namespace) -> dict[str, Any]:
    cache = load_cache(args.cache_json)
    reports = iter_reports(cache)
    selected = selected_reports(
        reports,
        latest_only=not args.all_versions,
        buy_only=args.buy_only,
        tickers=set(args.ticker) if args.ticker else None,
    )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    pdftotext = shutil.which("pdftotext") if args.convert else None
    results: list[dict[str, Any]] = []

    for report in selected:
        for attachment in report.message.get("attachments") or []:
            if not isinstance(attachment, dict):
                continue
            filename = str(attachment.get("filename", ""))
            if not filename.lower().endswith(".pdf"):
                continue
            pdf_path = args.out_dir / safe_filename(filename)
            txt_path = pdf_path.with_suffix(".txt")

            if pdf_path.exists() and not args.force:
                download_status, download_error = "existing", None
            else:
                download_status, download_error = download_pdf(attachment, pdf_path, args.timeout)

            convert_status, convert_error = convert_pdf(pdf_path, txt_path, pdftotext)
            results.append(
                {
                    "ticker": report.ticker,
                    "kind": report.kind,
                    "date": report.date,
                    "verdict": report.verdict,
                    "channel_id": report.channel_id,
                    "message_id": report.message_id,
                    "filename": filename,
                    "pdf_path": str(pdf_path),
                    "txt_path": str(txt_path),
                    "download_status": download_status,
                    "download_error": download_error,
                    "convert_status": convert_status,
                    "convert_error": convert_error,
                }
            )

    failures = [item for item in results if item["download_status"] == "failed" or item["convert_status"] == "failed"]
    manifest = {
        "cache_json": str(args.cache_json),
        "out_dir": str(args.out_dir),
        "latest_only": not args.all_versions,
        "buy_only": args.buy_only,
        "tickers": sorted(set(args.ticker or [])),
        "reports_seen": len(reports),
        "reports_selected": len(selected),
        "pdf_results": results,
        "failure_count": len(failures),
        "note": "Expired Discord attachment URLs return 404. Open the ticker threads in Discord, rerun cache_dump.py, then rerun this script.",
    }
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-json", type=Path, required=True, help="JSON produced by scripts/cache_dump.py")
    parser.add_argument("--out-dir", type=Path, default=Path("us_pdfs"), help="Directory for downloaded PDFs and .txt files")
    parser.add_argument("--manifest", type=Path, help="Write a JSON manifest with per-attachment status")
    parser.add_argument("--ticker", action="append", help="Limit to one ticker. Repeatable.")
    parser.add_argument("--buy-only", action="store_true", help="Keep only tickers whose latest research verdict is BUY")
    parser.add_argument("--all-versions", action="store_true", help="Download every cached report version, not just latest per ticker/kind")
    parser.add_argument("--no-convert", action="store_false", dest="convert", help="Skip pdftotext conversion")
    parser.add_argument("--force", action="store_true", help="Re-download PDFs even if they already exist")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if any download or conversion fails")
    parser.add_argument("--timeout", type=int, default=30, help="Per-download timeout in seconds")
    parser.set_defaults(convert=True)
    args = parser.parse_args()

    manifest = process_reports(args)
    results = manifest["pdf_results"]
    counts: dict[str, int] = {}
    for item in results:
        counts[item["download_status"]] = counts.get(item["download_status"], 0) + 1
    print(
        "reports_seen={reports_seen} reports_selected={reports_selected} pdfs={pdfs} failures={failures} download_status={counts}".format(
            reports_seen=manifest["reports_seen"],
            reports_selected=manifest["reports_selected"],
            pdfs=len(results),
            failures=manifest["failure_count"],
            counts=counts,
        )
    )
    if manifest["failure_count"]:
        print(manifest["note"], file=sys.stderr)
    return 1 if args.strict and manifest["failure_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
