freeze:
	pip freeze > requirements.txt
test:
	pytest
clean:
	rm -r .tox
