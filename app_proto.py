# app.py
from flask import Flask, request, render_template, jsonify,redirect, url_for, current_app
from main import *
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)


playlist=Stack()
def play_tracks(playlist):
    while not playlist.is_empty():
        current_track=playlist.pop()
        socketio.emit('playlist_update', {'value': playlist.items},namespace='/')
        eventlet.sleep(0)
        speak("song.wav")
        try:
            spotifyObject.start_playback(uris=[f'spotify:track:{current_track[0]}'])

        except spotipy.exceptions.SpotifyException as e:
            print("Token expired, refreshing token...")
            refresh_spotify_token()
            spotifyObject.start_playback(uris=[f'spotify:track:{current_track[0]}'])

        cara_tts(rj_speak('song end'), "end.wav")
        while True:
            try:
                playback = spotifyObject.current_playback()
            except:
                print("Token expired, refreshing token...")
                refresh_spotify_token()
                playback = spotifyObject.current_playback()
            progress_ms = playback['progress_ms']
            duration_ms = playback['item']['duration_ms']
            if duration_ms-progress_ms<=30000:
                cara_tts(rj_speak(f'song name: {playlist.items[-1][1]}'), "song.wav")
                break   
        wait_for_song_to_end(True)


def start_radio(song_name):
    with app.app_context():
        socketio.emit('playlist_update', {'value': playlist.items},namespace='/')
        # eventlet.sleep(0)
        track_id=get_track_id(song_name)
        alter_recommendations(playlist,track_id)
        playlist.push((track_id,song_name))
        socketio.emit('playlist_update', {'value': playlist.items},namespace='/')
        eventlet.sleep(0)
        print(playlist.items)  
        cara_tts(rj_speak(f'song name: {song_name}'),"song.wav")
        


def play_tracks_thread(song_name):
    start_radio(song_name)

@socketio.on('add_song')
def start_add_task(data):
    print('hello')
    song = data.get('param')
    print(f"Start adding song: {song}")
    track_id=get_track_id(song)
    song=get_track_name(track_id)
    playlist.push((track_id,song))
    socketio.emit('playlist_update', {'value': playlist.items},namespace='/')


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_task')
def handle_start_radio(data):
    play_tracks(playlist)
    song = data.get('param')
    start_radio(song)
    socketio.start_background_task(play_tracks,playlist)



if __name__ == '__main__':
    socketio.run(app, debug=True)
