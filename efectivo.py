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
            print(f'Se va a sumar: {a.total:,}')
            suma += a.total
            un += a.un_peso if a.un_peso is not None else 0
            tres += a.tres_pesos if a.tres_pesos is not None else 0
            cinco += a.cinco_pesos if a.cinco_pesos is not None else 0
            diez += a.diez_pesos if a.diez_pesos is not None else 0
            veinte += a.veinte_pesos if a.veinte_pesos is not None else 0
            cincuenta += a.cincuenta_pesos if a.cincuenta_pesos is not None else 0
            cien += a.cien_pesos if a.cien_pesos is not None else 0
            doscientos += a.doscientos_pesos if a.doscientos_pesos is not None else 0
            quinientos += a.quinientos_pesos if a.quinientos_pesos is not None else 0
            mil += a.mil_pesos if a.mil_pesos is not None else 0
            
        else:
            print(f'Se va a restar: {a.total:,}')
            suma -= a.total
            un -= a.un_peso if a.un_peso is not None else 0
            tres -= a.tres_pesos if a.tres_pesos is not None else 0
            cinco -= a.cinco_pesos if a.cinco_pesos is not None else 0
            diez -= a.diez_pesos if a.diez_pesos is not None else 0
            veinte -= a.veinte_pesos if a.veinte_pesos is not None else 0
            cincuenta -= a.cincuenta_pesos if a.cincuenta_pesos is not None else 0
            cien -= a.cien_pesos if a.cien_pesos is not None else 0
            doscientos -= a.doscientos_pesos if a.doscientos_pesos is not None else 0
            quinientos -= a.quinientos_pesos if a.quinientos_pesos is not None else 0
            mil -= a.mil_pesos if a.mil_pesos is not None else 0
        
        print(f'Suma va por: $ {suma:,}')
        print()

    print(f"Total: {suma:,}, $1: {un}, $3: {tres}, $5: {cinco}, $10: {diez}, $20: {veinte}")
    print(f"$50: {cincuenta}, $100: {cien}, $200: {doscientos}, $500: {quinientos}, $1000: {mil}")
    print(f"Desea actualizar (y/n)", end="")
    resp = input()
    if resp == "n":
        update = Cuenta.objects.get(cuenta='Efectivo')
        update(un_peso=un, tres_pesos=tres, cinco_pesos=cien, diez_pesos=diez, veinte_pesos=veinte,\
            cincuenta_pesos=cincuenta, cien_pesos==cien, doscientos_pesos=doscientos, quinientos_pesos=quinientos, mil_pesos=mil )
        update.save()
    else:
        exit()
# ALTER TABLE ventas_cuenta RENAME quientos_pesos TO quinie ntos_pesos;
# ALTER TABLE ventas_cuenta ADD un_peso NULL DEFAULT 0;

# ALTER TABLE ventas_cuenta ADD tres_pesos NULL DEFAULT 0;
# ALTER TABLE ventas_cuenta ADD cinco_pesos NULL DEFAULT 0;
# ALTER TABLE ventas_cuenta ADD diez_pesos NULL DEFAULT 0;
# ALTER TABLE ventas_cuenta ADD viente_pesos NULL DEFAULT 0;
# ALTER TABLE ventas_cuenta ADD cincuenta_pesos NULL DEFAULT 0;
# ALTER TABLE ventas_cuenta ADD cien_pesos NULL DEFAULT 0;
# ALTER TABLE ventas_cuenta ADD mil_pesos NULL DEFAULT 0;
# ALTER TABLE ventas_cuenta ADD doscientos_pesos NULL DEFAULT 0;
# ALTER TABLE ventas_cuenta ADD quinientos_pesos NULL DEFAULT 0;