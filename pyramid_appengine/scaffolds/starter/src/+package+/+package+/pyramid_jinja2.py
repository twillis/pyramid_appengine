"""
lightweight jinja2 renderer that will work with appengine
"""
from jinja2 import Environment, FileSystemLoader
import os


__here__ = os.path.dirname(os.path.abspath(__file__))

JINJA2_ENV = Environment(\
    loader=FileSystemLoader([os.path.join(__here__, "templates")]))


def render_to_string(template, data={}):
    """
    applies data to template
    """

    global JINJA2_ENV

    if not JINJA2_ENV:
        raise ValueError("JINJA2_ENV not set")
    else:
        t = JINJA2_ENV.get_template(template)
        if t:
            return t.render(**data)
        else:
            raise ValueError("template %s not found" % template)


class Jinja2Renderer(object):
    def __init__(self, info):
        self._info = info
        self._template = info.name

    def __call__(self, value, system):
        value.update(system)
        return render_to_string(self._template, value)
