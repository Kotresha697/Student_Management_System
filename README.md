# Student Management System

A web-based **Student Management System** built using **Python, Flask, MySQL, SQL, Pandas, and Docker** to manage student information, attendance, academic records, and generate structured reports.

The project demonstrates practical implementation of **Python backend development, relational database management, SQL, CRUD operations, data analysis, and containerization**.

## Features

- Student registration and management
- Add, view, update, and delete student records
- Manage student attendance
- Manage academic marks and grades
- Search and filter student records
- Relational database using MySQL
- SQL-based CRUD operations
- SQL joins and data retrieval
- Data analysis using Pandas
- Generate Excel-based student reports
- REST-style Flask backend
- Docker-based application setup
- Structured and normalized database design

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Database | MySQL |
| Database Language | SQL |
| Data Analysis | Pandas |
| Report Generation | OpenPyXL / Excel |
| Containerization | Docker |
| Development Environment | VS Code |
| Version Control | Git & GitHub |

## System Architecture

```text
                    +----------------------+
                    |       User           |
                    |   Web Interface      |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |       Flask          |
                    |    Web Application   |
                    +----------+-----------+
                               |
                +--------------+--------------+
                |                             |
                v                             v
       +----------------+            +------------------+
       |   Application  |            |      Pandas      |
       |     Logic      |            |  Data Analysis   |
       +--------+-------+            +--------+---------+
                |                             |
                v                             v
       +----------------+            +------------------+
       |      MySQL     |            | Excel Reports    |
       |    Database    |            |     (.xlsx)      |
       +----------------+            +------------------+
```

## Project Structure

```text
Student_Management_System/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
│
├── templates/
│   ├── index.html
│   ├── add_student.html
│   ├── update_student.html
│   ├── attendance.html
│   └── marks.html
│
├── static/
│   ├── css/
│   └── js/
│
├── database/
│   └── schema.sql
│
├── reports/
│   └── student_report.xlsx
│
└── data/
    └── student_data.csv
```

## Database Design

The system uses **MySQL** as the relational database.

The database is designed around student information, attendance, and academic records.

### Student Table

Stores the basic information of each student.

```sql
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    department VARCHAR(100),
    semester INT
);
```

### Attendance Table

Stores attendance information for students.

```sql
CREATE TABLE attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    total_classes INT,
    attended_classes INT,
    attendance_percentage DECIMAL(5,2),
    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
);
```

### Marks Table

Stores academic performance.

```sql
CREATE TABLE marks (
    mark_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    subject VARCHAR(100),
    marks DECIMAL(5,2),
    grade VARCHAR(5),
    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
);
```

## Database Relationships

```text
Students
   |
   | 1
   |
   |--------< Attendance
   |
   | 1
   |
   |--------< Marks
```

Each student can have multiple attendance records and multiple subject-wise marks.

Foreign keys are used to maintain **referential integrity** between related tables.

## Core Functionalities

### 1. Student Management

Users can:

- Add new students
- View student details
- Update student information
- Delete student records
- Search for students
- Filter students based on department or semester

These operations implement the basic **CRUD** functionality:

```text
Create
Read
Update
Delete
```

### 2. Attendance Management

The system stores:

- Total classes
- Attended classes
- Attendance percentage

Attendance percentage can be calculated as:

```text
Attendance Percentage =
(Attended Classes / Total Classes) × 100
```

This allows administrators to quickly identify students with low attendance.

### 3. Academic Management

The system maintains subject-wise marks and grades.

Example:

```text
Student: Rahul

Subject              Marks
---------------------------
DBMS                  85
Machine Learning      90
Computer Networks     78
Data Structures       88
```

The stored academic information can be queried and analyzed using SQL and Pandas.

### 4. Search and Filtering

Students can be searched or filtered using attributes such as:

- Student ID
- Student name
- Department
- Semester
- Subject

Example SQL query:

```sql
SELECT *
FROM students
WHERE department = 'Information Science';
```

## SQL Operations

The project demonstrates practical SQL concepts including:

### Insert

```sql
INSERT INTO students
(name, email, phone, department, semester)
VALUES
('Rahul Kumar',
 'rahul@example.com',
 '9876543210',
 'Information Science',
 7);
```

### Select

```sql
SELECT *
FROM students;
```

### Update

```sql
UPDATE students
SET semester = 8
WHERE student_id = 1;
```

### Delete

```sql
DELETE FROM students
WHERE student_id = 1;
```

### Join

