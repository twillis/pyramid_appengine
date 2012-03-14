===================
 pyramid_appengine
===================

A scaffold to help you get started writing a pyramid aplication that
will run on Google App Engine.

Installation
============

pyramid_appengine can be installed via pip or easy_install

::

   $ pip install -e git@github.com:twillis/pyramid_appengine.git#egg=pyramid_appengine



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

   http://mynewproject.appspot.com


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
     environment under ./parts/google_appengine . Due to python2.7
     recently being announced for general availability, and the SDK
     not able to support 2.7 development yet, the sdk is patched by
     replacing webob 0.9 with webob 1.1.1. This is done so that you
     can develop using pyramid version <=1.2.
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

Yes everyone will tell you to test your application, and you
should. But there's another reason to test your app engine application
if you are using the datastore. (and if you aren't there's not really
much reason to use appengine)

The reason is that you must declare your indexes in the index.yaml
file for your application before you deploy. 

If you write a view that does something with datastore that requires
an operation that app engine does not have an index for, your
application will raise an IndexNotFoundError to the lucky user that
calls that view after you've deployed. 

You can declare them yourself but that would require knowing a lot
about how datastore works, so the App Engine SDK provides a facility
to keep your index.yaml updated during development so that when you
are ready to deploy, everything is already in sync in theory.

It does this through the development server. So, when you hit a page
for your application through the devappserver, the devappserver will
write any changes required to your index.yaml. 

So, if you make sure that before you deploy, you hit every page for
your application, you should be good. But how practical is that?

To avoid this you have 2 possibilities.

#1 Hire a QA department. 

all those stodgy corporations do this already and they employ an army
of button monkeys to follow a script to click through the application
and report unexpected behavior to their bosses. 

#2 Write code to replace your QA department.

you can't fully replace QA obviously, and attempting to hasdominishing
returns, but you can automate a lot of the stuff they would be
testing. The benefit is if you have full functional test coverage, you
reduce the chances of getting a IndexNotFoundError.

To be clear, these are functional tests not unit tests. Functional
tests essentially reproduce the HTTP requests your application is
expected to handle and asserts that the HTTP response from your
application is what was expected. It's closer to an end to end kind of
test that QA would traditionally be doing by following a script for a
given use case rather than a traditional unit test that tests one
function in isolation and mocks out every dependency it can.

I recommend using WebTest and pyramid_appengine provides tools to help
with this, though one could easily use any other tool like selenium or
lettuce with the selenium web driver or windmill etc.... 
