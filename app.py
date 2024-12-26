from flask import Flask, send_file, send_from_directory, jsonify, session
from main import *
from tts import *
import os
app = Flask(__name__)

react_folder = 'radio_jockey'
directory= os.getcwd()+ f'/{react_folder}/build/static'
# tracks=[]
next_song_info=None

tts_ready = False

app.secret_key = 'your_secret_key_here'
@app.route('/')
def index():
    x=1+1
    session['tracks'] = []
    path= os.getcwd()+ f'/radio_jockey/build'
    return send_from_directory(directory=path,path='index.html')

#
@app.route('/static/<folder>/<file>')
def css(folder,file):
    
    path = folder+'/'+file
    return send_from_directory(directory=directory,path=path)

@app.route('/rj')
def rj():
    path= os.getcwd()+ f'/rj/build'
    print(path)
    return send_from_directory(directory=path,path='index.html')


@app.route('/rj/static/<folder>/<file>')
def css_rj(folder,file):
    directory= os.getcwd()+ f'/rj/build/static'
    # path = folder+'/'+file
    return send_from_directory(directory=directory,path=f'{folder}/{file}')

def monitor_spotify_queue():
    global next_song_info
    while True:
        try:
            current_next_song = get_next_song()
            if current_next_song != next_song_info:
                next_song_info = current_next_song  # Update the next song info
                if next_song_info:
                    print(f"Next song updated: {next_song_info[1]} by {next_song_info[2]}")
                else:
                    print("No upcoming songs in the queue.")
            time.sleep(5) 
        except Exception as e:
            print(f"Error monitoring Spotify queue: {e}")
            time.sleep(5)  # Handle errors and retry after a delay


def start_monitoring_thread():
    monitor_thread = threading.Thread(target=monitor_spotify_queue)
    monitor_thread.daemon = True  # Daemon thread will exit when the main program exits
    monitor_thread.start()

@app.route('/host_spotify',  methods=['POST'])
def handle_spotify():
    global tts_ready
    while True:
        playback=spotifyObject.current_playback()
        if playback['is_playing']:
            break
    song_id=spotifyObject.current_playback().get('item')['id']
    next_song()  
    eventlet.sleep(2)
    song_2=spotifyObject.current_playback().get('item')
    previous_song()
    eventlet.sleep(2)
    pause_song()
    add_to_queue(song_id)
    eventlet.sleep(2)
    session['tracks']=get_queue()
    if (session['tracks'][1][0]!=song_2['id']):
        session['tracks'].insert(1,(song_2['id'],song_2['name'],song_2['artists'][0]['name']))
    next_song()
    pause_song()
    print(session['tracks'])
    cara_tts(rj_speak(f'song name: {session['tracks'][0][1]} artist: {session['tracks'][0][2]}'),"song.wav")
    tts_ready=True
    return jsonify({"status": "tts_ready"})

       
@app.route('/check_tts_status', methods=['GET'])
def check_tts_status():
    global tts_ready

    # Return whether the TTS audio is ready
    if tts_ready:
        tts_ready=False
        return jsonify({"status": "ready"})
    else:
        return jsonify({"status": "not_ready"})



@app.route('/get-audio/<filename>', methods=['GET'])
def get_audio(filename):
    wav_file_path = f"{filename}.wav"  
    return send_file(wav_file_path, mimetype='audio/wav')

@app.route('/resume-song', methods=['POST'])
def resume_spotify():
    global tts_ready
    if len(session['tracks'])==0:        
        session['tracks']=get_queue()
        print(session['tracks'])
        
    resume_song()
    current_track=session['tracks'].pop(0)
    cara_tts(rj_speak(f'previous song:{current_track[0][1]} next song:{session['tracks'][0][1]} artist:{session['tracks'][0][2]}'),"song.wav")
    session['tracks']=get_queue()
    wait_for_song_to_end(False)
    pause_song()
    tts_ready=True
    return jsonify({"status": "tts_ready"})

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return '', 204  # Respond with no content (204)
if __name__ == '__main__':
    # start_monitoring_thread()
    app.run(debug=True, threaded=True)