from pyramid.view import notfound_view_config
from . import useful as us

# @notfound_view_config(renderer='../templates/404.jinja2', xhr=False)
# def notfound_view(request):
#     request.response.status = 404
#     return {}

@notfound_view_config(renderer='jsonp')
def nof_found(request):
    request.response.status = 404
    return us.JSONResponse(errors = ["404: view not found"])