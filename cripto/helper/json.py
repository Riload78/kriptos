import json

def to_json(data):
    diccionario = dict(data)
    jsonStr = json.dumps(diccionario)
    
    return jsonStr