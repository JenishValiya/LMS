from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'ec439af9136e68d8671bc30a22f7a394'  # Replace with a real secret key

# MySQL connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL user
        password='23092004',  # Replace with your MySQL password
        database='LMS'  # Replace with your database name
    )
    return connection

# Home page for staff
@app.route('/staff_home')
def staff_home():
    if 'user' in session and session['user_type'] == 'staff':
        return render_template('staff_home.html', user=session['user'])
    return redirect(url_for('login'))

# Home page for students
@app.route('/student_home')
def student_home():
    if 'user' in session and session['user_type'] == 'student':
        return render_template('student_home.html', user=session['user'])
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s AND user_type = %s',
                       (username, password, user_type))
        user = cursor.fetchone()
        connection.close()

        if user:
            session['user'] = username
            session['user_type'] = user_type
            if user_type == 'staff':
                return redirect(url_for('staff_home'))
            elif user_type == 'student':
                return redirect(url_for('student_home'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template('login.html')

# Forgot password route
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Logic to handle password reset
        flash('Password reset link sent to your email')
        return redirect(url_for('login'))

    return render_template('forgot_password.html')

# Staff routes
@app.route('/staff_attendance', methods=['GET', 'POST'])
def staff_attendance():
    if 'user' in session and session['user_type'] == 'staff':
        if request.method == 'POST':
            attendance_data = request.form['attendance_data']
            # Logic to save attendance data to the database
            flash('Attendance saved successfully')
        return render_template('staff_attendance.html')
    return redirect(url_for('login'))

@app.route('/staff_classroom')
def staff_classroom():
    if 'user' in session and session['user_type'] == 'staff':
        return render_template('staff_classroom.html')
    return redirect(url_for('login'))

@app.route('/staff_timetable')
def staff_timetable():
    if 'user' in session and session['user_type'] == 'staff':
        # Fetch timetable data from the database
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM timetable WHERE username = %s', (session['user'],))
        timetable = cursor.fetchall()
        connection.close()
        return render_template('staff_timetable.html', user=session['user'], timetable=timetable)
    return redirect(url_for('login'))

@app.route('/staff_view_details')
def staff_view_details():
    if 'user' in session and session['user_type'] == 'staff':
        # Fetch staff details from the database
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM staff WHERE username = %s', (session['user'],))
        details = cursor.fetchone()
        connection.close()
        return render_template('staff_view_details.html', user=session['user'], details=details)
    return redirect(url_for('login'))

@app.route('/student_attendance')
def student_attendance():
    if 'user' in session and session['user_type'] == 'student':
        # Fetch student attendance from the database
        return render_template('student_attendance.html')
    return redirect(url_for('login'))

@app.route('/student_classroom')
def student_classroom():
    if 'user' in session and session['user_type'] == 'student':
        return render_template('student_classroom.html')
    return redirect(url_for('login'))

@app.route('/student_timetable')
def student_timetable():
    if 'user' in session and session['user_type'] == 'student':
        # Fetch timetable data for the student
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM timetable WHERE username = %s', (session['user'],))
        timetable = cursor.fetchall()
        connection.close()
        return render_template('student_timetable.html', user=session['user'], timetable=timetable)
    return redirect(url_for('login'))

@app.route('/student_view_details')
def student_view_details():
    if 'user' in session and session['user_type'] == 'student':
        # Fetch student details from the database
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM students WHERE username = %s', (session['user'],))
        details = cursor.fetchone()
        connection.close()
        return render_template('student_view_details.html', user=session['user'], details=details)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))

@app.route('/upload_materials', methods=['GET', 'POST'])
def upload_materials():
    if 'user' in session and session['user_type'] == 'staff':
        if request.method == 'POST':
            # Logic for uploading materials
            flash('Materials uploaded successfully')
            return redirect(url_for('staff_home'))
        return render_template('upload_materials.html')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
