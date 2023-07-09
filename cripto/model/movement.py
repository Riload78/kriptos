from datetime import datetime
import sqlite3
import os
from cripto.helper.json import to_json

CURRENCIES = ("EUR", "BTC", "ETH", "USDT", "BNB", "XRP", "ADA", "SOL", "DOT", "MATIC")

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
            query = """
                CREATE TABLE "criptos" (
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
            conn.close()

    def insert(self, movement):
        # Validar if Moneda_from != EUR : Comprobar saldo 
        if movement.moneda_from == "EUR" or self.get_saldo(movement.moneda_from) == True:
            try:
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
                
                return ('status','success'), ('id','Id creado ???'), ('monedas', ["EUR", "...Esto hay que terminar"])
                
            except Exception as e:
                return ('status','fail'), ('mensaje',str(e))
            # end try
        else:
           
            return ('status','fail'), ('mensaje','Mensaje de error. ultimo else del insert')
                   
        
    def get_saldo(self,moneda):

        saldo = self.get_cantidades_to(moneda) - self.get_cantidades_from(moneda)
        
        print(saldo)
        if saldo > 0 :
            return True
        else :
            return ('status','fail'), ('mensaje','Saldo insificiente')
    
    def get_cantidades_to(self, moneda):
        
        query = """
            SELECT SUM(cantidad_to) AS sumatorio
            FROM criptos
            WHERE MONEDA_TO = ?
            """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query,(moneda,))
        res = cur.fetchone()
        conn.close()
        if res :
            print(type(res[0]))
            return res[0]
        else:
            return 'get_cantidades_to respuesta de error. Revisar'
        
    
    def get_cantidades_from(self, moneda):
        query = """
            SELECT SUM(cantidad_from) AS sumatorio
            FROM criptos
            WHERE MONEDA_TO = ?
            """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query,(moneda,))
        res = cur.fetchone()
        conn.close()
        if res :
            print(type(res[0]))
            return res[0]
        else:
            return 'get_cantidades_from respuesta de error. Revisar'
    
    
    
    # en principio no se va usar -> eliminar en el repaso del codigo si procede
    def get(self, id):
        query = """
        SELECT id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to
          FROM criptos
         WHERE id = ?;
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (id,))
        res = cur.fetchone()
        conn.close()
        if res:
            return Movement(*res)

        
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
            
            response = ("status","succes"),('data',movimientos)
            data = to_json(response)
            
            return data
        
        except sqlite3.Error as e:
            # Manejo de la excepción específica de SQLite
            error_message = f"Error de SQLite: {str(e)}"
            return error_message
        
    # en principio no se va usar -> eliminar en el repaso del codigo si procede
    def update(self, id, movement):
        query = """
        UPDATE criptos
           SET date = ?, abstract = ?, amount = ?, currency = ?
         WHERE id = ?;
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (movement.date, movement.abstract, movement.amount, movement.currency, id))
        conn.commit()
        conn.close()
        
        
    # en principio no se va usar -> eliminar en el repaso del codigo si procede    
    def to_dict(self):
        return{
            "id": self.id,
            "date": str(self.date),
            "abstract": self.abstract,
            "amount": float(self.amount),
            "currency": self.currency
            
        }


