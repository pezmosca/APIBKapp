import json
from pprint import pprint

with open('files.json') as outfile:
    data = json.load(outfile)

print data['dirnode']
