from pyramid.view import view_config
from pyramid.renderers import JSONP


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'wepitopes'}
