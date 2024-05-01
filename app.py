from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

# Routes
@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', users=users,books=books)

# Add/Edit User
@app.route('/user', methods=['GET', 'POST'])
def user():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if 'user_id' in request.form:
            user_id = request.form['user_id']
            conn.execute('UPDATE users SET name = ?, email = ? WHERE user_id = ?', (name, email, user_id))
        else:
            conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    user_id = request.args.get('user_id')
    if user_id:
        user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
        conn.close()
        return render_template('user.html', user=user)
    conn.close()
    return render_template('user.html')

# Add/Edit Book
@app.route('/book', methods=['GET', 'POST'])
def book():
    conn = get_db_connection()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        user_id = request.form['user_id']
        
        if 'book_id' in request.form:
            book_id = request.form['book_id']
            conn.execute('UPDATE books SET title = ?, author = ?, user_id = ? WHERE book_id = ?', (title, author, user_id, book_id))
        else:
            conn.execute('INSERT INTO books (title, author, user_id) VALUES (?, ?, ?)', (title, author, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    book_id = request.args.get('book_id')
    users = conn.execute('SELECT * FROM users').fetchall()
    if book_id:
        book = conn.execute('SELECT * FROM books WHERE book_id = ?', (book_id,)).fetchone()
        conn.close()
        return render_template('book.html', book=book, users=users)
    conn.close()
    return render_template('book.html', users=users)


# Delete User
@app.route('/delete_user', methods=['POST'])
def delete_user():
    conn = get_db_connection()
    user_id = request.form['user_id']
    conn.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


# Delete Book
@app.route('/delete_book', methods=['POST'])
def delete_book():
    conn = get_db_connection()
    book_id = request.form['book_id']
    conn.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Search/Filter/Sort Books
@app.route('/search', methods=['GET', 'POST'])
def search():
    conn = get_db_connection()
    if request.method == 'POST':
        search_query = request.form['search_query']
        sort_by = request.form['sort_by']
        if search_query:
            books = conn.execute('SELECT b.book_id, b.title, b.author, u.name FROM books b JOIN users u ON b.user_id = u.user_id WHERE b.title LIKE ? OR b.author LIKE ? OR u.name LIKE ? ORDER BY ? ASC', ('%'+search_query+'%', '%'+search_query+'%', '%'+search_query+'%', sort_by)).fetchall()
        else:
            books = conn.execute('SELECT b.book_id, b.title, b.author, u.name FROM books b JOIN users u ON b.user_id = u.user_id ORDER BY ? ASC', (sort_by,)).fetchall()
    else:
        books = conn.execute('SELECT b.book_id, b.title, b.author, u.name FROM books b JOIN users u ON b.user_id = u.user_id').fetchall()
    conn.close()
    return render_template('search.html', books=books)

# Summary Reports
@app.route('/reports')
def reports():
    conn = get_db_connection()
    user_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    book_count = conn.execute('SELECT COUNT(*) FROM books').fetchone()[0]
    # top_authors = conn.execute('SELECT author, COUNT(*) AS book_count FROM books GROUP BY author ORDER BY book_count DESC LIMIT 6').fetchall()
    top_authors = conn.execute('SELECT author, COUNT(*) AS book_count FROM books GROUP BY author ORDER BY book_count DESC').fetchall()
    conn.close()
    return render_template('reports.html', user_count=user_count, book_count=book_count, top_authors=top_authors)

# @app.route('/reports')
# def reports():
#     conn = get_db_connection()
#     user_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
#     book_count = conn.execute('SELECT COUNT(*) FROM books').fetchone()[0]
#     top_authors = conn.execute('SELECT author, COUNT(*) AS book_count FROM books GROUP BY author ORDER BY book_count DESC LIMIT 3').fetchall()
#     conn.close()
#     return render_template('reports.html', user_count=user_count, book_count=book_count, top_authors=top_authors)







if __name__ == '__main__':
    app.run(debug=True,port=7000)
