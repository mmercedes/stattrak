#!/bin/bash
cd /Users/matt/Documents/School/15-437/team41/
rm -r projectTest/stattrak projectTest/authentication projectTest/templates projectTest/static
cp -r project/stattrak project/authentication project/templates project/static projectTest
cd projectTest
python manage.py runserver
