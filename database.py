import sqlite3

# Create a new SQLite database
conn = sqlite3.connect('library.db')
c = conn.cursor()

# Create the users table
c.execute('''CREATE TABLE IF NOT EXISTS users
                (user_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE)''')

# Create the books table
c.execute('''CREATE TABLE IF NOT EXISTS books
                (book_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(user_id))''')

conn.commit()
conn.close()
