---
title: Read a file line by line
language: ruby
difficulty: beginner
tags: [files, io, iteration]
tested_with: Ruby 3.3
author: claude-sonnet-5-5
status: stable
---

# Read a file line by line

## Problem

You have a text file, possibly a large one, and want to process it one line at a time without loading it all into memory.

## Solution

```ruby
require "tmpdir"

Dir.mktmpdir do |dir|
  path = File.join(dir, "demo.txt")
  File.write(path, "alpha\nbeta\ngamma\n")

  File.foreach(path).with_index(1) do |line, number|
    puts "#{number} #{line.chomp}"
  end
end
```

## How it works

`File.foreach` opens the file, yields one line at a time, and closes it when done. Without a block it returns an enumerator, which is what lets `with_index(1)` number the lines starting at 1. Because lines are read as you go, memory use stays flat for any file size. `Dir.mktmpdir` with a block deletes the directory afterwards.

## When not to use this

If you need the whole file at once, `File.readlines(path, chomp: true)` is shorter. For CSV or JSON Lines, use the `csv` or `json` libraries on each line instead of splitting by hand.

## Notes

Each `line` keeps its trailing newline, so call `chomp` when you print or compare. You can also pass `chomp: true` to `File.foreach` to have it done for you.
