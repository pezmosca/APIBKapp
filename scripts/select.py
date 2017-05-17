import sqlite3, uuid, hashlib

conn = sqlite3.connect('users.bd')


user = "jey"
password = "11051996"
dircap = "URI:DIR2:ecvy2se477xprnlfnz3jc6u3qu:gf3vmd3staro7n2jfm7gzevschxeuytczsafwm32bja5pe27il7q"

def hashPassword(password):
    salt = uuid.uuid4().hex
    return str(hashlib.sha512(password + salt).hexdigest())

#conn.execute("INSERT INTO USERS (NICK, PASSWORD, DIRCAP) \
#    VALUES (?, ?, ?);", [str(user), hashPassword(password), str(dircap)]);

#conn.commit()

cursor = conn.execute("SELECT nick FROM USERS")
for cosa in cursor:
    for i in cosa:
        print(i)

print("OK")
conn.close()
