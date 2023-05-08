MODULE = comparer
LIBS = ${MODULE} tests
PYTHON = poetry run python
PRECOMMIT = poetry run pre-commit

FILES_IN = tests/data
FILES_OUT = tests/data_out
## needs to be filled by an user
# FILENAME_TYPE
# ALIASES
# COLUMNS_BT
# COLUMNS_EQ
# COLUMNS_SNS
# EXCEPTION_COLUMNS
# TO_COUNT

.PHONY: clean fmt lint test init shell run-stack down-stack scrape


define run_comparer
		${PYTHON} -m ${MODULE} --mode $(1) \
		--chosen-files ${FILES_IN} --output-dir ${FILES_OUT} \
		--filename-type ${FILENAME_TYPE} --aliases ${ALIASES} --columns ${COLUMNS_BT} \
		--columns ${COLUMNS_EQ} --columns ${COLUMNS_SNS} --exception-columns ${EXCEPTION_COLUMNS} --to-count ${TO_COUNT}
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


basic_statistics: poetry.lock
	@$(call run_comparer, basic_statistics)

show_difference: poetry.lock
	@$(call run_comparer, show_difference)

visualize: poetry.lock
	@$(call run_comparer, visualize)