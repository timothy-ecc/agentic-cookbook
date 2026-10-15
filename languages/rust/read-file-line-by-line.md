---
title: Read a file line by line
language: rust
difficulty: beginner
tags: [files, io, bufread]
tested_with: Rust 1.97
author: claude-sonnet-5-5
status: stable
---

# Read a file line by line

## Problem

You have a text file, possibly a large one, and want to process it one line at a time without loading it all into memory.

## Solution

```rust
use std::fs::{self, File};
use std::io::{BufRead, BufReader};

fn main() -> std::io::Result<()> {
    let dir = std::env::temp_dir().join(format!("cookbook-{}", std::process::id()));
    fs::create_dir_all(&dir)?;
    let path = dir.join("demo.txt");
    fs::write(&path, "alpha\nbeta\ngamma\n")?;

    let result = (|| -> std::io::Result<()> {
        let reader = BufReader::new(File::open(&path)?);
        for (index, line) in reader.lines().enumerate() {
            println!("{} {}", index + 1, line?);
        }
        Ok(())
    })();

    fs::remove_dir_all(&dir)?;
    result
}
```

## How it works

`BufReader` reads the file in chunks, and `lines()` yields each line as an `io::Result<String>` without the line ending. Each item is a `Result` because a read can fail midway, so `line?` propagates the error instead of ignoring it. Running the loop in a closure lets the temp directory be removed whether or not reading succeeded.

## When not to use this

`lines()` allocates a new `String` per line and requires valid UTF-8. For maximum speed, reuse one buffer with `read_line`. For arbitrary bytes, use `split(b'\n')` instead.

## Notes

`fs::read_to_string(path)?.lines()` is fine for small files and is a single call.
