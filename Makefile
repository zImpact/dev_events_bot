.PHONY: format lint test

format:
	black .
	isort .

lint:
	black --check .
	isort . --check --diff
	flake8 .
	ruff check
	mypy --strict .

test:
	pytest

run:
	python main.py
