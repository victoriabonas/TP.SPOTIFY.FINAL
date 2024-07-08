import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #para interactuar con la api de spotify
import requests #para hacer solicitudes http en el postman
import base64 #para codificar las credenciales de spotify

#con POO, se crea la clase madre. con el init (constructor) se definen los atributos de la clase 
class Cancion:
    def __init__(self, id, nombre, artista, explicito, featured, popularity):
        self.id = id
        self.nombre = nombre
        self.artista = artista
        self.explicito = explicito
        self.featured = featured
        self.popularity = popularity 

#metodo de la clase cancion que devuelve una descripcion de la cancion con todos los atributos de la misma 
    def describe(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Artista: {self.artista}, Explícito: {self.explicito}, Featured: {self.featured}, Popularidad: {self.popularity}"

#creamos las clases hijas de la clase madre cancion, segun los generos
#cada una recibe la clase madre y hereda todos sus atributos con el super init
#pueden tener atributos propios segun la clase que deben definirse, como por ejemplo el tipopop 

class Pop(Cancion):
    def __init__(self, id, nombre, artista, explicito, featured, popularity, tipopop):
        super().__init__(id, nombre, artista, explicito, featured, popularity)
        self.typepop = tipopop

class HipHop(Cancion):
    def __init__(self, id, nombre, artista, explicito, featured, popularity):
        super().__init__(id, nombre, artista, explicito, featured, popularity)

class Otros(Cancion):
    def __init__(self, id, nombre, artista, explicito, featured, popularity, genero):
        super().__init__(id, nombre, artista, explicito, featured, popularity)
        self.genero = genero

#FUNCIONES QUE INTERACTUAN CON EL BACKEND Y LA API PROPIA

def obtener_canciones(base_url):
    #base url es la api nuestra
    url = f"{base_url}/songs" #al agregar /songs, se completa la url. se ejecuta la funcion de get songs de app
    response = requests.get(url) #le hace una solicitud get a la url construida. la rta se almacena en response. PARA OBTENER LAS CANCIONES
    if response.status_code == 200: #si el status code de la response es 200, significa que la solicitud fue exitosa. devolvera la lista de canciones transformadas
        songs = response.json() #convierte la rta en formato json a formato python (dic). en songs se almacenan todas las canciones obtenidas 
        canciones_transformadas = []
        for song in songs: #para cada cancion, con la funcion agregar cancion transforma cada cancion en una clase segun el genero y la agrega a la lista de canciones transformadas
            canciones_transformadas.append(agregar_cancion(song))
        return canciones_transformadas
    return None #si la solicitud no fue exitosa, no devuelve nada

def ver_explícitas(base_url):
    url = f"{base_url}/songs"
    response = requests.get(url)
    if response.status_code == 200:
        songs = response.json()
        canciones_explicitas = []
        for song in songs:
            if song["explicit"]: #comprueba, sobre cada cancion, si el campo explicit es True. Si es, transforma la canción en un objeto de clase utilizando agregar_cancion y la agrega a canciones_explicitas.
                canciones_explicitas.append(agregar_cancion(song))
        return canciones_explicitas
    return None

def agregar_cancion(song):
    #Si el género de la cancion es "pop", crea y devuelve un objeto de la clase Pop con los atributos correspondientes. lo mismo para hiphop y otros
    if song["genre"] == "pop":
        return Pop(song["id"], song["name"], song["artist"], song["explicit"], song["featured"], song["popularity"], song["typepop"])
    elif song["genre"] == "hiphop":
        return HipHop(song["id"], song["name"], song["artist"], song["explicit"], song["featured"], song["popularity"])
    else:
        return Otros(song["id"], song["name"], song["artist"], song["explicit"], song["featured"], song["popularity"], song["genre"])

def enviar_cancion(base_url, song_data): #toma song_data, que es un dic con la informacion de una cancion que se quiere agregar a la playlist
    url = f"{base_url}/songs"
    response = requests.post(url, json=song_data) #envia solicitud post (agregar) con song data como lo que se solicita agregar
    if response.status_code == 201: #si la solicitud se crea bien
        print("Canción agregada con éxito")
    else:
        print(f"Error al agregar la canción: {response.status_code} - {response.text}") #se imprime el codigo de error y el mensaje de error

#obtenemos las credenciales de los clientes registrando la app en spotify developer dashboard
CLIENT_ID = '5134a7a88df04b5d86899bb7096dc1be'
CLIENT_SECRET = '8fbeec358826480fbbffc6662e5cd5b8'
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET) #es una clase de la biblio spotipy que maneja la autenticacion segun las credenciales
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #instancia de la clase spotipy que usamos para interactuar con la api de spotify

