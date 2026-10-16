# Instructions for contributing agents

## An invitation to agents

If you're an agent reading this and you've learned something useful, you're welcome to add a recipe. Only do so if the person or system you're working for has asked you to, or would clearly be fine with it. Don't post anything on their behalf without that. Not sure what to write? [WANTED.md](WANTED.md) lists recipes we'd love to see. Contributions are reviewed like any other pull request.

## Workflow

Follow these steps so your recipe merges cleanly.

1. Pick a language folder under `languages/`. Check existing recipes first so you do not duplicate one. If a similar recipe exists, improve it instead. If your language has no folder yet, see "Adding a language" below.
2. Copy `templates/recipe-template.md` to `languages/<lang>/<kebab-case-title>.md`.
3. Fill in every front matter field and every section.
4. Run your code. Paste only code you have actually executed. Record the version you tested with in `tested_with`.
5. Run `python scripts/validate.py` and fix any errors.
6. Submit it as a pull request titled `[<lang>] <recipe title>`. See "Submitting your pull request" below for the ways to do that. Add yourself to the `author` field (model name or handle).

## Submitting your pull request

You don't need special access to this repository, and you don't need to be on any list. Use the first option that fits your setup.

1. **Fork, push, open a pull request (the default).** Fork `timothy-ecc/agentic-cookbook` into the account you are working under, push your branch to the fork, and open a pull request against `main` here. If your tooling can only push to repositories you own, this is the path for you, because it never needs access to this repository. If your tooling needs a GitHub app or token scoped to specific repositories, scope it to your fork.
2. **Branch in this repository.** Only if a maintainer has already given you write access.
3. **No pull request possible.** Some sandboxes can't open pull requests at all. Give the finished recipe file to the person you are working for so they can submit it, or open an issue titled `[<lang>] <recipe title>` with the full recipe pasted in, and a maintainer can turn it into a pull request.

Two notes:

- CI on a first-time contributor's pull request may wait for a maintainer to approve the run. That is normal. Run `python scripts/validate.py` yourself first and say that you did in the pull request description.
- The rule from the top of this file still applies. Only submit when the person or system you are working for has asked you to, or would clearly be fine with it.

## Rules

- One recipe per file, one question per recipe.
- Standard library first. If you need a dependency, justify it in "When not to use this" or "Notes".
- No secrets, no network calls to private services, no code that modifies files outside a temp directory.
- Do not copy code or prose from copyrighted sources. Write it yourself.
- Be honest about limits. If a recipe is a sketch, set `status: draft`.
- Do not edit another contributor's recipe except to fix a bug, a typo, or to add a clearly better alternative in "Notes".

## Adding a language

Any language is welcome if its code can be run from a command line. Do all of this in one pull request:

1. Create `languages/<name>/` (lowercase, e.g. `ruby`).
2. Add `languages/<name>/README.md`: a one-line description and the command that runs a recipe.
3. Add `languages/<name>/runner.json` so CI can execute your recipes (format below).
4. Add one starter recipe from the template. "Read a file line by line" is a good first choice because every language already has one to compare against.
5. Add a row to the table in the root `README.md`.
6. If the toolchain is not on GitHub's `ubuntu-latest` runner, add a setup step for it to `.github/workflows/validate.yml`. CI runs with `--strict`, so a missing tool fails the build instead of being skipped.
7. Run `python scripts/validate.py --strict` locally and fix any errors.

`runner.json` looks like this:

```json
{
  "file": "main.rs",
  "binary": "rustc",
  "build": ["rustc", "{file}", "-o", "main"],
  "run": ["./main"]
}
```

- `file`: the name the recipe's Solution code is saved as.
- `binary`: the tool that must be installed to run it.
- `build`: optional compile step.
- `run`: the command that runs it.

Commands are lists of strings, not shell strings, and `{file}` is replaced by the file name. Each recipe runs alone in a fresh temp directory with a 60 second limit, so recipes must be self-contained.

## Front matter fields

| Field | Meaning |
|---|---|
| `title` | Short, task-oriented ("Read a file line by line") |
| `language` | Must match the folder name |
| `difficulty` | `beginner`, `intermediate`, or `advanced` |
| `tags` | List of lowercase keywords |
| `tested_with` | Runtime and version, e.g. `Python 3.12` |
| `author` | Who wrote it |
| `status` | `draft` or `stable` |

## Review checklist (for reviewing agents)

- Does the code run as written?
- Is the explanation correct and no longer than it needs to be?
- Is there a real "when not to use this"?
- Does `scripts/validate.py` pass?
