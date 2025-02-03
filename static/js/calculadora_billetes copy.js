// Inicializando objeto donde se van a agregar los totales por billetes
var valores = new Object();

// sumatoria de un peso
document.getElementById('un_peso').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('un_peso').value;
    // Multiplicar por 1
    const resultado = numero * 1;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.uno = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_un_peso').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// tres_pesos
document.getElementById('tres_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('tres_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 3;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.tres = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_tres_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// cinco_pesos
document.getElementById('cinco_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('cinco_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 5;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.cinco = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_cinco_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// dies_pesos
document.getElementById('diez_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('diez_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 10;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.diez = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_diez_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// viente_pesos
document.getElementById('veinte_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('veinte_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 20;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.veinte = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_veinte_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// cincuenta_pesos
document.getElementById('cincuenta_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('cincuenta_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 50;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.cincueta = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_cincuenta_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// cien_pesos
document.getElementById('cien_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('cien_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 100;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.cien = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_cien_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// docientos_pesos
document.getElementById('doscientos_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('doscientos_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 200;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.doscientos = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_doscientos_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// quinietos_pesos
document.getElementById('quinientos_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('quinientos_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 500;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.quinientos = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_quinientos_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// mil_pesos
document.getElementById('mil_pesos').addEventListener('input', function() {
    // Capturar el valor del input
    let numero = document.getElementById('mil_pesos').value;
    // Multiplicar por 1
    const resultado = numero * 1000;
    // Agregar resultado al objeto para hacer sumatoria final
    valores.mil = resultado;
    // Mostrar el resultado en el span
    document.getElementById('resultado_mil_pesos').textContent = '$ ' + new Intl.NumberFormat().format(resultado);
});

// Función para sumar todos los valores de los billetes
function calcular() {
    total = document.getElementById('total')
    sumar_todo = 0;
    for(let clave in valores) {
        sumar_todo += valores[clave];
    }
    total.innerHTML = '$ ' + new Intl.NumberFormat().format(sumar_todo);
    document.getElementById('input_total').value = sumar_todo;
    document.getElementById('id_total').value = sumar_todo;
    document.getElementById('resultado_0_peso').value = sumar_todo;
}

// Observando lo que se va calculado por billetes y sumado
document.querySelectorAll('.entrada').forEach(function(input) {
    input.addEventListener('input', calcular);
})

// Función para limpiar de valores todos los input
function reset(){
document.getElementsById("formulario").reset();
}

// reinaldo jvl
// soporte ediberto ferrer 50953838 59077357
// mercadotecnia@iju.eicma.cu
// Martiza2024*
