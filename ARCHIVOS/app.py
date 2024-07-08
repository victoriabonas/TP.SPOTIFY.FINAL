from flask import Flask, jsonify, request
#flask para crear la app web, jsonify convierte dics de python a formato json y request permite acceder a los datos enviados en las solicitudes http
import db_songs
import requests
import base64
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json

app = Flask(__name__) #creo instancia de flask y se crea la app

@app.route("/")
def hello():
    return "Hola, bienvenido a la API de canciones."

@app.route("/songs", methods=["GET"])
def get_songs():
    songs = db_songs.get_songs() #obtiene las canciones de la db
    clean_songs = []
    for song in songs:
        clean_songs.append({
            "id": song["id"],
            "song_id": song["song_id"],
            "song": song["song"],
            "artist": song["artist"],
            "popularity": song["popularity"],
            "genre": song["genre"],
            "explicit": song["explicit"],
            "feat": song["feat"],
            "feat_with": song["feat_with"]
        })
    return jsonify(clean_songs), 200 #devuelve la lista en json para que pueda ser leido por la api

@app.route("/songs/<int:id>", methods=["GET"])
def get_song(id): #obtener una cancion por el id
    songs=db_songs.get_songs()
    for song in songs:
        if song["id"] == id:
            return jsonify(song)
    return jsonify({"message": "song not found"}), 404

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
        track_id = response_data['tracks']['items'][0]['id']
        return track_id
    else:
        return None

@app.route("/agregar", methods=["POST"])
def add_song(): #toma la info para agregarla a la db con post
    song_details = request.get_json() #creo lo que el cliente agrega como cancion nueva. get json para que se imprima 
    song_id = obtener_id(song_details["artist"], song_details["song"])
    id=len(db_songs.get_songs()) + 1
    track_info = sp.track(obtener_id(song_details["artist"], song_details["song"]))
    popularity = track_info['popularity']
    if song_id:
        # Crear una nueva canción con el ID obtenido
        new_song = {
        "id": id,
        "song_id": song_id,
        "song": song_details["song"],
        "artist": song_details["artist"],
        "popularity": popularity,
        "genre": song_details["genre"],
        "explicit": song_details["explicit"],
        "feat": song_details["feat"],
        "feat_with": song_details["feat_with"]
        }
        # Agregar la canción a la base de datos
        db_songs.add_song(new_song["id"],new_song["song_id"],new_song["song"],new_song["artist"],new_song["popularity"],new_song["genre"], new_song["explicit"], new_song["feat"],new_song["feat_with"])
        return jsonify({"message": "Song successfully added"}), 200
    else:
        return jsonify({"message": "Could not find song on Spotify"}), 404

@app.route("/songs/<int:id>", methods=["PUT"])
def update_song(id):
    song_details = request.get_json()
    songs = db_songs.get_songs()
    for song in songs:
        if song["id"] == id:
            song["song"] = song_details["song"]
            song["popularity"] = song_details["popularity"]
            song["explicit"] = song_details["explicit"]
            song["feat"] = song_details["feat"]
            song["feat_with"] = song_details["feat_with"]
            db_songs.update_song(id, song)
            return jsonify({"message": "Song successfully updated"}), 200
    return jsonify({"message": "Song not found"}), 404

@app.route("/songs/<int:id>", methods=["DELETE"])
def delete_song(id):
    songs = db_songs.get_songs()
    for song in songs:
        if song["id"] == id:
            db_songs.delete_song(id)
            return jsonify({"message": "Song successfully deleted"}), 200
    return jsonify({"message": "Song not found"}), 404

if __name__ == "__main__":
    db_songs.create_tables()
    db_songs.insert_songs()
    app.run(debug=True, port=4000)