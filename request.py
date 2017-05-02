import requests
url = 'http://192.168.1.6:3456'

files = {'file': open('file2.txt','rb')}
#r = requests.put(url + '/uri/URI%3ADIR2%3A5ve74zzi3rqr5arqn5wj5helfm%3Advwnbm4hv2cww42xqnbkhj4vbhpwmiord2bkmsv2kkmscxhledyq/file.txt', files=files, data=values)
#r = requests.post(url + '/uri/URI%3ADIR2%3A5ve74zzi3rqr5arqn5wj5helfm%3Advwnbm4hv2cww42xqnbkhj4vbhpwmiord2bkmsv2kkmscxhledyq?t=upload', files=files)
r = requests.post(url + '/uri/URI%3ADIR2%3A5ve74zzi3rqr5arqn5wj5helfm%3Advwnbm4hv2cww42xqnbkhj4vbhpwmiord2bkmsv2kkmscxhledyq?t=mkdir&name=Toni')

print r.text
