import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests

from scripts.build import (
    CHANGELOG_THRESHOLD,
    ScraperError,
    _filter_metadata_lines,
    _strip_chapter_number,
    build_llms_full,
    build_llms_txt,
    build_meta_json,
    compute_diff_stats,
    fetch_github_metadata,
    format_changelog_entry,
    parse_print,
    parse_toc,
    truncate,
)

FIXTURES = Path(__file__).parent / "fixtures"


def toc_html() -> str:
    return (FIXTURES / "toc_minimal.html").read_text(encoding="utf-8")


def print_html() -> str:
    return (FIXTURES / "print_minimal.html").read_text(encoding="utf-8")


class TestParseToc:
    def test_section_and_page_counts(self):
        entries = parse_toc(toc_html())
        assert sum(1 for e in entries if e["is_section"]) == 2
        assert sum(1 for e in entries if not e["is_section"]) == 4

    def test_section_titles(self):
        entries = parse_toc(toc_html())
        titles = [e["title"] for e in entries if e["is_section"]]
        assert titles == ["Part I: Tutorial", "Part II: Reference"]

    def test_page_urls_are_absolute(self):
        entries = parse_toc(toc_html())
        pages = [e for e in entries if not e["is_section"]]
        assert all(e["url"].startswith("https://") for e in pages)

    def test_nested_depth(self):
        entries = parse_toc(toc_html())
        pages = {e["title"]: e for e in entries if not e["is_section"]}
        assert pages["Introduction"]["depth"] == 0
        assert pages["Sub Topic"]["depth"] == 1

    def test_spacer_skipped(self):
        entries = parse_toc(toc_html())
        assert all(e["title"] != "" for e in entries)

    def test_missing_chapter_ol_raises(self):
        with pytest.raises(ScraperError, match="ol class='chapter'"):
            parse_toc("<html><body><p>no toc here</p></body></html>")

    def test_chapter_number_prefix_stripped(self):
        html = (
            '<html><body><ol class="chapter">'
            '<li class="chapter-item">'
            '<a href="ch.html"><strong aria-hidden="true">7.</strong> Setting Up</a>'
            "</li></ol></body></html>"
        )
        entries = parse_toc(html)
        assert entries[0]["title"] == "Setting Up"

    def test_no_duplicate_urls(self):
        entries = parse_toc(toc_html())
        urls = [e["url"] for e in entries if not e["is_section"]]
        assert len(urls) == len(set(urls))


class TestStripChapterNumber:
    def test_single_level(self):
        assert _strip_chapter_number("7.Setting Up") == "Setting Up"

    def test_two_level(self):
        assert _strip_chapter_number("7.1.Installation") == "Installation"

    def test_multi_level(self):
        assert _strip_chapter_number("37.15.DESCRIBE PAGE") == "DESCRIBE PAGE"

    def test_no_number(self):
        assert _strip_chapter_number("Preface") == "Preface"

    def test_title_starting_with_digit(self):
        # "5-Minute Quickstart" after stripping "6." from "6.5-Minute Quickstart"
        assert _strip_chapter_number("6.5-Minute Quickstart") == "5-Minute Quickstart"


class TestParsePrint:
    def test_returns_nonempty_markdown(self):
        full_md, blurbs = parse_print(print_html())
        assert len(full_md) > 0
        assert isinstance(blurbs, dict)

    def test_blurbs_extracted_for_headings_with_paragraphs(self):
        _, blurbs = parse_print(print_html())
        assert "Introduction" in blurbs
        assert "Advanced" in blurbs

    def test_no_blurb_for_heading_without_following_paragraph(self):
        # "API Reference" h2 has no paragraph before end of content
        _, blurbs = parse_print(print_html())
        assert "API Reference" not in blurbs

    def test_blurb_is_first_paragraph_only(self):
        _, blurbs = parse_print(print_html())
        assert "second paragraph" not in blurbs.get("Introduction", "")

    def test_blurb_respects_max_length(self):
        _, blurbs = parse_print(print_html())
        for blurb in blurbs.values():
            assert len(blurb) <= 133  # MAX_BLURB_LEN + len("…")

    def test_nav_stripped(self):
        full_md, _ = parse_print(print_html())
        assert "Home" not in full_md

    def test_no_triple_newlines(self):
        full_md, _ = parse_print(print_html())
        assert "\n\n\n" not in full_md


