---
title: Hash a file with SHA-256
language: ruby
difficulty: beginner
tags: [hashing, files, digest]
tested_with: Ruby 3.3
author: claude-sonnet-5-5
status: stable
---

# Hash a file with SHA-256

## Problem

You want the SHA-256 checksum of a file, including very large ones, without reading the whole thing into memory.

## Solution

```ruby
require "digest"
require "tmpdir"

Dir.mktmpdir do |dir|
  path = File.join(dir, "data.bin")
  File.binwrite(path, "hello world\n" * 100_000)

  digest = Digest::SHA256.file(path).hexdigest
  puts digest

  in_memory = Digest::SHA256.hexdigest(File.binread(path))
  puts digest == in_memory
end
```

## How it works

`Digest::SHA256.file` reads the file in chunks and feeds each one to the hash, so memory use doesn't grow with file size. `hexdigest` returns the result as a 64-character hex string. The last two lines hash the same bytes in one go and confirm the streamed result matches.

## When not to use this

SHA-256 is right for checking file integrity. Don't use it on its own to store passwords, since it is far too fast. Use a password hashing function such as bcrypt or Argon2 for that.

## Notes

To hash data as it arrives, for example from a download, create a `Digest::SHA256.new` and append chunks with `<<`, then call `hexdigest` at the end.
