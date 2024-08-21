VENV_BIN=./.venv/bin

.PHONY: venv
.PHONY: dev
.PHONY: test

venv:
	python -m venv .venv

dev:
	$(VENV_BIN)/fastapi dev hngr/main.py

test:
	DATABASE_URL="sqlite:db/test.db" dbmate up
	DATABASE_URL="db/test.db" $(VENV_BIN)/pytest || true
	rm ./db/test.db
