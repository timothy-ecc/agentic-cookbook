---
title: Read a file line by line
language: javascript
difficulty: beginner
tags: [files, io, streams]
tested_with: Node.js 22
author: claude-sonnet-5-5
status: stable
---

# Read a file line by line

## Problem

You have a text file, possibly a large one, and want to process it one line at a time without loading it all into memory.

## Solution

```javascript
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const readline = require("node:readline");

async function main() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "cookbook-"));
  const file = path.join(dir, "demo.txt");
  fs.writeFileSync(file, "alpha\nbeta\ngamma\n");

  try {
    const rl = readline.createInterface({
      input: fs.createReadStream(file, { encoding: "utf8" }),
      crlfDelay: Infinity,
    });

    let number = 0;
    for await (const line of rl) {
      number += 1;
      console.log(number, line);
    }
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

main();
```

## How it works

`createReadStream` reads the file in chunks, and `readline` splits those chunks into lines. The interface is async iterable, so `for await` gives you one line at a time with backpressure handled for you. `crlfDelay: Infinity` makes `\r\n` count as a single line break.

## When not to use this

For small files, `fs.readFileSync(file, "utf8").split("\n")` is simpler. If you only need the stream of lines inside a pipeline, consider `stream.Readable` with a transform instead.

## Notes

Lines come without the trailing newline. A final line with no newline at the end is still delivered.
