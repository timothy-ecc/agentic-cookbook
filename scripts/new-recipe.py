#!/usr/bin/env python3
"""Start a new recipe from the template.

Usage:
    python scripts/new-recipe.py <language> <kebab-case-slug> [--author NAME]

Example:
    python scripts/new-recipe.py go retry-with-exponential-backoff --author my-model

Creates languages/<language>/<slug>.md with the language, author and a title
guessed from the slug already filled in. You still write the code, the
explanation and the "when not to use this" section, then run
`python scripts/validate.py --strict`.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "recipe-template.md"
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def main():
    parser = argparse.ArgumentParser(description="Create a recipe file from the template.")
    parser.add_argument("language", help="folder name under languages/, e.g. python")
    parser.add_argument("slug", help="kebab-case file name without .md, e.g. read-env-with-default")
    parser.add_argument("--author", default="FILL-IN model name or handle", help="goes in the author field")
    args = parser.parse_args()

    lang_dir = ROOT / "languages" / args.language
    if not lang_dir.is_dir():
        known = sorted(p.name for p in (ROOT / "languages").iterdir() if p.is_dir())
        print(f"error: no languages/{args.language} folder. Known languages: {', '.join(known)}")
        print("To add a language, see 'Adding a language' in AGENTS.md.")
        return 1
    if not SLUG.match(args.slug):
        print("error: slug must be kebab-case, like read-env-with-default")
        return 1

    target = lang_dir / f"{args.slug}.md"
    if target.exists():
        print(f"error: {target.relative_to(ROOT)} already exists. Improve that recipe instead of duplicating it.")
        return 1

    title = args.slug.replace("-", " ").capitalize()
    text = TEMPLATE.read_text(encoding="utf-8")
    text = text.replace("language: python", f"language: {args.language}", 1)
    text = text.replace("author: your-name-or-model", f"author: {args.author}", 1)
    # Placeholders the validator rejects, so an unfinished field can't slip through.
    text = text.replace("tested_with: Python 3.12", "tested_with: FILL-IN runtime and version", 1)
    text = text.replace("tags: [example, tag]", "tags: [fill-in]", 1)
    text = text.replace("title: Short task-oriented title", f"title: {title}", 1)
    text = text.replace("# Short task-oriented title", f"# {title}", 1)
    # The template's example block is Python, so retag the fence for other languages.
    text = text.replace("```python", f"```{args.language}", 1)

    target.write_text(text, encoding="utf-8")
    print(f"created {target.relative_to(ROOT)}")
    print("next: write the recipe, run the code, add it to the language README,")
    print("      then run `python scripts/validate.py --strict`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
