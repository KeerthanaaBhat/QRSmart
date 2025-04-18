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

@app.route('/index1')
def index1():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch timetable data
            sql = """SELECT t.time_start, t.time_end, t.day_of_week, s.subject_name, sec.section_name, l.lecturer_name 
                    FROM timetable t 
                    JOIN subjects s ON t.subject_id = s.subject_id 
                    JOIN sections sec ON t.section_id = sec.section_id 
                    JOIN lecturers l ON t.lecturer_id = l.lecturer_id 
                    ORDER BY sec.section_name, t.day_of_week, t.time_start"""

            cursor.execute(sql)
            timetable_data = cursor.fetchall()

            # Fetch students data for each section including QR code
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

            # Custom sorting logic
            def custom_sort(time_slot):
                # Define a high number for time slots you want at the end
                if time_slot in ["2:00:00 - 3:00:00", "3:00:00 - 4:00:00"]:
                    return (99, time_slot)  # Place at the end
                else:
                    # Parse and return hour for normal sorting
                    return (datetime.strptime(time_slot.split(' - ')[0], '%H:%M:%S').hour, time_slot)

            sorted_time_slots = sorted(time_slots, key=custom_sort)

            # Pass the data to the template, including sorted_time_slots
            return render_template('index1.html', timetable=timetable, time_slots=sorted_time_slots, students_data=students_data)
    finally:
        connection.close()


# --------------------------TIMETABLE-------------------------------------#

# Retrieves timetable data from a database
def fetch_timetable():
    timetable = {}
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Fetch timetable data; modify query based on your database structure
        cursor.execute("SELECT section_name, day, time_slot, subject FROM timetable")  
        
        for row in cursor.fetchall():
            section_name = row['section_name']
            day = row['day']
            time_slot = row['time_slot']
            subject = row['subject']

            if section_name not in timetable:
                timetable[section_name] = {}
            if day not in timetable[section_name]:
                timetable[section_name][day] = {}
            if time_slot not in timetable[section_name][day]:
                timetable[section_name][day][time_slot] = []
                
            timetable[section_name][day][time_slot].append({'subject': subject, 'section': section_name})

    finally:
        conn.close()
    return timetable

