#------------  Development ----------------

start:
	python3 manage.py runserver --settings=config.settings.dev

dev-install:
	pip install -r requirements/dev.txt

dev-m:
	python3 manage.py migrate --settings=config.settings.dev

dev-makem:
	python3 manage.py makemigrations --settings=config.settings.dev

dev-showm:
	python3 manage.py showmigrations --settings=config.settings.dev

dev-sqlm:
	python3 manage.py sqlmigrate $(a) $(m) --settings=config.settings.dev  

dev-dbshell:
	python3 manage.py dbshell --settings=config.settings.dev

dev-super:
	python3 manage.py createsuperuser --settings=config.settings.dev

dev-startapp:
	cd apps && python3 ../manage.py startapp $(app) --settings=config.settings.dev

dev-shell-plus:
	python3 manage.py shell_plus --settings=config.settings.dev


#-------------------- Production -------------------


prod-install:
	pip install -r requirements/prod.txt

prod-m:
	python3 manage.py migrate --settings=config.settings.prod

prod-makem:
	python3 manage.py makemigrations --settings=config.settings.prod

prod-super:
	python3 manage.py createsuperuser --settings=config.settings.prod

prod-shell-plus:
	python3 manage.py shell_plus --settings=config.settings.prod

prod-collectstatic:
	python3 manage.py collectstatic --settings=config.settings.prod

prod-gunicorn:
	gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.prod --bind 0.0.0.0:8000 -c config/prod/prod.py --log-file -


