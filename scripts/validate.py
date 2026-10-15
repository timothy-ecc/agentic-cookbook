#!/usr/bin/env python3
"""Validate cookbook recipes.

Usage:
    python scripts/validate.py            # structure checks only
    python scripts/validate.py --run      # also run each recipe's Solution code
    python scripts/validate.py --strict   # like --run, but fail if a toolchain is missing (use in CI)

Every language folder must contain a runner.json describing how to run its recipes:

    {
      "file": "main.rs",                          # name the Solution code is saved as
      "binary": "rustc",                          # tool that must be installed
      "build": ["rustc", "{file}", "-o", "main"], # optional compile step
      "run": ["./main"]                           # command that runs the recipe
    }

"{file}" in a command is replaced by the file name. Commands are lists, not shell strings.
Exit code is 0 when everything passes, 1 otherwise.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANG_DIR = ROOT / "languages"

FIELDS = ["title", "language", "difficulty", "tags", "tested_with", "author", "status"]
DIFFICULTIES = {"beginner", "intermediate", "advanced"}
STATUSES = {"draft", "stable"}
SECTIONS = ["Problem", "Solution", "How it works", "When not to use this"]
FILENAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")
FENCE = re.compile(r"^```(\w*)[^\n]*\n(.*?)^```", re.S | re.M)

RUNNER_REQUIRED = {"file", "binary", "run"}
RUNNER_OPTIONAL = {"build"}


def parse_front_matter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, text[m.end():]


def solution_code(body):
    m = re.search(r"^##\s+Solution\s*$(.*?)(?=^##\s|\Z)", body, re.S | re.M)
    if not m:
        return None
    block = FENCE.search(m.group(1))
    return block.group(2) if block else None


def is_command(value):
    return isinstance(value, list) and value and all(isinstance(p, str) and p for p in value)


def load_runner(lang_path):
    """Read languages/<lang>/runner.json. Returns (runner, list of errors)."""
    path = lang_path / "runner.json"
    if not path.exists():
        return None, ["missing runner.json (see 'Adding a language' in AGENTS.md)"]
    try:
        runner = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return None, [f"runner.json is not valid JSON: {e}"]
    if not isinstance(runner, dict):
        return None, ["runner.json must be a JSON object"]

    errors = []
    for key in sorted(RUNNER_REQUIRED - runner.keys()):
        errors.append(f"runner.json: missing '{key}'")
    for key in sorted(runner.keys() - RUNNER_REQUIRED - RUNNER_OPTIONAL):
        errors.append(f"runner.json: unknown key '{key}'")
    for key in ("file", "binary"):
        if key in runner and not (isinstance(runner[key], str) and runner[key]):
            errors.append(f"runner.json: '{key}' must be a non-empty string")
    if "file" in runner and isinstance(runner["file"], str) and "/" in runner["file"]:
        errors.append("runner.json: 'file' must be a plain file name")
    for key in ("run", "build"):
        if key in runner and not is_command(runner[key]):
            errors.append(f"runner.json: '{key}' must be a non-empty list of strings")
    return (None if errors else runner), errors


def check_recipe(path, lang):
    errors = []
    text = path.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text)

    if not FILENAME.match(path.name):
        errors.append("file name must be kebab-case, e.g. read-a-file.md")
    if meta is None:
        return errors + ["missing front matter (--- block at top of file)"]

    for field in FIELDS:
        if not meta.get(field):
            errors.append(f"front matter: missing or empty '{field}'")

    if meta.get("language") and meta["language"] != lang:
        errors.append(f"front matter: language '{meta['language']}' does not match folder '{lang}'")
    if meta.get("difficulty") and meta["difficulty"] not in DIFFICULTIES:
        errors.append(f"front matter: difficulty must be one of {sorted(DIFFICULTIES)}")
    if meta.get("status") and meta["status"] not in STATUSES:
        errors.append(f"front matter: status must be one of {sorted(STATUSES)}")

    tags = meta.get("tags", "")
    if tags:
        if not (tags.startswith("[") and tags.endswith("]")) or not tags[1:-1].strip():
            errors.append("front matter: tags must look like [one, two]")
        elif tags != tags.lower():
            errors.append("front matter: tags must be lowercase")

    for section in SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", body, re.M):
            errors.append(f"missing section '## {section}'")

    for fence in FENCE.finditer(body):
        if not fence.group(1):
            errors.append("a code block has no language tag")
            break

    if solution_code(body) is None:
        errors.append("no code block found under '## Solution'")

    return errors


def run_recipe(path, runner, strict):
    """Run the Solution code in a temp dir. Returns (error or None, skipped flag)."""
    binary = runner["binary"]
    if shutil.which(binary) is None:
        if strict:
            return f"'{binary}' is not installed (add a setup step to .github/workflows/validate.yml)", False
        return None, True

    _, body = parse_front_matter(path.read_text(encoding="utf-8"))
    code = solution_code(body)
    if code is None:
        return "no Solution code to run", False

    filename = runner["file"]

    def fill(cmd):
        return [part.replace("{file}", filename) for part in cmd]

    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / filename).write_text(code, encoding="utf-8")
        for label in ("build", "run"):
            cmd = runner.get(label)
            if not cmd:
                continue
            try:
                result = subprocess.run(fill(cmd), cwd=tmp, capture_output=True, text=True, timeout=60)
            except FileNotFoundError:
                return f"{label} command not found: {cmd[0]}", False
            except subprocess.TimeoutExpired:
                return f"{label} timed out after 60s", False
            if result.returncode != 0:
                return f"{label} failed (exit {result.returncode}):\n{result.stderr.strip()}", False
    return None, False


def main():
    args = sys.argv[1:]
    strict = "--strict" in args
    do_run = strict or "--run" in args
    failures = 0
    checked = 0
    skipped = 0

    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")

    if not LANG_DIR.is_dir():
        print("error: languages/ directory not found")
        return 1

    for lang_path in sorted(p for p in LANG_DIR.iterdir() if p.is_dir()):
        lang = lang_path.name
        if not (lang_path / "README.md").exists():
            print(f"FAIL languages/{lang}: missing README.md")
            failures += 1
        if f"languages/{lang}" not in root_readme:
            print(f"FAIL languages/{lang}: not listed in the root README")
            failures += 1

        runner, runner_errors = load_runner(lang_path)
        for e in runner_errors:
            print(f"FAIL languages/{lang}: {e}")
            failures += 1

        recipes = sorted(p for p in lang_path.glob("*.md") if p.name != "README.md")
        if not recipes:
            print(f"FAIL languages/{lang}: needs at least one recipe")
            failures += 1

        for recipe in recipes:
            checked += 1
            rel = recipe.relative_to(ROOT)
            errors = check_recipe(recipe, lang)
            if do_run and runner and not errors:
                err, was_skipped = run_recipe(recipe, runner, strict)
                if was_skipped:
                    skipped += 1
                    print(f"skip {rel}: '{runner['binary']}' is not installed here")
                elif err:
                    errors.append(err)
            if errors:
                failures += 1
                print(f"FAIL {rel}")
                for e in errors:
                    print(f"     - {e}")
            else:
                print(f"ok   {rel}")

    print(f"\n{checked} recipe(s) checked, {failures} failure(s)" + (f", {skipped} not run" if skipped else ""))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
