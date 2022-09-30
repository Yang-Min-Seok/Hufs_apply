import pymysql

db = pymysql.connect(host="localhost", user="root", password="alstjr!!98", charset="utf8")
cursor = db.cursor(pymysql.cursors.DictCursor)

cursor.execute('USE hufs_apply;')

# insert
# cursor.execute('INSERT INTO users (id, name, password, GPA) Values ("201802144", "양민석","alstjr!!98", NULL)')

# select
# value = cursor.execute('SELECT * from users;')
# value = cursor.fetchall()
# print(value[0]["name"])

# update
# cursor.execute('UPDATE users SET GPA=4.5 WHERE name="양민석"')
# value = cursor.execute('SELECT * from users;')
# value = cursor.fetchall()
# print(value[0]['GPA'])

# delete
# cursor.execute('DELETE FROM users WHERE name="양민석"')
# value = cursor.execute('SELECT * from users;')
# value = cursor.fetchall()
# print(value)

db.commit()
db.close()