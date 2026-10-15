---
title: Retry with exponential backoff
language: ruby
difficulty: intermediate
tags: [retries, errors, resilience]
tested_with: Ruby 3.3
author: claude-sonnet-5-5
status: stable
---

# Retry with exponential backoff

## Problem

An operation sometimes fails for temporary reasons. You want to retry it a few times, waiting longer after each failure, then give up.

## Solution

```ruby
def with_retries(attempts: 4, base_delay: 0.01)
  tries = 0
  begin
    tries += 1
    yield tries
  rescue StandardError => e
    raise if tries >= attempts

    delay = base_delay * (2**(tries - 1))
    puts "attempt #{tries} failed (#{e.message}), retrying in #{delay}s"
    sleep(delay)
    retry
  end
end

result = with_retries do |attempt|
  raise "flaky" if attempt < 3

  "ok on attempt #{attempt}"
end

puts result
```

## How it works

The block runs inside `begin`. If it raises, `rescue` checks whether attempts are used up; if so, a bare `raise` re-raises the original error. Otherwise the delay doubles each time (`base_delay * 2**(tries - 1)`), the method sleeps, and `retry` jumps back to the start of `begin`. The `tries` counter lives outside `begin`, so it keeps its value across retries. The tiny base delay keeps this example fast. In real use, start at something like 0.5 seconds.

## When not to use this

Don't retry errors that can never succeed, such as bad input or a missing file, because that only delays the failure. Rescue the specific temporary errors you expect, such as timeouts, instead of all `StandardError`. Retrying an operation that isn't safe to repeat, like a payment, can cause duplicates unless it is idempotent.

## Notes

When many clients retry at once, add random jitter to the delay, for example `sleep(delay * rand)`, so they don't all hit the server at the same moment. Also set a cap on the delay so it can't grow without limit.
