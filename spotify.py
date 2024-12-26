import json 
import spotipy 
import webbrowser
from dotenv import load_dotenv
import os
import time
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tts import speak
import eventlet
load_dotenv()



# Spotify credentials
username = os.getenv('USER_NAME')
clientID = os.getenv('SPOTIPY_CLIENT_ID')
clientSecret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

scope = 'user-read-playback-state user-modify-playback-state'
# Authenticate and get access token
oauth_object = SpotifyOAuth(clientID, clientSecret, redirect_uri)
token_dict = oauth_object.get_cached_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
# user_name = spotifyObject.current_user()
# spotifyObject = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id=clientID,
#     client_secret=clientSecret,
#     redirect_uri=redirect_uri,
#     scope=scope))


def play_song(song_name, artist):

    if artist=='': search_query=f'track:{song_name}'
    else:search_query=f'track:{song_name} artist:{artist}'
    
    # print (spotifyObject.search(search_query,1,0,'track'))
    json_response =spotifyObject.search(search_query,1,0,'track')
    json.dumps(json_response, sort_keys=True, indent=4)

    # data=json.loads(json_response)
    # track_external_urls = data['tracks']['items'][0]['external_urls']
    # print(track_external_urls)
    with open('search_response.json', 'w') as json_file:
        json.dump(json_response, json_file, indent=4)
    if json_response['tracks']['items']:
        track = json_response['tracks']['items'][0]
        spotify_url = track['external_urls']['spotify']
        webbrowser.open(spotify_url)
        return spotify_url
    else:
        return "Track not found"


def refresh_spotify_token():
    global token, spotifyObject
    token_dict = oauth_object.get_cached_token()
    token = token_dict['access_token']
    spotifyObject = spotipy.Spotify(auth=token)

def get_playlist_id(playlist_name):

      # Search for playlists with the given name
    search_query=f'playlist:{playlist_name}'
    json_response = spotifyObject.search(search_query, type='playlist', limit=10)
    json.dumps(json_response, sort_keys=True, indent=4)
    
    
    with open('search_response.json', 'w') as json_file:
        json.dump(json_response, json_file, indent=4)
    if json_response['playlists']['items']:
        playlist = json_response['playlists']['items'][0]
        id = playlist['id']
        return id
    else:
        return "Playlist not found"

def get_track_id(track_name, artist_name=None):
    query = f"track:{track_name}"
    if artist_name:
        query += f" artist:{artist_name}"

    results = spotifyObject.search(q=query, type='track', limit=1)
    tracks = results['tracks']['items']
    
    if tracks:
        return tracks[0]['id']
    else:
        return None


def get_playlist_tracks(playlist_id):

    tracks=[]
    results = spotifyObject.playlist_tracks(playlist_id, fields='items(track(id))', limit=100)

    for item in results['items']:
        tracks.append(item['track']['id'])
    return tracks



def get_track_name(track_id):
    track = spotifyObject.track(track_id)
    track_name = track['name']
    return track_name

def pause_song():
    try:
        spotifyObject.pause_playback()
        print("Playback paused.")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error pausing playback: {e}")

def resume_song():
    try:
        spotifyObject.start_playback()
        print("Playback resumed.")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error resuming playback: {e}")

def next_song():
    try:
        spotifyObject.next_track()
        print("Skipped to the next track.")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error skipping to the next track: {e}")

def previous_song():
    try:
        spotifyObject.previous_track()
        print("Went back to the previous track.")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error going back to the previous track: {e}")

def wait_for_song_to_end(sp=False):
    while True:
        try:
            playback = spotifyObject.current_playback()
        except:
            print("Token expired, refreshing token...")
            refresh_spotify_token()
            playback = spotifyObject.current_playback()
        if playback is None or playback['is_playing'] == False:
            return
        progress_ms = playback['progress_ms']
        duration_ms = playback['item']['duration_ms']

        if sp and duration_ms-progress_ms<=7000:
            speak("end.wav")
            return
        elif duration_ms-progress_ms<=2000:  # Adding a small buffer of 1 second
            return
        eventlet.sleep(1) 

