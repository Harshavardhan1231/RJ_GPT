from spotify import *
import random
import time
from rj import rj_speak
from tts import speak
from dj_cara import cara_tts
from stack import Stack
import threading
from queue import Queue, Empty
import eventlet

def play_tracks_in_random_order(playlist_name):
    
    playlist_id = get_playlist_id(playlist_name)
    if id == "Playlist not found":
        print("Playlist not found")
        return
    

    tracks = get_playlist_tracks(playlist_id) 
    random.shuffle(tracks)
    first_track_id=tracks[0]
    first_song_name=get_track_name(first_track_id)


    # cara_tts(rj_speak(f'playlist:{playlist_name}',[]),"playlist.wav")
    cara_tts(rj_speak(f'{playlist_name}: {first_song_name}'),"song.wav")
    
    # speak("playlist.wav")
    time.sleep(1)
    speak("song.wav")
    if not tracks:
        print("No tracks found in the playlist")
        return
        
    
    for i in range(len(tracks)):
        track_id=tracks[i]
        try:
            spotifyObject.start_playback(uris=[f'spotify:track:{track_id}'])
            print(f"Playing track ID: {track_id}")
        except spotipy.exceptions.SpotifyException as e:
            print("Token expired, refreshing token...")
            refresh_spotify_token()
            spotifyObject.start_playback(uris=[f'spotify:track:{track_id}'])

        next_track_id=tracks[i+1]
        next_song_name=get_track_name(next_track_id)
        cara_tts(rj_speak('song end'),"end.wav")
        cara_tts(rj_speak(f'song name: {next_song_name}'),"song.wav")
        
        wait_for_song_to_end(True)

        # speak("end.wav")
        time.sleep(1)
        speak("song.wav")
        


def get_current_playback_track():
    playback = spotifyObject.current_playback()
    if playback and playback['is_playing']:
        return playback['item']['id']
    return None



def get_recommendations(track_id='',limit=5):
    if track_id=='':
        recommendations = spotifyObject.recommendations(seed_tracks=[get_current_playback_track()], limit=limit)
    else:
        recommendations = spotifyObject.recommendations(seed_tracks=[track_id], limit=limit)
    return [(track['id'], track['name']) for track in recommendations['tracks']]




def alter_recommendations(playlist,track_id=''):
    if track_id=='':
        recommedations=get_recommendations(10)
    else:
        recommedations=get_recommendations(track_id,10)
    for track in recommedations:
        playlist.push(track)
        
def get_user_input(input_queue):
    ns = input("Do you have next song? press 'y' or 'n'").strip()
    input_queue.put(ns)
    if ns == 'y':
        next_song = input('Which song?').strip()
        input_queue.put(next_song)
        recommend = input("Do you want to alter recommendations? press 'y' or 'n'").strip()
        input_queue.put(recommend)

