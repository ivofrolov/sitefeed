.DEFAULT_GOAL := check

src = .
package = sitefeed

.PHONY: format
format:
	black $(src)/$(package)

.PHONY: lint
lint:
	ruff check $(src)/$(package)

.PHONY: typecheck
typecheck:
	pyright $(src)/$(package)

.PHONY: check
check: lint typecheck

.PHONY: ensure-pip-tools
ensure-pip-tools:
	@which pip-compile > /dev/null || python -m pip install pip-tools -q

.PHONY: requirements
requirements: ensure-pip-tools
	pip-compile -o requirements.txt pyproject.toml

.PHONY: install
install: ensure-pip-tools
	pip-sync
