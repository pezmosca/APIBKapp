
import requests, sys

######################################
##### FALTA PONER LA IP CORRECTA #####
######################################

if len(sys.argv) < 2:
    print "Usage: ./setFurl.py <path-where-introducer.furl-is>"
else:
    url = 'http://192.168.5.241:5000'
    path = sys.argv[1]
    fo = open(path + "/private/introducer.furl", "r")
    furl = fo.read()
    furl = str(furl).split("\n")[0]
    fo.close()
    r = requests.post(url+'/api/gestion', data = {'furl':furl})
    print r.text
