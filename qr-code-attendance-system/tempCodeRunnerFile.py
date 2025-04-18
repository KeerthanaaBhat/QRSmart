from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from datetime import datetime
from pyzbar.pyzbar import decode  # Import decode from pyzbar
from PIL import Image  # Import Image from Pillow
import pymysql
import qrcode
import io
import mysql.connector
from mysql.connector import Error
from flask import Flask, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')


# Connection to the database
def get_db_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',  
                                 db='qr_attendance_db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection



@app.route('/')
def home():
    return render_template('login.html')  #  Open the login page

@app.route('/login', methods=['POST'])
def login():
    # Get username and password from form
    username = request.form['username']
    password = request.form['password']

    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Query the database for student information based on student_name
    query = "SELECT * FROM students WHERE student_name = %s"
    cursor.execute(query, (username,))
    student = cursor.fetchone()

    if student:  # If student exists with the provided name
        # Check if the password matches the student_id
        if str(student['student_id']) == password:  # Ensure password matches student_id
            session['student_id'] = student['student_id']
            session['student_name'] = student['student_name']
            return redirect(url_for('index1'))  # Redirect to student dashboard
        else:
            return "Invalid password for student.", 400  # Invalid password
    
    # Query the database for lecturer information based on lecturer_name
    lecturer_query = "SELECT * FROM lecturers WHERE lecturer_name = %s"
    cursor.execute(lecturer_query, (username,))
    lecturer = cursor.fetchone()

    if lecturer:  # If lecturer exists with the provided name
        # Check if the password matches the lecturer_id
        if str(lecturer['lecturer_id']) == password:  # Ensure password matches lecturer_id
            session['user_type'] = 'lecturer'
            session['lecturer_id'] = lecturer['lecturer_id'] 
            return redirect(url_for('index'))  # Redirect to lecturer dashboard
        else:
            return "Invalid password for lecturer.", 400  # Invalid password
    
    else:
        return "Invalid credentials. Please try again.", 400  # If no matching user or admin found
    

@app.route('/logout')
def logout():
    return render_template('login.html')


from flask import session, redirect, url_for

@app.route('/index', methods=['GET'])
def index():
    # Get the logged-in lecturer's details
    lecturer_name = session.get('lecturer_name')
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch timetable data
            if lecturer_name:
                # Fetch the timetable for the logged-in lecturer
                sql = """SELECT t.time_start, t.time_end, t.day_of_week, s.subject_name, sec.section_name, l.lecturer_name 
                        FROM timetable t 
                        JOIN subjects s ON t.subject_id = s.subject_id 
                        JOIN sections sec ON t.section_id = sec.section_id 
                        JOIN lecturers l ON t.lecturer_id = l.lecturer_id
                        WHERE l.lecturer_name = %s
                        ORDER BY sec.section_name, t.day_of_week, t.time_start"""
                cursor.execute(sql, (lecturer_name,))
            else:
                # Fetch timetable for all sections (when no specific lecturer is logged in)
                sql = """SELECT t.time_start, t.time_end, t.day_of_week, s.subject_name, sec.section_name, l.lecturer_name 
                        FROM timetable t 
                        JOIN subjects s ON t.subject_id = s.subject_id 
                        JOIN sections sec ON t.section_id = sec.section_id 
                        JOIN lecturers l ON t.lecturer_id = l.lecturer_id 
                        ORDER BY sec.section_name, t.day_of_week, t.time_start"""
                cursor.execute(sql)
            
            timetable_data = cursor.fetchall()

            # Fetch students data for each section
            students_query = """
            SELECT st.student_name, st.student_id, st.qr_code, sec.section_name
            FROM students st
            JOIN sections sec ON st.section_id = sec.section_id
            WHERE sec.section_name IN ('Sec A', 'Sec B', 'Sec C')
            ORDER BY sec.section_name, st.student_name
            """
            cursor.execute(students_query)
            students_data = cursor.fetchall()

            # Organize timetable into a dictionary by section and day
            timetable = {
                'Sec A': {},
                'Sec B': {},
                'Sec C': {}
            }
            time_slots = set()

            for entry in timetable_data:
                day = entry['day_of_week']
                time_slot = f"{entry['time_start']} - {entry['time_end']}"
                subject = entry['subject_name']
                section = entry['section_name']
                lecturer = entry['lecturer_name']

                time_slots.add(time_slot)

                if section not in timetable:
                    continue  # Ignore sections that are not A, B, or C

                if day not in timetable[section]:
                    timetable[section][day] = {}

                if time_slot not in timetable[section][day]:
                    timetable[section][day][time_slot] = []

                timetable[section][day][time_slot].append({
                    'subject': subject,
                    'lecturer': lecturer,
                    'section': section
                })

            # Custom sorting logic for time slots
            def custom_sort(time_slot):
                # Define a high number for time slots you want at the end
                if time_slot in ["2:00:00 - 3:00:00", "3:00:00 - 4:00:00"]:
                    return (99, time_slot)  # Place at the end
                else:
                    return (datetime.strptime(time_slot.split(' - ')[0], '%H:%M:%S').hour, time_slot)

            sorted_time_slots = sorted(time_slots, key=custom_sort)

            # Pass the data to the template, including sorted_time_slots and lecturer's name
            return render_template('index.html', timetable=timetable, time_slots=sorted_time_slots, students_data=students_data, lecturer_name=lecturer_name)
    finally:
        connection.close()

