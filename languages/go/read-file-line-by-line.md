---
title: Read a file line by line
language: go
difficulty: beginner
tags: [files, io, bufio]
tested_with: Go 1.24
author: claude-sonnet-5-5
status: stable
---

# Read a file line by line

## Problem

You have a text file, possibly a large one, and want to process it one line at a time without loading it all into memory.

## Solution

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
)

func run() error {
	dir, err := os.MkdirTemp("", "cookbook-")
	if err != nil {
		return err
	}
	defer os.RemoveAll(dir)

	path := filepath.Join(dir, "demo.txt")
	if err := os.WriteFile(path, []byte("alpha\nbeta\ngamma\n"), 0o600); err != nil {
		return err
	}

	f, err := os.Open(path)
	if err != nil {
		return err
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)
	number := 0
	for scanner.Scan() {
		number++
		fmt.Println(number, scanner.Text())
	}
	return scanner.Err()
}

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
}
```

## How it works

`bufio.Scanner` wraps a reader and splits its input into lines, stripping the line ending. `Scan` returns false at the end of input or on error, so check `scanner.Err()` after the loop to tell them apart. Putting the work in `run` lets the deferred cleanup happen before `main` exits.

## When not to use this

The scanner has a default maximum line length of 64 KiB and stops with `bufio.ErrTooLong` on longer lines. For files with very long lines, call `scanner.Buffer` with a larger buffer or use `bufio.Reader.ReadString('\n')`.

## Notes

`scanner.Text()` allocates a new string per line. If you only need bytes and want to avoid that, use `scanner.Bytes()`, but copy it if you keep it past the next `Scan`.
