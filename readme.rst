===================
 pyramid_appengine
===================

A scaffold to help you get started writing a pyramid aplication that
will run on Google App Engine.

Installation
============

pyramid_appengine can be installed via pip or easy_install

::

   $ pip install -e git+git@github.com:twillis/pyramid_appengine.git#egg=pyramid_appengine



Once installation has completed, an appengine_starter template will be
made avaialable to use to create projects.

::

   $ paster create --list-templates
   Available templates:
     appengine_starter:      Pyramid scaffold for appengine
     ...



Getting Started
===============

To get started, first create your project skeleton.

::

   $ paster create -t appengine_starter mynewproject

A buildout environment for your project will be created. once
complete, run the buildout as usual


::

   $ cd meynewproject
   $ /usr/bin/python2.7 bootstrap.py --distribute
   $ ./bin/buildout

The buildout will take care of downloading and installing the App
Engine SDK (currently 1.6.3). it will be located in
"./parts/google_appengine" all utils for deploying and running the
development server will be located in "./bin"

Your source code for your project will be located at
"./src/mynewproject", a bundle of your source and it's dependencies
will be located at "./parts/mynewproject"

Running your project for development
====================================

::

   $ ./bin/devappserver parts/mynewproject

your pyramid site will be running on port 8080 so point your browser
at

::

   http://localhost:8080

Deploying your application to App Engine
========================================

Assuming you have created an application id "mynewproject" on app engine, the
application can be deployed like so.

::

   $ ./bin/appcfg update parts/mynewproject -A mynewproject -V dev

Then your application will be running at...

::

   http://dev.mynewproject.appspot.com


What It Does And Why
====================

...
