---
title: Read a file line by line
language: python
difficulty: beginner
tags: [files, io, iteration]
tested_with: Python 3.13
author: claude-sonnet-5-5
status: stable
---

# Read a file line by line

## Problem

You have a text file, possibly a large one, and want to process it one line at a time without loading it all into memory.

## Solution

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "demo.txt"
    path.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")

    with path.open(encoding="utf-8") as f:
        for number, line in enumerate(f, start=1):
            print(number, line.rstrip("\n"))
```

## How it works

A file object is an iterator over its lines. Python reads from disk in buffered chunks and hands you one line per loop pass, so memory use stays flat however large the file is. The `with` block closes the file even if the loop raises. Passing `encoding` avoids depending on the platform's default.

## When not to use this

If you need random access (jump to line 10,000) or the whole file at once, use `path.read_text().splitlines()` or an index. For CSV or JSON Lines, use the `csv` or `json` module on each line instead of splitting by hand.

## Notes

Each `line` still ends with `"\n"`; `rstrip("\n")` removes only that, keeping other trailing whitespace.
