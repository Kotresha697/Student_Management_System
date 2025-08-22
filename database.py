import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user='root',
    password='Suma@2005',
    database='student'
)

cursor = conn.cursor()

# Drop tables in correct order to avoid FK conflicts
cursor.execute("DROP TABLE IF EXISTS Enrollment")
cursor.execute("DROP TABLE IF EXISTS StudentForm")
cursor.execute("DROP TABLE IF EXISTS Courses")
cursor.execute("DROP TABLE IF EXISTS Loginform")

# Create StudentForm table (no spaces in column names)
cursor.execute("""
CREATE TABLE IF NOT EXISTS StudentForm (
    StudentUSN VARCHAR(50) NOT NULL UNIQUE PRIMARY KEY,
    StudentName VARCHAR(50) NOT NULL,
    Section VARCHAR(10) NOT NULL,
    Branch VARCHAR(50) NOT NULL,
    Semester INT NOT NULL,
    DateOfBirth DATE NOT NULL
)
""")

# Create Courses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Courses (
    CourseID INT AUTO_INCREMENT PRIMARY KEY,
    CourseName VARCHAR(100) NOT NULL,
    Credits INT NOT NULL
)
""")

# Create Enrollment table (FKs use consistent column names)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Enrollment (
    EnrollmentID INT AUTO_INCREMENT PRIMARY KEY,
    StudentUSN VARCHAR(50) NOT NULL,
    CourseID INT NOT NULL,
    EnrollmentDate DATE NOT NULL,
    FOREIGN KEY (StudentUSN) REFERENCES StudentForm(StudentUSN) ON DELETE CASCADE,
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID) ON DELETE CASCADE
)
""")

# Create Loginform table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Loginform (
    Username VARCHAR(50) NOT NULL PRIMARY KEY,
    Password VARCHAR(255) NOT NULL
)
""")
cursor.execute("""
INSERT INTO Courses (CourseName, Credits)
VALUES ('Operating Systems', 4)
""")

conn.commit()
conn.close()
