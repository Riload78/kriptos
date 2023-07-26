from flask import app
import requests
from cripto.config import apikey
from cripto.helper.json import to_json
import json
import decimal

class Rates():
    def __init__(self, currency, cripto):
        self.currency = currency
        self.cripto = cripto
        
    def get_rate(self):
        url = f"https://rest.coinapi.io/v1/exchangerate/{self.cripto}/{self.currency}?apikey={apikey}"
        
        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                res = ('status','succes'), ('rate',data['rate']), ('monedas',['EUR','Falta definir monendas posibles???'])
                data = to_json(res)
                return data
            else:
                res = ('status','fail'),('message', data["error"])
                data = to_json(res)
                return data
        except Exception as e:
            res = ('status','fail'),('message', 'Error en la llamada a CoinApi.io')
            data = to_json(res)
            return data
            
    
    def get_changes(self, currency):
        url =  f'https://rest.coinapi.io/v1/exchangerate/{currency}?apikey={apikey}' 
           
        try:
            response = requests.get(url)
            data = response.content

            diccionario = json.loads(data)
            new_currencies = []
            if response.status_code == 200:
                currencies = diccionario.get('rates')
                
                for currency in currencies:
                    rate_float = currency.get('rate')
                    numero_decimal_str = '{:.25f}'.format(rate_float)
                    rate = float(numero_decimal_str)
                    currency = currency.get('asset_id_quote')
                    new_currencies.append({
                        'asset_id_quote': currency,
                        'rate': rate
                    })
                    
                return new_currencies
            
            else: 
                res = json.loads(response.text)
                msg = res['error']
                mensaje_json = json.loads(msg)
                mensaje = mensaje_json['error']
                error = {
                    'message': mensaje,
                    'status' : 'fail'
                }
                return error
        
        except Exception as e:
            error = {
                    'message': 'Error en la llamada a CoinApi.io',
                    'status' : 'fail'
                }
            return error
        