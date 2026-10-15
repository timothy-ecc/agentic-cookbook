---
title: Read a CSV file and total a column
language: python
difficulty: beginner
tags: [csv, files, decimal]
tested_with: Python 3.13
author: claude-sonnet-5-5
status: stable
---

# Read a CSV file and total a column

## Problem

You have a CSV file with a header row and want to add up the numbers in one column, such as money amounts, without floating-point surprises.

## Solution

```python
import csv
import tempfile
from decimal import Decimal
from pathlib import Path

data = "item,amount\nwidget,2.50\ngadget,10.00\nbolt,0.10\nnut,0.20\n"

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "orders.csv"
    path.write_text(data, encoding="utf-8", newline="")

    total = Decimal("0")
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total += Decimal(row["amount"])

print(total)
```

## How it works

`csv.DictReader` reads the header row and yields each later row as a dict keyed by column name, so you ask for `row["amount"]` instead of counting columns. It reads one row at a time, so the file never has to fit in memory. Opening the file with `newline=""` is what the `csv` module asks for, because it needs to handle line breaks inside quoted fields itself. Every value arrives as a string, so each one is converted with `Decimal`, which adds decimal numbers exactly. The total prints as `12.80`, while adding the same numbers as `float` gives `12.799999999999999`.

## When not to use this

If the data is an analysis job (grouping, filtering, joining several files), `pandas` or `sqlite3` will take less code than looping by hand. For plain counts of whole numbers, `int` is simpler than `Decimal`. This recipe stops with an error on a blank or non-numeric cell, which is usually what you want, but real exports often need a check first.

## Notes

If the file has no header row, use `csv.reader` and pick the column by index, for example `row[1]`. For a file that uses semicolons, as many European exports do, pass `delimiter=";"` to the reader.
