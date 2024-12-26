# # app.py
# from flask import Flask,render_template

# def create_app():
#     app = Flask(__name__, template_folder='templates')
#     register_resources(app)
#     return app

# def register_resources(app):
#     @app.route('/')
#     def index():
#         return render_template("index.html")

# if __name__ == '__main__':
#     app=create_app()
#     app.run(debug=True)
##########################

from flask import Flask, send_from_directory
import os
app = Flask(__name__)

react_folder = 'radio_jockey'
directory= os.getcwd()+ f'/{react_folder}/build/static'


@app.route('/')
def index():
    path= os.getcwd()+ f'/radio_jockey/build'
    print(path)
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


#
@app.route('/rj/static/<folder>/<file>')
def css_rj(folder,file):
    directory= os.getcwd()+ f'/rj/build/static'
    # path = folder+'/'+file
    return send_from_directory(directory=directory,path=f'{folder}/{file}')


# @app.route('/rj/manifest.json')
# def manifest():
#     directory = os.getcwd() + '/rj/build'
#     return send_from_directory(directory=directory, path='manifest.json')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)