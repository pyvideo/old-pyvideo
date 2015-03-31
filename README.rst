======
README
======

This is the repository holding the pyvideo.org bits for running the site.

The site is at `<http://pyvideo.org/>`_.

pyvideo.org is an instance of `richard <https://github.com/pyvideo/richard/>`_
which is a Django-based web application for building video index sites like
pyvideo.

We hang out on IRC in ``#richard`` on freenode.net.


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
