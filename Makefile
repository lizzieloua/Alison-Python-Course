run:
	python3 11-Custom_Objects.py Lizzie Altena 25 100000
setup: requirements.txt
	pip3 install -r requirements.txt
test:
	pytest --cov 11-Custom_Objects 12-Unit_Testing.py