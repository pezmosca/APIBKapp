#!flask/bin/python
from flask import Flask, jsonify, send_file, request, make_response
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)

import sqlite3, requests, os, hashlib, uuid

URL_CLIENT_TAHOE = 'http://192.168.1.6:3456'

auth = HTTPBasicAuth()

def hashPassword(password):
    salt = uuid.uuid4().hex
    return str(hashlib.sha512(password + salt).hexdigest())

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
@auth.login_required
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
@auth.login_required
def get_file_user(user, fileName):
    if request.args.get('t') == "info":
        return fileName
    else:
        conn = sqlite3.connect('users.bd')
        dircap = getUserDirCap(user, conn)
        conn.close()
        response = requests.get(URL_CLIENT_TAHOE + '/uri/' + dircap + '/' + fileName)
        f = open(fileName, 'wb')
        f.write(response.content)
        os.remove(fileName)
        return send_file(f, as_attachment=True, attachment_filename=fileName)

@app.route('/api/user/upload_file', methods=['POST'])
def upload_file_user():
    files = {'upload_file': open('file.txt', 'rb')}

@app.route('/api/signup', methods=["POST"])
def signup():
    conn = sqlite3.connect('users.bd')
    #user = jsonify(request.get_json(force=True))
    user = request.get_json()
    signUpUser(user['user'], user['password'], user['dircap'], conn)
    conn.close()
    return "OK"

if __name__ == '__main__':
    app.run(debug=True)
