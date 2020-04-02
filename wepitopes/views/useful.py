from .. import configuration as conf
import time

class JSONResponse(dict):
    """Standard return format"""
    def __init__(self, messages=None, errors=None):
        super(JSONResponse, self).__init__()

        self["timestamp"] = time.ctime()
        self["version"] = conf.API_VERSION
        self["payload"] = {}

        if messages is None :
            self["messages"] = []
        else :
            self["messages"] = self.set_messages(messages)
     
        if errors is None :
            self["errors"] = []
            self["error"] = False
        else :
            self["errors"] = self.set_errors(errors)
            self["error"] = True

    def set_messages(self, messages):
        self["messages"] = list(messages)

    def append_message(self, message):
        self["messages"].append(messages)

    def set_errors(self, errors):
        self["errors"] = list(errors)
        self["error"] = True

    def append_error(self, error):
        self["errors"].append(errors)
        self["error"] = True

    def set_payload(self, payload):
        self["payload"] = payload

def get_extremum(db, collection, field, direction):
    """get min/ or max for a field"""
    aql = """
        FOR elmt in {collection}
            SORT elmt.{field} {direction}
            LIMIT 1
            RETURN elmt.{field}
    """.format(collection = collection, field = field, direction=direction)
    ret = db.AQLQuery(aql, rawResults=True, batchSize=1, bindVars={})
    return ret[0]

def get_enumeration(db, collection, field, max_number=None):
    """enumeration possible values"""

    if max_number is not None:
        max_number = ", %d" % max_number
    else :
        max_number = ""

    aql = """
        LET val = (
            FOR elmt in {collection}
                RETURN DISTINCT elmt.{field}
        )
        RETURN {{
            unique: LENGTH(val),
            values: SLICE(val, 0{max_number})
        }}
    """.format(collection = collection, field = field, max_number=max_number)
    ret = db.AQLQuery(aql, rawResults=True, batchSize=1, bindVars={})
    return ret[0]
