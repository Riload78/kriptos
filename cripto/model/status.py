import sqlite3
from cripto.helper.json import to_json, validate_dic
from cripto.model.change import Rates

# Creo que sobra
rates = Rates('EUR','BTC')

class Status():
    def __init__(self, db_path):
        self.db_path = db_path
            
    def wallet(self):

        kriptos_from = self.get_kriptos_from()
        kriptos_to = self.get_kriptos_to()
        if kriptos_from['status'] == 'fail':
            error = kriptos_from['message']
            new_wallet = None
            sum_actual_value = None
            return error, new_wallet, sum_actual_value 
        else:
            result = {}
            
            for key, value in kriptos_to.items():
                if key in kriptos_from:
                    result[key] = value - kriptos_from[key]
                else:
                    result[key] = value
            
            for key, value in kriptos_from.items():
                if key not in kriptos_to:
                    result[key] = -value
                    
            wallets = result
            if wallets:
                rates_collection = rates.get_changes('EUR')
                if 'status' in rates_collection:
                    error = rates_collection['message']
                    new_wallet = None
                    sum_actual_value  = None
                    
                else:
                    error = None
                    new_wallet = []
                    actual_value = []
                    native_rate = ""
                    
                    for wallet, balance in wallets.items():
                        for rate in rates_collection:
                            
                            native_rate = rate.get('asset_id_quote')
                            if str(native_rate) == wallet:
                                rate_float = rate['rate']
                                numero_decimal_str = '{:.25f}'.format(rate_float)
                                val= 1/float(numero_decimal_str)
                                
                                new_wallet.append({
                                    wallet:{
                                        "balance": balance,
                                        "value": val
                                    }
                                })
                                
                                actual_value.append(balance * val)
                    
                    sum_actual_value = sum(actual_value) 
                return error,new_wallet, sum_actual_value 
            else:
                error = 'No hay registros'
                new_wallet = None
                sum_actual_value = None
                return error, new_wallet, sum_actual_value 
 

    
    def price(self):
        
        price_to = self.price_to()
        price_from = self.price_from()

        precio_compra = price_to.get('EUR') - price_from.get('EUR') 
       
        return precio_compra
   
    
    def get_kriptos_from(self):
        try:
            query = """ 
                SELECT DISTINCT moneda_from, SUM(cantidad_from) AS sumatorio
                FROM criptos
                GROUP BY moneda_from
            """
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(query)
            res= cur.fetchall()
            conn.close()
            data = dict(res)
            print(data)
            return data            
            
        except Exception as e:
                    
            response = {
                'status':'fail',
                'message':str(e)
            }
            return response
        
    def get_kriptos_to(self):
        try:
            query = """ 
                SELECT DISTINCT moneda_to, SUM(cantidad_to) AS sumatorio
                FROM criptos
                GROUP BY moneda_to
            """
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(query)
            res= cur.fetchall()
            conn.close()
            data = dict(res)
            print(data)
            return data            
            
        except Exception as e:
                    
            response = {
                'status':'fail',
                'message':str(e)
            }
            return response
    
    def price_from(self):
        try:
            query = """ 
                SELECT DISTINCT moneda_from, SUM(cantidad_from) AS sumatorio
                FROM criptos
                WHERE moneda_from = "EUR"
            
            """
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(query)
            res= cur.fetchall()
            conn.close()
            data = dict(res)
            print(data)
            result = validate_dic(data)
            return result   
        
        except Exception as e:
                    
            response = {
                'status':'fail',
                'message':str(e)
            }
            return response
        
        
    def price_to(self):
        try:
            query = """ 
                SELECT DISTINCT moneda_to, SUM(cantidad_to) AS sumatorio
                FROM criptos
                WHERE moneda_to = "EUR"
            
            """
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(query)
            res= cur.fetchall()
            conn.close()
            data = dict(res)
            print(data)
            result = validate_dic(data)
            return result  
        
        
                 
        except Exception as e:
                    
            response = {
                'status':'fail',
                'message':str(e)
            }
            return response 