test:
	python -m pytest TP/tests/ -v

unit_test:
	python -m pytest TP/tests/unit/ -v -m "not perf"

perf_test:
	python -m pytest TP/tests/ -v -m "perf"

coverage:
	python -m coverage run -m pytest TP/tests/ -v
	python -m coverage report -m
	python -m coverage html

lint:
	python -m ruff check src/ TP/

doc:
	python -m pdoc --html --output-dir docs src/
