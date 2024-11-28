#!/bin/bash

while true; do
    poetry run alembic upgrade head
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done

poetry run gunicorn app.wsgi:app --workers 4 --bind 0.0.0.0:8000