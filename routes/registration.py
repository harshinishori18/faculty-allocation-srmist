from flask import Blueprint, request, jsonify
from config import db
from models.faculty import Faculty

registration_bp = Blueprint('registration', __name__)

# ADD a faculty
@registration_bp.route('/faculty/add', methods=['POST'])
def add_faculty():
    data = request.get_json()
    if Faculty.query.get(data['faculty_id']):
        return jsonify({"error": "Faculty ID already exists"}), 400

    new_faculty = Faculty(
        faculty_id = data['faculty_id'],
        username   = data['username'],
        email      = data['email'],
        contact    = data['contact']
    )
    db.session.add(new_faculty)
    db.session.commit()
    return jsonify({"message": "Faculty added successfully"}), 201

# EDIT a faculty
@registration_bp.route('/faculty/edit/<faculty_id>', methods=['PUT'])
def edit_faculty(faculty_id):
    faculty = Faculty.query.get(faculty_id)
    if not faculty:
        return jsonify({"error": "Faculty not found"}), 404

    data = request.get_json()
    faculty.username = data.get('username', faculty.username)
    faculty.email    = data.get('email',    faculty.email)
    faculty.contact  = data.get('contact',  faculty.contact)
    db.session.commit()
    return jsonify({"message": "Faculty updated successfully"})

# REMOVE a faculty
@registration_bp.route('/faculty/remove/<faculty_id>', methods=['DELETE'])
def remove_faculty(faculty_id):
    faculty = Faculty.query.get(faculty_id)
    if not faculty:
        return jsonify({"error": "Faculty not found"}), 404

    db.session.delete(faculty)
    db.session.commit()
    return jsonify({"message": "Faculty removed successfully"})

# LOGIN
@registration_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    faculty = Faculty.query.get(data['faculty_id'])
    if not faculty:
        return jsonify({"error": "Invalid Faculty ID"}), 401
    return jsonify({"message": "Login successful", "faculty": faculty.to_dict()})