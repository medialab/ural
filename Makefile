# Variables
SOURCE = ural

# Commands
all: lint test
test: unit
publish: clean lint test upload clean

clean:
	rm -rf *.egg-info .pytest_cache build dist
	find . -name "*.pyc" | xargs rm

lint:
	@echo Linting source code using pep8...
	pycodestyle --ignore E501,E722 $(SOURCE) test
	@echo
	@echo Searching for unused imports...
	importchecker $(SOURCE) | grep -v __init__ || true
	@echo

unit:
	@echo Running unit tests...
	pytest -s
	@echo

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*
