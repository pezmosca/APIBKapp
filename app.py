#!flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

URL_CLIENT_TAHOE = 'http://192.168.1.6:3456'
import requests

@app.route('/api/user/files', methods=['GET'])
def get_files_user():
    return requests.get(URL_CLIENT_TAHOE+'/uri/URI%3ADIR2%3A5ve74zzi3rqr5arqn5wj5helfm%3Advwnbm4hv2cww42xqnbkhj4vbhpwmiord2bkmsv2kkmscxhledyq?t=json').text
@app.route('/api/user/file', methods=['GET'])
def get_file_user():
    return requests.get(URL_CLIENT_TAHOE+'/uri/URI%3ADIR2%3A5ve74zzi3rqr5arqn5wj5helfm%3Advwnbm4hv2cww42xqnbkhj4vbhpwmiord2bkmsv2kkmscxhledyq/foto.jpg').text

@app.route('/api/user/upload_file', methods=['POST'])
def upload_file_user():
    files = {'upload_file': open('file.txt', 'rb')}

if __name__ == '__main__':
    app.run(debug=True)
