#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

# Create superuser only if it does not exist
python manage.py shell << END
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if username and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser created.")
else:
    print("Superuser already exists or missing env variables.")
END

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate