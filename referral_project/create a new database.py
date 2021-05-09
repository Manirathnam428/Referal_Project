import sqlite3

conn = sqlite3.connect('referaldb.db')
print("Opened database successfully")

conn.execute('CREATE TABLE reftable (name TEXT, email TEXT, pass TEXT,refcode TEXT, pin INT NOT NULL)')
print ("Table created successfully")
conn.close()
