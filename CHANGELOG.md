## 1.1.0 (2026-04-01)

### Features

- Add virtualenv-style prompt prefix showing the active mozconfig name (`BUILDWITH_SHOW_PROMPT`)

### Bug Fixes

- Unset `MOZCONFIG` when removing the currently active mozconfig

### CI

- Switch from Travis CI to GitHub Actions
- Add pre-commit with ruff linting and formatting

### Chores

- Switch from setuptools to uv
- Update minimum Python version to 3.9
- Add commitizen for changelog management and conventional commits enforcement

## 1.0.0 (2021-03-06)

### Features

- Support Python 3; drop Python 2

### Chores

- Switch from Travis CI to GitHub Actions

## 0.5.0 (2016-08-22)

### Features

- Make the buildwith export command configurable via `BUILDWITH_COMMAND`
- Echo the mozconfig path as part of the default build command

### Bug Fixes

- Quote `$BUILDWITH_HOME` to handle paths with spaces
- Use `subprocess.call` to improve command-line handling

## 0.4.0 (2016-05-15)

### Features

- Show usage when config name isn't provided to `buildwith`

### Bug Fixes

- Explicit clobbering when writing `.active` file

## 0.3.0 (2013-09-18)

### Features

- Keep track of activated mozconfig in file for persistence across shell sessions
- Append mozconfig name to `MOZ_OBJDIR` line in template

### Bug Fixes

- Fix tab completion for zsh
- Fix leftover `_virtualenvs` artifact
