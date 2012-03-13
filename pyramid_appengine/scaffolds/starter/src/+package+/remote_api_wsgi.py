"""
to have multithreading work, we run as wsgi instead of cgi
"""
from google.appengine.ext.remote_api.handler import application as app
