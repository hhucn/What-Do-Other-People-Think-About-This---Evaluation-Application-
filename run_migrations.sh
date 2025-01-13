#!/bin/sh

echo "Waiting for database to be ready..."

./wait-for-it.sh -t 60 db:5432

python3 manage.py migrate
