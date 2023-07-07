from flask import app
import requests
from config import apikey
from helper.date import convert_date
import json

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
                return True, data['rate']
            else:
                return False, data["error"]
        except requests.exceptions.RequestException as e:
            return False, str(e)
        
    def get_list_cripto(self):
        url = f"https://rest.coinapi.io/v1/assets?apikey={apikey}"
        try:
            response = requests.get(url)
            data = response.content

            diccionario = json.loads(data)

            list_cryptos = []
            if response.status_code == 200:
                for cripto in diccionario:
                    #date = convert_date(cripto['data_trade_end'])
                   
                    if cripto['type_is_crypto'] == 1 :
                        list_cryptos.append((cripto['name'],cripto['asset_id']))
                       
                        
                return True, list_cryptos
            else:
                return False, data["error"]
        except requests.exceptions.RequestException as e:
            return False, str(e)
        

data = Rates('EUR','ETMN')
change = data.get_rate()
crypto_list = data.get_list_cripto()
print(crypto_list)
print(change)
