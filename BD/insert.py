import sqlite3

conn = sqlite3.connect('test.bd')

conn.execute("INSERT INTO USERS (NICK, DIRCAP) \
	VALUES ('Pezmosca', 'URI:DIR2:w33clc45b4xxv65zdool2fy7hi:rr5ss6guvsxrzzjvtpoiqjfl57foisvcl2vj63s3ira57tk7iota');");

conn.commit()
print "OK"
conn.close()
