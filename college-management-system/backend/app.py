from flask import Flask,jsonify,request
from database import get_connection

app = Flask(__name__)

@app.route("/students", methods=["GET"])
def get_students():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(students)

@app.route("/students", methods=["POST"])
def add_students():
    data = request.json

    db = get_connection()
    cursor = db.cursor()

    query = """INSERT INTO students
        (name, email, phone, department, year, section)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
    values = (
        data["name"],data["email"],
        data["phone"],data["department"],
        data["curr_year"],data["section"]
    )

    cursor.execute(query,values)
    db.commit()

    cursor.close()
    db.close()

    return jsonify({"message" : "Student added successfully"})

@app.route("/students/<int:id>",methods=["PUT"])
def update_student():
    data = request.json

    db = get_connection()
    cursor = db.cursor()

    query = """
        UPDATE students
        SET name=%s,email=%s,phone=%s,
        department=%s,year=%s,section=%s
        WHERE id=%s
    """
    values = (
        data["name"],data["email"],
        data["phone"],data["department"],
        data["year"],data["section"],id
    )

    cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close()

    return jsonify({"message": "Student updated successfully"})

@app.route("/students/<int:id>",methods=["DELETE"])
def delete_students():
    db = get_connection()
    cursor = db.cursor()
    
    cursor.execute(
        "DELETE FROM students WHERE id=%s",
        (id,)
    )
    db.commit()
    
    cursor.close()
    db.close()
    
    return jsonify({"message": "Student deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)