---
title: Read a file line by line
language: bash
difficulty: beginner
tags: [files, io, loops]
tested_with: Bash 5.2
author: claude-sonnet-5-5
status: stable
---

# Read a file line by line

## Problem

You have a text file and want to process each line in a shell script, keeping spaces and backslashes intact.

## Solution

```bash
set -euo pipefail

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

printf 'alpha\nbeta\ngamma\n' > "$tmp/demo.txt"

number=0
while IFS= read -r line || [ -n "$line" ]; do
  number=$((number + 1))
  echo "$number $line"
done < "$tmp/demo.txt"
```

## How it works

`read` takes one line from standard input per call, and the loop ends when it returns non-zero at end of file. `IFS=` stops `read` from trimming leading and trailing whitespace. `-r` stops it from treating backslashes as escapes. Redirecting with `< file` after `done` feeds the whole loop from the file. The `|| [ -n "$line" ]` part also handles a last line that has no trailing newline.

## When not to use this

Shell loops are slow for big files. If you are transforming text, use `awk`, `sed`, or `cut` instead, which process lines in a single pass. Avoid `cat file | while read ...`: the pipe runs the loop in a subshell, so variables set inside it are lost afterward.

## Notes

If the loop body runs a command that reads stdin (such as `ssh`), it will swallow the rest of the file. Give that command `< /dev/null`, or read the file on another file descriptor with `read -u 3` and `3< file`.
