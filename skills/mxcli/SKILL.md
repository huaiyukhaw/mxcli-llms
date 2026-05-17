---
name: mxcli
description: Answer questions about the mxcli CLI tool using the published documentation. Use when the user asks how to do something with mxcli, wants to understand a command, or says "mxcli" anywhere in their message.
---

# mxcli Docs Lookup

1. Use WebFetch to load the index:
   `https://huaiyukhaw.github.io/mxcli-llms/llms.txt`

2. Scan the index for sections and pages relevant to the user's question.

3. If the index blurbs are enough to answer — answer directly.

4. If the user's question needs full content (command syntax, options, examples), pick the most relevant page URL(s) from the index and WebFetch each one. Prefer the specific page over the full dump.

5. Answer the user's question based on what you fetched. Cite the page title so the user knows where the answer came from.

## Notes

- The index (`llms.txt`) is ~45 KB and fits comfortably in context — always start there.
- Individual pages are small; fetch up to 3 if the question spans multiple topics.
- If the question is broad enough to require more than 3 pages, fetch `https://huaiyukhaw.github.io/mxcli-llms/llms-full.txt` instead (the entire book as one Markdown file — ~960 KB, may truncate near the end).
- The docs are rebuilt daily. If the user reports stale content, check `https://huaiyukhaw.github.io/mxcli-llms/meta.json` for the current version stamp.
