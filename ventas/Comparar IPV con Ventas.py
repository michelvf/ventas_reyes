# Importar Pandas
import pandas as pd

# Leer los 2 fichero Excel
eleventa = pd.read_excel("ELEVENTA-INVENTARIO-DI-MUUU-06-04-25.xlsx")
ipv = pd.read_excel("IPV_DI_MUUU-05-04-25.xlsx", sheet_name="01")

# Asegurar que la columna Inv.Final es de tipo float
ipv['Inv.Final'] = ipv['Inv.Final'].astype(float)

# Aseguramos que las columnas "Productos" y "Producto" sean comparables
ipv['Productos'] = ipv['Productos'].str.strip()
eleventa['Producto'] = eleventa['Producto'].str.strip()

# Realizar un merge para comparar por Productos
resultado = pd.merge(ipv, eleventa, left_on='Productos', right_on='Producto', how='inner')

# Crear una nueva columna booleana si Existencia == Inv.Final
resultado['Existencia_Igual_InvFinal'] = resultado['Existencia'] == resultado['Inv.Final']

# Filtrar las filas donde Existencia_Igual_InvFinal es False
resultado_filtrado = resultado[resultado['Existencia_Igual_InvFinal'] == False]

# Mostrar resultado
print(resultado_filtrado)

# Seleccionar las columnas específicas y mostrar solo esas
columnas_a_mostrar1 = [
    'Codigo', 'Productos', 'Inv.Final', 'Código', 'Producto', 'Existencia', 'Existencia_Igual_InvFinal'
]

# Asegurarnos de que las columnas existen en el DataFrame antes de imprimir
columnas_disponibles1 = [col for col in columnas_a_mostrar1 if col in resultado_filtrado.columns]

# Imprimir las columnas filtradas
print(resultado_filtrado[columnas_disponibles1])

# Opcional: Guardar el resultado en un nuevo archivo Excel
resultado_filtrado.to_excel('resultado_comparacion.xlsx', index=False)