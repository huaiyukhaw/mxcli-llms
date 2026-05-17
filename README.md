# mxcli-llms

Curated [mxcli](https://www.mxcli.org) documentation for AI coding assistants — updated daily.

---

## The files

| File | Size | What it is |
|---|---|---|
| [`llms.txt`](https://YOUR_GITHUB_USERNAME.github.io/mxcli-llms/llms.txt) | ~45 KB | [llms.txt-spec](https://llmstxt.org/) index: title, section headers, one link + blurb per page |
| [`llms-full.txt`](https://YOUR_GITHUB_USERNAME.github.io/mxcli-llms/llms-full.txt) | ~960 KB | Entire mxcli book as a single Markdown file — use this for in-context reference |

> **Replace `YOUR_GITHUB_USERNAME`** with your actual GitHub username in all URLs below.

---

## Integration recipes

### Claude Code

Add to your project's `CLAUDE.md` so every Claude Code session has mxcli docs in context:

```markdown
## mxcli reference
Use WebFetch on https://YOUR_GITHUB_USERNAME.github.io/mxcli-llms/llms-full.txt
for mxcli CLI documentation.
```

Or fetch on demand in any session:

```
Use WebFetch to read https://YOUR_GITHUB_USERNAME.github.io/mxcli-llms/llms-full.txt
then answer: how do I run a deployment?
```

### Cursor

1. Open **Settings** (⌘/Ctrl+Shift+J) → **Features** → **Docs**
2. Click **+ Add new doc**
3. Paste: `https://YOUR_GITHUB_USERNAME.github.io/mxcli-llms/llms-full.txt`
4. Reference it in chat with `@mxcli-llms`

### GitHub Copilot

Commit `llms-full.txt` to your repo root — Copilot reads workspace files as context:

```bash
curl -o llms-full.txt https://YOUR_GITHUB_USERNAME.github.io/mxcli-llms/llms-full.txt
git add llms-full.txt && git commit -m "chore: add mxcli docs for Copilot context"
```

### Windsurf

In the Cascade panel, type `@docs` and add the URL:

```
https://YOUR_GITHUB_USERNAME.github.io/mxcli-llms/llms-full.txt
```

### Continue.dev

Add to `~/.continue/config.json`:

```json
{
  "docs": [
    {
      "title": "mxcli",
      "startUrl": "https://YOUR_GITHUB_USERNAME.github.io/mxcli-llms/llms-full.txt"
    }
  ]
}
```

---

## What's inside

The scraper fetches two static endpoints from `mxcli.org` — both are pre-rendered by [mdBook](https://rust-lang.github.io/mdBook/) and require no JavaScript: `toc.html` for the table of contents structure, and `print.html` for the full book content in one page. The content is converted to clean Markdown and written to `dist/`. A second call to the GitHub API (`mendixlabs/mxcli`) records the latest release tag and commit SHA so every build is traceable to an exact upstream version. The entire pipeline is a single Python script with no LLM calls, no embeddings, and no headless browsers.

---

## Versioning & freshness

Every file is rebuilt daily at 02:00 UTC. The build is also triggerable manually from the Actions tab. Check `meta.json` to see what version is currently published:

```bash
curl -s https://YOUR_GITHUB_USERNAME.github.io/mxcli-llms/meta.json | python -m json.tool
```

```json
{
  "mxcli_release": "v0.10.0",
  "mxcli_commit": "849fb4e",
  "generated_at": "2026-05-17T03:08:21Z",
  "source": {
    "toc": "https://www.mxcli.org/toc.html",
    "print": "https://www.mxcli.org/print.html"
  },
  "outputs": {
    "llms_txt_chars": 46423,
    "llms_full_chars": 985522
  }
}
```

When upstream docs change by 20 or more lines, the build appends an entry to `dist/CHANGELOG.md` noting the line delta and which sections changed. If content is byte-identical to the previous build, no commit is made.

---

## License & attribution

The scraper code in this repository is MIT licensed — see [`LICENSE`](LICENSE).

The documentation content in `dist/` is scraped from [mxcli.org](https://www.mxcli.org) and remains the property of the mxcli authors / Mendix. It is reproduced here solely to enable AI tooling workflows. If the upstream authors request removal, this repository will be taken down immediately.

---

## Contributing

Bug reports and pull requests are welcome. If you change the scraper output format, make sure `python -m pytest tests/ -q` still passes and that running the script twice against the same upstream HTML produces byte-identical output — determinism is a hard requirement so diffs are meaningful.
