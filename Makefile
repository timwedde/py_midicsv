install:
	poetry install
	poetry run pre-commit install

update:
	poetry update

lint:
	poetry run flake8

format:
	poetry run black **/**.py

pc:
	poetry run pre-commit run -a

test:
	poetry run pytest --cov=py_midicsv --junitxml=report.xml

coverage:
	poetry run coverage report
	poetry run coverage html

clean:
	rm report.xml
	rm -rf htmlcov
	rm -rf docs

doc:
	poetry run pdoc --force --html --output-dir docs py_midicsv

docdev:
	poetry run pdoc --http localhost:8001 py_midicsv
