#!/usr/bin/env python3
"""Write the one-line dad joke entry for The One-Liner Groan-Off.

Reads the output directory from the MAKEFUN_OUTPUT_DIR environment
variable and writes entry.txt there as UTF-8 with no trailing newline.
"""

import os
import sys

ENTRY = "I told the iron to calm down. It said it just presses on."


class BlankError(ValueError):
    """Raised when the entry is empty or whitespace only."""


class MultiLineError(ValueError):
    """Raised when the entry contains a line break."""


class LengthError(ValueError):
    """Raised when the entry is outside the 1-140 character range."""


def validate(entry):
    if not entry.strip():
        raise BlankError("entry must not be blank")
    if "\n" in entry or "\r" in entry:
        raise MultiLineError("entry must be a single line with no line breaks")
    if not 1 <= len(entry) <= 140:
        raise LengthError(
            "entry must be 1-140 characters, got %d" % len(entry)
        )


def verify_written(path, expected_bytes):
    with open(path, "rb") as f:
        actual = f.read()
    if actual != expected_bytes:
        raise ValueError(
            "read-back verification failed for %s: wrote %d bytes, "
            "read back %d bytes" % (path, len(expected_bytes), len(actual))
        )


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    try:
        validate(ENTRY)
    except BlankError as exc:
        print("error: blank entry: %s" % exc, file=sys.stderr)
        return 1
    except MultiLineError as exc:
        print("error: multi-line entry: %s" % exc, file=sys.stderr)
        return 1
    except LengthError as exc:
        print("error: bad entry length: %s" % exc, file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    expected = ENTRY.encode("utf-8")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    try:
        verify_written(path, expected)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
