from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)  # <-- This line links SQLAlchemy to your app


app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kbt_id = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


    def __repr__(self):
        return f'<User {self.kbt_id}>'

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        kbt_id = request.form['kbt_id']
        password = request.form['password']

        user = User.query.filter_by(kbt_id=kbt_id, role=role).first()
        if user and check_password_hash(user.password, password):
            flash('Login successful!', 'success')
            if role == 'student':
                return redirect('/student/dashboard')
            else:
                return redirect('/tpo/dashboard')
        else:
            flash('Invalid credentials!', 'error')
            return redirect('/login')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        role = request.form['role']
        kbt_id = request.form['kbt_id']
        password = request.form['password']

        existing_user = User.query.filter_by(kbt_id=kbt_id).first()
        if existing_user:
            flash('KBT ID already exists. Please log in.', 'error')
            return redirect('/login')

        hashed_password = generate_password_hash(password)
        new_user = User(kbt_id=kbt_id, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.')
        return redirect('/login')

    return render_template('signup.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Handle password recovery logic here
        flash('Recovery link sent!')
        return redirect('/login')
    return render_template('forgot_password.html')

# Dummy dashboards
@app.route('/student/dashboard')
def student_dashboard():
    return "<h2>Welcome to the Student Dashboard!</h2>"

@app.route('/tpo/dashboard')
def tpo_dashboard():
    return "<h2>Welcome to the T&P Officer Dashboard!</h2>"

@app.route('/form/mba')
def mba_form():
    return render_template('mba.html')

@app.route('/form/ms')
def ms_form():
    return render_template('ms.html')

@app.route('/form/job')
def job_form():
    return render_template('job.html')

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3  # or use your DB connection method

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session handling

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please login first", "warning")
        return redirect(url_for('login'))
    return render_template('dashboard.html')


if __name__ == '__main__':
    db.create_all()  # <-- Make sure this comes AFTER your models
    app.run(debug=True)
