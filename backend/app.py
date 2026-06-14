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
    try:
        students = db.get_all_students()
        return jsonify(students), 200
    except Exception:
        return jsonify({"error": "Failed to fetch students"}), 404


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    # Getting the request body - replace with your implementation
    try:
        student_data = request.get_json(silent=True) or {}
        
        if not student_data or 'name' not in student_data or 'course' not in student_data:
            return jsonify({"error": "Missing required fields"}), 404
            
        name = student_data['name']
        course = student_data['course']
        mark = student_data.get('mark')
        
        if mark == "": 
            mark = None
        elif mark is not None: 
            mark = int(mark)
        
        new_student = db.insert_student(name, course, mark)
        return jsonify(new_student), 200
    except Exception:
        return jsonify({"error": "Bad Request"}), 404


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    # replace with your implementation
    try:
        data = request.get_json(silent=True) or {}
        name = data.get('name')
        course = data.get('course')
        mark = data.get('mark')
        
        if mark == "": 
            mark = None
        elif mark is not None: 
            mark = int(mark)
        
        updated_student = db.update_student(student_id, name=name, course=course, mark=mark)
        if not updated_student:
            return jsonify({"error": "Student not found"}), 404
            
        return jsonify(updated_student), 200
    except Exception:
        return jsonify({"error": "Bad Request"}), 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    # replace with your implementation
    try:
        result = db.delete_student(student_id)
        if not result:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(result), 200
    except Exception:
        return jsonify({"error": "Bad Request"}), 404


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    # replace with your implementation
    try:
        students = db.get_all_students()
        marks = [s['mark'] for s in students if s.get('mark') is not None]
        
        if not marks:
            return jsonify({"count": len(students), "average": None, "min": None, "max": None}), 200

        return jsonify({
            "count": len(students),
            "average": sum(marks) / len(marks),
            "min": min(marks),
            "max": max(marks)
        }), 200
    except Exception:
        return jsonify({"error": "Bad Request"}), 404


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)