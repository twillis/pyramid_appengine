===================
 pyramid_appengine
===================

A scaffold to help you get started writing a pyramid aplication that
will run on Google App Engine.

Installation
============

pyramid_appengine can be installed via pip or easy_install

::

   $ pip install pyramid_appengine



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

   $ pcreate -t appengine_starter mynewproject

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

Most pyramid scaffolds create a project directory structure that is an
installable through the pip/easy_install . However, App Engine
applications do not support that format. Instead App Engine assumes
that everything is contained in one directory including all of the
projects dependencies not provided by the App Engine run time. 

So a directory structure for an application deployable to App Engine
looks like this...

::

   /myproject/
   /myproject/app.yaml
   /myproject/app.py # some script referenced in app.yaml
   /myproject/index.yaml
   /myproject/queue.yaml
   /myproject/pyramid
   /myproject/verlruse
   /myproject/jinja2
   /myproject/newfangledlib

Because of this directory structure, which is vastly different from
what is expected by other tools, we need a way to develop in your
typical python egg format, but deploy in an App Engine format.

Enter Buildout
--------------

Buildout is a tool that can be used to support the kind of setup where
you develop your application as an egg but deploy what App Engine
expects. If you aren't familiar with buildout you may want to read up
on it. It has some of the same goals as virtualenv, but has more
features via recipes to help with deployment.

For running the buildout you typically do ...

::

   $ /path/to/python bootstrap.py --distribute
   $ ./bin/buildout

The buildout.cfg file distributed with python_appengine does the
following.

   - creates a buildout environment where the source for your project
     is located at ./src/nameofproject

When buildout is run ...

   - all the dependencies for your project are downloaded and setup in
     the buildout environment
   - the appengine sdk is downloaded and installed in the buildout
     environment under ./parts/google_appengine .
   - tools such as devappserver, appcfg which are tools distributed
     with the app engine sdk are put in the buildouts bin directory
   

Managing dependencies for deployment
====================================

As mentioned earlier, all dependencies must be contained in the
applications deployment directory under parts or provided by the app
engine runtime environment. As your application gets bigger and bigger
you will likely edit the buildout.cfg from time to time to add more
dependencies so that they are deployed with your application.

To update the dependencies for your application edit the packages
attribute under the stanza for your project in the buildout.cfg and
then run ./bin/buildout again to have the dependencies symlinked or
copied to parts/mynewproject


Testing
=======

As a general rule, having a thorough unit test suite is good. But in
the authors opinion it is essential for app engine applications. The
main reason being that app engine requires you to specify the
datastore indexes you need to support the application at deployment
time via the index.yaml.

The app engine sdk will update your index.yaml for you when you are
running your application on the development server. But it requires
you use something that generates an HTTP request in order to trigger
the behavior. So in theory, you would have to make sure you hit every
page of your application before you deploy to insure any new index
needs caused by new or updated queries are recorded. 

This method is error prone and time consuming. A better way is to have
your unit tests generate it. 

The project generated by the scaffold includes everything you need to
do this. By using py.test and hooks specified in conftest.py, a couple
things are guaranteed.

   #. a clean appengine environment is initialized before each test
   #. any changes to index.yaml are written after each test

Tests can be run from the root of the project directory like so.

::

   $ ../../bin/python setup.py test

or ...

::

   $ ../../bin/py.test
