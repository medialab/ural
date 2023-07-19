# Variables
SOURCE = ural

# Functions
define clean
	rm -rf *.egg-info .pytest_cache build dist
	find . -name "*.pyc" | xargs rm -f
	find . -name __pycache__ | xargs rm -rf
	rm -f *.spec
	rm -rf .tox
endef

# Commands
all: lint test
test: unit
publish: clean lint test upload
	$(call clean)

clean:
	$(call clean)

deps:
	pip3 install -U pip
	pip3 install -r requirements.txt

format:
	@echo Formatting source code using black
	black $(SOURCE) scripts test setup.py -t py33
	@echo

lint:
	@echo Searching for unused imports...
	importchecker $(SOURCE) | grep -v __init__ || true
	importchecker test | grep -v __init__ || true
	@echo

tld:
	@echo Upgrading internals...
	python -m ural upgrade
	black ural/tld_data.py -t py33
	@echo

unit:
	@echo Running unit tests...
	pytest -svvv
	@echo

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*
