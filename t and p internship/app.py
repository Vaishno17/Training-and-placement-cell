from flask import session, redirect, url_for

app.secret_key = 'supersecretkey'  # Required for session handling

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        kbt_id = request.form['kbt_id']
        password = request.form['password']

        if role == 'student' and kbt_id == 'student123' and password == 'pass':
            session['user'] = 'student'
            return redirect(url_for('student_dashboard'))
        elif role == 'tp' and kbt_id == 'tp123' and password == 'pass':
            session['user'] = 'tp'
            return redirect(url_for('tp_dashboard'))
        else:
            return "Invalid Credentials"

    return render_template('login.html')

# Dashboards
@app.route('/student_dashboard')
def student_dashboard():
    if session.get('user') != 'student':
        return redirect(url_for('login'))
    return render_template('student_form.html')

@app.route('/tp_dashboard')
def tp_dashboard():
    if session.get('user') != 'tp':
        return redirect(url_for('login'))
    # Load data for filtering UI
    return render_template('tpo_dashboard.html')
