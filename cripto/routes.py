from datetime import datetime
from cripto import app
from flask import render_template, request
from cripto.model.movement import Movement, MovementDAO
from cripto.model.change import Rates
from cripto.model.status import Status
from cripto.config import path_database
import sqlite3

dao = MovementDAO(path_database)
status = Status(path_database)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/movimientos', methods=['GET'])
def get_all():
    try:
        # comment: 
        movements = dao.get_all()
        response = {
            "status": "success",
            "data" : movements
        }
        return response
    except sqlite3.Error as e:
        response = {
            "status":"fail",
            "mensaje": str(e)
        }
        return response, 400
    # end try

@app.route('/api/v1/tasa/<from_moneda>/<to_moneda>', methods=['GET'])
def get_rates(from_moneda,to_moneda):
    rates = Rates(from_moneda,to_moneda)
    rate = rates.get_rate()
    
    return rate

@app.route('/api/v1/movimiento', methods=['POST'])
def insert():

    try:
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        moneda_from = request.json['moneda_from']
        cantidad_from = request.json['cantidad_from']
        moneda_to = request.json['moneda_to']
        cantidad_to = request.json['cantidad_to']
        
        res = dao.insert(Movement(date,time,moneda_from,cantidad_from,moneda_to,cantidad_to))
        print(res) 
        """ response = {
        "is_ok": True,
        "data": None
        } """
        
        return res
    except ValueError as e:
        response = {
            "status": 'fail',
            "data": str(e)
        }
        return response
    except sqlite3.Error as e:
        response = {
            "status": 'fail',
            "data": "Error en base de datos."
        }
    return response
        

@app.route('/api/v1/status', methods=['GET'])
def get_status():
    try:
        wallets, actual_value = status.wallet ()
        prices = status.price()

        if len(wallets) > 0 : 
            response = {
                "status" :'success',
                "data": {
                    "wallet": wallets,
                    "price": prices,
                    "actual_value": actual_value
                }
            }
        else :
            response = {
                "status": 'fail',
                "data": 'No hay registros aún'
            
        }
        return response
    
    except ValueError as e:
        response = {
            "status": 'fail',
            "data": str(e)
        }
        return response
    except sqlite3.Error as e:
        response = {
            "status": 'fail',
            "data": "Error en base de datos."
        }
    return response


@app.route('/api/v1/wallets')
def get_wallets():
    try:
        wallets = dao.get_wallets()
        response = {
            "status":"success",
            "data": wallets
        }
        return response

    except sqlite3.Error as e:
        response = {
            "status":"fail",
            "mensaje": str(e)
        }
        return response
