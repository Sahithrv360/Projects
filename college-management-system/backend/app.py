from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_connection

app = Flask(__name__)
CORS(app)

# GET all students
@app.route("/students", methods=["GET"])
def get_students():

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(students)


# POST - Add student
@app.route("/students", methods=["POST"])
def add_student():

    data = request.json

    db = get_connection()
    cursor = db.cursor()

    query = """
        INSERT INTO students
        (name, email, phone, department, curr_year, section)
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
    })


# PUT - Update student
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.json

    db = get_connection()
    cursor = db.cursor()

    query = """
        UPDATE students
        SET name=%s,
            email=%s,
            phone=%s,
            department=%s,
            curr_year=%s,
            section=%s
        WHERE id=%s
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


# DELETE - Delete student
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=%s",
        (id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Student deleted successfully"
    })

@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM students WHERE id=%s",
        (id,)
    )

    student = cursor.fetchone()

    cursor.close()
    db.close()

    if student:
        return jsonify(student)

    return jsonify({"message": "Student not found"}), 404

@app.route("/faculty", methods=["GET"])
def get_faculty():

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM faculty")

    faculty = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(faculty)

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

@app.route("/faculty", methods=["POST"])
def add_faculty():

    data = request.json

    db = get_connection()
    cursor = db.cursor()

    query = """
        INSERT INTO faculty
        (name, email, phone, department, designation)
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
# Run Flask
if __name__ == "__main__":
    app.run(debug=True)