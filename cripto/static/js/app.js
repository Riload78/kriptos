const calculateRate = document.querySelector('#calculate-rate')
const btnSaveMovement = document.querySelector('#save-movement')
const fromCurrency = document.querySelector('#from')
const toCurrency = document.querySelector('#to')
const qty = document.querySelector('#qty')
const pu = document.querySelector('#result-pu .form-label')
const result = document.querySelector('#result-q .form-label')
const puInput = document.querySelector('#pu-hidden')
const resultInput = document.querySelector('#qty-hidden')



document.addEventListener("DOMContentLoaded", function(event) {
    getMovements()
    getCurrenciesyTo()
    gerCurrenciesFrom()
    calculateRate.addEventListener('click', getRate)
    btnSaveMovement.addEventListener('click', saveMovement)

});

