from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        kbt_id = request.form['kbt_id']
        password = request.form['password']

        # Fake login logic (replace with DB check later)
        if kbt_id == '123' and password == 'pass':
            if role == 'student':
                return redirect('/student/dashboard')
            else:
                return redirect('/tpo/dashboard')
        else:
            flash('Invalid credentials!')
            return redirect('/login')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Save user to DB
        flash('Account created successfully!')
        return redirect('/login')
    return render_template('signup.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Password recovery logic
        flash('Recovery link sent!')
        return redirect('/login')
    return render_template('forgot_password.html')

# Dummy dashboard routes
@app.route('/student/dashboard')
def student_dashboard():
    return "<h2>Welcome to the Student Dashboard!</h2>"

@app.route('/tpo/dashboard')
def tpo_dashboard():
    return "<h2>Welcome to the T&P Officer Dashboard!</h2>"

if __name__ == '__main__':
    app.run(debug=True)
