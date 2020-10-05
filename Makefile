.PHONY: freeze test clean dist format

freeze:
	pip freeze > requirements.txt
test:
	pytest
clean:
	rm -r .tox
dist:
	python setup.py sdist bdist_wheel
	twine upload --skip-existing dist/*
format:
	black .
