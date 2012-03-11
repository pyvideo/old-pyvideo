#!/bin/bash

# cd /srv/pyvideo/

export PYTHONPATH=./config:./richard:./richard/apps:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=pyvideo_settings

./venv/bin/python scripts/import_pycon2012.py
