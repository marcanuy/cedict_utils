.PHONY: freeze test clean dist format

freeze:
	pip freeze > requirements.txt
test:
	pytest
clean:
	rm -r .tox
dist:
	python setup.py sdist bdist_wheel

dist-upload: dist
	twine upload --skip-existing dist/*

dist-test-upload:
	python3 -m twine upload --repository testpypi --skip-existing  dist/*
format:
	black .
