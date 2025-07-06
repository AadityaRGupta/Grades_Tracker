from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = "grades.db"

# Create DB table if it doesn't exist
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                grade REAL NOT NULL
            );
        ''')

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        students = conn.execute("SELECT * FROM students").fetchall()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    course = request.form['course']
    grade = float(request.form['grade'])

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO students (name, course, grade) VALUES (?, ?, ?)", (name, course, grade))
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
