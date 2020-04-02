def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('api_get_fields', '/api/get-fields')
    config.add_route('api_get_data', '/api/get-data')
    config.add_route('home', '/')
