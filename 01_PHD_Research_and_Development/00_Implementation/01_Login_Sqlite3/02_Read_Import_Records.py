import sqlite3

conn = sqlite3.connect("db\\users.db")
cursor = conn.cursor()

cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",
               ("itsaswin","Aswin@1234"))

cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",
               ("admin","1234"))

cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",
               ("student","student123"))

conn.commit()
conn.close()

print("Records Inserted")