# Update Timetable - handle form submissions to update data
@app.route('/update_timetable', methods=['POST'])
def update_timetable():
    try:
        # Get data from the form
        section_id = request.form['section_id']
        day_of_week = request.form['day_of_week']
        time_start = request.form['time_start']
        time_end = request.form['time_end']
        subject_id = request.form['subject_id']
        lecturer_id = request.form['lecturer_id'] 
        
        # Update timetable in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE timetable
            SET subject_id = %s, lecturer_id = %s
            WHERE section_id = %s AND day_of_week = %s AND time_start = %s AND time_end = %s
        """, (subject_id, lecturer_id, section_id, day_of_week, time_start, time_end))

        conn.commit()  # Save changes to the database
        return redirect(url_for('index'))  # Redirect back to the timetable page
    except Exception as e:
        print(f"Failed to update timetable: {e}")
        return f"Failed to update timetable: {e}"

# Edit timetable
@app.route('/edit-timetable', methods=['POST'])
def edit_timetable():
    timetable_id = request.form.get('timetable_id')
    lecturer_id = request.form.get('lecturer_id')
    day_of_week = request.form.get('day_of_week')
    section_id = request.form.get('section_id')
    subject_id = request.form.get('subject_id')
    time_start = request.form.get('time_start')
    time_end = request.form.get('time_end')

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """UPDATE timetable SET lecturer_id = %s, day_of_week = %s, section_id = %s, 
                     subject_id = %s, time_start = %s, time_end = %s WHERE timetable_id = %s"""
            cursor.execute(sql, (lecturer_id, day_of_week, section_id, subject_id, time_start, time_end, timetable_id))
            connection.commit()
            return redirect(url_for('index'))
    finally:
        connection.close()

# Delete a timetable entry
@app.route('/delete-timetable/<timetable_id>')
def delete_timetable(timetable_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM timetable WHERE timetable_id = %s"
            cursor.execute(sql, (timetable_id,))
            connection.commit()
            return redirect(url_for('index'))
    finally:
        connection.close()

# Subject details inside timetable subject
@app.route('/subject_details')
def subject_details():
    subject = request.args.get('subject')
    day = request.args.get('day')
    section = request.args.get('section')

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Get lecturer details, subject name, and time for the lecture
            lecturer_query = """
            SELECT l.lecturer_id, l.lecturer_name, s.subject_name, t.time_start, t.time_end
            FROM timetable t
            JOIN lecturers l ON t.lecturer_id = l.lecturer_id
            JOIN subjects s ON t.subject_id = s.subject_id
            WHERE s.subject_name = %s AND t.day_of_week = %s AND t.section_id = (
                SELECT section_id FROM sections WHERE section_name = %s
            )
            """
            cursor.execute(lecturer_query, (subject, day, section))
            lecturer_info = cursor.fetchone()

            # Get students for the section with their IDs, names, and section names
            students_query = """
            SELECT st.student_id, st.student_name, sec.section_name
            FROM students st
            JOIN sections sec ON st.section_id = sec.section_id
            WHERE sec.section_name = %s
            """
            cursor.execute(students_query, (section,))
            students = cursor.fetchall()

        return render_template('subject_details.html', subject=subject, day=day, section=section, lecturer_info=lecturer_info, students=students)
    finally:
        connection.close()

# Student details inside timetable subject
def fetch_students():
    students_data = []
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Fetch student data; modify query based on your database structure
        cursor.execute("SELECT student_id, student_name, section_name FROM students")
        
        for row in cursor.fetchall():
            students_data.append({
                'student_id': row['student_id'],
                'student_name': row['student_name'],
                'section_name': row['section_name']
            })

    finally:
        conn.close()
    return students_data

# Function to map subjects to colors
# <div style="background-color: {{ subject | subject_color }}">
#    {{ subject }}
# </div>
@app.template_filter('subject_color')
def get_subject_color(subject):
    color_mapping = {
    'AIML': '#C39898',  # Light Pink
    'DBMS': '#6EC5D1',  # Light Blue
    'DSA': '#78ABA8',   # Light Green
    'OOP': '#D8D2C2',   # Light Orange
    'GO': '#667BC6',    # Light Gray
    'NLP': '#9B86BD',   # Light Yellow
}
    return color_mapping.get(subject, '#ffffff')  # Default to white if subject not found


#---------------------------------------STUDENT DATA-------------------------------------------------

@app.route('/section_a')
def section_a():
    students_data = get_students_for_section('Sec A')
    return render_template('section_a.html', students_data=students_data)

@app.route('/section_b')
def section_b():
    students_data = get_students_for_section('Sec B')
    return render_template('section_b.html', students_data=students_data)

@app.route('/section_c')
def section_c():
    students_data = get_students_for_section('Sec C')
    return render_template('section_c.html', students_data=students_data)

# Function to fetch student data based on section
def get_students_for_section(section_name):
    students_data = []
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Fetch student data and join with sections table to get section_name
        cursor.execute("""
            SELECT st.student_id, st.student_name, sec.section_name 
            FROM students st
            JOIN sections sec ON st.section_id = sec.section_id 
            WHERE sec.section_name = %s
        """, (section_name,))
        
        for row in cursor.fetchall():
            students_data.append({
                'student_id': row['student_id'],
                'student_name': row['student_name'],
                'section_name': row['section_name']
            })
    finally:
        conn.close()

    return students_data

#generate QRCODE in STUDENT DATA
@app.route('/generate_qr/<student_id>')
def generate_qr(student_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch the student's QR code from the database
            cursor.execute("SELECT qr_code FROM students WHERE student_id = %s", (student_id,))
            result = cursor.fetchone()

            # Check if a result is found
            if result is None:
                return "QR code not found", 404
            
            qr_code = result['qr_code']

            # Generate the QR code
            #A QR code is created using the qrcode library and stored in the variable qr_img.
            qr_img = qrcode.make(qr_code) #Uses the qrcode library to generate a QR code image from the qr_code value
            img_byte_array = io.BytesIO()  #Python module, allows you to work with binary data (like images), it is used to store the QR code image data in memory 
            qr_img.save(img_byte_array, format='PNG') #Pillow (PIL) library,  It saves the qr_img (the QR code image created by the qrcode library) into the img_byte_array
            #Instead of saving the QR code to a file like qr_code.png on disk, the image is written directly into the img_byte_array memory buffer. 
            img_byte_array.seek(0)
            #seek(0) moves the file pointer back to the beginning of the byte stream. This is important because after writing the image data, the pointer is at the end of the stream, and attempting to read from it would return an empty result.

            return send_file(img_byte_array, mimetype='image/png')
    finally:
        connection.close()

# Delete student record
@app.route('/delete_student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Execute delete query
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            connection.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        connection.close()

# edit_student() is for displaying the current student data in a form for editing.
# GET Retrieve data from the server.
@app.route('/edit_student/<student_id>')
def edit_student(student_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT student_id, student_name FROM students WHERE student_id = %s", (student_id,))
            student = cursor.fetchone()
        return render_template('edit_student.html', student=student)
    finally:
        connection.close()

# update_student() is for updating the student’s data in the database based on the edited values submitted via a POST request.
#POST Send data to the server to create or update resources.
@app.route('/update_student', methods=['POST'])
def update_student():
    old_student_id = request.form['old_student_id']  # Existing student ID
    new_student_id = request.form['student_id']  # New student ID
    student_name = request.form['student_name']  # New student name

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE students 
                SET student_id = %s, student_name = %s 
                WHERE student_id = %s
            """, (new_student_id, student_name, old_student_id))
            connection.commit()
        return redirect(url_for('section_a'))
    finally:
        connection.close()

