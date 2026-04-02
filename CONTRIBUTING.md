# Contributing

## Development

Install dependencies with [uv](https://docs.astral.sh/uv/getting-started/installation/):

    uv sync

Run tests:

    uv run pytest

Run linters:

    uv run pre-commit run -a

Install the pre-commit hooks (runs automatically on each commit):

    uv run pre-commit install --hook-type commit-msg

Commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) format,
e.g. `feat: add new command` or `fix: handle missing config file`. This is enforced by the
pre-commit hook above.

## Releasing

1. Run `cz bump` to update the version and changelog:

       uv run cz bump

   This will increment the version in `pyproject.toml` based on the commit history since the
   last release, append the new section to `CHANGELOG.md`, and create a git tag.

2. Push the commit and tag:

       git push origin master --tags

3. Create a GitHub release for the new tag. The `pypi-publish` workflow will automatically
   build and publish the package to PyPI when the release is published.
