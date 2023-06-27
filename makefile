run:
	python3 manage.py runserver
superuser:
	python3 manage.py createsuperuser
makemigrations:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate