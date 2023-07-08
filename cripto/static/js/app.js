const getMovements = () => {

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


document.addEventListener("DOMContentLoaded", function(event) {
    const movements = getMovements()//código a ejecutar cuando existe la certeza de que el DOM está listo para recibir acciones
});

