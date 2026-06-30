#import matplotlib.pyplot as plt
#import pandas as pd
#import seaborn as sns
# carga los datos
#df=pd.read_csv("imdb_top_movies_1980_2026.csv")

#filtra string
#filtro_avanzado = df["title"].str.startswith("The", na=False)
#df_filtrado = df[filtro_avanzado]
#suma_dinero = df_filtrado["runtime_minutes"].sum()

#filtra numeros
#filtro_avanzado = df["gameDuration"].sum()
#print("---Reporte Automatizado---")
#print(f"duracion de partida {filtro_avanzado} tiempo")


#condicional

#if Default_Limite := (suma_dinero > 20000):
#    print("alerta")
#elif suma_dinero < 1200:
#    print("aviso")
#else:
#    print("placejolder") 

#grafico
#print("\n[generando GRAFICO de barras]")
#sns.set_theme(style="whitegrid")
#plt.figure(figsize=(10,6))
#sns.barplot(
 #data=df,
 #x="title",
 #y="runtime_minutes",
 #estimator=sum,
 #errorbar=None,
 #palette= "viridis",


#)      
#plt.title("Comparativa de Mercado por tipo de Hardware", fontsize=14)
#plt.xticks(rotation=20)

#guarda el grafico
#plt.tight_layout("grafico_barras.png",dpi=300)
#plt.show()

#print("\n hecho los graficos se guardaron en tu carpeta")



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargamos el CSV de películas
df = pd.read_csv("imdb_top_movies_1980_2026.csv")

# 2. Nos quedamos solo con las 10 películas con más votos
df_top10 = df.nlargest(10, 'num_votes')

# 3. Creamos el lienzo
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

# Usamos un gráfico de barras horizontales (Y=title, X=num_votes)
# ¡Es el mejor truco para que los títulos de las películas se lean perfectamente!
sns.barplot(
    data=df_top10,
    x='num_votes',
    y='title',
    palette="viridis"
)

plt.title("Top 10 Películas con Mayor Cantidad de Votos en IMDB", fontsize=14, fontweight="bold")
plt.xlabel("Número de Votos (en millones)", fontsize=11)
plt.ylabel("Película", fontsize=11)
plt.tight_layout()

# 4. Guardamos el archivo limpia de memoria
plt.savefig("top_peliculas_votos.png", dpi=300)
plt.close()

print("¡Hecho! 'top_peliculas_votos.png' generado sin amontonamientos.")