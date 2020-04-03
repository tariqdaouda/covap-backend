import wepitopes.models.db_collections as COL

from pyramid.view import view_config
from ..database import get_database
from . import useful as us
from .. import configuration as conf

@view_config(route_name='api_get_fields', renderer='jsonp')
def get_fields(request):
    """
    returns possible all fields for subsetting
    {limit: 5000} will limit the number of
    field for enumerations to the 5000 first. Otherwise
    the maximum is the used is the one defined the configuration
    of the back end
    """
    
    limit = conf.DEFAULT_ENUMERATION_LIMIT
    try :
        if 'limit' in request.json:
            limit = request.json["limit"]
    except :
        pass 
        
    db = get_database()
    payload = {}
    for col_cls in COL.__COLLECTIONS:
        col_name = col_cls.__name__
        payload[col_name] = {}
        for field_name in col_cls._fields.keys():
            typ = col_cls._field_types.get(field_name)
            if typ=="float":
                field_dct = {"type": typ}
                min_val = us.get_extremum(db, col_name, field_name, "ASC")
                max_val = us.get_extremum(db, col_name, field_name, "DESC")
                field_dct["range"] = [min_val, max_val]
            elif typ=="enumeration":
                field_dct = {"type": typ}
                try:
                    field_dct.update(us.get_enumeration(db, col_name, field_name, limit))
                except:
                    return us.JSONResponse(errors = ["Invalid request for field %s of %s" % (field_name, col_name)] ) 
            else:
                field_dct = {"type": "other"}
            
            payload[col_name][field_name] = field_dct
    
    ret = us.JSONResponse() 
    ret.set_payload(payload)
    return ret

@view_config(route_name='api_get_data', renderer='jsonp')
def get_data(request):
    # payload: {
    #     query:{
    #         score: {
    #             type: float,
    #             range: [0.9, 1],
    #         },
    #         region: {
    #             type: enumeration,
    #             cases: [wuhan]
    #         },
    #         length: {
    #             type: enumeration,
    #             cases: [9]
    #         },
    #         virus: {
    #             type: enumeration,
    #             cases: [sars-cov2]
    #         }
    #     },
    #     Limit: 5000
    #     additional_fields:[sequence]
    # }
    json_data = request.json
    # return us.JSONResponse(errors = ["No json body found" ] )

    check, aql_or_message = us.build_query(json_data["payload"])
    if not check:
        return us.JSONResponse(errors = [aql_or_message] )
    print(aql_or_message)
    db = get_database()
    result = db.AQLQuery(aql_or_message, rawResults=True, batchSize=conf.DEFAULT_BATCH_SIZE, bindVars={})
    ret = us.JSONResponse()
    ret.set_payload(result.result)
    return ret
