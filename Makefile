VENV_BIN=./.venv/bin
TEST_DB_FILE=db/test.db

.PHONY: venv
.PHONY: dev
.PHONY: start
.PHONY: test

venv:
	python -m venv .venv

dev:
	DEV=true $(VENV_BIN)/fastapi dev hngr/main.py

start:
	$(VENV_BIN)/fastapi run hngr/main.py

test:
	DATABASE_URL="sqlite:$(TEST_DB_FILE)" dbmate up
	DB=$(TEST_DB_FILE) $(VENV_BIN)/pytest -vv || true
	rm $(TEST_DB_FILE)

install-dbmate:
	sudo curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64
	sudo chmod +x /usr/local/bin/dbmate
