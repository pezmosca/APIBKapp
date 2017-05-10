import sqlite3

conn = sqlite3.connect('users.bd')

conn.execute('''CREATE TABLE USERS
	(NICK CHAR(50) PRIMARY KEY NOT NULL,
	PASSWORD CHAR(50) NOT NULL,
	DIRCAP BLOB NOT NULL);''')

conn.execute('''CREATE TABLE GESTION (FURL BLOB PRIMARY KEY NOT NULL);''')

conn.execute("INSERT INTO USERS (NICK, PASSWORD, DIRCAP) \
	VALUES ('Pezmosca', 'HELLO', 'URI:DIR2:w33clc45b4xxv65zdool2fy7hi:rr5ss6guvsxrzzjvtpoiqjfl57foisvcl2vj63s3ira57tk7iota');");

conn.commit()

print("OK")

conn.close()
