#!/bin/bash

export PYTHONPATH=./config:./richard:./richard/apps:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=pyvideo_settings

./venv/bin/python $1 $2

