import os
import pandas as pd
import matplotlib
# Configuración para que Matplotlib no intente abrir ventanas (Exportación Limpia para Linux)
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de variables con los nombres de columna exactos de tu visualización
ARCHIVO_CSV = "imdb_top_movies_1980_2026.csv" 
COL_CATEGORIA = "genres"       # Cambiado a 'genres' (con s) según tu captura
COL_NUMERICA = "num_votes"    
COL_EXTRA = "title"           

# Verificación de existencia del archivo antes de iniciar
if not os.path.exists(ARCHIVO_CSV):
    raise FileNotFoundError(f"No se encontró el archivo '{ARCHIVO_CSV}'. Asegúrate de que esté en la misma carpeta.")

# Carga del DataFrame original
df = pd.read_csv(ARCHIVO_CSV)

# Convertimos la columna a string
df[COL_CATEGORIA] = df[COL_CATEGORIA].astype(str)

# TRUCO PARA LOS GRÁFICOS: Nos quedamos solo con el primer género principal (antes de la coma)
# Esto evita que se amontonen combinaciones largas como 'Action,Crime,Drama'
df[COL_CATEGORIA] = df[COL_CATEGORIA].str.split(',').str[0]

# Ejercicio 1: Dimensiones de la Tabla de forma automatizada
filas, columnas = df.shape
print(f"La tabla contiene {filas} filas y {columnas} columnas.\n")

# Ejercicio 2: Filtrar por coincidencia exacta (Películas cuyo género principal sea exactamente Action)
VALOR_EXACTO = "Action"
filtro_exacto = df[df[COL_CATEGORIA] == VALOR_EXACTO]

# Ejercicio 3: Filtrar por texto parcial usando .str.contains()
# Buscamos películas que contengan la palabra 'Drama' en su género principal
filtro_avanzado = df[COL_CATEGORIA].str.contains("Drama", case=False, na=False)
df_filtrado_parcial = df[filtro_avanzado]

# Ejercicio 4: Selección de Columnas Clave a partir del filtro anterior
columnas_clave = df_filtrado_parcial[[COL_CATEGORIA, COL_NUMERICA]]
print("--- Ejercicio 4: Encabezado de columnas clave (Filtro Drama) ---")
print(columnas_clave.head())
print("-" * 50 + "\n")

# Ejercicio 5: Agrupación y Resumen ordenado de mayor a menor
resumen_agrupado = df.groupby(COL_CATEGORIA)[COL_NUMERICA].sum().sort_values(ascending=False)
print("--- Ejercicio 5: Resumen agrupado (Suma de votos por Género) ---")
print(resumen_agrupado)
print("-" * 50 + "\n")

# Ejercicio 6: Estructura de Control Automatizada con Operador Morsa (:=)
# Umbral crítico de 50 millones de votos acumulados para el filtro
UMBRAL_CRITICO = 50000000
print("--- Ejercicio 6: Alerta de Umbral ---")
if (suma_filtrada := columnas_clave[COL_NUMERICA].sum()) > UMBRAL_CRITICO:
    print(f"ALERTA: Prioridad Alta. La suma ({suma_filtrada:.2f}) supera el umbral ({UMBRAL_CRITICO}).")
else:
    print(f"Estado Normal. La suma ({suma_filtrada:.2f}) se mantiene bajo el umbral ({UMBRAL_CRITICO}).")
print("-" * 50 + "\n")

# Ejercicio 7: Gráfico de Barras Comparativo (Seaborn)
# Tomamos los 8 géneros principales para un diseño súper limpio
top_generos = resumen_agrupado.nlargest(8).index
df_top_generos = df[df[COL_CATEGORIA].isin(top_generos)]

plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")
# Gráfico horizontal para legibilidad impecable
sns.barplot(data=df_top_generos, x=COL_NUMERICA, y=COL_CATEGORIA, estimator=sum, errorbar=None, palette="viridis")
plt.title(f"Suma Total de {COL_NUMERICA} por Género Principal", fontsize=14, fontweight='bold')
plt.xlabel("Total de Votos")
plt.ylabel("Género")
plt.tight_layout()
plt.savefig("reporte_barras.png", dpi=300)
plt.close() 
print("Gráfico de barras generado con éxito como 'reporte_barras.png'.")

# Ejercicio 8: Gráfico de Torta Puro (Matplotlib)
# Limitamos estrictamente a los 5 géneros más grandes para evitar cualquier amontonamiento
top_torta = resumen_agrupado.nlargest(5)

plt.figure(figsize=(8, 8))
# wedgeprops define bordes blancos limpios entre porciones
plt.pie(top_torta, labels=top_torta.index, autopct='%1.1f%%', startangle=140, 
        wedgeprops={'linewidth': 2, 'edgecolor': 'white'}, colors=sns.color_palette("pastel"))
plt.title("Distribución de Votos en el Top 5 de Géneros", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig("reporte_torta.png", dpi=300)
plt.close() 
print("Gráfico de torta generado con éxito como 'reporte_torta.png'.")
print("-" * 50 + "\n")

# Ejercicio 9: Filtro Avanzado con .loc[] — Doble Condición y Selección Simultánea
# Condición extra: Películas con cantidad de votos mayor a la mediana del dataset
VALOR_NUMERICO_CORTE = df[COL_NUMERICA].median()
condicion_extra = df[COL_NUMERICA] > VALOR_NUMERICO_CORTE

# Una sola instrucción eficiente
resultado = df.loc[
    filtro_avanzado & condicion_extra,
    [COL_CATEGORIA, COL_NUMERICA, COL_EXTRA]
]

print("--- Ejercicio 9: Resultado de .loc[] con Doble Condición ---")
print(resultado.head())  # .head() para mostrar las primeras filas de forma elegante
print(f"\nFilas totales que cumplen ambas condiciones: {len(resultado)}")
print("-" * 50 + "\n")