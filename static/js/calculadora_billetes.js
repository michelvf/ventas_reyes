document.addEventListener('DOMContentLoaded', function() {
    const billInputs = document.querySelectorAll('.bill-input');
    const resetBtn = document.getElementById('resetBtn');
    //const calculateBtn = document.getElementById('calculateBtn');
    const grandTotalElement = document.getElementById('grandTotal');
    const resultSummary = document.getElementById('resultSummary');
    const summaryContent = document.getElementById('summaryContent');
    const total = document.getElementById('id_total');
            
    // Función para actualizar los subtotales y el total
    function updateCalculations() {
       let grandTotal = 0;
             
       billInputs.forEach(input => {
           const denomination = parseInt(input.dataset.denomination);
           const quantity = parseInt(input.value) || 0;
           const subtotal = denomination * quantity;
                    
           document.getElementById(`subtotal-${denomination}`).textContent = subtotal.toLocaleString();
           grandTotal += subtotal;
       });
                
       grandTotalElement.textContent = grandTotal.toLocaleString();
       total.value = grandTotal
    }
            
    // Actualizar cálculos cuando cambia un input
    billInputs.forEach(input => {
    	input.addEventListener('input', function() {
    
    	    // Asegurar que no haya valores negativos
    	    if (parseInt(this.value) < 0) {
       	        this.value = 0;
    	    }
                    
        updateCalculations();
      });
    });
            
    // Botón de reinicio
    resetBtn.addEventListener('click', function() {
        billInputs.forEach(input => {
            input.value = 0;
        });
               
        updateCalculations();
        resultSummary.style.display = 'none';
    });
            
    // Botón de cálculo
    /*
    calculateBtn.addEventListener('click', function() {
        updateCalculations();
                
        // Generar resumen
        let summary = '';
        let totalBills = 0;
                
        billInputs.forEach(input => {
             const denomination = parseInt(input.dataset.denomination);
             const quantity = parseInt(input.value) || 0;
                    
             if (quantity > 0) {
                 summary += `<div class="mb-1">
                              <span class="badge bg-primary">${quantity}</span> billetes de 
                              <span class="badge bg-secondary">$${denomination}</span> = 
                              <span class="badge bg-success">$${(denomination * quantity).toLocaleString()}</span>
                             </div>`;
                 totalBills += quantity;
             }
        });
                
        if (summary) {
            summary += `<hr>
                       <div class="d-flex justify-content-between">
                        <span>Total de billetes: <span class="badge bg-info">${totalBills}</span></span>
                        <span>Monto total: <span class="badge bg-warning text-dark">$${parseInt(grandTotalElement.textContent.replace(/,/g, '')).toLocaleString()}</span></span>
                    </div>`;
                    
                    summaryContent.innerHTML = summary;
                    resultSummary.style.display = 'block';
         } else {
                    resultSummary.style.display = 'none';
         }
});*/
            
            // Inicializar cálculos
            updateCalculations();
        });
