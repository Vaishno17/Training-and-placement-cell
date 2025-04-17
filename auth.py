from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# Mock database (replace with real database in production)
users = {
    'student': {
        'kbt123': generate_password_hash('student123'),
        'role': 'student'
    },
    'tpo': {
        'tpo123': generate_password_hash('tpo123'),
        'role': 'tpo'
    }
}

students_data = {
    'kbt123': {
        'name': 'John Doe',
        'birthdate': '2000-01-01',
        'tenth_marks': 85,
        'twelfth_marks': 78,
        'gender': 'Male',
        'backlogs': 0,
        'certifications': ['Python Certification', 'AWS Fundamentals'],
        'achievements': ['Hackathon Winner 2023']
    }
}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if role in users and username in users[role]:
            if check_password_hash(users[role][username], password):
                session['user_id'] = username
                session['role'] = role
                if role == 'student':
                    return redirect(url_for('student.dashboard'))
                else:
                    return redirect(url_for('tpo.dashboard'))
            else:
                flash('Invalid credentials', 'error')
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))