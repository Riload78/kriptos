const calculateRate = document.querySelector('#calculate-rate')
const btnSaveMovement = document.querySelector('#save-movement')
const fromCurrency = document.querySelector('#from')
const toCurrency = document.querySelector('#to')
const qty = document.querySelector('#qty')
const pu = document.querySelector('#result-pu .form-label')
const result = document.querySelector('#result-q .form-label')
const puInput = document.querySelector('#pu-hidden')
const resultInput = document.querySelector('#qty-hidden')
const tableBody = document.querySelector('#movements-table tbody')
const tableEmpty =  document.querySelector('#empty')

/* Balance */
const updateBtn = document.querySelector('#update-state')
const balanceList = document.querySelector('#balance-list')
const kripto = document.querySelector('#kripto')
const kritoBalance = document.querySelector('#kripto-balance')
const kriptoValue = document.querySelector('#kripto-value')
const value = document.querySelector('#value')
const price = document.querySelector('#price')
const resultBalance = document.querySelector('#result')



document.addEventListener("DOMContentLoaded", function(event) {
    getMovements()
    getCurrenciesTo()
    getCurrenciesFrom()
    
    calculateRate.addEventListener('click', getRate)
    btnSaveMovement.addEventListener('click', saveMovement)
    updateBtn.addEventListener('click',getWallets)
    

});

