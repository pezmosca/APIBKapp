#!flask/bin/python
from flask import Flask, jsonify, send_file, request, make_response, flash, Response, stream_with_context
from flask.ext.httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename

app = Flask(__name__)

import sqlite3, requests, os, hashlib, uuid, json

URL_CLIENT_TAHOE = 'http://192.168.5.240:3456'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'gz'])

auth = HTTPBasicAuth()

def hashPassword(password):
    salt = uuid.uuid4().hex
    return str(hashlib.sha512(password + salt).hexdigest())

def existUser(user):
    cursor = conn.execute("SELECT * FROM USERS WHERE nick =?", [str(user)])
    if not cursor.fethcall():
        return False
    else:
        return True

def insertFurl(furl, conn):
    conn.execute("INSERT INTO GESTION (FURL) VALUES (?);", [furl]);
    conn.commit()

def getFurl(conn):
    cursor = conn.execute("SELECT FURL FROM GESTION")
    return cursor.fetchone()[0]

def getUserDirCap(user, conn):
    cursor = conn.execute("SELECT dircap FROM USERS WHERE nick =?", [str(user)])
    return cursor.fetchone()[0]

def getUserPassword(user, conn):
    cursor = conn.execute("SELECT password FROM USERS WHERE nick =?", [str(user)])
    return cursor.fetchone()[0]

def signUpUser(user, password, dircap, conn):
    #conn.execute("INSERT INTO USERS (NICK, PASSWORD, DIRCAP) \
    	#VALUES (?, ?, ?);", [str(user), hashPassword(password), str(dircap)]);

    conn.execute("INSERT INTO USERS (NICK, PASSWORD, DIRCAP) \
    	VALUES (?, ?, ?);", [str(user), password, str(dircap)]);

    conn.commit()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.get_password
def get_password(username):
    conn = sqlite3.connect('users.bd')
    password = getUserPassword(username, conn)
    conn.close()
    return password

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/api/<user>/files', methods=['GET'])
#@auth.login_required
def get_files_user(user):
    conn = sqlite3.connect('users.bd')
    dircap = getUserDirCap(user, conn)
    conn.close()
    return requests.get(URL_CLIENT_TAHOE + '/uri/' + dircap + "?t=json").text

##GUARRADA PERO FUNCIONA##
#@app.route('/api/<user>/files', methods=['GET', 'POST'])
#def get_files_user(user):
#    conn = sqlite3.connect('users.bd')
#    credentials = request.get_json()
#    if credentials == None:
#        return make_response(jsonify({'error': 'Unauthorized access'}), 401)
#    if credentials['user'] == user and credentials['password'] == getUserPassword(user, conn):
#        dircap = getUserDirCap(user, conn)
#        conn.close()
#        return requests.get(URL_CLIENT_TAHOE + '/uri/' + dircap + "?t=json").text
#    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/api/<user>/<fileName>', methods=['GET'])
#@auth.login_required
def get_file_user(user, fileName):
    if request.args.get('t') == "info":
        return fileName
    else:
        conn = sqlite3.connect('users.bd')
        dircap = getUserDirCap(user, conn)
        conn.close()
        print(URL_CLIENT_TAHOE + '/uri/' + dircap + '/' + fileName)
        response = requests.get(URL_CLIENT_TAHOE + '/uri/' + dircap + '/' + fileName)
        return Response(stream_with_context(response.iter_content()), content_type = response.headers['content-type'])

@app.route('/api/<user>/upload_file', methods=['POST'])
#@auth.login_required
def upload_file_user(user):
    conn = sqlite3.connect('users.bd')
    dircap = getUserDirCap(user, conn)
    conn.close()
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        #return redirect(request.url)
        return "MAL"
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        #return redirect(request.url)
        return "MAL"
    #if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    files = {'file': filename}
    return requests.post(URL_CLIENT_TAHOE + '/uri/' + dircap + '?t=upload', files=files).text
    #return "HELLO"

@app.route('/api/signup', methods=["POST"])
def signup():
    #FALTA MIRAR QUE NO EXISTA EL USER
    conn = sqlite3.connect('users.bd')
    #user = jsonify(request.get_json(force=True))
    user = request.get_json()
    r = requests.post(URL_CLIENT_TAHOE + '/uri?t=mkdir&name=' + user['user'])
    signUpUser(user['user'], user['password'], r.text, conn)
    conn.close()
    return "OK"

@app.route('/api/signin', methods=["POST"])
def signin():
    conn = sqlite3.connect('users.bd')
    json = request.get_json()
    if existUser(json['user']):
        pass

@app.route('/api/gestion', methods=["GET", "POST"])
def gestion():
    if request.method == 'GET':
        conn = sqlite3.connect('users.bd')
        furl = getFurl(conn)
        return str(furl)
    if request.method == 'POST':
        conn = sqlite3.connect('users.bd')
        insertFurl(request.form['furl'], conn)
        conn.close()
        return request.form['furl']



if __name__ == '__main__':
    app.secret_key = 'kubernetesydockers'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
