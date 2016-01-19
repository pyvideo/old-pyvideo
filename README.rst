======
README
======

**This project is inactive.**

This project was sunset on 2016/01/15: `pyvideo status: January 15th, 2016 <http://bluesock.org/~willkg/blog/pyvideo/status_20160115.html>`_

This repository was historically used for holding the bits for running the pyvideo.org site.

pyvideo.org was an instance of `richard <https://github.com/pyvideo/richard/>`_
which is a Django-based web application for building video index sites like
pyvideo.

Setup notes
===========

There's a bunch of stuff in this repository. For running pyvideo, there are two
interesting directories:

* ``config/`` holds the pyvideo specific settings
* ``templates/`` holds templates that override richard templates

To run pyvideo locally, you need to set some environment variables and then
run richard's ``manage.py``::

  SITE_PATH=<path to richard>,<path to pyvideo/config>
  DJANGO_SETTINGS_MODULE=pyvideo_settings
  DJANGO_CONFIGURATION=PyvideoLocal
  DJANGO_DATABASES=<your db url>
  DJANGO_SECRET_KEY=<secret key>
