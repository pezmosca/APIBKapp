#!flask/bin/python
from flask import Flask, jsonify, send_file, request, make_response, flash, Response, stream_with_context
from flask_cors import CORS, cross_origin #habilitem cross domain api
from flask.ext.httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

import sqlite3, requests, os, hashlib, uuid, json

URL_CLIENT_TAHOE = 'http://192.168.5.240:3456'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'gz'])

auth = HTTPBasicAuth()

def new_salted_password(password):
    salt = uuid.uuid4().hex
    return str(hashlib.sha512(password + salt).hexdigest())

@auth.hash_password
def get_hash_password(username, password):
    salt = get_user_salt(username)
    return hashlib.sha512(str(password).encode('utf-8') + str(salt).encode('utf-8')).hexdigest()

@auth.get_password
def get_password(username):
    conn = sqlite3.connect('users.bd')
    password = get_user_password(username, conn)
    conn.close()
    return password


def exist_user(user):
    conn = sqlite3.connect('users.bd')
    cursor = conn.execute("SELECT * FROM USERS WHERE nick =?", [str(user)])
    if not cursor.fetchall():
        conn.close()
        return False
    else:
        conn.close()
        return True

def insert_furl(furl, conn):
    conn.execute("INSERT INTO GESTION (FURL) VALUES (?);", [furl]);
    conn.commit()

def get_furl(conn):
    cursor = conn.execute("SELECT FURL FROM GESTION")
    return cursor.fetchone()[0]

def get_user_dir_cap(user, conn):
    cursor = conn.execute("SELECT dircap FROM USERS WHERE nick =?", [str(user)])
    return cursor.fetchone()[0]

def get_user_password(user, conn):
    cursor = conn.execute("SELECT password FROM USERS WHERE nick =?", [str(user)])
    return cursor.fetchone()[0]

def get_user_salt(user):
    conn = sqlite3.connect('users.bd')
    cursor = conn.execute("SELECT salt FROM USERS WHERE nick =?", [str(user)])
    salt = cursor.fetchone()[0]
    conn.close()
    return salt

def sign_up_user(user, password, dircap):
    #conn.execute("INSERT INTO USERS (NICK, PASSWORD, DIRCAP) \
    	#VALUES (?, ?, ?);", [str(user), new_salted_password(password), str(dircap)]);
    conn = sqlite3.connect('users.bd')
    salt = uuid.uuid4().hex
    password = hashlib.sha512(str(password).encode('utf-8') + str(salt).encode('utf-8')).hexdigest()
    conn.execute("INSERT INTO USERS (NICK, SALT, PASSWORD, DIRCAP) \
    	VALUES (?, ?, ?, ?);", [str(user), salt, password, str(dircap)]);

    conn.commit()
    conn.close()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/api/<user>/files', methods=['GET'])
@auth.login_required
def get_files_user(user):
    if auth.username() == user:
        conn = sqlite3.connect('users.bd')
        dircap = get_user_dir_cap(user, conn)
        conn.close()
        return requests.get(URL_CLIENT_TAHOE + '/uri/' + dircap + "?t=json").text
    else:
        return unauthorized()

##GUARRADA PERO FUNCIONA##
#@app.route('/api/<user>/files', methods=['GET', 'POST'])
#def get_files_user(user):
#    conn = sqlite3.connect('users.bd')
#    credentials = request.get_json()
#    if credentials == None:
#        return make_response(jsonify({'error': 'Unauthorized access'}), 401)
#    if credentials['user'] == user and credentials['password'] == get_user_password(user, conn):
#        dircap = get_user_dir_cap(user, conn)
#        conn.close()
#        return requests.get(URL_CLIENT_TAHOE + '/uri/' + dircap + "?t=json").text
#    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/api/<user>/<fileName>', methods=['GET'])
@auth.login_required
def get_file_user(user, fileName):
    if auth.username() == user:
        if request.args.get('t') == "info":
            return fileName
        else:
            conn = sqlite3.connect('users.bd')
            dircap = get_user_dir_cap(user, conn)
            conn.close()
            print(URL_CLIENT_TAHOE + '/uri/' + dircap + '/' + fileName)
            response = requests.get(URL_CLIENT_TAHOE + '/uri/' + dircap + '/' + fileName)
            return Response(stream_with_context(response.iter_content()), content_type = response.headers['content-type'])
    else:
        return unauthorized()

@app.route('/api/<user>/upload_file', methods=['POST'])
@auth.login_required
def upload_file_user(user):
    if auth.username() == user:
        conn = sqlite3.connect('users.bd')
        dircap = get_user_dir_cap(user, conn)
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
    else:
        return unauthorized()

@app.route('/api/signup', methods=["POST"])
def sign_up():
    #FALTA MIRAR QUE NO EXISTA EL USER (ficar try exception)
    
    #user = jsonify(request.get_json(force=True))
    user = request.get_json()
    r = requests.post(URL_CLIENT_TAHOE + '/uri?t=mkdir&name=' + user['user'])
    sign_up_user(user['user'], user['password'], r.text)
    return jsonify(success=True)

@app.route('/api/signin', methods=["POST"])
def sign_in():
    json = request.get_json()
    if exist_user(json['user']):
        hash_in = get_hash_password(json['user'], json['password'])
        hash_out = get_password(json['user'])
        if hash_in == hash_out:
            return jsonify(success=True)
        else:
            return jsonify(success=False)
    
    return jsonify(success=False)

@app.route('/api/gestion', methods=["GET", "POST"])
def gestion():
    if request.method == 'GET':
        conn = sqlite3.connect('users.bd')
        furl = get_furl(conn)
        return str(furl)
    if request.method == 'POST':
        conn = sqlite3.connect('users.bd')
        insert_furl(request.form['furl'], conn)
        conn.close()
        return request.form['furl']



if __name__ == '__main__':
    app.secret_key = 'kubernetesydockers'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
