
SRC=./app
TEST=./tests
OUT=./build

compile:
	python -m compileall $(SRC)

clean-pyc:
	find . -name '__pycache__' -exec rm -fr {} +

test: clean-test
	export `cat ./.env` && pytest -s -v

test-cov: clean-pyc clean-test
	export `cat ./.env` && pytest --cov-report html `find ./app -type d -exec echo -n '--cov {} ' \;`
# find ./app -type d -print0  | xargs -0 printf -- "--cov %s "

clean-test:
	rm -f .coverage
	rm -f .coverage.*
	rm -rf htmlcov
	rm -rf .pytest_cache

dist:
	python -m build --sdist --outdir $(OUT)

dist-verf:
	ls -Art $(OUT) | tail -1 | xargs printf -- "$(OUT)/%s" | xargs -0 tar -tf

clean-dist:
	rm -rf $(SRC)/*.egg-info

lint: format
	export `cat ./.env` && pylint --recursive=y --jobs=2 --output-format=colorized $(SRC)/
	# --reports=y

format:
	isort $(SRC) $(TEST)
	yapf --in-place --recursive $(SRC) $(TEST)

clean: clean-pyc clean-test clean-dist

checks: test lint clean

.PHONY: checks
