"""Report unbalanced direction controls and review-worthy overrides in UTF-8 text."""

import argparse
import json
import sys
import unicodedata
from pathlib import Path

ISOLATES = frozenset("\u2066\u2067\u2068")
EMBEDDINGS = frozenset("\u202a\u202b\u202d\u202e")
OVERRIDES = frozenset("\u202d\u202e")
PDF = "\u202c"
PDI = "\u2069"


def finding(kind, line, column, char):
    return {
        "kind": kind, "line": line, "column": column,
        "codepoint": f"U+{ord(char):04X}", "name": unicodedata.name(char),
    }


def audit(text):
    findings = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        stack = []
        isolate_positions = []
        for column, char in enumerate(line, start=1):
            if char in OVERRIDES:
                findings.append(finding("override", line_number, column, char))
            if char in ISOLATES or char in EMBEDDINGS:
                if char in ISOLATES:
                    isolate_positions.append(len(stack))
                stack.append((char, column))
            elif char == PDF:
                if stack and stack[-1][0] in EMBEDDINGS:
                    stack.pop()
                else:
                    findings.append(finding("unmatched-closer", line_number, column, char))
            elif char == PDI:
                if not isolate_positions:
                    findings.append(finding("unmatched-closer", line_number, column, char))
                else:
                    isolate = isolate_positions.pop()
                    for opener, location in stack[isolate + 1:]:
                        findings.append(finding("unclosed-opener", line_number, location, opener))
                    del stack[isolate:]
        for opener, location in stack:
            findings.append(finding("unclosed-opener", line_number, location, opener))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="A UTF-8 text file, or - for UTF-8 standard input.")
    args = parser.parse_args()
    try:
        data = sys.stdin.buffer.read() if args.file == "-" else Path(args.file).read_bytes()
        findings = audit(data.decode("utf-8-sig"))
    except (OSError, UnicodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(findings, indent=2))
    return int(bool(findings))


if __name__ == "__main__":
    raise SystemExit(main())
