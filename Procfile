release: python manage.py migrate && python create_superuser.py
web: gunicorn mysite.wsgi --log-file -
