VENV_BIN=./.venv/bin
TEST_DB_FILE=db/test.db

.PHONY: venv
.PHONY: dev
.PHONY: test

venv:
	python -m venv .venv

dev:
	$(VENV_BIN)/fastapi dev hngr/main.py

test:
	DATABASE_URL="sqlite:$(TEST_DB_FILE)" dbmate up
	DATABASE_URL=$(TEST_DB_FILE) $(VENV_BIN)/pytest -vv || true
	rm $(TEST_DB_FILE)
