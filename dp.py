import pymysql

db = pymysql.connect(host="localhost", user="root", password="alstjr!!98", charset="utf8")
cursor = db.cursor()

cursor.execute('USE hufs_apply;')

# cursor.execute('INSERT INTO user_info (user_mail, user_name, user_password, user_major, user_GPA) Values ("kurooru@hufs.ac.kr", "양민석","alstjr!!98", NULL, NULL)')

# value = cursor.execute('SELECT * from users;')
# value = cursor.fetchall()
# print(value[0]["name"])

# cursor.execute('UPDATE users SET GPA=4.5 WHERE name="양민석"')
# value = cursor.execute('SELECT * from users;')
# value = cursor.fetchall()
# print(value[0]['GPA'])

# cursor.execute('DELETE FROM users WHERE name="양민석"')
# value = cursor.execute('SELECT * from users;')
# value = cursor.fetchall()
# print(value)

# db 끄기
db.commit()
db.close()