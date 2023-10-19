# adventofcode

These are the steps taken to build this python project.

Written in 2023 using `python3.11`

## GitHub CLI access

Login to GitHub via browser.
Generate a personal access token with at least `repo`, `workflow` and `read:org` permissions.

https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic

Do a git clone / git push, and enter:
``` 
Username: ruivitormeireles@gmail.com
Password: YOUR_PERSONAL_ACCESS_TOKEN
```

To avoid always having to enter the credentials:
```
yum install gh
gh auth login
# Select GitHub.com + HTTPS + token
# (otherwise, gh will respect the GITHUB_TOKEN environment variable)
```
https://cli.github.com/manual/


## Virtual Environment
Create venv:
```
python3.11 -m venv .venv
source .venv/bin/activate
```

Create `requirements.txt` file, then:
```
pip install -U pip
pip install -r requirements.txt
```

## VSCode
https://menziess.github.io/howto/enhance/your-python-vscode-workflow/

Install extensions:
- Python
- Error Lens
- GitLens
- Peacock
- Remote: SSH
- Vim

Add configurations to `.vscode/settings.json`
- Linting/Typing: Ignore `pylance` warnings
- Linting: Enable `flake8`, not `pylint`
- Typing: Enable `mypy` in `strict` mode
- Formatting: Enable `black`, format on save
- Testing: Enable `pytest`, not `unittest`

## Git
Create `.gitignore`

Also `.githooks/precommit`:
```
make test
```


## Packaging / Structuring a Python Project

https://medium.com/mlearning-ai/a-practical-guide-to-python-project-structure-and-packaging-90c7f7a04f95







## 

- dynaconf module
  - ./src/infra_creator/config.py
  - to read from ./settings.toml

- setuptools
  - to structure packages (so you can install them with pip)
  - packages are easy to test and to version
  - ./setup.py and ./Makefile and ./pyproject.toml
    https://menziess.github.io/howto/create/python-packages/
    https://setuptools.pypa.io/en/latest/index.html
	
	Module: a .py file containing functions that belong together
    Package: a collection of modules that is distributable
    Library: a package that is a not context aware

- Python-vscode 
  https://menziess.github.io/howto/enhance/your-python-vscode-workflow/

	- linter: flake8
	  - .flake8
	- typing: mypy
	- formatter: black

- Tests
  https://menziess.github.io/howto/test/python-code/
  - pytest
  - doctest
  
pytest --doctest-modules


Slightly overkill project setup
https://www.reddit.com/r/adventofcode/comments/r5vxvb/slightly_overkill_project_setup_python/?rdt=45855
