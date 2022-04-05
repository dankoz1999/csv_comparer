MODULE = comparer
LIBS = ${MODULE} tests
PYTHON = poetry run python
PRECOMMIT = poetry run pre-commit

FILES_DIR = data

.PHONY: clean fmt lint test init shell run-stack down-stack scrape

define run_comparer
		${PYTHON} -m ${MODULE} --mode $(1) \
		--files_dir ${FILES_DIR} --output_dir ${FILES_DIR} \
		--debug
endef

.git/hooks/pre-commit:
	@${PRECOMMIT} install
	@${PRECOMMIT} autoupdate
	@touch $@

pyproject.toml:
	@touch $@

poetry.lock: pyproject.toml
	@poetry env use "$(shell which python)"
	@poetry install
	@touch $@

init: poetry.lock .git/hooks/pre-commit

shell: poetry.lock
	@poetry shell

clean:
	@find . -type f -name "*.pyc" -delete
	@rm -f poetry.lock

lint: poetry.lock
	@${PYTHON} -m black ${LIBS}
	@${PYTHON} -m autoflake --in-place --recursive --remove-all-unused-imports --expand-star-imports ${LIBS}
	@${PYTHON} -m isort ${LIBS}
	@${PYTHON} -m mypy ${LIBS}
	@${PYTHON} -m bandit --configfile .bandit.yaml --recursive ${LIBS}

#TODO add comparision methods