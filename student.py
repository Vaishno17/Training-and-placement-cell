from flask import Blueprint, render_template, session, redirect, url_for

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('auth.login'))
    
    student_info = {
        'id': session['user_id'],
        'name': "Student Name",
        'branch': "Computer Engineering",
        'cgpa': 8.5
    }
    
    return render_template('student/dashboard.html', student=student_info)