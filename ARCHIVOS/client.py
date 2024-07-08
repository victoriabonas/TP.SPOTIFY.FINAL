import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import base64


class Cancion:
    def __init__(self, id, song, artist, explicit, feat, popularity):
        self.id = id
        self.song = song
        self.artist = artist
        self.explicit = explicit
        self.feat = feat
        self.popularity = popularity 

    def describe(self):
        return f"ID: {self.id}, Nombre: {self.song}, Artista: {self.artist}, Explícito: {self.explicit}, Feat: {self.feat}, Popularidad: {self.popularity}"

class Pop(Cancion):
    def __init__(self, id, song, artist, explicit, feat, popularity, tipopop):
        super().__init__(id, song, artist, explicit, feat, popularity)
        self.typepop = tipopop

class HipHop(Cancion):
    def __init__(self, id, song, artist, explicit, feat, popularity):
        super().__init__(id, song, artist, explicit, feat, popularity)

class Otros(Cancion):
    def __init__(self, id, song, artist, explicit, feat, popularity, genre):
        super().__init__(id, song, artist, explicit, feat, popularity)
        self.genre = genre

def obtener_canciones(base_url):
    url = f"{base_url}/songs"
    response = requests.get(url)
    if response.status_code == 200:
        songs = response.json()
        canciones_transformadas = []
        for song in songs:
            canciones_transformadas.append(agregar_cancion(song))
        return canciones_transformadas
    return None

def ver_explícitas(base_url):
    url = f"{base_url}/songs"
    response = requests.get(url)
    if response.status_code == 200:
        songs = response.json()
        canciones_explicitas = []
        for song in songs:
            if song["explicit"]:
                canciones_explicitas.append(agregar_cancion(song))
        return canciones_explicitas
    return None

def agregar_cancion(song):
    if song["genre"] == "pop":
        return Pop(song["id"], song["song"], song["artist"], song["explicit"], song["feat"], song["popularity"], song["genre"])
    elif song["genre"] == "hiphop":
        return HipHop(song["id"], song["song"], song["artist"], song["explicit"], song["feat"], song["popularity"], song["genre"])
    else:
        return Otros(song["id"], song["song"], song["artist"], song["explicit"], song["feat"], song["popularity"], song["genre"])

def enviar_cancion(base_url, song_data):
    url = f"{base_url}/agregar"  
    response = requests.post(url, json=song_data)
    if response.status_code == 200:
        print("Canción agregada con éxito")
    else:
        print(f"Error al agregar la canción: {response.status_code} - {response.text}")



CLIENT_ID = '5134a7a88df04b5d86899bb7096dc1be'
CLIENT_SECRET = '8fbeec358826480fbbffc6662e5cd5b8'
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def obtener_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode()).decode(),
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    return response_data['access_token']


def obtener_id(nombre_artista, nombre_cancion):
    token = obtener_token()
    query = f'{nombre_cancion} artist:{nombre_artista}'
    url = f'https://api.spotify.com/v1/search?q={query}&type=track'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response_data['tracks']['items']:
        song_id = response_data['tracks']['items'][0]['id']
        return song_id
    else:
        return None


def actualizar_cancion(base_url, song_id, updated_data):
    url = f"{base_url}/songs/{song_id}"
    response = requests.put(url, json=updated_data)
    if response.status_code == 200:
        print("Canción actualizada con éxito")
    else:
        print("Error al actualizar la canción")

def eliminar_cancion(base_url, song_id):
    url = f"{base_url}/songs/{song_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print("Canción eliminada con éxito")
    else:
        print("Error al eliminar la canción")

def obtener_genero_unica_cancion(track_id):
    track_info = sp.track(track_id)
    artist_id = track_info['artists'][0]['id']
    # Obtener los géneros del artista
    artist_genres = sp.artist(artist_id)['genres']
    return artist_genres[0]


def main():
    base_url = "http://127.0.0.1:4000"
    while True:
        print("Opciones")
        print("1: Ver todas las canciones")
        print("2: Ver canciones explícitas")
        print("3: Agregar una canción nueva")
        print("4: Actualizar una canción existente")
        print("5: Eliminar una canción existente")
        print("6: Salir")

        try:
            option = int(input("Seleccione una opción: "))
            if option == 1:
                print("1: Ver todas las canciones")
                songs = obtener_canciones(base_url)
                if songs:
                    for song in songs:
                        print(song.describe())
                else:
                    print("No se pudieron obtener las canciones")

            elif option == 2:
                print("2: Ver canciones explícitas")
                explicit_songs = ver_explícitas(base_url)
                if explicit_songs:
                    for song in explicit_songs:
                        print(song.describe())
                else:
                    print("No hay canciones explícitas")

            elif option == 3:
                song = input("Nombre de la canción: ")
                artist = input("Artista de la canción: ")
                song_id = obtener_id(artist, song)
                if song_id:
                    track_info = sp.track(song_id)
                    popularity = track_info['popularity']
                    explicit = track_info['explicit']
                    feat = len(track_info['artists']) > 1
                    if feat <1:
                        feat_with= input("Con quién colabora el artista?: ")
                    else:
                        feat_with=None
                    genre = obtener_genero_unica_cancion(song_id)
                    print(f"la cancion {song} tiene una popularidad de {popularity} y su genero es {genre}")
                    if genre == "pop":
                        typepop = input("Tipo de Pop: ")
                        nueva_cancion = {
                            "id": song_id,
                            "song": song,
                            "artist": artist,
                            "explicit": explicit,
                            "feat": feat,
                            "popularity": popularity,
                            "genre": genre,
                            "feat_with": feat_with,
                            "typepop": typepop
                        }
                    elif genre == "hiphop":
                        nueva_cancion = {
                            "id": song_id,
                            "song": song,
                            "artist": artist,
                            "explicit": explicit,
                            "feat": feat,
                            "popularity": popularity,
                            "feat_with": feat_with,
                            "genre": genre
                        }
                    else:
                        nueva_cancion = {
                            "id": song_id,
                            "song": song,
                            "artist": artist,
                            "explicit": explicit,
                            "feat": feat,
                            "popularity": popularity,
                            "feat_with": feat_with,
                            "genre": genre
                        }

                    enviar_cancion(base_url, nueva_cancion)
                else:
                    print("No se pudo encontrar la canción en Spotify")
                

            elif option == 4:
                print("4: Actualizar una canción existente")
                song_id = input("ID de la canción a actualizar: ")
                popularity= int(input("Nueva (o vieja) popularidad de la canción: "))
                feat= bool(input("Nuevo (o viejo) estado de colaboración de la canción: "))
                explicit=bool(input("Nuevo (o viejo) estado de explicitud de la canción: "))
                if feat==True:
                    feat_with=input("Si hay colaboración, quién?: ")
                else:
                    feat_with=None
                updated_data = {
                    "popularity": popularity,
                    "explicit": explicit,
                    "feat": feat,
                    "feat_with": feat_with
                }
                actualizar_cancion(base_url, song_id, updated_data)

            elif option == 5:
                print("5: Eliminar una canción existente")
                song_id = int(input("ID de la canción a eliminar: "))
                eliminar_cancion(base_url, song_id)

            elif option == 6:
                break

        except ValueError:
            print("Por favor, ingrese una opción numérica válida")

main()

if __name__ == "__main__":
    main()


