from flask import Flask, jsonify, request
from flask_cors import CORS

from database import get_connection


app = Flask(__name__)

CORS(app)


# ============================================================
#                         STUDENTS
# ============================================================


# ================= GET ALL STUDENTS =================

@app.route("/students", methods=["GET"])
def get_students():

    db = get_connection()

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM students"
    )

    students = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(students)


# ================= GET ONE STUDENT =================

@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):

    db = get_connection()

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM students WHERE id = %s",
        (id,)
    )

    student = cursor.fetchone()

    cursor.close()
    db.close()

    if student:

        return jsonify(student)

    return jsonify({
        "message": "Student not found"
    }), 404


# ================= ADD STUDENT =================

@app.route("/students", methods=["POST"])
def add_student():

    data = request.json

    db = get_connection()

    cursor = db.cursor()

    query = """
        INSERT INTO students
        (
            name,
            email,
            phone,
            department,
            curr_year,
            section
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        data["name"],
        data["email"],
        data["phone"],
        data["department"],
        data["curr_year"],
        data["section"]
    )

    cursor.execute(query, values)

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Student added successfully"
    }), 201


# ================= UPDATE STUDENT =================

@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.json

    db = get_connection()

    cursor = db.cursor()

    query = """
        UPDATE students
        SET
            name = %s,
            email = %s,
            phone = %s,
            department = %s,
            curr_year = %s,
            section = %s
        WHERE id = %s
    """

    values = (
        data["name"],
        data["email"],
        data["phone"],
        data["department"],
        data["curr_year"],
        data["section"],
        id
    )

    cursor.execute(query, values)

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Student updated successfully"
    })


# ================= DELETE STUDENT =================

@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    db = get_connection()

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Student deleted successfully"
    })


# ============================================================
#                          FACULTY
# ============================================================


# ================= GET ALL FACULTY =================

@app.route("/faculty", methods=["GET"])
def get_faculty():

    db = get_connection()

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM faculty"
    )

    faculty = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(faculty)


# ================= GET ONE FACULTY =================

@app.route("/faculty/<int:id>", methods=["GET"])
def get_one_faculty(id):

    db = get_connection()

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM faculty WHERE id = %s",
        (id,)
    )

    faculty = cursor.fetchone()

    cursor.close()
    db.close()

    if faculty:

        return jsonify(faculty)

    return jsonify({
        "message": "Faculty not found"
    }), 404


# ================= ADD FACULTY =================

@app.route("/faculty", methods=["POST"])
def add_faculty():

    data = request.json

    db = get_connection()

    cursor = db.cursor()

    query = """
        INSERT INTO faculty
        (
            name,
            email,
            phone,
            department,
            designation
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        data["name"],
        data["email"],
        data["phone"],
        data["department"],
        data["designation"]
    )

    cursor.execute(query, values)

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Faculty added successfully"
    }), 201


# ================= UPDATE FACULTY =================

@app.route("/faculty/<int:id>", methods=["PUT"])
def update_faculty(id):

    data = request.json

    db = get_connection()

    cursor = db.cursor()

    query = """
        UPDATE faculty
        SET
            name = %s,
            email = %s,
            phone = %s,
            department = %s,
            designation = %s
        WHERE id = %s
    """

    values = (
        data["name"],
        data["email"],
        data["phone"],
        data["department"],
        data["designation"],
        id
    )

    cursor.execute(query, values)

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Faculty updated successfully"
    })


# ================= DELETE FACULTY =================

@app.route("/faculty/<int:id>", methods=["DELETE"])
def delete_faculty(id):

    db = get_connection()

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM faculty WHERE id = %s",
        (id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Faculty deleted successfully"
    })


# ============================================================
#                          COURSES
# ============================================================


# ================= GET ALL COURSES =================

@app.route("/courses", methods=["GET"])
def get_courses():

    db = get_connection()

    cursor = db.cursor(dictionary=True)

    query = """
        SELECT
            courses.id,
            courses.course_code,
            courses.course_name,
            courses.department,
            courses.credits,
            courses.faculty_id,
            faculty.name AS faculty_name
        FROM courses
        LEFT JOIN faculty
            ON courses.faculty_id = faculty.id
    """

    cursor.execute(query)

    courses = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(courses)


# ================= GET ONE COURSE =================

