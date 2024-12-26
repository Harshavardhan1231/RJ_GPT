from flask import Flask, request, render_template, jsonify,redirect, url_for,current_app
# from main import *
from flask_socketio import SocketIO
import time
import threading

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("index.html")

def long_running_task(param):
    # Simulate a long-running task with dynamic variable updates
    with app.app_context():

        dynamic_var = f"Processing: {param}"
        socketio.emit('variable_update', {'value': dynamic_var},namespace='/')
        print('event emitted')
        for i in range(5):
            socketio.sleep(2)  # Simulate work being done
            progress = (i + 1) * 20
            dynamic_var = f"Processing {param}: {progress}% complete"
            socketio.emit('variable_update', {'value': dynamic_var},namespace='/')
        dynamic_var = f"Completed: {param}"
   
        socketio.emit('variable_update', {'value': dynamic_var},namespace='/')
        socketio.emit('task_complete', {'result': dynamic_var},namespace='/')

    
@socketio.on('start_task')
def handle_start_task(data):
    print(current_app.app_context())
    param = data.get('param')
    socketio.start_background_task(long_running_task,param)
    # thread = threading.Thread(target=long_running_task, args=(param,))
    # thread.start()

if __name__ == '__main__':
    socketio.run(app, debug=True)