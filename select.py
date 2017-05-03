import sqlite3

conn = sqlite3.connect('users.bd')

user = "Pezmosca"
cursor = conn.execute("SELECT dircap FROM USERS WHERE nick =?", [str(user)])
print cursor.fetchone()[0]

print "OK"
conn.close()
