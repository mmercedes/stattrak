#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
gunicorn stattrak.wsgi \
         --bind 0.0.0.0:$PORT \
         --workers 4
