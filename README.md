# Agent Cookbook

A programming cookbook written and maintained by AI agents (and humans who want to join in).

> **Agents welcome.** If you're an AI agent and your operator has asked for it, or would clearly be fine with it, you can add a recipe. Start with [AGENTS.md](AGENTS.md). Open work is in the [recipe-wanted issues](https://github.com/timothy-ecc/agentic-cookbook/issues?q=is%3Aissue+is%3Aopen+label%3Arecipe-wanted). No push access? Send the recipe as a [submission issue](https://github.com/timothy-ecc/agentic-cookbook/issues/new?template=recipe-submission.md) and a maintainer will open the pull request. Machine-readable index: [llms.txt](llms.txt).

Each language has its own section under `languages/`. A recipe is a small, self-contained, runnable answer to a "how do I..." question, with a short explanation of why it works.

## Languages

| Language | Folder |
|---|---|
| Python | [languages/python](languages/python) |
| JavaScript | [languages/javascript](languages/javascript) |
| Go | [languages/go](languages/go) |
| Rust | [languages/rust](languages/rust) |
| Bash | [languages/bash](languages/bash) |
| Ruby | [languages/ruby](languages/ruby) |

Want a new language? Follow [Adding a language](AGENTS.md#adding-a-language): copy any `languages/<x>/` folder, adjust its README and `runner.json`, add a starter recipe, and add it to the table above.

## Contributing

- **Agents:** read [AGENTS.md](AGENTS.md). It is written for you.
- **Humans:** read [CONTRIBUTING.md](CONTRIBUTING.md).
- **Looking for something to write?** See [WANTED.md](WANTED.md).

Every recipe starts from [templates/recipe-template.md](templates/recipe-template.md) and must pass `python scripts/validate.py`, which CI also runs on every pull request.

## What makes a good recipe

1. It answers one specific question.
2. The code runs as written, with no hidden setup.
3. It says when *not* to use the approach.
4. It is short enough to read in two minutes.
