#!flask/bin/python
from flask import Flask, jsonify, send_file, request

app = Flask(__name__)

import sqlite3, requests, os

URL_CLIENT_TAHOE = 'http://192.168.1.6:3456'

def getUserDirCap(user, conn):
    cursor = conn.execute("SELECT dircap FROM USERS WHERE nick =?", [str(user)])
    return cursor.fetchone()[0]

@app.route('/api/<user>/files', methods=['GET'])
def get_files_user(user):
    conn = sqlite3.connect('users.bd')
    dircap = getUserDirCap(user, conn)
    conn.close()
    return requests.get(URL_CLIENT_TAHOE + '/uri/' + dircap + "?t=json").text

@app.route('/api/<user>/<fileName>', methods=['GET'])
def get_file_user(user, fileName):

    if request.args.get('t') == "info":
        return fileName
    else:
        conn = sqlite3.connect('users.bd')
        dircap = getUserDirCap("Pezmosca", conn)
        conn.close()
        response = requests.get(URL_CLIENT_TAHOE + '/uri/' + dircap + '/' + fileName)
        f = open("/home/toni/" + fileName, 'wb')
        f.write(response.content)
        os.remove("/home/toni/" + fileName)
        return send_file(f, as_attachment=True, attachment_filename=fileName)

@app.route('/api/user/upload_file', methods=['POST'])
def upload_file_user():
    files = {'upload_file': open('file.txt', 'rb')}

if __name__ == '__main__':
    app.run(debug=True)
