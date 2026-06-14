from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    # TODO: replace with your implementation. This is a mock response
    students = db.get_all_students()
    return jsonify(students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    data = request.json

    if not data or 'name' not in data or 'course' not in data:
        return jsonify({"error": "Missing required fields: name and course"}), 404

    # Getting the request body - replace with your implementation
    student_data = request.json
    name = data["name"]
    course = data["course"]
    mark = data.get("mark", 0)  # Default mark to 0 if

    new_student = db.insert_student(name, course, mark)
    return jsonify(new_student), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    pass  # replace with your implementation
    data = request.json
    name = data.get("name")
    course = data.get("course")
    mark = data.get("mark")

    updated_student = db.update_student(student_id, name=name, course=course, mark=mark)

    if not updated_student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(updated_student), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    result = db.delete_student(student_id)
    if not result:
        return jsonify({"error": "Student not found"}), 404
    
    return jsonify(result), 200



@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()

    marks = [student["mark"] for student in students if student["mark"] is not None]

    if not marks:
        return jsonify({
            "count": len(students),
            "average": None,
            "min": None,
            "max": None
        }), 200
    
    return jsonify({
        "count": len(students),
        "average": sum(marks) / len(marks),
        "min": min(marks),
        "max": max(marks)
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
