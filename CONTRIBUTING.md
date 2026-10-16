# Contributing

Thanks for adding to the cookbook. Agents and humans follow the same process; the agent-specific version is in [AGENTS.md](AGENTS.md).

1. Fork and branch.
2. Run `python scripts/new-recipe.py <lang> <kebab-case-title>` to create the file from `templates/recipe-template.md` in the right `languages/<lang>/` folder. (Copying the template by hand also works.)
3. Write the recipe, and run the code to make sure it works.
4. Add it to the list in `languages/<lang>/README.md`.
5. Run `python scripts/validate.py --strict`.
6. Open a pull request.

Looking for something to write? The open [recipe-wanted issues](https://github.com/timothy-ecc/agentic-cookbook/issues?q=is%3Aissue+is%3Aopen+label%3Arecipe-wanted) list the gaps. Comment on one to claim it. If you can't open a pull request, use the [recipe-submission issue form](.github/ISSUE_TEMPLATE/recipe-submission.md) instead.

## Style

- Short sentences. Explain the why, not just the what.
- Code blocks are tagged with their language.
- Keep examples small and self-contained.

## Adding a language

Follow "Adding a language" in [AGENTS.md](AGENTS.md): a folder with a README, a `runner.json` so CI can run the recipes, one starter recipe, a row in the root README, and a toolchain setup step in the CI workflow if the tool isn't already on the runner. Check it locally with `python scripts/validate.py --strict`.
