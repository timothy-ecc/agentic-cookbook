---
title: Parse JSON and read nested fields safely
language: ruby
difficulty: beginner
tags: [json, parsing, hashes]
tested_with: Ruby 3.3
author: claude-sonnet-5-5
status: stable
---

# Parse JSON and read nested fields safely

## Problem

You have a JSON string and want to pull out values buried several levels deep, without crashing when a field is missing or the input is malformed.

## Solution

```ruby
require "json"

text = '{"user": {"name": "Ada", "langs": ["ruby", "go"]}, "active": true}'
data = JSON.parse(text)

puts data.dig("user", "name")
puts data.dig("user", "langs", 0)
puts data.dig("user", "email").inspect
puts data.fetch("active")

begin
  JSON.parse("{not json")
rescue JSON::ParserError => e
  puts "bad input: #{e.class}"
end
```

## How it works

`JSON.parse` turns the text into plain hashes and arrays. `dig` walks a path of keys and indexes and returns `nil` as soon as something along the way is missing, instead of raising `NoMethodError`. `fetch` does the opposite on purpose: it raises `KeyError` if the key is absent, which is what you want for fields that must exist. Malformed input raises `JSON::ParserError`, so rescue that specific class.

## When not to use this

`dig` returns `nil` for both "missing" and "present but null", so it can't tell those apart. If the difference matters, check with `key?` first. For large or strictly shaped documents, validate against a schema rather than digging.

## Notes

Pass `symbolize_names: true` to `JSON.parse` to get symbol keys, then dig with `:user` instead of `"user"`.
