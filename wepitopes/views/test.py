def build_query(db, json_payload, print_aql=False):
    from collections import defaultdict
    import json

    col_to_elmt = {}
    filters = defaultdict(list)
    ret = {}
    for name, filt in json_payload["query"].items():
        try :
            col_name, field = name.split(".")
        except :
            return (False, "query: Every item must be in the format: Collection.field")

        if col_name not in col_to_elmt:
            col_to_elmt[col_name] = "col%d" % len(col_to_elmt)
        elmt = "%s.%s" % (col_to_elmt[col_name], field )
        
        if filt["type"] == "float":
            filters[col_name].append(
                "FILTER {elmt} >= {min} && {elmt} <= {max}".format(elmt=elmt, min=filt["range"][0], max=filt["range"][1])
            )
        elif filt["type"] == "enumeration":
            filters[col_name].append(
                "FILTER {elmt} IN {vals}".format(elmt=elmt, vals=filt["cases"])
            )
        ret[name] = elmt

    if len(col_to_elmt) > 2:
        return (False, "Maximum two collections")

    if 'additional_fields' in json_payload:
        for val in json_payload['additional_fields']:
            try :
                sval1, sval2 = val.split(".")
            except :
                return (False, "additional_fields: Every item must be in the format: Collection.field")
            
            ret[val] = "%s.%s" % (sval1, sval2)
    
    limit = ""
    if 'limit' in json_payload:
        limit = "LIMIT %d" % limit
    
    sort = ""
    if 'sort' in json_payload:
        try:
            col, field = json_payload["sort"]["field"].split(".")
        except :
            return (False, "sort: Every item must be in the format: Collection.field")

        try:
            sort = "SORT %s.%s %s" % (col_to_elmt[col], field, json_payload["sort"]["direction"])
        except KeyError:
            return (False, "Sort must have a direction: ASC, DESC, RAND")

    if len(col_to_elmt) == 2:
        if "join" not in json_payload:
            return (False, "No join information given")
        join = json_payload["join"]

        if type(join) != list :
            return (False, "Join information must be an array")

        if len(join) != 2 :
            return (False, "Join information must be of two elements")

        try :
            join_col1, join_field1 = join[0].split(".")
            join_col2, join_field2 = join[1].split(".")
        except :
            return (False, "join: Every join item must be in the format: Collection.field")

        try :
            join_elmt1, join_elmt2 = col_to_elmt[join_col1], col_to_elmt[join_col2]
        except :
            return (False, "Join collections must be the same as query collections")

        join_str = "FILTER {elmt1}.{field1} == {elmt2}.{field2}".format(elmt1=join_elmt1, field1=join_field1, elmt2=join_elmt2, field2=join_field2)
        ret[join[0]] = "%s.%s" % (join_elmt1, join_field1)
        ret[join[1]] = "%s.%s" % (join_elmt2, join_field2)

        aql= """
            FOR {elmt1} IN {col1}
                {filters1}
                FOR {elmt2} IN {col2}
                    {join}
                    {filters2}
                    {sort}
                    {limit}
                    RETURN {ret}
        """.format(
            elmt1 = col_to_elmt[join_col1], col1=join_col1, filters1='\n'.join(filters[join_col1]),
            join = join_str,
            elmt2 = col_to_elmt[join_col2], col2=join_col2, filters2='\n'.join(filters[join_col2]),
            sort = sort,
            limit = limit,
            ret = json.dumps(ret).replace('"', '')
        )
    else :
        col, element = col_to_elmt.items()[0]
        aql= """
            FOR {elmt} IN {col}
                {filters}
                {sort}
                {limit}
                RETURN {ret}
        """.format(
            elmt = element, col=col, filters='\n'.join(filters[col]),
            join = join_str,
            sort = sort,
            limit = limit,
            ret = json.dumps(ret).replace('"', '')
        )

    if print_aql:
        print(aql)
    ret = db.AQLQuery(aql, rawResults=True, batchSize=1, bindVars={})
    return (True, ret)

if __name__ == '__main__':
    dct ={
        "payload": {
            "query":{
                "Peptides.score": {
                    "type": "float",
                    "range": [0.9, 1],
                },
                "VirusSequence.region": {
                    "type": "enumeration",
                    "cases": ["wuhan"]
                },
                "Peptides.length": {
                    "type": "enumeration",
                    "cases": [9]
                },
                "VirusSequence.family": {
                    "type": "enumeration",
                    "cases": ["sars-cov2"]
                }
            },
            "join": ["VirusSequence.Sub_accession", "Peptides.Sub_accession"],
            "Limit": 5000,
            "sort": {
                "field": "Peptides.score",
                "direction": "ASC"
            },
            "additional_fields":["VirusSequence.sequence"]
        }
    }
    print(build_query(None, dct["payload"]))