# Add student form
@app.route('/add_student', methods=['GET'])
def show_add_student_form():
    return render_template('add_student.html')

# Handle the form submission for adding a new student
@app.route('/add_student', methods=['POST'])
def add_student():
    student_id = request.form['student_id']
    student_name = request.form['student_name']
    section_id = request.form['section_id']
    qr_code = request.form['qr_code']  # Get the QR code input
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Insert the student data into the database
            cursor.execute("""
                INSERT INTO students (student_id, student_name, section_id, qr_code)
                VALUES (%s, %s, %s, %s)
            """, (student_id, student_name, section_id, qr_code))
            connection.commit()
        
        # Generate a QR code for the student (optional if qr_code is just a string identifier)
        qr_img = qrcode.make(qr_code)
        img_byte_array = io.BytesIO()
        qr_img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        
        # Redirect back to the index page after successfully adding the student
        return redirect(url_for('index'))
    finally:
        connection.close()




# GET data from server 
@app.route('/get_subject_details', methods=['GET'])
def get_subject_details():
    #request.args is an object in Flask that allows you to access query parameters from the URL of a GET request.
    subject = request.args.get('subject')
    day = request.args.get('day')
    section = request.args.get('section')
    print(f"Received: Subject={subject}, Day={day}, Section={section}")  # Debugging line
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Get the lecturer for the subject
            lecturer_query = """
            SELECT l.lecturer_name, l.lecturer_id FROM timetable t
            JOIN lecturers l ON t.lecturer_id = l.lecturer_id
            JOIN subjects s ON t.subject_id = s.subject_id
            WHERE s.subject_name = %s AND t.day_of_week = %s AND t.section_id = (
                SELECT section_id FROM sections WHERE section_name = %s
            )
            """
            cursor.execute(lecturer_query, (subject, day, section))
            lecturer = cursor.fetchone()
            lecturer_name = lecturer['lecturer_name'] if lecturer else 'Not found'
            lecturer_id = lecturer['lecturer_id'] if lecturer else 'Not found'

            # Get students for the section along with their IDs
            students_query = """
            SELECT student_name, student_id, section_id FROM students
            WHERE section_id = (SELECT section_id FROM sections WHERE section_name = %s)
            """
            cursor.execute(students_query, (section,))
            students = cursor.fetchall()  # Get all relevant fields

        return jsonify({
            'lecturer': lecturer_name,
            'lecturer_id': lecturer_id,
            'students': [{'name': student['student_name'], 
                          'id': student['student_id'], 
                          'section': section} for student in students]
        })
    finally:
        connection.close()

#----------------------------------Upload qr code-----------------------------------------------------------------

# Route to serve the student page
@app.route('/student')
def student_page():
    return render_template('student.html')  # Serve the student.html page

@app.route('/student1')
def student1():
    return render_template('student1.html')

@app.route('/status1')
def status1():
    return render_template('status1.html')

