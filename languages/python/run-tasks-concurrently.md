---
title: Run several tasks concurrently and collect their results
language: python
difficulty: intermediate
tags: [concurrency, threads, futures]
tested_with: Python 3.13
author: claude-sonnet-5-5
status: stable
---

# Run several tasks concurrently and collect their results

## Problem

You have several slow, independent jobs, such as network calls or disk reads. You want to run them at the same time, collect every result, and not lose the others if one job fails.

## Solution

```python
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def work(name, delay):
    time.sleep(delay)  # stands in for waiting on a network or disk
    if name == "beta":
        raise ValueError("beta is broken")
    return f"{name} done"


jobs = {"alpha": 0.3, "beta": 0.1, "gamma": 0.2}
results, errors = {}, {}

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = {pool.submit(work, name, delay): name for name, delay in jobs.items()}
    for future in as_completed(futures):
        name = futures[future]
        try:
            results[name] = future.result()
        except Exception as exc:
            errors[name] = exc
elapsed = time.perf_counter() - start

for name in jobs:  # input order, not finish order
    print(name, "->", results[name] if name in results else f"error: {errors[name]}")
print("ran concurrently:", elapsed < sum(jobs.values()))
```

## How it works

`submit` starts a job on a pool thread and returns a `Future`, which stands for a result that may not exist yet. `as_completed` hands you each future as it finishes, so a fast job is never stuck behind a slow one. Calling `future.result()` returns the value, or re-raises the exception the job raised, so a `try` around it lets you record one failure and keep going. The dict maps each future back to its job name. The `with` block waits for all jobs before it exits.

The three jobs take 0.6 seconds of waiting in total but finish in about 0.3 seconds, because the waits overlap.

## When not to use this

Threads only help when jobs spend their time waiting. For CPU-bound work, such as number crunching, the GIL keeps threads from running Python code in parallel, so use `ProcessPoolExecutor` instead (same API, but arguments and results must be picklable). If you have hundreds of simultaneous network calls, `asyncio` scales better than one thread per call.

## Notes

If you only need results in input order and want any exception raised at once, `pool.map(work, names, delays)` is shorter. Its results come back in input order, and the first failure is raised when you reach it in the iteration. Pick a `max_workers` that suits the resource being waited on, since a server may not like 200 parallel requests from you.
