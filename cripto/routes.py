from datetime import datetime
from cripto import app
from flask import render_template, request
from cripto.model.movement import Movement, MovementDAO
from cripto.model.change import Rates
from cripto.config import path_database

##config = app.config
dao = MovementDAO(path_database)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/movimientos', methods=['GET'])
def get_all():
    movements = dao.get_all()
    return movements 

@app.route('/api/v1/tasa/<from_moneda>/<to_moneda>', methods=['GET'])
def get_rates(from_moneda,to_moneda):
    rates = Rates(from_moneda,to_moneda)
    rate = rates.get_rate()
    
    return rate

@app.route('/api/v1/movimiento', methods=['GET','POST'])
def insert():

    if request.method == "GET":
        return 'Respuesta del post'
    
    else:
        
        try:
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M:%S")
            moneda_from = request.json['moneda_from']
            cantidad_from = request.json['cantidad_from']
            moneda_to = request.json['moneda_to']
            cantidad_to = request.json['cantidad_to']
            
            dao.insert(Movement(date,time,moneda_from,cantidad_from,moneda_to,cantidad_to))
            
            postman = f"Date:{date}\nTime: {time}\nMoneda_from: {moneda_from}\nCantidad_from: {cantidad_from}\nMoneda_to: {moneda_to}\nCantidad_to: {cantidad_to}"
            return (postman, 200, {"Access-Control-Allow-Origin": "*"})
        except Exception as e:
            raise e
        # end try
        

@app.route('/api/v1/status', methods=['GET'])
def get_status():
    return 'Status'