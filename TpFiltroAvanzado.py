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
# Tomamos los 8 géneros principales para un diseño 
top_generos = resumen_agrupado.nlargest(8).index
df_top_generos = df[df[COL_CATEGORIA].isin(top_generos)]

plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")
# Gráfico horizontal para legibilidad impecable
sns.barplot(
    data=df_top_generos, 
    x=COL_NUMERICA, 
    y=COL_CATEGORIA, 
    hue=COL_CATEGORIA, 
    legend=False, 
    estimator=sum, 
    errorbar=None, 
    palette="viridis"
)
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



# Ejercicio 10: Detección y Manejo de Valores Nulos
df_con_nulos = df.copy()
df_con_nulos.loc[[0, 1, 2], COL_NUMERICA] = None

df_sin_nulos = df_con_nulos.dropna()

media_votos = df_con_nulos[COL_NUMERICA].mean()
df_rellenado = df_con_nulos.fillna({COL_NUMERICA: round(media_votos, 2)})


# Ejercicio 11: Gráfico de Líneas con Anotación del Máximo
agrupado = df.groupby(COL_CATEGORIA)[COL_NUMERICA].sum().sort_values()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(agrupado.index, agrupado.values, marker='o', color='#2E75B6', linewidth=2, markersize=8)

idx_max = agrupado.idxmax()
val_max = agrupado.max()

ax.annotate(
    f'Máximo: {val_max:,.0f}',
    xy=(idx_max, val_max),
    xytext=(idx_max, val_max * 0.85),
    arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
    fontsize=11, color='red', fontweight='bold', ha='center'
)

ax.set_title('Evolución de Votos Totales por Género Principal', fontsize=14, fontweight='bold')
ax.set_xlabel('Género Principal')
ax.set_ylabel('Suma de Votos')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('grafico_lineas.png', dpi=150)
plt.close()




# Ejercicio 12: .query() — Filtros como texto
resultado_original = df[filtro_avanzado & condicion_extra]
resultado_query = df.query('genres.str.contains("Drama") and num_votes > @VALOR_NUMERICO_CORTE', engine='python')

print("--- Ejercicio 12: .query() vs Corchetes ---")
print("Resultado con corchetes:")
print(resultado_original.head())
print("\nResultado con .query():")
print(resultado_query.head())

son_iguales = resultado_original.equals(resultado_query)
print(f"\n¿El resultado de .query() es idéntico al original?: {son_iguales}")
print("-" * 50 + "\n")


# Ejercicio 13: .isin() y ~ (Incluir y Excluir)
generos_elegidos = ['Action', 'Comedy', 'Drama']

# Incluir y excluir
df_incluidos = df[df[COL_CATEGORIA].isin(generos_elegidos)]
df_excluidos = df[~df[COL_CATEGORIA].isin(generos_elegidos)]

print("--- Ejercicio 13: .isin() y ~ ---")
print(f"Filas incluidas ({len(df_incluidos)}):")
print(df_incluidos.head(2))
print(f"\nFilas excluidas ({len(df_excluidos)}):")
print(df_excluidos.head(2))

# suma total
total = len(df)
suma = len(df_incluidos) + len(df_excluidos)
print(f"\nTotal original: {total} | Incluidos + Excluidos: {suma}")
print(f"¿Coinciden los totales?: {total == suma}")
print("-" * 50 + "\n")


# Ejercicio 14: Exploración (.value_counts, .unique, .nunique)
print("--- Ejercicio 14: Exploración de Datos ---")
print("=== DataFrame completo ===")
print("Conteo por categoría:\n", df[COL_CATEGORIA].value_counts())
print("\nValores únicos:\n", df[COL_CATEGORIA].unique())
print("\nCantidad de categorías distintas:", df[COL_CATEGORIA].nunique())
print("\nPorcentajes (%):\n", (df[COL_CATEGORIA].value_counts(normalize=True) * 100).round(1))

df_filtrado_avanzado = df[filtro_avanzado]

print("\n=== DataFrame filtrado (Drama) ===")
print("Conteo por categoría:\n", df_filtrado_avanzado[COL_CATEGORIA].value_counts())
print("\nValores únicos:\n", df_filtrado_avanzado[COL_CATEGORIA].unique())
print("\nCantidad de categorías distintas:", df_filtrado_avanzado[COL_CATEGORIA].nunique())
print("\nPorcentajes (%):\n", (df_filtrado_avanzado[COL_CATEGORIA].value_counts(normalize=True) * 100).round(1))
print("-" * 50 + "\n")


# Ejercicio 15: Exportación CSV y Heatmap de Correlación


import numpy as np

print("--- Ejercicio 15: Exportación y Correlación ---")

# 1 Exportar a CSV
df_filtrado_avanzado.to_csv('mi_resultado_filtrado.csv', index=False)
print(f"Archivo exportado: 'mi_resultado_filtrado.csv' guardado exitosamente con {len(df_filtrado_avanzado)} filas.\n")

correlacion = df.corr(numeric_only=True)
print("Matriz de correlación:")
print(correlacion.round(2))

# 2 Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(
    correlacion,
    annot=True,
    fmt='.2f',
    cmap='plasma',
    linewidths=0.5,
    vmin=-1, vmax=1
)
plt.title('Correlación entre variables numéricas — Películas IMDb', fontweight='bold')
plt.tight_layout()
plt.savefig('heatmap_mi_dataset.png', dpi=150)
plt.close()

mask = np.triu(np.ones(correlacion.shape), k=0).astype(bool)
correlacion_sin_diag = correlacion.where(~mask)

par_max = correlacion_sin_diag.stack().idxmax()
val_max = correlacion_sin_diag.stack().max()

par_min = correlacion_sin_diag.stack().idxmin()
val_min = correlacion_sin_diag.stack().min()

print(f"\nPar más correlacionado: {par_max[0]} ↔ {par_max[1]} ({val_max:.2f})")
print(f"Par menos correlacionado: {par_min[0]} ↔ {par_min[1]} ({val_min:.2f})")
print("-" * 50 + "\n")