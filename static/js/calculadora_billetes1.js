// Inicializando objeto donde se van a agregar los totales por billetes
var valores = new Object();
var sumar_todo = 0;

// sumatoria de un peso
document.getElementById('id_un_peso').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('id_un_peso').value;
    // Multiplicar por 1
    const resultado = numero * 1;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.uno = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_un_peso').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// tres_pesos
document.getElementById('id_tres_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('id_tres_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 3;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.tres = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_tres_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// cinco_pesos
document.getElementById('id_cinco_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('id_cinco_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 5;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.cinco = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_cinco_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// dies_pesos
document.getElementById('id_diez_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('id_diez_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 10;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.diez = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_diez_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// viente_pesos
document.getElementById('id_veinte_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('id_veinte_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 20;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.veinte = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_veinte_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// cincuenta_pesos
document.getElementById('id_cincuenta_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('id_cincuenta_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 50;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.cincueta = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_cincuenta_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// cien_pesos
document.getElementById('id_cien_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('id_cien_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 100;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.cien = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_cien_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// docientos_pesos
document.getElementById('id_doscientos_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('id_doscientos_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 200;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.doscientos = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_doscientos_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// quinietos_pesos
document.getElementById('id_quinientos_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('id_quinientos_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 500;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.quinientos = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_quinientos_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// mil_pesos
document.getElementById('id_mil_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('id_mil_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 1000;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.mil = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_mil_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// Función para sumar todos los valores de los billetes
function calcular() {
    
    // sumar_todo = 0;
    for(let clave in valores) {
        sumar_todo += valores[clave];
    }
    document.getElementById('id_total').value = sumar_todo;
    document.getElementById('id_total_span').innerHTML =  '$ ' + new Intl.NumberFormat().format(sumar_todo);
    // document.getElementById('input_total').value = sumar_todo;
    // document.getElementById('resultado_0_peso').value = sumar_todo;
    console.log(`sumando da como resultado: ${sumar_todo}`)
}

// Observando lo que se va calculado por billetes y sumado
// document.querySelectorAll('.entrada').forEach(function(input) {
document.querySelectorAll('#formulario').forEach(function(input) {
    input.addEventListener('input', calcular);
})


// Función para limpiar de valores todos los input
function reset() {
    document.getElementsById("formulario").reset();
}

window.onload = function() {
    // Total
    const total = document.getElementById('id_total')
    if (total.value.trim() !== '') {
        const nuevoValor = '$ ' + total.value;
        // Selecciona el span correspondiente
        let span = document.querySelector('#id_total_span');
        // Coloca el nuevo valor en el 
        span.textContent = nuevoValor;
    }

    // un pesos
    const un = document.getElementById('id_un_peso')
    if (un.value.trim() !== '' && un.value !== '0') {
        const nuevoValor = '$ ' + un.value * 1;
        valores.uno = un.value * 1;
        // Selecciona el span correspondiente
        let span = document.querySelector('#resultado_un_peso');
        // Coloca el nuevo valor en el 
        span.textContent = nuevoValor;
    }

    // tres pesos
    const tres = document.getElementById('id_tres_pesos')
    if (tres.value.trim() !== '' && tres.value !== '0') {
        const nuevoValor = '$ ' + tres.value * 3;
        valores.tres = tres.value * 3;
        // Selecciona el span correspondiente
        let span = document.querySelector('#resultado_tres_pesos');
        // Coloca el nuevo valor en el 
        span.textContent = nuevoValor;
    }

    // cinco pesos
    const cinco = document.getElementById('id_cinco_pesos')
    if (cinco.value.trim() !== '' && cinco.value !== '0') {
        let nuevoValor = '$ ' + cinco.value * 5;
        valores.cinco = cinco.value * 5;
        // Selecciona el span correspondiente
        let span = document.querySelector('#resultado_cinco_pesos');
        // Coloca el nuevo valor en el 
        span.textContent = nuevoValor;
    }

    // diez pesos
    const diez = document.getElementById('id_diez_pesos')
    if (diez.value.trim() !== '' && diez.value !== '0') {
        const nuevoValor = '$ ' + diez.value * 10;
        valores.diez = diez.value * 10;
        // Selecciona el span correspondiente
        let span = document.querySelector('#resultado_diez_pesos');
        // Coloca el nuevo valor en el 
        span.textContent = nuevoValor;
    }

    // veinte pesos
    const veinte = document.getElementById('id_veinte_pesos')
    if (veinte.value.trim() !== '' && veinte.value !== '0') {
        const nuevoValor = '$ ' + veinte.value * 20;
        valores.veinte = veinte.value * 20;
        // Selecciona el span correspondiente
        let span = document.querySelector('#resultado_veinte_pesos');
        // Coloca el nuevo valor en el 
        span.textContent = nuevoValor;
    }

    // cincuenta pesos
    const cincuenta = document.getElementById('id_cincuenta_pesos')
    if (cincuenta.value.trim() !== '' && cincuenta.value !== '0') {
        const nuevoValor = '$ ' + cincuenta.value * 50;
        valores.cincuenta = cincuenta.value * 50;
        // Selecciona el span correspondiente
        let span = document.querySelector('#resultado_cincuenta_pesos');
        // Coloca el nuevo valor en el 
        span.textContent = nuevoValor;
    }

    // cien pesos
    const cien = document.getElementById('id_cien_pesos')
    if (cien.value.trim() !== '' && cien.value !== '0') {
        const nuevoValor = '$ ' + cien.value * 100;
        valores.cien = cien.value * 100;
        // Selecciona el span correspondiente
        let span = document.querySelector('#resultado_cien_pesos');
        // Coloca el nuevo valor en el 
        span.textContent = nuevoValor;
    }

    // doscientos pesos
    const doscientos = document.getElementById('id_doscientos_pesos')
    if (doscientos.value.trim() !== '' && doscientos.value !== '0') {
        const nuevoValor = '$ ' + doscientos.value * 200;
        valores.doscientos = doscientos.value * 200;
        // Selecciona el span correspondiente
        let span = document.querySelector('#resultado_doscientos_pesos');
        // Coloca el nuevo valor en el 
        span.textContent = nuevoValor;
    }

    // quinientos pesos
    const quinientos = document.getElementById('id_quinientos_pesos')
    if (quinientos.value.trim() !== '' && quinientos.value !== '0') {
        const nuevoValor = '$ ' + quinientos.value * 500;
        valores.quinientos = quinientos.value * 500;
        // Selecciona el span correspondiente
        let span = document.querySelector('#resultado_quinientos_pesos');
        // Coloca el nuevo valor en el 
        span.textContent = nuevoValor;
    }

    // mil pesos
    const mil = document.getElementById('id_mil_pesos')
    if (mil.value.trim() !== '' && mil.value !== '0') {
        const nuevoValor = '$ ' + mil.value * 1000;
        valores.mil = mil.value * 1000;
        // Selecciona el span correspondiente
        let span = document.querySelector('#resultado_mil_pesos');
        // Coloca el nuevo valor en el 
        span.textContent = nuevoValor;
    }
}

function limpiar_datos() {
    // document.getElementById('id_total').textContent = '';
    document.getElementById('id_total').value = 0;
    document.getElementById('id_total_span').textContent = '';
    document.getElementById('resultado_un_peso').textContent = '';
    document.getElementById('resultado_tres_pesos').textContent = '';
    document.getElementById('resultado_cinco_pesos').textContent = '';
    document.getElementById('resultado_diez_pesos').textContent = '';
    document.getElementById('resultado_veinte_pesos').textContent = '';
    document.getElementById('resultado_cincuenta_pesos').textContent = '';
    document.getElementById('resultado_cien_pesos').textContent = '';
    document.getElementById('resultado_doscientos_pesos').textContent = '';
    document.getElementById('resultado_quinientos_pesos').textContent = '';
    document.getElementById('resultado_mil_pesos').textContent = '';
    document.getElementById('formulario').reset();
    sumar_todo = 0;
}
// reinaldo jvl
// soporte ediberto ferrer 50953838 59077357
// mercadotecnia@iju.eicma.cu
// Martiza2024*
