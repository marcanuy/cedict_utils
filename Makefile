freeze:
	pip freeze > requirements.txt
test:
	pytest
clean:
	rm -r .tox
dist:
	python setup.py bdist_wheel
	twine upload dist/*
