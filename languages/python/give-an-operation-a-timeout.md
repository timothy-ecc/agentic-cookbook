---
title: Give an operation a timeout
language: python
difficulty: intermediate
tags: [timeouts, asyncio, resilience]
tested_with: Python 3.13
author: claude-sonnet-5-5
status: stable
---

# Give an operation a timeout

## Problem

An operation might hang or take far too long. You want to wait a fixed time for it, then give up and carry on.

## Solution

```python
import asyncio


async def work(seconds):
    await asyncio.sleep(seconds)  # stands in for a network call
    return f"finished after {seconds}s"


async def main():
    for seconds in (0.1, 2):
        try:
            async with asyncio.timeout(0.5):
                print(await work(seconds))
        except TimeoutError:
            print(f"gave up on the {seconds}s job after 0.5s")


asyncio.run(main())
```

## How it works

`asyncio.timeout(0.5)` starts a 0.5 second clock for the `async with` block. If the block is still running when the clock runs out, asyncio cancels it at its current `await` and raises `TimeoutError` just outside the block. The cancellation also runs any cleanup in the cancelled code, such as `finally` blocks. The fast job finishes in time and the slow one is stopped after half a second instead of two seconds.

## When not to use this

`asyncio.timeout` can only interrupt code at an `await`. A blocking call such as `time.sleep(2)` or a long loop inside the block can't be stopped, and the timeout fires only after it returns. It also needs Python 3.11 or newer; on older versions use `asyncio.wait_for(work(seconds), 0.5)`.

For a blocking job you must be able to kill, run it as a separate process, for example `subprocess.run(cmd, timeout=5)`, which terminates the child and raises `subprocess.TimeoutExpired`.

## Notes

With threads, `future.result(timeout=5)` stops your waiting after 5 seconds, but the thread keeps running in the background, because Python has no safe way to kill a thread. Treat that as "stop waiting", not "stop working".
