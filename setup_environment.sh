#!/bin/bash

# create virtualenvironment and install requirements
pip install -E ./venv/ -s -r richard/requirements/base.txt

# install Django
./venv/bin/python packages/Django-1.4b1/setup.py install
