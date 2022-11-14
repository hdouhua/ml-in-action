
SRC=./app
OUT=./build

compile:
	python -m compileall $(SRC)

clean-pyc:
	find . -name '__pycache__' -exec rm -fr {} +

test:
	#

dist:
	python -m build --sdist --outdir $(OUT)

dist-verf:
	ls -Art $(OUT) | tail -1 | xargs printf -- "$(OUT)/%s" | xargs -0 tar -tf

clean-dist:
	rm -rf $(SRC)/*.egg-info

lint:
	cat $(SRC)/.env && pylint $(SRC)/
	# --reports=y --jobs=4 

format:
	yapf --in-place --recursive $(SRC)/

clean: clean-pyc clean-dist


.PHONY: clean compile