class TestTruncate:
    def test_short_string_unchanged(self):
        assert truncate("hello", 10) == "hello"

    def test_truncates_at_word_boundary(self):
        result = truncate("one two three four five", 10)
        assert result.endswith("…")
        assert len(result) <= 12

    def test_strips_trailing_punctuation_before_ellipsis(self):
        result = truncate("hello world, more text here", 13)
        assert not result.rstrip("…").endswith(",")

    def test_exact_length_unchanged(self):
        s = "exactly ten"
        assert truncate(s, len(s)) == s


class TestBuildLlmsTxt:
    TOC = [
        {"title": "Tutorial", "url": "", "is_section": True, "depth": 0},
        {"title": "Page One", "url": "https://example.com/p.html", "is_section": False, "depth": 0},
    ]

    def test_title_and_description_present(self):
        out = build_llms_txt(self.TOC, {}, generated_at="T", version_stamp="")
        assert "# mxcli Documentation" in out
        assert "> CLI tool" in out

    def test_section_rendered_as_h2(self):
        out = build_llms_txt(self.TOC, {}, generated_at="T", version_stamp="")
        assert "## Tutorial" in out

    def test_page_rendered_as_list_item(self):
        out = build_llms_txt(self.TOC, {}, generated_at="T", version_stamp="")
        assert "- [Page One](https://example.com/p.html)" in out

    def test_blurb_appended_when_present(self):
        out = build_llms_txt(
            self.TOC, {"Page One": "A short blurb."}, generated_at="T", version_stamp=""
        )
        assert "- [Page One](https://example.com/p.html): A short blurb." in out

    def test_version_stamp_line_format(self):
        out = build_llms_txt(
            self.TOC, {}, generated_at="2026-01-01T00:00:00Z", version_stamp="v1.0 @ abc"
        )
        assert "Version: v1.0 @ abc | Generated: 2026-01-01T00:00:00Z" in out

    def test_no_version_stamp_fallback(self):
        out = build_llms_txt(self.TOC, {}, generated_at="2026-01-01T00:00:00Z", version_stamp="")
        assert "Generated: 2026-01-01T00:00:00Z" in out
        assert "Version:" not in out

    def test_deterministic(self):
        a = build_llms_txt(self.TOC, {}, generated_at="T", version_stamp="V")
        b = build_llms_txt(self.TOC, {}, generated_at="T", version_stamp="V")
        assert a == b


class TestBuildLlmsFull:
    def test_header_lines_present(self):
        out = build_llms_full("# Content", generated_at="2026-01-01T00:00:00Z", version_stamp="")
        assert "# mxcli Documentation — Full Reference" in out
        assert "Generated: 2026-01-01T00:00:00Z" in out
        assert "# Content" in out

    def test_version_line_present_when_stamp_given(self):
        out = build_llms_full("md", generated_at="T", version_stamp="v1.0 @ abc")
        assert "Version:   v1.0 @ abc" in out

    def test_no_version_line_without_stamp(self):
        out = build_llms_full("md", generated_at="T", version_stamp="")
        assert "Version:" not in out

    def test_separator_present(self):
        out = build_llms_full("content", generated_at="T", version_stamp="")
        assert "---" in out

    def test_deterministic(self):
        a = build_llms_full("md", generated_at="T", version_stamp="V")
        b = build_llms_full("md", generated_at="T", version_stamp="V")
        assert a == b


class TestBuildMetaJson:
    KWARGS = dict(
        mxcli_release="v1.0.0",
        mxcli_commit="abc1234",
        generated_at="2026-01-01T00:00:00Z",
        llms_txt_chars=100,
        llms_full_chars=9000,
    )

    def test_valid_json(self):
        json.loads(build_meta_json(**self.KWARGS))

    def test_all_fields_present(self):
        data = json.loads(build_meta_json(**self.KWARGS))
        assert data["mxcli_release"] == "v1.0.0"
        assert data["mxcli_commit"] == "abc1234"
        assert data["generated_at"] == "2026-01-01T00:00:00Z"
        assert data["source"]["toc"] == "https://www.mxcli.org/toc.html"
        assert data["source"]["print"] == "https://www.mxcli.org/print.html"
        assert data["outputs"]["llms_txt_chars"] == 100
        assert data["outputs"]["llms_full_chars"] == 9000

    def test_deterministic(self):
        assert build_meta_json(**self.KWARGS) == build_meta_json(**self.KWARGS)


