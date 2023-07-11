const currencies = ["EUR",'BTC','RTH','USDT','BNB','XRP','ADA','SOL','DOT','MATIC']

const getCurrenciesyTo = () => {
    for (const currency of currencies){
       option = `<option value="${currency}">${currency}</option>`

       toCurency.innerHTML += option
    }
}

const gerCurrenciesFrom = () => {

}


const getMovements = () => {  // cambiar llamada a fetch  y quitar axios

    axios.get('http://127.0.0.1:5001/api/v1/movimientos')
      .then(function (response) {
        // función que se ejecutará al recibir una respuesta
        
        
        const movementsData = response.data;
        if (movementsData.status == 'succes'){
            showMovements(movementsData.data)
           
        }else{  // creo que esto hay que meterlo en el catch
            alert(`Error ${movementsData.mensaje}`)
        }
      })
      .catch(function (error) {
        // función para capturar el error
        console.log(error);
      })
      .then(function () {
        // función que siempre se ejecuta
        console.log('en then');
      });
}

const showMovements = (movements) => {

    let tableBody = document.querySelector('#movements-table tbody')
    movements.forEach((movement) => {

        let item = `<tr>  
                        <td>${movement.id}</td>
                        <td>${movement.date}</td>
                        <td>${movement.time}</td>
                        <td>${movement.moneda_from}</td>
                        <td>${movement.cantidad_from}</td>
                        <td>${movement.moneda_to}</td>
                        <td>${movement.cantidad_to}</td>
                    </tr>`

        tableBody.innerHTML += item
    })
}

const getRate = () => {

    const value_from = fromCurrency.value;
    const value_to = toCurency.value;
    const qtyInput = qty.value

    const validate = validation(value_from,value_to,qtyInput)

    if(validate){
        const url = `/api/v1/tasa/${value_from}/${value_to}`
        fetch(url)
            .then(response => response.json())
            .then(function(data){
                console.log(data);
                let range = data.rate
                pu.innerHTML = `PU: ${range}`
                puInput.value = range
                const change = qtyInput / range
                result.innerHTML = `Q: ${change}`
                resultInput.value= change
            })
        }
}


const validation = (field1,filed2,qty) => {
    if(field1 === '' || filed2 ==='' || field1 === filed2 ){
        alert('La compra/venta se tiene que hacer con monedas diferentes')
    } else if(qty <= 0){
        
        alert('La cantidad tiene que ser mayor a 0.')
        
    } else{
        return true
    }
}


const saveMovement = () => {
    console.log('paso por aqui');

}



