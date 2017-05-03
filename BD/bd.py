import sqlite3

conn = sqlite3.connect('test.bd')

conn.execute('''CREATE TABLE USERS
	(NICK CHAR(50) PRIMARY KEY NOT NULL,
	DIRCAP BLOB NOT NULL);''')
print "OK"

conn.close()
