import json

def to_json(data):
    diccionario = dict(data)
    jsonStr = json.dumps(diccionario)
    
    return jsonStr

def validate_dic(diccionario):
    for key, value in diccionario.items():
        if value is None:
            return {'EUR' : 0} 

    return {key : value} 
