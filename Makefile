help:
	@grep '^[^#[:space:]].*:' Makefile | awk -F ":" '{print $$1}'

clean:
	@find . -name "*.pyc" -delete

run: clean
	@python api.py

deps:
	@pip install -r requirements.txt
	@pip install -r requirements_test.txt

setup: deps

violations:
	@echo "PEP8 code compliance"
	@-pep8 marketplace --ignore=E501,E126,E127

test: clean
	@nosetests
