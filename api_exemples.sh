echo "404"
curl -i http://127.0.0.1:6543/api/tratra -X GET -H "Content-Type: application/json"

echo "Get fields, limit the enumeration lists to 20"
curl -i http://127.0.0.1:6543/api/get-fields -X POST -H "Content-Type: application/json" --data '{"limit": 20}'

echo "Get fields, limit the enumeration lists to 20"
curl -i http://127.0.0.1:6543/api/get-fields/limit/20 -X GET -H "Content-Type: application/json"

echo "Get fields for collection VirusSequences, limit the enumeration lists to 20"
curl -i http://127.0.0.1:6543/api/get-fields/VirusSequences/limit/20 -X GET -H "Content-Type: application/json"

echo "Get values with join"
curl -i http://127.0.0.1:6543/api/get-data -X GET -H "Content-Type: application/json" --data '{
        "payload": {
            "query":{
                "Peptides.Score": {
                    "type": "float",
                    "range": [0.7, 1]
                },
                "Peptides.Length": {
                    "type": "enumeration",
                    "cases": [9]
                },
                "VirusSequences.Family": {
                    "type": "enumeration",
                    "cases": ["Coronaviridae"]
                }
            },
            "join": ["VirusSequences.Accession", "Peptides.Accession"],
            "limit": 3,
            "sort": {
              "field": "Peptides.Score",
                  "direction": "DESC"
            },
            "additional_fields":["VirusSequences.Sequence", "Peptides.Sequence"]
        }
    }'

echo "Get values without join"
curl -i http://127.0.0.1:6543/api/get-data -X GET -H "Content-Type: application/json" --data '{
        "payload": {
            "query":{
                "Peptides.Score": {
                    "type": "float",
                    "range": [0.7, 1]
                }
            },
            "limit": 3,
            "sort": {
              "field": "Peptides.Score",
                  "direction": "DESC"
            },
            "additional_fields":["Peptides.Sequence"]
        }
    }'

echo "Get peptides with a score >=0.7"
curl -i http://127.0.0.1:6543/api/get-data -X GET -H "Content-Type: application/json" --data '{
        "payload": {
            "query":{
                "Peptides.Score": {
                    "type": "float",
                    "range": [0.7, ":"]
                }
            },
            "limit": 3,
            "sort": {
              "field": "Peptides.Score",
                  "direction": "DESC"
            },
            "additional_fields":["Peptides.Sequence"]
        }
    }'

echo "Get peptides with a index >=10"
curl -i http://127.0.0.1:6543/api/get-data -X GET -H "Content-Type: application/json" --data '{
        "payload": {
            "query":{
                "Peptides.Index": {
                    "type": "float",
                    "range": [10, ":"]
                }
            },
            "limit": 3,
            "sort": {
              "field": "Peptides.Score",
                  "direction": "DESC"
            },
            "additional_fields":["Peptides.Sequence", "Peptides.Index"]
        }
    }'
