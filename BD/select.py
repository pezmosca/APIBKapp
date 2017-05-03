import sqlite3

conn = sqlite3.connect('test.bd')

user = "pezmosca"
cursor = conn.execute("SELECT dircap FROM USERS WHERE nick =?", [str(user)])

#cursor = conn.execute("SELECT nick, dircap from USERS")
#for row in cursor:
#    print row[0]
#    print row[1]

print "OK"
conn.close()
