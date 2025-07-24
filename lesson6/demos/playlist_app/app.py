from flask import Flask, render_template, request  
  
app = Flask(__name__)  
  
@app.route('/')  
def home():  
    return render_template('home_playlist.html')  
  
@app.route('/generate', methods=['POST'])  
def generate():  
    artist = request.form.get('artist')  
    num_songs = int(request.form.get('num_songs'))  
    songs, album_covers = get_songs_and_covers(artist)  
    playlist = build_playlist(songs, album_covers, num_songs)  
    return render_template('playlist.html', playlist=playlist)  
  
def get_songs_and_covers(artist):  
    artists = ["Michael Jackson", "Drake", "Kendrick Lamar", "Justin Timberlake"]  
    if artist == "Michael Jackson":  
        songs = ["Billie Jean", "Thriller", "Beat It"]  
    elif artist == "Drake":  
        songs = ["God's Plan", "Hotline Bling", "In My Feelings"]  
    elif artist == "Kendrick Lamar":  
        songs = ["HUMBLE.", "DNA.", "Alright"]  
    elif artist == "Justin Timberlake":  
        songs = ["Cry Me a River", "Can't Stop the Feeling!", "Mirrors"]  
    else:  
        songs = []  
    album_covers = ["https://placehold.co/200x200.png"] * len(songs)  
    return songs, album_covers  
  
def build_playlist(songs, album_covers, num_songs):  
    playlist = []  
    for song in songs[:num_songs]:  
        playlist.append({"title": song, "cover": album_covers[songs.index(song)]})  
    return playlist  
  
if __name__ == '__main__':  
    app.run(debug=True)  