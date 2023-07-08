import json
from cripto import app
from flask import render_template
from cripto.model.movement import MovementDAO
from cripto.model.change import Rates

##config = app.config
dao = MovementDAO(app.config.get('PATH_SQLITE', 'valor_por_defecto'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/all', methods=['GET'])
def get_all():
    movements = dao.get_all()
    return 'HOLA API'

@app.route('/api/v1/tasa/<from_moneda>/<to_moneda>', methods=['GET'])
def get_rates(from_moneda,to_moneda):
    rates = Rates(from_moneda,to_moneda)
    rate = rates.get_rate()
    print(rate)
    diccionario = dict(rate)
    #convert to JSON string
    jsonStr = json.dumps(diccionario)
    
    return jsonStr

@app.route('/api/v1/movimiento', methods=['POST'])
def insert():
    return 'Creacion de movimiento'

@app.route('/api/v1/status', methods=['GET'])
def get_status():
    return 'Status'