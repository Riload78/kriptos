import sqlite3
from cripto.helper.json import to_json
from cripto.model.change import Rates

rates = Rates('EUR','BTC')

class Status():
    def __init__(self, db_path):
        self.db_path = db_path
            
    def wallet(self):
        #Recoge al saldo de todas las criptomonedas registradas
        #traerme el listado de monedas de las BBDD
            #get_kriptos
        kriptos_from = self.get_kriptos_from('moneda_from','cantidad_from')
        kriptos_to = self.get_kriptos_to('moneda_to','cantidad_to')
        print('Kriptos_from:',kriptos_from)
        print('Kriptos_to:',kriptos_to)
        #para cada una de las monedas que h
        ## unir dos diccionarios que puedan tener mismas claves. 
        ## En caso de que tengan mismas claves el valor sera la resta de uno y otro
        result = {}
        for key, value in kriptos_to.items():
            if key in kriptos_from:
                result[key] = value - kriptos_from[key]
            else:
                result[key] = value
        # Agregar las claves únicas de dict2 que no estan en dic1 y las agrega a result pero con signmo negativo
        for key, value in kriptos_from.items():
            if key not in kriptos_to:
                result[key] = -value
                
        wallets = result
        values = self.value()
        new_wallet = []
        
        for wallet, balance in wallets.items():
            for rate in values:
                if rate.get('asset_id_quote') ==  wallet:
                    rate_float = rate['rate']
                    numero_decimal_str = '{:.25f}'.format(rate_float)
                    value= 1/float(numero_decimal_str)

                    new_wallet.append({
                        wallet:{
                            "balance": balance,
                            "value": value
                        }
                    })
                    
                
        return new_wallet
        # Por cada moneda tengo que ver 
    
    def price(self):
        
       price_to = self.price_to()
       price_from = self.price_from()
       precio_compra = price_to.get('EUR') - price_from.get('EUR') 
       
       return precio_compra
        
    
    def value(self):
        # tengo el diicionarario de cambios
        rates_collection = rates.get_changes('EUR')
        return rates_collection 
    
    def get_kriptos_from(self, tabla, cantidad):
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
            raise e
        
    def get_kriptos_to(self, tabla, cantidad):
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
            raise e
    
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
            return data   
        
        except Exception as e:
            raise e 
        
        
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
            return data   
        
        
                 
        except Exception as e:
            raise e 