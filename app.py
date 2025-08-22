import mysql.connector
from flask import session, Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from flask import send_file
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

from flask import redirect, url_for
from werkzeug.security import generate_password_hash
import mysql.connector

@app.route('/')
def home():
    conn = mysql.connector.connect(
        host="localhost",
        user='root',
        password='Suma@2005',
        database='student'
    )
    cursor = conn.cursor()

    # Check if Loginform table exists
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = 'student' AND table_name = 'Loginform'
    """)
    login_table_exists = cursor.fetchone()[0] == 1

    # Create Loginform table if it doesn't exist
    if not login_table_exists:
        cursor.execute("""
            CREATE TABLE Loginform (
                Username VARCHAR(50) PRIMARY KEY,
                Password VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()

    # Insert default admin account if Loginform is empty
    cursor.execute("SELECT COUNT(*) FROM Loginform")
    if cursor.fetchone()[0] == 0:
        hashed_pw = generate_password_hash('password')
        cursor.execute("INSERT INTO Loginform (Username, Password) VALUES (%s, %s)", ('admin', hashed_pw))
        conn.commit()

    cursor.close()
    conn.close()

    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    conn = mysql.connector.connect(
        host="localhost",
        user='root',
        password='Suma@2005',
        database='student'
    )
    cursor = conn.cursor()
    message = None

    # Check if the Courses table exists
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = 'student' AND table_name = 'Courses'
    """)
    table_exists = cursor.fetchone()[0] == 1

    # Create the Courses table if it doesn't exist
    if not table_exists:
        try:
            cursor.execute("""
                CREATE TABLE Courses (
                    CourseID INT AUTO_INCREMENT PRIMARY KEY,
                    CourseName VARCHAR(100) NOT NULL,
                    Credits INT NOT NULL
                )
            """)
            conn.commit()
        except mysql.connector.Error as err:
            conn.close()
            return render_template('add_course.html', message=[f"Failed to create Courses table: {err}"])

    if request.method == 'POST':
        course_name = request.form.get('CourseName')
        credits = request.form.get('Credits')

        try:
            # Since CourseID is auto_increment, only check by CourseName
            cursor.execute("SELECT * FROM Courses WHERE CourseName = %s", (course_name,))
            existing_course = cursor.fetchone()

            if existing_course:
                message = ["Course already exists!"]
            else:
                cursor.execute("""
                    INSERT INTO Courses (CourseName, Credits)
                    VALUES (%s, %s)
                """, (course_name, credits))
                conn.commit()
                message = ["Course added successfully!"]
        except mysql.connector.Error as err:
            message = [f"Database Error: {err}"]

    cursor.close()
    conn.close()
    return render_template('add_course.html', message=message)

@app.route('/view_courses')
def view_courses():
    conn = mysql.connector.connect(
        host="localhost",
        user='root',
        password='Suma@2005',
        database='student'
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Courses")
    courses = cursor.fetchall()
    column = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()
    return render_template('view_courses.html', courses=courses, column=column)

@app.route('/enroll_student', methods=['GET', 'POST'])
def enroll_student():
    conn = mysql.connector.connect(
        host="localhost",
        user='root',
        password='Suma@2005',
        database='student'
    )
    cursor = conn.cursor()

    # Get students and courses for dropdown
    cursor.execute("SELECT StudentUSN, StudentName FROM StudentForm")
    students = cursor.fetchall()

    cursor.execute("SELECT CourseID, CourseName FROM Courses")
    courses = cursor.fetchall()

    message = None

    if request.method == 'POST':
        student_usn = request.form.get('student_usn')
        course_id = request.form.get('course_id')
        enroll_date = datetime.today().strftime('%Y-%m-%d')

        # Check if already enrolled
        cursor.execute("SELECT * FROM Enrollment WHERE StudentUSN = %s AND CourseID = %s", (student_usn, course_id))
        if cursor.fetchone():
            message = ["Student is already enrolled in this course."]
        else:
            cursor.execute("""
                INSERT INTO Enrollment (StudentUSN, CourseID, EnrollmentDate)
                VALUES (%s, %s, %s)
            """, (student_usn, course_id, enroll_date))
            conn.commit()
            message = ["Enrollment successful!"]

    cursor.close()
    conn.close()
    return render_template('enroll_student.html', students=students, courses=courses, message=message)
@app.route('/download_enrollments_excel')
#@login_required
def download_enrollments_excel():
    conn = mysql.connector.connect(
        host="localhost",
        user='root',
        password='Suma@2005',
        database='student'
    )
    cursor = conn.cursor()

    # Check if Enrollment table exists
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = 'student' AND table_name = 'Enrollment'
    """)
    table_exists = cursor.fetchone()[0] == 1

    if not table_exists:
        
        cursor.close()
        conn.close()
        flash("Table 'Enrollment' does not exist. Cannot download data.", "error")
        return redirect(url_for('enroll_student'))

    try:
        # Query enrollment data with student name and course name joined
        query = """
            SELECT e.StudentUSN, s.StudentName, e.CourseID, c.CourseName, e.EnrollmentDate
            FROM Enrollment e
            JOIN StudentForm s ON e.StudentUSN = s.StudentUSN
            JOIN Courses c ON e.CourseID = c.CourseID
        """
        df = pd.read_sql(query, conn)
    except Exception as e:
        cursor.close()
        conn.close()
        flash(f"Error reading data: {str(e)}", "error")
        return redirect(url_for('enroll_student'))

    cursor.close()
    conn.close()

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Enrollments')

    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        download_name='enrolled_students.xlsx',
        as_attachment=True
    )

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'logged_in' not in session:  
            flash("You must be logged in to view this page!", "error")
            return redirect(url_for('login'))  
        return f(*args, **kwargs)
    return wrapper

