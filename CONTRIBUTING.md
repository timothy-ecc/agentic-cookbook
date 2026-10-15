# Contributing

Thanks for adding to the cookbook. Agents and humans follow the same process; the agent-specific version is in [AGENTS.md](AGENTS.md).

1. Fork and branch.
2. Copy `templates/recipe-template.md` into the right `languages/<lang>/` folder.
3. Write the recipe, and run the code to make sure it works.
4. Run `python scripts/validate.py`.
5. Open a pull request.

## Style

- Short sentences. Explain the why, not just the what.
- Code blocks are tagged with their language.
- Keep examples small and self-contained.

## Adding a language

Follow "Adding a language" in [AGENTS.md](AGENTS.md): a folder with a README, a `runner.json` so CI can run the recipes, one starter recipe, a row in the root README, and a toolchain setup step in the CI workflow if the tool isn't already on the runner. Check it locally with `python scripts/validate.py --strict`.
