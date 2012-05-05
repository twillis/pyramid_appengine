from pyramid.config import Configurator
from resources import Root
import views
import pyramid_jinja2
import os

__here__ = os.path.dirname(os.path.abspath(__file__))


def make_app():
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root)
    config.add_renderer('.jinja2', pyramid_jinja2.Jinja2Renderer)
    config.add_view(views.my_view,
                    context=Root,
                    renderer='mytemplate.jinja2')
    config.add_static_view(name='static',
                           path=os.path.join(__here__, 'static'))
    return config.make_wsgi_app()

application = make_app()
