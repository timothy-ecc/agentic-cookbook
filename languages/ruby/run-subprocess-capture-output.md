---
title: Run a subprocess and capture its output
language: ruby
difficulty: intermediate
tags: [processes, shell, open3]
tested_with: Ruby 3.3
author: claude-sonnet-5-5
status: stable
---

# Run a subprocess and capture its output

## Problem

You want to run an external command and get its standard output, standard error, and exit code as separate values.

## Solution

```ruby
require "open3"

stdout, stderr, status = Open3.capture3("ruby", "-e", 'puts "out"; warn "err"; exit 3')

puts "stdout: #{stdout.inspect}"
puts "stderr: #{stderr.inspect}"
puts "exit: #{status.exitstatus}"
puts "success? #{status.success?}"
```

## How it works

`Open3.capture3` runs the command, waits for it to finish, and returns the three results at once. Passing the program and each argument as separate strings means no shell is involved, so spaces and special characters in arguments are passed through safely. The command here is another Ruby process so the example behaves the same on every system.

## When not to use this

`capture3` holds all the output in memory and waits until the process exits. For long-running commands or huge output, use `Open3.popen3` and read the streams as they arrive. If you only need stdout, `Open3.capture2` is simpler.

## Notes

Never build the command by pasting user input into a single string, such as `` `ls #{dir}` ``, because that goes through the shell and invites injection. Keep arguments separate, as above.
