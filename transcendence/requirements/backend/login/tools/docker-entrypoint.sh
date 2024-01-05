#!/bin/bash

if [ ! -d "/app/login" ]; then

    echo "Login project not found!"
    mkdir -p /app/login
    django-admin startproject transcendence /app
    django-admin startapp login /app/login

else
    echo "Login project found"
fi

exec python /app/manage.py runserver 0.0.0.0:8000