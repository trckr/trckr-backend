#!/bin/bash

# Quickfix to wait for postgres
sleep 5

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
