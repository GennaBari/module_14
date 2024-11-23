import sqlite3



def initiate_db():
    connection = sqlite3.connect('products2.db')
    cursor = connection.cursor()
    #cursor.execute('DELETE FROM Products') # очищаем таблицу от предыдущих записей
    # создаём таблицу и заполняем её данными
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    for i in range(1, 5):
        cursor.execute(
                'INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
            (f'Продукт {i}', f'Описание {i}', i * 100))


    cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users(email)")
    connection.commit()
    connection.close()

def add_user(username, email, age):
    connection = sqlite3.connect('products2.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f'{username}', f'{email}', f'{age}', 1000))

    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('products2.db')
    cursor = connection.cursor()
    check_user = cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if check_user.fetchone():
        return True
    else:
        return False

def get_all_products():
    connection = sqlite3.connect('products2.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, title, description, price FROM Products')
    db = cursor.fetchall()

    connection.commit()
    connection.close()
    return list(db)

initiate_db()
add_user('newuser', 'email@com', '28')
print (is_included('newuser'))
get_all_products()