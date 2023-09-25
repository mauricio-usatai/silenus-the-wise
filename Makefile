PORT ?= 8080
URL_BASE_PATHNAME ?= /

app:
	uvicorn main:app --host="0.0.0.0" --port=${PORT} --root-path ${URL_BASE_PATHNAME}

pylint:
	git ls-files '*.py' | xargs pylint --disable=duplicate-code --fail-under=10

black:
	git ls-files '*.py' | black --check .

pytest:
	pytest --no-cov-on-fail --cov-fail-under=70 --cov-branch --cov-report=term --cov-report=html:htmlcov --cov=apps --cov=src
