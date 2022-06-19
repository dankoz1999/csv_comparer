MODULE = comparer
LIBS = ${MODULE} tests
PYTHON = poetry run python
PRECOMMIT = poetry run pre-commit

FILES_IN = tests/data
FILES_OUT = tests/data_out
FILENAME_TYPE = bottom_tables equipment tag_assignments
ALIASES = bottom_tables equipment sensors
COLUMNS_BT = filename drawing_number drawing_title_name drawing_description major_equipment major_equipment_parsed
COLUMNS_EQ = service_description yard_no equipment_code scraped_equipment_type
COLUMNS_SNS = sensor_name primary_equipment_count filename equipment_code

.PHONY: clean fmt lint test init shell run-stack down-stack scrape


define run_comparer
		${PYTHON} -m ${MODULE} --mode $(1) \
		--chosen-files ${FILES_IN} --output-dir ${FILES_OUT} \
		--filename-type ${FILENAME_TYPE} --aliases ${ALIASES} --columns ${COLUMNS_BT} \
		--columns ${COLUMNS_EQ} --columns ${COLUMNS_SNS}
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