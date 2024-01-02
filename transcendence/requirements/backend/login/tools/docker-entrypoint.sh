#!/bin/bash

if [ ! -d "/app/login" ]; then
    echo "Login project not found!"
    django-admin startproject login /app
else
    echo "Login project found"
fi

exec python /app/manage.py runserver 0.0.0.0:8000