# ---------------Personalized Timetable ************************************8
@app.route('/timetable')
def timetable():
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    lecturer_id = session['lecturer_id']  # or dynamically fetch based on the logged-in user

    # Fetch the lecturer's name
    lecturer_query = "SELECT lecturer_name FROM lecturers WHERE lecturer_id = %s"
    cursor.execute(lecturer_query, (lecturer_id,))
    lecturer = cursor.fetchone()

    # Handle case where lecturer is not found
    if lecturer:
        lecturer_name = lecturer['lecturer_name']
    else:
        lecturer_name = "Lecturer"  # Fallback if no lecturer found

    query = """
    SELECT t.timetable_id, t.day_of_week, t.section_id, s.subject_name, t.time_start, t.time_end
    FROM timetable t
    JOIN subjects s ON t.subject_id = s.subject_id
    WHERE t.lecturer_id = %s
    """
    # Execute the query and fetch data
    cursor.execute(query, (lecturer_id,))
    rows = cursor.fetchall()

    # Convert the data into a dictionary format
    timetable_data = {}
    for row in rows:
        day = row['day_of_week']
        time_slot = f"{row['time_start']} - {row['time_end']}"
        subject = row['subject_name']
        section = row['section_id']

        # Organize timetable by day, then time slot
        if day not in timetable_data:
            timetable_data[day] = []
        timetable_data[day].append({
            'time_slot': time_slot,
            'subject': subject,
            'section': section
        })

    # Define the correct order of days
    days_of_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    # Sort the timetable data according to the order of days
    sorted_timetable_data = {day: timetable_data.get(day, []) for day in days_of_week_order}

    # Send the lecturer's name and sorted timetable data to the template
    return render_template('timetable.html', timetable_data=sorted_timetable_data, lecturer_name=lecturer_name)

@app.route('/dashboard')
def dashboard():
    # Get the lecturer_id from session
    lecturer_id = session.get('lecturer_id')

    if not lecturer_id:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch the lecturer's name using the lecturer_id from the session
    lecturer_query = "SELECT lecturer_name FROM lecturers WHERE lecturer_id = %s"
    cursor.execute(lecturer_query, (lecturer_id,))
    lecturer = cursor.fetchone()

    if lecturer:
        lecturer_name = lecturer['lecturer_name']
    else:
        lecturer_name = "Lecturer"  # Fallback if no lecturer found

    # Send lecturer_id to the frontend so it can filter data from localStorage
    return render_template('dashboard.html', lecturer_name=lecturer_name, lecturer_id=lecturer_id)

@app.route('/dashboard1')
def dashboard1():
    # Check if student is logged in
    student_id = session.get('student_id')

    if not student_id:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Get student's name from session
    student_name = session.get('student_name', 'Student')  # Fallback if no name found

    # Render the student dashboard template
    return render_template('dashboard1.html', student_name=student_name, student_id=student_id)


from flask import request, jsonify

@app.route('/mark_class', methods=['POST'])
def mark_class():
    connection = get_db_connection()
    cursor = connection.cursor()
    lecturer_name = request.form['lecturer_name']
    subject_name = request.form['subject_name']
    section = request.form['section']
    time_slot = request.form['time_slot']
    date = request.form['date']

    # You can now save this data to your database.
    # Example query to insert into the table:
    query = """
    INSERT INTO marked_classes (lecturer_name, subject_name, section, time_slot, date)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor = get_db_connection().cursor()
    cursor.execute(query, (lecturer_name, subject_name, section, time_slot, date))
    connection.commit()

    return jsonify({'status': 'success'})

@app.route('/table')
def table():
    return render_template('table.html')