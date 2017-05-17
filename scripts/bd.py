import sqlite3

conn = sqlite3.connect('users.bd')

conn.execute('''CREATE TABLE USERS
	(NICK CHAR(50) PRIMARY KEY NOT NULL,
	SALT BLOB NOT NULL,
	PASSWORD BLOB NOT NULL,
	DIRCAP BLOB NOT NULL);''')

conn.execute('''CREATE TABLE GESTION (FURL BLOB PRIMARY KEY NOT NULL);''')

conn.execute("INSERT INTO GESTION (FURL) VALUES ('hello')");

conn.commit()

print("OK")

conn.close()
