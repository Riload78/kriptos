from flask import make_response, jsonify
from datetime import datetime
import sqlite3
import os
from cripto.helper.json import to_json
from cripto.model.status import Status
from cripto.config import path_database

CURRENCIES = ("EUR", "BTC", "ETH", "USDT", "BNB", "XRP", "ADA", "SOL", "DOT", "MATIC")

status = Status(path_database)

class Movement:
    def __init__(self, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, id = None):
        self.id = id
        self.date = date
        self.time = time
        self.moneda_from = moneda_from
        self.cantidad_from = cantidad_from
        self.moneda_to = moneda_to
        self.cantidad_to = cantidad_to
        

        """ self.abstract = abstract
        self.amount = amount
        self.currency = currency """

    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        now = datetime.now()
        self._date = value
        if self._date != now.strftime("%Y-%m-%d"):
            raise ValueError("date must be today")
        
    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, value):
        now = datetime.now()
        self._time = value
        if self._time != now.strftime("%H:%M:%S"):
            raise ValueError("time must be current hour and minute")
        
    @property
    def moneda_from(self):
        return self._moneda_from
    
    @moneda_from.setter
    def moneda_from(self,value):
        self._moneda_from = value
        if self.moneda_from not in CURRENCIES:
            raise ValueError(f"{self.moneda_from} is an invalid currency code.")
       
        
    @property
    def cantidad_from(self):
        return self._cantidad_from
    
    @cantidad_from.setter
    def cantidad_from(self, value):
        self._cantidad_from = float(value)
        if self._cantidad_from == 0:
            raise ValueError("amount must be positive or negative")
        
    @property
    def moneda_to(self):
        return self._moneda_to
    
    @moneda_to.setter
    def moneda_to(self,value):
        self._moneda_to = value
        if self.moneda_to not in CURRENCIES:
            raise ValueError(f"{self.moneda_to} is an invalid currency code.")  
        
    @property
    def cantidad_to(self):
        return self._cantidad_to
    
    @cantidad_to.setter
    def cantidad_to(self, value):
        self._cantidad_to = float(value)
        if self._cantidad_to == 0:
            raise ValueError("amount must be positive or negative")
    
    @property
    def currency(self):
        return self._currency
    
    @currency.setter
    def currency(self, value):
        self._currency = value
        if self._currency not in CURRENCIES:
            raise ValueError(f"currency must be in {CURRENCIES}")

    def __eq__(self, other):
        return self.date == other.date and self.time == other.time and self.moneda_from == other.moneda_from and self.cantidad_from == other.cantidad_from and self.moneda_to == other.moneda_to and self.cantidad_to == other.cantidad_to

    def __repr__(self):
        return f"Movimiento: {self.date} - {self.time} - {self.moneda_from} - {self.cantidad_from} - {self.moneda_to} - {self.cantidad_to}"
    
    

