from datetime import date
import sqlite3
import os
from cripto.helper.json import to_json

CURRENCIES = ("EUR", "USD")

class Movement:
    def __init__(self, input_date, abstract, amount, currency, id = None):
        self.date = input_date
        self.id = id

        self.abstract = abstract
        self.amount = amount
        self.currency = currency

    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        self._date = date.fromisoformat(value)
        if self._date > date.today():
            raise ValueError("date must be today or lower")
        
    @property
    def amount(self):
        return self._amount
    
    @amount.setter
    def amount(self, value):
        self._amount = float(value)
        if self._amount == 0:
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
        return self.date == other.date and self.abstract == other.abstract and self.amount == other.amount and self.currency == other.currency

    def __repr__(self):
        return f"Movimiento: {self.date} - {self.abstract} - {self.amount} {self.currency}"

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

        query = """
        INSERT INTO criptos
               (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (movement.date, movement.abstract,
                            movement.amount, movement.currency))
        conn.commit()
        conn.close()

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
        
    def to_dict(self):
        return{
            "id": self.id,
            "date": str(self.date),
            "abstract": self.abstract,
            "amount": float(self.amount),
            "currency": self.currency
            
        }


