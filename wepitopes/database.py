import pyArango.connection as CON

_DB_CONNECTION = None
_DB = None

def includeme(config):
    import os
    global _DB
    global _DB_CONNECTION

    url = os.environ.get('WEPITOPES_ARANGODB_URL')
    username = os.environ.get('WEPITOPES_ARANGODB_USERNAME')
    password = os.environ.get('WEPITOPES_ARANGODB_PASSWORD')

    # print(url, username, password)

    if url is None or username is None or password is None:
        print("Error: please set environement vaiables: WEPITOPES_ARANGODB_URL, WEPITOPES_ARANGODB_USERNAME, WEPITOPES_ARANGODB_PASSWORD")
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

def get_connection():
    global _DB_CONNECTION
    return _DB_CONNECTION

def get_database():
    global _DB
    return _DB
