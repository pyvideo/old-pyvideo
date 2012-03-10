#!/bin/bash

export PYTHONPATH=./config:./richard:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=pyvideo_settings

./venv/bin/python richard/manage.py $@
