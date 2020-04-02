from pyramid.config import Configurator
from pyramid.renderers import JSONP


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.add_renderer('jsonp', JSONP(param_name='callback'))
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include('.database')
        config.scan()
    return config.make_wsgi_app()