class MovementDAO:
    def __init__(self, db_path):
        self.path = db_path
        # Falta por comprobar -> Borrar BBDD y probar si la crea
        if not os.path.isfile(db_path):
            print('aqui')
            try:
       
                query = """
                    CREATE TABLE IF NOT EXISTS "criptos" (
                        "id" INTEGER,
                        "date" TEXT NOT NULL,
                        "time" TEXT NOT NULL,
                        "moneda_from" TEXT NOT NULL,
                        "cantidad_from" REAL NOT NULL,
                        "moneda_to"	TEXT NOT NULL,
                        "cantidad_to" REAL NOT NULL,
                        PRIMARY KEY("id" AUTOINCREMENT)
                    );
                """
            
                conn = sqlite3.connect(self.path)
                cur = conn.cursor()
                cur.execute(query)
                conn.commit()
                conn.close()
                print("Tabla criptos creada correctamente.")
            except sqlite3.Error as e:
                print(f"Error al crear la tabla criptos: {e}")


    def insert(self, movement):
        # Validar if Moneda_from != EUR : Comprobar saldo 
                try:
                    saldo = self.get_saldo(movement)
                    if movement.moneda_from != "EUR" and saldo >= movement.cantidad_from :
                    
                        query = """
                        INSERT INTO criptos
                            (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """

                        conn = sqlite3.connect(self.path)
                        cur = conn.cursor()
                        cur.execute(query, (movement.date, movement.time,movement.moneda_from, movement.cantidad_from,
                                            movement.moneda_to, movement.cantidad_to))
                        conn.commit()
                        conn.close()
                        
                        #self.set_response('status','success'), ('id','Id creado ???'), ('monedas', ["EUR", "...Esto hay que terminar"])
                        return self.set_response({
                            'status':'success',
                            'id':'Id creado ???',
                            'monedas': ["EUR", "...Esto hay que terminar"]
                        })
                    elif movement.moneda_from != "EUR" and saldo < movement.cantidad_from :
                        response = {
                            'status':'faild',
                            'message':'Saldo insuficiente'
                            
                        }
                        return response
                    elif movement.moneda_from == "EUR":
                         # comment: 
                        query = """
                        INSERT INTO criptos
                            (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """

                        conn = sqlite3.connect(self.path)
                        cur = conn.cursor()
                        cur.execute(query, (movement.date, movement.time,movement.moneda_from, movement.cantidad_from,
                                            movement.moneda_to, movement.cantidad_to))
                        conn.commit()
                        conn.close()

                        response = {
                            'status':'success',
                            'id':'Nuevo id creado',
                            'monedas':['EUR','....']
                        }
                        
                        return response
                    
                except Exception as e:
                    
                    response = {
                        'status':'fail',
                        'message':str(e)
                    }
                    return response
                   

    def set_response(self,response):
           res = make_response(jsonify(response))
           return res
                   
        
    def get_saldo(self, movement):

        
        cantidades_to = self.get_cantidades_to(movement.moneda_from)
        cantidades_from = self.get_cantidades_from(movement.moneda_from)
        result = cantidades_to - cantidades_from
       
        
        return result
    # Mirar si puedo mejorar la lllamda para que se haga en una sola funcion
    def get_cantidades_to(self, moneda_to):
        
        query = """
            SELECT IFNULL(SUM(cantidad_to), 0) AS sumatorio
            FROM criptos
            WHERE moneda_to = ?
            """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query,(moneda_to,))
        res = cur.fetchone()
        conn.close()
        if res :
            print(res)
            if res[0] == None:
                print(res[0])
          
                return 0
            else:
                return res[0]
        else:
            response = {
                        'status':'fail',
                        'message':'No se ha podido traer los datos'
                    } 
            return response
        
    
    def get_cantidades_from(self, moneda_from):
        query = """
            SELECT IFNULL(SUM(cantidad_from),0) AS sumatorio_from
            FROM criptos
            WHERE moneda_from = ?
            """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query,(moneda_from,))
        res = cur.fetchone()
        conn.close()
        if res :
            print(res)
            if res[0] == 0:
                print(res[0])
                query = """
                    SELECT IFNULL(SUM(cantidad_to),0) AS sumatorio_to
                    FROM criptos
                    WHERE moneda_from = ?
                    """
                conn = sqlite3.connect(self.path)
                cur = conn.cursor()
                cur.execute(query,(moneda_from,))
                res = cur.fetchone()
                conn.close()
                if res:
                    print(res)
                    if res[0] == 0:
                        print(res[0])
                        return 0
                    else:
                        return -res[0]
                else:  
                    
                    response = {
                        'status':'fail',
                        'message':'No se ha podido traer los datos'
                    } 
                    return response
            else:
                return res[0]
        else:
            response = {
                        'status':'fail',
                        'message':'Nose ha podido traer los datos'
                    } 
            return response
    

        
    def get_all(self):
        
        try:
            query = """
                SELECT id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to
                FROM criptos
                ORDER by id;
            """
            conn = sqlite3.connect(self.path)
            cur = conn.cursor()
            cur.execute(query)
            res = cur.fetchall()
            movimientos = []
            for reg in res:
                movimientos.append(
                    {
                        "id": reg[0],
                        "date": reg[1],
                        "time": reg[2],
                        "moneda_from": reg[3],
                        "cantidad_from": reg[4],
                        "moneda_to": reg[5],
                        "cantidad_to": reg[6]
                    }
                )
                
            conn.close()
            
            return movimientos
        
        except sqlite3.Error as e:
            # Manejo de la excepción específica de SQLite
            error_message = f"Error de SQLite: {str(e)}"
            return error_message
        
        
    # en principio no se va usar -> eliminar en el repaso del codigo si procede    
    def to_dict(self):
        return{
            "id": self.id,
            "date": str(self.date),
            "abstract": self.abstract,
            "amount": float(self.amount),
            "currency": self.currency
            
        }
        
    def get_wallets(self):
        try:

            query = """ 
                SELECT DISTINCT moneda_to 
                FROM "criptos"; 
            """
            
            conn = sqlite3.connect(self.path)
            cur = conn.cursor()
            cur.execute(query)
            res = cur.fetchall()
            wallets = ["EUR"]
 
            
            if res :
                for reg in res:
                    if reg[0] != 'EUR':
                        wallets.append(reg[0])
                
                return wallets
            
            else :
                
                return wallets
                
        except sqlite3.Error as e:
            error_message = f"Error de SQLite: {str(e)}"
            return ('status','fail'), ('mensaje',error_message)
        
        

