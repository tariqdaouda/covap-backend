import wepitopes.models.db_collections as COL

from pyramid.view import view_config
from ..database import get_database, get_contacts_database
from . import useful as us
from .. import configuration as conf
from pyArango.theExceptions import ValidationError
from pyramid.response import Response
from pyArango.validation import Email

@view_config(route_name='vital', renderer='jsonp', request_method="OPTIONS")
@view_config(route_name='vital', renderer='jsonp', request_method="GET")
def vital(request):
    """
    Returns a random peptide to check that everything is up
    """
    db = get_database()
    payload = db["Peptides"].fetchFirstExample({"Length": 9}, rawResults=True).result
    ret = us.JSONResponse()
    ret.set_payload(payload)
    return ret


@view_config(route_name='api_get_fields', renderer='jsonp', request_method="OPTIONS")
@view_config(route_name='api_get_fields', renderer='jsonp', request_method="POST")
def get_fields(request):
    """
    returns possible all fields for subsetting
    {limit: 5000} will limit the number of
    field for enumerations to the 5000 first. Otherwise
    the maximum is the used is the one defined the configuration
    of the back end
    """
    limit = conf.DEFAULT_ENUMERATION_LIMIT
    try:
        json_data = request.json
    except Exception as e:
        return us.JSONResponse(errors = ["Invalid json body"])
    
    if 'limit' in json_data:
        try :
            limit = int(json_data["limit"])
        except Exception as e:
            us.JSONResponse(errors = ["limit must be a valid integer"])

    db = get_database()
    check, payload = us.get_fields(db, COL.__COLLECTIONS.values(), limit)
    if not check:
        return us.JSONResponse(errors = payload)

    ret = us.JSONResponse()
    ret.set_payload(payload)
    return ret

@view_config(route_name='api_get_fields_limit', renderer='jsonp', request_method="OPTIONS")
@view_config(route_name='api_get_fields_limit', renderer='jsonp', request_method="GET")
def get_fields_limit(request):
    """
    returns possible all fields.
    'limit=5000' will limit the number of
    field for enumerations to the 5000 first.
    """
    try:
        limit = int(request.matchdict['limit'])
    except Exception as e:
        us.JSONResponse(errors = ["limit must be a valid integer"])
    
    db = get_database()
    check, payload = us.get_fields(db, COL.__COLLECTIONS.values(), limit)
    if not check:
        return us.JSONResponse(errors = payload)

    ret = us.JSONResponse() 
    ret.set_payload(payload)
    return ret

@view_config(route_name='api_get_collection_fields_limit', renderer='jsonp', request_method="OPTIONS")
@view_config(route_name='api_get_collection_fields_limit', renderer='jsonp', request_method="GET")
def get_collection_fields_limit(request):
    """
    returns possible all fields for a collection
    'limit=5000' will limit the number of
    field for enumerations to the 5000 first.
    """
    try:
        limit = int(request.matchdict['limit'])
    except Exception as e:
        us.JSONResponse(errors = ["limit must be a valid integer"])
    
    db = get_database()

    try:
        colname = request.matchdict['collection']
        collection = COL.__COLLECTIONS[colname]#db[colname].__class__
    except Exception as e:
        return us.JSONResponse(errors = ["Collection name must be valid"])
    
    check, payload = us.get_fields(db, [collection], limit)
    if not check:
        return us.JSONResponse(errors = payload)
    ret = us.JSONResponse() 
    ret.set_payload(payload)
    return ret

@view_config(route_name='api_get_data', renderer='jsonp', request_method="OPTIONS")
@view_config(route_name='api_get_data', renderer='jsonp', request_method="POST")
def get_data(request):
    try:
        json_data = request.json
    except Exception as e:
        return us.JSONResponse(errors = ["Invalid json body"])
    
    try:
        check, aql_or_message = us.build_query(COL.__COLLECTIONS.values(), json_data["payload"], print_aql=False)
    except Exception as e:
        print(e)
        return us.JSONResponse(errors = ["Unable to prossess requests. Please verify format"] )
        
    if not check:
        return us.JSONResponse(errors = [aql_or_message] )

    db = get_database()
    result = db.AQLQuery(aql_or_message, rawResults=True, batchSize=conf.DEFAULT_BATCH_SIZE, bindVars={})
    
    ret = us.JSONResponse()
    ret.set_payload(result.result)
    return ret

@view_config(route_name='api_update_contacts', renderer='jsonp', request_method="OPTIONS")
@view_config(route_name='api_update_contacts', renderer='jsonp', request_method="POST")
def update_contact(request):
    """
    Saves an email contact to the database (meaning someone downloaded some data)
    """
    try:
        json_data = request.json
    except Exception as e:
        return us.JSONResponse(errors=["Invalid json body"])
        
    json_response = us.JSONResponse()
    try:
        email = json_data["payload"]["email"]
        Email().validate(email)
        db = get_contacts_database()
        contacts = db["Contacts"]
        contact_request = contacts.fetchFirstExample({"email": email})
        # if email exists
        if len(contact_request) >= 1:
            contact = contact_request[0]
            contact["nbDownloads"] = int(contact["nbDownloads"]) + 1
            contact.patch()
        else:
            contact = contacts.createDocument()
            contact.set({
                "email": email,
                "nbDownloads": 1
            })
            contact.save()
    except ValidationError as ve:
        return us.JSONResponse(errors=["invalid email: " + email])
        
    except Exception as e:
        return us.JSONResponse(errors=["unable to process the request"])
        
    return us.JSONResponse()
