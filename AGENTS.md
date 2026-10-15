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
6. Open a pull request titled `[<lang>] <recipe title>`. Add yourself to the `author` field (model name or handle).

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
