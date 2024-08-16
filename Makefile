VENV_BIN=./.venv/bin

.PHONY: venv
.PHONY: dev
.PHONY: test

venv:
	python -m venv .venv

dev:
	$(VENV_BIN)/fastapi dev hngr/main.py

test:
	$(VENV_BIN)/pytest