class TestFetchGithubMetadata:
    def test_returns_unknown_on_request_error(self):
        with patch("scripts.build.requests.get") as mock_get:
            mock_get.side_effect = requests.RequestException("timeout")
            result = fetch_github_metadata(token=None)
        assert result == {"release": "unknown", "commit": "unknown"}

    def test_extracts_release_and_7char_commit(self):
        release_resp = Mock()
        release_resp.json.return_value = {"tag_name": "v1.2.3"}
        release_resp.raise_for_status = Mock()
        commit_resp = Mock()
        commit_resp.json.return_value = {"sha": "abc1234567890"}
        commit_resp.raise_for_status = Mock()
        with patch("scripts.build.requests.get", side_effect=[release_resp, commit_resp]):
            result = fetch_github_metadata(token="tok")
        assert result["release"] == "v1.2.3"
        assert result["commit"] == "abc1234"

    def test_partial_failure_commit_unknown(self):
        release_resp = Mock()
        release_resp.json.return_value = {"tag_name": "v2.0.0"}
        release_resp.raise_for_status = Mock()
        with patch(
            "scripts.build.requests.get",
            side_effect=[release_resp, requests.RequestException("timeout")],
        ):
            result = fetch_github_metadata(token=None)
        assert result["release"] == "v2.0.0"
        assert result["commit"] == "unknown"


class TestFilterMetadataLines:
    def test_strips_generated_line(self):
        lines = ["# Title", "Generated: 2026-01-01T00:00:00Z", "## Section"]
        assert _filter_metadata_lines(lines) == ["# Title", "## Section"]

    def test_strips_version_line(self):
        lines = ["# Title", "Version:   mxcli v1.0 @ abc", "## Section"]
        assert _filter_metadata_lines(lines) == ["# Title", "## Section"]

    def test_preserves_content_lines(self):
        lines = ["## Installation", "Run the following command."]
        assert _filter_metadata_lines(lines) == lines


class TestComputeDiffStats:
    def test_identical_lines_zero_changes(self):
        lines = ["# Doc", "## Section A", "Some content."]
        added, removed, sections = compute_diff_stats(lines, lines)
        assert added == 0
        assert removed == 0
        assert sections == []

    def test_added_line_counted(self):
        old = ["# Doc", "## Section A", "Old content."]
        new = ["# Doc", "## Section A", "Old content.", "New line."]
        added, removed, sections = compute_diff_stats(old, new)
        assert added == 1
        assert removed == 0

    def test_removed_line_counted(self):
        old = ["# Doc", "## Section A", "Line one.", "Line two."]
        new = ["# Doc", "## Section A", "Line one."]
        added, removed, _ = compute_diff_stats(old, new)
        assert added == 0
        assert removed == 1

    def test_changed_section_detected(self):
        old = ["## Installation", "Run pip install."]
        new = ["## Installation", "Run pip install mxcli."]
        _, _, sections = compute_diff_stats(old, new)
        assert "## Installation" in sections

    def test_unchanged_section_not_reported(self):
        old = ["## Alpha", "Alpha content.", "## Beta", "Beta content."]
        new = ["## Alpha", "Alpha content.", "## Beta", "Changed beta content."]
        _, _, sections = compute_diff_stats(old, new)
        assert "## Beta" in sections
        assert "## Alpha" not in sections

    def test_threshold_constant_is_positive(self):
        assert CHANGELOG_THRESHOLD > 0


class TestFormatChangelogEntry:
    def test_contains_date_and_version(self):
        out = format_changelog_entry(
            date="2026-05-17",
            version_stamp="mxcli v1.0 @ abc1234",
            added=10,
            removed=5,
            sections=[],
        )
        assert "2026-05-17" in out
        assert "mxcli v1.0 @ abc1234" in out

    def test_line_counts_present(self):
        out = format_changelog_entry(
            date="D", version_stamp="V", added=42, removed=7, sections=[]
        )
        assert "+42" in out
        assert "-7" in out

    def test_sections_listed(self):
        out = format_changelog_entry(
            date="D",
            version_stamp="V",
            added=1,
            removed=1,
            sections=["## Part I: Tutorial", "## Part II: Reference"],
        )
        assert "Part I: Tutorial" in out
        assert "Part II: Reference" in out

    def test_empty_sections_shows_unclassified(self):
        out = format_changelog_entry(
            date="D", version_stamp="V", added=1, removed=1, sections=[]
        )
        assert "unclassified" in out

    def test_many_sections_truncated(self):
        sections = [f"## Section {i}" for i in range(20)]
        out = format_changelog_entry(
            date="D", version_stamp="V", added=1, removed=1, sections=sections
        )
        assert "more" in out
