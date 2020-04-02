import wepitopes.models.db_collections as COL

from pyramid.view import view_config
from ..database import get_database
from . import useful as us
from .. import configuration as conf

@view_config(route_name='api_get_fields', renderer='jsonp')
def get_fields(request):
    """
    returns possible all fields for subsetting
    {max_enumeration_size: 5000} will limit the number of
    field for enumaration to the 5000 first. Otherwise
    the maximum is the used is the one defined the configuration
    of the back end
    """
    
    max_enumeration_size = conf.MAX_UNIQUE_ENUMERATION
    try :
        if 'max_enumeration_size' in request.json:
            max_enumeration_size = request.json["max_enumeration_size"]
    except :
        pass 
        
    db = get_database()
    payload = {}
    for col_cls in COL.__COLLECTIONS:
        col_name = col_cls.__name__
        payload[col_name] = {}
        for field_name, typ in col_cls._field_types.items():
            if typ=="float" or typ=="enumeration" :
                field_dct = {"type": typ}
                if typ=="float":
                    min_val = us.get_extremum(db, col_name, field_name, "ASC")
                    max_val = us.get_extremum(db, col_name, field_name, "DESC")
                    field_dct["range"] = [min_val, max_val]
                if typ=="enumeration":
                    try:
                        field_dct = us.get_enumeration(db, col_name, field_name, max_enumeration_size)
                    except:
                        return us.JSONResponse(errors = ["Invalid request for field %s of %s" % (field_name, col_name)] ) 
                payload[col_name][field_name] = field_dct
    
    ret = us.JSONResponse() 
    ret.set_payload(payload)
    return ret

