#!/bin/bash
export PG_HOST=127.0.0.1
export PG_PORT=5432
export PG_USER=test
export PG_PASSWORD=test
export PG_DBNAME=postgres
export SECRET_KEY="django-insecure-d4!is5w%3kx@@9%d+r_=l8@(nu_l7^v50#7e2_vd!#_if=t@#-"
cd second/restaurants
python3 manage.py test $1
