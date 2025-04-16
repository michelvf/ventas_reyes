# pip install "python-barcode[image]"
import pandas as pd
from barcode import Gs1_128
from barcode.writer import ImageWriter

    # codigo_bar = BARCODE(new_codigo, writer=ImageWriter())
excel_file = pd.read_excel('ALMACEN.xls')
codigo = excel_file['Codigo']
# predicado = '-La Parada'

# Vocales
# y,z = 'ÁÉÍÓÚ','AEIOU'
# convert = str.maketrans(y, z)

for a in excel_file.Codigo:
    indice = excel_file.index.get_loc(excel_file[excel_file['Codigo'] == a].index[0])
    predicado = '-' + excel_file['Departamento'][indice]
    # tamano = len(str(a))
    # if tamano == 1:
    #     new_codigo = '000' + str(a) + predicado
    # elif tamano == 2:
    #     new_codigo = '00' + str(a) + predicado
    # elif tamano == 3:
    #     new_codigo = '0' + str(a) + predicado
    # elif tamano == 4:
    #     new_codigo = str(a) + predicado
    
    # Cambiando las Tildes
    # new_codigo = str(a).translate(convert) + predicado
    # Para Di Muu
    #new_codigo = str(a) + predicado[0:-1]
    new_codigo = str(a) + predicado
    
    # Formar código de barra
    
    
    barra = Gs1_128(new_codigo)
    barra.save(new_codigo)
    # nombre_fichero = codigo_bar.save(new_codigo)
    # print(f'Código viejo: {a}, Código nuevo: {new_codigo}')
    # excel_file.loc[excel_file['Codigo'] == a, 'Codigo'] == new_codigo
    excel_file.Codigo = excel_file.Codigo.replace({a: new_codigo})
# excel_file

# Exportar a Excel sin índice
excel_file.to_excel('nuevos codigos Almacen.xlsx', index=False)

