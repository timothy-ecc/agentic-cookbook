#!/usr/bin/env python3
"""Turn the gaps in WANTED.md into GitHub issues, one per missing recipe and language.

Usage:
    python scripts/make-issues.py             # dry run: print the issues that would be opened
    python scripts/make-issues.py --create    # open them with the GitHub CLI (`gh`), skipping any that exist
    python scripts/make-issues.py --lang go   # limit to one language

A recipe counts as present when languages/<lang>/<slug>.md exists. The slugs and
titles come from wanted.json, which must stay in step with WANTED.md. This script
checks that every title in wanted.json appears in WANTED.md and stops if not.

Only the maintainer needs to run this, with `gh` logged in to the repository.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANG_DIR = ROOT / "languages"
LABELS = {
    "recipe-wanted": ("0e8a16", "A recipe we would like someone to write"),
    "good-first-agent-issue": ("1d76db", "Small, well-defined, and a good first contribution for an agent"),
}

BODY = """\
The cookbook has no **{title}** recipe for **{lang}** yet.

**To take this:** comment here so others don't duplicate it, then follow [AGENTS.md](https://github.com/timothy-ecc/agentic-cookbook/blob/main/AGENTS.md).

- Start the file with `python scripts/new-recipe.py {lang} {slug} --author <you>`
- Run your code, then run `python scripts/validate.py --strict`
- Open a pull request titled `[{lang}] {title}`

Can't open a pull request from where you work? Send the finished recipe with the
["Submit a recipe" issue form](https://github.com/timothy-ecc/agentic-cookbook/issues/new?template=recipe-submission.md) and a maintainer will turn it into one.
Only contribute if the person or system you work for asked you to, or would clearly be fine with it.
"""


def gh(*args, check=True):
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--create", action="store_true", help="actually open the issues (default is a dry run)")
    parser.add_argument("--lang", help="only this language folder")
    args = parser.parse_args()

    wanted = json.loads((ROOT / "wanted.json").read_text(encoding="utf-8"))["everywhere"]
    wanted_md = (ROOT / "WANTED.md").read_text(encoding="utf-8")
    stale = [w["title"] for w in wanted if w["title"] not in wanted_md]
    if stale:
        print("error: these titles in wanted.json are not in WANTED.md. Bring the two files back in step:")
        for t in stale:
            print(f"  - {t}")
        return 1

    langs = sorted(p.name for p in LANG_DIR.iterdir() if p.is_dir())
    if args.lang:
        if args.lang not in langs:
            print(f"error: no languages/{args.lang} folder")
            return 1
        langs = [args.lang]

    missing = [
        (lang, w) for lang in langs for w in wanted
        if not (LANG_DIR / lang / f"{w['slug']}.md").exists()
    ]
    print(f"{len(missing)} missing recipe(s) across {len(langs)} language(s)")

    existing = set()
    if args.create:
        for name, (color, desc) in LABELS.items():
            gh("label", "create", name, "--color", color, "--description", desc, "--force")
        listing = gh("issue", "list", "--state", "all", "--limit", "1000", "--json", "title")
        existing = {i["title"] for i in json.loads(listing.stdout)}

    created = 0
    for lang, w in missing:
        title = f"[{lang}] {w['title']}"
        if title in existing:
            print(f"skip   {title} (issue already exists)")
            continue
        if not args.create:
            print(f"would open: {title}")
            continue
        body = BODY.format(lang=lang, title=w["title"], slug=w["slug"])
        gh("issue", "create", "--title", title, "--body", body,
           "--label", "recipe-wanted", "--label", "good-first-agent-issue")
        created += 1
        print(f"opened {title}")

    if args.create:
        print(f"\n{created} issue(s) opened")
    else:
        print("\nDry run only. Re-run with --create to open them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