# Route to handle QR code scan and fetch student details
@app.route('/upload_qr_image', methods=['POST'])
def upload_qr_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    img = Image.open(io.BytesIO(file.read()))
    #Image.open(io.BytesIO(file.read())) reads the file content and opens it as an image using the Pillow library. 
    # The image data is wrapped in a BytesIO object, which allows it to be treated as a file-like object.
    decoded_objects = decode(img)
    #decode(img) uses a QR code decoding library (likely pyzbar or a similar library) to decode the QR code in the uploaded image.

    if not decoded_objects:
        return jsonify({"error": "No QR code found"}), 400

    student_id = decoded_objects[0].data.decode('utf-8')

    # Fetch student details based on student_id from the database
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT student_id, student_name, section_id FROM students WHERE student_id = %s"
            cursor.execute(sql, (student_id,))
            student_info = cursor.fetchone()
    finally:
        connection.close()

    if not student_info:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "student_id": student_info['student_id'],
        "name": student_info['student_name'],
        "section": student_info['section_id']
    })

# Route to get the subject and lecturer based on time slot
@app.route('/get_subject_for_time/<time_slot>', methods=['GET'])
def get_subject_for_time(time_slot):
    section_id = request.args.get('section')  # Student's section
    day_of_week = request.args.get('day')  # Get the selected day

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # SQL query to get subject and lecturer details based on time slot and day
        cursor.execute(''' 
            SELECT s.subject_name, l.lecturer_name 
            FROM timetable t
            JOIN subjects s ON t.subject_id = s.subject_id
            JOIN lecturers l ON t.lecturer_id = l.lecturer_id
            WHERE t.section_id = %s AND t.day_of_week = %s AND (t.time_start <= %s AND t.time_end > %s)
        ''', (section_id, day_of_week, time_slot, time_slot))

        subject_info = cursor.fetchone()
        print("Subject Info:", subject_info)  # Debug line to see what is returned
    finally:
        cursor.close()
        conn.close()

    if subject_info:
        return jsonify({"subject": subject_info['subject_name'], "lecturer": subject_info['lecturer_name']})

    return jsonify({"error": "No subject found for this time slot and day"}), 404


#------------------------QR SCANNING-----------------------------------------

@app.route('/qr')
def qr():
    return render_template('qr.html')

@app.route('/qr1')
def qr1():
    return render_template('qr1.html')



@app.route('/attendance1')
def attendance1():
    return render_template('attendance1.html')

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')


@app.route('/status')
def attendance_page():
    return render_template('status.html')

@app.route('/get_attendance')
def get_attendance():
    subject = request.args.get("subject")
    section = request.args.get("section")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT attendance_id, student_id, student_name, section_id, subject_name, time_slot, attendance_date, status
        FROM attendance
        WHERE subject_name = %s AND section = %s
    """, (subject, section))
    
    rows = cursor.fetchall()
    conn.close()

    return jsonify(rows)



@app.route('/get_student_data/<qr_code>', methods=['GET'])
def get_student_data(qr_code):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # SQL query to fetch student data
            sql = "SELECT student_id, student_name, section_id FROM students WHERE student_id = %s"
            cursor.execute(sql, (qr_code,))
            student = cursor.fetchone()

            if student:
                # Return student data as a JSON response
                return jsonify({
                    'student_id': student['student_id'],
                    'name': student['student_name'],
                    'section': student['section_id']
                })
            else:
                return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        print(f"Error fetching student data: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)





# Route to handle QR code scan and fetch student details
@app.route('/get_student_details/<student_id>', methods=['GET'])
def get_student_details(student_id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
    conn.close()
    
    if student:
        return jsonify({"name": student['name'], "section": student['section_id']})
    return jsonify({"error": "Student not found"}), 404





@app.route('/submit', methods=['POST'])
def submit():
    if 'qr_code' not in request.files:
        return "No file part"
    
    file = request.files['qr_code']
    if file.filename == '':
        return "No selected file"

    # Process the uploaded file (e.g., save it, decode the QR code, etc.)
    # You can call your QR code decoding function here.

    time_selected = request.form['time']  # This should now work correctly
    print("Time Selected:", time_selected)  # Debugging line

    # Process the selected time as needed

    # Redirect or render another template after processing
    return redirect(url_for('student_page'))

