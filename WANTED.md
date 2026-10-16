# Recipes wanted

Looking for something to write? Pick anything here. Recipes must run offline, so no network calls.

**To claim one:** each gap has an issue titled `[<lang>] <recipe title>` and labeled `recipe-wanted`. Comment on it to claim it. If there isn't an issue yet, open a draft pull request or an issue with that title so others don't duplicate it. When a recipe exists in every language folder, delete its line from this file in the same pull request.

**For maintainers:** the list below is mirrored in `wanted.json`. After you change either, run `python scripts/make-issues.py` to preview the issues for missing recipes, and `python scripts/make-issues.py --create` to open them with the GitHub CLI.

## Ideas for every language

Each of these is wanted in each language folder, and any one is a good first contribution.

- Parse JSON from a string and read nested fields safely
- Read a CSV file and total a column
- Count word frequencies in a text and print the top 5
- Hash a file with SHA-256 without loading it all into memory
- Run a subprocess and capture its output and exit code
- Parse command-line arguments with flags and defaults
- Read an environment variable with a default
- Retry a flaky operation with exponential backoff
- Run several tasks concurrently and collect their results
- Give an operation a timeout
- Match text with a regex using named groups
- Format and parse dates, including time zones
- Write to a temporary file and clean it up reliably

## New languages wanted

TypeScript, Java, Kotlin, C, C++, Zig, Swift, PHP, Lua, Haskell, SQL (via SQLite), and anything else you can run from a command line. See "Adding a language" in [AGENTS.md](AGENTS.md).
