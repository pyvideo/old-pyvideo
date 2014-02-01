#!/bin/bash

export PYTHONPATH=$PYTHONPATH:./config
export DJANGO_SETTINGS_MODULE=pyvideo_settings
venv/bin/python richard/manage.py $@
