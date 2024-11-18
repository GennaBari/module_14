import sqlite3


connection = sqlite3.connect("not_telegram.db ")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER 
)
''')

#cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")

for i in range(1,11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                      (f'User{i + 1}', f'example{i}@gmail.com', f'{i * 10}', 1000))

for i in range(1,11,2):
    cursor.execute("UPDATE Users SET balance = ? WHERE username = ?", (500, f"User{i}"))

for i in range(1,11,3):
    cursor.execute("DELETE FROM Users WHERE username = ?", (f"User{i}",))

cursor.execute("SELECT username, email, age, balance FROM Users WHERE AGE != 60")

users = cursor.fetchall()
for user in users:
    username, email, age, balance = user
    #print(f'Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}')
    print(f'Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')
    #print(f'Имя: {user[1]} | Почта: {user[2]} | Возраст: {user[3]} | Баланс: {user[4]}')

connection.commit()
connection.close()
