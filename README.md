<h2 align="center">demo-tpl-py boilerplate setup guide</h2>

# DISCLAIMER
This boilerplate is used for demo purposes as part of education sessions/trainings. It doesn't include many aspects which should be present in production-ready project setup. However, all the tools around the sample code are configured properly and can be reused in projects.
# Software requirements
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) for Python version and dependency management. A separate Python installation is not required.
2. Install Bash (Git Bash on Windows) to run the project scripts.
3. Install [make](https://www.gnu.org/software/make/) CLI tool.
   ```bash
   # Debian-based Linux distro
   $ sudo apt update
   $ sudo apt install build-essential
   ```
   OR
   ```powershell
   # Windows
   $ choco install make
   ```
# Initial setup
1. Clone the repository.
2. Execute ```make build-all```.
# Build process digested into step by step
You can see all steps documented with the following command:
```bash
$ make help
```
## Install project dependencies
```bash
$ make init
```
This installs the Python version pinned in `.python-version` and creates `.venv`
with the runtime and development dependencies from `uv.lock`.
Without Make or Bash, run these commands directly:
```bash
$ uv python install
$ uv sync --locked
```
Use `uv run --locked <command>` to run tools in the project environment without
activating it. Configure your IDE to use the Python interpreter in `.venv`.

## Manage Python and dependencies
```bash
# Add runtime or development dependencies (updates pyproject.toml and uv.lock).
$ uv add <package>
$ uv add --dev <package>
# Upgrade locked dependencies within the declared version constraints.
$ uv lock --upgrade
$ uv sync --locked
# Change the project Python version.
$ uv python pin <version>
$ uv python install
$ uv sync --locked
```
Commit `.python-version`, `pyproject.toml`, and `uv.lock` when they change.
Docker builds use the same Python pin and lockfile; the production base image
installs only runtime dependencies, while the development image includes both groups.

## Install pre-commit hooks
Install `pre-commit` as a persistent uv tool:
```bash
$ uv tool install pre-commit
```
If the `pre-commit` command is not on your `PATH`, run `uv tool update-shell`
and restart your shell. Then install the Git hooks for this repository:
```bash
$ pre-commit install
```
## Format all files
```bash
$ make format
```
## Static code analysis of all files
* Runs all checks on your local OS
```bash
$ make check
```
* Runs all checks inside a Linux Docker container:
```bash
$ make docker-check
```
## Tests with coverage check
```bash
$ make test
```
# Solution
## Run locally
```bash
$ make run
```
## Run in Docker
```bash
$ make docker-build
$ make docker-run
```
