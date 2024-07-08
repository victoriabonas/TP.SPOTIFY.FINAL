import pandas as pd #importa pandas para levantar el df
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Songs_csv.csv')

# Gráfico de barras horizontales para la popularidad de cada canción
plt.figure(figsize=(12, 8))
sns.barplot(x='popularity', y='song', data=df, color='skyblue')
plt.xlabel('Popularidad')
plt.ylabel('Nombre de la Canción')
plt.title('Popularidad de Cada Canción')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Frecuencia de géneros musicales más escuchados
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

plt.figure(figsize=(10, 6))
sns.barplot(x='genre', y='count', data=genre_counts, palette='pink')
plt.title('Frecuencia de Géneros Musicales Más Escuchados')
plt.xlabel('Género Musical')
plt.ylabel('Cantidad de Canciones')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Popularidad por explícito
popularity_by_explicit = df.groupby('explicit')['popularity'].mean().reset_index()

plt.figure(figsize=(8, 6))
sns.barplot(x='explicit', y='popularity', data=popularity_by_explicit, palette=['skyblue', 'lightgreen'])
plt.title('Comparación de Popularidad entre Canciones Explícitas y No Explícitas')
plt.xlabel('Explícito')
plt.ylabel('Popularidad (Promedio)')
plt.xticks([0, 1], ['No Explícito', 'Explícito'], rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()