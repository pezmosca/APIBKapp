import requests

######################################
##### FALTA PONER LA IP CORRECTA #####
######################################

url = 'http://192.168.5.241:5000'
response = requests.get(url+'/api/gestion').text
#print (response)

fo = open("introducer.furl", "w")
fo.write(response)
fo.close()
