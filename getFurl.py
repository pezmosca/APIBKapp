import requests

######################################
##### FALTA PONER LA IP CORRECTA #####
######################################

url = 'http://127.0.0.1:5000'
response = requests.get(url+'/api/gestion').text

fo = open("introducer.furl", "wb")
fo.write(str(response))
fo.close()
