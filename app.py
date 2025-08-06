from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'mysecret'

# Create database & users table if not exists
def init_db():
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
init_db()

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/home')
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('users.db') as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM users WHERE username=?', (username,))
            if cur.fetchone():
                return "User already exists!"
            cur.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, password))
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('users.db') as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
            if cur.fetchone():
                session['username'] = username
                return redirect('/home')
            else:
                return "Invalid credentials!"
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect('/login')
    result = None
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operation = request.form['operation']
        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                result = "Cannot divide by zero!"
            else:
                result = num1 / num2
    return render_template('home.html', username=session['username'], result=result)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
