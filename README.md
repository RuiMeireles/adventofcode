# adventofcode

Python Project

- Virtual Environment
  https://menziess.github.io/howto/manage/virtual-environments/

- git
  - .gitignore
  - .githooks/precommit: make test

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
