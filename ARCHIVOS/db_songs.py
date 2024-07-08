import sqlite3
import json

def connect_to_database(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as error_conexion:
        print(f"Error al conectar a la base de de datos '{db_file}': {error_conexion}")
        return None

def create_tables():
    conn = connect_to_database('songs.db')
    try:
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS songs')
        c.execute('''CREATE TABLE IF NOT EXISTS songs
                    (id INTEGER PRIMARY KEY,
                    song_id TEXT,
                    song TEXT,
                    artist TEXT,
                    popularity INTEGER,
                    genre TEXT,
                    explicit BOOLEAN,
                    feat BOOLEAN,
                    feat_with TEXT)''')
        conn.commit()
        print("La tabla se ha creado correctamente")
    except sqlite3.Error as error_creacion:
        print(f"Error al crear la tabla 'songs': {error_creacion}")

def insert_songs(): 
    songs = [
        {"id": 1, "song_id": "7lPN2DXiMsVn7XUKtOW1CS", "song": "drivers license", "artist": "Olivia Rodrigo", "popularity": 92, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 2, "song_id": "5QO79kh1waicV47BqGRL3g", "song": "Save Your Tears", "artist": "The Weeknd", "popularity": 90, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 3, "song_id": "0VjIjW4GlUZAMYd2vXMi3b", "song": "Blinding Lights", "artist": "The Weeknd", "popularity": 95, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 4, "song_id": "463CkQjx2Zk1yXoBuierM9", "song": "Levitating", "artist": "Dua Lipa", "popularity": 88, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 5, "song_id": "67BtfxlNbhBmCDR2L2l8qd", "song": "Montero (Call Me By Your Name)", "artist": "Lil Nas X", "popularity": 89, "genre": "hip hop", "explicit": True, "feat": False, "feat_with": None},
        {"id": 6, "song_id": "4iJyoBOLtHqaGxP12qzhQI", "song": "Peaches (feat. Daniel Caesar & Giveon)", "artist": "Justin Bieber", "popularity": 87, "genre": "pop", "explicit": False, "feat": True, "feat_with": json.dumps(["Daniel Caesar", "Giveon"])},
        {"id": 7, "song_id": "6PERP62TejQjgHu81OHxgM", "song": "good 4 u", "artist": "Olivia Rodrigo", "popularity": 93, "genre": "pop rock", "explicit": True, "feat": False, "feat_with": None},
        {"id": 8, "song_id": "7MAibcTli4IisCtbHKrGMh", "song": "Leave The Door Open", "artist": "Bruno Mars", "popularity": 91, "genre": "r&b", "explicit": False, "feat": True, "feat_with": json.dumps(["Anderson .Paak", "Silk Sonic"])},
        {"id": 9, "song_id": "6qBNQCJ4Cw6K1Ach3tDQoT", "song": "MONTERO", "artist": "Lil Nas X", "popularity": 86, "genre": "hip hop", "explicit": True, "feat": False, "feat_with": None},
        {"id": 10, "song_id": "6UelLqGlWMcVH1E5c4H7lY", "song": "Watermelon Sugar", "artist": "Harry Styles", "popularity": 89, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 11, "song_id": "4MzXwWMhyBbmu6hOcLVD49", "song": "DÁKITI", "artist": "Bad Bunny", "popularity": 88, "genre": "reggaeton", "explicit": True, "feat": True, "feat_with": json.dumps(["Jhay Cortez"])},
        {"id": 12, "song_id": "35mvY5S1H3J2QZyna3TFe0", "song": "positions", "artist": "Ariana Grande", "popularity": 87, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 13, "song_id": "7lidXGPXPYLNThITAOTlkK", "song": "Heat Waves", "artist": "Glass Animals", "popularity": 85, "genre": "indie pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 14, "song_id": "6PQ88X9TkUIAUIZJHW2upE", "song": "deja vu", "artist": "Olivia Rodrigo", "popularity": 86, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 15, "song_id": "1OuBO4z6RJcveYVddZDItn", "song": "Friday (feat. Mufasa & Hypeman) - Dopamine Re-Edit", "artist": "Riton, Nightcrawlers", "popularity": 83, "genre": "house", "explicit": False, "feat": True, "feat_with": json.dumps(["Mufasa", "Hypeman"])},
        {"id": 16, "song_id": "1XLWox9w1Yvbodui0SRhUQ", "song": "Astronaut In The Ocean", "artist": "Masked Wolf", "popularity": 88, "genre": "hip hop", "explicit": True, "feat": False, "feat_with": None},
        {"id": 17, "song_id": "27NovPIUIRrOZoCHxABJwK", "song": "WITHOUT YOU", "artist": "The Kid LAROI", "popularity": 87, "genre": "pop rap", "explicit": True, "feat": False, "feat_with": None},
        {"id": 18, "song_id": "3tjFYV6RSFtuktYl3ZtYcq", "song": "Mood (feat. iann dior)", "artist": "24kGoldn", "popularity": 90, "genre": "pop rap", "explicit": True, "feat": True, "feat_with": json.dumps(["iann dior"])},
        {"id": 19, "song_id": "2DEZmgHKAvm41k4J3R2E9Y", "song": "GOOBA", "artist": "6ix9ine", "popularity": 84, "genre": "hip hop", "explicit": True, "feat": False, "feat_with": None},
        {"id": 20, "song_id": "5T490vvoFNU6psep0NPmxs", "song": "Savage Love (Laxed - Siren Beat)", "artist": "Jawsh 685", "popularity": 88, "genre": "pop", "explicit": False, "feat": True, "feat_with": json.dumps(["Jason Derulo"])},
        {"id": 21, "song_id": "7ytR5pFWmSjzHJIeQkgog4", "song": "Rockstar (feat. Roddy Ricch)", "artist": "DaBaby", "popularity": 89, "genre": "hip hop", "explicit": True, "feat": True, "feat_with": json.dumps(["Roddy Ricch"])},
        {"id": 22, "song_id": "3Dv1eDb0MEgF93GpLXlucZ", "song": "Say So", "artist": "Doja Cat", "popularity": 86, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 23, "song_id": "24ySl2hOPGCDcxBxFIqWBu", "song": "Rain On Me (with Ariana Grande)", "artist": "Lady Gaga", "popularity": 87, "genre": "pop", "explicit": False, "feat": True, "feat_with": json.dumps(["Ariana Grande"])},
        {"id": 24, "song_id": "4HBZA5flZLE435QTztThqH", "song": "Stuck with U (with Justin Bieber)", "artist": "Ariana Grande", "popularity": 85, "genre": "pop", "explicit": False, "feat": True, "feat_with": json.dumps(["Justin Bieber"])},
        {"id": 25, "song_id": "0nbXyq5TXYPCO7pr3N8S4I", "song": "The Box", "artist": "Roddy Ricch", "popularity": 90, "genre": "hip hop", "explicit": True, "feat": False, "feat_with": None},
        {"id": 26, "song_id": "696DnlkuDOXcMAnKlTgXXK", "song": "ROXANNE", "artist": "Arizona Zervas", "popularity": 88, "genre": "pop rap", "explicit": True, "feat": False, "feat_with": None},
        {"id": 27, "song_id": "017PF4Q3l4DBUiWoXk4OWT", "song": "Break My Heart", "artist": "Dua Lipa", "popularity": 89, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 28, "song_id": "1rgnBhdG2JDFTbYkYRZAku", "song": "Dance Monkey", "artist": "Tones And I", "popularity": 90, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 29, "song_id": "21jGcNKet2qwijlDFuPiPb", "song": "Circles", "artist": "Post Malone", "popularity": 92, "genre": "pop rap", "explicit": False, "feat": False, "feat_with": None},
        {"id": 30, "song_id": "41L3O37CECZt3N7ziG2z7l", "song": "Yummy", "artist": "Justin Bieber", "popularity": 85, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 31, "song_id": "3AzjcOeAmA57TIOr9zF1ZW", "song": "Physical", "artist": "Dua Lipa", "popularity": 86, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 32, "song_id": "6WrI0LAC5M1Rw2MnX2ZvEg", "song": "Don't Start Now", "artist": "Dua Lipa", "popularity": 87, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 33, "song_id": "2xLMifQCjDGFmkHkpNLD9h", "song": "SICKO MODE", "artist": "Travis Scott", "popularity": 88, "genre": "hip hop", "explicit": True, "feat": False, "feat_with": None},
        {"id": 34, "song_id": "2Fxmhks0bxGSBdJ92vM42m", "song": "bad guy", "artist": "Billie Eilish", "popularity": 91, "genre": "pop", "explicit": False, "feat": False, "feat_with": None},
        {"id": 35, "song_id": "2qOm7ukLyHUXWyR4ZWLwxA", "song": "Senorita", "artist": "Shawn Mendes", "popularity": 90, "genre": "pop", "explicit": False, "feat": True, "feat_with": json.dumps(["Camila Cabello"])}
    ]

    conn = connect_to_database('songs.db')
    c = conn.cursor()

    try:
        for song in songs:
            c.execute('''INSERT INTO songs (id, song_id, song, artist, popularity, genre, explicit, feat, feat_with)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (song["id"], song["song_id"], song["song"], song["artist"], song["popularity"], song["genre"], song["explicit"], song["feat"], song["feat_with"]))
        conn.commit()
        print("Canciones insertadas en la base de datos con éxito.")
    except sqlite3.Error as error:
        print(f"Error al insertar canciones: {error}")
    finally:
        conn.close()


def get_songs():
    conn = connect_to_database('songs.db')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM songs")
        songs = c.fetchall()

        songs_list = []
        for song in songs:
            song_dict = {
                "id": song[0],
                "song_id": song[1],
                "song": song[2],
                "artist": song[3],
                "popularity": song[4],
                "genre": song[5],
                "explicit": bool(song[6]),
                "feat": bool(song[7]),
                "feat_with": json.loads(song[8]) if song[8] else None
            }
            songs_list.append(song_dict)

        return songs_list

    except sqlite3.Error as error:
        print(f"Error al obtener las canciones: {error}")
        return []

    finally:
        conn.close()

def add_song(id, song_id, song, artist, popularity, genre, explicit, feat, feat_with):
    conn = sqlite3.connect('songs.db')
    c = conn.cursor()
    c.execute('INSERT INTO songs (id, song_id, song, artist, popularity, genre, explicit, feat, feat_with) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (id, song_id, song, artist, popularity, genre, explicit, feat, json.dumps(feat_with)))
    conn.commit()
    conn.close()

def update_song(id, updated_song):
    conn = sqlite3.connect('songs.db')
    c = conn.cursor()
    c.execute('''UPDATE songs
                 SET song = ?, popularity = ?, explicit = ?, feat = ?, feat_with = ?
                 WHERE id = ?''',
              (updated_song["song"], updated_song["popularity"], updated_song["explicit"], updated_song["feat"], json.dumps(updated_song["feat_with"]), id))
    conn.commit()
    conn.close()
    return True

def delete_song(id):
    conn = sqlite3.connect('songs.db')
    c = conn.cursor()
    c.execute('DELETE FROM songs WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return True if c.rowcount > 0 else False

# Ejemplo de uso:
if __name__ == "__main__":
    create_tables()
    insert_songs()
    songs = get_songs()