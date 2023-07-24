const getWallets = () => {
    balanceList.innerHTML = ''
    price.innerHTML = ''
    emptyInversion.style.display ='block'
    const url = '/api/v1/status'

    fetch(url)
        .then(response => response.json())
        .then((res) => {
            if(res.status == 'success'){
                emptyInversion.innerHTML= ""
                walletList(res.data.wallet)
                getTotals(res.data)

            } else{
            
                error = `<div class="alert alert-danger text-center" role="alert">${res.message}</div>`
                emptyInversion.innerHTML = error
                hideMessage(emptyInversion)
             
            }
        })
        .catch(processError)
}


const walletList = (list) => {
    if (typeof list != undefined){  
        list.forEach((obj, index) => {
            let arr = Object.entries(obj)
    
            let item = ` <li class="list-group-item d-flex justify-content-between lh-sm">
                            <div>
                                <h6 class="my-0">${arr[0][0]}</h6>
                                <small class="text-body-secondary">Unidades: ${arr[0][1]['balance']}</small>
                            </div>
                            <span class="text-body-secondary">Rate: ${arr[0][1]['value'].toFixed(2)}</span>
                        </li>`
    
            balanceList.innerHTML += item
    
        })
    }

}


const getTotals = (list) =>{
    if (typeof list != 'string') {

        let actualValue = list.actual_value.toFixed(2)
        let priceTotal = list.price.toFixed(2)
        let result = actualValue - Math. abs(priceTotal)
        let formatResult =  result.toFixed(2)
    
        priceTotal < 0 ?  price.classList.add('text-danger') : price.classList.remove('text-danger') 
        value.innerHTML = `${actualValue} EUR`

        price.innerHTML = `${priceTotal} EUR`
        formatResult < 0 ? resultBalance.classList.add('text-danger') : resultBalance.classList.remove('text-danger')
        resultBalance.innerHTML = `${formatResult} EUR`
    }


}