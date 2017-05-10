import requests

fo = open("introducer.furl", "r")
furl = fo.read()
furl = str(furl).split("\n")[0]
fo.close()
r = requests.post('http://127.0.0.1:5000/api/gestion', data = {'furl':furl})
print r.text