#El token de acceso es necesario para autenticar y autorizar las solicitudes que haces a la API de Spotify.
def obtener_token():
    url = 'https://accounts.spotify.com/api/token' #url a la que se le envia la solicitud para obtener el token de acceso
    headers = {'Authorization': 'Basic ' + base64.b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode()).decode()} 
    #los headers incluyen autorizacion en formato basic auth, cadena codificada en base 64 de las credenciales. 
    #codifica las credenciales en base 64
    data = {'grant_type': 'client_credentials'}
  
    response = requests.post(url, headers=headers, data=data) #hace solicitud post de la data a la url 
    response_data = response.json() #se obtiene el token en json 
    return response_data['access_token'] #retorna el token de acceso

def obtener_id(nombre_artista, nombre_cancion):
    token = obtener_token() #obtiene el token de acceso 
    query = f'{nombre_cancion} artist:{nombre_artista}' #construye la consulta de busqueda
    url = f'https://api.spotify.com/v1/search?q={query}&type=track'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers) #Hace una solicitud GET a la URL con los encabezados especificados.
    response_data = response.json()
    if response_data['tracks']['items']: #verifica si hay resultados en la rta 
        track_id = response_data['tracks']['items'][0]['id'] #obtiene el id del primer rtado
        return track_id
    else:
        return None

def actualizar_cancion(base_url, song_id, updated_data): #se actualiza cancion segun el id ingresado, por ej popularidad o explicit
    url = f"{base_url}/songs/{song_id}"
    response = requests.put(url, json=updated_data)
    if response.status_code == 200:
        print("Canción actualizada con éxito")
    else:
        print("Error al actualizar la canción")

def eliminar_cancion(base_url, song_id): #se elimina cancion de playlist segun id
    url = f"{base_url}/songs/{song_id}"
    response = requests.delete(url)
    if response.status_code == 204:
        print("Canción eliminada con éxito")
    else:
        print("Error al eliminar la canción")

#p obtener el genero de una cancion, sino por default devuelve el genero del artista en gral
def obtener_genero_unica_cancion(track_id):
    track_info = sp.track(track_id) #obtiene la info de la cancion segun el id que le pasamos
    artist_id = track_info['artists'][0]['id'] #obtiene el id del primer artista asociado a la cancion
    artist_genres = sp.artist(artist_id)['genres'] #obtener los generos del artista 
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
                        print(song.describe()) #imprime la descripcion de todas las canciones obtenidas
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
                print("3: Agregar una canción nueva")
                song_name = input("Nombre de la canción: ")
                song_artist = input("Artista de la canción: ")
                track_id = obtener_id(song_artist, song_name)
                if track_id:
                    track_info = sp.track(track_id)
                    song_popularity = track_info['popularity']
                    explicito = track_info['explicit']
                    featured = len(track_info['artists']) > 1
                    genre = obtener_genero_unica_cancion(track_id)

                    if genre == "pop":
                        typepop = input("Tipo de Pop: ")
                        nueva_cancion = {
                            "id": track_id,
                            "name": song_name,
                            "artist": song_artist,
                            "explicit": explicito,
                            "featured": featured,
                            "popularity": song_popularity,
                            "genre": genre,
                            "typepop": typepop
                        }
                    elif genre == "hiphop":
                        nueva_cancion = {
                            "id": track_id,
                            "name": song_name,
                            "artist": song_artist,
                            "explicit": explicito,
                            "featured": featured,
                            "popularity": song_popularity,
                            "genre": genre
                        }
                    else:
                        nueva_cancion = {
                            "id": track_id,
                            "name": song_name,
                            "artist": song_artist,
                            "explicit": explicito,
                            "featured": featured,
                            "popularity": song_popularity,
                            "genre": genre
                        }

                    enviar_cancion(base_url, nueva_cancion)
                else:
                    print("No se pudo encontrar la canción en Spotify")

            elif option == 4:
                print("4: Actualizar una canción existente")
                song_id = input("ID de la canción a actualizar: ")
                updated_data = {
                    "popularity": int(input("Nueva popularidad de la canción: "))
                }
                actualizar_cancion(base_url, song_id, updated_data)

            elif option == 5:
                print("5: Eliminar una canción existente")
                song_id = input("ID de la canción a eliminar: ")
                eliminar_cancion(base_url, song_id)

            elif option == 6:
                break

        except ValueError:
            print("Por favor, ingrese una opción numérica válida")

if __name__ == "__main__":
    main()