pipenv shell:
	pipenv shell

run-dev:
	export FLASK_APP=urlshort && export FLASK_ENV=development && flask run

pytest:
	pytest