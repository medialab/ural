# Variables
SOURCE = ural

# Commands
all: lint test
test: unit
publish: upload clean

clean:
	rm -rf *.egg-info .pytest_cache build dist

lint:
	@echo Linting source code using pep8...
	pycodestyle --ignore E501 $(SOURCE) test
	@echo

unit:
	@echo Running unit tests...
	pytest -s
	@echo

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*
