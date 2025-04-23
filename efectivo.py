def efectivo():
    suma = 0
    montos = Contador_billete.objects.all()
    for a in montos:
        print(f'Tipo {a.tipo_cuenta}')
        if a.tipo_cuenta.id == 1:
            print(f'Es un Credito, se va a sumar: +{a.total}')
            suma += a.total
        else:
           print(f'Es un Debito, se va a restar: -{a.total}')
           suma -= a.total
        print(f'Suma va por: $ {suma}')