@app.route("/courses/<int:id>", methods=["GET"])
def get_course(id):

    db = get_connection()

    cursor = db.cursor(dictionary=True)

    query = """
        SELECT
            courses.id,
            courses.course_code,
            courses.course_name,
            courses.department,
            courses.credits,
            courses.faculty_id,
            faculty.name AS faculty_name
        FROM courses
        LEFT JOIN faculty
            ON courses.faculty_id = faculty.id
        WHERE courses.id = %s
    """

    cursor.execute(query, (id,))

    course = cursor.fetchone()

    cursor.close()
    db.close()

    if course:

        return jsonify(course)

    return jsonify({
        "message": "Course not found"
    }), 404


# ================= ADD COURSE =================

@app.route("/courses", methods=["POST"])
def add_course():

    data = request.json

    db = get_connection()

    cursor = db.cursor()

    query = """
        INSERT INTO courses
        (
            course_code,
            course_name,
            department,
            credits,
            faculty_id
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        data["course_code"],
        data["course_name"],
        data["department"],
        data["credits"],
        data["faculty_id"]
    )

    cursor.execute(query, values)

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Course added successfully"
    }), 201


# ================= UPDATE COURSE =================

@app.route("/courses/<int:id>", methods=["PUT"])
def update_course(id):

    data = request.json

    db = get_connection()

    cursor = db.cursor()

    query = """
        UPDATE courses
        SET
            course_code = %s,
            course_name = %s,
            department = %s,
            credits = %s,
            faculty_id = %s
        WHERE id = %s
    """

    values = (
        data["course_code"],
        data["course_name"],
        data["department"],
        data["credits"],
        data["faculty_id"],
        id
    )

    cursor.execute(query, values)

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Course updated successfully"
    })


# ================= DELETE COURSE =================

@app.route("/courses/<int:id>", methods=["DELETE"])
def delete_course(id):

    db = get_connection()

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM courses WHERE id = %s",
        (id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Course deleted successfully"
    })

# ============================================================
#                       ATTENDANCE
# ============================================================


# ================= GET ALL ATTENDANCE =================

@app.route("/attendance", methods=["GET"])
def get_attendance():

    db = get_connection()

    cursor = db.cursor(dictionary=True)

    query = """
        SELECT
            attendance.id,
            attendance.student_id,
            attendance.course_id,
            attendance.attendance_date,
            attendance.status,

            students.name AS student_name,

            courses.course_code,
            courses.course_name

        FROM attendance

        JOIN students
            ON attendance.student_id = students.id

        JOIN courses
            ON attendance.course_id = courses.id

        ORDER BY attendance.attendance_date DESC
    """

    cursor.execute(query)

    attendance = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(attendance)


# ================= GET ONE ATTENDANCE =================

@app.route("/attendance/<int:id>", methods=["GET"])
def get_one_attendance(id):

    db = get_connection()

    cursor = db.cursor(dictionary=True)

    query = """
        SELECT
            attendance.id,
            attendance.student_id,
            attendance.course_id,
            attendance.attendance_date,
            attendance.status,

            students.name AS student_name,

            courses.course_code,
            courses.course_name

        FROM attendance

        JOIN students
            ON attendance.student_id = students.id

        JOIN courses
            ON attendance.course_id = courses.id

        WHERE attendance.id = %s
    """

    cursor.execute(query, (id,))

    record = cursor.fetchone()

    cursor.close()
    db.close()

    if record:

        return jsonify(record)

    return jsonify({
        "message": "Attendance record not found"
    }), 404


# ================= ADD ATTENDANCE =================

@app.route("/attendance", methods=["POST"])
def add_attendance():

    data = request.json

    db = get_connection()

    cursor = db.cursor()

    query = """
        INSERT INTO attendance
        (
            student_id,
            course_id,
            attendance_date,
            status
        )
        VALUES (%s, %s, %s, %s)
    """

    values = (
        data["student_id"],
        data["course_id"],
        data["attendance_date"],
        data["status"]
    )

    cursor.execute(query, values)

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Attendance added successfully"
    }), 201


# ================= UPDATE ATTENDANCE =================

@app.route("/attendance/<int:id>", methods=["PUT"])
def update_attendance(id):

    data = request.json

    db = get_connection()

    cursor = db.cursor()

    query = """
        UPDATE attendance

        SET
            student_id = %s,
            course_id = %s,
            attendance_date = %s,
            status = %s

        WHERE id = %s
    """

    values = (
        data["student_id"],
        data["course_id"],
        data["attendance_date"],
        data["status"],
        id
    )

    cursor.execute(query, values)

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Attendance updated successfully"
    })


# ================= DELETE ATTENDANCE =================

@app.route("/attendance/<int:id>", methods=["DELETE"])
def delete_attendance(id):

    db = get_connection()

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM attendance WHERE id = %s",
        (id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Attendance deleted successfully"
    })
# ============================================================
#                         RUN SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )