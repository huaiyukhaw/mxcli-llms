#!/usr/bin/env python3
"""
Scrape mxcli docs → dist/llms.txt + dist/llms-full.txt

Usage:
    python scripts/build.py [--dry-run]
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as to_md

BASE_URL = "https://www.mxcli.org"
TOC_URL = f"{BASE_URL}/toc.html"
PRINT_URL = f"{BASE_URL}/print.html"

SITE_TITLE = "mxcli Documentation"
SITE_DESCRIPTION = (
    "CLI tool and MDL (Mendix Definition Language) for reading, querying, "
    "and modifying Mendix application projects headlessly. Designed primarily "
    "for AI coding agents (Claude Code, Cursor, GitHub Copilot) and CI/CD pipelines."
)

REQUEST_HEADERS = {
    "User-Agent": "llms-txt-builder/1.0",
    "Accept": "text/html,application/xhtml+xml",
}

MAX_BLURB_LEN = 130
CHANGELOG_THRESHOLD = 20   # min added+removed lines before writing a CHANGELOG entry
DIST_DIR = Path(__file__).parent.parent / "dist"
GITHUB_API = "https://api.github.com"
GITHUB_REPO = "mendixlabs/mxcli"

# Lines in llms-full.txt that change every run regardless of doc content.
# Filtered out before content comparison so a new timestamp or commit SHA
# alone doesn't trigger a spurious commit.
_METADATA_LINE_RE = re.compile(r"^(Generated: |Version:)")

_CHAPTER_NUMBER_RE = re.compile(r"^(\d+\.)+")  # strips "7." / "7.1." / "37.15." prefixes


class ScraperError(Exception):
    """Raised on unrecoverable structural failures (site HTML changed, etc.)."""


# ── Utilities ─────────────────────────────────────────────────────────────────

def truncate(text: str, n: int) -> str:
    """Truncate to n chars at a word boundary."""
    if len(text) <= n:
        return text
    return text[:n].rsplit(" ", 1)[0].rstrip(".,;:") + "…"


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── I/O functions ─────────────────────────────────────────────────────────────

def fetch_html(url: str) -> str:
    """Fetch URL and return raw HTML. Raises ScraperError on network/HTTP failure."""
    print(f"  GET {url}")
    try:
        r = requests.get(url, headers=REQUEST_HEADERS, timeout=30)
        r.raise_for_status()
    except requests.RequestException as exc:
        raise ScraperError(f"Failed to fetch {url}: {exc}") from exc
    return r.text


def fetch_toc() -> str:
    return fetch_html(TOC_URL)


def fetch_print() -> str:
    return fetch_html(PRINT_URL)


def write_outputs(outputs: dict[str, str], dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for filename, content in outputs.items():
        (dest / filename).write_text(content, encoding="utf-8")


def fetch_github_metadata(token: str | None) -> dict:
    """
    Fetch latest mxcli release tag and main branch commit SHA from GitHub API.
    Never raises — on any failure logs a warning and returns 'unknown' values.
    token: GITHUB_TOKEN env var; None falls back to unauthenticated (60 req/hour).
    """
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    release = "unknown"
    commit = "unknown"

    try:
        r = requests.get(
            f"{GITHUB_API}/repos/{GITHUB_REPO}/releases/latest",
            headers=headers,
            timeout=10,
        )
        r.raise_for_status()
        release = r.json().get("tag_name", "unknown")
    except requests.RequestException as exc:
        print(f"  [warn] GitHub releases API: {exc} -- using 'unknown'", file=sys.stderr)

    try:
        r = requests.get(
            f"{GITHUB_API}/repos/{GITHUB_REPO}/commits/main",
            headers=headers,
            timeout=10,
        )
        r.raise_for_status()
        sha = r.json().get("sha", "")
        commit = sha[:7] if sha else "unknown"
    except requests.RequestException as exc:
        print(f"  [warn] GitHub commits API: {exc} -- using 'unknown'", file=sys.stderr)

    return {"release": release, "commit": commit}


# ── TOC parsing ───────────────────────────────────────────────────────────────

def _strip_chapter_number(text: str) -> str:
    """Strip leading mdBook number prefix: '7.' / '7.1.' / '37.15.' → bare title."""
    return _CHAPTER_NUMBER_RE.sub("", text).strip()


def parse_toc(html: str) -> list[dict]:
    """
    Parse the mdBook toc.html <ol class='chapter'> into a flat ordered list.

    Entry shape:
        {
            "title":      str,
            "url":        str,   # empty for section dividers
            "depth":      int,   # ancestor <ol> count between this li and ol.chapter
            "is_section": bool,  # True for Part headers (no link)
        }

    Uses a flat traversal over ALL li descendants rather than recursive=False,
    because html.parser does not auto-close <li> tags the way browsers do — the
    mxcli.org toc.html has no explicit </li> before sibling chapters, causing
    html.parser to nest the entire book inside the first chapter that has a
    sub-section. Flat traversal + seen_urls dedup produces correct output regardless.

    mdBook renders chapter numbers via <strong aria-hidden="true">N.</strong>;
    get_text(strip=True) concatenates to "7.Setting Up" — _strip_chapter_number
    removes the prefix so titles match print.html headings.

    The chapter link lives inside <span class="chapter-link-wrapper"><a href="...">.
    Falls back to a direct <a href> child for non-standard themes and test fixtures.
    """
    soup = BeautifulSoup(html, "html.parser")
    ol = soup.select_one("ol.chapter")
    if not ol:
        raise ScraperError(
            "Could not find <ol class='chapter'> in toc.html — "
            "the site structure may have changed. Check the HTML manually."
        )

    entries: list[dict] = []
    seen_urls: set[str] = set()

    for li in ol.find_all("li"):
        classes = li.get("class", [])

        if "spacer" in classes:
            continue

        if "part-title" in classes:
            title = li.get_text(strip=True)
            if title:
                entries.append({"title": title, "url": "", "depth": 0, "is_section": True})
            continue

        if "chapter-item" not in classes:
            continue

        # Prefer mdBook's <span class="chapter-link-wrapper"> for the page link.
        # Fall back to direct <a href> child for non-standard themes / test fixtures.
        wrapper = li.find("span", class_="chapter-link-wrapper")
        if wrapper:
            a = wrapper.find("a", href=True)
        else:
            a = li.find("a", href=True, recursive=False)

        if not a:
            continue

        href = a.get("href", "")
        url = urljoin(TOC_URL, href) if not href.startswith("http") else href

        if url in seen_urls:
            continue
        seen_urls.add(url)

        # Depth = number of <ol> ancestors between this li and ol.chapter.
        depth = 0
        node = li.parent
        while node and node is not ol:
            if node.name == "ol":
                depth += 1
            node = node.parent

        entries.append({
            "title": _strip_chapter_number(a.get_text(strip=True)),
            "url": url,
            "depth": depth,
            "is_section": False,
        })

    return entries


# ── print.html parsing ────────────────────────────────────────────────────────

def parse_print(html: str) -> tuple[str, dict[str, str]]:
    """
    Extract full book Markdown and per-section blurbs from print.html.

    Returns:
        full_md : entire book as Markdown string
        blurbs  : {section title → first paragraph text (truncated)}

    Blurb lookup is exact-match on heading text vs TOC entry title. Unmatched
    TOC entries get no blurb — acceptable per llms.txt spec.
    """
    soup = BeautifulSoup(html, "html.parser")
    # mdBook print.html nests content in div#content > div#content-main
    body = (
        soup.select_one("div#content-main")
        or soup.select_one("div#content")
        or soup.select_one("main")
        or soup.body
    )
    if body is None:
        raise ScraperError("Could not locate content element in print.html.")

    # Strip navigation chrome that bleeds into print view
    for sel in [
        "nav",
        ".nav-chapters",
        ".mobile-nav-chapters",
        "#menu-bar",
        "#searchbar",
        ".search-results",
        ".search-wrapper",
        "footer",
    ]:
        for el in body.select(sel):
            el.decompose()

    # For each h1/h2, walk forward siblings to find the first real paragraph.
    blurbs: dict[str, str] = {}
    for h in body.find_all(["h1", "h2"]):
        title = h.get_text(strip=True)
        sib = h.find_next_sibling()
        while sib:
            if sib.name == "p":
                text = sib.get_text(" ", strip=True)
                if text:
                    blurbs[title] = truncate(text, MAX_BLURB_LEN)
                break
            if sib.name in ("h1", "h2"):
                break
            sib = sib.find_next_sibling()

    full_md = to_md(
        str(body),
        heading_style="ATX",
        bullets="-",
        strip=["script", "style"],
    )
    # Collapse 3+ blank lines to 2
    full_md = re.sub(r"\n{3,}", "\n\n", full_md).strip()

    return full_md, blurbs


# ── Output builders ───────────────────────────────────────────────────────────

def build_llms_txt(
    toc: list[dict],
    blurbs: dict[str, str],
    *,
    generated_at: str,
    version_stamp: str,
) -> str:
    """
    Produce spec-compliant llms.txt (https://llmstxt.org/).

    version_stamp: e.g. "mxcli v0.x.y @ abc1234", or "" before Phase 1.
    generated_at and version_stamp are injected by main() — no datetime.now() here.
    """
    if version_stamp:
        stamp_line = f"Version: {version_stamp} | Generated: {generated_at}"
    else:
        stamp_line = f"Generated: {generated_at}"

    lines: list[str] = [
        f"# {SITE_TITLE}",
        "",
        f"> {SITE_DESCRIPTION}",
        "",
        stamp_line,
        "",
        f"Full content (entire book, single page): {PRINT_URL}",
        "",
    ]

    for entry in toc:
        if entry["is_section"]:
            lines.append("")
            lines.append(f"## {entry['title']}")
        else:
            blurb = blurbs.get(entry["title"], "")
            suffix = f": {blurb}" if blurb else ""
            lines.append(f"- [{entry['title']}]({entry['url']}){suffix}")

    lines.append("")
    return "\n".join(lines)


def build_llms_full(
    full_md: str,
    *,
    generated_at: str,
    version_stamp: str,
) -> str:
    """
    generated_at and version_stamp injected by main() — no datetime.now() here.
    The Generated: line is the only one that changes between identical-content runs;
    Phase 2 diff logic strips lines matching ^Generated: before comparing.
    """
    version_line = f"Version:   {version_stamp}\n" if version_stamp else ""
    header = (
        f"# {SITE_TITLE} — Full Reference\n\n"
        f"Source:    {PRINT_URL}\n"
        f"{version_line}"
        f"Generated: {generated_at}\n\n"
        f"---\n\n"
    )
    return header + full_md


# ── Change detection ──────────────────────────────────────────────────────────

def _filter_metadata_lines(lines: list[str]) -> list[str]:
    """Strip Generated:/Version: header lines before content comparison."""
    return [ln for ln in lines if not _METADATA_LINE_RE.match(ln)]


def compute_diff_stats(
    old_lines: list[str], new_lines: list[str]
) -> tuple[int, int, list[str]]:
    """
    Diff two lists of content lines (metadata lines already stripped).
    Returns (added_count, removed_count, sorted section titles with changes).

    Section titles are derived from the nearest preceding # / ## heading in
    the ndiff output — informational only, used for CHANGELOG entries.
    """
    diff = list(difflib.ndiff(old_lines, new_lines))
    added   = sum(1 for d in diff if d.startswith("+ "))
    removed = sum(1 for d in diff if d.startswith("- "))

    changed_sections: set[str] = set()
    current_section: str | None = None
    for token in diff:
        code    = token[:2]   # "  " / "+ " / "- " / "? "
        content = token[2:]
        if code in ("  ", "+ ", "- ") and (
            content.startswith("# ") or content.startswith("## ")
        ):
            current_section = content.strip()
        if code in ("+ ", "- ") and current_section:
            changed_sections.add(current_section)

    return added, removed, sorted(changed_sections)


def format_changelog_entry(
    *,
    date: str,
    version_stamp: str,
    added: int,
    removed: int,
    sections: list[str],
) -> str:
    """Format a single CHANGELOG.md entry block (no trailing newline)."""
    MAX_SECTIONS = 8
    clean = [s.lstrip("#").strip() for s in sections]
    if clean:
        sections_str = ", ".join(clean[:MAX_SECTIONS])
        if len(clean) > MAX_SECTIONS:
            sections_str += f" (+{len(clean) - MAX_SECTIONS} more)"
    else:
        sections_str = "(unclassified)"
    return (
        f"## {date} -- {version_stamp}\n"
        f"- +{added} / -{removed} lines\n"
        f"- Sections changed: {sections_str}"
    )


def build_meta_json(
    *,
    mxcli_release: str,
    mxcli_commit: str,
    generated_at: str,
    llms_txt_chars: int,
    llms_full_chars: int,
) -> str:
    data = {
        "mxcli_release": mxcli_release,
        "mxcli_commit": mxcli_commit,
        "generated_at": generated_at,
        "source": {"toc": TOC_URL, "print": PRINT_URL},
        "outputs": {
            "llms_txt_chars": llms_txt_chars,
            "llms_full_chars": llms_full_chars,
        },
    }
    return json.dumps(data, indent=2) + "\n"


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build mxcli llms.txt and llms-full.txt")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Build outputs in memory and print sizes without writing to disk.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    generated_at = utcnow_iso()
    token = os.getenv("GITHUB_TOKEN")

    try:
        print("Step 1/4  Resolving mxcli version from GitHub...")
        gh = fetch_github_metadata(token)
        print(f"          release={gh['release']}  commit={gh['commit']}")
        version_stamp = f"mxcli {gh['release']} @ {gh['commit']}"

        print("\nStep 2/4  Parsing TOC from toc.html...")
        toc = parse_toc(fetch_toc())
        n_sections = sum(1 for e in toc if e["is_section"])
        n_pages    = sum(1 for e in toc if not e["is_section"])
        print(f"          {n_sections} part sections, {n_pages} pages")

        print("\nStep 3/4  Fetching full book (print.html)...")
        full_md, blurbs = parse_print(fetch_print())
        print(f"          {len(full_md):,} chars Markdown | {len(blurbs)} blurbs extracted")

        unmatched = [
            e["title"] for e in toc
            if not e["is_section"] and e["title"] not in blurbs
        ]
        if unmatched:
            print(
                f"          [warn] No blurb for {len(unmatched)} pages "
                f"(TOC title vs heading mismatch)"
            )
            if len(unmatched) <= 10:
                for t in unmatched:
                    print(f"             - {t}")

        print("\nStep 4/4  Building outputs...")
        llms_txt  = build_llms_txt(
            toc, blurbs, generated_at=generated_at, version_stamp=version_stamp
        )
        llms_full = build_llms_full(
            full_md, generated_at=generated_at, version_stamp=version_stamp
        )
        meta_json = build_meta_json(
            mxcli_release=gh["release"],
            mxcli_commit=gh["commit"],
            generated_at=generated_at,
            llms_txt_chars=len(llms_txt),
            llms_full_chars=len(llms_full),
        )
        print(f"          llms.txt      : {len(llms_txt):,} chars")
        print(f"          llms-full.txt : {len(llms_full):,} chars")

        # ── Change detection ──────────────────────────────────────────────────
        content_changed = True
        added = removed = 0
        changed_sections: list[str] = []

        old_full_path = DIST_DIR / "llms-full.txt"
        if old_full_path.exists():
            old_text  = old_full_path.read_text(encoding="utf-8")
            old_lines = _filter_metadata_lines(old_text.splitlines())
            new_lines = _filter_metadata_lines(llms_full.splitlines())
            if old_lines == new_lines:
                content_changed = False
            else:
                added, removed, changed_sections = compute_diff_stats(old_lines, new_lines)

        if not content_changed:
            print("\nContent unchanged -- nothing written.")
            return

        print(f"\nContent changed: +{added} / -{removed} lines")

        # Build output dict; add CHANGELOG when diff is meaningful
        outputs: dict[str, str] = {
            "llms.txt": llms_txt,
            "llms-full.txt": llms_full,
            "meta.json": meta_json,
        }
        if added + removed >= CHANGELOG_THRESHOLD:
            entry = format_changelog_entry(
                date=generated_at[:10],
                version_stamp=version_stamp,
                added=added,
                removed=removed,
                sections=changed_sections,
            )
            changelog_path = DIST_DIR / "CHANGELOG.md"
            existing = (
                changelog_path.read_text(encoding="utf-8")
                if changelog_path.exists()
                else ""
            )
            outputs["CHANGELOG.md"] = entry + "\n\n" + existing
            print(
                f"          CHANGELOG.md  : +1 entry "
                f"({len(changed_sections)} sections)"
            )

        if args.dry_run:
            print("\n--dry-run: outputs not written.")
            return

        write_outputs(outputs, DIST_DIR)
        print(f"\nDone. Written to {DIST_DIR}/")

    except ScraperError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
