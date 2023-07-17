const currencies = ["EUR",'BTC','ETH','USDT','BNB','XRP','ADA','SOL','DOT','MATIC']

const getCurrenciesTo = () => {
    for (const currency of currencies){
       option = `<option value="${currency}">${currency}</option>`

       toCurrency.innerHTML += option
    }
}

const getCurrenciesFrom = () => {
    const url = '/api/v1/wallets'
   
    fetch(url)
        .then(response => response.json())
        .then(function(res){
            console.log(res)
            if(res.data.length >= 1){
                fromCurrency.options.length=1 // remove all options firstly
                console.log('por aqui');
                const wallets = res.data
                for (const currency of wallets){
                    
                    option = `<option value="${currency}">${currency}</option>`
             
                    fromCurrency.innerHTML += option
                    
                 }
                 
            } else {

                option = `<option value="EUR">EUR</option>`
                fromCurrency.innerHTML += option
                
            }
        })
}


const getMovements = () => { 
    const url = '/api/v1/movimientos'

    fetch(url)
        .then(response => response.json())
        .then(function(res){
            console.log(res)
            const movementsData = res;
            if (movementsData.status == 'success'){
                if(movementsData.data.length == 0){
                    return noResultsFound()
                }else {
                    
                    tableEmpty.innerHTML = ''
                    return showMovements(movementsData.data)
                }
               
            }else{  // creo que esto hay que meterlo en el catch
                alert(`Error ${movementsData.mensaje}`)
            }
        })
        .catch(processError)
      
}

const showMovements = (movements) => {

    
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

const noResultsFound = () => {
    let emptyMessage = ' <div class="alert alert-primary text-center" role="alert">No hay registros</div>'
    tableEmpty.innerHTML = emptyMessage
}

const getRate = () => {

    const value_from = fromCurrency.value;
    const value_to = toCurrency.value;
    const qtyInput = qty.value

    const validate = validation(value_from,value_to,qtyInput)

    if(validate){
        const url = `/api/v1/tasa/${value_from}/${value_to}`
        fetch(url)
            .then(response => response.json())
            .then(function(data){
                let range = data.rate
                pu.innerHTML = `PU: ${range}`
                puInput.value = range
                const change = qtyInput / range
                result.innerHTML = `Q: ${change}`
                resultInput.value= change
                btnSaveMovement.disabled = false
                })
            .catch(processError)
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

    const moneda_from = fromCurrency.value
    const moneda_to   = toCurrency.value
    const cantidad_from = qty.value
    const cantidad_to = resultInput.value

    const url = '/api/v1/movimiento'
    let data = {
        "moneda_from": moneda_from,
        "cantidad_from": parseFloat(cantidad_from),
        "moneda_to"  : moneda_to ,
        "cantidad_to": cantidad_to
    }

    let fechData = {
        method:'POST',
        body:JSON.stringify(data),
        headers:{
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    }

    fetch(url, fechData)
        .then(response => response.json())
        .then(processInsert)
        .catch(processError)
}

const processInsert = (data) => {
    console.log(data);
    if(data.status === 'success') {
        if(data.message){
            return data.message
        }  else if(data.id){
            let tableBody = document.querySelector('#movements-table tbody')
            tableBody.innerHTML = ''
            qty.value = ""
            resetSelect(fromCurrency)
            resetSelect(toCurrency)
            result.innerHTML="Q:"
            pu.innerHTML="PU"
            btnSaveMovement.disabled = true
            getCurrenciesFrom()
            getMovements()
            getWallets()
        } else{
          // REVISAR alert(`Se ha producido un error: ${data.data}`) // revisAR
          processError(data.data)
          btnSaveMovement.disabled = true
        }
    } else{
        processError(data.message)
        btnSaveMovement.disabled = true
    }
}

const processError = (error) =>{
    alert('Se ha producido el siguiente error: ' + error)
}

const resetSelect = (select) =>{
    for (var i = 0, l = select.length; i < l; i++) {
        select[i].selected = select[i].defaultSelected;
    }
}




