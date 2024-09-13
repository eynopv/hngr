VENV="./.venv"
VENV_BIN=$(VENV)/bin
TEST_DB_FILE=db/test.db
PIP_COMPILE=$(VENV_BIN)/pip-compile
PIP_INSTALL=$(VENV_BIN)/pip install

.PHONY: setup
.PHONY: setup-dbmate
.PHONY: compile
.PHONY: test
.PHONY: dev
.PHONY: start
.PHONY: clean

setup:
	python -m venv .venv
	$(PIP_INSTALL) -r requirements-dev.txt
	$(PIP_INSTALL) -r requirements.txt

setup-dbmate:
	sudo curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64
	sudo chmod +x /usr/local/bin/dbmate

compile:
	$(PIP_COMPILE) --strip-extras requirements.in
	$(PIP_COMPILE) --strip-extras requirements-dev.in

test:
	DATABASE_URL="sqlite:$(TEST_DB_FILE)" dbmate up
	DB=$(TEST_DB_FILE) $(VENV_BIN)/pytest -vv || true
	rm $(TEST_DB_FILE)

dev:
	DEV=true $(VENV_BIN)/fastapi dev hngr/main.py

start:
	$(VENV_BIN)/fastapi run hngr/main.py

clean:
	rm -rf $(VENV)
