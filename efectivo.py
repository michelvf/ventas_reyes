def efectivo():
    from ventas.models import Contador_billete, Cuenta
    suma = 0
    un = 0
    tres = 0
    cinco = 0
    diez = 0
    veinte = 0
    cincuenta = 0
    cien = 0
    doscientos = 0
    quinientos = 0
    mil = 0
    
    montos = Contador_billete.objects.all()
    for a in montos:
        if a.tipo_cuenta.id == 1:
            print(f'Se va a sumar: {a.total}')
            suma += a.total
            un += a.un_peso
            tres += a.tres_pesos
            cinco += a.cinco_pesos
            diez += a.diez_pesos
            veinte += a.veinte_pesos
            cincuenta += a.cincuenta_pesos
            cien += a.cien_pesos
            doscientos += a.doscientos_pesos
            quinientos += a.quinientos_pesos
            mil += a.mil_pesos
            
        else:
            print(f'Se va a restar: {a.total}')
            suma -= a.total
            un -= a.un_peso
            tres -= a.tres_pesos
            cinco -= a.cinco_pesos
            diez -= a.diez_pesos
            veinte -= a.veinte_pesos
            cincuenta -= a.cincuenta_pesos
            cien -= a.cien_pesos
            doscientos -= a.doscientos_pesos
            quinientos -= a.quinientos_pesos
            mil -= a.mil_pesos
            print(f'Suma va por: $ {suma}')

    print(f"Total: {suma}, un peso: {un}, tres: {tres}, cinco: {cinco}, diez: {diez}, viente: {veinte}")
    print(f"cincuenta: {cincuenta}, cien: {cien}, doscientos: {doscientos}, quinientos: {quinientos}, mil: {mil}")
# ALTER TABLE ventas_cuenta RENAME quientos_pesos TO quinientos_pesos;
# ALTER TABLE ventas_cuenta ADD tres_peso NULL DEFAULT 0;