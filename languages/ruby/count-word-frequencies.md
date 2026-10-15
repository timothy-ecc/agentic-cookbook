---
title: Count word frequencies
language: ruby
difficulty: beginner
tags: [text, counting, enumerable]
tested_with: Ruby 3.3
author: claude-sonnet-5-5
status: stable
---

# Count word frequencies

## Problem

You have a block of text and want the most common words, with a stable order when counts tie.

## Solution

```ruby
text = "the quick brown fox jumps over the lazy dog the fox"

counts = text.downcase.scan(/[a-z']+/).tally
top = counts.sort_by { |word, count| [-count, word] }.first(5)

top.each { |word, count| puts "#{word} #{count}" }
```

## How it works

`scan` pulls out every run of letters and apostrophes, which splits on spaces and punctuation. `tally` counts how many times each item appears and returns a hash. Sorting by `[-count, word]` puts the highest counts first and breaks ties alphabetically, so the output is the same on every run.

## When not to use this

The regex only handles plain English letters, so accented or non-Latin words are dropped. Use `/[\p{L}']+/` for Unicode letters. For text too big for memory, read it line by line and add to a counts hash as you go instead of scanning one huge string.

## Notes

`counts.max_by(5) { |_, c| c }` gets the top five without a full sort, but its tie order isn't guaranteed.
