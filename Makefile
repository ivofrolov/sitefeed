.DEFAULT_GOAL := lint

src = .
package = sitefeed

.PHONY: format
format:
	ruff format $(src)/$(package)

.PHONY: lint
lint:
	ruff check --output-format pylint $(src)/$(package)
	pyright $(src)/$(package)

.PHONY: ensure-pip-tools
ensure-pip-tools:
	@which pip-compile > /dev/null || python -m pip install pip-tools -q

.PHONY: requirements
requirements: ensure-pip-tools
	pip-compile -U -o requirements.txt pyproject.toml

.PHONY: install
install: ensure-pip-tools
	pip-sync
