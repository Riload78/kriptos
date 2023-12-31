import pytest
from datetime import datetime
from cripto.model.movement import Movement

def test_create_movement():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    m = Movement(date,time,"EUR",1000,"BTC",0.23)
    assert m.date == date
    assert m.time == time
    assert m.moneda_from == "EUR"
    assert m.cantidad_from == 1000
    assert m.moneda_to == "BTC"
    assert m.cantidad_to == 0.23
    
def test_fails_date_not_equal():
    with pytest.raises(ValueError):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        m = Movement('2023-01-05',time,"EUR",1000,"BTC",0.23)

def test_fails_time_not_equal():
    with pytest.raises(ValueError):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        m = Movement(date,'12:03:15',"EUR",1000,"BTC",0.23)
        
def test_moneda_from_equal_euro():        
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    m = Movement(date,time,"EUR",1000,"BTC",0.23)
    assert m.moneda_from == "EUR"
    
def test_moneda_from_not_in_currencies():
    with pytest.raises(ValueError):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        m = Movement(date,time,"HHH",1000,"BTC",0.23)
        

## Falta por comprobar -> Hay que hecer el método que se traiga el saldo 
# antes de grabar el movimiento
def test_moneda_from_not_equal_euro():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    m = Movement(date,time,"ETH",1000,"BTC",0.23)
    
def test_cantidad_from_not_cero():
    with pytest.raises(ValueError):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        m = Movement(date,time,"EUR",0,"BTC",0.23)
        
def test_moneda_to_equal_euro():        
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    m = Movement(date,time,"BTC",1000,"EUR",0.23)
    assert m.moneda_to == "EUR"
    
def test_moneda_to_not_in_currencies():
    with pytest.raises(ValueError):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        m = Movement(date,time,"HHH",1000,"BTC",0.23)
        
def test_cantidad_to_not_cero():
    with pytest.raises(ValueError):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        m = Movement(date,time,"EUR",0,"BTC",0)