Student information can be combined with academic records using SQL joins.

```sql
SELECT
    s.student_id,
    s.name,
    s.department,
    m.subject,
    m.marks
FROM students s
JOIN marks m
ON s.student_id = m.student_id;
```

## Data Analysis

The project uses **Pandas** for analyzing student records and generating reports.

Example analysis tasks include:

- Average marks
- Highest marks
- Lowest marks
- Attendance analysis
- Student performance analysis
- Subject-wise performance
- Department-wise statistics

Example:

```python
import pandas as pd

df = pd.read_csv("student_data.csv")

average_marks = df["marks"].mean()

print("Average Marks:", average_marks)
```

## Excel Report Generation

Student information can be exported into structured Excel reports.

Example report:

| Student ID | Name | Department | Subject | Marks | Attendance |
|---|---|---|---|---:|---:|
| 101 | Rahul | ISE | DBMS | 85 | 92% |
| 102 | Priya | ISE | ML | 90 | 88% |
| 103 | Arun | CSE | CN | 78 | 81% |

Reports can be used by faculty or administrators for academic analysis.

## Flask Backend

Flask acts as the application backend and handles:

- HTTP requests
- Routing
- Form submission
- Database operations
- Student management logic
- Report generation

Typical application routes include:

```text
/
```

Displays the main dashboard.

```text
/add_student
```

Adds a new student.

```text
/students
```

Displays student records.

```text
/update/<student_id>
```

Updates an existing student.

```text
/delete/<student_id>
```

Deletes a student.

```text
/attendance
```

Manages attendance records.

```text
/marks
```

Manages academic marks.

## Installation

### Prerequisites

Install the following:

- Python 3.x
- MySQL
- Git
- Docker (optional)

### Clone the Repository

```bash
git clone https://github.com/Kotresha697/Student_Management_System.git
```

Navigate to the project:

```bash
cd Student_Management_System
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Database Configuration

Create a MySQL database:

```sql
CREATE DATABASE student_management;
```

Select the database:

```sql
USE student_management;
```

Execute the database schema:

```bash
mysql -u root -p student_management < database/schema.sql
```

Update the database configuration in the Flask application according to your MySQL credentials.

Example:

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "student_management"
```

## Running the Application

Start the Flask application:

```bash
python app.py
```

The application will run locally.

```text
http://127.0.0.1:5000
```

Open the URL in a web browser.

## Running with Docker

The project can also be containerized using Docker.

Build the application:

```bash
docker build -t student-management-system .
```

Run the container:

```bash
docker run -p 5000:5000 student-management-system
```

If using Docker Compose:

```bash
docker-compose up --build
```

This allows the application and database environment to be managed consistently.

## Example Workflow

```text
1. Administrator opens the application
                ↓
2. Adds student information
                ↓
3. Student record is stored in MySQL
                ↓
4. Attendance and marks are recorded
                ↓
5. SQL queries retrieve required information
                ↓
6. Pandas analyzes student data
                ↓
7. Excel report is generated
```

## Key Concepts Demonstrated

This project demonstrates practical knowledge of:

- Python Programming
- Flask
- REST API concepts
- SQL
- MySQL
- Relational Database Management Systems
- Database Design
- Normalization
- Primary Keys
- Foreign Keys
- CRUD Operations
- SQL Joins
- Data Filtering
- Data Aggregation
- Pandas
- Data Analysis
- Excel Report Generation
- Docker
- Git and GitHub

## Future Enhancements

Possible improvements include:

- User authentication and role-based access
- Admin and faculty dashboards
- Student login
- Advanced data visualization
- Automated email notifications
- Attendance alerts
- Machine Learning-based student performance prediction
- REST API documentation using Swagger
- Cloud deployment
- PostgreSQL support
- React-based frontend
- Automated testing using PyTest

## Learning Outcomes

Through this project, the following practical skills were developed:

- Designing and working with relational databases
- Writing and optimizing SQL queries
- Building backend applications using Flask
- Performing data preprocessing and analysis using Pandas
- Working with structured academic datasets
- Generating automated reports
- Understanding database relationships and normalization
- Containerizing applications using Docker
- Integrating multiple technologies into a complete application

## Author

**Kotresha DK**

B.E. Information Science & Engineering  
Bangalore Institute of Technology, Bangalore

GitHub:  
https://github.com/Kotresha697

LinkedIn:  
https://www.linkedin.com/in/kotresha-dk/

## License

This project is intended for educational and demonstration purposes.
