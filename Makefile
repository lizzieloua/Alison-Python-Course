run:
	python3 Advanced/custom_object.py Lizzie Altena 25 100000
	python3 Advanced/inheritance.py Bobbers 5
setup: requirements.txt
	pip3 install -r requirements.txt
test:
	cd Advanced; pytest --cov custom_object tests/test_custom_object.py --cov-report term-missing;