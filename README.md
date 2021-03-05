<h2 align="center">demo-tpl-py boilerplate setup guide</h2>

# DISCLAIMER
This boilerplate is used for demo purposes as part of education sessions/trainings. It doesn't include many aspects which should be present in production-ready project setup. However, all the tools around the sample code are configured properly and can be reused in projects.
# Software requirements
1. Install [pyenv](https://github.com/pyenv/pyenv) (*Unix) or [pyenv-win](https://github.com/pyenv-win/pyenv-win) (Windows).
2. Install latest python version as global one via _pyenv_. If you have already an installed Python on a system level, skip this step.
   ```bash
   # Commands below illustrate what you need to do as an idea.
   # Exact commands might change depending on a particular OS.
   $ pyenv install -l | grep 3.9
   $ pyenv install 3.9.x
   $ pyenv global 3.9.x
   ```
3. Install [Poetry](https://python-poetry.org/docs/) package manager.
4. Install [make](https://www.gnu.org/software/make/) CLI tool.
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
