import pyArango.connection as CON

_DB_CONNECTION = None
_DB = None
_CONTACTS_DB = None

def includeme(config):
    import os
    global _DB
    global _DB_CONNECTION
    global _CONTACTS_DB

    url = os.environ.get('WEPITOPES_ARANGODB_URL')
    username = os.environ.get('WEPITOPES_ARANGODB_USERNAME')
    password = os.environ.get('WEPITOPES_ARANGODB_PASSWORD')
    contacts_database_name = os.environ.get("WEPITOPES_CONTACTS_DATABASE")

    if url is None or username is None or password is None or contacts_database_name is None:
        print("Error: please set environement vaiables: WEPITOPES_ARANGODB_URL, WEPITOPES_ARANGODB_USERNAME, WEPITOPES_ARANGODB_PASSWORD, WEPITOPES_CONTACTS_DATABASE")
        return 

    _DB_CONNECTION = CON.Connection(
      arangoURL = url,
      username = username,
      password = password,
      verify = True,
      verbose = False,
      statsdClient = None,
      reportFileName = None,
      loadBalancing = "round-robin",
      use_grequests = False,
      use_jwt_authentication=False,
      use_lock_for_reseting_jwt=True,
      max_retries=5
    )

    _DB = _DB_CONNECTION["Covap"]
    _CONTACTS_DB = _DB_CONNECTION[contacts_database_name]

def get_connection():
    global _DB_CONNECTION
    return _DB_CONNECTION

def get_database():
    global _DB
    return _DB

def get_contacts_database():
    global _CONTACTS_DB
    return _CONTACTS_DB
