import requests
url = 'http://192.168.1.6:3456'

files = {'file': open('user.json','rb')}
#r = requests.put(url + '/uri/URI%3ADIR2%3A5ve74zzi3rqr5arqn5wj5helfm%3Advwnbm4hv2cww42xqnbkhj4vbhpwmiord2bkmsv2kkmscxhledyq/file.txt', files=files, data=values)
#r = requests.post(url + '/uri/URI%3ADIR2%3Aw33clc45b4xxv65zdool2fy7hi%3Arr5ss6guvsxrzzjvtpoiqjfl57foisvcl2vj63s3ira57tk7iota?t=upload', files=files)
#r = requests.post("http://127.0.0.1:5000/api/Pezmosca/upload_file", files=files)
#r = requests.post(url + '/uri/URI%3ADIR2%3A5ve74zzi3rqr5arqn5wj5helfm%3Advwnbm4hv2cww42xqnbkhj4vbhpwmiord2bkmsv2kkmscxhledyq?t=mkdir&name=cosas')
r = requests.post(url + '/uri?t=mkdir&name=cosas')

print(r.text)
