def efectivo():
    suma = 0
    montos = Contador_billete.objects.all()
    for a in montos:
        print(f'Se va a sumar: {a.total}')
        suma += a.total
        print(f'Suma va por: $ {suma}')

