.DEFAULT_GOAL := lint

src = .
package = sitefeed

.PHONY: format
format:
	ruff format $(src)/$(package)

.PHONY: lint
lint:
	ruff check --output-format pylint $(src)/$(package)
	ty check --output-format concise --color never --no-progress $(src)/$(package)

.PHONY: install
install:
	pip install --upgrade --upgrade-strategy=eager -e .
