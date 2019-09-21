#!/bin/sh


echo 'waiting for db to start...'

until mysqladmin ping -h db --password=password -u root; do
    sleep 1
done

echo 'db has started'

sleep 3

gunicorn -b 0.0.0.0:5000 -w 4 --preload app:app
