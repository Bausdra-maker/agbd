#permite transforar datos
import pandas as pd

#importa el csv 
df=pd.read_csv("games.csv")


#si el python3 "nombre de archivo".py esta bien muestra eso
print("oka' archivo cargado correctamente")

#muestra el df en la terminal
print(df.head())

#cuenta todas las partidas 
#total_gameDuration = df['gameDuration'].count()

#suma el total de tiempo de todas las partidas
total_gameDuration = df['gameDuration'].sum()

print(total_gameDuration)

print("----analisisi avanzado de Datos---")


filtro_avanzado = df['gameDuration'] >1500

print(filtro_avanzado)