def play_recommended_tracks(song_name):
    
    playlist=Stack()
    current_track_id=get_track_id(song_name)
    cara_tts(rj_speak(f'song name: {song_name}'),"song.wav")
    cara_tts(rj_speak('song end'),"end.wav")
    speak("song.wav")

    try:
        spotifyObject.start_playback(uris=[f'spotify:track:{current_track_id}'])

    except spotipy.exceptions.SpotifyException as e:
        print("Token expired, refreshing token...")
        refresh_spotify_token()
        spotifyObject.start_playback(uris=[f'spotify:track:{current_track_id}'])


    eventlet.sleep(2)
    alter_recommendations(playlist)

    # print(playlist.items[-1][1])
    cara_tts(rj_speak(f'song name: {playlist.items[-1][1]}'),"song.wav")
      
    # cara_tts(rj_speak('song end'),"end.wav")
    wait_for_song_to_end(True)


    while not playlist.is_empty():

        print(playlist.items)

        current_track=playlist.pop()
        speak("song.wav")

        try:
            spotifyObject.start_playback(uris=[f'spotify:track:{current_track[0]}'])

        except spotipy.exceptions.SpotifyException as e:
            print("Token expired, refreshing token...")
            refresh_spotify_token()
            spotifyObject.start_playback(uris=[f'spotify:track:{current_track[0]}'])
        
        input_queue=Queue()
        input_thread=threading.Thread(target=get_user_input, args=(input_queue,))
        input_thread.start()
        
        tts_thread = threading.Thread(target=cara_tts, args=(rj_speak('song end'), "end.wav"))
        tts_thread.start()
        
        user_input_received=False
        while True:
            try:
                ns = input_queue.get_nowait()
                user_input_received = True
                if ns == 'n':
                    break
                elif ns=='y':
                    next_song = input_queue.get()
                    next_song_id = get_track_id(next_song)
                    next_song_name=get_track_name(next_song_id)
                    recommend = input_queue.get()
                    if recommend=='y':
                        alter_recommendations(playlist)
                        # time.sleep(1)
                    playlist.push((next_song_id,next_song_name))
                    break
            except Empty:
                try:
                    playback = spotifyObject.current_playback()
                except:
                    print("Token expired, refreshing token...")
                    refresh_spotify_token()
                    playback = spotifyObject.current_playback()
                progress_ms = playback['progress_ms']
                duration_ms = playback['item']['duration_ms']
                if duration_ms-progress_ms<=30000:
                    if not user_input_received:
                        ns='n'
                        break
        if playlist.size() > 0:
            cara_tts(rj_speak(f'song name: {playlist.items[-1][1]}'), "song.wav")   
        wait_for_song_to_end(True)
        input_thread.join(timeout=1)
        tts_thread.join(timeout=1)
        eventlet.sleep(1)

playlist=Stack()    
added_tracks = set()

def get_queue():
    queue = spotifyObject._get('me/player/queue')
    track_names = []
    upcoming_tracks = queue.get('queue', [])
    for track in upcoming_tracks:
        track_names.append((track['id'],track['name'],track['artists'][0]['name']))
    return track_names

def get_next_song():
    queue = spotifyObject._get('me/player/queue')
    upcoming_tracks = queue.get('queue', [])
    if upcoming_tracks:
        next_track = upcoming_tracks[0]  # Get the first track from the queue
        return (next_track['id'], next_track['name'], next_track['artists'][0]['name'])
    else:
        return None 

def add_to_queue(track_id):
     track_uri=f"spotify:track:{track_id}"
     if track_id not in added_tracks:
        spotifyObject.add_to_queue(uri=track_uri)
        added_tracks.add(track_id)

def refresh_queue():
    songs=get_queue()
    for song in songs:
        add_to_queue(song[0])
    return songs

def host_spotify():
    while True:
        playback=spotifyObject.current_playback()
        if playback['is_playing']:
            break
    song_id=spotifyObject.current_playback().get('item')['id']
    next_song()  
    previous_song()
    pause_song()
    tracks=[]
    add_to_queue(song_id)
    eventlet.sleep(2)
    while True:
        if len(tracks)==0:        
            tracks=get_queue()
            print(tracks)
            cara_tts(rj_speak(f'song name: {tracks[0][1]} artist: {tracks[0][2]}'),"song.wav")
            speak("song.wav")
            next_song()
        resume_song()
        current_track=tracks.pop(0)
        cara_tts(rj_speak(f'previous song:{current_track[0][1]} next song:{tracks[0][1]} artist:{tracks[0][2]}'),"end.wav")
        tracks=get_queue()
        wait_for_song_to_end(False)
        pause_song()
        speak("end.wav")


# host_spotify()
# while True:
#     print(get_next_song())
#     eventlet.sleep(5)

# play_recommended_tracks('Hello Lionel')
# print(get_current_playback_track())
# print(get_recommendations('7e89621JPkKaeDSTQ3avtg',10))