@app.route('/add_student', methods=['GET', 'POST'])
#@login_required
def add_student():
    message = []
    column = []

    # Establish DB connection
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user='root',
            password='Suma@2005',
            database='student'
        )
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'student' AND table_name = 'StudentForm'
        """)
        table_exists = cursor.fetchone()[0] == 1

        # Create table if not exists
        if not table_exists:
            cursor.execute("""
                CREATE TABLE StudentForm (
                    StudentUSN VARCHAR(50) PRIMARY KEY,
                    StudentName VARCHAR(50),
                    Section VARCHAR(10),
                    Branch VARCHAR(50),
                    Semester INT,
                    DateOfBirth DATE
                )
            """)
            conn.commit()
            message.append("Table 'StudentForm' created successfully.")

        # Describe table for rendering
        cursor.execute("DESCRIBE StudentForm")
        column = cursor.fetchall()

        if request.method == 'POST':
            # Get data from form
            usn = request.form.get('StudentUSN', '').strip()
            name = request.form.get('StudentName', '').strip()
            section = request.form.get('Section', '').strip()
            branch = request.form.get('Branch', '').strip()
            semester = request.form.get('Semester', '').strip()
            dob = request.form.get('DateOfBirth', '').strip()

            # Validate input
            if not all([usn, name, section, branch, dob, semester]):
                message.append("All fields are required.")
            elif not semester.isdigit() or int(semester) not in range(1, 9):
                message.append("Please select a valid semester.")
            else:
                try:
                    semester = int(semester)
                    # Check for existing USN
                    cursor.execute("SELECT * FROM StudentForm WHERE StudentUSN = %s", (usn,))
                    if cursor.fetchone():
                        message.append("Student already entered!")
                    else:
                        # Insert new student
                        cursor.execute("""
                            INSERT INTO StudentForm (StudentUSN, StudentName, Section, Branch, Semester, DateOfBirth)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (usn, name, section, branch, semester, dob))
                        conn.commit()
                        flash("Student added successfully!", "success")
                        return redirect(url_for('add_student'))  # Redirect after POST
                except mysql.connector.Error as err:
                    message.append(f"Database Error: {err}")

    except mysql.connector.Error as conn_err:
        message.append(f"Connection Error: {conn_err}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    return render_template('add_student.html', column=column, message=message)

@app.route('/view_students', methods=['GET'])
#@login_required
def view_students():
    conn = mysql.connector.connect(
        host="localhost",
        user='root',
        password='Suma@2005',
        database='student'
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables 
        WHERE table_schema = 'student' AND table_name = 'StudentForm'
    """)
    table_exists = cursor.fetchone()[0] == 1

    if not table_exists:
        cursor.close()
        conn.close()
        return render_template('view_student.html', students=[], column=[], message=["Table 'StudentForm' does not exist."])

    cursor.execute("SELECT * FROM StudentForm")
    students = cursor.fetchall()
    column = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()
    return render_template('view_student.html', students=students, column=column)

@app.route('/download_students_excel')
@login_required
def download_students_excel():
    conn = mysql.connector.connect(
        host="localhost",
        user='root',
        password='Suma@2005',
        database='student'
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) 
        FROM information_schema.tables 
        WHERE table_schema = 'student' AND table_name = 'StudentForm'
    """)
    table_exists = cursor.fetchone()[0] == 1

    if not table_exists:
        cursor.close()
        conn.close()
        flash("Table 'StudentForm' does not exist. Cannot download data.", "error")
        return redirect(url_for('view_students'))

    try:
        query = "SELECT * FROM StudentForm"
        df = pd.read_sql(query, conn)
    except Exception as e:
        cursor.close()
        conn.close()
        flash(f"Error reading data: {str(e)}", "error")
        return redirect(url_for('view_students'))

    cursor.close()
    conn.close()

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Students')

    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        download_name='student_data.xlsx',
        as_attachment=True
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Suma@2005",
            database="student"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT Password FROM Loginform WHERE Username=%s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            stored_hashed_password = result[0]
            if check_password_hash(stored_hashed_password, password):
                session['logged_in'] = True
                session['username'] = username
                flash("Login successful!", "success")
                return redirect(url_for('home'))  # 👈 Redirect to home page
            else:
                flash("Incorrect password!", "error")
        else:
            flash("Username not found!", "error")

    return render_template('home.html')

@app.route('/view_enrollments')
#@login_required
def view_enrollments():
    conn = mysql.connector.connect(
        host="localhost",
        user='root',
        password='Suma@2005',
        database='student'
    )
    cursor = conn.cursor()

    # Check if Enrollment table exists
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = 'student' AND table_name = 'Enrollment'
    """)
    table_exists = cursor.fetchone()[0] == 1

    if not table_exists:
        cursor.close()
        conn.close()
        flash("Table 'Enrollment' does not exist.", "error")
        return redirect(url_for('enroll_student'))

    # Join Enrollment with StudentForm and Courses to get full info
    query = """
        SELECT e.StudentUSN, s.StudentName, e.CourseID, c.CourseName, e.EnrollmentDate
        FROM Enrollment e
        JOIN StudentForm s ON e.StudentUSN = s.StudentUSN
        JOIN Courses c ON e.CourseID = c.CourseID
        ORDER BY e.EnrollmentDate DESC
    """
    cursor.execute(query)
    enrollments = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    return render_template('view_enrollments.html', enrollments=enrollments, columns=columns)




if __name__ == '__main__':
    app.run(debug=True, port=5050)