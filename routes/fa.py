import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scheduler'))

from flask import Blueprint, request, jsonify
from config import db
from models.fa_entry import FAEntry
from models.faculty import Faculty
from schedule_generator import generate_schedule
from analytics.workload import analyze_faculty_workload

fa_bp = Blueprint('fa', __name__)

# Add FA entry
@fa_bp.route('/fa/add', methods=['POST'])
def add_fa():
    data = request.get_json()
    entry = FAEntry(
        year             = data['year'],
        specialization   = data['specialization'],
        section          = data['section'],
        student_count    = int(data['student_count']),
        faculty_advisor  = data['faculty_advisor'],
        academic_advisor = data['academic_advisor']
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({'message': 'FA entry added', 'entry': entry.to_dict()}), 201

# Get all FA entries
@fa_bp.route('/fa/all', methods=['GET'])
def get_all_fa():
    entries = FAEntry.query.all()
    return jsonify([e.to_dict() for e in entries])

# Delete FA entry
@fa_bp.route('/fa/delete/<int:id>', methods=['DELETE'])
def delete_fa(id):
    entry = FAEntry.query.get(id)
    if not entry:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

# Subject allocation sheet
@fa_bp.route('/allocation/sheet', methods=['GET'])
def allocation_sheet():
    schedule   = generate_schedule()
    workload   = analyze_faculty_workload(schedule)
    faculties  = Faculty.query.all()

    # Build subject map: name -> list of subjects
    subject_map = {}
    for entry in schedule:
        name = entry['faculty_name']
        subj = entry['subject']
        if name not in subject_map:
            subject_map[name] = []
        if subj not in subject_map[name]:
            subject_map[name].append(subj)

    result = []
    for i, f in enumerate(faculties, 1):
        name     = f.username
        subjects = subject_map.get(name, [])
        wl       = workload.get(name, {})
        result.append({
            'sno':        i,
            'faculty_id': f.faculty_id,
            'workload':   wl.get('total_classes', 0),
            'name':       name,
            'position':   'Faculty',
            'subject1':   subjects[0] if len(subjects) > 0 else '—',
            'subject2':   subjects[1] if len(subjects) > 1 else '—'
        })

    return jsonify(result)