# Bidi Text Audit

Find invisible Unicode direction controls that can make text display in an unexpected order. The tool reports unmatched or unclosed directional isolates and embeddings, and flags directional overrides for review. Useful when preparing UTF-8 translations, subtitles, or documentation in mixed Arabic and English.

```sh
python bidi_audit.py path/to/translation.txt
python -m unittest -v
```

Use `-` to read UTF-8 from stdin. Output is JSON with one-based line and code-point column, Unicode code point and control name. Exit 0 means there are no findings, 1 means there are findings, and 2 means the input could not be read or decoded.

This is an explicit pairing check per line rather than a full implementation of the Unicode Bidirectional Algorithm. Controls that are syntactically valid can still warrant review. Arabic and Hebrew letters, ordinary directional marks, and well-paired isolates are accepted. The tool never rewrites the input.

Python 3.10 or newer. No dependencies. Licensed under 0BSD. Initial implementation prepared with assistance from OpenAI Codex.
