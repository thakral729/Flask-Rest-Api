import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

query = "select * from users"

result = cursor.execute(query)
for row in result :
    print(row)