#!/bin/bash

export PYTHONPATH=./config:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=pyvideo_settings

PYTHON=./venv/bin/python
FIXTURES=./fixtures

$PYTHON ./richard/manage.py reset videos sitenews
$PYTHON ./richard/manage.py syncdb

$PYTHON ./richard/manage.py loaddata \
    $FIXTURES/tags.json \
    $FIXTURES/speakers.json \
    $FIXTURES/categories.json \
    $FIXTURES/sitenews.json \
    $FIXTURES/bostonpy.json \
    $FIXTURES/chipy.json \
    $FIXTURES/pyatl.json \
    $FIXTURES/djangocon-2009.json \
    $FIXTURES/djangocon-2010.json \
    $FIXTURES/djangocon-2011.json \
    $FIXTURES/kiwi-pycon-2009.json \
    $FIXTURES/pycon-2009.json \
    $FIXTURES/pycon-2010.json \
    $FIXTURES/pycon-2011.json \
    $FIXTURES/pycon-au-2010.json \
    $FIXTURES/pygotham-2011.json \
    $FIXTURES/pyohio-2010.json \
    $FIXTURES/pyohio-2011.json \
    $FIXTURES/pytexas-2011.json

#    pycon-au-2011.json \

$PYTHON ./richard/manage.py rebuild_index
